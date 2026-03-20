"""
TajBench Sample Anonymization Mapping

Creates a deterministic mapping from real sample IDs to anonymized IDs.
The mapping is consistent across all benchmark items.

THIS FILE IS GITIGNORED — never commit the mapping or real sample names.

Usage:
    python scripts/anonymize_mapping.py

Reads:  G:/panel/final/sample_manifest.tsv
Writes: scripts/.anon_mapping.json  (gitignored)
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

MANIFEST = Path(r"G:\panel\final\sample_manifest.tsv")
OUT_PATH = Path(__file__).parent / ".anon_mapping.json"

# Prefix scheme: panel type -> anonymized prefix
PANEL_PREFIX = {
    "WGS_Reference": "WGS",
    "TrueCut_Imputed": "TC",
    "KANN_Imputed": "KN",
}


def load_manifest(path: Path) -> list[dict]:
    """Load the sample manifest TSV."""
    rows = []
    lines = path.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    for line in lines[1:]:
        if not line.strip():
            continue
        vals = line.split("\t")
        rows.append(dict(zip(header, vals)))
    return rows


def build_mapping(rows: list[dict]) -> dict:
    """
    Create a deterministic mapping: real_id -> anon_id.

    Within each panel, samples are sorted alphabetically then numbered
    sequentially. This ensures the same manifest always produces the
    same mapping.
    """
    # Group by panel
    panels: dict[str, list[str]] = {}
    for row in rows:
        panel = row.get("panel", "Unknown")
        sample_id = row["sample_id"]
        panels.setdefault(panel, []).append(sample_id)

    mapping = {}
    reverse = {}

    for panel, samples in sorted(panels.items()):
        prefix = PANEL_PREFIX.get(panel, "UNK")
        for idx, sample_id in enumerate(sorted(samples), start=1):
            anon_id = f"{prefix}_{idx:03d}"
            mapping[sample_id] = anon_id
            reverse[anon_id] = sample_id

    return {
        "real_to_anon": mapping,
        "anon_to_real": reverse,
        "panel_counts": {p: len(s) for p, s in sorted(panels.items())},
    }


def anonymize_text(text: str, mapping: dict[str, str]) -> str:
    """Replace all real sample IDs in a text string with their anon equivalents.

    Replaces longer names first to avoid partial matches.
    """
    result = text
    for real_id in sorted(mapping.keys(), key=len, reverse=True):
        result = result.replace(real_id, mapping[real_id])
    return result


def main() -> None:
    if not MANIFEST.exists():
        print(f"ERROR: Manifest not found at {MANIFEST}", file=sys.stderr)
        sys.exit(1)

    rows = load_manifest(MANIFEST)
    print(f"Loaded {len(rows)} samples from manifest")

    data = build_mapping(rows)
    print(f"Panel counts: {data['panel_counts']}")
    print(f"Total mapped: {len(data['real_to_anon'])} samples")

    OUT_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Written to {OUT_PATH}")
    print("WARNING: This file contains real sample IDs — do NOT commit it.")


if __name__ == "__main__":
    main()
