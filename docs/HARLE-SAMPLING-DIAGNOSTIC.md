# Category-shift and pair-base-measure diagnostic

Post-outcome audit, 2026-10-01. This is a mathematical/methodological result, not a biological discovery. The original measured-feedback negative is preserved.

In the fixed pair partition, development Achilles/MASHUP hits are 45/513 pair-line endpoints (8.77%), versus 54/2592 (2.08%) in evaluation. Paralog hits are 74/1404 (5.27%) in development versus 671/5670 (11.83%) in evaluation. This shows category calibration shift for this partition; no causal explanation or universally stable enrichment is established. These reused pair-line outcomes are dependent observations, not independent clinical samples.

At zero policy weights, choosing a first gene uniformly and then an incident partner uniformly gives pair probability P({u,v}) = [1/deg(u)+1/deg(v)]/number_of_genes. In this evaluation library, highest/lowest pair base probability is 3.4286. It is not uniform random pair sampling.

`src/slrl/pair_sampling.py` now implements an exact two-stage base measure. Let edge weight w_e = exp(score_e). Choose gene g with mass proportional to the sum of weights over its incident edges, then choose an incident edge with probability proportional to w_e. Summing both orientations gives P(e) = w_e / sum_edges w_e, exactly the pair softmax. Zero scores produce uniform pair probabilities on an irregular graph. The four regression tests check irregular-graph uniformity, nonzero softmax identity, duplicate-orientation rejection and legal sampling.

This correction is mathematically equivalent to direct pair softmax. Do not present it as a completely new algorithm or as evidence that sequential RL adds value. It corrects a choice-of-base-measure defect and supplies a transparent control. It has not yet been integrated into a new benchmark run. A rerun after this diagnostic is post-outcome development; an independent untouched screen is still needed to validate its value.

Source screen: https://link.springer.com/article/10.1186/s13059-025-03737-w . Input workbook hash and query traces are recorded in the ingestion and benchmark artifacts. Generated diagnostic: `results/harle-category-diagnostic.json`.
