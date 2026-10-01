# Separate D14-to-D28 follow-on depletion estimand: preregistration draft

2026-10-01. This draft is not the locked original preregistration and does not inherit its HGSOC or healthy-preservation gates. No outcome contrast has been computed for this proposed estimand. The curated archive was inspected for identities, count-vector validity and time labels only. Published original result tables and benchmark outputs have already been inspected, so this is not a blind prospective discovery.

## Different question and baseline
Question: which assayed dual-guide constructs show greater additional depletion between day 14 and day 28 than expected from their matched single-guide controls in A375, MeWo and RPE1?

Baseline is the same line's day-14 counts, not the primary Cas9-negative A375 day-7 library. It measures late-window persistence or emergence of fitness interactions conditional on survival through day 14, not cumulative knockout effect from baseline. Early lethal constructs can already be depleted by day 14, creating floor/selection effects. A pair negative under this window cannot be called a new cumulative screen hit or a validation of day-7 replication.

Primary day-7 route EGAD00001006648 is behind EGA DAC access. No access request, account action or acquisition from that route will be pursued. Source: https://ega-archive.org/datasets/EGAD00001006648 . This closes the raw-baseline recovery route for this assignment, not the biological question itself.

## Source and units
Curated SLKB study 33637726, archive SHA-256 05ece8a60b58916fcfb576be1b5a824773b42471f21e2c6b141b81de7da72576. Each line has 41,838 guide-pair rows and three day14/day28 columns. Primary paper calls these technical replicates. They are not three independent biological models. Verify sample-name-to-line bindings and guide construct uniqueness before proceeding. No row may be duplicated to imitate another orientation.

A_B/B_A metadata is canonical gene-label ordering until physical guide/promoter mapping is independently verified against the primary library. Do not pool it as bidirectional experimental evidence or claim orientation robustness from these labels alone.

## Eligibility and next freeze
Before any effect calculation:
1. Verify every count record's two guide IDs and target symbols against the primary 41,838-design workbook, including guide sequences and target-control labels.
2. Resolve BA/BB/BD sample prefixes to primary sample identities for each line. A database line label alone cannot fix a contradictory sample header.
3. Identify non-targeting/control constructs, their early counts and each gene-targeting guide's exact single-control partner. No nearest-gene or first-matching-guide substitution.
4. List missing matched singles, duplicated constructions, ambiguous guide targets and baseline-zero constructs. Freeze exclusions from baseline/design only, not based on negative contrasts.
5. Freeze normalization from validated negative controls, pseudocount policy, eligibility thresholds, per-guide interaction formula and gene aggregation before contrasts. The primary analysis will not borrow the authors' processed score thresholds without a new calibration argument.

Proposed conservative starting formula, not yet finalized: use negative-control-centered log2((D28+p)/(D14+p)) per replicate; for an eligible double guide with exact matched single guide constructs, calculate residual double LFC minus the sum of corresponding single LFCs. Preserve shared-control dependence. An unmatched residual is not estimated. Baseline and pseudocount sensitivity must be prespecified after baseline-only QC, not chosen for positive hits.

No p-value or confidence interval treating technical guide constructs as independent biological replicates will be used to claim biological discovery. Ranking may be descriptive with replicate/guide concordance only; inferential calibration requires explicit controls and source design support. RPE1 is a non-transformed retinal comparator, not healthy fallopian-tube epithelium, so no HGSOC-selective claim follows.

## Frozen restrictions
- No use of original author outcomes to set exclusions or ranking rules.
- Exclude or separately flag 212 pair identities already exposed in Harle when later discussing independent validation.
- No adaptive policy or leading-model benchmark until matched count/control inputs and equal-information endpoint are verified.
- No novel gene-pair claim from rediscovering published data without independent source-specific novelty checks and validation.
- Report the day14-conditioned estimand separately from day7 replication, original HGSOC discovery and the negative Harle active-query benchmark.

## Current decision
Draft only. Complete design/control mapping before finalizing effect and calibration details. No fit, ranking, D14-to-D28 interaction calculation or policy run has been launched.
