#!/usr/bin/env python3
"""Tests for audit-instance.py — zero external dependency (unittest + fixtures)."""
from __future__ import annotations

import unittest
import sys
from pathlib import Path

# Add parent dir to path so we can import the script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import functions from audit-instance.py (hyphen in filename)
import importlib
audit = importlib.import_module("audit-instance")

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "mini-instance"


class TestParseFrontmatter(unittest.TestCase):

    def test_valid_frontmatter(self):
        text = "---\nde: alice\npour: bob\nnature: note\n---\n# Title"
        fm = audit.parse_frontmatter_from_text(text)
        self.assertIsNotNone(fm)
        self.assertEqual(fm["de"], "alice")
        self.assertEqual(fm["pour"], "bob")

    def test_no_frontmatter(self):
        text = "# Just a title\nSome content."
        fm = audit.parse_frontmatter_from_text(text)
        self.assertIsNone(fm)

    def test_empty_frontmatter(self):
        text = "---\n---\n# Title"
        fm = audit.parse_frontmatter_from_text(text)
        self.assertIsNone(fm)

    def test_value_with_colon(self):
        text = "---\nobjet: adr-051: review\n---\n"
        fm = audit.parse_frontmatter_from_text(text)
        self.assertIsNotNone(fm)
        self.assertEqual(fm["objet"], "adr-051: review")

    def test_file_parse(self):
        fm = audit.parse_frontmatter(FIXTURES / "shared" / "notes" / "note-bob-arch-alice.md")
        self.assertIsNotNone(fm)
        self.assertEqual(fm["de"], "alice")

    def test_file_no_frontmatter(self):
        fm = audit.parse_frontmatter(FIXTURES / "shared" / "notes" / "note-sans-frontmatter.md")
        self.assertIsNone(fm)


class TestNormalizeFrontmatter(unittest.TestCase):

    def test_standard_fields(self):
        fm = {"de": "Alice", "pour": "Bob", "nature": "review"}
        n = audit.normalize_frontmatter(fm)
        self.assertEqual(n["de"], "alice")
        self.assertEqual(n["pour"], ["bob"])
        self.assertEqual(n["nature"], "review")

    def test_aliases(self):
        fm = {"auteur": "Alice", "destinataire": "Bob", "type": "signal"}
        n = audit.normalize_frontmatter(fm)
        self.assertEqual(n["de"], "alice")
        self.assertEqual(n["pour"], ["bob"])
        self.assertEqual(n["nature"], "signal")

    def test_multi_recipients(self):
        fm = {"de": "alice", "pour": "bob, charlie"}
        n = audit.normalize_frontmatter(fm)
        self.assertEqual(n["pour"], ["bob", "charlie"])

    def test_accents(self):
        fm = {"de": "léa", "pour": "équipe"}
        n = audit.normalize_frontmatter(fm)
        self.assertEqual(n["de"], "lea")
        self.assertEqual(n["pour"], ["equipe"])


class TestFrictionMarkers(unittest.TestCase):

    def test_all_markers(self):
        text = "---\nde: x\n---\n✓ ok\n~ contestable\n⚡ trop\n◐ oubli\n✗ faux"
        counts = audit.count_friction_markers_from_text(text)
        self.assertEqual(counts["juste"], 1)
        self.assertEqual(counts["contestable"], 1)
        self.assertEqual(counts["simplification"], 1)
        self.assertEqual(counts["angle_mort"], 1)
        self.assertEqual(counts["faux"], 1)

    def test_no_markers(self):
        text = "---\nde: x\n---\nJust regular text."
        counts = audit.count_friction_markers_from_text(text)
        self.assertEqual(sum(counts.values()), 0)

    def test_tilde_in_text_not_counted(self):
        text = "---\nde: x\n---\nThe path ~/home is not a marker."
        counts = audit.count_friction_markers_from_text(text)
        self.assertEqual(counts["contestable"], 0)

    def test_tilde_as_list_marker(self):
        text = "---\nde: x\n---\n- ~ contestable item\n* ~ another one"
        counts = audit.count_friction_markers_from_text(text)
        self.assertEqual(counts["contestable"], 2)

    def test_from_fixture(self):
        counts = audit.count_friction_markers_from_text(
            (FIXTURES / "shared" / "notes" / "note-bob-arch-alice.md").read_text())
        self.assertEqual(counts["juste"], 1)
        self.assertEqual(counts["contestable"], 1)
        self.assertEqual(counts["simplification"], 1)

    def test_review_fixture(self):
        counts = audit.count_friction_markers_from_text(
            (FIXTURES / "shared" / "review" / "review-code-alice.md").read_text())
        self.assertEqual(counts["juste"], 1)
        self.assertEqual(counts["angle_mort"], 1)
        self.assertEqual(counts["faux"], 1)


