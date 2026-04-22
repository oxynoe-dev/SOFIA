"""E2E tests — End-to-end integration tests.

E2E-1b: create-instance.py → probe → analysis pipeline
E2E-2:  analysis (2 instances) → aggregate → build_dist (h2a workflow)
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Import analysis.py (the script, not the package) — name conflict workaround
import importlib.util
_spec = importlib.util.spec_from_file_location("analysis_main", ROOT / "analysis.py")
analysis_main = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(analysis_main)
run_pipeline = analysis_main.run_pipeline

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MINI_1 = FIXTURES / "mini-instance"
MINI_2 = FIXTURES / "mini-instance-2"


class TestE2E_1b_CreateInstance(unittest.TestCase):
    """E2E-1b: create-instance.py → probe → analysis pipeline."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_full_lifecycle(self):
        """Create instance → probe passes → analysis produces output."""
        # Import dynamically (filename has hyphen)
        import importlib
        spec = importlib.util.spec_from_file_location(
            "create_instance",
            Path(__file__).resolve().parent.parent / "create-instance.py",
        )
        create_instance = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(create_instance)

        # E2E-1b.1: Create instance
        instance_path = self.tmpdir / "test-lab"
        create_instance.create_instance(
            instance_path,
            ["Eve", "Frank"],
            "Test Lab",
        )

        # E2E-1b.2: Verify structure
        self.assertTrue((instance_path / "sofia.md").is_file())
        self.assertTrue((instance_path / "shared" / "conventions.md").is_file())
        self.assertTrue((instance_path / "shared" / "orga" / "personas" / "persona-eve.md").is_file())
        self.assertTrue((instance_path / "shared" / "orga" / "personas" / "persona-frank.md").is_file())
        self.assertTrue((instance_path / "eve" / "sessions").is_dir())
        self.assertTrue((instance_path / "frank" / "sessions").is_dir())

        # E2E-1b.3: Probe passes
        from analysis.cli.probe import probe_instances
        probe_data = probe_instances([instance_path])
        self.assertIn("test-lab", probe_data)
        checks = probe_data["test-lab"]["structure"]["checks"]
        fails = [c for c in checks if c["status"] == "fail"]
        self.assertEqual(len(fails), 0, f"Probe failures: {fails}")

        # E2E-1b.4: Simulate a session with friction
        session_dir = instance_path / "eve" / "sessions"
        session_file = session_dir / "2026-04-22-eve.md"
        session_file.write_text(
            "---\n"
            "nature: session\n"
            "persona: eve\n"
            "date: 2026-04-22\n"
            "---\n\n"
            "# Session 22/04 — Eve\n\n"
            "## Produced\n"
            "- prototype v1\n\n"
            "## Orchestrator friction\n"
            "- ✓ API design — [eve] proposed REST, PO agrees\n"
            "- ~ Error handling — [PO] thinks it's too permissive\n",
            encoding="utf-8",
        )

        # E2E-1b.5: Run analysis pipeline
        from analysis.cli.scan import scan_instances
        from analysis.cli.mirror import build_mirror
        from analysis.cli.lens import build_lens

        records = scan_instances([instance_path])
        self.assertIn("test-lab", records)
        frictions = records["test-lab"]["friction_records"]
        self.assertEqual(len(frictions), 2)

        mirror = build_mirror(records)
        self.assertIn("test-lab", mirror["instances"])

        lens = build_lens(records)
        self.assertIn("test-lab", lens["instances"])

        # E2E-1b.6: Verify output structure with --output
        out_dir = self.tmpdir / "output"
        # run_pipeline imported at module level
        run_pipeline([instance_path], output_dir=out_dir)

        self.assertTrue((out_dir / "test-lab" / "mirror.json").is_file())
        self.assertTrue((out_dir / "test-lab" / "lens.json").is_file())
        self.assertTrue((out_dir / "test-lab" / "records.json").is_file())
        self.assertTrue((out_dir / "mirror.json").is_file())
        self.assertTrue((out_dir / "index.json").is_file())


