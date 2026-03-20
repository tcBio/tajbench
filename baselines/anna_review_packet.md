# TajBench -- Domain Expert Review Packet

**Reviewer:** Anna (population genetics)
**Generated:** 2026-03-19
**Total items:** 50

## Summary

| Tier | Label | Count |
|------|-------|-------|
| 1 | Tier 1 -- Parsing | 10 |
| 2 | Tier 2 -- Statistics | 16 |
| 3 | Tier 3 -- Structure | 16 |
| 4 | Tier 4 -- Methods | 8 |

## Tier 1 -- Parsing (10 items)

---
### tier1_vcf_001
**Tier**: 1 | **Difficulty**: 1 | **Type**: parsing | **Scoring**: exact_match | **Data**: wgs

**PROMPT:**
> The following VCF record was produced by GLnexus joint-genotyping of a cannabis WGS cohort. What is the reference allele, the alternative allele(s), and the total read depth for sample TC_042?

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	TC_042	TC_043	TC_044
NC_044370.1	1023847	.	G	A,T	.	PASS	AF=0.083,0.021;AN=96;AC=8,2	GT:GQ:DP:AD:PL	0/1:43:31:19,12,0:380,0,540,400,560,620	0/0:52:28:28,0,0:0,84,980,84,980,1020	1/2:18:14:0,8,6:520,460,600,0,180,240
```

**CORRECT ANSWER:**
REF=G; ALT=A,T (two alternative alleles); DP for TC_042=31

**RUBRIC:**
Must identify REF as G, ALT as A and T (both), and extract DP=31 from the FORMAT/DP field for TC_042. Partial credit if two of three are correct.

**NOTES:** Tests multi-allelic VCF parsing and FORMAT field extraction. DP is the 3rd FORMAT sub-field.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier1_vcf_002
**Tier**: 1 | **Difficulty**: 2 | **Type**: parsing | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> The following record is from a Beagle 5.4 imputed VCF produced from sparse RAD-seq targets imputed against a cannabis WGS reference panel. Identify (a) the imputation quality score for this site, (b) whether this site should be retained if the analysis requires DR2 > 0.8, and (c) the genotype call and posterior probability for sample GBS_011.

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	GBS_011	GBS_012
NC_044372.1	4481923	.	C	T	.	PASS	AF=0.312;AN=2160;AC=674;DR2=0.723;IMP	GT:DS:GP	0/1:0.98:0.03,0.96,0.01	1/1:2.00:0.00,0.01,0.99
```

**CORRECT ANSWER:**
(a) DR2=0.723; (b) No, 0.723 < 0.80 threshold, site should be filtered out; (c) GT=0/1 (heterozygous), GP=0.03,0.96,0.01 (posterior probability of het = 0.96)

**RUBRIC:**
Must extract DR2=0.723 correctly. Must state the site fails DR2>0.8 filter. Must correctly read GT as 0/1 and identify the GP values. Major error: stating site passes filter, or reading GT from GBS_012 instead of GBS_011.

**NOTES:** Tests imputation quality field (DR2) extraction and threshold reasoning, plus GP posterior probability parsing.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier1_vcf_003
**Tier**: 1 | **Difficulty**: 2 | **Type**: parsing | **Scoring**: llm_judge | **Data**: wgs

**PROMPT:**
> The following BCF record has a sample with a missing genotype (./.). Compute the allele frequency (AF) of the ALT allele from the genotyped samples only, using the AC and AN fields. Show your calculation.

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S1	S2	S3	S4	S5
NC_044371.1	789012	.	A	G	.	PASS	AC=3;AN=8;AF=0.375	GT:GQ:DP	0/1:38:22	./.:0:0	0/0:55:30	1/1:60:41	0/1:42:18
```

**CORRECT ANSWER:**
AF = AC/AN = 3/8 = 0.375. S2 is missing (./.), so AN=8 counts only the 4 genotyped diploid samples (S1,S3,S4,S5 = 8 alleles). AC=3 from S1 (1 alt) + S4 (2 alts) + S5 (1 alt). AF=0.375.

**RUBRIC:**
Must correctly identify that the missing sample (./.) contributes 0 to AN. Must compute AC=3 from the non-missing genotypes. AF=3/8=0.375 must be stated. Must show the derivation steps.

**NOTES:** Tests understanding of how missing genotypes affect AC/AN computation, a common source of confusion.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier1_vcf_004
**Tier**: 1 | **Difficulty**: 1 | **Type**: parsing | **Scoring**: exact_match | **Data**: wgs

**PROMPT:**
> How many distinct alleles (including the reference) are present at this multi-allelic site?

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003	S004
NC_044371.1	542891	.	A	T,G,C	312	PASS	AF=0.31,0.12,0.07;AN=8;AC=3,1,1	GT:GQ:DP:AD	0/1:35:28:14,12,2,0	0/0:42:31:31,0,0,0	1/2:18:19:0,11,8,0	0/3:22:24:15,0,0,9
```

**CORRECT ANSWER:**
4

**RUBRIC:**
Must answer 4. The site has REF allele A and three ALT alleles (T, G, C) for a total of 4 distinct alleles.

**NOTES:** Tests ability to count alleles at a multi-allelic site. REF=A plus ALT=T,G,C gives 4 distinct alleles. The AD field has 4 values corresponding to each allele.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier1_vcf_005
**Tier**: 1 | **Difficulty**: 2 | **Type**: parsing | **Scoring**: regex_match | **Data**: wgs

**PROMPT:**
> Which sample has the highest read depth (DP), and what is its DP value?

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003	S004	S005
NC_044370.1	2847193	.	G	A	445	PASS	AF=0.40;AN=10;AC=4	GT:GQ:DP:AD:PL	0/1:30:18:10,8:255,0,210	0/0:42:42:42,0:0,126,1260	0/1:12:7:3,4:85,0,62	1/1:35:35:0,35:980,105,0	0/1:29:29:15,14:350,0,310
```

**CORRECT ANSWER:**
S002, DP=42

**RUBRIC:**
Must identify S002 as having the highest DP and report DP=42. DP is the 3rd field in the FORMAT column (GT:GQ:DP:AD:PL).

**NOTES:** Tests FORMAT field positional parsing across multiple samples. DP values: S001=18, S002=42, S003=7, S004=35, S005=29. S002's GQ also happens to be 42, testing whether the model reads the correct sub-field.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier1_vcf_006
**Tier**: 1 | **Difficulty**: 2 | **Type**: parsing | **Scoring**: llm_judge | **Data**: wgs

**PROMPT:**
> For sample S003, the PL (phred-scaled genotype likelihood) field shows three values corresponding to genotypes 0/0, 0/1, and 1/1. Which genotype is most likely according to the PL values, and does it match the GT (hard-call genotype) field? Explain your reasoning.

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003
NC_044372.1	1538742	.	C	T	289	PASS	AF=0.33;AN=6;AC=2	GT:GQ:DP:AD:PL	0/0:40:25:25,0:0,75,840	1/1:38:22:0,22:690,66,0	0/1:28:19:8,11:180,0,95

Note: PL values are phred-scaled likelihoods for genotypes 0/0, 0/1, 1/1. Lower PL = more likely genotype. PL=0 marks the most likely genotype.
```

**CORRECT ANSWER:**
The PL values for S003 are 180, 0, 95, corresponding to genotypes 0/0, 0/1, and 1/1 respectively. Since PL=0 for 0/1, the heterozygous genotype is most likely. This matches the GT field which shows 0/1. The PL=180 for 0/0 means the homozygous reference genotype is 10^(180/10) = 10^18 times less likely than the best genotype. The PL=95 for 1/1 means homozygous alt is 10^9.5 times less likely.

**RUBRIC:**
Full marks (3): Correctly identifies 0/1 as most likely (PL=0), confirms GT match, explains PL scale (lower = more likely, phred-scaled). Mostly correct (2): Gets the right genotype and match but doesn't explain PL scale. Partial (1): Identifies that PL=0 is relevant but misinterprets which genotype it corresponds to. Incorrect (0): Gets the genotype wrong. Major error: Claiming PL=180 is the most likely genotype.

**NOTES:** Tests understanding of PL (phred-scaled likelihood) field ordering and interpretation. PL=0 marks the most likely genotype; values are ordered 0/0, 0/1, 1/1 for biallelic sites.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier1_vcf_007
**Tier**: 1 | **Difficulty**: 1 | **Type**: parsing | **Scoring**: regex_match | **Data**: wgs

**PROMPT:**
> Which samples have missing genotypes (./.) at this site?

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003	S004	S005	S006
NC_044373.1	891204	.	T	C	156	PASS	AF=0.25;AN=8;AC=2	GT:DP	0/1:22	./.:	0/0:18	0/1:15	./.:	0/0:30
```

**CORRECT ANSWER:**
S002 and S005

**RUBRIC:**
Must identify both S002 and S005 as having missing genotypes (./.). Note AN=8 reflects only 4 called samples (8 alleles / 2 per sample).

**NOTES:** Tests recognition of missing genotype encoding (./.) in VCF. AN=8 is consistent with 4 genotyped diploid samples out of 6 total.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier1_vcf_008
**Tier**: 1 | **Difficulty**: 1 | **Type**: parsing | **Scoring**: exact_match | **Data**: wgs

**PROMPT:**
> How many of the three VCF records below pass quality filtering?

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002
NC_044370.1	5012841	.	A	G	342	PASS	AF=0.50;AN=4;AC=2	GT:DP	0/1:25	0/1:30
NC_044370.1	5012903	.	C	T	28	LowQual	AF=0.25;AN=4;AC=1	GT:DP	0/0:8	0/1:5
NC_044370.1	5012967	.	G	A	512	PASS	AF=0.75;AN=4;AC=3	GT:DP	0/1:35	1/1:40
```

**CORRECT ANSWER:**
2

**RUBRIC:**
Must answer 2. Records at positions 5012841 and 5012967 have FILTER=PASS. The record at 5012903 has FILTER=LowQual and does not pass.

**NOTES:** Tests understanding of the FILTER column in VCF. PASS indicates the record passed all filters; any other value (e.g., LowQual) indicates a failed filter.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier1_vcf_009
**Tier**: 1 | **Difficulty**: 2 | **Type**: parsing | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> For sample S001 at the site below, explain the relationship between the GT (hard-call genotype), DS (allele dosage), and GP (genotype posterior probability) fields. Is the hard-call genotype well-supported by the posterior probabilities?

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003
NC_044375.1	3201847	.	A	T	.	.	AF=0.35;AN=170;AC=60;DR2=0.61;IMP	GT:DS:GP	0/1:0.82:0.28,0.62,0.10	0/0:0.05:0.95,0.05,0.00	1/1:1.94:0.01,0.05,0.94

