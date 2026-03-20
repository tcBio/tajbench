# Gemini Remaining Prompts — Items 36–50

Paste each block into a fresh Google AI Mode chat with system prompt active:

> You are an expert population geneticist and bioinformatician. Answer the following question about genomic data precisely and concisely. Do not add caveats or hedging beyond what the data supports.

---

## Item 36 — `tier3_pca_001`

```
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
```

---

## Item 37 — `tier3_pca_002`

```
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
```

---

## Item 38 — `tier3_pca_003`

```
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
```

---

## Item 39 — `tier3_pca_004`

```
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
```

---

## Item 40 — `tier3_pca_005`

```
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
```

---

## Item 41 — `tier3_pca_006`

```
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
```

---

## Item 42 — `tier3_pca_007`

```
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
```

---

## Item 43 — `tier4_method_001`

```
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
```

---

## Item 44 — `tier4_method_002`

```
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
```

---

## Item 45 — `tier4_method_003`

```
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
```

---

## Item 46 — `tier4_method_004`

```
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
```

---

## Item 47 — `tier4_method_005`

```
A researcher plans to run both ADMIXTURE and PCA on a merged cannabis panel (706 samples, 14.9M biallelic SNPs). They propose using the same LD-pruned variant set for both analyses, with PLINK2 parameters: window=50, step=5, r²=0.2. This produces 2.1M independent variants. Is this parameter choice appropriate for both analyses, and should the same pruned set be used?

--- DATA ---
Panel: 706 samples (492 WGS reference + 85 RAD-seq imputed + 129 WGS imputed)
Starting variants: 14.9M biallelic SNPs (post-QC)
LD pruning result: 2.1M variants retained (14.1% of input)

PLINK2 parameters: --indep-pairwise 50 5 0.2
  window = 50 variants
  step   = 5 variants
  r²     = 0.2 (variants with r² > 0.2 pruned)
```

---

## Item 48 — `tier4_method_006`

```
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
```

---

## Item 49 — `tier4_method_007`

```
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
```

---

## Item 50 — `tier4_method_008`

```
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
```