class TestDiscoverPersonas(unittest.TestCase):

    def test_discover(self):
        personas = audit.discover_personas(FIXTURES)
        self.assertEqual(personas, {"alice", "bob"})

    def test_missing_dir(self):
        personas = audit.discover_personas(Path("/nonexistent"))
        self.assertEqual(personas, set())


class TestCheckStructure(unittest.TestCase):

    def test_basic_checks(self):
        checks = audit.check_structure(FIXTURES)
        by_id = {c["id"]: c for c in checks}

        self.assertEqual(by_id["S1"]["status"], "pass")  # sofia.md
        self.assertEqual(by_id["S2"]["status"], "pass")  # shared/
        self.assertEqual(by_id["S3"]["status"], "pass")  # conventions.md
        self.assertEqual(by_id["S8"]["status"], "pass")  # workspaces with CLAUDE.md
        self.assertEqual(by_id["R1"]["status"], "pass")  # roadmap header


class TestScanArtifacts(unittest.TestCase):

    def test_scan(self):
        artifacts, warnings = audit.scan_artifacts(FIXTURES)
        # 3 notes with frontmatter (including archived) + 1 review = 4
        # note-sans-frontmatter.md should be in warnings
        self.assertTrue(len(artifacts) >= 3)
        self.assertTrue(any("sans-frontmatter" in w for w in warnings))

    def test_emitters(self):
        artifacts, _ = audit.scan_artifacts(FIXTURES)
        emitters = {a["de"] for a in artifacts}
        self.assertIn("alice", emitters)
        self.assertIn("bob", emitters)


class TestMatrices(unittest.TestCase):

    def test_exchange_matrix(self):
        artifacts, _ = audit.scan_artifacts(FIXTURES)
        matrix = audit.build_exchange_matrix(artifacts)
        # alice -> bob: at least 2 (note + review)
        self.assertGreaterEqual(matrix.get("alice", {}).get("bob", 0), 2)

    def test_friction_matrix(self):
        artifacts, _ = audit.scan_artifacts(FIXTURES)
        matrix = audit.build_friction_matrix(artifacts)
        # alice -> bob: signal + review = 2
        self.assertGreaterEqual(matrix.get("alice", {}).get("bob", 0), 2)

    def test_marker_totals(self):
        artifacts, _ = audit.scan_artifacts(FIXTURES)
        totals = audit.build_marker_totals(artifacts)
        # alice emits friction with markers
        self.assertGreater(totals.get("alice", {}).get("juste", 0), 0)


class TestSessionFriction(unittest.TestCase):

    def test_scan(self):
        po_friction, _ = audit.scan_session_friction(FIXTURES)
        self.assertIn("alice", po_friction)
        self.assertEqual(po_friction["alice"]["total_sessions"], 1)
        self.assertEqual(po_friction["alice"]["sessions_with_friction"], 1)
        # 1 juste, 1 contestable, 1 angle_mort
        self.assertEqual(po_friction["alice"]["juste"], 1)
        self.assertEqual(po_friction["alice"]["contestable"], 1)
        self.assertEqual(po_friction["alice"]["angle_mort"], 1)

    def test_initiative_tags(self):
        po_friction, _ = audit.scan_session_friction(FIXTURES)
        alice = po_friction["alice"]
        # 1 PO, 2 alice
        self.assertEqual(alice["initiative_po"], 1)
        self.assertEqual(alice["initiative_persona"], 2)

    def test_bob_no_friction_section(self):
        po_friction, _ = audit.scan_session_friction(FIXTURES)
        self.assertIn("bob", po_friction)
        self.assertEqual(po_friction["bob"]["total_sessions"], 1)
        self.assertEqual(po_friction["bob"]["sessions_with_friction"], 0)


class TestSignals(unittest.TestCase):

    def test_filtered_signals(self):
        artifacts, _ = audit.scan_artifacts(FIXTURES)
        exchange = audit.build_exchange_matrix(artifacts)
        friction = audit.build_friction_matrix(artifacts)
        markers = audit.build_marker_totals(artifacts)
        po_friction, _ = audit.scan_session_friction(FIXTURES)
        real = audit.discover_personas(FIXTURES)

        all_p = sorted({a["de"] for a in artifacts} | {p for a in artifacts for p in a["pour"]})
        signals = audit.generate_signals(exchange, friction, markers, po_friction, all_p, real)

        # "equipe" should NOT appear in signals (pseudo-persona)
        for s in signals:
            self.assertNotIn("equipe", s)

    def test_domestication(self):
        # Bob has no friction emitted -> should not trigger domestication
        # (domestication requires markers, bob has none)
        artifacts, _ = audit.scan_artifacts(FIXTURES)
        markers = audit.build_marker_totals(artifacts)
        # bob should have 0 markers total
        bob_total = sum(markers.get("bob", {}).values())
        self.assertEqual(bob_total, 0)


if __name__ == "__main__":
    unittest.main()