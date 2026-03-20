# TajBench Item Writing Guide

This guide is for contributors writing benchmark items for Tiers 2, 3, and 4. Engineering handles Tier 1. Read this before writing your first item.

---

## The One Rule

**Every item must have a defensible correct answer.** If two domain experts looking at the same data would disagree about what the right answer is, the item is too ambiguous. Either narrow the question or pick different data.

---

## Item Format

Each item is a JSON file in `benchmark/items/tier{N}_{topic}/`.

```json
{
  "id": "tier2_fst_002",
  "tier": 2,
  "task_type": "interpretation",
  "data_layer": "wgs",
  "difficulty": 2,
  "prompt": "...",
  "context": "...",
  "correct_answer": "...",
  "rubric": "...",
  "source_method": "Weir-Cockerham FST via PLINK2",
  "population_groups": ["indica", "japonica"],
  "scoring_method": "llm_judge",
  "answer_pattern": "",
  "notes": "..."
}
```

### Field-by-field

| Field | What to put |
|-------|-------------|
| `id` | `tier{N}_{topic}_{NNN}` -- e.g. `tier2_fst_002`. Number sequentially within a topic. |
| `tier` | 1=parsing, 2=stats, 3=structure, 4=methods |
| `task_type` | `interpretation` (what does this mean?), `comparison` (which is higher/lower?), `decision` (which method should I use?), `parsing` (extract a field value) |
| `data_layer` | `wgs`, `rad_gbs`, `imputed`, `derived`, or `methodology` |
| `difficulty` | 1=textbook definition, 2=contextual reasoning with data, 3=expert judgment call |
| `prompt` | The question shown to the model. Be specific about what you want. |
| `context` | The data excerpt the model sees. Tables, VCF records, statistics. |
| `correct_answer` | **The most important field.** Write what a correct answer must contain. Not a list of bullet points -- a complete answer a knowledgeable person would give. |
| `rubric` | Scoring criteria for the judge. Describe 3 (full), 2 (mostly), 1 (partial), 0 (wrong). State what the major error looks like. |
| `source_method` | What tool/method produced the data in `context` |
| `population_groups` | Which populations appear in this item. Use: `indica`, `tropical-japonica`, `temperate-japonica`, `aus`, `aromatic`, `admixed` |
| `scoring_method` | Always `llm_judge` for Tier 2-4 |
| `notes` | Optional. Background, caveats, where the numbers come from |

---

## Writing Good Prompts

**Do:**
- Include specific numbers to anchor the question: "Given FST=0.35 between indica and japonica..."
- Ask for interpretation + reasoning, not just a label
- Name the population groups in the question

**Don't:**
- Ask for literature citations (models hallucinate these)
- Ask what the "best" or "correct" approach is in the abstract -- ground it in the data shown
- Put trick questions in the context that aren't relevant to the question

**Example (good):**
> "The Tajima's D distribution for indica rice shows a mean of -0.62 with 28% of 100 kb windows below -1.5. What does this pattern suggest about the demographic and selective history of this subpopulation?"

**Example (too vague):**
> "What does Tajima's D tell you about rice populations?"

---

## Writing the `correct_answer`

Write the answer as if you are writing a one-paragraph methods note for a paper. Include:

1. The correct interpretation of the statistic/structure shown
2. The biological meaning in the rice domestication context
3. Any caveat or alternative explanation that a careful scientist would note

**Length**: 3-6 sentences is typical. This is not a one-liner.

The `correct_answer` is never shown to the model. It is only used by the LLM judge to evaluate the model's response.

---

## Writing the `rubric`

The rubric is what the LLM judge uses to score 0-3. Write it as explicit criteria, not a restatement of the answer.

**Template:**
```
Full marks (3): [specific things that must be present]
Mostly correct (2): [what the main insight is, what minor omission is acceptable]
Partial (1): [some relevant content but what significant error earns this]
Incorrect (0): [what would make you fail this item entirely]
Major error: [describe the most common wrong answer to watch for]
```

**Example:**
```
Full marks: Correctly identifies negative D as consistent with expansion/selective sweeps,
            links it to domestication bottleneck and artificial selection in indica.
Mostly correct: Gets the sign interpretation right but doesn't link to breeding history.
Partial: Mentions Tajima's D but inverts the interpretation (calls negative D balancing selection).
Incorrect: Doesn't engage with the data or gives an unrelated answer.
Major error: Stating that negative Tajima's D = balancing selection (the inverted sign error).
```

---

## Difficulty Guidelines

| Level | Description | Example |
|-------|-------------|---------|
| 1 | Textbook knowledge, no context-specific reasoning needed | "What does a positive Tajima's D indicate?" |
| 2 | Correct answer requires reasoning about the specific data shown | "Given this FST matrix, which rice subpopulations are most differentiated and why?" |
| 3 | Expert judgment -- reasonable scientists could weigh tradeoffs differently, but one answer is more defensible | "Should I apply MAF > 0.05 uniformly or stratify by subpopulation for this downstream analysis?" |

