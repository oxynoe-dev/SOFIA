#!/usr/bin/env python3
"""sanitize.py — Strip sensitive fields from analysis JSON before publication.

Usage:
    python sanitize.py <input_dir> <output_dir>

Reads records.json, mirror.json, lens.json, probe.json from <input_dir>.
Writes sanitized versions to <output_dir>.

What it strips:
- friction_records / contribution_records: removes 'description', 'source', 'source_type', 'ref'
- probe checks: removes 'detail' (contains filenames), keeps id + status
- probe exchange_matrix / friction_matrix: replaces non-persona keys with 'orchestrator'
- probe signals: removes (may contain filenames)
- meta.persona_roles: removes (contains real role descriptions)
- meta.context_sizes: removes contexte_files (contains filenames)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


KNOWN_PERSONAS = {
    # methodes
    "aurele", "solene", "emile", "garance",
    # produits
    "mira", "axel", "lea", "nora", "sofia",
    # oxynoe
    "alma", "livia", "marc", "winston",
    # generic
    "equipe", "team",
}

RECORD_STRIP_FIELDS = {"description", "source", "source_type", "ref", "is_amendment"}


# --- Wrapper handling ---
# JSON files may have two shapes:
#   Flat:    {"methodes": {...}, "produits": {...}}
#   Wrapped: {"instances": {"methodes": {...}, ...}, "default": "methodes", "all": {...}}
# The sanitizer functions work on instance dicts. This helper dispatches.

def sanitize_file(data: dict, instance_sanitizer) -> dict:
    """Apply instance_sanitizer to each instance in the data, handling both shapes."""
    if "instances" in data and isinstance(data["instances"], dict):
        # Wrapped shape
        out = {}
        out["instances"] = {
            name: instance_sanitizer(content)
            for name, content in data["instances"].items()
        }
        if "default" in data:
            out["default"] = data["default"]
        if "all" in data and isinstance(data["all"], dict):
            out["all"] = instance_sanitizer(data["all"])
        return out
    else:
        # Flat shape
        return {
            name: instance_sanitizer(content)
            for name, content in data.items()
            if isinstance(content, dict)
        }


# --- Per-instance sanitizers ---

def sanitize_records_instance(content: dict) -> dict:
    out = {}
    if "meta" in content:
        out["meta"] = sanitize_meta(content["meta"])
    if "friction_records" in content:
        out["friction_records"] = [strip_record(r) for r in content["friction_records"]]
    if "contribution_records" in content:
        out["contribution_records"] = [strip_record(r) for r in content["contribution_records"]]
    if "signaler_patterns" in content:
        out["signaler_patterns"] = content["signaler_patterns"]
    if "session_dates" in content:
        out["session_dates"] = content["session_dates"]
    return out


def sanitize_mirror_instance(content: dict) -> dict:
    out = {}
    if "meta" in content:
        out["meta"] = sanitize_meta(content["meta"])
    if "friction_records" in content:
        out["friction_records"] = [strip_record(r) for r in content["friction_records"]]
    if "personas" in content:
        out["personas"] = {
            persona: sanitize_persona_view(pdata)
            for persona, pdata in content["personas"].items()
        }
    if "map" in content:
        out["map"] = strip_descriptions(content["map"])
    for key in ("trajectory", "radars"):
        if key in content:
            out[key] = content[key]
    return out


def sanitize_lens_instance(content: dict) -> dict:
    out = {}
    if "meta" in content:
        out["meta"] = sanitize_meta(content["meta"])
    for key in ("totals", "time_series", "personas"):
        if key in content:
            out[key] = content[key]
    return out


def sanitize_probe_instance(content: dict) -> dict:
    out = {}
    if "meta" in content:
        out["meta"] = sanitize_meta(content["meta"])
    if "structure" in content and "checks" in content["structure"]:
        out["structure"] = {
            "checks": [
                {"id": c["id"], "status": c["status"]}
                for c in content["structure"]["checks"]
            ]
        }
    if "context_sizes" in content:
        out["context_sizes"] = {
            persona: {
                "total_lines": cs.get("total_lines"),
                "status": cs.get("status"),
            }
            for persona, cs in content["context_sizes"].items()
        }
    for matrix_key in ("exchange_matrix", "friction_matrix"):
        if matrix_key in content:
            out[matrix_key] = anonymize_matrix(content[matrix_key])
    for key in ("friction_po", "activite"):
        if key in content:
            out[key] = content[key]
    for key in ("echanges", "friction"):
        if key in content and isinstance(content[key], dict):
            section = content[key]
            if "matrix" in section:
                out[key] = {
                    k: (anonymize_matrix(v) if k == "matrix" else v)
                    for k, v in section.items()
                }
            else:
                out[key] = anonymize_matrix(section)
        elif key in content:
            out[key] = content[key]
    return out


# --- Top-level sanitizers (called by main / build_dist) ---

def sanitize_records(data: dict) -> dict:
    return sanitize_file(data, sanitize_records_instance)

def sanitize_mirror(data: dict) -> dict:
    return sanitize_file(data, sanitize_mirror_instance)

def sanitize_lens(data: dict) -> dict:
    return sanitize_file(data, sanitize_lens_instance)

def sanitize_probe(data: dict) -> dict:
    return sanitize_file(data, sanitize_probe_instance)


# --- Helpers ---

def strip_record(rec: dict) -> dict:
    return {k: v for k, v in rec.items() if k not in RECORD_STRIP_FIELDS}


def sanitize_persona_view(pdata: dict) -> dict:
    out = {}
    for k, v in pdata.items():
        if k in ("friction_records", "contribution_records"):
            out[k] = [strip_record(r) for r in v]
        else:
            out[k] = v
    return out


def sanitize_meta(meta: dict) -> dict:
    out = {}
    for k, v in meta.items():
        if k == "persona_roles":
            continue
        elif k == "context_sizes":
            out[k] = {
                persona: {
                    "total_lines": cs.get("total_lines"),
                    "status": cs.get("status"),
                }
                for persona, cs in v.items()
            }
        else:
            out[k] = v
    return out


def strip_descriptions(obj):
    if isinstance(obj, dict):
        return {k: strip_descriptions(v) for k, v in obj.items() if k != "description"}
    elif isinstance(obj, list):
        return [strip_descriptions(item) for item in obj]
    return obj


def anonymize_matrix(matrix: dict) -> dict:
    out = {}
    for sender, targets in matrix.items():
        clean_sender = sender if sender in KNOWN_PERSONAS else "orchestrator"
        if clean_sender not in out:
            out[clean_sender] = {}
        for target, count in targets.items():
            clean_target = target if target in KNOWN_PERSONAS else "orchestrator"
            out[clean_sender][clean_target] = out[clean_sender].get(clean_target, 0) + count
    return out


def main():
    parser = argparse.ArgumentParser(description="Sanitize analysis JSON for publication")
    parser.add_argument("input_dir", type=Path, help="Directory with raw JSON (analysis/data/)")
    parser.add_argument("output_dir", type=Path, help="Directory for sanitized JSON")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    sanitizers = {
        "records.json": sanitize_records,
        "mirror.json": sanitize_mirror,
        "lens.json": sanitize_lens,
        "probe.json": sanitize_probe,
    }

    for filename, sanitizer in sanitizers.items():
        input_path = args.input_dir / filename
        if not input_path.exists():
            print(f"  skip {filename} (not found)")
            continue
        with open(input_path) as f:
            data = json.load(f)
        sanitized = sanitizer(data)
        output_path = args.output_dir / filename
        with open(output_path, "w") as f:
            json.dump(sanitized, f, indent=2, ensure_ascii=False)
        print(f"  {filename} → {output_path}")

    print("done")


if __name__ == "__main__":
    main()
