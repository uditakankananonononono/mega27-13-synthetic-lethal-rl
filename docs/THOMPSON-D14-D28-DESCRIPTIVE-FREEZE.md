# Curated-only descriptive late-window analysis freeze

Frozen October 1, 2026 before any D14-to-D28 contrast calculation. Parent chose curated-only provenance for this internal descriptive analysis.

Mandatory output label: "sample-line binding per SLKB curation, not independently recovered from primary headers". This is not independent validation. BA=A375, BB=MEWO, BD=RPE1 only under that curated binding. No original HGSOC or healthy-selectivity gate is borrowed.

## Formula and exclusions
For each line and technical replicate index, guide-construct LFC = log2((D28+1)/(D14+1)). Center using the median LFC of the 498 double-negative control constructs with D14>=20 in all three technical replicates. No library-size normalization or essentiality inference is substituted. Reject a line if fewer than 50 such control constructs are eligible.

A double guide is eligible only if its own D14 counts and the exact FLUC single-guide controls for both constituent guides are >=20 in all three replicates. Both exact singles must exist uniquely; exclude the 74 unmapped dual constructs per line. No observed late-time outcome enters eligibility. Residual for each replicate = centered double LFC minus centered singleA LFC minus centered singleB LFC. Gene-pair summary is the median over guide constructs for each replicate. Require at least four eligible double constructs per gene pair. Report number of guide constructs, residuals per technical replicate, median residual and whether all three technical-replicate medians are negative. This sign is descriptive, not a hit call.

Count-floor sensitivities: retain the same primary eligible rows and recompute with pseudocount 0.5 and 5, not reselect on outcomes. Report whether signs change. No p-values, BH, guide-bootstrap significance or biological confidence intervals. Technical replicate indices align only under curated sample naming, not recovered biological pairing.

## Caveats and comparisons
Physical dual order matches the primary library, but singles are always in one promoter configuration. Exact guide identity does not make single-versus-double promoter context identical. Residuals are thus descriptive deviations with this design confound, not calibrated epistasis.

Same-screen RPE1 comparisons may be tabulated only as retinal non-transformed context, never healthy fallopian-tube selectivity. Published prior hits and 212 Harle-exposed pairs remain exposure flags, not new discoveries. No candidate recommendation, ranking for intervention, RL run, or external leading-model claim follows. Any follow-up hypothesis needs independent evidence and novelty review.

All output files carry the curated-binding label and descriptive-only scope. Retain every eligible pair in canonical order rather than promoting negative-ranked pairs. Record source/archive and design checksums and exclusions. Stop if control identity, counts, sequence mapping or dimensions disagree with the verified audit.