Note: DS = expected alternate allele dosage (0-2). GP = posterior probabilities for genotypes 0/0, 0/1, 1/1 (sum to 1.0).
```

**CORRECT ANSWER:**
For S001: GT=0/1 (heterozygous hard call), DS=0.82 (expected alt dosage), GP=0.28,0.62,0.10 (28% probability of 0/0, 62% probability of 0/1, 10% probability of 1/1). The hard call 0/1 matches the highest GP (0.62), so the call is consistent. However, the support is weak — only 62% posterior probability for the called genotype, with 28% probability of being homozygous reference. DS=0.82 reflects this uncertainty: a confident heterozygote would have DS≈1.0, but the pull toward reference (DS<1.0) indicates the 0/0 probability (0.28) is non-trivial. The site's DR2=0.61 confirms moderate imputation quality. This genotype should be used with caution in analyses sensitive to individual genotype accuracy.

**RUBRIC:**
Full marks (3): Correctly explains GT/DS/GP relationship, notes the weak support (62% GP), interprets DS<1.0 as uncertainty toward reference, connects to DR2 quality. Mostly correct (2): Gets the field meanings right but doesn't flag the weak support. Partial (1): Identifies the fields but misinterprets GP ordering or DS meaning. Incorrect (0): Confuses DS with depth or GP with PL. Major error: Claiming GP=0.62 means 'high confidence'.

**NOTES:** Tests understanding of imputed VCF fields (GT, DS, GP) and their interrelationship. DS=0.82 is the expected dosage computed as 0*0.28 + 1*0.62 + 2*0.10 = 0.82, confirming internal consistency. DR2=0.61 indicates moderate imputation quality.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier1_vcf_010
**Tier**: 1 | **Difficulty**: 1 | **Type**: parsing | **Scoring**: exact_match | **Data**: imputed

**PROMPT:**
> Which samples have phased genotypes and which have unphased genotypes? State the separator character that distinguishes them.

**CONTEXT:**
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	S001	S002	S003	S004
NC_044370.1	7821456	.	C	T	.	.	AF=0.38;AN=8;AC=3	GT:DS:GP	0|1:1.00:0.00,1.00,0.00	0/0:0.02:0.98,0.02,0.00	1|0:0.98:0.01,0.98,0.01	0/1:0.85:0.22,0.63,0.15
```

**CORRECT ANSWER:**
Phased: S001 (0|1) and S003 (1|0). Unphased: S002 (0/0) and S004 (0/1). Pipe (|) separator indicates phased, forward slash (/) indicates unphased.

**RUBRIC:**
Must identify S001 and S003 as phased (| separator) and S002 and S004 as unphased (/ separator). Must state that pipe = phased and slash = unphased.

**NOTES:** Tests recognition of phased vs unphased genotype notation in VCF. Note S003 is 1|0 (not 0|1), meaning the first haplotype carries the ALT allele — phase order matters for haplotype-aware analyses.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

## Tier 2 -- Statistics (16 items)

---
### tier2_dr2_001
**Tier**: 2 | **Difficulty**: 3 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> After Beagle 5.4 imputation of cannabis RAD-seq samples against a WGS reference panel, the DR2 (dosage r-squared) distribution is shown below stratified by minor allele frequency (MAF) bin. A researcher proposes applying a uniform DR2 > 0.8 filter across all MAF bins before computing population structure statistics. Evaluate this proposal and recommend an alternative approach if appropriate.

**CONTEXT:**
```
DR2 distribution by MAF bin (post-imputation, 40.9M sites, 933 sparse samples):

MAF bin     Median DR2  % sites > 0.8  N sites
< 0.01      0.31        12%            18.2M
0.01-0.05   0.61        38%            9.4M
0.05-0.20   0.84        71%            8.7M
0.20-0.50   0.93        89%            4.6M

Note: The WGS reference panel has 407 samples; sparse targets are predominantly
RAD-seq MseI with ~200K sites overlapping the reference panel per sample.
```

