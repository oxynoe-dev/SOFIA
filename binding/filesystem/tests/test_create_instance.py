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

from analysis.lib import parser as audit_parser
from analysis.cli import probe as audit_probe
# Compat namespace
from types import SimpleNamespace
audit = SimpleNamespace(
    check_structure=audit_probe.check_structure,
    parse_frontmatter=audit_parser.parse_frontmatter,
    parse_frontmatter_from_text=audit_parser.parse_frontmatter_from_text,
)


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

    def test_creates_sofia_md(self):
        self._create()
        self.assertTrue((self.instance / "sofia.md").is_file())

    def test_creates_conventions(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "conventions.md").is_file())

    def test_creates_team_orga(self):
        self._create()
        self.assertTrue((self.instance / "shared" / "orga" / "team-orga.md").is_file())

    def test_no_notes_dir(self):
        """Scaffolding minimal — notes/ n'est pas pre-cree."""
        self._create()
        self.assertFalse((self.instance / "shared" / "notes").exists())

    def test_no_review_dir(self):
        """Scaffolding minimal — review/ n'est pas pre-cree."""
        self._create()
        self.assertFalse((self.instance / "shared" / "review").exists())

    def test_no_features_dir(self):
        """Scaffolding minimal — features/ n'est pas pre-cree."""
        self._create()
        self.assertFalse((self.instance / "shared" / "features").exists())

    def test_no_roadmap(self):
        """Scaffolding minimal — roadmap n'est pas pre-creee."""
        self._create()
        self.assertFalse((self.instance / "shared" / "roadmap-monprojet.md").exists())

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

    def test_sofia_md_lists_personas(self):
        self._create()
        text = (self.instance / "sofia.md").read_text(encoding="utf-8")
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
        # sofia.md + conventions + team-orga + 2*(persona + contexte + CLAUDE.md) = 9
        self.assertEqual(len(created), 9)

    def test_file_count_3_personas(self):
        created = self._create(personas=["alice", "bob", "charlie"])
        # 3 base + 3*3 per persona = 12
        self.assertEqual(len(created), 12)

    # --- Produit with spaces ---

    def test_produit_with_spaces(self):
        self._create(produit="mon super projet")
        self.assertTrue((self.instance / "shared" / "orga" / "contextes" / "contexte-alice-mon-super-projet.md").is_file())

    # --- Content checks ---

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

    def test_conventions_has_frontmatter_spec(self):
        self._create()
        text = (self.instance / "shared" / "conventions.md").read_text(encoding="utf-8")
        for field in ["from:", "to:", "nature:", "status:", "date:"]:
            self.assertIn(field, text, f"Conventions must document frontmatter field '{field}'")

    def test_conventions_has_commit_format(self):
        self._create()
        text = (self.instance / "shared" / "conventions.md").read_text(encoding="utf-8")
        self.assertIn("persona", text.lower())
        self.assertIn("commit", text.lower())

    def test_conventions_has_resolutions(self):
        self._create()
        text = (self.instance / "shared" / "conventions.md").read_text(encoding="utf-8")
        for tag in ["ratified", "contested", "revised", "rejected"]:
            self.assertIn(tag, text, f"Conventions must document resolution tag '{tag}'")

    def test_conventions_has_mutabilite(self):
        self._create()
        text = (self.instance / "shared" / "conventions.md").read_text(encoding="utf-8")
        self.assertIn("ref:", text, "Conventions must document mutabilite inter-sessions (ref:)")

    def test_sofia_md_has_method_link(self):
        self._create()
        text = (self.instance / "sofia.md").read_text(encoding="utf-8")
        self.assertIn("oxynoe-dev/sofia", text, "sofia.md must link to SOFIA repo")

    def test_sofia_md_has_version(self):
        self._create()
        text = (self.instance / "sofia.md").read_text(encoding="utf-8")
        self.assertIn("Version methode", text, "sofia.md must mention method version")


if __name__ == "__main__":
    unittest.main()
