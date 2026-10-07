# Dual-guide DNA-repair screen candidates vs the locked HGSOC gate (2026-10-07)
Locked gate (docs/PREREGISTRATION.md) is unchanged. Result: no candidate is eligible.

| Candidate | Evidence read | Status |
|---|---|---|
| Genome Biology 2025, pan-cancer combinatorial compendium (s13059-025-03737-w) | Full text | Excluded. 472 pairs, 27 melanoma/pancreatic/lung lines, no HGSOC, no matched normal. 272 of 472 pairs overlap SLKB (exposed Thompson data). Code on GitHub/Zenodo; no raw-count accession found in text read. At most a separately labelled methodological check. |
| PARPi genetic-interaction network (PMC10462155) | Full text | Excluded. K562 CRISPRi screen, RPE1 validation only. Same CRISPRi family as SPIDR. Not HGSOC. |
| Cell Reports 2025 DNA-repair network (S2211-1247(25)01622-5) | Search snippet only | Not verified. No evidence of HGSOC or matched normal. |
| Cas12a DDR combinatorial knockout screens | Listing only, primary source not found | Not verified. |
| Cell 2021 DSB-repair landscape (S0092-8674(21)01176-4) | Search snippet only | Not verified. |

The original discovery gate stays data-blocked. Unverified rows are not counted as ineligible-with-proof; they are unread.
Sources: https://link.springer.com/article/10.1186/s13059-025-03737-w ; https://pmc.ncbi.nlm.nih.gov/articles/PMC10462155/

## Amendment 2026-10-08
The Genome Biology 2025 compendium (Harle et al.) is the same source as the Harle methods benchmark used in results/harle-corrected-development.json. It is excluded for the locked HGSOC gate (no HGSOC, no matched normal, SLKB overlap) but is counted once in results/dataset-count-audit.json as a retrospective methods benchmark, not an independent validation set.
