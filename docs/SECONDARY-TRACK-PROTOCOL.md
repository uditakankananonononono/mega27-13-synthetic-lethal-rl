# Secondary track: single-gene dependency biomarker hypotheses (FROZEN before any calculation)
Status: SEPARATE from docs/PREREGISTRATION.md. The locked HGSOC gate is untouched and remains data-blocked. Nothing here can satisfy any completion gate. Outputs are hypotheses only.

## Question
Among DNA-repair genes (GO:0006281, 548-gene SPIDR universe), which have CRISPR dependency that tracks loss/alteration of a second repair gene in ovarian-lineage lines?

## Data (independent of Harle, Thompson/SLKB, SPIDR, CombiGEM)
- DepMap public CRISPR gene effect (Chronos) and mutation/copy-number tables, one pinned release, accession and sha256 recorded at download.
- Project Score (Sanger) CRISPR scores as a separate cohort when retrievable.
- Lines: ovarian lineage (HGSOC-annotated where DepMap annotation allows) as the test set; all other lineages as comparison. Nonmalignant lines are not available in DepMap; no matched-normal claim is made.

## Method
1. Biomarker genes: BRCA1, BRCA2, CCNE1 (amplification), RB1, TP53 status, plus any other repair gene with >=5 altered ovarian lines.
2. Per (biomarker, target repair gene): difference in mean gene effect between altered and unaltered lines, within ovarian lineage; Mann-Whitney test; BH correction across all tested pairs.
3. Hit threshold: BH q < 0.1 and effect difference <= -0.3 in DepMap, with same sign in Project Score where the lines overlap. Common-essential targets (dependency <= -0.5 in >= 90% of lines) are flagged and excluded as non-selective.
4. No tuning on outcomes. Thresholds above are fixed now.
5. Report all tested pairs, not only hits.

## Limits
Observational, small altered-line counts, lineage and confounding by shared ancestry of lines. Any hit is a hypothesis needing independent experimental validation; it is not a discovery.
