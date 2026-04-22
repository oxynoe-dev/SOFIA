"""T3 — Aggregate tests.

Verify multi-instance aggregation from per-instance JSON files.
Uses tmpdir with mock JSON — no real instances needed.
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aggregate import (
    _discover_instances, _aggregate_mirror, _aggregate_lens, _build_index, aggregate,
)


def _make_mirror_json(instance_name, frictions=5, flux_h=3, flux_a=2):
    """Create a minimal mirror.json structure for one instance."""
    return {
        "instances": {
            instance_name: {
                "meta": {"instance": instance_name, "date": "2026-04-22", "personas": ["alice", "bob"]},
                "friction_records": [
                    {"persona": "alice", "marker": "sound", "date": "2026-04-10"}
                    for _ in range(frictions)
                ],
                "personas": {
                    "alice": {
                        "flux_h": flux_h, "flux_a": flux_a,
                        "flux_types_h": {"substance": flux_h},
                        "flux_types_a": {"structure": flux_a},
                    },
                },
                "map": {"persona_roles": {"alice": "Architect"}},
                "trajectory": {"labels": ["w1"], "challenge_pct": [30]},
                "radars": {"alice": {"challenge": 50}},
                "kpi": {"friction_density": 2.5},
                "map_cards": {"alice": {"frictions": frictions}},
                "open_frictions": [],
            },
        },
        "default": instance_name,
    }


def _make_lens_json(instance_name, sessions=10, frictions=5):
    """Create a minimal lens.json structure for one instance."""
    return {
        "instances": {
            instance_name: {
                "meta": {
                    "instance": instance_name, "date": "2026-04-22",
                    "personas": ["alice", "bob"],
                    "sessions_scanned": sessions, "artifacts_scanned": 3,
                },
                "totals": {"signaler_pattern": 0},
                "time_series": {
                    "week": {
                        "labels": ["2026-W15", "2026-W16"],
                        "markers": {"sound": [3, 2], "contestable": [1, 0],
                                    "simplification": [0, 0], "blind_spot": [0, 0], "refuted": [0, 0]},
                        "directions": {"a_corroborates_h": [1, 1], "a_contests_h": [1, 0],
                                       "h_corroborates_a": [2, 1], "h_contests_a": [0, 1]},
                        "resolutions": {"ratified": [3, 1], "contested": [0, 0],
                                        "revised": [1, 1], "rejected": [0, 0]},
                        "flux_h": [2, 1], "flux_a": [3, 2],
                        "sessions": [3, 2],
                        "frictions_per_session": [1.33, 1.0],
                        "resolutions_per_session": [1.33, 1.0],
                    },
                    "day": {"labels": [], "markers": {}, "directions": {}, "resolutions": {}},
                },
                "personas": {
                    "alice": {
                        "markers": {"sound": 3, "contestable": 1, "simplification": 0, "blind_spot": 0, "refuted": 0},
                        "directions": {"a_corroborates_h": 1, "a_contests_h": 1, "h_corroborates_a": 2, "h_contests_a": 1},
                        "resolutions": {"ratified": 3, "contested": 0, "revised": 1, "rejected": 0},
                        "frictions": frictions, "flux_h": 3, "flux_a": 2,
                        "flux_h_pct": 60, "flux_a_pct": 40,
                        "flux_types_h": {"substance": 3}, "flux_types_a": {"structure": 2},
                        "sessions": sessions, "direction_ratio": 1.0,
                        "signaler_pattern_count": 0, "signaler_pattern_erreur_llm": 0,
                        "signaler_pattern_conviction": 0, "signaler_pattern_resistance": 0,
                    },
                },
            },
        },
        "default": instance_name,
    }


class TestDiscoverInstances(unittest.TestCase):

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_finds_subdirs_with_lens(self):
        inst = self.tmpdir / "alpha"
        inst.mkdir()
        (inst / "lens.json").write_text("{}")
        result = _discover_instances(self.tmpdir)
        self.assertEqual(result, ["alpha"])

    def test_finds_subdirs_with_mirror(self):
        inst = self.tmpdir / "beta"
        inst.mkdir()
        (inst / "mirror.json").write_text("{}")
        result = _discover_instances(self.tmpdir)
        self.assertEqual(result, ["beta"])

    def test_ignores_subdirs_without_json(self):
        inst = self.tmpdir / "empty"
        inst.mkdir()
        result = _discover_instances(self.tmpdir)
        self.assertEqual(result, [])

    def test_ignores_files(self):
        (self.tmpdir / "not-a-dir.json").write_text("{}")
        result = _discover_instances(self.tmpdir)
        self.assertEqual(result, [])

    def test_sorted_order(self):
        for name in ["charlie", "alpha", "bravo"]:
            inst = self.tmpdir / name
            inst.mkdir()
            (inst / "lens.json").write_text("{}")
        result = _discover_instances(self.tmpdir)
        self.assertEqual(result, ["alpha", "bravo", "charlie"])


class TestAggregateMirror(unittest.TestCase):

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _write_instance(self, name, **kwargs):
        inst = self.tmpdir / name
        inst.mkdir(exist_ok=True)
        data = _make_mirror_json(name, **kwargs)
        (inst / "mirror.json").write_text(json.dumps(data))

    def test_single_instance_no_all(self):
        self._write_instance("alpha")
        result = _aggregate_mirror(self.tmpdir, ["alpha"])
        self.assertIn("alpha", result["instances"])
        self.assertNotIn("all", result)

    def test_two_instances_produces_all(self):
        self._write_instance("alpha", frictions=3, flux_h=2, flux_a=1)
        self._write_instance("beta", frictions=5, flux_h=4, flux_a=3)
        result = _aggregate_mirror(self.tmpdir, ["alpha", "beta"])
        self.assertIn("all", result)
        self.assertEqual(len(result["all"]["friction_records"]), 8)

    def test_all_sums_flux(self):
        self._write_instance("alpha", flux_h=2, flux_a=1)
        self._write_instance("beta", flux_h=4, flux_a=3)
        result = _aggregate_mirror(self.tmpdir, ["alpha", "beta"])
        alice = result["all"]["personas"]["alice"]
        self.assertEqual(alice["flux_h"], 6)
        self.assertEqual(alice["flux_a"], 4)

    def test_default_is_first_instance(self):
        self._write_instance("alpha")
        self._write_instance("beta")
        result = _aggregate_mirror(self.tmpdir, ["alpha", "beta"])
        self.assertEqual(result["default"], "alpha")


class TestAggregateLens(unittest.TestCase):

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _write_instance(self, name, **kwargs):
        inst = self.tmpdir / name
        inst.mkdir(exist_ok=True)
        data = _make_lens_json(name, **kwargs)
        (inst / "lens.json").write_text(json.dumps(data))

    def test_single_instance_no_all(self):
        self._write_instance("alpha")
        result = _aggregate_lens(self.tmpdir, ["alpha"])
        self.assertIn("alpha", result["instances"])
        self.assertNotIn("all", result)

    def test_two_instances_produces_all(self):
        self._write_instance("alpha", sessions=10)
        self._write_instance("beta", sessions=5)
        result = _aggregate_lens(self.tmpdir, ["alpha", "beta"])
        self.assertIn("all", result)
        self.assertEqual(result["all"]["meta"]["sessions_scanned"], 15)

    def test_time_series_merged_by_label(self):
        self._write_instance("alpha")
        self._write_instance("beta")
        result = _aggregate_lens(self.tmpdir, ["alpha", "beta"])
        ts = result["all"]["time_series"]["week"]
        self.assertIn("2026-W15", ts["labels"])
        # sound values should be summed: 3+3=6 for W15
        idx = ts["labels"].index("2026-W15")
        self.assertEqual(ts["markers"]["sound"][idx], 6)

    def test_persona_data_merged(self):
        self._write_instance("alpha", frictions=5)
        self._write_instance("beta", frictions=3)
        result = _aggregate_lens(self.tmpdir, ["alpha", "beta"])
        alice = result["all"]["personas"]["alice"]
        self.assertEqual(alice["frictions"], 8)


class TestBuildIndex(unittest.TestCase):

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_lists_instances(self):
        result = _build_index(self.tmpdir, ["alpha", "beta", "gamma"])
        self.assertEqual(result["instances"], ["alpha", "beta", "gamma"])
        self.assertIn("generated", result)


class TestAggregateIdempotent(unittest.TestCase):

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_idempotent(self):
        inst = self.tmpdir / "alpha"
        inst.mkdir()
        (inst / "mirror.json").write_text(json.dumps(_make_mirror_json("alpha")))
        (inst / "lens.json").write_text(json.dumps(_make_lens_json("alpha")))

        aggregate(self.tmpdir)
        first_mirror = json.loads((self.tmpdir / "mirror.json").read_text())
        first_lens = json.loads((self.tmpdir / "lens.json").read_text())

        aggregate(self.tmpdir)
        second_mirror = json.loads((self.tmpdir / "mirror.json").read_text())
        second_lens = json.loads((self.tmpdir / "lens.json").read_text())

        # Remove generated timestamp for comparison
        first_idx = json.loads((self.tmpdir / "index.json").read_text())
        second_idx = json.loads((self.tmpdir / "index.json").read_text())
        self.assertEqual(first_idx["instances"], second_idx["instances"])

        self.assertEqual(first_mirror["instances"], second_mirror["instances"])
        self.assertEqual(first_lens["instances"], second_lens["instances"])


if __name__ == "__main__":
    unittest.main()
