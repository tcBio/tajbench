# TajBench Gemini Eval — Progress Tracker

**Last updated**: 2026-03-19
**Responses file**: `baselines/responses_gemini_2_5_pro.json` (35 items saved)

---

## Status: 35/50 items complete (70%)

| Tier | Items | Done | Remaining | Status |
|------|-------|------|-----------|--------|
| 1 — Parsing | 1-10 | 10/10 | 0 | ✅ Complete |
| 2 — Statistics | 11-26 | 16/16 | 0 | ✅ Complete |
| 3 — Structure | 27-42 | 9/16 | 7 (items 36-42) | 🔄 In progress |
| 4 — Methods | 43-50 | 0/8 | 8 (items 43-50) | ⏳ Pending |

**15 items remaining** (items 36-50)

---

## How to Resume

### Method: Google AI Mode (free, no credits needed)
1. Go to `google.com` → click **AI Mode** tab
2. Click compose icon (📝) on left sidebar for new chat
3. Click input box → type condensed prompt → press Enter
4. Wait ~15s for response → screenshot to verify
5. Record response text in the JSON file

### Prompts location
All 50 prompts are in `baselines/gemini_eval_handoff.md`:
- **Item 36** starts at line ~995 (`tier3_pca_001`)
- **Item 43** starts at line ~1209 (`tier4_method_001`)

### Prompt format for AI Mode
Prepend system prompt inline:
```
You are an expert population geneticist. [condensed question + data]
```

### Items remaining (36-50):

| # | Item ID | Tier | Topic |
|---|---------|------|-------|
| 36 | tier3_pca_001 | 3 | PCA on 1080 samples, imputed vs WGS concerns |
| 37 | tier3_pca_002 | 3 | DR2>0.3 vs DR2>0.8 PCA comparison |
| 38 | tier3_pca_003 | 3 | Full panel vs TrueCut-only PCA variance |
| 39 | tier3_pca_004 | 3 | Identify imputed samples from PCA coordinates |
| 40 | tier3_pca_005 | 3 | Phenotypic variants second-degree kinship |
| 41 | tier3_pca_006 | 3 | TC_048 outlier — mislabel vs contamination vs admixture |
| 42 | tier3_pca_007 | 3 | Drug-only vs full panel PCA resolution |
| 43 | tier4_method_001 | 4 | PLINK PCA vs PCAngsd for RAD-seq |
| 44 | tier4_method_002 | 4 | Beagle 5.4 vs GLIMPSE2 for RAD-seq imputation |
| 45 | tier4_method_003 | 4 | Nucleotide diversity with repeat regions |
| 46 | tier4_method_004 | 4 | RAD coverage footprint BED file error |
| 47 | tier4_method_005 | 4 | LD pruning for ADMIXTURE + PCA |
| 48 | tier4_method_006 | 4 | Mean-centering correction for batch effects in PCA |
| 49 | tier4_method_007 | 4 | --geno 0.10 threshold for merged panel |
| 50 | tier4_method_008 | 4 | Pre-QC vs post-QC variants for KING |

---

## After all 50 items collected

1. Score with harness:
```bash
python -m harness.runner --model gemini-2.5-pro --input baselines/responses_gemini_2_5_pro.json
```

2. Save results to `baselines/results/gemini_2_5_pro.json`

3. Update leaderboard in `README.md`

---

## Notes
- Items 1-5 were run via **AI Studio** (Gemini 2.5 Pro with system prompt, thinking mode auto-enabled)
- Items 6-35 were run via **Google AI Mode** (free, system prompt prepended inline)
- AI Mode uses grounded search — responses may include web citations
- All responses are strong quality; Gemini handles the domain well
- Model version in AI Mode is not explicitly labeled but appears to be Gemini 2.5 Pro equivalent
