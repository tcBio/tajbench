"""Quick analysis of baseline results to identify hard items and scoring patterns."""
import json
from pathlib import Path

FILES = {
    "opus": Path(r"baselines\results\claude-opus-4-6_20260319_214852.json"),
    "sonnet": Path(r"baselines\results\claude-sonnet-4-6_20260319_214525.json"),
    "o3": Path(r"baselines\results\o3_20260319_215221.json"),
    "gpt4o": Path(r"baselines\results\gpt-4o_20260319_215325.json"),
}

scores = {}
all_items = set()
for model, fpath in FILES.items():
    data = json.loads(fpath.read_text())
    for r in data["results"]:
        all_items.add(r["item_id"])
        scores[(model, r["item_id"])] = (r["score"], r.get("rationale", ""))

models = ["opus", "sonnet", "o3", "gpt4o"]
header = f"{'Item':<30} {'Opus':>4} {'Son':>4} {'o3':>4} {'4o':>4}  {'Mean':>5}"
print(header)
print("-" * len(header))
for item in sorted(all_items):
    ss = [scores.get((m, item), (None, ""))[0] for m in models]
    if any(s is not None and s < 3 for s in ss):
        vals = [s for s in ss if s is not None]
        mean = sum(vals) / len(vals) if vals else 0
        row = "  ".join(f"{s if s is not None else '?':>4}" for s in ss)
        print(f"{item:<30} {row}  {mean:>5.2f}")

print("\n\n=== Items scored < 3 by Claude models (potential judge bias or genuine difficulty) ===")
for item in sorted(all_items):
    for m in ["opus", "sonnet"]:
        s, rat = scores.get((m, item), (3, ""))
        if s < 3:
            print(f"\n{m} | {item} | score={s}/3")
            print(f"  Rationale: {rat[:200]}")

print("\n\n=== o3 low scores (items Claude aces but o3 misses) ===")
for item in sorted(all_items):
    o3_s = scores.get(("o3", item), (3, ""))[0]
    opus_s = scores.get(("opus", item), (3, ""))[0]
    if o3_s < 3 and opus_s == 3:
        rat = scores.get(("o3", item), (3, ""))[1]
        print(f"\no3 | {item} | score={o3_s}/3 (Opus got 3)")
        print(f"  Rationale: {rat[:200]}")
