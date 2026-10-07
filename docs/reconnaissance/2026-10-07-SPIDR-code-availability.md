# SPIDR code availability check (2026-10-07)
- Paper Code availability and Reporting Summary (MOESM2) name BBMap + GEMINI (github.com/sellerslab/gemini); modified code is in Supplementary Information (MOESM1 docx, "modified GEMINI calculate LFC function", pseudocount 10, no median-centering).
- The supplied function only computes normalized counts/LFC from an already-built Input object. It contains no guide-name parsing, no pair-orientation handling, no count-to-design mapping.
- Result: the publisher's orientation processing remains unrecovered. Count-derived SPIDR contrasts stay STOPPED. No orientation swap is permitted.
- Sources: https://www.nature.com/articles/s41586-025-08815-4 ; MOESM1 docx and MOESM2 pdf under media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-025-08815-4/MediaObjects/