class TestE2E_2_PipelineH2A(unittest.TestCase):
    """E2E-2: Full h2a-data workflow with 2 instances.

    analysis (instance-1) → analysis (instance-2) → aggregate → build_dist
    """

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.h2a_data = self.tmpdir / "h2a-data"
        self.h2a_data_dir = self.h2a_data / "data"
        self.h2a_dashboard = self.h2a_data / "dashboard"
        self.h2a_data_dir.mkdir(parents=True)
        self.h2a_dashboard.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_e2e_2_1_structure_created(self):
        """E2E-2.1: h2a-data structure exists."""
        self.assertTrue(self.h2a_data_dir.is_dir())
        self.assertTrue(self.h2a_dashboard.is_dir())

    def test_e2e_2_full_workflow(self):
        """E2E-2.2 → E2E-2.9: Full pipeline test."""
        # run_pipeline imported at module level
        from aggregate import aggregate
        from build_dist import build_dist

        # E2E-2.2: Run analysis on instance 1 with --sanitize
        run_pipeline([MINI_1], output_dir=self.h2a_data_dir, sanitize=True)

        self.assertTrue((self.h2a_data_dir / "mini-instance" / "mirror.json").is_file())
        self.assertTrue((self.h2a_data_dir / "mini-instance" / "lens.json").is_file())
        self.assertTrue((self.h2a_data_dir / "mini-instance" / "records.json").is_file())
        self.assertTrue((self.h2a_data_dir / "index.json").is_file())

        # E2E-2.3: Verify sanitization
        records = json.loads((self.h2a_data_dir / "mini-instance" / "records.json").read_text())
        inst_key = next(iter(records.keys())) if "instances" not in records else None
        if inst_key:
            recs = records[inst_key].get("friction_records", [])
        else:
            inst_data = next(iter(records.get("instances", {}).values()), {})
            recs = inst_data.get("friction_records", [])
        if recs:
            self.assertNotIn("description", recs[0])
            self.assertNotIn("source", recs[0])

        # E2E-2.4 + E2E-2.5: Run analysis on instance 2
        run_pipeline([MINI_2], output_dir=self.h2a_data_dir, sanitize=True)

        self.assertTrue((self.h2a_data_dir / "mini-instance-2" / "mirror.json").is_file())
        self.assertTrue((self.h2a_data_dir / "mini-instance-2" / "lens.json").is_file())

        # E2E-2.6: Aggregate
        aggregate(self.h2a_data_dir)

        index = json.loads((self.h2a_data_dir / "index.json").read_text())
        self.assertIn("mini-instance", index["instances"])
        self.assertIn("mini-instance-2", index["instances"])
        self.assertEqual(len(index["instances"]), 2)

        # Aggregated files should have "all" key
        mirror_agg = json.loads((self.h2a_data_dir / "mirror.json").read_text())
        self.assertIn("all", mirror_agg)
        self.assertIn("mini-instance", mirror_agg["instances"])
        self.assertIn("mini-instance-2", mirror_agg["instances"])

        lens_agg = json.loads((self.h2a_data_dir / "lens.json").read_text())
        self.assertIn("all", lens_agg)

        # E2E-2.7: Build dashboard
        build_dist(self.h2a_dashboard, data_dir=self.h2a_data_dir)

        self.assertTrue((self.h2a_dashboard / "index.html").is_file())
        self.assertTrue((self.h2a_dashboard / "css").is_dir())
        self.assertTrue((self.h2a_dashboard / "js").is_dir())
        self.assertTrue((self.h2a_dashboard / "data").is_dir())

        # E2E-2.8: Dashboard data contains aggregated JSON
        dash_mirror = self.h2a_dashboard / "data" / "mirror.json"
        self.assertTrue(dash_mirror.is_file())
        dash_data = json.loads(dash_mirror.read_text())
        self.assertIn("instances", dash_data)

        # E2E-2.9: Canary survives rebuild
        canary = self.h2a_dashboard / "README.md"
        canary.write_text("# h2a-data dashboard")
        build_dist(self.h2a_dashboard, data_dir=self.h2a_data_dir)
        self.assertTrue(canary.is_file())
        self.assertEqual(canary.read_text(), "# h2a-data dashboard")


class TestE2E_2_AggregateExternal(unittest.TestCase):
    """Test adding an external instance via aggregate.py only (no re-analysis)."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.data_dir = self.tmpdir / "data"
        self.data_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_add_external_instance(self):
        """Simulate a contributor adding their data to h2a-data."""
        # run_pipeline imported at module level
        from aggregate import aggregate

        # Existing instance
        run_pipeline([MINI_1], output_dir=self.data_dir, sanitize=True)

        # Verify single instance
        index = json.loads((self.data_dir / "index.json").read_text())
        self.assertEqual(len(index["instances"]), 1)

        mirror_before = json.loads((self.data_dir / "mirror.json").read_text())
        self.assertNotIn("all", mirror_before)

        # External contributor adds their instance (pre-analyzed JSON)
        ext_dir = self.data_dir / "external-lab"
        ext_dir.mkdir()
        # Copy mini-instance-2 analysis output as if it were external
        run_pipeline([MINI_2], output_dir=self.tmpdir / "tmp-analysis")
        tmp_inst = self.tmpdir / "tmp-analysis" / "mini-instance-2"
        for f in tmp_inst.glob("*.json"):
            shutil.copy2(f, ext_dir / f.name)

        # Re-aggregate (this is what the orchestrator runs after merge)
        aggregate(self.data_dir)

        # Now we should have 2 instances + "all"
        index = json.loads((self.data_dir / "index.json").read_text())
        self.assertEqual(len(index["instances"]), 2)
        self.assertIn("external-lab", index["instances"])

        mirror_after = json.loads((self.data_dir / "mirror.json").read_text())
        self.assertIn("all", mirror_after)
        self.assertIn("mini-instance", mirror_after["instances"])
        self.assertIn("external-lab", mirror_after["instances"])


if __name__ == "__main__":
    unittest.main()
