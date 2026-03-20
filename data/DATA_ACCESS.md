# TajBench Dataset Access

## Primary Data Source

TajBench is built on the **3,000 Rice Genomes Project** (3K RGP), a fully public dataset.

- **Reference**: Wang et al. (2018) *Nature* 557, 43-49
- **SRA accession**: PRJEB6180
- **AWS S3**: `s3://3kricegenome/` (no sign-in required)
- **Registry**: https://registry.opendata.aws/3kricegenome/

## Public Derived Artifacts

The following derived artifacts are freely available in `data/derived/`:

| Artifact | Description | Location |
|----------|-------------|----------|
| PCA coordinates | PC1-PC10 eigenvectors for 3,010 accessions (anonymised sample IDs) | `data/derived/pca_coordinates/` |
| VCF snippets | Curated 20-record VCF excerpts for benchmark Tier 1 items | `data/derived/vcf_snippets/` |
| Site frequency spectra | Folded SFS per subpopulation (indica, japonica, aus, aromatic) | `data/derived/sfs/` |
| FST matrices | Pairwise Weir-Cockerham FST between the five major subpopulations | `data/derived/fst/` |
| Imputation QC | DR2 distributions per chromosome and by MAF bin | `data/derived/imputation_qc/` |

These files contain no raw reads and use anonymised sample IDs.

## Full Dataset Access

The 3K RGP data is **fully public** and can be accessed directly:

```bash
# List available files on AWS S3
aws s3 ls --no-sign-request s3://3kricegenome/

# Download SNP data
aws s3 cp --no-sign-required s3://3kricegenome/snp/ ./snp/ --recursive
```

Raw sequence data is also available from the European Nucleotide Archive (ENA) under accession PRJEB6180.

## Reference Genome

- **Assembly**: IRGSP-1.0 (Os-Nipponbare-Reference)
- **Size**: ~390 Mb, 12 chromosomes
- **Source**: https://rapdb.dna.affrc.go.jp/
