# Category-only measured-feedback benchmark: negative against random

2026-10-01. This is a separate retrospective pan-cancer methods pivot, not the locked HGSOC selective-lethality project. See the frozen protocol and its explicit preliminary row exposure in `HARLE-METHODS-BENCHMARK-PLAN.md`. No novel interaction is claimed.

The publisher supplementary workbook supplies 472 measured author-screened pairs across 27 lung/pancreas/melanoma lines. The frozen hash split assigns 87 development pairs and 385 evaluation pairs, consistently across lines. Design categories are the only policy features. Development endpoints are available equally to all nonrandom algorithms for each line. Query feedback is revealed one pair at a time, without replacement, with reset between lines and seeds. The sequential policy chooses a first gene and then an eligible partner and updates after measured binary hit feedback. No simulated viability or normal-state reward enters this test.

Twenty seed IDs per line, five methods and 60 unique queries per method give 2,700 trial traces. These traces reuse the same biological screen; they are not 2,700 independent experiments or datasets. All query identities and feedback are saved. Table S4's published hit indicator and S5's binary matrix agree across all 12,744 pair-line endpoints. There are no duplicate pair-line keys. `harle-benchmark-integrity.json` records these checks. The first-query regression test checks that unseen evaluation labels do not alter the first query. These checks do not establish a perfect absence of every implementation defect.

| Method | Mean hits at 60 | Mean cumulative-hit curve |
|---|---:|---:|
| Random without replacement | 4.6593 | 2.3079 |
| Sequential REINFORCE | 4.3463 | 2.3069 |
| Ridge greedy, 0.1 exploration | 4.3259 | 2.1573 |
| Fixed development category rank | 2.7167 | 1.4053 |
| Ridge UCB | 2.3056 | 0.9127 |

Sequential REINFORCE minus random is -0.3130 hits at 60, with a paired line-resampling percentile 95% interval [-0.5204, -0.1056]. RL retrieves fewer hits in 20 of 27 line averages. RL minus ridge greedy is +0.0204, interval [-0.6611, +0.6778], not an established difference. Beating weak fixed-category or UCB controls does not satisfy a benchmark-win gate when random performs better. The interval treats cell lines as resampling units; shared pair library and lineage dependence limit its interpretation. Seeds quantify algorithm randomness, not biological replication.

## Interpretation and limitations
The category-only first-pass RL policy does not improve measured interaction retrieval over the strongest control. Category incidence can introduce gene-degree sampling effects. Category probabilities estimated from only 87 development pairs can be unstable; the fixed category score also need not match class enrichment in evaluation pairs. Do not attribute failure to either mechanism without a separate analysis.

The benchmark endpoints are the authors' processed hit calls, not directly measured cellular viability. Pair partitions share genes. The library was selected using prior paralog/dependency evidence, so it is not a genome-wide unbiased sample. S3 has fractional counts, and its processing provenance is unresolved. This run does not faithfully reproduce or defeat a published leading external predictor. It establishes a bounded negative measured-feedback comparison, not a biological discovery.

Source article: https://link.springer.com/article/10.1186/s13059-025-03737-w

Publisher workbook: https://media.springernature.com/original/springer-static/esm/art%3A10.1186%2Fs13059-025-03737-w/MediaObjects/13059_2025_3737_MOESM1_ESM.xlsx

Workbook SHA-256: 297ed1ee52a753ea82b42fc46ffe196889a4a15e1725ae93b98a27eba1135aa9. The repository stores scripts and derived audit/traces, not the workbook. No HGSOC, matched-normal, discovery, judge-round, dataset-count, tool-count or paper gate is closed by this result.
