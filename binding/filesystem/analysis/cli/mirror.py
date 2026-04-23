"""mirror.py — Produce mirror.json from records.json.

Aggregates friction records into:
- Trajectory (challenge % over time)
- Radar (5 axes per persona)
- KPI (friction density, resolution rate)
- Failure modes (5 tribology-based indicators)
- Map (persona cards, links)

Calls scan.py internally if records.json is absent or stale.
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from analysis.lib.constants import FRICTION_MARKERS, RESOLUTION_TAGS, DIRECTION_KEYS, strip_accents
from analysis.lib.parser import parse_frontmatter, date_to_week


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def ensure_records(instance_paths: list[Path] | None = None) -> dict:
    """Load records.json, regenerating via scan.py if needed."""
    records_path = DATA_DIR / "records.json"
    if records_path.is_file():
        return json.loads(records_path.read_text(encoding="utf-8"))

    if not instance_paths:
        raise FileNotFoundError("records.json not found and no instance paths provided")

    from analysis.cli.scan import scan_instances, write_records
    records = scan_instances(instance_paths)
    write_records(records, records_path)
    return records


def build_mirror(records: dict) -> dict:
    """Build mirror.json content from scan records."""
    result = {"instances": {}}

    for inst_name, inst_data in records.items():
        friction_records = inst_data.get("friction_records", [])
        contrib_records = inst_data.get("contribution_records", [])
        sp_records = inst_data.get("signaler_patterns", [])
        personas = inst_data.get("meta", {}).get("personas", [])

        # --- Per-persona aggregation ---
        by_persona = defaultdict(lambda: {
            "markers": defaultdict(int),
            "resolutions": defaultdict(int),
            "directions": defaultdict(int),
            "frictions": 0, "sessions_frictions": 0, "artifact_frictions": 0,
            "flux_h": 0, "flux_a": 0,
            "flux_types_h": defaultdict(int),
            "flux_types_a": defaultdict(int),
        })

        # Count sessions per persona (from friction sources)
        sessions_per_persona = defaultdict(set)
        for r in friction_records:
            p = r["persona"]
            by_persona[p]["markers"][r["marker"]] += 1
            by_persona[p]["resolutions"][r.get("resolution", "none")] += 1
            by_persona[p]["directions"][r["direction"]] += 1
            by_persona[p]["frictions"] += 1
            if r["source_type"] == "session":
                by_persona[p]["sessions_frictions"] += 1
                sessions_per_persona[p].add(r["source"])
            else:
                by_persona[p]["artifact_frictions"] += 1

        for r in contrib_records:
            p = r["persona"]
            ctype = r.get("type", "substance")
            if r["direction"] == "H":
                by_persona[p]["flux_h"] += 1
                by_persona[p]["flux_types_h"][ctype] += 1
            else:
                by_persona[p]["flux_a"] += 1
                by_persona[p]["flux_types_a"][ctype] += 1

        # --- Trajectory (challenge % by week) ---
        by_week = defaultdict(lambda: {"total": 0, "challenge": 0})
        for r in friction_records:
            if r.get("is_amendment"):
                continue
            w = r.get("week", "unknown")
            by_week[w]["total"] += 1
            if r["marker"] != "sound":
                by_week[w]["challenge"] += 1

        sorted_weeks = sorted(by_week.keys())
        trajectory = {
            "labels": sorted_weeks,
            "challenge_pct": [
                round(by_week[w]["challenge"] / max(by_week[w]["total"], 1) * 100, 1)
                for w in sorted_weeks
            ],
            "density": [by_week[w]["total"] for w in sorted_weeks],
        }

        # --- Radar (5 axes per persona) ---
        radars = {}
        for p in personas:
            d = by_persona.get(p, {})
            total_f = d.get("frictions", 0)
            markers = d.get("markers", {})
            resolutions = d.get("resolutions", {})
            directions = d.get("directions", {})

            # Diversity: how many different marker types used (0-100, 5 = 100)
            types_used = sum(1 for v in markers.values() if v > 0)
            diversity = round(types_used / 5 * 100) if total_f > 0 else 0

            # Challenge: % non-sound
            non_sound = total_f - markers.get("sound", 0)
            challenge = round(non_sound / max(total_f, 1) * 100) if total_f > 0 else 0

            # Resolution: % resolved
            resolved = sum(v for k, v in resolutions.items() if k in RESOLUTION_TAGS)
            resolution = round(resolved / max(total_f, 1) * 100) if total_f > 0 else 0

            # Coverage: sessions with friction / total sessions
            sess_count = len(sessions_per_persona.get(p, set()))
            total_sess = inst_data["meta"].get("sessions_scanned", 0)
            coverage = round(sess_count / max(total_sess, 1) * 100)

            # Contribution: A contributions / total flux
            flux_total = d.get("flux_h", 0) + d.get("flux_a", 0)
            contribution = round(d.get("flux_a", 0) / max(flux_total, 1) * 100) if flux_total > 0 else 0

            radars[p] = {
                "diversity": diversity,
                "challenge": challenge,
                "resolution": resolution,
                "coverage": coverage,
                "contribution": contribution,
            }

        # --- KPI ---
        total_frictions = len([r for r in friction_records if not r.get("is_amendment")])
        total_resolved = sum(1 for r in friction_records if r.get("resolution") in RESOLUTION_TAGS and not r.get("is_amendment"))
        total_sessions = inst_data["meta"].get("sessions_scanned", 0)
        challenge_count = sum(1 for r in friction_records if r["marker"] != "sound" and not r.get("is_amendment"))

        kpi = {
            "friction_density": round(total_frictions / max(total_sessions, 1), 1),
            "resolution_rate": round(total_resolved / max(total_frictions, 1) * 100),
            "challenge_pct": round(challenge_count / max(total_frictions, 1) * 100),
            "total_frictions": total_frictions,
            "total_sessions": total_sessions,
        }

        # --- Map cards ---
        map_cards = {}
        for p in personas:
            d = by_persona.get(p, {})
            map_cards[p] = {
                "frictions": d.get("frictions", 0),
                "sessions": len(sessions_per_persona.get(p, set())),
            }

        # --- Open frictions (no resolution) ---
        open_frictions = [
            {"persona": r["persona"], "date": r["date"], "marker": r["marker"],
             "description": r.get("description", "")[:80], "source": r["source"]}
            for r in friction_records
            if not r.get("resolution") and not r.get("is_amendment")
        ]

        # --- Map topology ---
        persona_roles = inst_data["meta"].get("persona_roles", {})
        context_sizes = inst_data["meta"].get("context_sizes", {})
        links = []
        for p in personas:
            d = by_persona.get(p, {})
            total = d.get("frictions", 0)
            if total > 0:
                links.append({"persona": p, "total": total})

        map_data = {
            "persona_roles": persona_roles,
            "links": links,
            "context_sizes": context_sizes,
            "description": "",
        }

        # --- Per-persona data for client-side rendering ---
        personas_data = {}
        for p in personas:
            d = by_persona.get(p, {})
            personas_data[p] = {
                "flux_h": d.get("flux_h", 0),
                "flux_a": d.get("flux_a", 0),
                "flux_types_h": dict(d.get("flux_types_h", defaultdict(int))),
                "flux_types_a": dict(d.get("flux_types_a", defaultdict(int))),
            }

        # --- Failure modes (5 tribology indicators) ---
        failure_modes = compute_failure_modes(
            friction_records, trajectory, kpi, by_week, by_persona, personas
        )

        result["instances"][inst_name] = {
            "meta": inst_data["meta"],
            "friction_records": friction_records,
            "personas": personas_data,
            "map": map_data,
            "trajectory": trajectory,
            "radars": radars,
            "kpi": kpi,
            "failure_modes": failure_modes,
            "map_cards": map_cards,
            "open_frictions": open_frictions[-20:],  # last 20
        }

    if result["instances"]:
        result["default"] = next(iter(result["instances"]))

    # ── Cross-instance aggregation ──
    if len(result["instances"]) > 1:
        all_friction = []
        all_personas_data = {}
        all_map = {}
        all_personas_set = set()
        for inst_name, inst_data in records.items():
            all_friction.extend(inst_data.get("friction_records", []))
            all_personas_set.update(inst_data.get("meta", {}).get("personas", []))
            # Build map per instance
            if inst_name in result["instances"]:
                all_map[inst_name] = result["instances"][inst_name]["map"]
        # Merge personas flux
        all_contrib = []
        for inst_data in records.values():
            all_contrib.extend(inst_data.get("contribution_records", []))
        by_p = defaultdict(lambda: {"flux_h": 0, "flux_a": 0, "flux_types_h": defaultdict(int), "flux_types_a": defaultdict(int)})
        for r in all_contrib:
            p = r["persona"]
            ctype = r.get("type", "substance")
            if r["direction"] == "H":
                by_p[p]["flux_h"] += 1
                by_p[p]["flux_types_h"][ctype] += 1
            else:
                by_p[p]["flux_a"] += 1
                by_p[p]["flux_types_a"][ctype] += 1
        sorted_personas = sorted(all_personas_set)
        for p in sorted_personas:
            d = by_p.get(p, {})
            all_personas_data[p] = {
                "flux_h": d.get("flux_h", 0),
                "flux_a": d.get("flux_a", 0),
                "flux_types_h": dict(d.get("flux_types_h", defaultdict(int))),
                "flux_types_a": dict(d.get("flux_types_a", defaultdict(int))),
            }
        # Compute trajectory, KPI, failure_modes for "all"
        all_records_clean = [r for r in all_friction if not r.get("is_amendment")]
        all_by_week = defaultdict(lambda: {"total": 0, "challenge": 0})
        for r in all_records_clean:
            w = r.get("week", "unknown")
            all_by_week[w]["total"] += 1
            if r["marker"] != "sound":
                all_by_week[w]["challenge"] += 1
        all_sorted_weeks = sorted(all_by_week.keys())
        all_trajectory = {
            "labels": all_sorted_weeks,
            "challenge_pct": [
                round(all_by_week[w]["challenge"] / max(all_by_week[w]["total"], 1) * 100, 1)
                for w in all_sorted_weeks
            ],
            "density": [all_by_week[w]["total"] for w in all_sorted_weeks],
        }
        all_total_frictions = len(all_records_clean)
        all_total_resolved = sum(1 for r in all_records_clean if r.get("resolution") in RESOLUTION_TAGS)
        all_total_sessions = sum(d["meta"].get("sessions_scanned", 0) for d in records.values())
        all_challenge_count = sum(1 for r in all_records_clean if r["marker"] != "sound")
        all_kpi = {
            "friction_density": round(all_total_frictions / max(all_total_sessions, 1), 1),
            "resolution_rate": round(all_total_resolved / max(all_total_frictions, 1) * 100),
            "challenge_pct": round(all_challenge_count / max(all_total_frictions, 1) * 100),
            "total_frictions": all_total_frictions,
            "total_sessions": all_total_sessions,
        }
        # Per-persona aggregation for failure modes
        all_by_persona = defaultdict(lambda: {
            "markers": defaultdict(int), "resolutions": defaultdict(int),
            "directions": defaultdict(int), "frictions": 0,
        })
        for r in all_friction:
            p = r["persona"]
            all_by_persona[p]["markers"][r["marker"]] += 1
            all_by_persona[p]["resolutions"][r.get("resolution", "none")] += 1
            all_by_persona[p]["directions"][r["direction"]] += 1
            all_by_persona[p]["frictions"] += 1
        all_failure_modes = compute_failure_modes(
            all_friction, all_trajectory, all_kpi, all_by_week, all_by_persona, sorted_personas
        )

        result["all"] = {
            "meta": {
                "instance": "all",
                "date": next(iter(records.values()))["meta"]["date"],
                "personas": sorted_personas,
            },
            "friction_records": all_friction,
            "personas": all_personas_data,
            "map": {"instances": all_map},
            "trajectory": all_trajectory,
            "kpi": all_kpi,
            "failure_modes": all_failure_modes,
        }

    return result


# ── Failure mode helpers ──────────────────────────────────────────────


def _marker_entropy(counts: dict) -> float:
    """Shannon entropy of marker distribution. Max ~2.32 for 5 equiprobable markers."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    probs = [c / total for c in counts.values() if c > 0]
    return -sum(p * math.log2(p) for p in probs)


