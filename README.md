# TajBench

**Rigorous population genomics reasoning evaluation for frontier LLMs**

An open benchmark for evaluating frontier LLMs on plant population genomics reasoning -- built on the 3,000 Rice Genomes Project (3,010 accessions, ~18M SNPs across 12 chromosomes) and grounded in peer-reviewed methodology.

> **Why TajBench?** Frontier models plateau on standard bioinformatics Q&A but struggle with interpretive reasoning over real population genetics data -- FST matrices, PCA projections, Tajima's D distributions, imputation quality stratification. TajBench exposes these failure modes with 200 items across four difficulty tiers, scored by deterministic matching and calibrated LLM-as-judge rubrics. If your model can't read a VCF or reason about domestication signals in an SFS, this benchmark will show it.

---

## Leaderboard

*v0.3 -- 59 items, evaluated March 2026. Baselines pending re-run on v1.0 (202 items).*

| Model | Tier 1 (Parsing) | Tier 2 (Statistics) | Tier 3 (Structure) | Tier 4 (Methods) | **Overall** |
|-------|:---:|:---:|:---:|:---:|:---:|
| Claude Opus 4.6 | 100.0% | 94.4% | 98.2% | 86.1% | **94.9%** |
| Claude Sonnet 4.6 | 100.0% | 88.9% | 96.5% | 80.6% | **91.5%** |
| o3 | 90.0% | 85.2% | 93.0% | 66.7% | **84.8%** |
| GPT-4o | 70.0% | 61.1% | 61.4% | 58.3% | **62.2%** |
| Gemini 2.5 Pro | -- | -- | -- | -- | -- |
| Gemini 2.5 Flash | -- | -- | -- | -- | -- |

*Scores are mean fraction of maximum score (0-3 per item). Full results in [`baselines/results/`](baselines/results/). v1.0 corpus: 202 items (55 T1, 57 T2, 55 T3, 35 T4).*

---

## Benchmark Design

TajBench evaluates LLMs across four tiers of genomic reasoning, ordered by interpretive difficulty:

### Tier 1 -- Parsing & Structural Understanding
**Scoring**: Exact/regex match | **Target items**: 55

VCF/BCF format comprehension: multi-allelic records, FORMAT field extraction, INFO field parsing, filter flag interpretation, missing genotype handling, imputation quality scores (DR2/INFO).

### Tier 2 -- Diversity & Differentiation Statistics
**Scoring**: LLM-as-judge | **Target items**: 55

FST matrix interpretation, nucleotide diversity (pi), Tajima's D inference in domestication context, LD decay reasoning, imputation quality (DR2) stratification by MAF, site frequency spectrum interpretation.

### Tier 3 -- Population Structure
**Scoring**: LLM-as-judge | **Target items**: 55

PCA output interpretation, batch effect vs. real structure discrimination, ADMIXTURE Q-matrix reading, indica-japonica differentiation, subpopulation assignment logic.

### Tier 4 -- Methodological Decision-Making
**Scoring**: LLM-as-judge | **Target items**: 35

When to use PCAngsd vs. PLINK PCA, GBS vs. WGS tradeoffs for population inference, Beagle imputation strategy, LD pruning for structure analyses, MAF filtering decisions.

---

## Dataset

TajBench is grounded in the 3,000 Rice Genomes Project:

- **3,010 accessions** from 89 countries (Oryza sativa L.)
- **~18M SNPs** across 12 chromosomes (IRGSP-1.0 assembly, ~390 Mb genome)
- **Five major subpopulations**: indica, tropical japonica, temperate japonica, aus, aromatic + admixed
- **Sequencing**: Illumina WGS at ~14x average depth
- **Pipeline**: BWA-MEM -> GATK HaplotypeCaller -> SNP filtering -> ADMIXTURE / PCA
- **Public access**: AWS S3 (`s3://3kricegenome/`), SRA PRJEB6180

Public-safe derived artifacts (PCA coordinates, VCF snippets, SFS, FST matrices) are in [`data/derived/`](data/derived/).
Full dataset access: see [`data/DATA_ACCESS.md`](data/DATA_ACCESS.md).

---

## Quick Start

```bash
git clone https://github.com/truecultivar/tajbench
cd tajbench
pip install -e ".[dev]"
cp .env.example .env   # add your API keys

# Validate all benchmark items
python -m benchmark.schema

# Smoke test: run 5 items against Claude
python -m harness.runner --model claude-sonnet-4-6 --limit 5 --dry-run

# Full tier 1 eval
python -m harness.runner --model claude-sonnet-4-6 --tier 1
```

---

## Scoring Methodology

**Tier 1** uses normalised exact match or regex match -- deterministic, zero human judgment required.

**Tier 2-4** use LLM-as-judge with Claude Sonnet 4.6 as the judge model. Each item has:
- A rubric defining what constitutes 0/1/2/3 (published in the item JSON)
- A tier-specific judge prompt (in [`harness/judge_prompts/`](harness/judge_prompts/))

Inter-rater agreement (human vs. judge) is reported in the paper. Judge prompts are fully published so the scoring is reproducible and auditable.

---

## Repository Structure

```
tajbench/
├── benchmark/
│   ├── schema.py              # BenchmarkItem dataclass + corpus validator
│   └── items/
│       ├── tier1_parsing/     # 55 VCF parsing tasks
│       ├── tier2_statistics/  # 55 diversity/differentiation tasks
│       ├── tier3_structure/   # 55 population structure tasks
│       └── tier4_methods/     # 35 methodological decision tasks
├── harness/
│   ├── runner.py              # CLI eval orchestrator
│   ├── scorer.py              # Exact match + LLM-as-judge
│   ├── models/                # API adapters (Claude, GPT-4o, Gemini, HuggingFace)
│   └── judge_prompts/         # Per-tier judge prompt templates
├── baselines/results/         # JSON results per model
├── data/
│   ├── derived/               # Public-safe derived artifacts
│   └── DATA_ACCESS.md
└── paper/                     # arXiv manuscript (LaTeX)
```

---

## Submit a Result

To add your model to the leaderboard:

1. Run the harness: `python -m harness.runner --model <your-model> --output results.json`
2. Open a PR adding your results JSON to `baselines/results/`
3. Update the leaderboard table in `README.md`

Results are accepted if the harness version matches the current `pyproject.toml` version tag.

---

## Citation

```bibtex
@misc{tajbench2026,
  title  = {TajBench: Evaluating Frontier LLMs on Plant Population Genomics Reasoning},
  author = {[Authors]},
  year   = {2026},
  url    = {https://github.com/truecultivar/tajbench},
  note   = {arXiv preprint arXiv:2026.XXXXX}
}
```

---

## License

MIT -- benchmark harness and item schema.
Dataset derived artifacts: see [DATA_ACCESS.md](data/DATA_ACCESS.md).

---

*Built by [True Cultivar](https://truecultivar.com) -- Grounded in the 3,000 Rice Genomes Project and peer-reviewed rice population genomics methodology*
