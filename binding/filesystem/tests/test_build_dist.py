"""T4 — Build dist tests.

Verify static dashboard build: selective cleanup, JS patching, probe removal.
Uses tmpdir — no real dashboard needed.
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from build_dist import build_dist

ROOT = Path(__file__).resolve().parent.parent


class TestBuildDist(unittest.TestCase):

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.output = self.tmpdir / "dashboard"
        # Create minimal data files expected by build_dist
        data_dir = ROOT / "analysis" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        for f in ["lens.json", "mirror.json"]:
            p = data_dir / f
            if not p.is_file():
                p.write_text("{}")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_creates_expected_structure(self):
        build_dist(self.output)
        self.assertTrue((self.output / "index.html").is_file())
        self.assertTrue((self.output / "css").is_dir())
        self.assertTrue((self.output / "js").is_dir())
        self.assertTrue((self.output / "data").is_dir())

    def test_canary_survives_rebuild(self):
        """Non-generated files must survive rebuild (fix rmtree)."""
        build_dist(self.output)
        canary = self.output / "CANARY.txt"
        canary.write_text("I must survive")

        # Rebuild
        build_dist(self.output)

        self.assertTrue(canary.is_file())
        self.assertEqual(canary.read_text(), "I must survive")

    def test_git_dir_survives_rebuild(self):
        """A .git directory must survive rebuild."""
        build_dist(self.output)
        git_dir = self.output / ".git"
        git_dir.mkdir()
        (git_dir / "HEAD").write_text("ref: refs/heads/main")

        build_dist(self.output)

        self.assertTrue(git_dir.is_dir())
        self.assertTrue((git_dir / "HEAD").is_file())

    def test_no_probe_in_html(self):
        build_dist(self.output)
        html = (self.output / "index.html").read_text()
        self.assertNotIn("probe.js", html)
        self.assertNotIn("switchTab('probe')", html)

    def test_no_refresh_button_in_html(self):
        build_dist(self.output)
        html = (self.output / "index.html").read_text()
        self.assertNotIn("btn-refresh", html)

    def test_js_paths_patched(self):
        build_dist(self.output)
        app_js = (self.output / "js" / "app.js").read_text()
        self.assertIn("data/lens.json", app_js)
        self.assertIn("data/mirror.json", app_js)
        self.assertNotIn("fetch('/lens')", app_js)
        self.assertNotIn("fetch('/mirror')", app_js)

    def test_probe_js_not_included(self):
        build_dist(self.output)
        self.assertFalse((self.output / "js" / "probe.js").is_file())

    def test_external_data_dir(self):
        ext_data = self.tmpdir / "external-data"
        build_dist(self.output, data_dir=ext_data)
        self.assertTrue(ext_data.is_dir())
        # Data also in dashboard/data/
        self.assertTrue((self.output / "data").is_dir())


if __name__ == "__main__":
    unittest.main()
