"""
Extract imputation quality (DR2/INFO) distributions from per-chromosome
Beagle imputed VCFs and write summary statistics to data/derived/imputation_qc/.

Source: d:\local\3krgp\imputation\output\chr{01-12}_imputed.vcf.gz
Requires: bcftools on PATH (or pysam if preferred)

Output:
  data/derived/imputation_qc/dr2_by_maf_bin.json    — DR2 distribution by MAF bin
  data/derived/imputation_qc/dr2_by_chromosome.json — median DR2 per chromosome
  data/derived/imputation_qc/site_counts.json        — filtered site counts
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RICE_3K = Path(r"d:\local\3krgp")
VCF_DIR = RICE_3K / "imputation" / "output"
OUT_DIR = REPO_ROOT / "data" / "derived" / "imputation_qc"

# Rice chromosomes (IRGSP-1.0 assembly)
CHROMOSOMES = [f"chr{i:02d}" for i in range(1, 13)]

MAF_BINS = [
    (0.0,  0.01, "lt_0.01"),
    (0.01, 0.05, "0.01_0.05"),
    (0.05, 0.20, "0.05_0.20"),
    (0.20, 0.50, "0.20_0.50"),
]


def _bcftools_query(vcf_path: Path, fields: str) -> list[str]:
    """Run bcftools query and return output lines."""
    cmd = ["bcftools", "query", "-f", fields, str(vcf_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        raise RuntimeError(f"bcftools error: {result.stderr[:500]}")
    return result.stdout.splitlines()


def _maf_bin(af: float) -> str | None:
    maf = min(af, 1.0 - af)
    for lo, hi, label in MAF_BINS:
        if lo <= maf < hi:
            return label
    return None


def process_chromosome(vcf_path: Path) -> dict:
    """Extract DR2 and AF per site; return bin statistics."""
    print(f"  {vcf_path.name}...", end=" ", flush=True)

    lines = _bcftools_query(vcf_path, "%AF\t%DR2\n")

    bin_dr2: dict[str, list[float]] = defaultdict(list)
    total = 0

    for line in lines:
        parts = line.strip().split("\t")
        if len(parts) < 2:
            continue
        try:
            af = float(parts[0])
            dr2 = float(parts[1])
        except ValueError:
            continue
        total += 1
        label = _maf_bin(af)
        if label:
            bin_dr2[label].append(dr2)

    stats: dict[str, dict] = {}
    for lo, hi, label in MAF_BINS:
        vals = bin_dr2[label]
        if not vals:
            stats[label] = {"n": 0}
            continue
        vals_sorted = sorted(vals)
        n = len(vals_sorted)
        stats[label] = {
            "n": n,
            "median_dr2": round(vals_sorted[n // 2], 4),
            "mean_dr2": round(sum(vals_sorted) / n, 4),
            "pct_above_0.8": round(sum(1 for v in vals_sorted if v >= 0.8) / n * 100, 2),
            "pct_above_0.9": round(sum(1 for v in vals_sorted if v >= 0.9) / n * 100, 2),
        }

    all_dr2 = [v for vals in bin_dr2.values() for v in vals]
    median_overall = sorted(all_dr2)[len(all_dr2) // 2] if all_dr2 else 0.0

    print(f"{total:,} sites, median DR2={median_overall:.3f}")
    return {"total_sites": total, "by_maf_bin": stats, "median_dr2_overall": round(median_overall, 4)}


def main() -> None:
    # Check bcftools available
    check = subprocess.run(["bcftools", "--version"], capture_output=True)
    if check.returncode != 0:
        print("ERROR: bcftools not found on PATH. Install bcftools or run on the analysis server.", file=sys.stderr)
        sys.exit(1)

    if not VCF_DIR.exists():
        print(f"ERROR: VCF directory not found: {VCF_DIR}", file=sys.stderr)
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    chr_results = {}
    combined_bins: dict[str, list] = defaultdict(list)

    for chrom in CHROMOSOMES:
        vcf = VCF_DIR / f"{chrom}_imputed.vcf.gz"
        if not vcf.exists():
            print(f"  SKIP {vcf.name} (not found)")
            continue
        result = process_chromosome(vcf)
        chr_results[chrom] = result
        for label, bin_stats in result["by_maf_bin"].items():
            if bin_stats.get("n", 0) > 0:
                combined_bins[label].append(bin_stats)

    # Aggregate across chromosomes
    aggregated = {}
    for lo, hi, label in MAF_BINS:
        all_stats = combined_bins[label]
        if not all_stats:
            continue
        total_n = sum(s["n"] for s in all_stats)
        wtd_median = sum(s["median_dr2"] * s["n"] for s in all_stats) / total_n
        wtd_pct_08 = sum(s["pct_above_0.8"] * s["n"] for s in all_stats) / total_n
        aggregated[label] = {
            "n_sites": total_n,
            "median_dr2": round(wtd_median, 4),
            "pct_above_0.8": round(wtd_pct_08, 2),
        }

    # Write outputs
    (OUT_DIR / "dr2_by_maf_bin.json").write_text(
        json.dumps({"aggregated": aggregated, "by_chromosome": chr_results}, indent=2)
    )
    print(f"\nWritten dr2_by_maf_bin.json")

    site_counts = {
        chrom: r["total_sites"] for chrom, r in chr_results.items()
    }
    site_counts["total"] = sum(site_counts.values())
    (OUT_DIR / "site_counts.json").write_text(json.dumps(site_counts, indent=2))
    print(f"Written site_counts.json  (total={site_counts['total']:,} sites)")


if __name__ == "__main__":
    main()
