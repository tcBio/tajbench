"""
TajBench Scorer

Scores a ModelResponse against a BenchmarkItem using the method
specified in item.scoring_method:

  exact_match  — normalised string equality
  regex_match  — item.answer_pattern must match anywhere in response
  llm_judge    — Claude grades the response against item.rubric (0-3 scale)
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass

import anthropic

from benchmark.schema import BenchmarkItem
from harness.models.base import ModelResponse

JUDGE_MODEL = "claude-sonnet-4-6"

JUDGE_SYSTEM = """\
You are an expert population geneticist evaluating an AI assistant's answer to a \
genomics benchmark question. Score the answer using the provided rubric on a \
0–3 integer scale:

  3 — Fully correct: all key points addressed, no factual errors
  2 — Mostly correct: main insight correct, minor omissions or imprecision
  1 — Partially correct: some relevant content but significant errors or gaps
  0 — Incorrect or irrelevant

Return ONLY a JSON object with two keys:
  {"score": <int 0-3>, "rationale": "<one sentence>"}
Do not include any other text.
"""


@dataclass
class ScoreResult:
    item_id: str
    scoring_method: str
    score: int          # 0-3 for llm_judge; 0 or 3 for exact/regex
    max_score: int      # always 3
    rationale: str
    judge_model: str = ""


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def score_response(item: BenchmarkItem, response: ModelResponse) -> ScoreResult:
    method = item.scoring_method

    if method == "exact_match":
        norm_resp = _normalise(response.response_text)
        norm_ans = _normalise(item.correct_answer)
        match = norm_ans in norm_resp
        return ScoreResult(
            item_id=item.id,
            scoring_method=method,
            score=3 if match else 0,
            max_score=3,
            rationale="Exact match" if match else "No exact match",
        )

    if method == "regex_match":
        found = re.search(item.answer_pattern, response.response_text, re.IGNORECASE | re.DOTALL)
        return ScoreResult(
            item_id=item.id,
            scoring_method=method,
            score=3 if found else 0,
            max_score=3,
            rationale=f"Pattern matched: {found.group()}" if found else "Pattern not found",
        )

    if method == "llm_judge":
        return _llm_judge(item, response)

    raise ValueError(f"Unknown scoring_method: {method!r}")


def _llm_judge(item: BenchmarkItem, response: ModelResponse) -> ScoreResult:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    user_prompt = f"""\
QUESTION:
{item.prompt}

DATA CONTEXT:
{item.context}

CORRECT ANSWER (rubric):
{item.correct_answer}

RUBRIC CRITERIA:
{item.rubric}

MODEL ANSWER TO EVALUATE:
{response.response_text}
"""

    msg = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=256,
        system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = msg.content[0].text.strip()
    try:
        parsed = json.loads(raw)
        score = int(parsed["score"])
        rationale = str(parsed["rationale"])
    except Exception:
        # Fallback: try to extract score integer from text
        m = re.search(r'"score"\s*:\s*([0-3])', raw)
        score = int(m.group(1)) if m else 0
        rationale = f"Parse error; raw judge output: {raw[:200]}"

    return ScoreResult(
        item_id=item.id,
        scoring_method="llm_judge",
        score=max(0, min(3, score)),
        max_score=3,
        rationale=rationale,
        judge_model=JUDGE_MODEL,
    )
