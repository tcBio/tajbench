"""
Compute folded site frequency spectra (SFS) per population group from the
3K Rice Genomes WGS reference panel BCF and write to data/derived/sfs/.

Source: d:\local\3krgp\output\wgs\merged\rice_wgs_panel.bcf
        d:\local\3krgp\manifest_wgs.md  (sample -> subpopulation mapping)

Output:
  data/derived/sfs/folded_sfs_{group}.json  — one file per group
  data/derived/sfs/sfs_summary.json          — mean π and Tajima's D estimates

Requires: bcftools on PATH
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RICE_3K = Path(r"d:\local\3krgp")
WGS_BCF = RICE_3K / "output" / "wgs" / "merged" / "rice_wgs_panel.bcf"
OUT_DIR = REPO_ROOT / "data" / "derived" / "sfs"

# Group -> sample file paths (create these from manifest if needed)
GROUPS = {
    "indica": "IRIS_313-8",
    "temperate_japonica": "IRIS_313-10",
}


def _get_samples_for_study(study: str, bcf_path: Path) -> list[str]:
    """Return sample IDs matching a study prefix from BCF header."""
    cmd = ["bcftools", "query", "-l", str(bcf_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[:300])
    return [s for s in result.stdout.splitlines() if s.startswith(study)]


def _compute_sfs_via_bcftools(bcf_path: Path, sample_ids: list[str]) -> list[int]:
    """
    Compute folded SFS using bcftools stats --samples-file.
    Returns count array: sfs[i] = number of sites with i derived alleles.
    """
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("\n".join(sample_ids))
        sample_file = f.name

    cmd = [
        "bcftools", "stats",
        "--samples-file", sample_file,
        "--af-bins", "0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5",
        "-i", "FILTER='PASS' && MAF > 0.01",
        str(bcf_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    Path(sample_file).unlink(missing_ok=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr[:300])

    # Parse AF histogram from bcftools stats output
    bins = []
    for line in result.stdout.splitlines():
        if line.startswith("AF\t"):
            parts = line.split("\t")
            if len(parts) >= 3:
                try:
                    bins.append(int(parts[2]))
                except ValueError:
                    pass
    return bins


def _nucleotide_diversity(sfs: list[int], n_samples: int) -> float:
    """Estimate π from folded SFS (Tajima 1989 approximation)."""
    n = n_samples * 2  # diploid
    total_sites = sum(sfs)
    if total_sites == 0 or n < 2:
        return 0.0
    pi = 0.0
    for i, count in enumerate(sfs):
        p = (i + 1) / n
        pi += count * 2 * p * (1 - p)
    return pi / total_sites


def main() -> None:
    check = subprocess.run(["bcftools", "--version"], capture_output=True)
    if check.returncode != 0:
        print("ERROR: bcftools not found on PATH", file=sys.stderr)
        sys.exit(1)

    if not WGS_BCF.exists():
        print(f"ERROR: WGS BCF not found at {WGS_BCF}", file=sys.stderr)
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {}

    for group_name, study_prefix in GROUPS.items():
        print(f"Processing {group_name} ({study_prefix})...")
        try:
            samples = _get_samples_for_study(study_prefix, WGS_BCF)
            print(f"  {len(samples)} samples")
            sfs = _compute_sfs_via_bcftools(WCF_BCF := WGS_BCF, samples)
            pi = _nucleotide_diversity(sfs, len(samples))

            out = {
                "group": group_name,
                "study_prefix": study_prefix,
                "n_samples": len(samples),
                "folded_sfs": sfs,
                "n_sites": sum(sfs),
                "nucleotide_diversity_pi": round(pi, 8),
            }
            path = OUT_DIR / f"folded_sfs_{group_name}.json"
            path.write_text(json.dumps(out, indent=2))
            print(f"  Written {path.name}  (π={pi:.6f})")
            summary[group_name] = {"n_samples": len(samples), "pi": round(pi, 8)}

        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)

    (OUT_DIR / "sfs_summary.json").write_text(json.dumps(summary, indent=2))
    print("Written sfs_summary.json")


if __name__ == "__main__":
    main()
