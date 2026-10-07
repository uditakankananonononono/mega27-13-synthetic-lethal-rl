"""Builds paper/draft.docx (Times New Roman) from the evidence-gated skeleton. Every claim cites a repo artifact."""
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
S = [
 ("Abstract", ["[STATUS: skeleton] Sequential RL for selecting DNA-repair gene pairs and triples in high-grade serous ovarian carcinoma (HGSOC) did not beat random selection on an external measured benchmark, and no new biological discovery is claimed. Evidence: results/evidence-gate-ledger.json."]),
 ("1. Introduction", ["[TODO] DNA-repair synthetic lethality in HGSOC; why combinatorial search; the pre-registered question (docs/PREREGISTRATION.md, hash-pinned)."]),
 ("2. Pre-registration and evidence gates", ["The locked gate and eight completion gates are listed in results/evidence-gate-ledger.json. All eight are UNMET at this draft. Narrower methodological questions are labelled separately from the locked gate."]),
 ("3. Methods", ["3.1 Sequential RL policy and baselines (greedy, beam, random). [TODO from src/slrl].",
   "3.2 Surrogate and measured benchmarks. Harle pan-cancer retrospective: 27 lines, 2,700 trials.",
   "3.3 Data inclusion rule: a dataset counts only if raw or primary-derived measurements were retrieved and analysed (results/dataset-count-audit.json)."]),
 ("4. Results", ["4.1 External measured benchmark: mean random hits@60 4.659 versus RL 4.346; corrected policy minus random -0.452 (results/evidence-gate-ledger.json). RL does not beat random.",
   "4.2 GSE154112 (OVCAR8-ADR): 455 evaluable triples, 0 at BH q<0.05, no matched normal (docs/GSE154112-NEGATIVE.md).",
   "4.3 SPIDR score-level description: cross-context Spearman 0.020 to 0.110, selection- and censoring-limited; count-level contrasts stopped on unrecovered orientation processing (docs/SPIDR-IDENTITY-AUDIT-FREEZE.md).",
   "4.4 Secondary track (Project Score): zero hits, structurally underpowered at 3 to 6 altered lines; a data limitation, not a biological result (docs/SECONDARY-TRACK-RESULT-1.md).",
   "4.5 Rejected or stopped sources: PEO1 QC stop, CombiGEM (same lab and line), DepMap (terms not accepted)."]),
 ("5. Limitations", ["No matched nonmalignant viability data; no independent HGSOC multi-model dual-guide dataset; five datasets counted of the 120 targeted; no external judge round completed."]),
 ("6. Discussion", ["[TODO] What a future adequately powered, independent HGSOC screen would need."]),
 ("7. Data and code availability", ["Repository: github.com/uditakankananonononono/mega27-13-synthetic-lethal-rl. Raw third-party files are not redistributed; accessions and hashes are in docs/reconnaissance/."]),
]
d = Document()
for st in ("Normal", "Heading 1", "Title"):
    s = d.styles[st]; s.font.name = "Times New Roman"; s.font.color.rgb = None
    s.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
d.styles["Normal"].font.size = Pt(12)
d.add_heading("Sequential reinforcement learning for DNA-repair synthetic-lethal search in HGSOC: a negative-result draft", 0)
for h, ps in S:
    d.add_heading(h, 1)
    for p in ps: d.add_paragraph(p)
d.save("paper/draft.docx"); print("saved")
