# PEO1 source reconciliation, 2026-10-01

The official GEO SOFT record now maps every one of the 14 CRISPR count-table sample labels to a GSM identity. No sample was relabeled based on its counts. The machine-readable evidence is `results/peo1-source-reconciliation.json`; regeneration uses `scripts/peo1_source_reconciliation.py` with the source SOFT gzip and EuropePMC article XML. Both inputs are SHA-256 hashed in the result.

GEO records A10_A/B/C as GSM3499358/59/60 and S10_A/B as GSM3499364/65. All these samples explicitly say they were transduced with GeCKO libraries A and B together. Sample replicate suffixes must not be interpreted as guide-library identities.

The article says duplicates of adherent day 10 versus suspension day 10 were selected using PCA and clustering. Three adherent day-10 columns exist. Neither the inspected article nor GEO metadata specifies which two were selected. Picking the most correlated pair now would be a new post-outcome selection rule, not reproduction of the authors' analysis.

There is a processing-description conflict: CRISPR GEO sample metadata names Hisat2, bedtools and edgeR with an RNA-expression description, while the article names DESeq2 for differential guide abundance. This could be generic submission metadata, but that explanation is unverified. Metadata is not evidence that the workbook is the authors' exact inferential input.

The primary supplementary methods PDF link returned challenge HTML instead of a PDF. A browser read recovered the real supplement links but a PDF fetch still returned challenge HTML. EuropePMC full-text XML worked; its supplementary ZIP did not complete in bounded requests. No supplementary figure has been inspected, and no selected replicate identities are claimed.

Decision: preserve the no-ranking/no-benchmark stop. Sample identity mapping is improved; replicate selection, normalization provenance and guide-level concordance remain unresolved. This monogenic anchorage-independence screen cannot establish pair/triple synthetic lethality, matched normal selectivity or a new discovery even if those QC issues are fixed.

## Sources inspected
- https://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123290/soft/GSE123290_family.soft.gz
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6710300/fullTextXML
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6710300/
- https://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123290/suppl/
- Supplement link observed on the article, but not retrieved as a valid PDF: https://pmc.ncbi.nlm.nih.gov/articles/instance/6710300/bin/mmc1.pdf
