# Corrected base measure: tested, not a benchmark rescue

The prespecified post-outcome correction uses degree-weighted first-gene mass and edge-weighted partners, producing exact pair softmax. The implementation is tested analytically and by unrevealed-first-query checks. `--include-correction` enables it in the benchmark runner; omission keeps the original five arms.

Across the same exposed screen, 27 lines and 20 seeds, corrected policy retrieves mean 4.2074 published hits in 60 queries. Original RL retrieves 4.3463 and random 4.6593. All 2,700 original-arm traces reproduce exactly. The corrected run has 3,240 total traces; each contains 60 unique pair queries. The paired corrected-minus-random result and line-bootstrap interval are in `results/harle-corrected-integrity.json`.

This is post-outcome development, not independent validation. It refutes the claim that this mathematical base-measure fix alone recovers performance. Pair-softmax factorization is a transparent correction/control, not a novel discovery. No more tuning on this evaluation set will be labeled an untouched benchmark.

Judge prompt is prepared but no submission, response or implemented judge round is claimed. The next scientific step requires a new measured screen and a source-audited comparable predictor, not more simulation wins.
