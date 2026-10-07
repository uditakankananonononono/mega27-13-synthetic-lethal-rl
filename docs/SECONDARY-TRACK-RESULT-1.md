# Secondary track result 1 (Project Score only; hypothesis track; locked gate untouched)
Protocol sha256 f3b3648028c6be8658bfdf7be645c80e58d70f147a5e09fb6e51f5eae898f23e; deviation 1 sha256 6ca9fa1ba7c8c41903d67096c279d50318ca56b7447992b8744b97a63fa9b58d. Single cohort: no DepMap, no cross-cohort sign check.
Result: zero hits under the frozen thresholds (BH q<0.1 and median diff <= -0.3, common-essential excluded).
- Ovary set: 31 models. Altered/unaltered: BRCA1 3/28, BRCA2 3/28, RB1 2/29 (not tested, <3), TP53 18/13, CCNE1 6/25. 71,980 pairs tested.
- HGSOC-annotated sensitivity: 10 models. BRCA1/BRCA2/RB1 1/9 (not tested), TP53 7/3, CCNE1 4/6. 35,990 pairs tested.
All tested pairs: results/secondary-track-projectscore-all-pairs.tsv.gz. Script: scripts/secondary_track_projectscore.py.
Interpretation: a null with very low power (3 altered lines for BRCA1/2). It supports no biological claim and moves no gate. Licence note: Sanger licence grants internal research and educational use; only derived statistics are committed, not raw files.

## Power (simulation, results/secondary-track-power.json)
Assumes a true -0.3 median shift, 25 unaltered lines, p<1e-4 as a stand-in for BH q<0.1 over ~72k pairs. Power is 0.0 at 3 altered lines and at most 0.13 at 20 (SD 0.3); with SD 0.5 it is under 0.01 even at 20. With 3 altered vs 25, the smallest possible Mann-Whitney p is about 6e-4, so the test cannot pass at this multiplicity. The null in this track says nothing about BRCA1/2-linked dependencies.

## Status: capped by data (2026-10-07)
The secondary track stops here. This is a data limitation, not a biological finding. Reasons: DepMap terms were not accepted (indemnity, jurisdiction consent, AI-training carve-out); Project Score has 3 to 6 altered ovarian lines for BRCA1/2 and CCNE1, which cannot pass the frozen multiplicity; no second public ovarian dependency cohort with deposited counts was found (Cell Death Dis 2022 is a 33-gene assay in 6 lines with no accession; the Cell Oncol 2025 review lists none). Reopening needs a user decision on DepMap terms or a verified public cohort.
