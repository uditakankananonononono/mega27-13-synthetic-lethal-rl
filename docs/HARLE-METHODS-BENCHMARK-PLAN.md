# Separate retrospective pan-cancer methods benchmark

Frozen 2026-10-01 before full outcome extraction, after schema inspection exposed the first three Table S4 outcomes and four Table S5 rows. This is not a blinded discovery experiment. The author-selected library and published hit thresholds are known. Do not claim a novel gene pair from this benchmark.

## Scope and inputs
Harle et al. (2025), https://link.springer.com/article/10.1186/s13059-025-03737-w . Publisher workbook SHA-256: 297ed1ee52a753ea82b42fc46ffe196889a4a15e1725ae93b98a27eba1135aa9. Table S1 gives guide-pair design, S3 is labeled count matrix but contains non-integer values, S4 has per-line genetic-interaction outputs, and S5 contains the author binary hit matrix. Do not treat S3 as raw integer reads or use an integer-count likelihood without reconciliation.

The 27 screened models are lung, pancreas and melanoma. There is no HGSOC screen or matched nonmalignant perturbation viability. This benchmark is a separately labeled methodological pivot and cannot close the locked biological gate.

## Planned estimand
Retrospective measured-feedback retrieval of author-defined interaction hits, not direct viability prediction. Every algorithm gets the same measured-feedback query budget, the same eligible library and the same feature whitelist. Unique tested pairs count as queries; repeated queries spend budget and gain no new information. Report cumulative hits at budgets 10, 30 and 60, unique queries, and area under the cumulative retrieval curve. Keep published GI score as a secondary continuous endpoint, not a silently substituted primary reward.

## Leakage boundaries
Canonical unordered gene pairs are the unit. Hash split by SHA-256 of `harle-methods-v1|GENEA|GENEB`: first eight hex digits modulo five equal zero is development; all others are evaluation. All lines for a pair share its partition. Freeze this split before extracting labels. Development tuning never uses evaluation labels, including across cell lines. Evaluation is a simulated adaptive experiment: an evaluation label is exposed only when its pair is queried. Do not carry any evaluation pair outcome between lines or seed trials. The paper's early exposed row identities remain listed as exposure, not as untouched holdouts.

Primary features allowed: source-selection category from S1, gene expression and copy number from S4. S4's guide significance, residuals, FDR, single-gene depletion from this screen, BAGEL/MAGeCK screen scores and S5 hit totals are forbidden features. Outcome-derived normalization is also forbidden. Expression and copy number provenance needs audit before use. Gene identity embeddings require an explicit separate sensitivity arm; they cannot quietly transfer outcomes across evaluation pairs.

## Controls and proposed policy
Random without replacement, a fixed development-only feature ranker, adaptive ridge greedy with fixed exploration, and ridge uncertainty/UCB. Proposed sequential two-gene REINFORCE must choose only an eligible listed pair: choose a first gene, then a legal partner, update only after measured query feedback. If its structure collapses to a one-step contextual bandit, label it as such. No simulator viability reward or unmeasured normal-preservation reward is allowed.

20 fixed seed IDs (0 through 19), paired across methods. Primary comparisons against the strongest control, not random alone. Paired line-level aggregate differences with resampling across cell lines; seed replicates are not independent biological replicates. Report every control, negative outcomes and uncertainty. This does not by itself establish a win against a published world-leading model; such a model needs a faithfully executable, comparable implementation and separate provenance.

## Current status
Only ingestion/schema and split design are underway. No policy has run on this screen. No benchmark win, new discovery, validation or count-gate completion is claimed.

## First-pass restriction, before algorithm execution
Use only S1 design-selection category for the first run, because expression/copy-number provenance is unresolved. All algorithms may use all development-pair outcomes for the same line. No evaluation feedback crosses lines or seeds. Freeze greedy exploration probability 0.1, ridge penalty 1, UCB multiplier 1 and REINFORCE learning rate 0.05 without evaluation tuning. First-pass sequential policy uses design-category incidence for the first gene and pair categories for its partner. Its label remains a sequential pair-query policy, not a virtual-cell or mechanistic simulator. Published binary S5 hits are the primary endpoint; missing/invalid pair-line endpoints fail closed.

## Post-outcome correction arm, 2026-10-01
Keep original arms and seeds unchanged. Add `degree_corrected_pair_softmax`, using the exact two-stage weighted-incidence sampler tested in `pair_sampling.py`. Pair logits use category features and initial development category scores, with REINFORCE gradient x_chosen minus the expected pair feature and learning rate 0.05. This is algebraically a pair contextual bandit; the two-stage factorization is not evidence of an RL-specific advantage. Compare to all original controls, preserve original outcome, and label every corrected-arm result post-outcome development. No re-tuning or new biological finding.

Judge round is deferred on provenance caution. Packet is prepared, but no external submission or response exists and no completed judge round is counted.
