#!/usr/bin/env python3
"""Tests for create-instance.py — zero external dependency (unittest)."""
from __future__ import annotations

import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent dir to path so we can import the script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import importlib
create = importlib.import_module("create-instance")
audit = importlib.import_module("audit-instance")


class TestCreateInstance(unittest.TestCase):

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.instance = self.tmpdir / "test-instance"

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _create(self, personas=None, produit="monprojet"):
        if personas is None:
            personas = ["alice", "bob"]
        return create.create_instance(self.instance, personas, produit)

    # --- Structure ---

    def test_creates_voix_md(self):
        self._create()
        self.assertTrue((self.instance / "voix.md").is_file())

    def test_creates_conventions(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "conventions.md").is_file())

    def test_creates_team_orga(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "orga" / "team-orga.md").is_file())

    def test_creates_roadmap(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "roadmap-monprojet.md").is_file())

    def test_creates_notes_with_archives(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "notes" / "archives").is_dir())

    def test_creates_review_with_archives(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "review" / "archives").is_dir())

    def test_creates_features(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "features").is_dir())

    # --- Per persona ---

    def test_creates_persona_file(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "orga" / "personas" / "persona-alice.md").is_file())
        self.assertTrue((self.instance / "shared" / "orga" / "personas" / "persona-bob.md").is_file())

    def test_creates_contexte_file(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "orga" / "contextes" / "contexte-alice-monprojet.md").is_file())
        self.assertTrue((self.instance / "shared" / "orga" / "contextes" / "contexte-bob-monprojet.md").is_file())

    def test_creates_workspace(self):
        self._create()
        self.assertTrue((self.instance / "alice").is_dir())
        self.assertTrue((self.instance / "bob").is_dir())

    def test_creates_claude_md(self):
        self._create()
        self.assertTrue((self.instance / "alice" / "CLAUDE.md").is_file())
        self.assertTrue((self.instance / "bob" / "CLAUDE.md").is_file())

    def test_creates_sessions_dir(self):
        self._create()
        self.assertTrue((self.instance / "alice" / "sessions").is_dir())
        self.assertTrue((self.instance / "bob" / "sessions").is_dir())

    # --- Content ---

    def test_conventions_has_friction_markers(self):
        self._create()
        text = (self.instance / "shared" / "conventions.md").read_text(encoding="utf-8")
        for marker in ["✓", "~", "⚡", "◐", "✗"]:
            self.assertIn(marker, text, f"Marqueur {marker} absent de conventions.md")

    def test_persona_has_7_dimensions(self):
        self._create()
        text = (self.instance / "shared" / "orga" / "personas" / "persona-alice.md").read_text(encoding="utf-8")
        for section in ["Profil", "Posture", "Domaines d'intervention",
                        "Ce qu'il/elle produit", "Ce qu'il/elle challenge",
                        "Ce qu'il/elle ne fait pas", "Collaboration"]:
            self.assertIn(section, text, f"Section '{section}' absente de persona-alice.md")

    def test_contexte_has_operational_sections(self):
        self._create()
        text = (self.instance / "shared" / "orga" / "contextes" / "contexte-alice-monprojet.md").read_text(encoding="utf-8")
        for section in ["Perimetre", "Documents cles", "Isolation", "Conventions",
                        "Workflow", "Emergence", "Protocole de session"]:
            self.assertIn(section, text, f"Section '{section}' absente de contexte")

    def test_contexte_has_friction_markers(self):
        self._create()
        text = (self.instance / "shared" / "orga" / "contextes" / "contexte-alice-monprojet.md").read_text(encoding="utf-8")
        self.assertIn("✓", text)
        self.assertIn("✗", text)

    def test_claude_md_is_aiguillage(self):
        self._create()
        text = (self.instance / "alice" / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("persona-alice.md", text)
        self.assertIn("contexte-alice-monprojet.md", text)

    def test_voix_md_lists_personas(self):
        self._create()
        text = (self.instance / "voix.md").read_text(encoding="utf-8")
        self.assertIn("alice", text)
        self.assertIn("bob", text)

    def test_team_orga_lists_personas(self):
        self._create()
        text = (self.instance / "shared" / "orga" / "team-orga.md").read_text(encoding="utf-8")
        self.assertIn("Alice", text)
        self.assertIn("Bob", text)

    # --- File count ---

    def test_file_count_2_personas(self):
        created = self._create()
        # voix.md + conventions + team-orga + roadmap + 2*(persona + contexte + CLAUDE.md) = 10
        self.assertEqual(len(created), 10)

    def test_file_count_3_personas(self):
        created = self._create(personas=["alice", "bob", "charlie"])
        # 4 base + 3*3 per persona = 13
        self.assertEqual(len(created), 13)

    # --- Produit with spaces ---

    def test_produit_with_spaces(self):
        self._create(produit="mon super projet")
        self.assertTrue((self.instance / "shared" / "roadmap-mon-super-projet.md").is_file())
        self.assertTrue((self.instance / "shared" / "orga" / "contextes" / "contexte-alice-mon-super-projet.md").is_file())

    # --- Idempotence ---

    def test_does_not_overwrite_existing(self):
        self._create()
        # Modify a file
        conv = self.instance / "shared" / "conventions.md"
        conv.write_text("custom content", encoding="utf-8")
        # Re-create overwrites (by design — script is for new instances)
        self._create()
        text = conv.read_text(encoding="utf-8")
        self.assertIn("Marqueurs de friction", text)

    # --- Convention conformity ---

    def test_persona_has_frontmatter(self):
        self._create()
        text = (self.instance / "shared" / "orga" / "personas" / "persona-alice.md").read_text(encoding="utf-8")
        fm = audit.parse_frontmatter_from_text(text)
        self.assertIsNotNone(fm, "Persona file must have frontmatter")
        self.assertIn("nom", fm)
        self.assertIn("role", fm)

    def test_contexte_has_frontmatter(self):
        self._create()
        text = (self.instance / "shared" / "orga" / "contextes" / "contexte-alice-monprojet.md").read_text(encoding="utf-8")
        fm = audit.parse_frontmatter_from_text(text)
        self.assertIsNotNone(fm, "Contexte file must have frontmatter")
        self.assertIn("persona", fm)
        self.assertIn("produit", fm)
        self.assertEqual(fm["persona"], "alice")
        self.assertEqual(fm["produit"], "monprojet")

    def test_claude_md_paths_are_relative(self):
        self._create()
        text = (self.instance / "alice" / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("../shared/orga/personas/", text, "CLAUDE.md paths must be relative with ../")
        self.assertIn("../shared/orga/contextes/", text, "CLAUDE.md paths must be relative with ../")
        self.assertNotIn("/shared/orga/", text.split("../shared")[0], "No absolute paths before relative")

    def test_conventions_has_frontmatter_spec(self):
        self._create()
        text = (self.instance / "shared" / "conventions.md").read_text(encoding="utf-8")
        for field in ["de:", "pour:", "nature:", "statut:", "date:"]:
            self.assertIn(field, text, f"Conventions must document frontmatter field '{field}'")

    def test_conventions_has_archivage(self):
        self._create()
        text = (self.instance / "shared" / "conventions.md").read_text(encoding="utf-8")
        self.assertIn("archives/", text, "Conventions must document archivage")

    def test_conventions_has_commit_format(self):
        self._create()
        text = (self.instance / "shared" / "conventions.md").read_text(encoding="utf-8")
        self.assertIn("persona", text.lower())
        self.assertIn("commit", text.lower())

    def test_conventions_has_all_5_markers(self):
        self._create()
        text = (self.instance / "shared" / "conventions.md").read_text(encoding="utf-8")
        self.assertIn("Juste", text)
        self.assertIn("Contestable", text)
        self.assertIn("Simplification", text)
        self.assertIn("Angle mort", text)
        self.assertIn("Faux", text)

    def test_roadmap_has_owner(self):
        self._create()
        text = (self.instance / "shared" / "roadmap-monprojet.md").read_text(encoding="utf-8")
        self.assertIn("Owner", text, "Roadmap must declare an Owner")

    def test_roadmap_has_version_metadata(self):
        self._create()
        text = (self.instance / "shared" / "roadmap-monprojet.md").read_text(encoding="utf-8")
        self.assertIn("<!-- produit:", text, "Roadmap version must have metadata comment")

    def test_voix_md_has_method_link(self):
        self._create()
        text = (self.instance / "voix.md").read_text(encoding="utf-8")
        self.assertIn("oxynoe-dev/sofia", text, "voix.md must link to SOFIA repo")

    def test_voix_md_has_version(self):
        self._create()
        text = (self.instance / "voix.md").read_text(encoding="utf-8")
        self.assertIn("Version methode", text, "voix.md must mention method version")

    # --- Audit conformity (integration test) ---

    def test_audit_passes_on_created_instance(self):
        """Run the audit script on a created instance — all structural checks should pass."""
        self._create()
        checks = audit.check_structure(self.instance)
        fails = [c for c in checks if c["status"] == "fail"]
        self.assertEqual(len(fails), 0,
                         f"Audit structural fails on created instance: {[c['detail'] for c in fails]}")

    def test_audit_no_warnings_on_created_instance(self):
        """Run the audit script on a created instance — no warnings expected."""
        self._create()
        checks = audit.check_structure(self.instance)
        warns = [c for c in checks if c["status"] == "warn"]
        self.assertEqual(len(warns), 0,
                         f"Audit structural warnings on created instance: {[c['detail'] for c in warns]}")


if __name__ == "__main__":
    unittest.main()
