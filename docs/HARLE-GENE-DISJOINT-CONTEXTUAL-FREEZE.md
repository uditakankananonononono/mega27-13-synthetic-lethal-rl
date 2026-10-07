# Gene-disjoint contextual-representation experiment (FROZEN before any run)
Date: 2026-10-08. Origin: the single R01 ChatGPT judge round (docs/judge/R01-response-verbatim-2026-10-08.txt) proposed testing whether the category-only bottleneck, not the RL algorithm, explains the Harle benchmark loss to random. The judge's text is advice; this document is our own frozen design. It does NOT touch the locked HGSOC gate and is a separately labelled methods experiment. Target gate effect: none. Any result is a methods result on a lung/pancreas/melanoma benchmark, not HGSOC, not matched-normal, not discovery.

## Disclosure (not blind)
The pair-disjoint benchmark on the same workbook was already run (results/harle-corrected-development.json), so aggregate random/RL/greedy hit rates for the older split are known to us. The gene-disjoint evaluation pairs are a subset of the pairs in that benchmark. Before this freeze I read only design information: the Table S1 pair list (473 canonical gene pairs, 845 genes) and whether genes are present in the Project Score matrix. No Table S5 outcome was read for this experiment. The plan is frozen before this partition's outcomes are scored, not before the earlier aggregate results.

## Inputs
1. Harle et al. 2025 workbook, SHA-256 297ed1ee52a753ea82b42fc46ffe196889a4a15e1725ae93b98a27eba1135aa9 (Table S1 design, Table S5 binary hits, 27 lines).
2. Sanger Project Score 2019 essentiality matrices, SHA-256 52bc7a58e39cbe8b973a82868057431f4b645c325d4994d20f11531a875c9d46, file 03_scaledBayesianFactors.tsv (17,995 genes x 325 lines). Single-gene dependency only. Contains no pair outcomes and predates Harle by six years.

## Gene representation and why evaluation outcomes cannot reach it
z_g = row of scaled Bayesian factors for gene g across Project Score columns, EXCLUDING every column whose model name matches one of the 27 Harle screened lines (name match: uppercase, alphanumerics only). Standardize each retained column across all genes (mean 0, sd 1, NaN to 0). Representation u_g = first 8 principal components of the standardized all-gene matrix (SVD, fit on all 17,995 genes, no Harle information used in fitting). Guarantees: (a) the only input to u_g is the Project Score file above; (b) Harle Table S3/S4/S5 columns, labels and guide data are never read when building u_g; (c) the 27 Harle lines' own Project Score columns are removed, so the representation is not computed from the lines being evaluated; (d) u_g is computed and its hash recorded before the script opens Table S5; (e) the run script exposes an evaluation label to a trial only when its pair is queried (as in the existing benchmark). Residual risk, stated not removed: Harle selected library pairs using dependency and expression information (categories CRISPR/RNA-Seq, Achilles/MASHUP), so u_g may correlate with how pairs were chosen even though it holds no outcome label.

## Gene-disjoint split (frozen)
Gene partition: SHA-256 of "harle-genedisjoint-v1|GENE", first 8 hex digits mod 2: 0 = development genes, 1 = evaluation genes. A pair is development if both genes are development genes, evaluation if both are evaluation genes; mixed pairs are discarded. Pairs with a gene absent from Project Score are dropped from every arm (identical pool for all arms). Design-only counts before freeze: 111 development and 108 evaluation pairs, 254 mixed; with Project Score coverage 103 development and 102 evaluation pairs. Because the evaluation pool is only 102 pairs, a budget of 60 queries is more than half the pool; random's expected H60 is therefore high relative to the ceiling. Reported, not corrected.

## Arms (same seeds 0-19, same 27 lines, same budget, same development outcomes per line)
1. random without replacement.
2. category_greedy: existing ridge-greedy on the exclusive design-category one-hot (ridge penalty 1, exploration 0.1).
3. contextual_greedy (the proposed method): linear ridge (penalty 1) greedy, exploration 0.1, on x = [u_g + u_h, |u_g - u_h|] (16 dims) concatenated with the category one-hot (3 dims). Initialised from the development pairs for the same line, updated only with queried evaluation outcomes within a trial.
4. shuffled_contextual (control): arm 3 with gene vectors permuted across genes by a fixed permutation (seed 20261008) before pair features are built. Tests whether signal comes from the specific gene representation or generic features.
No RL arm: the judge's own analysis and ours say the representation, not the optimiser, is the question. No hyperparameter is tuned; all values above are fixed.

## Pre-registered primary endpoint and success rule
Primary: Delta = mean over lines of [mean over seeds of H60(contextual_greedy) - mean over seeds of H60(random)] on the evaluation pool.
Uncertainty: percentile bootstrap over the 27 lines, 10,000 resamples, numpy seed 314159, 95% interval. Seeds are not biological replicates and lines share lineage structure, so intervals are optimistic.
The contextual method is called USEFUL only if ALL hold: (1) Delta > 0; (2) the 95% interval lower bound > 0; (3) contextual_greedy > random on at least 14 of 27 lines (majority); (4) contextual_greedy minus category_greedy has mean > 0 and interval lower bound > 0; (5) no evaluation outcome was used to build u_g (guaranteed by design above).
Failure condition: any of (1)-(4) not met means no demonstrated value, and it is reported as such.
Secondary, descriptive only: H10 and H30; AUC; contextual minus shuffled; per-line table; counts of pairs and lines used. No claim of a biological finding, an external benchmark win over a published model, or a discovery may be drawn from this experiment under any outcome.

## Outputs
results/harle-gene-disjoint-contextual.json (summary, differences, per-line numbers; trial traces compressed), scripts/harle_gene_disjoint_contextual.py, docs result note. The representation hash is recorded in the result.
