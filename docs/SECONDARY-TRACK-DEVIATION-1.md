# Secondary track deviation 1 (FROZEN before any calculation; amends nothing in the locked gate)
Parent: docs/SECONDARY-TRACK-PROTOCOL.md (sha256 f3b3648028c6be8658bfdf7be645c80e58d70f147a5e09fb6e51f5eae898f23e).
Reason: DepMap terms not accepted, so only Sanger Project Score (2019 matrices, 325 lines) is available. Every result must state: single cohort, no cross-cohort sign check.
1. Effect measure: 01_corrected_logFCs.tsv (CRISPRcleaned logFC). The -0.3 effect-difference threshold is carried over numerically; it is NOT a Chronos-equivalent.
2. Universe: all 17,995 genes in the matrix (the GO:0006281 list is not available offline). BH across all tested pairs. A DNA-repair subset is not reported.
3. Common-essential flag: gene is binary-dependent (04_binaryDepScores) in >=90% of all 325 lines; flagged and excluded.
4. Test set: ovary-tissue models (model_list tissue == Ovary) present in the matrix by case-insensitive model_name match. HGSOC-annotated subset reported separately as a sensitivity analysis.
5. Biomarkers and alteration calls: BRCA1, BRCA2, RB1 = coding nonsense/frameshift/ess_splice mutation; TP53 = those plus coding missense; CCNE1 = cn_category Amplification. Minimum 3 altered and 3 unaltered lines per biomarker or it is not tested.
6. Test: Mann-Whitney U (two-sided), altered vs unaltered; hit = BH q < 0.1 and median difference <= -0.3. All tested pairs are written to results.
7. Outputs are hypotheses only. No gate counts change.
