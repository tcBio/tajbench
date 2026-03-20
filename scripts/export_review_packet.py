#!/usr/bin/env python3
"""Export a review packet for domain-expert review of all TajBench items.

Reads every benchmark item and produces a clean Markdown file grouped by tier,
suitable for offline review by a domain expert (Anna).

Usage:
    python scripts/export_review_packet.py
"""

from __future__ import annotations

import sys
import textwrap
from collections import defaultdict
from datetime import date
from pathlib import Path

# Ensure the project root is on sys.path so we can import benchmark.schema
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from benchmark.schema import BenchmarkItem, load_corpus

ITEMS_DIR = PROJECT_ROOT / "benchmark" / "items"
OUTPUT_PATH = PROJECT_ROOT / "baselines" / "anna_review_packet.md"

TIER_LABELS = {
    1: "Tier 1 -- Parsing",
    2: "Tier 2 -- Statistics",
    3: "Tier 3 -- Structure",
    4: "Tier 4 -- Methods",
}


def render_item(item: BenchmarkItem) -> str:
    """Render a single benchmark item as a Markdown section."""
    lines: list[str] = []

    lines.append("---")
    lines.append(f"### {item.id}")
    lines.append(
        f"**Tier**: {item.tier} | "
        f"**Difficulty**: {item.difficulty} | "
        f"**Type**: {item.task_type} | "
        f"**Scoring**: {item.scoring_method} | "
        f"**Data**: {item.data_layer}"
    )
    lines.append("")

    # Prompt -- block-quoted so long text wraps nicely
    lines.append("**PROMPT:**")
    for para in item.prompt.strip().splitlines():
        lines.append(f"> {para}")
    lines.append("")

    # Context -- fenced code block to preserve whitespace / tables
    lines.append("**CONTEXT:**")
    lines.append("```")
    lines.append(item.context.strip())
    lines.append("```")
    lines.append("")

    # Correct answer
    lines.append("**CORRECT ANSWER:**")
    lines.append(item.correct_answer.strip())
    lines.append("")

    # Rubric
    lines.append("**RUBRIC:**")
    lines.append(item.rubric.strip())
    lines.append("")

    # Notes (only if non-empty)
    if item.notes and item.notes.strip():
        lines.append(f"**NOTES:** {item.notes.strip()}")
        lines.append("")

    # Review checkboxes
    lines.append("**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut")
    lines.append("**Comments:** _______________")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    # Load all items
    items = load_corpus(ITEMS_DIR)
    if not items:
        print("ERROR: No items found in", ITEMS_DIR, file=sys.stderr)
        sys.exit(1)

    # Group by tier
    by_tier: dict[int, list[BenchmarkItem]] = defaultdict(list)
    for item in items:
        by_tier[item.tier].append(item)

    # Build the full document
    doc: list[str] = []
    doc.append("# TajBench -- Domain Expert Review Packet")
    doc.append("")
    doc.append(f"**Reviewer:** Anna (domain expert)")
    doc.append(f"**Generated:** {date.today().isoformat()}")
    doc.append(f"**Total items:** {len(items)}")
    doc.append("")

    # Summary table
    doc.append("## Summary")
    doc.append("")
    doc.append("| Tier | Label | Count |")
    doc.append("|------|-------|-------|")
    for tier_num in sorted(by_tier):
        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
        doc.append(f"| {tier_num} | {label} | {len(by_tier[tier_num])} |")
    doc.append("")

    # Render each tier
    for tier_num in sorted(by_tier):
        label = TIER_LABELS.get(tier_num, f"Tier {tier_num}")
        doc.append(f"## {label} ({len(by_tier[tier_num])} items)")
        doc.append("")
        for item in by_tier[tier_num]:
            doc.append(render_item(item))

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(doc), encoding="utf-8")
    print(f"Review packet written to {OUTPUT_PATH}")
    print(f"  {len(items)} items across {len(by_tier)} tiers")


if __name__ == "__main__":
    main()