Aim for mostly difficulty 2. We want items that require looking at the data, not just recalling definitions.

---

## Rice Population Groups

The 3K Rice Genomes dataset contains five major subpopulations:

| Group | Abbreviation | Typical N | Key features |
|-------|-------------|-----------|--------------|
| indica | IND | ~1,300 | Largest group, tropical/subtropical lowland, two independent domestication origin |
| tropical japonica | TRJ | ~500 | Upland tropical varieties, distinct from temperate japonica |
| temperate japonica | TEJ | ~400 | East Asian varieties (Japan, Korea, N. China) |
| aus | AUS | ~250 | South Asian (Bangladesh, India), drought-tolerant |
| aromatic | ARO | ~100 | Basmati/jasmine types, smallest group |
| admixed | ADM | ~400 | Intermediate ancestry, not cleanly assigned |

Use these as `population_groups` values.

---

## What to Derive from the 3K RGP Data

Use these as source material for the `context` field:

| Source | What to extract | Tier |
|--------|----------------|------|
| PCA eigenvectors | PC coordinates, variance explained | 3 |
| Pairwise FST matrix | Between-subpopulation FST values | 2 |
| ADMIXTURE Q-matrix | Ancestry proportions per sample | 3 |
| SFS / Tajima's D | Per-subpopulation neutrality statistics | 2 |
| VCF records | SNP records from the 3K SNP call set | 1 |
| LD decay curves | r-squared vs. distance per subpopulation | 2 |

For VCF context: use short excerpts (6-10 records), anonymise sample IDs (S001, S002...), keep only the most relevant FORMAT fields.

---

## File Naming

```
benchmark/items/tier2_statistics/tier2_fst_002.json
benchmark/items/tier2_statistics/tier2_pi_001.json
benchmark/items/tier3_structure/tier3_pca_003.json
benchmark/items/tier4_methods/tier4_method_004.json
```

Use the topic abbreviations: `vcf`, `fst`, `pi`, `tajima`, `dr2`, `ld`, `het`, `gp`, `sfs`, `ibs`, `miss`, `af`, `roh`, `fcoeff`, `tstv`, `kinship`, `qa`, `pca`, `admix`, `tree`, `treemix`, `ibd`, `demo`, `assign`, `clone`, `family`, `introg`, `method`.

---

## Validation

Before submitting:
```bash
python -m benchmark.schema
```

This validates every item in the corpus. Fix any errors it reports before opening a PR.

---

## v1.0 Corpus Summary (202 items)

### Tier 1 -- Parsing (55 items)
| Topic | Count |
|-------|-------|
| VCF parsing (GT, DP, GQ, AD, PL, DS, GP, INFO, FILTER, multi-allelic, MNP, half-calls) | 55 |

### Tier 2 -- Statistics (57 items)
| Topic | Count |
|-------|-------|
| Kinship (KING-robust) | 9 |
| FST interpretation | 6 |
| Nucleotide diversity (pi, piN/piS) | 4 |
| Tajima's D | 4 |
| DR2 / imputation quality | 4 |
| LD decay | 4 |
| Heterozygosity | 4 |
| Genotype probability / concordance | 4 |
| Site frequency spectrum (1D, 2D-SFS) | 3 |
| IBS | 3 |
| Missingness | 3 |
| Allele frequency distributions | 2 |
| Runs of homozygosity (ROH) | 2 |
| Inbreeding coefficients | 2 |
| Ts/Tv ratios | 2 |
| Quality awareness | 1 |

### Tier 3 -- Structure (55 items)
| Topic | Count |
|-------|-------|
| PCA (scree, loadings, projection, outliers, filtering) | 17 |
| ADMIXTURE (Q-matrix, CV error, stability, hierarchy, chromosome-specific) | 15 |
| Family / pedigree reconstruction | 4 |
| Phylogenetic trees (NJ, RAxML) | 3 |
| IBD segment analysis | 3 |
| Population assignment | 3 |
| Demographic modeling (PSMC, fastsimcoal2) | 3 |
| Duplicate / clone detection | 2 |
| TreeMix admixture graphs | 2 |
| Introgression (D-statistic, local ancestry) | 2 |
| Kinship network | 1 |

### Tier 4 -- Methods (35 items)
| Topic | Count |
|-------|-------|
| Pipeline design, GWAS, variant calling, imputation, GRM, QC, genomic prediction, phasing, selection scans, FST methods, ROH params, LD analysis, demographic inference, batch effects, SNP filtering, heritability, genotyping platform selection, ADMIXTURE preprocessing, introgression study design, duplicate retention | 35 |

**v1.0 complete.** All 202 items pass `python -m benchmark.schema`.
