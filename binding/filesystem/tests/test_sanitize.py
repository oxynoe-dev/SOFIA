"""T2 — Sanitize tests.

Verify sensitive fields are stripped, non-sensitive fields preserved.
Pure functions: dict in → dict out, no file I/O.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sanitize import (
    sanitize_records, sanitize_mirror, sanitize_lens, sanitize_probe,
    strip_record, sanitize_meta, anonymize_matrix,
)


SAMPLE_FRICTION = {
    "persona": "alice",
    "date": "2026-04-10",
    "week": "2026-W15",
    "marker": "contestable",
    "initiative": "PO",
    "direction": "h_contests_a",
    "resolution": "ratified",
    "description": "Alice proposed X but it conflicts with Y",
    "source": "2026-04-10-alice.md",
    "source_type": "session",
    "ref": "s3/2",
    "is_amendment": True,
}

SAMPLE_CONTRIBUTION = {
    "persona": "alice",
    "date": "2026-04-10",
    "direction": "A",
    "type": "substance",
    "description": "Provided analysis of Z",
    "source": "2026-04-10-alice.md",
    "source_type": "session",
}


class TestStripRecord(unittest.TestCase):

    def test_strips_sensitive_fields(self):
        result = strip_record(SAMPLE_FRICTION)
        for field in ("description", "source", "source_type", "ref", "is_amendment"):
            self.assertNotIn(field, result)

    def test_preserves_non_sensitive_fields(self):
        result = strip_record(SAMPLE_FRICTION)
        for field in ("persona", "date", "week", "marker", "initiative", "direction", "resolution"):
            self.assertIn(field, result)
            self.assertEqual(result[field], SAMPLE_FRICTION[field])


class TestSanitizeMeta(unittest.TestCase):

    def test_strips_persona_roles(self):
        meta = {
            "instance": "test",
            "personas": ["alice", "bob"],
            "persona_roles": {"alice": "Architect", "bob": "Developer"},
        }
        result = sanitize_meta(meta)
        self.assertNotIn("persona_roles", result)
        self.assertIn("personas", result)

    def test_strips_contexte_files_from_context_sizes(self):
        meta = {
            "instance": "test",
            "context_sizes": {
                "alice": {"total_lines": 180, "status": "warn", "contexte_files": ["ctx-alice.md"]},
            },
        }
        result = sanitize_meta(meta)
        self.assertNotIn("contexte_files", result["context_sizes"]["alice"])
        self.assertEqual(result["context_sizes"]["alice"]["total_lines"], 180)


class TestAnonymizeMatrix(unittest.TestCase):

    def test_preserves_known_personas(self):
        matrix = {"alice": {"bob": 3}, "bob": {"alice": 1}}
        # alice and bob are not in KNOWN_PERSONAS but let's test with known ones
        from sanitize import KNOWN_PERSONAS
        known = list(KNOWN_PERSONAS)[:2]
        matrix = {known[0]: {known[1]: 5}}
        result = anonymize_matrix(matrix)
        self.assertIn(known[0], result)
        self.assertIn(known[1], result[known[0]])

    def test_anonymizes_unknown_keys(self):
        matrix = {"olivier": {"alice": 3}}
        result = anonymize_matrix(matrix)
        self.assertIn("orchestrator", result)
        self.assertNotIn("olivier", result)


class TestSanitizeRecords(unittest.TestCase):

    def test_wrapped_shape(self):
        data = {
            "instances": {
                "test": {
                    "meta": {"instance": "test", "personas": ["alice"]},
                    "friction_records": [SAMPLE_FRICTION],
                    "contribution_records": [SAMPLE_CONTRIBUTION],
                },
            },
            "default": "test",
        }
        result = sanitize_records(data)
        rec = result["instances"]["test"]["friction_records"][0]
        self.assertNotIn("description", rec)
        self.assertIn("marker", rec)

    def test_flat_shape(self):
        data = {
            "test": {
                "meta": {"instance": "test", "personas": ["alice"]},
                "friction_records": [SAMPLE_FRICTION],
                "contribution_records": [SAMPLE_CONTRIBUTION],
            },
        }
        result = sanitize_records(data)
        rec = result["test"]["friction_records"][0]
        self.assertNotIn("description", rec)

    def test_preserves_signaler_patterns(self):
        data = {
            "instances": {
                "test": {
                    "meta": {"instance": "test", "personas": ["alice"]},
                    "friction_records": [],
                    "contribution_records": [],
                    "signaler_patterns": [{"persona": "alice", "choix": "conviction"}],
                },
            },
        }
        result = sanitize_records(data)
        self.assertEqual(len(result["instances"]["test"]["signaler_patterns"]), 1)


class TestSanitizeMirror(unittest.TestCase):

    def test_strips_friction_descriptions(self):
        data = {
            "instances": {
                "test": {
                    "meta": {"instance": "test", "personas": ["alice"]},
                    "friction_records": [SAMPLE_FRICTION],
                    "personas": {},
                    "trajectory": {"labels": ["w1"], "challenge_pct": [30]},
                    "radars": {"alice": {"challenge": 50}},
                },
            },
        }
        result = sanitize_mirror(data)
        rec = result["instances"]["test"]["friction_records"][0]
        self.assertNotIn("description", rec)

    def test_preserves_trajectory_and_radars(self):
        data = {
            "instances": {
                "test": {
                    "meta": {"instance": "test", "personas": ["alice"]},
                    "friction_records": [],
                    "personas": {},
                    "trajectory": {"labels": ["w1"], "challenge_pct": [30]},
                    "radars": {"alice": {"challenge": 50}},
                },
            },
        }
        result = sanitize_mirror(data)
        self.assertEqual(result["instances"]["test"]["trajectory"]["challenge_pct"], [30])
        self.assertEqual(result["instances"]["test"]["radars"]["alice"]["challenge"], 50)

    def test_handles_all_key(self):
        data = {
            "instances": {"test": {"meta": {"instance": "test"}, "friction_records": [SAMPLE_FRICTION], "personas": {}}},
            "all": {"meta": {"instance": "all"}, "friction_records": [SAMPLE_FRICTION], "personas": {}},
        }
        result = sanitize_mirror(data)
        self.assertIn("all", result)
        self.assertNotIn("description", result["all"]["friction_records"][0])


class TestSanitizeLens(unittest.TestCase):

    def test_preserves_time_series(self):
        data = {
            "instances": {
                "test": {
                    "meta": {"instance": "test", "personas": ["alice"]},
                    "totals": {"signaler_pattern": 0},
                    "time_series": {"week": {"labels": ["2026-W15"], "markers": {"sound": [5]}}},
                    "personas": {"alice": {"frictions": 10}},
                },
            },
        }
        result = sanitize_lens(data)
        self.assertEqual(result["instances"]["test"]["time_series"]["week"]["labels"], ["2026-W15"])


class TestSanitizeProbe(unittest.TestCase):

    def test_strips_check_details(self):
        data = {
            "test": {
                "meta": {"instance": "test"},
                "structure": {
                    "checks": [
                        {"id": "PS1", "status": "pass", "detail": "sofia.md found at /path/to/file"},
                        {"id": "PA1", "status": "warn", "detail": "2 artifacts missing frontmatter"},
                    ],
                },
            },
        }
        result = sanitize_probe(data)
        for check in result["test"]["structure"]["checks"]:
            self.assertNotIn("detail", check)
            self.assertIn("id", check)
            self.assertIn("status", check)

    def test_anonymizes_matrices(self):
        data = {
            "test": {
                "meta": {"instance": "test"},
                "structure": {"checks": []},
                "exchange_matrix": {"olivier": {"aurele": 5}},
                "friction_matrix": {"olivier": {"aurele": 3}},
            },
        }
        result = sanitize_probe(data)
        self.assertIn("orchestrator", result["test"]["exchange_matrix"])
        self.assertNotIn("olivier", result["test"]["exchange_matrix"])


if __name__ == "__main__":
    unittest.main()