def _slope(values: list[float]) -> float:
    """Simple linear regression slope (least squares). Returns 0.0 if < 2 points."""
    n = len(values)
    if n < 2:
        return 0.0
    x_mean = (n - 1) / 2
    y_mean = sum(values) / n
    num = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
    den = sum((i - x_mean) ** 2 for i in range(n))
    return num / den if den != 0 else 0.0


def _trend(values: list[float], min_points: int = 3, threshold: float = 0.5) -> str:
    """Classify trend as descending/stable/ascending/insufficient_data."""
    if len(values) < min_points:
        return "insufficient_data"
    s = _slope(values)
    if s < -threshold:
        return "descending"
    if s > threshold:
        return "ascending"
    return "stable"


def compute_failure_modes(
    friction_records: list[dict],
    trajectory: dict,
    kpi: dict,
    by_week: dict,
    by_persona: dict,
    personas: list[str],
) -> dict:
    """Compute 5 instrumented failure mode indicators from friction data.

    Modes (tribology vocabulary):
    - glissement (slip): friction not arbitrated
    - usure (wear): friction smoothed out over time
    - ecrasement (crush): friction forced out by one side
    - asymetrie (asymmetry): friction flows one way only
    - instabilite (instability): no convergence, stick-slip
    """
    # Filter out amendments for all computations
    records = [r for r in friction_records if not r.get("is_amendment")]
    total = len(records)

    # ── Glissement ──
    unresolved = sum(1 for r in records if not r.get("resolution"))
    non_resolution_rate = round(unresolved / max(total, 1) * 100, 1)

    # Recurrence: same persona + same marker without resolution, 3+ times
    recurrence_key = defaultdict(int)
    for r in records:
        if not r.get("resolution"):
            recurrence_key[(r["persona"], r["marker"])] += 1
    recurrence_count = sum(1 for v in recurrence_key.values() if v >= 3)

    # Reflexive ratification: ratified / total resolutions
    total_resolved = sum(1 for r in records if r.get("resolution") in RESOLUTION_TAGS)
    ratified_count = sum(1 for r in records if r.get("resolution") == "ratified")
    reflexive_ratification = round(ratified_count / max(total_resolved, 1) * 100, 1)

    # Cross-signal: non_resolution > 60% AND density stable
    density_values = trajectory.get("density", [])
    density_trend = _trend([float(d) for d in density_values])
    glissement_cross = non_resolution_rate > 60 and density_trend == "stable"

    glissement_level = "ok"
    if non_resolution_rate > 60:
        glissement_level = "alert" if glissement_cross else "signal"
    elif reflexive_ratification > 90 and kpi.get("challenge_pct", 0) > 20:
        glissement_level = "signal"

    # ── Usure ──
    challenge_values = trajectory.get("challenge_pct", [])
    challenge_trend = _trend(challenge_values)

    # Refuted count in recent weeks (last 4)
    sorted_weeks = sorted(by_week.keys())
    recent_weeks = set(sorted_weeks[-4:]) if len(sorted_weeks) >= 4 else set(sorted_weeks)
    refuted_recent = sum(
        1 for r in records
        if r["marker"] == "refuted" and r.get("week") in recent_weeks
    )

    # Marker entropy per week, trend
    entropy_per_week = []
    week_markers = defaultdict(lambda: defaultdict(int))
    for r in records:
        week_markers[r.get("week", "unknown")][r["marker"]] += 1
    for w in sorted_weeks:
        entropy_per_week.append(_marker_entropy(dict(week_markers[w])))
    entropy_trend = _trend(entropy_per_week)

    # Delta baseline/recent challenge %
    if len(challenge_values) >= 4:
        half = len(challenge_values) // 2
        baseline_avg = sum(challenge_values[:half]) / max(half, 1)
        recent_avg = sum(challenge_values[half:]) / max(len(challenge_values) - half, 1)
        delta_baseline_recent = round(recent_avg / max(baseline_avg, 0.1) * 100, 1)
    else:
        delta_baseline_recent = 100.0  # not enough data

    # Cross-signal
    usure_cross = None
    if challenge_trend == "descending" and total >= 10:
        # Check coverage trend
        coverage_values = []
        for w in sorted_weeks:
            week_personas = set(r["persona"] for r in records if r.get("week") == w)
            coverage_values.append(len(week_personas))
        coverage_trend = _trend([float(c) for c in coverage_values])
        if coverage_trend in ("stable", "ascending"):
            usure_cross = "usure"
        elif coverage_trend == "descending":
            usure_cross = "desengagement"

    usure_level = "ok"
    if total < 10 or len(sorted_weeks) < 3:
        usure_level = "ok"  # insufficient data
    elif challenge_trend == "descending" and delta_baseline_recent < 50:
        usure_level = "alert"
    elif challenge_trend == "descending" or (refuted_recent == 0 and len(recent_weeks) >= 4):
        usure_level = "signal"

    # ── Ecrasement ──
    rejected_count = sum(1 for r in records if r.get("resolution") == "rejected")
    revised_count = sum(1 for r in records if r.get("resolution") == "revised")
    rejection_rate = round(rejected_count / max(total_resolved, 1) * 100, 1)
    revised_rate = round(revised_count / max(total_resolved, 1) * 100, 1)

    # Density ratio: recent / baseline
    if len(density_values) >= 4:
        half = len(density_values) // 2
        baseline_density = sum(density_values[:half]) / max(half, 1)
        recent_density = sum(density_values[half:]) / max(len(density_values) - half, 1)
        density_ratio = round(recent_density / max(baseline_density, 0.1), 1)
    else:
        density_ratio = 1.0

    # Direction for cross-signal
    a_contests = sum(1 for r in records if r["direction"] == "a_contests_h")
    h_contests = sum(1 for r in records if r["direction"] == "h_contests_a")
    ecrasement_dir = None
    if rejection_rate > 50:
        if h_contests > a_contests:
            ecrasement_dir = "h_crushes_a"
        elif a_contests > h_contests:
            ecrasement_dir = "a_crushes_h"

    ecrasement_level = "ok"
    if rejection_rate > 50:
        ecrasement_level = "alert"
    elif density_ratio > 2.0 and revised_rate < 10:
        ecrasement_level = "signal"

    # ── Asymetrie ──
    a_total = sum(1 for r in records if r["direction"] in ("a_contests_h", "a_corroborates_h"))
    h_total = sum(1 for r in records if r["direction"] in ("h_contests_a", "h_corroborates_a"))
    total_dir = a_total + h_total
    direction_ratio = round(a_total / max(total_dir, 1) * 100, 1)

    per_persona_ratio = {}
    for p in personas:
        p_records = [r for r in records if r["persona"] == p]
        p_a = sum(1 for r in p_records if r["direction"] in ("a_contests_h", "a_corroborates_h"))
        p_h = sum(1 for r in p_records if r["direction"] in ("h_contests_a", "h_corroborates_a"))
        p_total = p_a + p_h
        per_persona_ratio[p] = round(p_a / max(p_total, 1) * 100, 1) if p_total > 0 else None

    asymetrie_level = "ok"
    if total >= 5:
        if direction_ratio == 0 or direction_ratio == 100:
            asymetrie_level = "alert"
        elif direction_ratio < 10 or direction_ratio > 90:
            asymetrie_level = "signal"

    # ── Instabilite ──
    # Count windows where revised > 80% of resolutions
    revised_dominant_windows = 0
    for w in sorted_weeks:
        w_records = [r for r in records if r.get("week") == w]
        w_resolved = sum(1 for r in w_records if r.get("resolution") in RESOLUTION_TAGS)
        w_revised = sum(1 for r in w_records if r.get("resolution") == "revised")
        if w_resolved >= 3 and w_revised / max(w_resolved, 1) > 0.8:
            revised_dominant_windows += 1

    revised_rate_recent = 0.0
    if recent_weeks:
        recent_resolved = sum(1 for r in records if r.get("week") in recent_weeks and r.get("resolution") in RESOLUTION_TAGS)
        recent_revised = sum(1 for r in records if r.get("week") in recent_weeks and r.get("resolution") == "revised")
        revised_rate_recent = round(recent_revised / max(recent_resolved, 1) * 100, 1)

    # Recontestation chains via ref field
    refs = [r.get("ref") for r in records if r.get("ref") and r.get("resolution") == "revised"]
    recontestation_chains = 0
    # Simple: count ref chains of depth 3+
    ref_targets = defaultdict(int)
    for ref in refs:
        ref_targets[ref] += 1
    recontestation_chains = sum(1 for v in ref_targets.values() if v >= 3)

    instabilite_level = "ok"
    if revised_dominant_windows >= 3:
        instabilite_level = "alert"
    elif revised_dominant_windows >= 1 and revised_rate_recent > 80:
        instabilite_level = "signal"

    # ── Per-persona diagnostics (non-exclusive) ──
    N_PERSONA = 25  # window size for baseline/recent per persona
    persona_diagnostics = {}
    for p in personas:
        p_recs = [r for r in records if r["persona"] == p]
        p_total = len(p_recs)
        modes = []

        if p_total < 3:
            persona_diagnostics[p] = {"modes": [], "dominant": "healthy"}
            continue

        # Glissement: non-resolution per persona
        p_unresolved = sum(1 for r in p_recs if not r.get("resolution"))
        p_non_res_rate = p_unresolved / max(p_total, 1) * 100
        p_resolved = sum(1 for r in p_recs if r.get("resolution") in RESOLUTION_TAGS)
        p_ratified = sum(1 for r in p_recs if r.get("resolution") == "ratified")
        p_ratif_rate = p_ratified / max(p_resolved, 1) * 100
        if p_non_res_rate > 60:
            modes.append(("glissement", "alert" if density_trend == "stable" else "signal"))
        elif p_ratif_rate > 90 and p_total >= 5:
            p_challenge = sum(1 for r in p_recs if r["marker"] != "sound")
            if p_challenge / max(p_total, 1) * 100 > 20:
                modes.append(("glissement", "signal"))

        # Usure: challenge % descending per persona
        if p_total >= N_PERSONA:
            baseline_recs = p_recs[:N_PERSONA]
            recent_recs = p_recs[-N_PERSONA:]
            bl_challenge = sum(1 for r in baseline_recs if r["marker"] != "sound") / len(baseline_recs) * 100
            rc_challenge = sum(1 for r in recent_recs if r["marker"] != "sound") / len(recent_recs) * 100
            if bl_challenge > 10 and rc_challenge <= bl_challenge * 0.5:
                modes.append(("usure", "alert" if rc_challenge < bl_challenge * 0.25 else "signal"))
        elif p_total >= 5:
            p_all_sound = all(r["marker"] == "sound" for r in p_recs)
            if p_all_sound:
                modes.append(("usure", "signal"))

        # Ecrasement: high rejection or A→H = 0 (persona never contests back)
        p_rejected = sum(1 for r in p_recs if r.get("resolution") == "rejected")
        p_rejection_rate = p_rejected / max(p_resolved, 1) * 100
        if p_rejection_rate > 50 and p_resolved >= 3:
            modes.append(("ecrasement", "alert"))
        else:
            p_a_contests = sum(1 for r in p_recs if r["direction"] == "a_contests_h")
            if p_total >= 10 and p_a_contests == 0:
                modes.append(("ecrasement", "signal"))

        # Asymetrie: direction ratio extreme per persona
        p_a = sum(1 for r in p_recs if r["direction"] in ("a_contests_h", "a_corroborates_h"))
        p_h = sum(1 for r in p_recs if r["direction"] in ("h_contests_a", "h_corroborates_a"))
        p_dir_total = p_a + p_h
        if p_dir_total >= 5:
            p_dir_ratio = p_a / p_dir_total * 100
            if p_dir_ratio == 0 or p_dir_ratio == 100:
                modes.append(("asymetrie", "alert"))
            elif p_dir_ratio < 20 or p_dir_ratio > 80:
                modes.append(("asymetrie", "signal"))

        # Instabilite: revised dominant per persona
        p_revised = sum(1 for r in p_recs if r.get("resolution") == "revised")
        p_revised_rate = p_revised / max(p_resolved, 1) * 100
        if p_resolved >= 5 and p_revised_rate > 80:
            modes.append(("instabilite", "alert" if p_revised_rate > 90 else "signal"))

        # Dominant = most severe mode
        dominant = "healthy"
        if modes:
            alert_modes = [m for m, l in modes if l == "alert"]
            dominant = alert_modes[0] if alert_modes else modes[0][0]

        persona_diagnostics[p] = {
            "modes": [{"mode": m, "level": l} for m, l in modes],
            "dominant": dominant,
        }

    return {
        "per_persona": persona_diagnostics,
        "glissement": {
            "level": glissement_level,
            "non_resolution_rate": non_resolution_rate,
            "recurrence_count": recurrence_count,
            "reflexive_ratification": reflexive_ratification,
            "cross_signal": glissement_cross,
        },
        "usure": {
            "level": usure_level,
            "challenge_pct_trend": challenge_trend,
            "refuted_count_recent": refuted_recent,
            "marker_entropy_trend": entropy_trend,
            "delta_baseline_recent": delta_baseline_recent,
            "cross_signal": usure_cross,
        },
        "ecrasement": {
            "level": ecrasement_level,
            "density_ratio": density_ratio,
            "revised_rate": revised_rate,
            "rejection_rate": rejection_rate,
            "direction": ecrasement_dir,
        },
        "asymetrie": {
            "level": asymetrie_level,
            "direction_ratio": direction_ratio,
            "per_persona": per_persona_ratio,
        },
        "instabilite": {
            "level": instabilite_level,
            "revised_rate_recent": revised_rate_recent,
            "revised_dominant_windows": revised_dominant_windows,
            "recontestation_chains": recontestation_chains,
        },
    }


def write_mirror(mirror_data: dict, output_path: Path | None = None):
    """Write mirror.json."""
    if output_path is None:
        output_path = DATA_DIR / "mirror.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(mirror_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build mirror.json from records")
    parser.add_argument("instances", nargs="*", help="Instance paths (triggers scan if records.json absent)")
    args = parser.parse_args()

    paths = [Path(p).resolve() for p in args.instances] if args.instances else None
    records = ensure_records(paths)
    mirror = build_mirror(records)
    write_mirror(mirror)
    print(f"✓ mirror.json — {len(mirror['instances'])} instances")