**CORRECT ANSWER:**
The uniform DR2 > 0.8 filter is problematic for rare variants (MAF < 0.05): only 12-38% of sites pass, which will severely deplete rare alleles and bias downstream statistics (e.g. Tajima's D, private allele counts). For population structure analysis using PCA or FST, a MAF > 0.05 filter combined with DR2 > 0.8 is more appropriate: this retains 71-89% of common sites where imputation is reliable. Rare variant analyses should either be restricted to WGS samples or use a genotype-likelihood approach rather than hard-call imputed genotypes.

**RUBRIC:**
Must identify that DR2 quality is highly MAF-dependent. Must flag that a uniform filter will disproportionately remove rare alleles. Should recommend MAF-stratified filtering or a combined MAF+DR2 threshold. Full marks only if the population structure vs. rare variant distinction is made. Partial: identifies MAF dependence but gives no concrete recommendation.

**NOTES:** This item tests a non-obvious failure mode: LLMs tend to accept uniform DR2 thresholds without questioning the MAF stratification issue.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_fcoeff_001
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> The following table shows heterozygosity rates and inbreeding coefficients (F) for 8 anonymized cannabis cultivar samples from a RAD-seq dataset imputed against a WGS reference panel. What does the F-coefficient distribution tell you about the breeding population structure of these drug-type cannabis cultivars?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
The uniformly positive F-coefficients (0.44–0.71) indicate excess homozygosity relative to HWE across all samples. This is consistent with a highly inbred breeding population — expected for drug-type cannabis cultivars which undergo intensive line selection. The range suggests varying degrees of inbreeding: samples with F > 0.65 (TC_072, TC_033, TC_011, TC_001) likely represent highly stabilized lines (multiple generations of selfing or backcrossing), while F ~ 0.45 (TC_013, TC_014) suggests more recent crosses or a broader genetic base. The absence of negative F values (heterozygote excess) confirms no recent outbreeding to unrelated populations.

**RUBRIC:**
Full marks (3): Identifies excess homozygosity from uniformly positive F, links to inbreeding/line selection in cannabis breeding, and interprets the F range meaningfully (high F = stabilized lines, lower F = recent crosses). Mostly correct (2): Gets homozygosity/inbreeding interpretation right but doesn't discuss what the range of F values implies. Partial (1): Mentions F relates to homozygosity but misinterprets direction or doesn't connect to cannabis breeding biology. Incorrect (0): Misidentifies negative F or claims the population is in HWE. Major error flag: Claiming F > 0 indicates a population bottleneck rather than directional inbreeding from line selection.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_fst_001
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: wgs

**PROMPT:**
> The following pairwise Weir-Cockerham FST estimates were computed between four cannabis populations using the WGS reference panel (n>30 per group). Interpret the population differentiation pattern. Which two populations are most genetically similar, and what does the FST between drug-type cannabis and hemp suggest about their evolutionary history?

**CONTEXT:**
```
Pairwise FST matrix (Weir-Cockerham estimator, 197,412 LD-pruned SNPs):

                    Drug-type  Hemp-fiber  Feral-CA  Feral-EU
Drug-type           0.000
Hemp-fiber          0.183      0.000
Feral-CA            0.094      0.221       0.000
Feral-EU            0.211      0.157       0.248     0.000

All FST estimates p < 0.001 (permutation test, 1000 permutations).
```

**CORRECT ANSWER:**
Drug-type and Feral-CA are most similar (FST=0.094). Drug-type vs. hemp-fiber FST=0.183 indicates moderate-to-high differentiation consistent with divergent selection under domestication for distinct end-uses (cannabinoid vs. fiber production), suggesting a long history of independent breeding from a shared ancestral gene pool rather than a recent split.

**RUBRIC:**
Must correctly identify Drug-type / Feral-CA as the most similar pair (lowest FST=0.094). Must interpret Drug-type vs Hemp FST=0.183 as moderate-high differentiation and link it to divergent selection / breeding history. Major errors: reading FST table incorrectly, or stating the two groups are closely related.

**NOTES:** Values are representative of the True Cultivar / PRJNA866500 cohort analysis.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_gp_001
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> The table below shows mean genotype posterior confidence (GP%) by 1 Mb window on cannabis chromosome NC_044370.1 for 85 imputed samples. The first 5 Mb and the last 2 Mb of the chromosome show notably lower GP confidence than the interior regions. What biological or technical factors explain this pattern?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
The lower GP confidence in the first 5 Mb (88.6-92.0%) corresponds to the pericentromeric region of NC_044370.1. Pericentromeric regions have (1) suppressed recombination, leading to longer haplotype blocks with less informative LD for imputation, (2) higher repeat content which reduces alignment quality and reference panel informativeness, and (3) lower variant density in the reference panel at these positions. The 19-20 Mb region shows high GP (95.1%) but very few variants (2,247), suggesting this is a gene-poor region with few sites to impute. The interior regions (8-11 Mb) achieve 94-95% GP because they have both high variant density and strong LD from recombination, making imputation most reliable.

**RUBRIC:**
Full marks (3): Identifies pericentromeric effect (suppressed recombination, repeat content), links to imputation mechanism (LD-based inference requires informative haplotypes). Mostly correct (2): Notes positional dependence but attributes only to variant density without mentioning recombination. Partial (1): Mentions GP varies but gives no mechanistic explanation. Incorrect (0): Claims it is random noise or a software bug. Major error: Attributing low GP to sample quality rather than genomic position.

**NOTES:** Tests whether the model can connect positional variation in imputation quality to pericentromeric genomic features. All sample IDs anonymized; data derived from RAD-seq imputation on CS10 cannabis assembly.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_gp_002
**Tier**: 2 | **Difficulty**: 2 | **Type**: comparison | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> Two 1 Mb regions on chromosome NC_044370.1 have different imputation profiles. Region A (6-7 Mb) has mean GP = 94.4% with 33,286 variants. Region B (19-20 Mb) has mean GP = 95.1% with only 2,247 variants. A researcher concludes that Region B has 'better imputation quality' because of higher GP. Is this conclusion valid? Explain.

**CONTEXT:**
```
Region     Mean_GP(%)  N_Variants  Min_GP(%)
6-7 Mb     94.41       33,286      2.4
19-20 Mb   95.09        2,247      11.8

Panel: 85 RAD-seq samples imputed via GLIMPSE2 against 492-sample WGS panel.
Total chromosome variants: ~15.3M imputed sites.
```

**CORRECT ANSWER:**
The conclusion is misleading. Region B's higher mean GP is partly an artifact of having far fewer variants -- only 2,247 vs 33,286. With fewer sites, the imputation algorithm only attempts variants where it has high confidence (likely common, well-tagged SNPs), inflating the mean. Region A imputes 15x more variants including rare and difficult sites, which pulls the mean GP down but provides far more information. The Min_GP tells a different story: Region B's minimum (11.8%) is higher than Region A's (2.4%), but this again reflects the filtered variant set. For downstream analyses, Region A provides better coverage despite slightly lower mean GP. Imputation quality should be assessed jointly by GP confidence AND variant yield, not GP alone.

**RUBRIC:**
Full marks (3): Identifies the variant count confound, explains why fewer variants inflate mean GP, recommends joint assessment. Mostly correct (2): Notes the variant count difference but doesn't explain the mechanism. Partial (1): Agrees the conclusion is wrong but for the wrong reason. Incorrect (0): Agrees with the researcher's conclusion. Major error: Treating mean GP as the sole quality metric.

**NOTES:** Tests understanding of the GP-variant density tradeoff. A common pitfall is treating mean GP as a standalone quality metric without considering the number of variants attempted.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_het_001
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> Sample TC_014 has the highest heterozygosity rate in the panel (12.19%) alongside the lowest genotype posterior confidence (GP=90.31%). The population average heterozygosity is ~10.1%. Is this elevated heterozygosity a quality concern or a genuine biological signal? What additional evidence would help you distinguish between the two explanations?

**CONTEXT:**
```
Per-sample QA metrics for selected samples (RAD-seq imputed against WGS panel):

Sample    Het_Rate(%)   GP_Confidence(%)   F_Coefficient
TC_014    12.19         90.31              0.437
TC_035    10.99         94.01              0.492
TC_057    10.15         93.75              0.531
TC_072    6.34          94.43              0.707

Population summary (85 drug-type cultivars): mean Het = 10.1%, SD = 1.6%, mean GP = 92.7%.
Imputation method: Beagle 5.4 against 492-sample WGS reference panel, 15.3M variants.
```

**CORRECT ANSWER:**
TC_014's het rate (12.19%) is ~1.3 SD above the mean — elevated but not extreme. However, its low GP confidence (90.31%) raises a quality concern: imputation at lower confidence can inflate heterozygosity because uncertain genotype calls are more likely to be assigned heterozygous genotypes by the imputation algorithm. To distinguish quality artifact from biology: (1) check if high het is concentrated at low-DR2 sites — if so, it reflects imputation uncertainty rather than true genotype variation; (2) compare het rate before vs after applying a DR2 > 0.8 filter — if het rate normalizes after filtering, it is an imputation artifact; (3) check if this sample has lower RAD-seq read coverage than others, which would explain lower imputation confidence. If het rate persists after stringent quality filtering, the sample may genuinely be an F1 hybrid or a less-inbred cultivar with a broader genetic base.

**RUBRIC:**
Full marks (3): Identifies the GP/het correlation as a potential imputation artifact (lower confidence inflates het calls), and provides at least 2 concrete diagnostic steps (e.g., DR2 filtering, coverage check, pre/post filter comparison). Mostly correct (2): Notes the quality concern from low GP but doesn't propose specific diagnostics to resolve it. Partial (1): Mentions het is elevated but attributes it entirely to biology (e.g., F1 hybrid) without considering imputation quality as a confound. Incorrect (0): Dismisses the observation as unimportant or misinterprets the metrics. Major error flag: Concluding the sample is contaminated based on heterozygosity rate alone.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_ibs_001
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> Two genomic windows on chromosome NC_044374.1 show elevated mean identity-by-state (IBS) compared to the chromosome-wide average. Interpret what these hotspots indicate about the genomic region and the population.

**CONTEXT:**
```
Chromosome-wide mean IBS: 0.832 (85 drug-type cannabis samples, 1000-variant sliding windows)

IBS Hotspots on NC_044374.1:
Window    Start       End        Mean_IBS   N_Variants
1         27,678      56,527     0.925      1,000
14        460,195     489,241    0.915      1,000

For comparison, typical windows on this chromosome:
Window    Start       End        Mean_IBS   N_Variants
50        2,104,339   2,178,521  0.831      1,000
100       5,421,876   5,512,003  0.829      1,000
```

**CORRECT ANSWER:**
The two hotspots show mean IBS of 0.915-0.925 vs. the chromosome average of 0.832 -- approximately 10% higher allele sharing. Both are in the first 500 kb of the chromosome, likely pericentromeric or subtelomeric. Possible explanations: (1) a selective sweep has driven one or a few haplotypes to high frequency in this breeding population, reducing diversity, (2) the region has lower recombination rate (pericentromeric), preserving longer identical-by-descent tracts, or (3) structural variation or repeat content reduces effective polymorphism. In a drug-type cannabis breeding population, selective sweeps around cannabinoid biosynthesis or flowering time genes would be consistent with the first explanation. The positional clustering (both within 500 kb of chromosome start) supports the pericentromeric hypothesis.

**RUBRIC:**
Full marks (3): Identifies at least 2 plausible mechanisms (selective sweep, low recombination), notes positional clustering, connects to breeding population context. Mostly correct (2): Gives one correct explanation but misses the positional clustering. Partial (1): Notes IBS is elevated but offers no biological mechanism. Incorrect (0): Misinterprets IBS direction or claims it's a data error. Major error: Confusing high IBS with high diversity.

**NOTES:** Tests interpretation of localized IBS elevation in the context of cannabis population genetics. All sample IDs anonymized; window-level summary statistics only.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_ibs_002
**Tier**: 2 | **Difficulty**: 3 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> The table below shows mean and range of window-level IBS scores across 5 cannabis chromosomes. Chromosome NC_044371.1 has both the lowest minimum IBS (0.755) and the widest range. What does this cross-chromosome variation suggest?

**CONTEXT:**
```
Chromosome-level IBS summary (85 drug-type samples, 1000-variant windows):

Chromosome       Mean_IBS  Min_IBS  Max_IBS  Range    N_Windows
NC_044370.1      0.841     0.780    0.907    0.127    20
NC_044371.1      0.822     0.755    0.900    0.145    18
NC_044372.1      0.849     0.802    0.893    0.091    16
NC_044373.1      0.838     0.789    0.884    0.095    15
NC_044374.1      0.843     0.791    0.925    0.134    14

Note: Cannabis sativa has 10 chromosomes (CS10 assembly). Window size = 1,000 variants.
```

**CORRECT ANSWER:**
The cross-chromosome variation reflects differences in recombination landscape, gene density, and selective history. NC_044371.1 has the lowest minimum IBS (0.755) and widest range (0.145), suggesting it contains both highly selected regions (high IBS near 0.90) and regions of high diversity (low IBS at 0.755). The low-IBS windows may correspond to regions under balancing selection or recent introgression from diverse germplasm. NC_044372.1 has the narrowest range (0.091) and highest minimum (0.802), suggesting more uniform selection or a more homogeneous recombination landscape. NC_044374.1 has the highest maximum (0.925, the two hotspots) but otherwise moderate diversity. In a breeding population, chromosomes carrying major-effect loci (e.g., cannabinoid pathway genes) would show more extreme IBS heterogeneity than chromosomes without strong selection targets.

**RUBRIC:**
Full marks (3): Connects IBS variance to recombination, selection, and gene content; identifies NC_044371.1's wide range as evidence of mixed selective pressures; mentions the breeding context. Mostly correct (2): Identifies recombination or selection but doesn't link to specific chromosomal features. Partial (1): Describes the numbers but offers no population genetics interpretation. Incorrect (0): Claims all chromosomes should have identical IBS distributions. Major error: Attributing cross-chromosome variance solely to technical artifacts.

**NOTES:** Difficulty 3 item requiring expert-level synthesis across chromosomes. Tests whether the model can integrate recombination landscape, selection, and breeding history to explain IBS heterogeneity. All sample IDs anonymized.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_kinship_001
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> The following table shows pairwise KING-robust kinship coefficients and IBS0 statistics for six sample pairs from a cannabis genetics study. Using the standard KING thresholds (Duplicate/MZ twin: >0.354, First-degree: 0.177–0.354, Second-degree: 0.0884–0.177, Third-degree: 0.0442–0.0884, Unrelated: <0.0442), classify each pair's relationship degree. Comment on any notable differences in IBS0 between pairs in the same relationship category.

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
Pair 1 (TC_042/TC_023, kinship=0.290): First-degree (0.177–0.354). Pair 2 (WGS_247/WGS_221, kinship=0.246): First-degree (0.177–0.354). Pair 3 (TC_011/TC_009, kinship=0.102): Second-degree (0.0884–0.177). Pair 4 (TC_004/WGS_221, kinship=-0.012): Unrelated (<0.0442). Pair 5 (TC_016/WGS_300, kinship=0.031): Unrelated (<0.0442). Pair 6 (TC_055/TC_042, kinship=0.114): Second-degree (0.0884–0.177). Notably, pairs 1 and 2 are both classified as first-degree, but pair 1 (imputed panel) has a much lower IBS0 (0.00577) compared to pair 2 (WGS panel, IBS0=0.02032). This difference likely reflects imputation smoothing in the TrueCut panel, where imputed genotypes tend to reduce observed IBS0 by filling in missing data with population-frequency haplotypes rather than reflecting a true biological difference in relatedness type.

**RUBRIC:**
Must correctly classify all six pairs into the appropriate KING threshold categories. Must note the IBS0 discrepancy between pairs 1 and 2 despite both being first-degree, and attribute it to imputation effects rather than a biological difference. Must correctly handle negative kinship (pair 4) as unrelated. Major errors: misclassifying any pair's relationship degree, interpreting negative kinship as an error, or failing to note the IBS0 difference between imputed and WGS first-degree pairs.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_kinship_002
**Tier**: 2 | **Difficulty**: 3 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> The following table shows KING-robust kinship coefficients for four cannabis sample pairs, all classified as first-degree relatives. Additional genotype discordance analysis is provided for a subset of samples. Are all four pairs the same type of relationship? How would you distinguish clones from first-degree relatives in this dataset, and what metric is most informative for making that distinction?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
These four pairs are not all the same type of relationship despite having similar kinship coefficients in the first-degree range (0.281–0.290). Pairs 1–3 (TC_042, TC_023, TC_009) form a clone group, while pair 4 (TC_062/TC_016) is a true first-degree relative pair (parent-offspring or full siblings). Kinship values alone cannot distinguish clones from parent-offspring at these values because both fall within the first-degree range (0.177–0.354). The key evidence for clonality comes from: (1) IBS0 — all clone-group pairs have extremely low IBS0 (<0.006), meaning nearly zero loci where the two samples share no alleles; true parent-offspring pairs will have measurable IBS0 since offspring inherit only one allele from each parent. (2) The genotype discordance analysis showing only 3.9% differences across 100K variants, consistent with somatic mutation and imputation noise rather than Mendelian segregation. (3) The mean kinship within the group (0.361) exceeds the standard duplicate threshold (>0.354) when computed across the full variant set, confirming clonality. IBS0 is the single most informative discriminator: clones should have near-zero IBS0, while parent-offspring pairs will have measurable IBS0 from loci where the parents are heterozygous for different alleles. The individual pairwise kinship values (0.287–0.290) fall below the standard duplicate threshold of 0.354 because imputation noise inflates genotype differences, illustrating that the KING duplicate threshold was designed for directly genotyped or sequenced data, not imputed data.

**RUBRIC:**
Must explain that kinship alone cannot distinguish clones from parent-offspring when values fall in the first-degree range. Must identify IBS0 as the key discriminator (clones have near-zero IBS0). Must reference the discordance analysis (3.9%) as supporting evidence for clonality. Must note that the individual pairwise kinship values (0.287–0.290) are below the duplicate threshold (0.354) due to imputation noise, while the group mean (0.361) exceeds it. Should mention vegetative propagation as the biological mechanism. Major errors: stating that kinship >0.354 is required for clone detection (the KING duplicate threshold is designed for identical genotyping, not imputed data where clones may show lower kinship due to imputation noise), or failing to identify IBS0 as the key clone-vs-parent-offspring discriminator.

**NOTES:** Pair 4 (TC_062/TC_016) also has very low IBS0 (0.00563), which is a deliberate challenge — the model should note this similarity but still distinguish the pair from the clone group based on the absence of discordance analysis data and the lack of a three-way clustering pattern.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_kinship_003
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> The following table shows KING-robust kinship coefficients for four sample pairs from a cannabis genetics study. Two of the pairs have negative kinship values. What do negative KING kinship coefficients mean? Should negative values be treated as a data quality concern?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
Negative KING kinship coefficients do not mean the samples are 'more unrelated than random' or that there is a data quality problem. KING-robust estimates kinship relative to the average allele sharing in the sample population. A negative value indicates that the pair shares fewer alleles than the population average. This typically occurs when the two samples come from different subpopulations — in this case, cross-panel pairs comparing drug-type cannabis (TrueCut_Imputed) against hemp or feral reference samples (WGS_Reference). Because drug-type cannabis and hemp have been under divergent selection for different traits (cannabinoid production vs. fiber/grain), they carry different allele frequencies at many loci, leading to below-average allele sharing and thus negative kinship estimates. This is an expected and well-understood property of the KING-robust estimator in multi-population datasets. Pair 1 (kinship=-0.012) shows the strongest negative signal, likely reflecting the greatest population differentiation between those two samples. Pair 2 (kinship=0.008) is near zero, still consistent with unrelated cross-population samples. Neither value indicates a data quality issue. In contrast, pair 4 (kinship=0.290) is within the same panel and shows strong first-degree relatedness.

**RUBRIC:**
Must explain that negative KING kinship reflects below-average allele sharing relative to the sample population, not an error. Must connect negative values to population structure (drug-type vs. hemp/feral samples from different subpopulations). Must state that this is expected behavior for the KING-robust estimator in multi-population panels. Should note that the cross-panel pairs span different cannabis types under divergent selection. Major errors: interpreting negative kinship as a data quality problem, interpreting it as meaning the samples are biologically incompatible, or failing to connect negative values to population substructure.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_kinship_004
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> The following symmetric kinship matrix shows KING-robust kinship coefficients for five cannabis samples from the TrueCut_Imputed panel. Identify which samples form a close genetic cluster and describe the overall relatedness structure among all five samples. Use the standard KING thresholds for relationship classification (Duplicate/MZ twin: >0.354, First-degree: 0.177–0.354, Second-degree: 0.0884–0.177, Third-degree: 0.0442–0.0884, Unrelated: <0.0442).

**CONTEXT:**
```
KING-robust pairwise kinship matrix (TrueCut_Imputed panel, imputed genotypes):

            TC_042  TC_023  TC_009  TC_055  TC_004
TC_042      0.500   0.290   0.290   0.114   0.043
TC_023      0.290   0.500   0.287   0.116   0.039
TC_009      0.290   0.287   0.500   0.115   0.041
TC_055      0.114   0.116   0.115   0.500   0.045
TC_004      0.043   0.039   0.041   0.045   0.500

Diagonal values of 0.5 represent self-kinship (expected for non-inbred diploids).
```

**CORRECT ANSWER:**
TC_042, TC_023, and TC_009 form a tight genetic cluster with pairwise kinship values of 0.287–0.290, all within the first-degree range (0.177–0.354). The remarkably similar and high kinship values among all three pairs, combined with the symmetric three-way pattern, strongly suggest these are clones or full siblings rather than independent parent-offspring pairs (a parent-offspring trio would not produce three nearly identical pairwise kinship values). TC_055 is second-degree related to all three clone-group members (kinship 0.114–0.116, within the 0.0884–0.177 range), suggesting it shares one parent with the clone group or is a half-sibling. The consistent second-degree kinship to all three members of the clone group reinforces that TC_055 is related to the lineage, not just one individual. TC_004 sits at the boundary between unrelated and third-degree relative to the other samples: kinship of 0.043 to TC_042 (just above the 0.0442 third-degree threshold), 0.039 to TC_023 (unrelated), 0.041 to TC_009 (unrelated), and 0.045 to TC_055 (just above third-degree). These borderline values suggest TC_004 is essentially unrelated to the other samples, with the marginal values likely reflecting background population structure rather than recent shared ancestry.

**RUBRIC:**
Must identify TC_042, TC_023, and TC_009 as a tight cluster with first-degree kinship (~0.29). Must note the three-way symmetry as evidence for clonality or full sibship rather than independent parent-offspring pairs. Must classify TC_055 as second-degree related to the clone group (~0.114–0.116). Must classify TC_004 as unrelated or borderline third-degree (~0.039–0.045). Should note that TC_055's consistent second-degree relatedness to all clone-group members suggests a half-sibling or shared-parent relationship. Major errors: failing to identify the three-sample cluster, misclassifying relationship degrees, or interpreting the diagonal values as meaningful relatedness.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_kinship_005
**Tier**: 2 | **Difficulty**: 3 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> The pair TC_012 / TC_010 has a KING kinship coefficient of 0.173, which falls just below the standard first-degree threshold of 0.177. A researcher classifies this as second-degree. Is this classification reliable? What factors could cause a true first-degree pair to fall below the threshold?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
The classification is not reliable at this boundary. TC_012/TC_010 at 0.173 is only 0.004 below the first-degree cutoff (0.177), well within estimation noise. Several factors can deflate kinship in imputed data: (1) imputation errors at low-DR2 sites introduce random genotype discordance, reducing apparent allele sharing, (2) high homozygosity (F>0.5) in inbred cannabis lines compresses the kinship coefficient range because there is less heterozygosity to detect sharing, (3) the KING thresholds were calibrated for outbred human populations, not inbred plant cultivars. The low IBS0 (0.016) — similar to the confirmed first-degree pair TC_075/TC_079 (IBS0=0.014) — suggests this pair shares very few opposite-homozygote sites, more consistent with first-degree than second-degree. Recommend treating this as a probable first-degree pair requiring manual review.

**RUBRIC:**
Full marks (3): Identifies boundary uncertainty, explains at least 2 factors that deflate kinship in imputed/inbred data, uses IBS0 as supporting evidence. Mostly correct (2): Notes the boundary issue but only gives one deflation factor. Partial (1): Says the classification might be wrong but doesn't explain why. Incorrect (0): Accepts the second-degree classification without question. Major error: Claiming KING thresholds are always definitive regardless of data type.

**NOTES:** TC_012 and TC_010 are anonymized cultivar IDs. Kinship value 0.173 is from actual KING-robust analysis and falls in the boundary zone between first- and second-degree relatedness. This item tests understanding of threshold sensitivity in imputed, inbred plant data.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_kinship_006
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> Two first-degree pairs are identified in the panel. Pair A (WGS_247/WGS_221, both from WGS reference panel) has KINSHIP=0.246. Pair B (TC_075/TC_079, both RAD-seq imputed) has KINSHIP=0.195. Both are classified as first-degree. Why is there a systematic difference in kinship magnitude between WGS and imputed samples?

**CONTEXT:**
```
Pair A (WGS):      KINSHIP=0.246, IBS0=0.02032, N_SNPs=1,387,334
Pair B (Imputed):  KINSHIP=0.195, IBS0=0.01389, N_SNPs=1,387,334

Panel summary:
  WGS reference:     492 samples, hard-call genotypes (DeepVariant+GLnexus)
  TrueCut imputed:    85 samples, imputed genotypes (GLIMPSE2, mean DR2=0.72)
```

**CORRECT ANSWER:**
The systematic kinship deflation in imputed samples (0.195 vs 0.246 for the same relationship degree) is expected and has two main causes: (1) Imputation introduces genotype uncertainty — even at DR2=0.72, a fraction of genotypes are miscalled, creating artificial discordance that lowers kinship estimates. This disproportionately affects allele-sharing metrics. (2) The KING-robust estimator assumes hard-call genotypes are accurate. When imputed hard calls carry uncertainty, the estimator systematically underestimates kinship. This is why Pair B (KINSHIP=0.195) falls lower in the first-degree range than Pair A (0.246) despite potentially being the same biological relationship. This bias should be accounted for when applying standard thresholds to imputed data — consider lowering thresholds by ~0.02-0.05 for imputed panels.

**RUBRIC:**
Full marks (3): Identifies imputation error as the cause, explains the mechanism (hard-call assumption violation), recommends threshold adjustment. Mostly correct (2): Notes the difference but attributes it to 'data quality' without specifics. Partial (1): Observes the difference but offers no explanation. Incorrect (0): Claims the pairs have different biological relationships. Major error: Attributing the difference to population structure rather than genotype accuracy.

**NOTES:** Kinship values are from actual KING-robust analysis. WGS pair from reference panel, imputed pair from RAD-seq GLIMPSE2 panel. Tests understanding of how genotype accuracy affects kinship estimation.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_qa_001
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> Using the quality tier criteria below, assign each of the 4 samples to the appropriate tier (A, B, or C). Justify each assignment by showing which criteria were met or failed.

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
TC_001 → Tier A: GP=93.71% >= 93.4%, |Het_z|=1.44 < 2.0, |F_z|=1.44 < 2.0 — all three Tier A criteria met. TC_004 → Tier B: GP=91.72% >= 91.0% but < 93.4%, so fails the Tier A GP threshold; no outlier flags, so qualifies for Tier B. TC_013 → Tier C: GP=89.80% < 91.0%, which triggers Tier C regardless of z-scores. TC_014 → Tier C: GP=90.31% < 91.0%, which triggers Tier C. The tier system prioritizes genotype posterior confidence (GP%) as the primary quality metric, with z-scores serving as secondary guards against statistical outliers. Notably, TC_014 narrowly misses Tier B (GP 90.31% vs 91.0% threshold), which could be revisited if the sample has high biological value.

**RUBRIC:**
Full marks (3): Correctly assigns all 4 tiers with explicit threshold comparisons for each sample. Mostly correct (2): Gets 3 out of 4 assignments correct with reasonable justification. Partial (1): Gets the logic right for at least 2 samples but makes errors on boundary cases. Incorrect (0): Misapplies the criteria systematically (e.g., using z-scores as primary rather than GP). Major error flag: Confusing which metric drives each tier boundary, or reversing the tier direction (assigning high-GP samples to Tier C).

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier2_tajima_001
**Tier**: 2 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: wgs

**PROMPT:**
> The following Tajima's D values were computed in 50 kb windows across chromosome NC_044370.1 for two cannabis population groups. Interpret the difference between the two distributions and what it implies about the demographic and selective history of each group.

**CONTEXT:**
```
Tajima's D summary statistics (50 kb windows, NC_044370.1, WGS data):

Group             N samples  Mean D   Median D  % windows D < -1.5  % windows D > 1.5
Drug-type (TC)    82         -0.81    -0.93     34%                  4%
Hemp-fiber (IPK)  130        +0.22    +0.18     8%                   19%

Minimum window SNPs: 50. Windows with <50 SNPs excluded.
```

**CORRECT ANSWER:**
Drug-type cannabis shows strongly negative Tajima's D (mean -0.81, 34% of windows below -1.5), consistent with a population expansion or selective sweeps removing variation — expected under intensive selective breeding for high-THC content. Hemp-fiber shows near-neutral to slightly positive D (mean +0.22, 19% of windows above +1.5), consistent with balancing selection or a population bottleneck followed by admixture, plausible given the diverse European germplasm in the IPK hemp collection. The contrast supports divergent breeding histories rather than a shared recent demographic event.

**RUBRIC:**
Must correctly interpret negative D as expansion/selection and positive D as balancing selection or bottleneck+admixture. Must link interpretations to the biology (intensive THC breeding vs diverse hemp germplasm). Major errors: reversing the interpretation of D sign, or treating both groups as having the same demographic history.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

## Tier 3 -- Structure (16 items)

---
### tier3_admix_001
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> ADMIXTURE was run on 323 cannabis WGS samples at K=2, K=3, and K=4. Below are Q-values for 5 representative samples across the three K values. Which K is most informative for classifying cultivars by cannabinoid type (THC-dominant vs CBD-dominant vs balanced), and why?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
K=4 is the most informative for cultivar classification by cannabinoid type. At K=2, drug-type and hemp separate cleanly, but CBD cultivars (TC_004=0.68, TC_079=0.62 drug component) appear as partially admixed drug-type samples — the model cannot distinguish THC-dominant from CBD-dominant cultivars. At K=3, a landrace component emerges but CBD cultivars still split between drug-type and landrace components without a dedicated CBD cluster. At K=4, a fourth component (CBD-drug) appears that specifically captures CBD cultivar genetics: TC_004 and TC_079 both show ~0.45-0.47 in Comp_4, cleanly separating them from THC-dominant cultivars (TC_036=0.04, TC_062=0.06 in Comp_4). This is biologically meaningful because modern CBD cultivars were bred by introgressing CBD-producing alleles from hemp/landrace backgrounds into drug-type breeding lines, creating a genetically distinct subpopulation that K=2 and K=3 collapse into drug-type. The cross-validation error also supports K=4 (0.391, lowest among K=2-5).

**RUBRIC:**
Full marks (3): Selects K=4, explains that it resolves CBD cultivars as a distinct component that lower K values collapse into drug-type or split between drug and landrace, references the Q-values for CBD samples at each K, and notes the cross-validation error supports K=4. Mostly correct (2): Selects K=4 with correct reasoning about CBD resolution but does not trace the progression through K=2 and K=3 or does not mention cross-validation. Partial (1): Selects K=3 or K=4 but reasoning is vague or focuses only on cross-validation error without interpreting the biological meaning of the components. Incorrect (0): Selects K=2 or K=3 as most informative, or selects K=4 for wrong reasons. Major error: Claiming K=2 is best because it has the clearest separation, ignoring that it cannot distinguish THC from CBD cultivars.

**NOTES:** Q-values are constructed to illustrate the progressive resolution of CBD cultivar genetics. Cross-validation errors are realistic.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_admix_002
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> ADMIXTURE at K=3 was run on a cannabis panel including both THC-dominant and CBD-dominant cultivars. The three components correspond to drug-type, hemp-fiber, and landrace ancestry. Compare the ancestry proportions of the 4 CBD cultivars to the 4 THC cultivars below. What does this difference imply about how CBD production was achieved in modern cultivar breeding?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
CBD cultivars carry substantially more landrace ancestry (mean Comp_C=0.44) than THC cultivars (mean Comp_C=0.10), a 4.4-fold difference. They also show reduced drug-type ancestry (0.43 vs 0.86). This pattern strongly suggests that CBD production in modern cultivars was achieved by introgressing CBD-producing alleles from landrace populations — which are naturally CBD-dominant or produce balanced CBD:THC ratios — into drug-type breeding lines, rather than by de novo mutation within THC-dominant breeding pools. The ~44% landrace component in CBD cultivars indicates approximately half their genome derives from landrace backgrounds, consistent with one or two generations of backcrossing after an initial landrace x drug-type cross. The modest hemp component in CBD cultivars (0.13 vs 0.05) may reflect additional hemp introgression for CBD alleles or shared ancestry between hemp and landrace populations. This has practical implications: CBD cultivars occupy a genetically intermediate position between drug-type and landrace pools, making them useful bridge germplasm for introducing landrace diversity into drug-type breeding programs.

**RUBRIC:**
Full marks (3): Identifies the ~4x higher landrace ancestry in CBD vs THC cultivars, correctly infers introgression from landraces as the mechanism for CBD trait introduction (not mutation within drug-type), estimates the degree of backcrossing implied by ~44% landrace component, and notes the bridge genetics implications. Mostly correct (2): Gets the core inference (CBD cultivars derive CBD-producing alleles from landrace introgression) and cites the specific ancestry proportions, but does not discuss backcrossing extent or bridge genetics. Partial (1): Notes the difference in ancestry proportions but does not connect it to the mechanism of CBD trait origin, or vaguely mentions 'hybridisation' without specifying the direction (landrace into drug-type). Incorrect (0): Claims CBD and THC cultivars have similar genetic backgrounds, or attributes CBD production to selection within drug-type lines despite the ancestry evidence. Major error: Ignoring the landrace ancestry difference or claiming CBD production arose by mutation within THC-dominant lines.

**NOTES:** Ancestry proportions are constructed to illustrate the landrace introgression hypothesis for CBD cultivar origins. TC_004=Alpha Explorer, TC_006=Auto CBD, TC_075=Suver Haze, TC_079=The Wife.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_admix_003
**Tier**: 3 | **Difficulty**: 3 | **Type**: comparison | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> Two pairs of cannabis cultivars are presented with both ADMIXTURE ancestry proportions (K=3) and KING-robust kinship coefficients. Pair A has very similar ancestry proportions but moderate kinship. Pair B has dissimilar ancestry proportions but lower kinship. Which pair is more closely related, and why do ancestry proportions fail to predict kinship?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
Pair A (TC_057/TC_060, kinship=0.164) is more closely related than Pair B (TC_036/TC_055, kinship=0.094), despite Pair A having very similar ancestry proportions and Pair B having dissimilar ones. This illustrates a fundamental distinction between ancestry proportions and kinship. ADMIXTURE Q-values reflect population-of-origin composition — the proportion of an individual's genome that traces back to each ancestral population. Two unrelated individuals from the same breeding pool will have similar Q-values simply because they were drawn from the same population, not because they share recent ancestors. Kinship (KING-robust) measures identity-by-descent (IBD) — the proportion of the genome inherited from a specific recent common ancestor. TC_057 and TC_060 share a recent ancestor (half-sibs or avuncular, kinship=0.164 near the first-degree boundary) even though their similar ancestry proportions could be coincidental. TC_036 and TC_055 have different ancestry proportions (TC_036 is 85% drug-type while TC_055 is only 60%, with more hemp/landrace) indicating they come from different breeding pools, yet they still share some recent ancestry (kinship=0.094). The practical lesson: population ancestry proportions describe where genome segments originated, while kinship describes whether two individuals inherited specific segments from the same recent source. They measure different timescales and should not be used interchangeably.

**RUBRIC:**
Full marks (3): Correctly identifies Pair A as more closely related (higher kinship), clearly distinguishes ancestry proportions (population-of-origin) from kinship (recent IBD sharing), explains why similar Q-values do not imply close relatedness (same breeding pool), and explains why different Q-values do not preclude relatedness (different populations can share recent ancestors through crosses). Mostly correct (2): Identifies Pair A as more closely related and explains the ancestry vs kinship distinction, but does not fully articulate why similar ancestry proportions arise in unrelated individuals from the same population. Partial (1): Correctly identifies which pair is more related but conflates ancestry and kinship in the explanation, or provides a superficial distinction. Incorrect (0): Identifies Pair B as more closely related, or claims similar ancestry proportions indicate close relatedness. Major error: Stating that ancestry proportions predict kinship, or that dissimilar Q-values mean two samples cannot be related.

**NOTES:** Kinship values are from actual KING-robust analysis. This item tests understanding of the fundamental difference between population ancestry and individual relatedness.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_admix_004
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> At K=4, sample TC_005 shows near-equal ancestry proportions across all four components (0.28, 0.25, 0.22, 0.25). Most other samples have a dominant component (>0.60). Is TC_005 a genuinely admixed cultivar, or could this pattern be an artifact? What evidence would distinguish these explanations?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
A near-uniform ancestry profile (0.22-0.28 across 4 components) can be either biological or artifactual. Biological explanation: TC_005 is a genuinely admixed cultivar with recent ancestry from multiple breeding pools (drug-type, CBD, hemp, landrace), possibly an intentional cross between divergent lines. Artifact explanations: (1) the sample has low genotyping quality (low GP, high missingness), causing ADMIXTURE to assign diffuse ancestry rather than confident assignment, (2) the sample is from a population not well-represented by any of the K=4 components, forcing the algorithm to 'average' across components. To distinguish: check TC_005's GP confidence and DR2 distribution — if quality metrics are comparable to other samples, the admixture is likely real. Also run ADMIXTURE at K=5 and K=6 — if a new component emerges that TC_005 dominates, it represents a distinct genetic background rather than true admixture.

**RUBRIC:**
Full marks (3): Proposes both biological and artifact explanations, provides at least 2 concrete diagnostic steps (quality check, run higher K). Mostly correct (2): Mentions both possibilities but only one diagnostic. Partial (1): Accepts one explanation uncritically. Incorrect (0): Concludes it must be contamination. Major error: Claiming near-equal proportions always indicate poor data quality.

**NOTES:** TC_005 is an anonymized sample ID. This item tests the ability to distinguish genuine multi-way admixture from artifacts of poor genotype quality or model misspecification in ADMIXTURE analysis.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_admix_005
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> The table below shows ADMIXTURE cross-validation (CV) error for K=2 through K=8. Based on these results, what is the optimal K, and what does the CV error curve shape tell you about population structure?

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
The optimal K is 5 or 6, where CV error reaches its minimum (0.3918 and 0.3905 respectively). However, the curve shape is informative: the large drop from K=2 (0.452) to K=4 (0.394) indicates strong hierarchical structure — the first 2-3 splits capture major population divisions (likely drug-type vs hemp, then landrace separation). The plateau from K=4 to K=7 (0.394 to 0.391) shows diminishing returns — additional components capture fine-scale structure or noise. The slight uptick at K=8 (0.392) suggests overfitting. For practical purposes, K=4 is often preferred over K=5-6 because it captures the major biological groups without splitting them into sub-clusters that may reflect sampling bias. The choice between K=4 and K=6 should depend on the research question: K=4 for broad population assignment, K=6 for fine-scale admixture analysis.

**RUBRIC:**
Full marks (3): Identifies K=5-6 as statistical optimum, interprets the curve shape (steep drop then plateau), recommends K=4 as practical alternative with reasoning. Mostly correct (2): Picks the right K but doesn't interpret the curve shape. Partial (1): Picks a K but without reference to CV error pattern. Incorrect (0): Picks K=2 or K=8. Major error: Claiming the lowest K is always best, or that you should always use the statistical minimum.

**NOTES:** CV error values are representative of typical cannabis panel analyses. This item tests understanding of ADMIXTURE cross-validation interpretation and the distinction between statistical optimum and biologically meaningful K.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_admixture_001
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: wgs

**PROMPT:**
> The following ADMIXTURE Q-matrix was computed at K=3 on 323 cannabis WGS samples (drug-type, hemp-fiber, and feral populations). Interpret the ancestry composition of sample TC_017 and explain what the admixture pattern implies about its breeding history.

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
TC_017 carries predominantly drug-type ancestry (Comp_A=0.61) with substantial hemp-fiber ancestry (Comp_B=0.31) and minor feral/landrace ancestry (Comp_C=0.08). This mixed profile is consistent with a cultivar that derives from a drug-type breeding program that incorporated hemp genetics, possibly for fiber content, CBD profile, or broadened adaptation. The 31% hemp component is unusually high for a cultivar in the True Cultivar drug-type panel (compare TC_021 at 4% hemp) and should be flagged for investigation — it could reflect intentional hybridisation, mislabelling, or contamination.

**RUBRIC:**
Must correctly read Q-values for TC_017. Must identify the dominant component (drug-type) and the notable hemp admixture. Must compare to TC_021 to contextualise the unusual hemp proportion. Should recommend flagging/investigation. Partial: reads values correctly but does not flag the anomaly relative to other TC samples.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_clone_001
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> Clone detection was performed on 85 imputed cannabis cultivar samples using KING-robust kinship at multiple thresholds. The table below shows the number of clone groups and samples identified at each threshold. Explain how threshold choice affects clone detection in imputed data, and recommend the most appropriate threshold for this dataset.

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
At the canonical WGS threshold of 0.354 (or higher, e.g., 0.45), zero clones are detected — this is too stringent for imputed data because imputation introduces genotype uncertainty that systematically depresses kinship estimates below their true values. True clones that would show kinship ~0.5 in WGS data may show kinship ~0.35-0.40 after imputation noise. At threshold 0.35, one group of 3 samples (TC_042, TC_023, TC_009) is detected with mean kinship 0.361 and 3.9% discordance — this is consistent with true clones whose kinship was reduced by imputation error. At threshold 0.30, a second group (TC_011, TC_044) appears with kinship 0.308 and 7.2% discordance — this higher discordance and lower kinship suggests these may be parent-offspring or full-sibs rather than true clones. The 0.35 threshold is most appropriate for this imputed dataset because: (1) it accounts for imputation-reduced kinship while still requiring near-first-degree relatedness; (2) the detected group has low discordance (3.9%) supporting clonal identity; (3) dropping to 0.30 risks including parent-offspring pairs (Group 2's 7.2% discordance is too high for clones). The stability between 0.30 and 0.25 (same 2 groups, 5 samples) suggests no additional clone-like pairs exist in that kinship range.

**RUBRIC:**
Full marks (3): Explains that imputation depresses kinship below canonical WGS thresholds, recommends 0.35 as appropriate with correct reasoning (accounts for imputation noise, low discordance in Group 1), explains why 0.30 risks false positives (Group 2 has higher discordance consistent with parent-offspring rather than clones), and notes the threshold stability below 0.25. Mostly correct (2): Recommends 0.35 and explains the imputation depression of kinship, but does not use the discordance percentages to evaluate whether Group 2 represents true clones. Partial (1): Discusses threshold sensitivity but recommends 0.30 or 0.45 with incomplete reasoning, or does not address the imputation effect on kinship. Incorrect (0): Recommends 0.45 as appropriate, or fails to recognize that imputation affects kinship estimation. Major error: Claiming that the zero detections at 0.45 mean there are no clones in the panel, ignoring imputation effects.

**NOTES:** Clone threshold data from actual KING-robust analysis on TrueCut imputed panel. Group 1 represents a confirmed clone group; Group 2 is likely parent-offspring.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_family_001
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> Strain family clustering was performed on 85 drug-type cannabis cultivars using KING-robust kinship estimates. Five families were identified, with highly asymmetric sizes. Interpret what the family structure implies about breeding program diversity, and discuss practical consequences for downstream genetic analyses.

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
The extreme size asymmetry — Family 4 containing 73 of 85 cultivars (86%) — indicates that the drug-type cannabis breeding pool is genetically narrow, with most commercial cultivars descending from a small number of foundational lines. The remaining families (0-3) with 2-5 members each represent genetically distinct lineages: Family 1 (3 CBD cultivars with mean F=0.645 and highest within-family kinship at 0.198) is a tight cluster of highly inbred, closely related CBD breeding lines. Family 0 (5 members, within-kinship=0.147) and Family 2 (2 members, within-kinship=0.108) represent smaller but still distinct genetic groups. Family 4's mean within-kinship of 0.055 (third-degree level) confirms pervasive background relatedness — these cultivars are not independent samples but share distant common ancestry. Practical consequences: (1) GWAS statistical power is reduced because cryptic relatedness within Family 4 inflates test statistics unless a kinship matrix is included as a covariate; (2) genomic prediction models will overfit if training and test sets both draw from Family 4 without accounting for relatedness; (3) breeding programs should deliberately outcross to Family 0-3 germplasm (especially Family 1 CBD lines) to increase genetic diversity and heterosis; (4) the overall mean F of 0.538 indicates moderate-to-high inbreeding across the panel, consistent with intensive selection.

**RUBRIC:**
Full marks (3): Identifies the narrow genetic base implied by Family 4 dominance (86%), interprets Family 1 as a distinct CBD cluster, explains that mean within-kinship of 0.055 represents background relatedness (third-degree), and discusses at least two practical consequences (GWAS relatedness correction, breeding diversity implications). Mostly correct (2): Gets the core insight (narrow breeding pool, one dominant family) and mentions at least one practical consequence, but does not distinguish between the smaller families or discuss the kinship levels quantitatively. Partial (1): Notes the size asymmetry but interprets it superficially (e.g., 'most cultivars are similar') without connecting to breeding history or downstream analytical implications. Incorrect (0): Fails to recognize the asymmetry as meaningful or interprets Family 4 as the most diverse family. Major error: Claiming that 73 members in one family indicates high genetic diversity rather than a narrow breeding base.

**NOTES:** Family structure from actual KING-robust clustering on TrueCut panel. Family 1 CBD cultivars include samples like TC_083 (Wild Cat CBD), TC_034 (Fruit Leak CBD), and TC_075 (Suver Haze). The high background relatedness in Family 4 is typical of intensive crop breeding programs.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_family_002
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> Founder analysis was performed on 85 drug-type cannabis cultivars using a kinship-network-based scoring method. The top 5 cultivars by founder score are listed below. Interpret which cultivars are likely breeding hub genotypes versus derived lines, and what the score distribution implies about the structure of the cannabis breeding program.

**CONTEXT:**
```
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
```

**CORRECT ANSWER:**
TC_036 (score=0.218) and TC_055 (score=0.213) are the dominant founders — these cultivars have the highest network centrality, meaning they appear as parents or grandparents of the most other cultivars in the panel. Their scores are 4x the panel mean (0.052) and they each have 11-12 first/second-degree connections, indicating they are breeding hubs from which many other cultivars derive. TC_062 (0.170), TC_057 (0.145), and TC_004 (0.139) are secondary founders with progressively fewer connections. The steep drop-off from rank 1-2 (0.218-0.213) to rank 3-5 (0.170-0.139) indicates a highly hierarchical breeding structure dominated by 2-3 key parents. This is typical of intensive selection programs where a few elite genotypes are used extensively as breeding stock. TC_036 and TC_055 are both in Family 4 (the 73-member dominant family), confirming their role as the genetic backbone of the commercial breeding pool. Notably, TC_057 (Family 0) and TC_004 (Family 1, CBD) are founders from minority families, suggesting they contributed genetics from outside the main breeding pool — TC_004 as a CBD founder likely introduced cannabidiol-producing alleles into the broader program. The bottom 10 cultivars (scores 0.008-0.019) are terminal derived lines with minimal genetic contribution to other cultivars, representing the most recent products of breeding programs built on the top founders.

**RUBRIC:**
Full marks (3): Identifies TC_036 and TC_055 as dominant breeding hub founders, notes the steep score drop-off as indicating hierarchical breeding structure, connects founder family membership to their role (Family 4 founders vs minority-family founders like TC_004), and interprets the low-scoring cultivars as derived terminal lines. Mostly correct (2): Correctly identifies the top two as dominant founders and discusses the hierarchical breeding structure, but does not connect founder scores to family membership or discuss the role of TC_004 as a CBD-lineage founder. Partial (1): Notes that some cultivars have higher scores than others but does not interpret the score distribution quantitatively or explain what 'founder' means in the breeding network context. Incorrect (0): Misinterprets founder scores as genetic diversity measures or fails to identify the top-ranked cultivars as breeding hubs. Major error: Claiming that high founder scores indicate the cultivar is derived from many parents (confusing incoming vs outgoing genetic contribution).

**NOTES:** Founder scores from actual kinship network analysis. The top two founders dominate the breeding network, consistent with known cannabis breeding history.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_pca_001
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> The following PCA was computed on 1,080 cannabis samples (407 WGS + 673 imputed RAD-seq) using PCAngsd with 197,412 LD-pruned SNPs (DR2 > 0.8, MAF > 0.05). PC1 explains 53.1% and PC2 explains 19.0% of variance. Interpret the population structure and identify any potential concerns about the imputed samples.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
PC1 separates drug-type (positive) from hemp-fiber (negative) populations, capturing the primary domestication axis — this is the expected major axis of variation in cannabis. PC2 separates PRJNA1206134 hemp from IPK hemp, likely reflecting geographic/breeding origin differences within hemp. The imputed TC_cultivars cluster tightly with WGS drug-type samples (centroid distance ~0.01-0.03), suggesting imputation quality is sufficient to preserve population structure for this group. Concern: PRJNA1206134 shows higher within-study spread (0.147 vs 0.031 for TC), which may reflect genuine diversity or imputation noise from less well-represented hemp accessions in the WGS reference panel.

**RUBRIC:**
Must correctly identify PC1 as drug-type vs hemp axis. Must note that TC imputed samples cluster with WGS drug-type (validating imputation). Must identify the higher spread in PRJNA1206134 as a concern (could be reference panel representation or genuine diversity). Partial: identifies main axis but misses imputation quality concern.

**NOTES:** Values derived from actual PCAngsd run on the glNexus imputed cohort.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_pca_002
**Tier**: 3 | **Difficulty**: 3 | **Type**: comparison | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> A researcher computed PCA twice on the same 85 True Cultivar RAD-seq imputed samples: once using all imputed sites (DR2 > 0.3), and once using high-confidence sites only (DR2 > 0.8). The variance explained by PC1 increased from 41% to 53% when the stricter filter was applied, but the number of sites dropped from 12.4M to 3.1M. Two phenotypic replicates (same cultivar sequenced twice) are included. Interpret what the change in PC1 variance explained tells you, and explain whether you would prefer the DR2 > 0.3 or DR2 > 0.8 result for cultivar identity verification.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
The increase in PC1 variance explained (41% → 53%) when using DR2 > 0.8 indicates that low-quality imputed sites (DR2 0.3-0.8) add noise that dilutes the true population structure signal. More diagnostic: the signal-to-noise ratio (between-cultivar distance / within-replicate distance) improves from 1.15 to 2.44 with the stricter filter — a near doubling of discriminatory power. For cultivar identity verification, DR2 > 0.8 is strongly preferred: phenotypic replicate distance drops from 0.062 to 0.018, while between-cultivar distance remains meaningful at 0.044, giving much cleaner cultivar discrimination.

**RUBRIC:**
Must explain the PC1 variance increase as signal-to-noise improvement, not simply 'more variance'. Must use the replicate pair distances as the key discriminatory metric. Must recommend DR2 > 0.8 with correct reasoning (replicate distance much lower, between-cultivar distance sufficient). Partial: recommends correct filter without explaining the replicate-based rationale.

**NOTES:** Numbers match the actual True Cultivar phenotypic replicate validation analysis.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_pca_003
**Tier**: 3 | **Difficulty**: 2 | **Type**: comparison | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> PCA was computed using PCAngsd on two overlapping sample sets from the same imputed cannabis cohort. The full panel includes 706 samples spanning drug-type cultivars, hemp-fiber accessions, Chinese landraces, European hemp, and feral populations. The TrueCut-only subset includes 85 drug-type cultivars. Compare the variance explained by the top PCs in each analysis and explain why PC1 captures much more variance in the smaller subset.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
The full panel contains multiple genetically divergent populations (drug-type, hemp, Chinese landraces, European hemp, feral) that differ along several independent axes of variation — drug vs hemp, East vs West, cultivated vs feral. This distributes variance across multiple PCs (PC1=25.5%, PC2=14.8%, PC3=9.2%), with no single axis dominating. In the 85-sample TrueCut subset, all samples are drug-type cultivars, removing between-group axes. The remaining structure is dominated by a single axis (likely THC-type vs CBD-type, or high-inbreeding vs outcrossed), which concentrates 53.1% of variance in PC1. The lesson is that PCA variance proportions are relative to the sample composition — a higher PC1 percentage does not mean 'more structure'; it means the structure present is lower-dimensional. This is critical for interpreting cannabis population genomics because subsetting to a breeding pool collapses the multi-axis divergence into a simpler signal.

**RUBRIC:**
Full marks (3): Explains that adding diverse populations distributes variance across multiple independent axes, correctly identifies that the 85-sample subset is dominated by one axis concentrating variance in PC1, and notes that PCA variance proportions are relative to sample composition. Mostly correct (2): Gets the core insight (diverse panels spread variance, homogeneous panels concentrate it) but does not explicitly discuss the specific population groups creating multiple axes. Partial (1): Mentions sample composition matters but incorrectly attributes the difference to SNP count, sample size alone, or technical artifacts. Incorrect (0): Claims the TrueCut subset has 'more structure' or that the full panel result is wrong. Major error: Interpreting higher PC1 variance in the subset as indicating greater genetic diversity or stronger population differentiation.

**NOTES:** Variance values from actual PCAngsd runs. This item tests understanding that PCA eigenvalue proportions are relative to sample composition, not absolute measures of structure.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_pca_004
**Tier**: 3 | **Difficulty**: 2 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> Six cannabis samples from three genotyping panels were projected into a shared PCA space computed on 197K LD-pruned SNPs. Two samples are from whole-genome sequencing (WGS), two are from TrueCut RAD-seq imputed to WGS density, and two are from Kannapedia RAD-seq imputed to WGS density. From the PCA coordinates below, identify which samples are likely imputed (not WGS) and explain the artifact you observe.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
Samples S_C, S_D, and S_E have coordinates that are compressed toward the drug-type centroid across all three PCs — their PC1 values (0.271, 0.273, 0.269) cluster within a narrow 0.004 range near the centroid (0.275), and their PC2/PC3 values are all within ~0.01 of zero. In contrast, S_A (PC1=0.287, PC2=-0.041), S_B (PC2=+0.012), and S_F (PC1=0.291, PC2=+0.024) show larger deviations from the centroid, consistent with genuine genetic individuality captured by WGS. The imputed samples are likely S_C, S_D, and S_E (four of the six were supposed to be imputed — likely S_C/S_D from one imputed panel and S_E plus one other). The compression artifact arises because imputation replaces missing genotypes with population-frequency-weighted estimates, shrinking individual-specific variation toward population means. This is a known PCA artifact for imputed data: imputed samples have lower effective genetic individuality in PCA space, appearing artificially clustered. This can be mistaken for genuine genetic similarity if not accounted for.

**RUBRIC:**
Full marks (3): Correctly identifies that the samples closest to the centroid with smallest spread (S_C, S_D, S_E) are likely imputed, explains the compression/shrinkage artifact of imputation on PCA coordinates, and notes that imputation replaces missing data with population-frequency estimates that reduce individual-specific variation. Mostly correct (2): Identifies the compressed samples as imputed and mentions imputation artifacts, but does not explain the mechanism (frequency-weighted fill-in). Partial (1): Notices the difference in spread but attributes it to sequencing depth, batch effects, or quality differences rather than the imputation shrinkage mechanism. Incorrect (0): Identifies the wrong samples as imputed or fails to detect the pattern. Major error: Claiming the tightly clustered samples are WGS because they are 'more consistent' or 'higher quality'.

**NOTES:** Coordinates are constructed to illustrate the imputation compression artifact. S_A and S_F are WGS, S_B could be either. The key signal is the reduced PCA spread of imputed samples.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_pca_005
**Tier**: 3 | **Difficulty**: 3 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> Two cannabis cultivars, TC_033 and TC_032, are described as phenotypic variants of the same cultivar — TC_033 has white pistils and TC_032 has green pistils, but they share the same cultivar name and breeder. Both are highly inbred (inbreeding coefficient F > 0.71). Their KING-robust kinship coefficient is 0.108, classifying them as second-degree relatives. Given the high inbreeding and distinct phenotypes, what does the second-degree kinship tell us about the genetic architecture of the phenotypic difference between these two samples?

**CONTEXT:**
```
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

**CORRECT ANSWER:**
The second-degree kinship (0.108) between TC_033 and TC_032 is far below the duplicate threshold (>0.354) and even below first-degree (>0.177), meaning these are NOT clones or parent-offspring despite being sold as variants of the same cultivar. This rules out somatic mutation as the explanation for the pistil color difference — if the phenotypic difference were due to a somatic mutation in an otherwise identical genetic background, kinship would be at or near the duplicate level. Instead, the second-degree kinship (consistent with half-siblings sharing one parent) suggests the two 'variants' were bred from partially overlapping but distinct crosses. In highly inbred lines (F > 0.71), even modest genetic differences between parents can produce visible phenotypic divergence because inbreeding fixes alleles — a single segregating locus controlling pistil color could produce the observed difference. This finding is important for cultivar identity verification: these two should be classified as related but distinct genotypes, not as phenotypic variants of a single genotype. Breeders labeling them as the same cultivar is genetically inaccurate.

**RUBRIC:**
Full marks (3): Correctly interprets second-degree kinship as ruling out clonal/somatic mutation origin, explains that the phenotypic difference reflects distinct genetic backgrounds (likely half-sibs), connects high inbreeding to the visibility of small genetic differences, and notes implications for cultivar identity classification. Mostly correct (2): Gets the core point (not clones, not somatic mutation, distinct genetic backgrounds) but does not discuss how inbreeding amplifies phenotypic effects of small genetic differences. Partial (1): Correctly reads the kinship value but concludes they are 'closely related variants' without distinguishing this from clonal identity, or fails to address the somatic mutation hypothesis. Incorrect (0): Claims the kinship supports them being the same cultivar, or interprets second-degree as 'essentially identical'. Major error: Stating that second-degree kinship is consistent with somatic mutation or clonal propagation.

**NOTES:** TC_033 and TC_032 are phenotypic variants of the same cultivar (white vs green pistil morphology). The kinship value (0.108) is from actual KING-robust analysis. This item tests whether the model can distinguish clonal identity from familial relatedness in the context of cultivar verification.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_pca_006
**Tier**: 3 | **Difficulty**: 3 | **Type**: interpretation | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> In a PCA of 706 cannabis samples, one drug-type cultivar (TC_048) clusters far from other drug-type samples and instead falls near the hemp/landrace cluster. The sample passed all QC filters (call rate > 0.95, no excess heterozygosity). Evaluate whether this positioning is most likely due to (a) sample mislabeling, (b) DNA contamination, or (c) genuine admixture, and describe what additional evidence would distinguish among these explanations.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
TC_048's PCA position (PC1=-0.198) places it between the drug-type centroid (+0.275) and the hemp/landrace centroids (-0.295 / -0.234), not firmly in any cluster. The ADMIXTURE profile (38% drug, 41% hemp, 21% landrace) shows tri-partite ancestry rather than one dominant component, which is more consistent with genuine admixture than with mislabeling or contamination. Mislabeling would produce a clean hemp or landrace profile (e.g., Comp_B > 0.85), not a three-way mixture. Contamination (cross-sample DNA mixing) would manifest as excess heterozygosity, but TC_048's het rate (0.312) is within the normal drug-type range (0.28-0.35) and its F (0.285) is within the drug-type range, arguing against gross contamination. Genuine admixture is the most parsimonious explanation: TC_048 is likely a hybrid between drug-type and hemp/landrace germplasm, possibly a CBD cultivar with intentional hemp introgression. To further distinguish: (1) check IBD segment analysis — admixture produces long haplotype blocks from the non-drug parent, while contamination produces short, random heterozygous stretches; (2) examine the cannabinoid chemotype — if TC_048 produces CBD, hemp introgression is expected; (3) re-extract and re-sequence to rule out contamination definitively.

**RUBRIC:**
Full marks (3): Correctly identifies genuine admixture as most likely, rules out mislabeling (would show clean single-population profile) and contamination (het rate is normal), interprets the three-way ADMIXTURE Q-values as supporting admixture, and proposes at least two appropriate follow-up tests (IBD segments, chemotype, re-sequencing). Mostly correct (2): Identifies admixture as most likely and rules out at least one alternative with correct reasoning, but proposes only one follow-up or misses the het rate argument against contamination. Partial (1): Identifies the anomalous positioning but does not systematically evaluate all three hypotheses, or incorrectly favors mislabeling or contamination. Incorrect (0): Concludes mislabeling or contamination without engaging with the ADMIXTURE or QC evidence. Major error: Claiming excess heterozygosity supports contamination when the het rate is within normal range.

**NOTES:** TC_048 is a constructed example to test differential diagnosis of PCA outliers. Coordinates are realistic for a genuine admixed sample in this dataset.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier3_pca_007
**Tier**: 3 | **Difficulty**: 2 | **Type**: comparison | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> Two PCA analyses were run on different subsets of the same cannabis panel. Analysis A (85 drug-type cultivars only) has PC1 explaining 53.1% of variance. Analysis B (all 706 samples including hemp, landraces, and feral) has PC1 explaining 25.5%. A researcher concludes that Analysis A provides 'better resolution' because PC1 captures more variance. Evaluate this conclusion.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
The conclusion is wrong. Higher variance on PC1 does not mean better resolution — it reflects lower genetic diversity in the sample set. In Analysis A, 85 drug-type cultivars share a narrow genetic background, so most variation falls along a single axis (likely inbreeding level or one major breeding lineage split). In Analysis B, the full panel includes genetically divergent groups (hemp, landraces, feral, drug-type) that differ along multiple independent axes, distributing variance more evenly across PCs. Analysis B actually provides MORE resolution for distinguishing populations — it just requires more PCs to capture the structure. The 'better resolution' question depends on the goal: Analysis A is better for fine-scale drug-type cultivar discrimination, while Analysis B is necessary for understanding the broader population context. Both are valid for different purposes.

**RUBRIC:**
Full marks (3): Correctly explains that concentrated PC1 variance reflects narrow diversity, not better resolution; distinguishes the two analyses by their appropriate use cases. Mostly correct (2): Identifies the conclusion as wrong but doesn't fully explain why. Partial (1): Discusses variance explained but accepts the researcher's framing. Incorrect (0): Agrees that higher PC1 variance means better analysis. Major error: Equating high PC1 variance with high data quality.

**NOTES:** Variance explained values are representative of real cannabis PCA analyses. This item tests a common misunderstanding about interpreting PCA variance explained across datasets of different genetic breadth.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

## Tier 4 -- Methods (8 items)

---
### tier4_method_001
**Tier**: 4 | **Difficulty**: 2 | **Type**: decision | **Scoring**: llm_judge | **Data**: rad_gbs

**PROMPT:**
> A population genetics study has 85 drug-type cannabis samples sequenced with RAD-seq at 8–15× average coverage and wants to compute a PCA for population structure analysis. A collaborator suggests using PLINK2's --pca command on hard-called genotypes. Evaluate this approach and state whether PCAngsd would be preferable, with justification.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
PCAngsd is preferable. PLINK2 --pca on hard-called genotypes will treat all genotype calls as equally certain, but at 8-15× coverage many heterozygous sites will have inflated error rates and the 28% missing data rate will force either imputation or exclusion, both introducing bias. PCAngsd uses the genotype likelihood (GL) or posterior probability (GP) distribution directly, properly weighting uncertain calls at low depth. For RAD-seq data specifically, where depth is highly variable across loci and samples, the likelihood-based approach of PCAngsd substantially improves PCA accuracy and avoids the missing data problem by treating uncertain genotypes probabilistically rather than excluding them.

**RUBRIC:**
Must recommend PCAngsd over PLINK2 hard calls. Must cite at least two of: genotype uncertainty at low depth, variable depth in RAD-seq, missing data treatment, or likelihood-based vs hard-call approach. Partial: recommends PCAngsd but only gives one reason. Zero: recommends PLINK2 or states both are equivalent.

**NOTES:** This is the core methodological choice in True Cultivar's pipeline.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier4_method_002
**Tier**: 4 | **Difficulty**: 3 | **Type**: decision | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> A lab has 200 new cannabis RAD-seq samples and wants to impute them using a WGS reference panel of 407 samples. They ask whether Beagle 5.4 or GLIMPSE2 is more appropriate for this use case, given the reference panel size and the RAD-seq data characteristics.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
GLIMPSE2 is generally preferable when depth is variable and some samples have limited site overlap. GLIMPSE2 uses genotype likelihoods directly from sequencing depth at each site, so it handles the 50-100K low-overlap samples better than Beagle, which treats all hard-called sites equally and can be misled by low-coverage miscalls. However, Beagle 5.4 is a defensible choice if the overlapping sites are pre-filtered to DP >= 5 and the low-overlap samples are excluded or treated separately. The key decision criterion is whether the lowest-quality samples can be cleaned to a reliable hard-call set; if not, GLIMPSE2's likelihood model is the safer choice.

**RUBRIC:**
Must identify the likelihood-vs-hard-call distinction as the core difference. Must recommend GLIMPSE2 for variable depth / low-overlap samples with valid justification. Should acknowledge Beagle is acceptable with strict pre-filtering. Major error: recommending Beagle unconditionally or stating both are equivalent without nuance.

**NOTES:** Directly relevant to the True Cultivar pipeline decision history.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier4_method_003
**Tier**: 4 | **Difficulty**: 2 | **Type**: decision | **Scoring**: llm_judge | **Data**: wgs

**PROMPT:**
> A collaborator shares a joint-called cannabis VCF and wants to compute nucleotide diversity (π) across the genome for two population groups. They plan to use all PASS-filter sites including those in repeat regions. Evaluate this plan and recommend any modifications.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
Including repeat and low-complexity regions will inflate π estimates and make comparisons unreliable, because these regions accumulate more variants due to alignment errors and repeat-driven variation rather than true population diversity. The plan should add a mask file (BED format) excluding RepeatMasker and low-complexity regions before computing π. Additionally, a minimum-depth filter (e.g. DP >= 5 per sample) and a maximum-missing filter (e.g. < 20% missing per site) should be applied. After masking, compute π on the retained ~50% of PASS sites. This is standard practice for plant genome diversity analyses where repeat content is high.

**RUBRIC:**
Must identify the repeat/low-complexity masking problem as the primary concern. Must recommend a BED mask exclusion. Should also mention depth/missing filters. Partial: mentions repeat masking but omits the depth/missing filters. Zero: approves the plan without modification or raises only irrelevant concerns.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier4_method_004
**Tier**: 4 | **Difficulty**: 2 | **Type**: decision | **Scoring**: llm_judge | **Data**: rad_gbs

**PROMPT:**
> A researcher building a RAD-aware reference panel for GLIMPSE2 imputation used the following command to create the RAD coverage footprint from BAM files:
> 
>   samtools depth -r NC_044370.1 sample.bam | awk '$3 > 0 {print $1"\t"$2-1"\t"$2}'
> 
> This produced 54 million single-base positions (1.6 GB BED file), and extracting WGS variants at these positions yielded 28 million variants. GLIMPSE2 failed with '#non-ref gls: 0'. Identify the error and propose the correct approach.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
The error is using per-base depth positions instead of merged RAD read intervals. The samtools depth command outputs individual base positions with coverage, creating 54M single-base entries that essentially represent the entire genome rather than the ~62K distinct restriction fragment intervals. This produces an unphaseable number of variants (28M) and GLIMPSE2 fails because the reference panel at these positions doesn't meaningfully overlap the sparse RAD-seq reads. The correct approach is to convert BAM reads to intervals (bedtools bamtobed), sort, and merge overlapping intervals with a gap tolerance (bedtools merge -d 100), then filter to intervals >= 50bp. This produces ~63K merged intervals covering ~45% of the chromosome, yielding ~2.4M extractable SNPs — a manageable count for phasing and imputation.

**RUBRIC:**
Full marks (3): Identifies the per-base vs merged-interval error, explains why 54M positions are wrong, provides the correct bedtools bamtobed + merge pipeline. Mostly correct (2): Identifies the problem but doesn't describe the correct solution in detail. Partial (1): Notes the BED file is too large but doesn't explain the root cause. Incorrect (0): Suggests the error is in GLIMPSE2 parameters or reference panel. Major error: Recommending to increase the GLIMPSE2 thread count or retry.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier4_method_005
**Tier**: 4 | **Difficulty**: 2 | **Type**: decision | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> A researcher plans to run both ADMIXTURE and PCA on a merged cannabis panel (706 samples, 14.9M biallelic SNPs). They propose using the same LD-pruned variant set for both analyses, with PLINK2 parameters: window=50, step=5, r²=0.2. This produces 2.1M independent variants. Is this parameter choice appropriate for both analyses, and should the same pruned set be used?

**CONTEXT:**
```
Panel: 706 samples (492 WGS reference + 85 RAD-seq imputed + 129 WGS imputed)
Starting variants: 14.9M biallelic SNPs (post-QC)
LD pruning result: 2.1M variants retained (14.1% of input)

PLINK2 parameters: --indep-pairwise 50 5 0.2
  window = 50 variants
  step   = 5 variants
  r²     = 0.2 (variants with r² > 0.2 pruned)
```

**CORRECT ANSWER:**
The r²=0.2 threshold is appropriate for ADMIXTURE, which requires approximately independent markers and is sensitive to LD-induced artifacts. However, PCA is more robust to LD and can benefit from a less stringent threshold (r²=0.5 or even unpruned for large datasets). Using the same pruned set for both is acceptable as a practical compromise — the 2.1M variants provide sufficient resolution for PCA while meeting ADMIXTURE's independence requirements. One caveat: for PCA, the 14.1% retention rate removes a lot of genomic signal, potentially reducing resolution for fine-scale structure discrimination. If the researcher needs maximum PCA resolution (e.g., distinguishing closely related cultivars), a separate PCA run on the full or lightly pruned set would be more informative.

**RUBRIC:**
Full marks (3): Distinguishes ADMIXTURE vs PCA sensitivity to LD, evaluates the r²=0.2 threshold for each, provides a nuanced recommendation (shared set acceptable with caveats). Mostly correct (2): Notes r²=0.2 is for ADMIXTURE, missing the PCA nuance. Partial (1): Discusses LD pruning generally without distinguishing the two analyses. Incorrect (0): Recommends no pruning for both, or much stricter pruning. Major error: Claiming PCA requires stricter pruning than ADMIXTURE.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier4_method_006
**Tier**: 4 | **Difficulty**: 3 | **Type**: decision | **Scoring**: llm_judge | **Data**: imputed

**PROMPT:**
> In a merged panel of 706 cannabis samples from three sources (WGS, RAD-seq imputed, WGS imputed), PCA reveals that PC3 separates samples primarily by data type rather than biological population. A researcher proposes mean-centering and variance-scaling each data-type panel independently before merging, then re-running PCA. Evaluate this correction strategy.

**CONTEXT:**
```
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

**CORRECT ANSWER:**
The correction is statistically aggressive and risks removing real biological signal. Mean-centering per panel is defensible if the batch effect is purely additive (e.g., systematic genotype probability inflation in imputed samples). However, variance-scaling per panel is dangerous: if the three panels differ in genuine genetic diversity (e.g., WGS includes diverse landraces while RAD-seq is only drug-type), scaling to unit variance will artificially equalize diversity that is biologically real. A better approach: (1) verify the batch effect by checking whether WGS and imputed samples from the same biological population cluster differently, (2) if confirmed, use only the batch-affected PC (PC3, PC4) as covariates in downstream analyses rather than correcting the genotype matrix, or (3) restrict cross-panel comparisons to shared biological populations where batch vs. biology can be disentangled.

**RUBRIC:**
Full marks (3): Identifies the risk of removing biological signal with variance-scaling, distinguishes mean-centering (defensible) from variance-scaling (dangerous), proposes covariate-based alternative. Mostly correct (2): Notes the risk but doesn't propose concrete alternatives. Partial (1): Approves the correction uncritically, or rejects it without explanation. Incorrect (0): Recommends even more aggressive normalization. Major error: Treating all PC variance from imputed vs WGS as purely technical.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier4_method_007
**Tier**: 4 | **Difficulty**: 3 | **Type**: decision | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> A researcher is merging three cannabis genotyping panels (492 WGS + 85 RAD-seq imputed + 129 WGS imputed = 706 samples) into a single dataset for population structure analysis. The merged VCF has 59M variants but substantial structural missingness: variants called in the WGS panel may be absent from imputed panels and vice versa. The researcher applies --geno 0.10 (remove variants missing in >10% of samples), which removes 25.9M variants. Is this threshold appropriate?

**CONTEXT:**
```
Pre-filter: 59,000,000 variants across 706 samples
Post --geno 0.10: 33,100,000 variants retained (56.1% retained)

Missingness structure:
  Variants in WGS panel only:           ~18M (absent from imputed panels)
  Variants in imputed panels only:      ~6M
  Variants shared across all 3 panels:  ~21M
  Variants shared between 2 panels:     ~14M

Panel sizes: WGS=492 (69.7%), RAD-seq=85 (12.0%), WGS_imputed=129 (18.3%)
```

**CORRECT ANSWER:**
The --geno 0.10 threshold is reasonable but imperfect. It effectively removes variants present in only one panel: variants exclusive to the WGS panel (18M) will have ~30% missingness (missing in the 214 imputed samples = 30.3% of 706), so they get removed. Variants shared across all panels (21M) are retained. The issue is that this is structural missingness (panel design), not quality missingness (random genotype failure). A more principled approach: (1) first identify the intersection of confidently-imputed sites across panels (using DR2 thresholds), (2) apply --geno only to filter quality missingness within that intersection, or (3) accept higher missingness for variants present in 2+ panels (e.g., --geno 0.30) and use downstream methods that handle missingness (PCAngsd, which uses genotype likelihoods). The 0.10 threshold's main risk is over-filtering: it may remove informative variants that are well-imputed in 2 of 3 panels but absent from the third.

**RUBRIC:**
Full marks (3): Distinguishes structural from quality missingness, evaluates the 0.10 threshold in context of panel sizes, proposes a more nuanced alternative. Mostly correct (2): Identifies structural missingness but doesn't quantify or propose alternatives. Partial (1): Evaluates the threshold without considering the multi-panel structure. Incorrect (0): Recommends stricter filtering (--geno 0.01). Major error: Treating all missingness as quality failures.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________

---
### tier4_method_008
**Tier**: 4 | **Difficulty**: 2 | **Type**: decision | **Scoring**: llm_judge | **Data**: derived

**PROMPT:**
> A researcher wants to run KING relatedness estimation on 85 imputed cannabis cultivars. They have two variant sets: (A) 17.5M LD-pruned variants from the pre-QC merged panel, and (B) 2.1M LD-pruned variants from the post-QC panel (after --geno 0.10, --maf 0.01, --hwe 1e-6 filters). Which variant set should be used for KING, and why?

**CONTEXT:**
```
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

**CORRECT ANSWER:**
Variant set B (post-QC, 2.1M) is strongly preferred. KING-robust is designed for population-level relatedness estimation and assumes reasonable genotype quality. Using pre-QC variants (set A) introduces several problems: (1) sites with high missingness create artificial kinship deflation for sample pairs where one has missing data, (2) rare variants (MAF < 0.01) are poorly imputed and contribute noise rather than signal to kinship estimates, (3) HWE-violating sites may reflect genotyping errors or imputation artifacts rather than real variation. The 2.1M post-QC variants still provide ample resolution — KING performs well with as few as 100K common SNPs. The quality of variants matters far more than quantity for kinship estimation.

**RUBRIC:**
Full marks (3): Recommends set B with 2+ specific reasons (missingness bias, rare variant noise, HWE artifacts), notes KING doesn't need millions of variants. Mostly correct (2): Picks set B but gives only one reason. Partial (1): Picks the right set but reasoning is vague ("cleaner data"). Incorrect (0): Recommends set A for "more information." Major error: Claiming more variants always improves kinship estimation.

**Review:** [ ] Approved  [ ] Needs revision  [ ] Cut
**Comments:** _______________
