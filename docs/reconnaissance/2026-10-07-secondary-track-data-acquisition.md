# Secondary-track data acquisition (2026-10-07)
Protocol: docs/SECONDARY-TRACK-PROTOCOL.md (frozen, unchanged; sha256 f3b36480...f23e). Raw files are NOT committed (licence + size); only hashes and derived tables will be.

## DepMap (Broad) - NOT used
Terms (https://depmap.org/portal/terms/, rev. 2026-04-02) include indemnification, Massachusetts jurisdiction consent and a non-commercial / AI-training carve-out. Not accepted. Nothing downloaded.

## Project Score / Cell Model Passports (Sanger) - used
Licence (https://www.sanger.ac.uk/tool/project-score-database/): non-exclusive internal research and educational use; resale and commercial services excluded; data "as is", warranties excluded. No account, no click-through, plain HTTP. No indemnity or jurisdiction clause seen.

| File | URL | bytes | sha256 |
|---|---|---|---|
| essentiality_matrices.zip | https://cog.sanger.ac.uk/cmp/download/essentiality_matrices.zip | 241487762 | 52bc7a58e39cbe8b973a82868057431f4b645c325d4994d20f11531a875c9d46 |
| model_list_latest.csv.gz | https://cog.sanger.ac.uk/cmp/download/model_list_latest.csv.gz | 145029 | 333affaa690c9f7e517467a6f78b00ffb418cb8449e2eb1cc5d93d85f7b0862e |
| mutations_all_latest.csv.gz | https://cog.sanger.ac.uk/cmp/download/mutations_all_latest.csv.gz | 309032595 | 350e8ce1fb5c8f56eead2128006f43a138d9a65e8dac0d9275f969b71529a461 |
| cnv_summary_20250207.zip | https://cog.sanger.ac.uk/cmp/download/cnv_summary_20250207.zip | 8344149 | e4dcab120ca283d0a0cfac72e68e333b0bee23c85ad1121df91a52e1987e0a8c |
| mutations_all_20230202.zip | https://cog.sanger.ac.uk/cmp/download/mutations_all_20230202.zip | 112642865 | bcd4a11690ed308706cc507377f8af2cc7abd2612fdf050c99ebd75631af58cb |

Essentiality matrices: 17,995 genes x 325 samples (Project Score 2019; scaled Bayesian factors, binary dependency calls, corrected logFCs).
Name-match scan (not a final cohort definition): 31 ovary-tissue models in the matrix, 10 annotated High Grade Ovarian Serous (OVCAR-8, OVCAR-5, OVCAR-3, JHOS-4, JHOS-2, TYK-nu, OVMIU, KURAMOCHI, Caov-4, Hey). Altered-line counts per biomarker will be small; power is limited and no nonmalignant lines exist here.
Caveat: only Project Score is available now, so the protocol's DepMap cohort and cross-cohort sign check cannot run. The protocol thresholds are unchanged; any deviation (single cohort) must be stated in results.
