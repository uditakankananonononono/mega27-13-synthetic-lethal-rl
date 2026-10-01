# Independent screen and baseline source audit, 2026-10-01

## Thompson 2021: measured non-transformed comparator, different disease

Primary source inspected: https://www.nature.com/articles/s41467-021-21478-9 . It screens 1,191 pairs in A375 and MeWo melanoma lines and near-diploid non-transformed RPE-1, explicitly described as a normal comparator. Day 14 and 28 guide depletion is measured; this is not a matched fallopian-tube normal model or direct HGSOC DNA-repair viability. Eight selected pairs were validated by competitive growth assays in the original publication. Those known hits are not new discoveries.

The common early-time control is a Cas9-negative A375 line sampled at day 7, not an unperturbed matched control for every line. The guide orientation is asymmetric. This affects baseline compatibility. A proposed fair screen-scoring comparison requires guide/library provenance, orientation/control reconciliation and an orthogonal endpoint. A predictor that reads every late-time outcome cannot be compared as if it were an active-query policy with 60 labels.

## Executable strong baseline evidence

The primary 2025 GI-scoring benchmark at https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12464814/fullTextXML compares five methods on five studies. No score wins all screens. Gemini-Sensitive is a reasonable general first choice, but Parrish score performs best on asymmetric Thompson/Parrish screens under several endpoints. The benchmarking adaptations include control substitutions and duplicated orientations for Orthrus; these do not create independent replicates. Code: https://github.com/cancergenetics/Benchmarking-GI-Scores . Published output dataset inspected through https://api.figshare.com/v2/articles/27868350 , whose metadata reports CC BY 4.0.

Four Thompson score files were downloaded, independently hashed and schema checked. All have 1,191 unique pairs. The two files named `Gemini_Thompson_Sensitive.csv` are distinct provider IDs 52694606 and 52694642, with different hashes. One is complete; the other has 1,665 missing score cells. This likely corresponds to filtering variants, but that inference is not yet source-reconciled. Do not choose one by score quality or silently merge them. Day14/day28 column order differs across score methods and must be aligned by names, not position. `results/thompson-baseline-source-audit.json` records the IDs, hashes, columns, missingness and overlap with the already-exposed Harle pair set.

No Thompson model fit, ranking, win or discovery has run. Pair overlap means a later Thompson validation must explicitly exclude exposed Harle pairs or separately report overlap; study independence is not pair independence. The published scored tables are candidate baseline artifacts, not a fresh untouched blind holdout.

## Ovarian organoid lead does not supply the missing lethal assay

Primary paper: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12248148/fullTextXML . It uses Trp53-deficient mouse tubal organoids with combinatorial mutation of 20 candidate HGSC drivers and measures transformation, histology and drug response. The live official GSE298617 SOFT record at https://ftp.ncbi.nlm.nih.gov/geo/series/GSE298nnn/GSE298617/soft/GSE298617_family.soft.gz identifies the deposited assay as RNA-seq of mesenchymal/papillary tumors, 13 sample records, not guide-pair fitness counts. Neither the accession nor tumor RNA-seq supplies the locked selective-lethality validation. Mechanistic context might be useful later, but mutation constellations and transcriptomic association do not identify a therapeutic synthetic-lethal pair.

## Next bounded work
Recover Thompson primary guide-count/design download links and exact filtered/unfiltered score-file identities. Define an endpoint and equal-information comparison before a run. Keep the original HGSOC and matched-normal gates unmet until an eligible assay exists. Metadata records, model/timepoint columns, algorithm score variants and repeated trials must not be counted as independent datasets or external tool executions.

## Variant reconciliation update
The benchmark repository's `Gemini_on_Thompson.R` explicitly writes an unfiltered `gemini_score(..., pc_threshold=-Inf)` output and a filtered `gemini_score(..., pc_gene=essentials)` output to same-named files in different directories. Provider metadata states filtered/unfiltered variants are included. Direct comparison shows all 5,481 retained cells in ID 52694642 equal ID 52694606 exactly, with 1,665 missing cells and identical 1,191 pair identities. Thus the files exhibit the documented full-versus-masked variant pattern; provider IDs do not encode the directory, so this is a content/source-code reconciliation, not a recovered directory assertion. No imputation or mixing is performed.

The Thompson analysis notebook flips the signs of zdLFC, Orthrus and Parrish outputs for larger-is-more-SL ranking, but does not flip Gemini outputs. This is critical: raw-score numerical comparisons or rank direction cannot be copied between methods without this source-grounded alignment. The source notebook is `Analysis/Thompson-Analysis.ipynb` in https://github.com/cancergenetics/Benchmarking-GI-Scores . This audit has not executed those scoring algorithms on raw counts.

The primary guide-library workbook (Supplementary Data 4) was retrieved, SHA-256 0a41dfda583b3b6fb9e955fa1387e47868d6fe5250e276ae05c3645e10512ad9. It has 41,838 design rows after four header rows and includes guide IDs/sequences and pair origin. Raw read counts remain unrecovered. Do not transform design rows into biological replicates.
