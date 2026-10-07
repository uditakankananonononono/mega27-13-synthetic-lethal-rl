# Gene-disjoint contextual experiment: result (frozen run, run once)

Freeze: docs/HARLE-GENE-DISJOINT-CONTEXTUAL-FREEZE.md (sha256 466e9e78...). Output: results/harle-gene-disjoint-contextual.json.
Representation sha256 d23039b6...; 325 columns, 21 Harle-line columns removed, 17,995 genes. Dev 103 pairs, eval 102 pairs.

Means (H60 / H30 / H10): random 4.724/2.113/0.789; category_greedy 6.361/3.354/1.048; contextual_greedy 5.072/2.763/0.863; shuffled 4.959/2.585/0.835.

Primary: contextual minus random H60 = +0.348, 95% CI -0.067 to +0.752; better on 17 of 27 lines, worse on 10.
Contextual minus category_greedy = -1.289, CI -1.737 to -0.857 (better on 2, worse on 25).
Contextual minus shuffled control = +0.113, CI -0.459 to +0.633.

Success rule: CI lower bound for the primary is below 0, and contextual is clearly worse than category_greedy. Result: NO DEMONSTRATED VALUE.
Note: a first execution crashed (KeyError ATP5PB) because features were built for pairs absent from Project Score; fixed by building features only for included pairs. No frozen parameter changed, and no results had been produced before the fix.
Caveats: methods-only; lung/pancreas/melanoma; 102-pair pool with ceiling effect; shared lineage structure; no discovery, no published-model beat.
