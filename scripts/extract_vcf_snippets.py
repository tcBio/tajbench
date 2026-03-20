"""
Extract and anonymise short VCF record excerpts for Tier 1 benchmark items.

Pulls representative records from the 3K RGP joint VCF, anonymises sample IDs,
and writes them as formatted text files suitable for embedding in item context fields.

Source: d:\local\3krgp\output\wgs\merged\rice_wgs_panel.bcf
Output: data/derived/vcf_snippets/  (one .txt per snippet type)

Snippet types produced:
  multiallelic.txt    — multi-allelic sites with AC/AN/AF for Tier 1 parsing
  imputed_dr2.txt     — imputed records with DR2/GP fields
  missing_gt.txt      — sites with ./. missing genotypes for AF calculation tasks
"""

from __future__ import annotations

import random
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RICE_3K = Path(r"d:\local\3krgp")
WGS_BCF = RICE_3K / "output" / "wgs" / "merged" / "rice_wgs_panel.bcf"
IMPUTED_VCF = RICE_3K / "imputation" / "output" / "chr01_imputed.vcf.gz"
OUT_DIR = REPO_ROOT / "data" / "derived" / "vcf_snippets"

N_SAMPLES_SHOW = 5  # Show only this many samples per snippet (anonymised)
RANDOM_SEED = 42


def _bcftools_view(vcf_path: Path, filters: list[str], region: str = "", n: int = 20) -> str:
    cmd = ["bcftools", "view", "--no-version"]
    for f in filters:
        cmd += ["-i", f]
    if region:
        cmd += ["-r", region]
    cmd.append(str(vcf_path))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[:500])
    lines = result.stdout.splitlines()
    # Keep header + first n data lines
    header = [l for l in lines if l.startswith("#")]
    data = [l for l in lines if not l.startswith("#")][:n]
    return "\n".join(header + data)


def anonymise_sample_ids(vcf_text: str, n_show: int = N_SAMPLES_SHOW) -> str:
    """Replace real sample IDs in the VCF header and data with S001, S002, ..."""
    lines = vcf_text.splitlines()
    chrom_line = None
    for i, line in enumerate(lines):
        if line.startswith("#CHROM"):
            chrom_line = i
            break
    if chrom_line is None:
        return vcf_text

    header_parts = lines[chrom_line].split("\t")
    fixed = header_parts[:9]
    samples = header_parts[9:]

    # Pick n_show samples deterministically
    rng = random.Random(RANDOM_SEED)
    chosen_indices = sorted(rng.sample(range(len(samples)), min(n_show, len(samples))))
    anon_names = [f"S{i+1:03d}" for i in range(len(chosen_indices))]

    new_header = "\t".join(fixed + anon_names)
    new_lines = [lines[chrom_line - j] if j > 0 else new_header
                 for j in range(len(lines) - chrom_line, -1, -1)]

    # Rebuild: keep lines before CHROM unchanged, replace CHROM line, subset data cols
    result = lines[:chrom_line] + [new_header]
    for line in lines[chrom_line + 1:]:
        if line.startswith("#"):
            result.append(line)
            continue
        parts = line.split("\t")
        fixed_cols = parts[:9]
        sample_cols = [parts[9 + idx] for idx in chosen_indices if 9 + idx < len(parts)]
        result.append("\t".join(fixed_cols + sample_cols))

    return "\n".join(result)


def write_snippet(name: str, content: str) -> None:
    out = OUT_DIR / f"{name}.txt"
    out.write_text(content, encoding="utf-8")
    n_records = len([l for l in content.splitlines() if l and not l.startswith("#")])
    print(f"  Written {out.name}  ({n_records} records)")


def main() -> None:
    check = subprocess.run(["bcftools", "--version"], capture_output=True)
    if check.returncode != 0:
        print("ERROR: bcftools not found on PATH", file=sys.stderr)
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Extracting multi-allelic snippet...")
    try:
        raw = _bcftools_view(WGS_BCF, ["N_ALT > 1", 'FILTER="PASS"'], n=8)
        anon = anonymise_sample_ids(raw)
        write_snippet("multiallelic", anon)
    except Exception as e:
        print(f"  SKIP (bcftools error): {e}")

    print("Extracting missing-genotype snippet...")
    try:
        # Sites where at least one sample has missing GT
        raw = _bcftools_view(WGS_BCF, ['GT[*]="mis"', 'FILTER="PASS"', "MAF > 0.05"], n=6)
        anon = anonymise_sample_ids(raw)
        write_snippet("missing_gt", anon)
    except Exception as e:
        print(f"  SKIP (bcftools error): {e}")

    print("Extracting imputed DR2 snippet...")
    try:
        raw = _bcftools_view(
            IMPUTED_VCF,
            ["INFO/DR2 > 0.3", "INFO/DR2 < 0.9", "MAF > 0.05"],
            region="chr01:1000000-2000000",
            n=6,
        )
        anon = anonymise_sample_ids(raw)
        write_snippet("imputed_dr2", anon)
    except Exception as e:
        print(f"  SKIP (bcftools error): {e}")

    print("Done.")


if __name__ == "__main__":
    main()
