"""Tests for benchmark.schema — item validation and corpus loading."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from benchmark.schema import BenchmarkItem, corpus_stats, load_corpus, validate_corpus

ITEMS_DIR = Path(__file__).parent.parent / "benchmark" / "items"


# ── Fixtures ────────────────────────────────────────────────────────────────

def _make_item(**overrides) -> BenchmarkItem:
    defaults = dict(
        id="tier1_vcf_999",
        tier=1,
        task_type="parsing",
        data_layer="wgs",
        difficulty=1,
        prompt="What is the REF allele?",
        context="chr01\t100\t.\tA\tT\t.\tPASS\t.\tGT\t0/1",
        correct_answer="A",
        rubric="REF must be A",
        source_method="GATK",
        population_groups=["indica"],
        scoring_method="exact_match",
    )
    defaults.update(overrides)
    return BenchmarkItem(**defaults)


# ── Validation tests ─────────────────────────────────────────────────────────

class TestItemValidation:
    def test_valid_item_no_errors(self):
        item = _make_item()
        assert item.validate() == []

    def test_bad_id_format(self):
        item = _make_item(id="bad_id")
        errs = item.validate()
        assert any("id" in e for e in errs)

    def test_empty_prompt(self):
        item = _make_item(prompt="   ")
        errs = item.validate()
        assert any("prompt" in e for e in errs)

    def test_empty_correct_answer(self):
        item = _make_item(correct_answer="")
        errs = item.validate()
        assert any("correct_answer" in e for e in errs)

    def test_regex_match_requires_pattern(self):
        item = _make_item(scoring_method="regex_match", answer_pattern="")
        errs = item.validate()
        assert any("answer_pattern" in e for e in errs)

    def test_regex_match_with_pattern_valid(self):
        item = _make_item(scoring_method="regex_match", answer_pattern=r"0\.375")
        assert item.validate() == []

    def test_exact_match_on_tier2_warns(self):
        item = _make_item(id="tier2_fst_999", tier=2, scoring_method="exact_match")
        errs = item.validate()
        assert any("tier 2" in e for e in errs)

    def test_empty_population_groups(self):
        item = _make_item(population_groups=[])
        errs = item.validate()
        assert any("population_groups" in e for e in errs)


# ── Serialisation round-trip ─────────────────────────────────────────────────

class TestSerialisation:
    def test_dict_roundtrip(self):
        item = _make_item()
        reconstructed = BenchmarkItem.from_dict(item.to_dict())
        assert reconstructed == item

    def test_json_roundtrip(self):
        item = _make_item()
        reconstructed = BenchmarkItem.from_json(item.to_json())
        assert reconstructed == item

    def test_json_is_valid_json(self):
        item = _make_item()
        parsed = json.loads(item.to_json())
        assert parsed["id"] == "tier1_vcf_999"
        assert parsed["tier"] == 1


# ── Corpus loading ───────────────────────────────────────────────────────────

class TestCorpusLoading:
    def test_load_seed_corpus(self):
        items = load_corpus(ITEMS_DIR)
        assert len(items) >= 200, "Expect at least 200 items for v1.0"

    def test_all_tiers_present(self):
        items = load_corpus(ITEMS_DIR)
        tiers = {i.tier for i in items}
        assert tiers == {1, 2, 3, 4}

    def test_validate_corpus_passes(self):
        failures = validate_corpus(ITEMS_DIR)
        assert failures == {}, f"Corpus validation errors: {failures}"

    def test_corpus_stats_keys(self):
        items = load_corpus(ITEMS_DIR)
        stats = corpus_stats(items)
        assert "total" in stats
        assert "by_tier" in stats
        assert "by_scoring_method" in stats

    def test_no_duplicate_ids(self):
        items = load_corpus(ITEMS_DIR)
        ids = [i.id for i in items]
        assert len(ids) == len(set(ids)), f"Duplicate item IDs: {[x for x in ids if ids.count(x) > 1]}"


# ── Runner dry-run ──────────────────────────────────────────────────────────

class TestRunnerDryRun:
    def test_dry_run_completes(self):
        """Smoke test: dry-run should complete without API calls."""
        from harness.runner import run_benchmark
        items = load_corpus(ITEMS_DIR)
        # Use only 3 items to keep the test fast
        result = run_benchmark("test-model", items[:3], dry_run=True)
        assert result["model"] == "test-model"
        assert result["n_items"] == 3
        assert result["n_scored"] == 0  # dry-run produces no scores
        assert result["n_errors"] == 0
