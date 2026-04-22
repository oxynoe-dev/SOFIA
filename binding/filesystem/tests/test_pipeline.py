"""T1 — Pipeline unit tests.

Verify scan → mirror → lens using the mini-instance fixture.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.cli.scan import scan_instances
from analysis.cli.mirror import build_mirror
from analysis.cli.lens import build_lens

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "mini-instance"


class TestScan(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.records = scan_instances([FIXTURES])

    def test_produces_instance_key(self):
        self.assertIn("mini-instance", self.records)

    def test_has_friction_records(self):
        inst = self.records["mini-instance"]
        self.assertIn("friction_records", inst)
        self.assertGreater(len(inst["friction_records"]), 0)

    def test_has_meta(self):
        meta = self.records["mini-instance"]["meta"]
        self.assertIn("instance", meta)
        self.assertIn("personas", meta)
        self.assertIn("sessions_scanned", meta)
        self.assertIn("artifacts_scanned", meta)

    def test_friction_record_has_required_fields(self):
        rec = self.records["mini-instance"]["friction_records"][0]
        for field in ("persona", "date", "marker"):
            self.assertIn(field, rec)

    def test_meta_personas_not_empty(self):
        personas = self.records["mini-instance"]["meta"]["personas"]
        self.assertGreater(len(personas), 0)


class TestMirror(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        records = scan_instances([FIXTURES])
        cls.mirror = build_mirror(records)

    def test_has_instances(self):
        self.assertIn("instances", self.mirror)
        self.assertIn("mini-instance", self.mirror["instances"])

    def test_has_default(self):
        self.assertEqual(self.mirror["default"], "mini-instance")

    def test_instance_has_required_keys(self):
        inst = self.mirror["instances"]["mini-instance"]
        for key in ("meta", "friction_records", "personas", "kpi"):
            self.assertIn(key, inst)

    def test_kpi_has_expected_fields(self):
        kpi = self.mirror["instances"]["mini-instance"]["kpi"]
        for field in ("friction_density", "resolution_rate", "challenge_pct", "total_frictions", "total_sessions"):
            self.assertIn(field, kpi)

    def test_no_all_with_single_instance(self):
        self.assertNotIn("all", self.mirror)


class TestLens(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        records = scan_instances([FIXTURES])
        cls.lens = build_lens(records)

    def test_has_instances(self):
        self.assertIn("instances", self.lens)
        self.assertIn("mini-instance", self.lens["instances"])

    def test_instance_has_time_series(self):
        inst = self.lens["instances"]["mini-instance"]
        self.assertIn("time_series", inst)
        self.assertIn("week", inst["time_series"])
        self.assertIn("day", inst["time_series"])

    def test_time_series_has_labels(self):
        ts = self.lens["instances"]["mini-instance"]["time_series"]["week"]
        self.assertIn("labels", ts)

    def test_time_series_has_markers(self):
        ts = self.lens["instances"]["mini-instance"]["time_series"]["week"]
        self.assertIn("markers", ts)
        for marker in ("sound", "contestable", "simplification", "blind_spot", "refuted"):
            self.assertIn(marker, ts["markers"])

    def test_instance_has_personas(self):
        inst = self.lens["instances"]["mini-instance"]
        self.assertIn("personas", inst)
        self.assertGreater(len(inst["personas"]), 0)

    def test_persona_has_markers(self):
        personas = self.lens["instances"]["mini-instance"]["personas"]
        p = next(iter(personas.values()))
        self.assertIn("markers", p)

    def test_no_all_with_single_instance(self):
        self.assertNotIn("all", self.lens)


class TestCrossInstance(unittest.TestCase):
    """Test "all" aggregation with duplicated fixture as 2 instances."""

    @classmethod
    def setUpClass(cls):
        records = scan_instances([FIXTURES])
        # Simulate 2 instances by duplicating under a different name
        data = records["mini-instance"]
        records["mini-instance-2"] = data
        cls.mirror = build_mirror(records)
        cls.lens = build_lens(records)

    def test_mirror_has_all(self):
        self.assertIn("all", self.mirror)

    def test_mirror_all_has_friction_records(self):
        self.assertGreater(len(self.mirror["all"]["friction_records"]), 0)

    def test_lens_has_all(self):
        self.assertIn("all", self.lens)

    def test_lens_all_has_time_series(self):
        self.assertIn("time_series", self.lens["all"])

    def test_lens_all_sessions_doubled(self):
        single = self.lens["instances"]["mini-instance"]["meta"]["sessions_scanned"]
        total = self.lens["all"]["meta"]["sessions_scanned"]
        self.assertEqual(total, single * 2)


if __name__ == "__main__":
    unittest.main()
