"""Audit judge scoring for bias -- compare rationales across models for key items."""
import json
from pathlib import Path

FILES = {
    "opus": Path(r"baselines\results\claude-opus-4-6_20260319_214852.json"),
    "sonnet": Path(r"baselines\results\claude-sonnet-4-6_20260319_214525.json"),
    "o3": Path(r"baselines\results\o3_20260319_215221.json"),
    "gpt4o": Path(r"baselines\results\gpt-4o_20260319_215325.json"),
}

FOCUS_ITEMS = [
    "tier2_fst_002",      # Sonnet 0, Opus 3, o3 3, gpt4o 2
    "tier4_method_011",   # Sonnet 1, Opus 2, o3 0, gpt4o 1
    "tier4_method_012",   # Sonnet 0, Opus 2, o3 3, gpt4o 2
    "tier2_kinship_001",  # o3 1, gpt4o 2, Opus 2, Sonnet 3
]

data = {}
for model, fpath in FILES.items():
    data[model] = {r["item_id"]: r for r in json.loads(fpath.read_text())["results"]}

sep = "=" * 80
for item_id in FOCUS_ITEMS:
    print(f"\n{sep}")
    print(f"ITEM: {item_id}")
    print(sep)
    for model in ["opus", "sonnet", "o3", "gpt4o"]:
        r = data[model].get(item_id)
        if not r:
            continue
        print(f"\n--- {model} | score={r['score']}/3 ---")
        print(f"Rationale: {r['rationale'][:400]}")
        print(f"Response (first 300 chars): {r['response_text'][:300]}...")
