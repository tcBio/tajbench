"""Tests for harness.scorer — exact match and regex match scoring (no API calls)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from benchmark.schema import BenchmarkItem
from harness.models.base import ModelResponse
from harness.scorer import ScoreResult, _normalise, score_response


def _item(**overrides) -> BenchmarkItem:
    defaults = dict(
        id="tier1_vcf_999",
        tier=1,
        task_type="parsing",
        data_layer="wgs",
        difficulty=1,
        prompt="What is the REF allele?",
        context="REF=A",
        correct_answer="A",
        rubric="REF must be A",
        source_method="GLnexus",
        population_groups=["indica"],
        scoring_method="exact_match",
        answer_pattern="",
    )
    defaults.update(overrides)
    return BenchmarkItem(**defaults)


def _response(text: str, item_id: str = "tier1_vcf_999") -> ModelResponse:
    return ModelResponse(
        model="test-model",
        item_id=item_id,
        response_text=text,
        latency_ms=100.0,
    )


# ── Normalisation ─────────────────────────────────────────────────────────────

class TestNormalise:
    def test_strips_whitespace(self):
        assert _normalise("  A  ") == "a"

    def test_collapses_internal_whitespace(self):
        assert _normalise("A\t B") == "a b"

    def test_lowercases(self):
        assert _normalise("REF=G") == "ref=g"


# ── Exact match ───────────────────────────────────────────────────────────────

class TestExactMatch:
    def test_correct_answer_scores_3(self):
        item = _item(correct_answer="A", scoring_method="exact_match")
        result = score_response(item, _response("A"))
        assert result.score == 3
        assert result.max_score == 3

    def test_wrong_answer_scores_0(self):
        item = _item(correct_answer="A", scoring_method="exact_match")
        result = score_response(item, _response("G"))
        assert result.score == 0

    def test_case_insensitive(self):
        item = _item(correct_answer="pass", scoring_method="exact_match")
        result = score_response(item, _response("PASS"))
        assert result.score == 3

    def test_extra_whitespace_ignored(self):
        item = _item(correct_answer="REF=G", scoring_method="exact_match")
        result = score_response(item, _response("  ref=g  "))
        assert result.score == 3


# ── Regex match ───────────────────────────────────────────────────────────────

class TestRegexMatch:
    def test_pattern_found_scores_3(self):
        item = _item(scoring_method="regex_match", answer_pattern=r"DR2=0\.\d+")
        result = score_response(item, _response("The site has DR2=0.723 which is below 0.8"))
        assert result.score == 3

    def test_pattern_not_found_scores_0(self):
        item = _item(scoring_method="regex_match", answer_pattern=r"DR2=0\.\d+")
        result = score_response(item, _response("There is no quality score mentioned"))
        assert result.score == 0

    def test_case_insensitive_flag(self):
        item = _item(scoring_method="regex_match", answer_pattern=r"pass")
        result = score_response(item, _response("The filter is PASS"))
        assert result.score == 3


# ── LLM judge (mocked) ────────────────────────────────────────────────────────

class TestLLMJudge:
    def _mock_claude(self, score: int, rationale: str):
        import json
        mock_client = MagicMock()
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text=json.dumps({"score": score, "rationale": rationale}))]
        mock_client.messages.create.return_value = mock_msg
        return mock_client

    def test_llm_judge_returns_score_result(self):
        item = _item(
            id="tier3_pca_999",
            tier=3,
            scoring_method="llm_judge",
            correct_answer="PC1 separates indica from japonica.",
            rubric="Must identify PC1 axis correctly.",
        )
        mock_client = self._mock_claude(3, "Correct identification of PC1.")
        with patch("harness.scorer.anthropic.Anthropic", return_value=mock_client):
            result = score_response(item, _response("PC1 separates indica from japonica subpopulations."))
        assert isinstance(result, ScoreResult)
        assert result.score == 3
        assert result.scoring_method == "llm_judge"

    def test_llm_judge_score_clamped(self):
        item = _item(tier=2, id="tier2_fst_999", scoring_method="llm_judge",
                     correct_answer="x", rubric="y")
        mock_client = self._mock_claude(5, "Out of range")  # score=5 should clamp to 3
        with patch("harness.scorer.anthropic.Anthropic", return_value=mock_client):
            result = score_response(item, _response("some answer"))
        assert result.score == 3

    def test_llm_judge_bad_json_fallback(self):
        item = _item(tier=2, id="tier2_fst_999", scoring_method="llm_judge",
                     correct_answer="x", rubric="y")
        mock_client = MagicMock()
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text='{"score": 2, malformed json')]
        mock_client.messages.create.return_value = mock_msg
        with patch("harness.scorer.anthropic.Anthropic", return_value=mock_client):
            result = score_response(item, _response("some answer"))
        assert 0 <= result.score <= 3  # fallback should not crash


# ── Unknown method ─────────────────────────────────────────────────────────────

class TestUnknownMethod:
    def test_raises_value_error(self):
        item = _item(scoring_method="unknown_method")
        with pytest.raises(ValueError, match="Unknown scoring_method"):
            score_response(item, _response("answer"))
