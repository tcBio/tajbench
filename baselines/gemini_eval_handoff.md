# TajBench Gemini Evaluation Handoff

Manual evaluation protocol for running Gemini 2.5 Pro and Gemini 2.5 Flash on all 50 TajBench v0.1 items via the browser (AI Studio or Gemini web interface).

---

## 1. Context

TajBench is a population genomics benchmark evaluating frontier LLMs on plant population genetics reasoning. It is built on a real cannabis WGS + RAD-seq imputation dataset (1,080 samples, 40.9M variants) and grounded in peer-reviewed methodology.

### Current leaderboard (v0.1, 50 items)

| Model | Overall |
|-------|---------|
| Claude Opus 4.6 | **97.3%** |
| Claude Sonnet 4.6 | 94.0% |
| o3 | 88.7% |
| Gemini 2.5 Pro | **TBD** |
| Gemini 2.5 Flash | **TBD** |

We need to evaluate **Gemini 2.5 Pro** and **Gemini 2.5 Flash** on all 50 items. Because the Gemini API adapter is not yet wired into the harness, we collect responses manually through the browser and then score them using the existing harness scorer.

---

## 2. System Prompt

Before running any items, set the following system prompt in Gemini (via AI Studio's "System instructions" field, or paste it as an initial instruction if using the Gemini web UI):

```
You are an expert population geneticist and bioinformatician. Answer the following question about genomic data precisely and concisely. Do not add caveats or hedging beyond what the data supports.
```

**Important**: Use this exact system prompt for every item. Do not modify it. This is the same system prompt used for Claude and o3 evaluations to ensure fair comparison.

---

## 3. Scoring Methodology

Each item is scored on a 0–3 scale. The scoring method depends on the tier:

### Tier 1 — Parsing & Structural Understanding (10 items)

- **Scoring**: `regex_match` or `exact_match` — deterministic, binary (0 or 3)
- The model's response is matched against a regex pattern or exact string
- Match = 3 points, no match = 0 points
- No partial credit, no human/LLM judgment needed

### Tier 2 — Diversity & Differentiation Statistics (16 items)
### Tier 3 — Population Structure (16 items)
### Tier 4 — Methodological Decision-Making (8 items)

- **Scoring**: `llm_judge` — Claude Sonnet 4.6 scores each response on a 0–3 scale
- Each item has a rubric defining what constitutes 0/1/2/3
- Tier-specific judge prompts are in `harness/judge_prompts/`
- The judge model reads the item rubric + the model's response and assigns a score

**Overall score** is the mean fraction of maximum score across all 50 items (i.e., mean of score/3 for each item, expressed as a percentage).

---

## 4. All 50 Prompts

Below are all 50 items. For each one, copy the **User Prompt** block (everything inside the fenced code block) and paste it into the Gemini chat. Make sure the system prompt from Section 2 is active.

**Workflow per item:**
1. Start a new conversation (or clear context) in Gemini
2. Ensure the system prompt is set
3. Paste the user prompt below
4. Copy Gemini's full response
5. Record it in the response template (Section 5)

---

### Tier 1 — Parsing & Structural Understanding

#### Item 1/50: `tier1_vcf_001`

- **Tier**: 1
- **Scoring**: `regex_match`
- **Expected answer**: `REF=G; ALT=A,T; DP=31`

**User Prompt** (copy everything between the fences):

````text
The following VCF record was produced by GLnexus joint-genotyping of a cannabis WGS cohort. What is the reference allele, the alternative allele(s), and the total read depth for sample TC_042? Answer in the format: REF=_; ALT=_; DP=_

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	TC_042	TC_043	TC_044
NC_044370.1	1023847	.	G	A,T	.	PASS	AF=0.083,0.021;AN=96;AC=8,2	GT:GQ:DP:AD:PL	0/1:43:31:19,12,0:380,0,540,400,560,620	0/0:52:28:28,0,0:0,84,980,84,980,1020	1/2:18:14:0,8,6:520,460,600,0,180,240
````

---

#### Item 2/50: `tier1_vcf_002`

- **Tier**: 1
- **Scoring**: `regex_match`
- **Expected answer**: `(a) DR2=0.723; (b) No, 0.723 < 0.80 threshold, site should be filtered out; (c) GT=0/1, GP=0.03,0.96,0.01`

**User Prompt** (copy everything between the fences):

````text
The following record is from a Beagle 5.4 imputed VCF produced from sparse RAD-seq targets imputed against a cannabis WGS reference panel. Identify (a) the imputation quality score (DR2) for this site, (b) whether this site should be retained if the analysis requires DR2 > 0.8, and (c) the genotype call (GT) and full genotype-posterior triplet (GP) for sample GBS_011.

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	GBS_011	GBS_012
NC_044372.1	4481923	.	C	T	.	PASS	AF=0.312;AN=2160;AC=674;DR2=0.723;IMP	GT:DS:GP	0/1:0.98:0.03,0.96,0.01	1/1:2.00:0.00,0.01,0.99
````

---

#### Item 3/50: `tier1_vcf_003`

- **Tier**: 1
- **Scoring**: `regex_match`
- **Expected answer**: `(a) AC=3; (b) AN=8; (c) AF=0.375; (d) S2 has the missing genotype (./.).`

**User Prompt** (copy everything between the fences):

````text
The following BCF record has a sample with a missing genotype (./.). Using the INFO fields, report (a) AC, (b) AN, (c) AF of the ALT allele, and (d) which sample has the missing genotype.

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S1	S2	S3	S4	S5
NC_044371.1	789012	.	A	G	.	PASS	AC=3;AN=8;AF=0.375	GT:GQ:DP	0/1:38:22	./.:0:0	0/0:55:30	1/1:60:41	0/1:42:18
````

---

#### Item 4/50: `tier1_vcf_004`

- **Tier**: 1
- **Scoring**: `exact_match`
- **Expected answer**: `4`

**User Prompt** (copy everything between the fences):

````text
How many distinct alleles (including the reference) are present at this multi-allelic site?

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003	S004
NC_044371.1	542891	.	A	T,G,C	312	PASS	AF=0.31,0.12,0.07;AN=8;AC=3,1,1	GT:GQ:DP:AD	0/1:35:28:14,12,2,0	0/0:42:31:31,0,0,0	1/2:18:19:0,11,8,0	0/3:22:24:15,0,0,9
````

---

#### Item 5/50: `tier1_vcf_005`

- **Tier**: 1
- **Scoring**: `regex_match`
- **Expected answer**: `S002, DP=42`

**User Prompt** (copy everything between the fences):

````text
Which sample has the highest read depth (DP), and what is its DP value?

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003	S004	S005
NC_044370.1	2847193	.	G	A	445	PASS	AF=0.40;AN=10;AC=4	GT:GQ:DP:AD:PL	0/1:30:18:10,8:255,0,210	0/0:42:42:42,0:0,126,1260	0/1:12:7:3,4:85,0,62	1/1:35:35:0,35:980,105,0	0/1:29:29:15,14:350,0,310
````

---

#### Item 6/50: `tier1_vcf_006`

- **Tier**: 1
- **Scoring**: `regex_match`
- **Expected answer**: `(a) PL=180,0,95; (b) 0/1 is most likely (PL=0); (c) Yes, GT=0/1 matches.`

**User Prompt** (copy everything between the fences):

````text
For sample S003, the PL (phred-scaled genotype likelihood) field shows three values corresponding to genotypes 0/0, 0/1, and 1/1. Report (a) the three PL values, (b) which genotype is most likely (PL=0 marks the most likely), and (c) whether the most likely genotype matches the GT field.

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003
NC_044372.1	1538742	.	C	T	289	PASS	AF=0.33;AN=6;AC=2	GT:GQ:DP:AD:PL	0/0:40:25:25,0:0,75,840	1/1:38:22:0,22:690,66,0	0/1:28:19:8,11:180,0,95

Note: PL values are phred-scaled likelihoods for genotypes 0/0, 0/1, 1/1. Lower PL = more likely genotype. PL=0 marks the most likely genotype.
````

---

#### Item 7/50: `tier1_vcf_007`

- **Tier**: 1
- **Scoring**: `regex_match`
- **Expected answer**: `S002 and S005`

**User Prompt** (copy everything between the fences):

````text
Which samples have missing genotypes (./.) at this site?

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003	S004	S005	S006
NC_044373.1	891204	.	T	C	156	PASS	AF=0.25;AN=8;AC=2	GT:DP	0/1:22	./.:	0/0:18	0/1:15	./.:	0/0:30
````

---

#### Item 8/50: `tier1_vcf_008`

- **Tier**: 1
- **Scoring**: `exact_match`
- **Expected answer**: `2`

**User Prompt** (copy everything between the fences):

````text
How many of the three VCF records below pass quality filtering?

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002
NC_044370.1	5012841	.	A	G	342	PASS	AF=0.50;AN=4;AC=2	GT:DP	0/1:25	0/1:30
NC_044370.1	5012903	.	C	T	28	LowQual	AF=0.25;AN=4;AC=1	GT:DP	0/0:8	0/1:5
NC_044370.1	5012967	.	G	A	512	PASS	AF=0.75;AN=4;AC=3	GT:DP	0/1:35	1/1:40
````

---

#### Item 9/50: `tier1_vcf_009`

- **Tier**: 1
- **Scoring**: `regex_match`
- **Expected answer**: `(a) GT=0/1; (b) DS=0.82; (c) GP=0.28,0.62,0.10; (d) highest GP is 0.62, corresponding to genotype 0/1.`

**User Prompt** (copy everything between the fences):

````text
For sample S001 at the site below, report (a) the GT value, (b) the DS value, (c) the full GP triplet, and (d) which GP value is highest and which genotype it corresponds to.

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003
NC_044375.1	3201847	.	A	T	.	.	AF=0.35;AN=170;AC=60;DR2=0.61;IMP	GT:DS:GP	0/1:0.82:0.28,0.62,0.10	0/0:0.05:0.95,0.05,0.00	1/1:1.94:0.01,0.05,0.94

Note: DS = expected alternate allele dosage (0-2). GP = posterior probabilities for genotypes 0/0, 0/1, 1/1 (sum to 1.0).
````

---

#### Item 10/50: `tier1_vcf_010`

- **Tier**: 1
- **Scoring**: `regex_match`
- **Expected answer**: `Phased: S001 (0|1) and S003 (1|0). Unphased: S002 (0/0) and S004 (0/1). Pipe (|) separator indicates phased, forward slash (/) indicates unphased.`

**User Prompt** (copy everything between the fences):

````text
Which samples have phased genotypes and which have unphased genotypes? State the separator character that distinguishes them.

--- DATA ---
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003	S004
NC_044370.1	7821456	.	C	T	.	.	AF=0.38;AN=8;AC=3	GT:DS:GP	0|1:1.00:0.00,1.00,0.00	0/0:0.02:0.98,0.02,0.00	1|0:0.98:0.01,0.98,0.01	0/1:0.85:0.22,0.63,0.15
````

---

### Tier 2 — Diversity & Differentiation Statistics

#### Item 11/50: `tier2_dr2_001`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
After Beagle 5.4 imputation of cannabis RAD-seq samples against a WGS reference panel, the DR2 (dosage r-squared) distribution is shown below stratified by minor allele frequency (MAF) bin. A researcher proposes applying a uniform DR2 > 0.8 filter across all MAF bins before computing population structure statistics. Evaluate this proposal and recommend an alternative approach if appropriate.

--- DATA ---
DR2 distribution by MAF bin (post-imputation, 40.9M sites, 933 sparse samples):

MAF bin     Median DR2  % sites > 0.8  N sites
< 0.01      0.31        12%            18.2M
0.01-0.05   0.61        38%            9.4M
0.05-0.20   0.84        71%            8.7M
0.20-0.50   0.93        89%            4.6M

Note: The WGS reference panel has 407 samples; sparse targets are predominantly
RAD-seq MseI with ~200K sites overlapping the reference panel per sample.
````

---

#### Item 12/50: `tier2_fcoeff_001`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The following table shows heterozygosity rates and inbreeding coefficients (F) for 8 anonymized cannabis cultivar samples from a RAD-seq dataset imputed against a WGS reference panel. What does the F-coefficient distribution tell you about the breeding population structure of these drug-type cannabis cultivars?

--- DATA ---
Per-sample QA metrics (85 drug-type cannabis cultivars, RAD-seq imputed against 492-sample WGS panel, 15.3M variants):

Sample             Het_Rate(%)   F_Coefficient
TC_072             6.34          0.707
TC_033             6.24          0.712
TC_011             7.23          0.666
TC_001             7.52          0.653
TC_057             10.15         0.531
TC_004             10.91         0.496
TC_013             11.72         0.459
TC_014             12.19         0.437

F-coefficients computed via PLINK2 --het. Positive F indicates excess homozygosity relative to Hardy-Weinberg expectation; negative F indicates excess heterozygosity.
````

---

#### Item 13/50: `tier2_fst_001`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The following pairwise Weir-Cockerham FST estimates were computed between four cannabis populations using the WGS reference panel (n>30 per group). Interpret the population differentiation pattern. Which two populations are most genetically similar, and what does the FST between drug-type cannabis and hemp suggest about their evolutionary history?

--- DATA ---
Pairwise FST matrix (Weir-Cockerham estimator, 197,412 LD-pruned SNPs):

                    Drug-type  Hemp-fiber  Feral-CA  Feral-EU
Drug-type           0.000
Hemp-fiber          0.183      0.000
Feral-CA            0.094      0.221       0.000
Feral-EU            0.211      0.157       0.248     0.000

All FST estimates p < 0.001 (permutation test, 1000 permutations).
````

---

#### Item 14/50: `tier2_gp_001`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The table below shows mean genotype posterior confidence (GP%) by 1 Mb window on cannabis chromosome NC_044370.1 for 85 imputed samples. The first 5 Mb and the last 2 Mb of the chromosome show notably lower GP confidence than the interior regions. What biological or technical factors explain this pattern?

--- DATA ---
Region              Mean_GP(%)  N_Variants  Min_GP(%)
0-1 Mb              92.02       20,892      14.1
1-2 Mb              88.60       18,798       9.4
2-3 Mb              90.80       31,145      20.0
3-4 Mb              90.38       25,421      15.3
4-5 Mb              91.25       21,423      10.6
...
8-9 Mb              94.33       30,248       9.4
9-10 Mb             94.86       29,266       5.9
10-11 Mb            94.28       30,371       8.2
...
19-20 Mb            95.09        2,247      11.8
20-21 Mb            95.44       11,461       1.2

Note: 85 RAD-seq samples imputed via GLIMPSE2 against 492-sample WGS reference panel. Chromosome NC_044370.1 is 104.99 Mb with centromere estimated near 3-5 Mb.
````

---

#### Item 15/50: `tier2_gp_002`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Two 1 Mb regions on chromosome NC_044370.1 have different imputation profiles. Region A (6-7 Mb) has mean GP = 94.4% with 33,286 variants. Region B (19-20 Mb) has mean GP = 95.1% with only 2,247 variants. A researcher concludes that Region B has 'better imputation quality' because of higher GP. Is this conclusion valid? Explain.

--- DATA ---
Region     Mean_GP(%)  N_Variants  Min_GP(%)
6-7 Mb     94.41       33,286      2.4
19-20 Mb   95.09        2,247      11.8

Panel: 85 RAD-seq samples imputed via GLIMPSE2 against 492-sample WGS panel.
Total chromosome variants: ~15.3M imputed sites.
````

---

#### Item 16/50: `tier2_het_001`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Sample TC_014 has the highest heterozygosity rate in the panel (12.19%) alongside the lowest genotype posterior confidence (GP=90.31%). The population average heterozygosity is ~10.1%. Is this elevated heterozygosity a quality concern or a genuine biological signal? What additional evidence would help you distinguish between the two explanations?

--- DATA ---
Per-sample QA metrics for selected samples (RAD-seq imputed against WGS panel):

Sample    Het_Rate(%)   GP_Confidence(%)   F_Coefficient
TC_014    12.19         90.31              0.437
TC_035    10.99         94.01              0.492
TC_057    10.15         93.75              0.531
TC_072    6.34          94.43              0.707

Population summary (85 drug-type cultivars): mean Het = 10.1%, SD = 1.6%, mean GP = 92.7%.
Imputation method: Beagle 5.4 against 492-sample WGS reference panel, 15.3M variants.
````

---

#### Item 17/50: `tier2_ibs_001`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Two genomic windows on chromosome NC_044374.1 show elevated mean identity-by-state (IBS) compared to the chromosome-wide average. Interpret what these hotspots indicate about the genomic region and the population.

--- DATA ---
Chromosome-wide mean IBS: 0.832 (85 drug-type cannabis samples, 1000-variant sliding windows)

IBS Hotspots on NC_044374.1:
Window    Start       End        Mean_IBS   N_Variants
1         27,678      56,527     0.925      1,000
14        460,195     489,241    0.915      1,000

For comparison, typical windows on this chromosome:
Window    Start       End        Mean_IBS   N_Variants
50        2,104,339   2,178,521  0.831      1,000
100       5,421,876   5,512,003  0.829      1,000
````

---

#### Item 18/50: `tier2_ibs_002`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The table below shows mean and range of window-level IBS scores across 5 cannabis chromosomes. Chromosome NC_044371.1 has both the lowest minimum IBS (0.755) and the widest range. What does this cross-chromosome variation suggest?

--- DATA ---
Chromosome-level IBS summary (85 drug-type samples, 1000-variant windows):

Chromosome       Mean_IBS  Min_IBS  Max_IBS  Range    N_Windows
NC_044370.1      0.841     0.780    0.907    0.127    20
NC_044371.1      0.822     0.755    0.900    0.145    18
NC_044372.1      0.849     0.802    0.893    0.091    16
NC_044373.1      0.838     0.789    0.884    0.095    15
NC_044374.1      0.843     0.791    0.925    0.134    14

Note: Cannabis sativa has 10 chromosomes (CS10 assembly). Window size = 1,000 variants.
````

---

#### Item 19/50: `tier2_kinship_001`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The following table shows pairwise KING-robust kinship coefficients and IBS0 statistics for six sample pairs from a cannabis genetics study. Using the standard KING thresholds (Duplicate/MZ twin: >0.354, First-degree: 0.177–0.354, Second-degree: 0.0884–0.177, Third-degree: 0.0442–0.0884, Unrelated: <0.0442), classify each pair's relationship degree. Comment on any notable differences in IBS0 between pairs in the same relationship category.

--- DATA ---
KING-robust kinship estimates for six cannabis sample pairs:

Pair | Sample_A | Sample_B | KINSHIP | IBS0   | Panel
-----|----------|----------|---------|--------|------------------
1    | TC_042   | TC_023   | 0.290   | 0.00577| TrueCut_Imputed
2    | WGS_247  | WGS_221  | 0.246   | 0.02032| WGS_Reference
3    | TC_011   | TC_009   | 0.102   | 0.02147| TrueCut_Imputed
4    | TC_004   | WGS_221  | -0.012  | 0.089  | Cross-panel
5    | TC_016   | WGS_300  | 0.031   | 0.078  | Cross-panel
6    | TC_055   | TC_042   | 0.114   | 0.02417| TrueCut_Imputed

TrueCut_Imputed panel: imputed genotypes from targeted amplicon sequencing. WGS_Reference panel: whole-genome sequencing genotypes. Cross-panel pairs compare one sample from each panel.
````

---

#### Item 20/50: `tier2_kinship_002`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The following table shows KING-robust kinship coefficients for four cannabis sample pairs, all classified as first-degree relatives. Additional genotype discordance analysis is provided for a subset of samples. Are all four pairs the same type of relationship? How would you distinguish clones from first-degree relatives in this dataset, and what metric is most informative for making that distinction?

--- DATA ---
KING-robust kinship estimates:

Pair | Sample_A | Sample_B | KINSHIP | IBS0    | Panel
-----|----------|----------|---------|---------|------------------
1    | TC_042   | TC_023   | 0.290   | 0.00577 | TrueCut_Imputed
2    | TC_042   | TC_009   | 0.290   | 0.00570 | TrueCut_Imputed
3    | TC_023   | TC_009   | 0.287   | 0.00586 | TrueCut_Imputed
4    | TC_062   | TC_016   | 0.281   | 0.00563 | TrueCut_Imputed

Clone discordance analysis for the group {TC_042, TC_023, TC_009}:
- Genotype discordance rate: 3.9% across 100,000 imputed variants
- Mean pairwise kinship within group: 0.361
- All three samples flagged as a clone group by KING --duplicate

Standard KING thresholds: Duplicate/MZ twin >0.354, First-degree 0.177–0.354, Third-degree 0.0442–0.0884, Unrelated <0.0442.

Note: Cannabis is vegetatively propagated through cuttings, so clone groups (genetically identical cultivars) are expected in cultivar collections.
````

---

#### Item 21/50: `tier2_kinship_003`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The following table shows KING-robust kinship coefficients for four sample pairs from a cannabis genetics study. Two of the pairs have negative kinship values. What do negative KING kinship coefficients mean? Should negative values be treated as a data quality concern?

--- DATA ---
KING-robust kinship estimates for four cannabis sample pairs:

Pair | Sample_A | Sample_B | KINSHIP | IBS0  | Panel
-----|----------|----------|---------|-------|------------------
1    | TC_004   | WGS_221  | -0.012  | 0.089 | Cross-panel
2    | TC_057   | WGS_300  | 0.008   | 0.081 | Cross-panel
3    | TC_016   | WGS_300  | 0.031   | 0.078 | Cross-panel
4    | TC_042   | TC_023   | 0.290   | 0.006 | TrueCut_Imputed

Panel descriptions:
- TrueCut_Imputed: drug-type cannabis cultivars genotyped by targeted amplicon sequencing and imputed to a genome-wide variant set.
- WGS_Reference: hemp and feral cannabis reference samples genotyped by whole-genome sequencing.
- Cross-panel: one sample from each panel.
````

---

#### Item 22/50: `tier2_kinship_004`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The following symmetric kinship matrix shows KING-robust kinship coefficients for five cannabis samples from the TrueCut_Imputed panel. Identify which samples form a close genetic cluster and describe the overall relatedness structure among all five samples. Use the standard KING thresholds for relationship classification (Duplicate/MZ twin: >0.354, First-degree: 0.177–0.354, Second-degree: 0.0884–0.177, Third-degree: 0.0442–0.0884, Unrelated: <0.0442).

--- DATA ---
KING-robust pairwise kinship matrix (TrueCut_Imputed panel, imputed genotypes):

            TC_042  TC_023  TC_009  TC_055  TC_004
TC_042      0.500   0.290   0.290   0.114   0.043
TC_023      0.290   0.500   0.287   0.116   0.039
TC_009      0.290   0.287   0.500   0.115   0.041
TC_055      0.114   0.116   0.115   0.500   0.045
TC_004      0.043   0.039   0.041   0.045   0.500

Diagonal values of 0.5 represent self-kinship (expected for non-inbred diploids).
````

---

#### Item 23/50: `tier2_kinship_005`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The pair TC_012 / TC_010 has a KING kinship coefficient of 0.173, which falls just below the standard first-degree threshold of 0.177. A researcher classifies this as second-degree. Is this classification reliable? What factors could cause a true first-degree pair to fall below the threshold?

--- DATA ---
KING-robust pairwise kinship results (selected pairs):

Pair               KINSHIP   IBS0      Panel              Classification
TC_012 / TC_010    0.173     0.01563   TrueCut_Imputed    Second_Degree (?)
TC_075 / TC_079    0.195     0.01388   TrueCut_Imputed    First_Degree
WGS_247 / WGS_221  0.246     0.02032   WGS_Reference      First_Degree
TC_067 / TC_073    0.048     0.01814   TrueCut_Imputed    Third_Degree

Standard KING thresholds:
  First-degree:  0.177 – 0.354
  Second-degree: 0.0884 – 0.177
  Third-degree:  0.0442 – 0.0884

Note: 85 drug-type cannabis cultivars, RAD-seq imputed via GLIMPSE2.
````

---

#### Item 24/50: `tier2_kinship_006`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Two first-degree pairs are identified in the panel. Pair A (WGS_247/WGS_221, both from WGS reference panel) has KINSHIP=0.246. Pair B (TC_075/TC_079, both RAD-seq imputed) has KINSHIP=0.195. Both are classified as first-degree. Why is there a systematic difference in kinship magnitude between WGS and imputed samples?

--- DATA ---
Pair A (WGS):      KINSHIP=0.246, IBS0=0.02032, N_SNPs=1,387,334
Pair B (Imputed):  KINSHIP=0.195, IBS0=0.01389, N_SNPs=1,387,334

Panel summary:
  WGS reference:     492 samples, hard-call genotypes (DeepVariant+GLnexus)
  TrueCut imputed:    85 samples, imputed genotypes (GLIMPSE2, mean DR2=0.72)
````

---

#### Item 25/50: `tier2_qa_001`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Using the quality tier criteria below, assign each of the 4 samples to the appropriate tier (A, B, or C). Justify each assignment by showing which criteria were met or failed.

--- DATA ---
Quality tier criteria for imputed cannabis genotype samples:

  Tier A: GP >= 93.4% AND |Het_zscore| < 2.0 AND |F_zscore| < 2.0
  Tier B: GP >= 91.0% AND no outlier flags (but does not meet all Tier A thresholds)
  Tier C: GP < 91.0% OR any outlier flag present

Sample metrics:

Sample    GP(%)    Het_zscore   F_zscore   Outlier_flags
TC_001    93.71    -1.44        1.44       None
TC_004    91.72    0.66         -0.66      None
TC_013    89.80    1.16         -1.16      None
TC_014    90.31    1.46         -1.46      None

Population: 85 drug-type cannabis cultivars, RAD-seq imputed against 492-sample WGS panel.
````

---

#### Item 26/50: `tier2_tajima_001`

- **Tier**: 2
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The following Tajima's D values were computed in 50 kb windows across chromosome NC_044370.1 for two cannabis population groups. Interpret the difference between the two distributions and what it implies about the demographic and selective history of each group.

--- DATA ---
Tajima's D summary statistics (50 kb windows, NC_044370.1, WGS data):

Group             N samples  Mean D   Median D  % windows D < -1.5  % windows D > 1.5
Drug-type (TC)    82         -0.81    -0.93     34%                  4%
Hemp-fiber (IPK)  130        +0.22    +0.18     8%                   19%

Minimum window SNPs: 50. Windows with <50 SNPs excluded.
````

---

### Tier 3 — Population Structure

#### Item 27/50: `tier3_admix_001`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
ADMIXTURE was run on 323 cannabis WGS samples at K=2, K=3, and K=4. Below are Q-values for 5 representative samples across the three K values. Which K is most informative for classifying cultivars by cannabinoid type (THC-dominant vs CBD-dominant vs balanced), and why?

--- DATA ---
ADMIXTURE Q-values at K=2:

Sample    Comp_1(drug)  Comp_2(hemp)
TC_036    0.95          0.05
TC_062    0.92          0.08
TC_004    0.68          0.32
IPK_041   0.06          0.94
TC_079    0.62          0.38

ADMIXTURE Q-values at K=3:

Sample    Comp_1(drug)  Comp_2(hemp)  Comp_3(landrace)
TC_036    0.91          0.04          0.05
TC_062    0.87          0.05          0.08
TC_004    0.51          0.12          0.37
IPK_041   0.04          0.86          0.10
TC_079    0.44          0.14          0.42

ADMIXTURE Q-values at K=4:

Sample    Comp_1(THC-drug)  Comp_2(hemp)  Comp_3(landrace)  Comp_4(CBD-drug)
TC_036    0.89              0.03          0.04              0.04
TC_062    0.84              0.04          0.06              0.06
TC_004    0.18              0.09          0.28              0.45
IPK_041   0.03              0.84          0.09              0.04
TC_079    0.12              0.10          0.31              0.47

Cross-validation error: K=2: 0.412, K=3: 0.398, K=4: 0.391, K=5: 0.394

Sample notes:
  TC_036, TC_062: THC-dominant cultivars
  TC_004: CBD-dominant cultivar (Alpha Explorer)
  TC_079: CBD-dominant cultivar (The Wife)
  IPK_041: Hemp-fiber accession
````

---

#### Item 28/50: `tier3_admix_002`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
ADMIXTURE at K=3 was run on a cannabis panel including both THC-dominant and CBD-dominant cultivars. The three components correspond to drug-type, hemp-fiber, and landrace ancestry. Compare the ancestry proportions of the 4 CBD cultivars to the 4 THC cultivars below. What does this difference imply about how CBD production was achieved in modern cultivar breeding?

--- DATA ---
ADMIXTURE K=3 ancestry proportions:

CBD cultivars:
Sample    Comp_A(drug)  Comp_B(hemp)  Comp_C(landrace)  Cannabinoid_type
TC_004    0.42          0.12          0.46              CBD-dominant
TC_006    0.38          0.15          0.47              CBD-dominant
TC_075    0.48          0.10          0.42              CBD-dominant
TC_079    0.44          0.14          0.42              CBD-dominant
Mean      0.43          0.13          0.44

THC cultivars:
Sample    Comp_A(drug)  Comp_B(hemp)  Comp_C(landrace)  Cannabinoid_type
TC_036    0.91          0.04          0.05              THC-dominant
TC_055    0.82          0.03          0.15              THC-dominant
TC_062    0.87          0.05          0.08              THC-dominant
TC_072    0.84          0.06          0.10              THC-dominant
Mean      0.86          0.05          0.10

Population reference:
  Landrace accessions (N=95): mean Comp_C = 0.84
  Hemp accessions (N=264): mean Comp_B = 0.89
  Drug-type WGS references (N=182): mean Comp_A = 0.91
````

---

#### Item 29/50: `tier3_admix_003`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Two pairs of cannabis cultivars are presented with both ADMIXTURE ancestry proportions (K=3) and KING-robust kinship coefficients. Pair A has very similar ancestry proportions but moderate kinship. Pair B has dissimilar ancestry proportions but lower kinship. Which pair is more closely related, and why do ancestry proportions fail to predict kinship?

--- DATA ---
Pair A:
Sample    Comp_A(drug)  Comp_B(hemp)  Comp_C(landrace)  F
TC_057    0.71          0.09          0.20              0.580
TC_060    0.68          0.11          0.21              0.490
KINSHIP(TC_057, TC_060) = 0.164  [Second_Degree]

Pair B:
Sample    Comp_A(drug)  Comp_B(hemp)  Comp_C(landrace)  F
TC_036    0.85          0.10          0.05              0.505
TC_055    0.60          0.25          0.15              0.498
KINSHIP(TC_036, TC_055) = 0.094  [Second_Degree]

KING-robust kinship thresholds:
  > 0.354  = Duplicate/MZ twin
  0.177–0.354 = First-degree (parent-offspring / full-sib)
  0.0884–0.177 = Second-degree (half-sib / avuncular)
  0.0442–0.0884 = Third-degree

Note: Both pairs are classified as second-degree, but Pair A's kinship (0.164) is near the first-degree boundary while Pair B's (0.094) is near the third-degree boundary.
````

---

#### Item 30/50: `tier3_admix_004`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
At K=4, sample TC_005 shows near-equal ancestry proportions across all four components (0.28, 0.25, 0.22, 0.25). Most other samples have a dominant component (>0.60). Is TC_005 a genuinely admixed cultivar, or could this pattern be an artifact? What evidence would distinguish these explanations?

--- DATA ---
ADMIXTURE K=4 ancestry proportions (selected samples):

Sample   Comp_A    Comp_B    Comp_C    Comp_D    Dominant
TC_036   0.82      0.08      0.06      0.04      Drug-type
TC_075   0.12      0.05      0.71      0.12      Landrace
TC_005   0.28      0.25      0.22      0.25      None (high entropy)
TC_054   0.74      0.11      0.08      0.07      Drug-type
TC_040   0.69      0.15      0.09      0.07      Drug-type

Population means:
  Drug-type (n=65): Comp_A=0.71, Comp_B=0.12, Comp_C=0.09, Comp_D=0.08
  CBD (n=12):       Comp_A=0.18, Comp_B=0.08, Comp_C=0.52, Comp_D=0.22
  Hemp-fiber (n=8): Comp_A=0.05, Comp_B=0.78, Comp_C=0.11, Comp_D=0.06
````

---

#### Item 31/50: `tier3_admix_005`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The table below shows ADMIXTURE cross-validation (CV) error for K=2 through K=8. Based on these results, what is the optimal K, and what does the CV error curve shape tell you about population structure?

--- DATA ---
ADMIXTURE cross-validation error:

K    CV Error
2    0.4521
3    0.4187
4    0.3942
5    0.3918
6    0.3905
7    0.3911
8    0.3923

Panel: 706 cannabis samples (492 WGS + 85 RAD-seq imputed + 129 WGS imputed)
Variants: 2.1M LD-pruned biallelic SNPs
````

---

#### Item 32/50: `tier3_admixture_001`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The following ADMIXTURE Q-matrix was computed at K=3 on 323 cannabis WGS samples (drug-type, hemp-fiber, and feral populations). Interpret the ancestry composition of sample TC_017 and explain what the admixture pattern implies about its breeding history.

--- DATA ---
ADMIXTURE K=3 results (cross-validation error minimised at K=3)

Ancestry components:
  Component A: predominant in drug-type cultivars (modal = 0.91)
  Component B: predominant in hemp-fiber cultivars (modal = 0.89)
  Component C: predominant in feral/landrace accessions (modal = 0.84)

Selected sample Q-values:
Sample   Comp_A  Comp_B  Comp_C  Source
TC_017   0.61    0.31    0.08    True Cultivar RAD-seq imputed
TC_021   0.94    0.04    0.02    True Cultivar RAD-seq imputed
IPK_088  0.07    0.88    0.05    PRJNA866500 WGS
FRL_014  0.11    0.15    0.74    Feral accession WGS
````

---

#### Item 33/50: `tier3_clone_001`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Clone detection was performed on 85 imputed cannabis cultivar samples using KING-robust kinship at multiple thresholds. The table below shows the number of clone groups and samples identified at each threshold. Explain how threshold choice affects clone detection in imputed data, and recommend the most appropriate threshold for this dataset.

--- DATA ---
Clone detection results at varying kinship thresholds (85 TrueCut RAD-seq imputed samples):

Threshold   Clone_groups   Samples_in_groups
0.45        0              0
0.40        0              0
0.35        1              3
0.30        2              5
0.25        2              5

Clone group details at threshold 0.35:
  Group 1: TC_042, TC_023, TC_009 — pairwise discordance 3.917% across 100K variants, mean kinship 0.361

Clone group details at threshold 0.30 (additional group):
  Group 1: TC_042, TC_023, TC_009 (same as above)
  Group 2: TC_011, TC_044 — pairwise discordance 7.2% across 100K variants, mean kinship 0.308

Reference kinship thresholds (for WGS data, not imputed):
  Identical twins / clones: KINSHIP > 0.354
  First-degree (parent-offspring): 0.177–0.354

Note: Data were imputed from RAD-seq (~2% genome coverage) to WGS density using Beagle5.4 with a cannabis reference panel.
````

---

#### Item 34/50: `tier3_family_001`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Strain family clustering was performed on 85 drug-type cannabis cultivars using KING-robust kinship estimates. Five families were identified, with highly asymmetric sizes. Interpret what the family structure implies about breeding program diversity, and discuss practical consequences for downstream genetic analyses.

--- DATA ---
Strain family summary (85 TrueCut cultivars, KING-robust kinship clustering):

Family   N_members   Mean_F    Mean_within_kinship   Notes
0        5           0.505     0.147                  Mixed drug-type cultivars
1        3           0.645     0.198                  All CBD cultivars
2        2           0.580     0.108                  Paired cultivars
3        4           0.498     0.082                  Diverse drug-type
4        73          0.537     0.055                  Most TrueCut cultivars

Total: 85 cultivars in 5 families.
Family 4 contains 73 of 85 cultivars (85.9%).

KING-robust kinship thresholds for reference:
  Second-degree: 0.0884–0.177
  Third-degree: 0.0442–0.0884

Population-level statistics:
  Overall mean F (inbreeding coefficient): 0.538
  Overall mean pairwise kinship: 0.061
````

---

#### Item 35/50: `tier3_family_002`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Founder analysis was performed on 85 drug-type cannabis cultivars using a kinship-network-based scoring method. The top 5 cultivars by founder score are listed below. Interpret which cultivars are likely breeding hub genotypes versus derived lines, and what the score distribution implies about the structure of the cannabis breeding program.

--- DATA ---
Top 5 founder scores (KING-robust kinship network, 85 TrueCut cultivars):

Rank   Sample    Founder_score   Mean_kinship_to_panel   N_first_or_second_degree_connections
1      TC_036    0.218           0.078                   12
2      TC_055    0.213           0.075                   11
3      TC_062    0.170           0.068                   8
4      TC_057    0.145           0.063                   7
5      TC_004    0.139           0.061                   6

For reference — panel statistics:
  Mean founder score across all 85 cultivars: 0.052
  Median founder score: 0.041
  Bottom 10 cultivars: founder scores 0.008–0.019

Family membership:
  TC_036: Family 4 (73 members)
  TC_055: Family 4
  TC_062: Family 4
  TC_057: Family 0 (5 members)
  TC_004: Family 1 (3 members, CBD cultivars)

Note: Founder score is computed as the mean kinship contribution to the panel weighted by the number of connections at second-degree or closer.
````

---

#### Item 36/50: `tier3_pca_001`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
The following PCA was computed on 1,080 cannabis samples (407 WGS + 673 imputed RAD-seq) using PCAngsd with 197,412 LD-pruned SNPs (DR2 > 0.8, MAF > 0.05). PC1 explains 53.1% and PC2 explains 19.0% of variance. Interpret the population structure and identify any potential concerns about the imputed samples.

--- DATA ---
Sample coordinates (PC1, PC2) — representative centroids by study:

Study              N    PC1_mean  PC2_mean  Data type
PRJNA866500_hemp  130   -0.312    +0.018    WGS
PRJNA734114_drug   82   +0.289    -0.021    WGS
PRJNA738519_CAN    31   +0.261    -0.008    WGS
TC_cultivars       85   +0.271    -0.015    RAD-seq imputed
PRJNA1206134_hemp 673   -0.287    +0.183    RAD-seq imputed

Variance explained: PC1=53.1%, PC2=19.0%, PC3=6.5%, PC4=4.6%

Within-study spread (mean Euclidean distance from study centroid):
PRJNA866500_hemp: 0.089 | TC_cultivars: 0.031 | PRJNA1206134_hemp: 0.147
````

---

#### Item 37/50: `tier3_pca_002`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
A researcher computed PCA twice on the same 85 True Cultivar RAD-seq imputed samples: once using all imputed sites (DR2 > 0.3), and once using high-confidence sites only (DR2 > 0.8). The variance explained by PC1 increased from 41% to 53% when the stricter filter was applied, but the number of sites dropped from 12.4M to 3.1M. Two phenotypic replicates (same cultivar sequenced twice) are included. Interpret what the change in PC1 variance explained tells you, and explain whether you would prefer the DR2 > 0.3 or DR2 > 0.8 result for cultivar identity verification.

--- DATA ---
DR2 > 0.3 run (12.4M sites):
  PC1=41.2%, PC2=14.8%, PC3=7.1%
  Phenotypic replicate pair Euclidean distance: 0.062
  Mean between-cultivar distance: 0.071
  Signal-to-noise ratio (between/within): 1.15

DR2 > 0.8 run (3.1M sites):
  PC1=53.1%, PC2=19.0%, PC3=6.5%
  Phenotypic replicate pair Euclidean distance: 0.018
  Mean between-cultivar distance: 0.044
  Signal-to-noise ratio (between/within): 2.44
````

---

#### Item 38/50: `tier3_pca_003`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
PCA was computed using PCAngsd on two overlapping sample sets from the same imputed cannabis cohort. The full panel includes 706 samples spanning drug-type cultivars, hemp-fiber accessions, Chinese landraces, European hemp, and feral populations. The TrueCut-only subset includes 85 drug-type cultivars. Compare the variance explained by the top PCs in each analysis and explain why PC1 captures much more variance in the smaller subset.

--- DATA ---
PCA variance explained — Full panel (706 samples, 197K LD-pruned SNPs):
  PC1 = 25.5%
  PC2 = 14.8%
  PC3 =  9.2%
  PC4 =  6.1%
  PC5 =  4.3%
  Cumulative (PC1-5) = 59.9%

PCA variance explained — TrueCut only (85 drug-type cultivars, same SNP set):
  PC1 = 53.1%
  PC2 = 19.0%
  PC3 =  6.5%
  PC4 =  4.6%
  Cumulative (PC1-4) = 83.2%

Populations in full panel: drug-type cultivars (N=182), hemp-fiber (N=264), Chinese landraces (N=95), European hemp (N=112), feral (N=53).
````

---

#### Item 39/50: `tier3_pca_004`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Six cannabis samples from three genotyping panels were projected into a shared PCA space computed on 197K LD-pruned SNPs. Two samples are from whole-genome sequencing (WGS), two are from TrueCut RAD-seq imputed to WGS density, and two are from Kannapedia RAD-seq imputed to WGS density. From the PCA coordinates below, identify which samples are likely imputed (not WGS) and explain the artifact you observe.

--- DATA ---
PCA coordinates for 6 drug-type cannabis samples:

Sample    PC1      PC2      PC3      Panel
S_A      +0.287   -0.041   +0.019   ???
S_B      +0.264   +0.012   -0.007   ???
S_C      +0.271   -0.018   +0.003   ???
S_D      +0.273   -0.009   +0.001   ???
S_E      +0.269   -0.015   -0.002   ???
S_F      +0.291   +0.024   -0.015   ???

Drug-type centroid: PC1=+0.275, PC2=-0.008, PC3=+0.000
PC coordinate standard deviation across all drug-type WGS samples: PC1=0.024, PC2=0.031, PC3=0.018

Note: All six samples are confirmed drug-type cultivars from independent breeding programs.
````

---

#### Item 40/50: `tier3_pca_005`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Two cannabis cultivars, TC_033 and TC_032, are described as phenotypic variants of the same cultivar — TC_033 has white pistils and TC_032 has green pistils, but they share the same cultivar name and breeder. Both are highly inbred (inbreeding coefficient F > 0.71). Their KING-robust kinship coefficient is 0.108, classifying them as second-degree relatives. Given the high inbreeding and distinct phenotypes, what does the second-degree kinship tell us about the genetic architecture of the phenotypic difference between these two samples?

--- DATA ---
Pairwise relatedness (KING-robust estimator):

Sample_1   Sample_2   KINSHIP   Relationship    F_sample1   F_sample2
TC_033     TC_032     0.108     Second_Degree   0.714       0.723

KING-robust kinship thresholds:
  > 0.354  = Duplicate/MZ twin
  0.177–0.354 = First-degree (parent-offspring / full-sib)
  0.0884–0.177 = Second-degree (half-sib / avuncular)
  0.0442–0.0884 = Third-degree

Phenotype notes:
  TC_033: White pistil phenotype, otherwise typical drug-type morphology
  TC_032: Green pistil phenotype, otherwise typical drug-type morphology
  Both marketed as variants of the same cultivar line by the same breeder.

For reference — a confirmed clone pair in this panel:
  TC_042 / TC_023: KINSHIP = 0.361, classified as Duplicate
````

---

#### Item 41/50: `tier3_pca_006`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
In a PCA of 706 cannabis samples, one drug-type cultivar (TC_048) clusters far from other drug-type samples and instead falls near the hemp/landrace cluster. The sample passed all QC filters (call rate > 0.95, no excess heterozygosity). Evaluate whether this positioning is most likely due to (a) sample mislabeling, (b) DNA contamination, or (c) genuine admixture, and describe what additional evidence would distinguish among these explanations.

--- DATA ---
PCA coordinates for selected samples:

Sample     PC1      PC2      Type_label
TC_048    -0.198   +0.072   drug-type (breeder-reported)
TC_021    +0.289   -0.021   drug-type
TC_036    +0.274   -0.033   drug-type
IPK_041   -0.305   +0.024   hemp-fiber
IPK_088   -0.312   +0.018   hemp-fiber
LR_022    -0.241   +0.098   Chinese landrace
LR_009    -0.228   +0.105   Chinese landrace

Drug-type centroid: PC1=+0.275, PC2=-0.008
Hemp centroid: PC1=-0.295, PC2=+0.031
Landrace centroid: PC1=-0.234, PC2=+0.101

QC metrics for TC_048:
  Call rate: 0.973
  Mean depth: 8.2x
  Het rate: 0.312
  Inbreeding coefficient F: 0.285
  ADMIXTURE K=3 Q-values: Comp_A(drug)=0.38, Comp_B(hemp)=0.41, Comp_C(landrace)=0.21

For comparison — typical drug-type QC:
  Het rate range: 0.28–0.35
  F range: 0.20–0.75
  ADMIXTURE K=3: Comp_A > 0.85 typically
````

---

#### Item 42/50: `tier3_pca_007`

- **Tier**: 3
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
Two PCA analyses were run on different subsets of the same cannabis panel. Analysis A (85 drug-type cultivars only) has PC1 explaining 53.1% of variance. Analysis B (all 706 samples including hemp, landraces, and feral) has PC1 explaining 25.5%. A researcher concludes that Analysis A provides 'better resolution' because PC1 captures more variance. Evaluate this conclusion.

--- DATA ---
Analysis A (drug-type only):
  Samples: 85 drug-type cultivars (RAD-seq imputed)
  PC1: 53.1%  PC2: 19.0%  PC3: 6.5%  PC4: 4.6%
  Top 2 PCs: 72.1% cumulative

Analysis B (full panel):
  Samples: 706 (492 WGS + 85 imputed drug-type + 129 imputed mixed)
  PC1: 25.5%  PC2: 14.8%  PC3: 9.2%  PC4: 6.1%
  Top 2 PCs: 40.3% cumulative

Both analyses: 2.1M LD-pruned SNPs, PCAngsd.
````

---

### Tier 4 — Methodological Decision-Making

#### Item 43/50: `tier4_method_001`

- **Tier**: 4
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
A population genetics study has 85 drug-type cannabis samples sequenced with RAD-seq at 8–15× average coverage and wants to compute a PCA for population structure analysis. A collaborator suggests using PLINK2's --pca command on hard-called genotypes. Evaluate this approach and state whether PCAngsd would be preferable, with justification.

--- DATA ---
Dataset properties:
- 85 samples, RAD-seq MseI protocol
- Average depth: 8-15x (range 3-42x)
- Missing genotype rate: 28% per sample (variable coverage across RAD loci)
- SNP count after joint calling: 187,432 biallelic SNPs
- Many sites have DP < 5 in 20-40% of samples

Available tools:
- PLINK2 --pca: requires hard-called genotypes (GT field)
- PCAngsd: uses genotype likelihood matrices (GL/GP fields) and handles uncertainty
````

---

#### Item 44/50: `tier4_method_002`

- **Tier**: 4
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
A lab has 200 new cannabis RAD-seq samples and wants to impute them using a WGS reference panel of 407 samples. They ask whether Beagle 5.4 or GLIMPSE2 is more appropriate for this use case, given the reference panel size and the RAD-seq data characteristics.

--- DATA ---
Reference panel: 407 phased WGS samples (SHAPEIT5-phased)
Target samples: 200 RAD-seq samples, MseI protocol
  - ~200K sites overlapping reference panel per sample
  - Average depth at overlapping sites: 12x
  - Some samples have 50-100K overlapping sites (low-quality RAD)

Tools under consideration:
  Beagle 5.4: array-style imputation; requires hard-called genotypes at reference sites;
              scales well with large reference panels
  GLIMPSE2:   low-coverage WGS imputation using genotype likelihoods;
              designed for <1x WGS but works with any GL input;
              particularly accurate when depth is variable
````

---

#### Item 45/50: `tier4_method_003`

- **Tier**: 4
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
A collaborator shares a joint-called cannabis VCF and wants to compute nucleotide diversity (π) across the genome for two population groups. They plan to use all PASS-filter sites including those in repeat regions. Evaluate this plan and recommend any modifications.

--- DATA ---
Dataset: 212 samples, joint-called GLnexus VCF, cannabis genome (CS10 assembly)
  - Total PASS sites: 2.31M
  - Sites in annotated repeats (RepeatMasker): ~38% of PASS sites
  - Sites in low-complexity regions: ~12% of PASS sites
  - Sites in coding/genic regions: ~22% of PASS sites

Planned analysis:
  vcftools --window-pi 50000 --keep pop1.txt
  vcftools --window-pi 50000 --keep pop2.txt
  (No additional site filters beyond PASS)
````

---

#### Item 46/50: `tier4_method_004`

- **Tier**: 4
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
A researcher building a RAD-aware reference panel for GLIMPSE2 imputation used the following command to create the RAD coverage footprint from BAM files:

  samtools depth -r NC_044370.1 sample.bam | awk '$3 > 0 {print $1"\t"$2-1"\t"$2}'

This produced 54 million single-base positions (1.6 GB BED file), and extracting WGS variants at these positions yielded 28 million variants. GLIMPSE2 failed with '#non-ref gls: 0'. Identify the error and propose the correct approach.

--- DATA ---
Pipeline output from incorrect approach:
  BED positions:    54,000,000 (1.6 GB)
  Extracted variants: 28,341,000
  SNP density:     ~270 SNPs/kb
  GLIMPSE2 error:  "#non-ref gls: 0"

For comparison, a correct pipeline on the same data should produce:
  Merged intervals: ~63,000
  Coverage:         ~45% of chromosome
  Extracted SNPs:   ~2.4M
  SNP density:      ~50 SNPs/kb

Note: 5 RAD-seq BAMs (MseI digest, 8-15x depth), chromosome NC_044370.1 (104.99 Mb).
````

---

#### Item 47/50: `tier4_method_005`

- **Tier**: 4
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
A researcher plans to run both ADMIXTURE and PCA on a merged cannabis panel (706 samples, 14.9M biallelic SNPs). They propose using the same LD-pruned variant set for both analyses, with PLINK2 parameters: window=50, step=5, r²=0.2. This produces 2.1M independent variants. Is this parameter choice appropriate for both analyses, and should the same pruned set be used?

--- DATA ---
Panel: 706 samples (492 WGS reference + 85 RAD-seq imputed + 129 WGS imputed)
Starting variants: 14.9M biallelic SNPs (post-QC)
LD pruning result: 2.1M variants retained (14.1% of input)

PLINK2 parameters: --indep-pairwise 50 5 0.2
  window = 50 variants
  step   = 5 variants
  r²     = 0.2 (variants with r² > 0.2 pruned)
````

---

#### Item 48/50: `tier4_method_006`

- **Tier**: 4
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
In a merged panel of 706 cannabis samples from three sources (WGS, RAD-seq imputed, WGS imputed), PCA reveals that PC3 separates samples primarily by data type rather than biological population. A researcher proposes mean-centering and variance-scaling each data-type panel independently before merging, then re-running PCA. Evaluate this correction strategy.

--- DATA ---
Pre-correction PCA:
  PC1 (25.5%): Separates drug-type from hemp/landrace (biological)
  PC2 (14.8%): Separates Chinese landraces from European hemp (biological)
  PC3 (9.2%):  Separates WGS from imputed samples (technical)
  PC4 (6.1%):  Separates RAD-seq imputed from WGS imputed (technical)

Panel composition:
  WGS reference:    492 samples (hemp, landrace, drug-type, feral)
  RAD-seq imputed:   85 samples (drug-type cultivars)
  WGS imputed:      129 samples (mixed drug-type)

Proposed correction: For each panel, subtract panel mean and divide by panel SD
on each variant independently, then concatenate and re-run PCA.
````

---

#### Item 49/50: `tier4_method_007`

- **Tier**: 4
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
A researcher is merging three cannabis genotyping panels (492 WGS + 85 RAD-seq imputed + 129 WGS imputed = 706 samples) into a single dataset for population structure analysis. The merged VCF has 59M variants but substantial structural missingness: variants called in the WGS panel may be absent from imputed panels and vice versa. The researcher applies --geno 0.10 (remove variants missing in >10% of samples), which removes 25.9M variants. Is this threshold appropriate?

--- DATA ---
Pre-filter: 59,000,000 variants across 706 samples
Post --geno 0.10: 33,100,000 variants retained (56.1% retained)

Missingness structure:
  Variants in WGS panel only:           ~18M (absent from imputed panels)
  Variants in imputed panels only:      ~6M
  Variants shared across all 3 panels:  ~21M
  Variants shared between 2 panels:     ~14M

Panel sizes: WGS=492 (69.7%), RAD-seq=85 (12.0%), WGS_imputed=129 (18.3%)
````

---

#### Item 50/50: `tier4_method_008`

- **Tier**: 4
- **Scoring**: `llm_judge`

**User Prompt** (copy everything between the fences):

````text
A researcher wants to run KING relatedness estimation on 85 imputed cannabis cultivars. They have two variant sets: (A) 17.5M LD-pruned variants from the pre-QC merged panel, and (B) 2.1M LD-pruned variants from the post-QC panel (after --geno 0.10, --maf 0.01, --hwe 1e-6 filters). Which variant set should be used for KING, and why?

--- DATA ---
Variant set A (pre-QC): 17.5M variants
  - LD-pruned (r² < 0.2)
  - Includes sites with up to 30% missingness
  - Includes rare variants (MAF < 0.01)
  - Includes HWE-violating sites

Variant set B (post-QC): 2.1M variants
  - LD-pruned (r² < 0.2)
  - Missingness < 10% per site
  - MAF ≥ 0.01
  - No HWE violations (p > 1e-6)

Panel: 85 RAD-seq imputed drug-type cannabis cultivars.
````

---

## 5. Response Collection Template

Copy the JSON template below into a file called `responses_gemini_2_5_pro.json` (or `responses_gemini_2_5_flash.json`). For each item, replace `"PASTE GEMINI RESPONSE HERE"` with the full response text from Gemini.

```json
[
  {
    "item_id": "tier1_vcf_001",
    "tier": 1,
    "scoring_method": "regex_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier1_vcf_002",
    "tier": 1,
    "scoring_method": "regex_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier1_vcf_003",
    "tier": 1,
    "scoring_method": "regex_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier1_vcf_004",
    "tier": 1,
    "scoring_method": "exact_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier1_vcf_005",
    "tier": 1,
    "scoring_method": "regex_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier1_vcf_006",
    "tier": 1,
    "scoring_method": "regex_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier1_vcf_007",
    "tier": 1,
    "scoring_method": "regex_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier1_vcf_008",
    "tier": 1,
    "scoring_method": "exact_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier1_vcf_009",
    "tier": 1,
    "scoring_method": "regex_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier1_vcf_010",
    "tier": 1,
    "scoring_method": "regex_match",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_dr2_001",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_fcoeff_001",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_fst_001",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_gp_001",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_gp_002",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_het_001",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_ibs_001",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_ibs_002",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_kinship_001",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_kinship_002",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_kinship_003",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_kinship_004",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_kinship_005",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_kinship_006",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_qa_001",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier2_tajima_001",
    "tier": 2,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_admix_001",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_admix_002",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_admix_003",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_admix_004",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_admix_005",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_admixture_001",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_clone_001",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_family_001",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_family_002",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_pca_001",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_pca_002",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_pca_003",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_pca_004",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_pca_005",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_pca_006",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier3_pca_007",
    "tier": 3,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier4_method_001",
    "tier": 4,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier4_method_002",
    "tier": 4,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier4_method_003",
    "tier": 4,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier4_method_004",
    "tier": 4,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier4_method_005",
    "tier": 4,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier4_method_006",
    "tier": 4,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier4_method_007",
    "tier": 4,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  },
  {
    "item_id": "tier4_method_008",
    "tier": 4,
    "scoring_method": "llm_judge",
    "model": "gemini-2.5-pro",
    "response_text": "PASTE GEMINI RESPONSE HERE"
  }
]
```

**Tips for response collection:**

- Preserve the model's exact output, including any formatting, newlines, or code blocks
- In the JSON, escape double quotes inside responses as `\"` and newlines as `\n`
- If the model refuses to answer or gives an error, record the full refusal/error text
- Run each model in a separate file (one for Pro, one for Flash)

---

## 6. Scoring Instructions

Once all 50 responses have been collected for a model, score them using the TajBench harness.

### Option A: Automated scoring via the harness

```bash
# Score Gemini 2.5 Pro responses
python -m harness.runner --model gemini-2.5-pro --input responses_gemini_2_5_pro.json

# Score Gemini 2.5 Flash responses
python -m harness.runner --model gemini-2.5-flash --input responses_gemini_2_5_flash.json
```

This will:
1. Load the responses from the JSON file
2. For Tier 1 items: apply `regex_match` or `exact_match` scoring (deterministic)
3. For Tier 2–4 items: send each response to the Claude Sonnet 4.6 LLM judge for 0–3 scoring
4. Output a results JSON file with per-item scores and the overall percentage

### Option B: Manual scoring

If the harness `--input` flag is not yet implemented, you can score manually:

**Tier 1 items** (deterministic):

For each Tier 1 item, check the response against the `answer_pattern` (regex) or `correct_answer` (exact). A match scores 3, a miss scores 0. The patterns for each Tier 1 item are:

| Item ID | Scoring | Pattern / Expected Answer |
|---------|---------|--------------------------|
| `tier1_vcf_001` | regex_match | `REF=G.*ALT=A,\s*T.*DP=31` |
| `tier1_vcf_002` | regex_match | `(?=.*DR2\s*[=:]\s*0\.723)(?=.*(?:\bno\b|\bnot\s+retained\b|\bshould\s+be\s+filtered\s+out\b|\bshould\s+be\s+excluded\b|\bfails?\s+(?:the\s+)?(?:DR2\s*)?(?:threshold|filter)\b|\bexclude(?:d)?\b|\bremove(?:d)?\b|\bfiltered?\s+out\b))(?=.*0/1)(?=.*0\.03\s*,\s*0\.96\s*,\s*0\.01)` |
| `tier1_vcf_003` | regex_match | `(?=.*AC[^=:\d]*[=:]\s*3\b)(?=.*AN[^=:\d]*[=:]\s*8\b)(?=.*0\.375)(?=.*S2)` |
| `tier1_vcf_004` | exact_match | `4` |
| `tier1_vcf_005` | regex_match | `S002.*42|42.*S002` |
| `tier1_vcf_006` | regex_match | `(?=.*\b180\b)(?=.*\b95\b)(?=.*0/1.*(?:PL|most likely))(?=.*(?:\byes\b|\bmatch|\bconsistent\b|\bcorrect\b|\bconfirm))` |
| `tier1_vcf_007` | regex_match | `S002.*S005|S005.*S002` |
| `tier1_vcf_008` | exact_match | `2` |
| `tier1_vcf_009` | regex_match | `(?=.*GT.*0/1)(?=.*DS.*0\.82)(?=.*0\.28\s*,\s*0\.62\s*,\s*0\.10)(?=.*0\.62.*0/1)` |
| `tier1_vcf_010` | regex_match | `(?=.*S001.*(?:phased|\|))(?=.*S003.*(?:phased|\|))(?=.*S002.*(?:unphased|/))(?=.*S004.*(?:unphased|/))` |

**Tier 2–4 items** (LLM judge):

Run each response through the Claude Sonnet 4.6 judge using the rubric from the item JSON and the judge prompt templates in `harness/judge_prompts/`. The judge assigns a 0–3 score per item.

### Computing the overall score

```python
overall_pct = mean(score_i / 3 for each item i) * 100
```

For example, if all 50 items score 3/3, the overall is 100%. If the sum of all scores is 135 out of 150 maximum, the overall is 90.0%.

### Saving results

Save the scored results to `baselines/results/gemini_2_5_pro.json` (or `gemini_2_5_flash.json`) and update the leaderboard table in `README.md`.

---

*Generated for TajBench v0.1 — 50 items across 4 tiers.*