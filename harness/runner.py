"""
TajBench Evaluation Runner

Usage:
  python -m harness.runner --model claude-sonnet-4-6 [options]

Options:
  --model MODEL         Model name (see harness/models/__init__.py REGISTRY)
  --items DIR           Path to benchmark items dir (default: benchmark/items/)
  --tier INT            Filter to a specific tier (1-4); default: all tiers
  --limit INT           Evaluate only the first N items (for smoke tests)
  --output FILE         Write results JSON to this path (default: auto-named)
  --dry-run             Print items without calling any model API
  --parallel INT        Number of concurrent API calls (default: 1)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Load .env from repo root if present (no hard dependency on python-dotenv)
def _load_dotenv() -> None:
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip())

_load_dotenv()
import time
from datetime import datetime, timezone

# Allow running as `python -m harness.runner` from repo root
sys.path.insert(0, str(Path(__file__).parent.parent))

from benchmark.schema import BenchmarkItem, load_corpus
from harness.models import get_adapter
from harness.scorer import score_response, ScoreResult


def _eval_single_item(
    adapter, item: BenchmarkItem, idx: int, total: int,
) -> tuple[dict | None, dict | None]:
    """Evaluate one item. Returns (result_dict, error_dict)."""
    label = f"[{idx:>3}/{total}] {item.id} (tier={item.tier}, diff={item.difficulty})"
    try:
        system, user = adapter.build_prompt(item.prompt, item.context)
        response = adapter.complete(system, user, item.id)
        score = score_response(item, response)
        pct = score.score / score.max_score
        print(f"{label} score={score.score}/3 ({pct:.0%})", flush=True)
        return ({
            "item_id": item.id,
            "tier": item.tier,
            "task_type": item.task_type,
            "data_layer": item.data_layer,
            "difficulty": item.difficulty,
            "scoring_method": item.scoring_method,
            "score": score.score,
            "max_score": score.max_score,
            "pct": pct,
            "rationale": score.rationale,
            "judge_model": score.judge_model,
            "response_text": response.response_text,
            "latency_ms": round(response.latency_ms, 1),
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
        }, None)
    except Exception as exc:
        print(f"{label} ERROR: {exc}", flush=True)
        return (None, {"item_id": item.id, "error": str(exc)})


def run_benchmark(
    model_name: str,
    items: list[BenchmarkItem],
    dry_run: bool = False,
    parallel: int = 1,
) -> dict:
    """
    Run all items against model_name.

    Returns a results dict suitable for JSON serialisation.
    """
    adapter = get_adapter(model_name) if not dry_run else None
    results = []
    errors = []

    if dry_run:
        for i, item in enumerate(items, 1):
            print(f"[{i:>3}/{len(items)}] {item.id} (tier={item.tier}, diff={item.difficulty}) (dry-run)")
    elif parallel <= 1:
        for i, item in enumerate(items, 1):
            res, err = _eval_single_item(adapter, item, i, len(items))
            if res:
                results.append(res)
            if err:
                errors.append(err)
    else:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        print(f"Running with {parallel} parallel workers\n", flush=True)
        futures = {}
        with ThreadPoolExecutor(max_workers=parallel) as pool:
            for i, item in enumerate(items, 1):
                fut = pool.submit(_eval_single_item, adapter, item, i, len(items))
                futures[fut] = item.id
            for fut in as_completed(futures):
                res, err = fut.result()
                if res:
                    results.append(res)
                if err:
                    errors.append(err)
        # Sort results by item_id for deterministic output
        results.sort(key=lambda r: r["item_id"])

    # Aggregate stats
    if results:
        overall_pct = sum(r["pct"] for r in results) / len(results)
        by_tier: dict[int, list[float]] = {}
        for r in results:
            by_tier.setdefault(r["tier"], []).append(r["pct"])
        tier_summary = {t: sum(v) / len(v) for t, v in by_tier.items()}
    else:
        overall_pct = 0.0
        tier_summary = {}

    return {
        "model": model_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "n_items": len(items),
        "n_scored": len(results),
        "n_errors": len(errors),
        "overall_pct": round(overall_pct, 4),
        "tier_summary": {f"tier{k}": round(v, 4) for k, v in sorted(tier_summary.items())},
        "results": results,
        "errors": errors,
    }


def _default_output_path(model_name: str) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = model_name.replace("/", "_").replace(":", "_")
    return Path("baselines/results") / f"{safe}_{ts}.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="TajBench evaluation runner")
    parser.add_argument("--model", required=True, help="Model name")
    parser.add_argument("--items", default="benchmark/items", help="Items directory")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4], help="Filter to tier")
    parser.add_argument("--limit", type=int, help="Max items to evaluate")
    parser.add_argument("--output", help="Output JSON path")
    parser.add_argument("--dry-run", action="store_true", help="Print items, skip API calls")
    parser.add_argument("--parallel", type=int, default=1, help="Concurrent API calls (default: 1)")
    args = parser.parse_args()

    items_dir = Path(args.items)
    if not items_dir.exists():
        print(f"Error: items directory not found: {items_dir}", file=sys.stderr)
        sys.exit(1)

    items = load_corpus(items_dir)
    if args.tier:
        items = [i for i in items if i.tier == args.tier]
    if args.limit:
        items = items[: args.limit]

    if not items:
        print("No items matched the given filters.", file=sys.stderr)
        sys.exit(1)

    print(f"\nTajBench — model={args.model}  items={len(items)}  dry_run={args.dry_run}\n")

    results = run_benchmark(args.model, items, dry_run=args.dry_run, parallel=args.parallel)

    if not args.dry_run:
        out_path = Path(args.output) if args.output else _default_output_path(args.model)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"\nResults written to {out_path}")
        print(f"Overall: {results['overall_pct']:.1%}")
        for tier_key, pct in results["tier_summary"].items():
            print(f"  {tier_key}: {pct:.1%}")


if __name__ == "__main__":
    main()
