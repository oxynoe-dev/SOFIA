"""constants.py — Single source of truth for H2A protocol constants.

All markers, resolutions, aliases, and frontmatter field mappings
used by scan, mirror, lens, probe, and the legacy scripts.
"""
from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Schema & SOFIA version
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1.0"


def get_instance_sofia_version(instance_path: Path) -> str:
    """Return the SOFIA protocol version from an instance's sofia.md frontmatter."""
    for name in ("sofia.md", "voix.md"):
        f = instance_path / name
        if f.is_file():
            for line in f.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("sofia:"):
                    return line.split(":", 1)[1].strip()
    return "unknown"

# ---------------------------------------------------------------------------
# Friction markers — EN canonical, icon → key
# ---------------------------------------------------------------------------

FRICTION_MARKERS = {
    "✓": "sound",
    "~": "contestable",
    "⚡": "simplification",
    "◐": "blind_spot",
    "✗": "refuted",
}

# Bracket aliases — FR→EN mapping for retrocompat (ADR-013)
FRICTION_BRACKET_ALIASES = {
    "juste": "sound",
    "angle-mort": "blind_spot",
    "faux": "refuted",
    # EN brackets map to themselves
    "sound": "sound",
    "blind_spot": "blind_spot",
    "blind-spot": "blind_spot",
    "refuted": "refuted",
    # Identical FR/EN
    "contestable": "contestable",
    "simplification": "simplification",
}

# ---------------------------------------------------------------------------
# Resolution tags
# ---------------------------------------------------------------------------

RESOLUTION_TAGS = {"ratified", "contested", "revised", "rejected"}

RESOLUTION_ALIASES = {
    "ratifie": "ratified",
    "conteste": "contested",
    "revise": "revised",
    "rejete": "rejected",
    "ratified": "ratified",
    "contested": "contested",
    "revised": "revised",
    "rejected": "rejected",
}

# ---------------------------------------------------------------------------
# Frontmatter field aliases (bilingual)
# ---------------------------------------------------------------------------

EMITTER_KEYS = {"de", "auteur", "emetteur", "from"}
RECIPIENT_KEYS = {"pour", "destinataire", "destinataires", "to", "for"}
NATURE_KEYS = {"nature", "type"}
STATUT_KEYS = {"statut", "status"}
OBJET_KEYS = {"objet", "subject", "object"}

VALID_STATUTS = {"nouveau", "lu", "traite", "new", "read", "done"}

STATUT_ALIASES = {
    "nouveau": "nouveau", "new": "nouveau",
    "lu": "lu", "read": "lu",
    "traite": "traite", "done": "traite",
}

# ---------------------------------------------------------------------------
# Direction enum (computed from initiative + marker)
# ---------------------------------------------------------------------------

DIRECTION_KEYS = [
    "a_corroborates_h",
    "a_contests_h",
    "h_corroborates_a",
    "h_contests_a",
]

# ---------------------------------------------------------------------------
# Accent stripping
# ---------------------------------------------------------------------------

_ACCENT_MAP = str.maketrans(
    "àâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ",
    "aaaeeeeiioouuycAAAEEEEIIOOUUYC",
)


def strip_accents(s: str) -> str:
    """Remove French accents from a string."""
    return s.translate(_ACCENT_MAP)

# ---------------------------------------------------------------------------
# Artifact type prefixes for audit check IDs
# ---------------------------------------------------------------------------

ARTIFACT_TYPE_PREFIXES = {
    "notes": "AN",
    "reviews": "AR",
    "features": "AF",
    "adr": "AD",
}
