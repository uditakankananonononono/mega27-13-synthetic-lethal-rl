# CombiGEM 2016 lead fails independence, 2026-10-07

Lead: Wong et al. 2016, "Multiplexed barcoded CRISPR-Cas9 screening enabled by CombiGEM", PNAS 113(9):2544-2549, https://www.pnas.org/doi/abs/10.1073/pnas.1517883113 . Data at GEO GSE71074 per the article's data-deposition statement.

Finding: this is NOT an independent validation source for the exposed GSE154112 analysis. GSE154112 is Zhou et al. 2020, "A Three-Way Combinatorial CRISPR Screen for Analyzing Interactions among Druggable Targets" (PubMed 32783942), with Alan S.L. Wong as corresponding author - the same laboratory lineage as the 2016 CombiGEM paper. Both screens use the same cell line, OVCAR8-ADR, and the same barcoded combinatorial library technology family. The locked preregistration splits data by cell line and by source laboratory, so GSE71074 fails independence on both axes before any outcome inspection.

Scope failures against the original gate, independent of the independence failure:
- 23,409 dual-gRNA combinations over 50 epigenetic-regulator genes, not the locked DNA-repair module.
- Single line (OVCAR8-ADR); no HGSOC multi-model evidence, no matched nonmalignant comparator.
- Pairwise only; no seven-subset triple measurements.
- Growth-depletion window day 15 to 20; not direct viability against a normal reference.
- Published hits (KDM4C/BRD4, KDM6B/BRD4) are known source results; no novelty credit possible.

No data from GSE71074 was downloaded or inspected beyond the article's public abstract/methods statements. It remains usable only as methodological context for barcoded combinatorial library design, clearly labeled as same-lab/same-line relative to exposed data. All original gates stay UNMET.

Sources: https://www.pnas.org/doi/abs/10.1073/pnas.1517883113 (GSE71074 deposition); https://pubmed.ncbi.nlm.nih.gov/32783942/ (GSE154112 authorship); https://www.omicsdi.org/dataset/geo/GSE154112 .
