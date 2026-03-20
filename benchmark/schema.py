"""
TajBench Item Schema

Each benchmark item is a dict conforming to BenchmarkItem.
Items are stored as JSON files in benchmark/items/tier{N}_*/
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Literal

# ── Types ──────────────────────────────────────────────────────────────────

Tier = Literal[1, 2, 3, 4]
TaskType = Literal["parsing", "interpretation", "comparison", "decision"]
DataLayer = Literal["wgs", "rad_gbs", "imputed", "derived", "methodology"]
Difficulty = Literal[1, 2, 3]
ScoringMethod = Literal["exact_match", "regex_match", "llm_judge"]


@dataclass
class BenchmarkItem:
    """Single evaluation item in the TajBench benchmark."""

    # Identity
    id: str                          # e.g. "tier3_pca_001"
    tier: Tier                       # 1=parsing, 2=stats, 3=structure, 4=methods
    task_type: TaskType
    data_layer: DataLayer
    difficulty: Difficulty           # 1=textbook, 2=contextual, 3=expert judgment

    # Content
    prompt: str                      # Instruction shown to the model
    context: str                     # Data excerpt (VCF snippet, PCA coords, etc.)
    correct_answer: str              # Rubric-defined correct answer (not shown to model)
    rubric: str                      # Scoring criteria (used by LLM judge)

    # Metadata
    source_method: str               # e.g. "PCAngsd", "Beagle5.4", "GLnexus"
    population_groups: list[str]     # e.g. ["indica", "tropical-japonica"]
    scoring_method: ScoringMethod    # how this item is scored
    answer_pattern: str = ""         # regex for regex_match items; empty otherwise

    # Optional free-form notes (not used in scoring)
    notes: str = ""

    # ── Validation ──────────────────────────────────────────────────────────

    def validate(self) -> list[str]:
        """Return list of validation errors; empty list means valid."""
        errors: list[str] = []

        if not re.match(r"^tier[1-4]_\w+_\d{3}$", self.id):
            errors.append(f"id '{self.id}' must match tier{{N}}_<topic>_{{NNN}}")

        if not self.prompt.strip():
            errors.append("prompt is empty")

        if not self.context.strip():
            errors.append("context is empty")

        if not self.correct_answer.strip():
            errors.append("correct_answer is empty")

        if not self.rubric.strip():
            errors.append("rubric is empty")

        if self.scoring_method == "regex_match" and not self.answer_pattern:
            errors.append("regex_match items require a non-empty answer_pattern")

        if self.scoring_method == "exact_match" and self.tier > 1:
            errors.append(f"tier {self.tier} items should use llm_judge, not exact_match")

        if not self.population_groups:
            errors.append("population_groups must not be empty")

        return errors

    # ── Serialisation ───────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, d: dict) -> "BenchmarkItem":
        return cls(**d)

    @classmethod
    def from_json(cls, s: str) -> "BenchmarkItem":
        return cls.from_dict(json.loads(s))

    @classmethod
    def from_file(cls, path: Path) -> "BenchmarkItem":
        return cls.from_json(path.read_text(encoding="utf-8"))


# ── Corpus helpers ──────────────────────────────────────────────────────────

def load_corpus(items_dir: Path) -> list[BenchmarkItem]:
    """Load all *.json item files from the benchmark/items/ tree."""
    items = []
    for path in sorted(items_dir.rglob("*.json")):
        items.append(BenchmarkItem.from_file(path))
    return items


def validate_corpus(items_dir: Path) -> dict[str, list[str]]:
    """Validate every item; return {id: [errors]} for any invalid items."""
    failures: dict[str, list[str]] = {}
    for path in sorted(items_dir.rglob("*.json")):
        try:
            item = BenchmarkItem.from_file(path)
            errs = item.validate()
            if errs:
                failures[str(path)] = errs
        except Exception as exc:
            failures[str(path)] = [f"Parse error: {exc}"]
    return failures


def corpus_stats(items: list[BenchmarkItem]) -> dict:
    """Return summary statistics over a loaded corpus."""
    from collections import Counter
    return {
        "total": len(items),
        "by_tier": dict(Counter(i.tier for i in items)),
        "by_task_type": dict(Counter(i.task_type for i in items)),
        "by_data_layer": dict(Counter(i.data_layer for i in items)),
        "by_difficulty": dict(Counter(i.difficulty for i in items)),
        "by_scoring_method": dict(Counter(i.scoring_method for i in items)),
    }


# ── CLI entry point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    items_dir = Path(__file__).parent / "items"
    failures = validate_corpus(items_dir)

    if failures:
        print(f"VALIDATION FAILED — {len(failures)} item(s) with errors:\n")
        for path, errs in failures.items():
            print(f"  {path}")
            for e in errs:
                print(f"    • {e}")
        sys.exit(1)

    items = load_corpus(items_dir)
    stats = corpus_stats(items)
    print(f"TajBench corpus valid — {stats['total']} items")
    for k, v in stats.items():
        if k != "total":
            print(f"  {k}: {v}")
