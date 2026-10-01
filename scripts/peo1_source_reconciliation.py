"""Recover GEO sample identities without selecting outcome-favored replicates."""
import argparse
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

EXPECTED = ['A10_A','A10_B','A10_C','A5_A','A5_B','A5_C','Ctrl_A','Ctrl_B','Ctrl_C','S10_A','S10_B','S5_A','S5_B','S5_C']

def reconcile(soft_text, paper_xml):
    samples = {}
    for block in soft_text.split('^SAMPLE = ')[1:]:
        accession = block.splitlines()[0].strip()
        fields = {}
        for line in block.splitlines()[1:]:
            if line.startswith('!Sample_') and ' = ' in line:
                key, value = line.split(' = ', 1)
                fields.setdefault(key, []).append(value)
        labels = [v for v in fields.get('!Sample_description', []) if v in EXPECTED]
        if not labels:
            continue
        if len(labels) != 1 or labels[0] in samples:
            raise ValueError('ambiguous or repeated workbook sample identity')
        samples[labels[0]] = {'geo_accession':accession,
            'title':fields.get('!Sample_title', []),
            'characteristics':fields.get('!Sample_characteristics_ch1', []),
            'processing':fields.get('!Sample_data_processing', [])}
    missing = sorted(set(EXPECTED) - set(samples))
    root = ET.fromstring(paper_xml)
    paragraphs = [' '.join(p.itertext()) for p in root.iter('p')]
    selection = [p for p in paragraphs if 'duplicates of Adherent Day 10' in p]
    paper_deseq = any('DESEq2' in p or 'DESeq2' in p for p in paragraphs)
    geo_edger = any('edgeR' in v for s in samples.values() for v in s['processing'])
    return {'schema':'peo1-source-reconciliation-v1',
        'scope':'Sample identity reconciliation only; not a ranking, benchmark, interaction or discovery',
        'samples':samples, 'missing_workbook_columns':missing,
        'paper_selected_duplicate_evidence':selection,
        'paper_guide_differential_abundance_mentions_deseq2':paper_deseq,
        'geo_crispr_processing_mentions_edger':geo_edger,
        'processing_conflict':paper_deseq and geo_edger,
        'adherent_pair_selected_by_primary_paper':'UNRESOLVED',
        'benchmark_eligible':False,
        'reasons':['Selected A10 pair not recovered from inspected primary article and GEO metadata',
            'Supplementary methods/figures not retrieved as valid PDF',
            'GEO processing description conflicts with paper guide-analysis description',
            'Monogenic suspension/adherent depletion cannot validate pair/triple synthetic lethality or normal selectivity']}

def main():
    p=argparse.ArgumentParser();p.add_argument('--soft',required=True);p.add_argument('--paper-xml',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();soft=Path(a.soft);paper=Path(a.paper_xml)
    out=reconcile(gzip.decompress(soft.read_bytes()).decode(),paper.read_text())
    out['source_sha256']={str(soft.name):hashlib.sha256(soft.read_bytes()).hexdigest(),str(paper.name):hashlib.sha256(paper.read_bytes()).hexdigest()}
    out['source_urls']=['https://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123290/soft/GSE123290_family.soft.gz','https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6710300/fullTextXML','https://pmc.ncbi.nlm.nih.gov/articles/PMC6710300/']
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'mapped_columns':len(out['samples']),'missing':out['missing_workbook_columns'],'processing_conflict':out['processing_conflict'],'benchmark_eligible':out['benchmark_eligible']}))
if __name__=='__main__':main()
