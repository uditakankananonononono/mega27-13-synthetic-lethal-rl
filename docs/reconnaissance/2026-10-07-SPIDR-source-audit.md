# SPIDR: real repair interaction data, different biological scope

Primary published source: https://www.nature.com/articles/s41586-025-08815-4 . Full-text record also retrieved at https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12018271/fullTextXML .

Three numeric/design artifacts have been retrieved, hashes and observed source URLs in `results/spidr-source-audit.json`. The ZIP called Supplementary Table 2 contains guide-library design, not count data: 697,233 construct rows plus two headers, with two sets of twelve guide metadata fields. Supplementary Table 3 is a three-column scored gene-pair CSV. Supplementary Table 4 has exactly 1,165 distinct selected pair strings and complete RPE1, K562 and HeLa GEMINI score cells. Cell counts and source hashes are provenance, not independent dataset counts.

The full screen is hTERT RPE-1 TP53-KO dCas9-KRAB, not HGSOC. The follow-up targets the strongest 1,165 RPE1 pairs in K562 and HeLa S3. It cannot estimate unbiased all-pair transport, and cannot establish normal tubal preservation. RPE1 TP53-KO is not a healthy matched fallopian comparator. These data do not close the locked biological gate.

Replicate wording differs: 2023 preprint calls two technical duplicates; 2025 paper calls biological duplicates. The published methods describe a shared transduction/selection followed by expansion and division into two replicates. Independent transduction origin is not established by either label. Preserve that uncertainty instead of counting two independent biological origins.

Primary sequencing deposition: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA988447 . Live ENA run metadata returned four paired-end runs with generic sample titles. The eight FASTQ files total tens of gigabytes; raw downloading is not justified for this initial source audit. GSE236062 is ChIP-seq, not the screen count table. A direct processed-count artifact has not yet been recovered.

Exposure: primary headline pairs, top scored rows and article aggregate replication statistics are already seen. They cannot provide blind nomination/novelty credit. No fitting or hit-list selection has been done. The targeted numeric matrix is a possible separately frozen descriptive/methodological input only, conditional on selection and without HGSOC claims.

## Processed-count recovery
A bounded curl retry succeeded for Supplementary Table 8. It is the RPE1 source-normalized count matrix with day0 and day14 replicate1/2 columns. Exact bytes/hash and schema QC are in the source manifest. No re-normalization, contrast fitting or significance analysis was done. Decimal normalized counts must not be treated as raw Poisson sequencing counts. The independent-transduction ambiguity remains. Recovery replaces the earlier retrieval blocker, not the HGSOC/matched-normal scope blocker.
