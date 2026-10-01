# Descriptive late-window residuals, not synthetic-lethal hits

Sample-line binding per SLKB curation, not independently recovered from primary headers.

The separate October 1 freeze was committed before contrasts. This run uses curated D14-to-D28 counts, not the primary day7 baseline. It is conditional on constructs surviving to day14 and cannot reproduce cumulative screen results. Formula, baseline-only eligibility and pseudocount sensitivities are in `THOMPSON-D14-D28-DESCRIPTIVE-FREEZE.md`.

| Curated line | Eligible descriptive pairs | All three technical medians negative | Any technical sign changes with p=0.5 or p=5 |
|---|---:|---:|---:|
| A375 | 1,184 | 155 | 36 |
| MeWo | 1,184 | 416 | 13 |
| RPE1 | 1,184 | 739 | 94 |

Negative-sign counts are not hits, significance, mechanistic epistasis, selective-lethality candidates or discovery counts. A negative sign need not have a meaningful effect magnitude. RPE1 is retinal, not a matched healthy tubal model. No ranking for intervention is produced; all pair rows are in canonical alphabetical order. Technical replicates are not independent biological replication.

All 498 double-negative controls pass baseline>=20 in all three replicates. Their LFC median shifts with p=1 are approximately [0.213, 0.470, 0.224] for A375, [0.200, 0.018, 0.049] for MeWo and [-1.119, -1.289, -0.898] for RPE1. Centering is fixed per line and replicate, but it does not make cross-line residuals validated normal-preservation measurements. Exact single controls use FLUC_GRNA_1 and differ in promoter context from double targeting, a remaining source/design confound.

Each line excludes 74 double constructs with missing exact singles. Additional baseline-count exclusions are 1,001 A375, 780 MeWo and 1,082 RPE1 double constructs. Two otherwise represented pairs per line have fewer than four eligible constructs and are excluded from pair summaries. Eligibility never uses D28 outcomes.

The full output carries the curated-binding label, archive and mapping checksums. A second run reproduced it byte-for-byte. Formula/control regression tests pass; the full engineering suite has 69 tests. These tests validate implementation, not biology.

Primary study: https://www.nature.com/articles/s41467-021-21478-9 . Curated count archive: https://ndownloader.figshare.com/files/41055392 . Verified primary guide workbook: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-021-21478-9/MediaObjects/41467_2021_21478_MOESM7_ESM.xlsx . No raw EGA access was pursued. All original HGSOC, matched normal viability, new discovery and external benchmark-win gates stay unmet.
