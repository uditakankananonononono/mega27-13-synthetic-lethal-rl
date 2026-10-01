"""Audit schema and split; author outcomes are endpoints, never input features."""
import argparse,collections,hashlib,json
from pathlib import Path
import openpyxl

def canonical(pair):
    a,b=pair.split('|')
    if not a or not b or a==b:raise ValueError('invalid pair')
    return '|'.join(sorted((a,b)))

def partition(pair):
    return 'development' if int(hashlib.sha256(('harle-methods-v1|'+canonical(pair)).encode()).hexdigest()[:8],16)%5==0 else 'evaluation'

def rows(sheet,header):
    it=sheet.iter_rows(values_only=True)
    for _ in range(header-1):next(it)
    h=next(it)
    for r in it:
        if r[0] is not None or r[1] is not None:yield dict(zip(h,r))

def audit(path):
    w=openpyxl.load_workbook(path,read_only=True,data_only=True)
    designs={}
    for r in rows(w['Table S1'],3):
        if r.get('guide_type')=='gene|gene' and isinstance(r.get('sorted_gene_pair'),str):
            p=canonical(r['sorted_gene_pair']);designs.setdefault(p,set()).add(r['sgrna_group'])
    endpoints=list(rows(w['Table S4'],5))
    pairs={canonical(r['sorted_gene_pair']) for r in endpoints}
    lines=sorted({r['cell_line_label'] for r in endpoints})
    bytype=collections.defaultdict(set)
    for r in endpoints:bytype[r['cancer_type']].add(r['cell_line_label'])
    key_counts=collections.Counter((canonical(r['sorted_gene_pair']),r['cell_line_label']) for r in endpoints)
    dup=[list(k) for k,v in key_counts.items() if v!=1]
    selected=set(pairs)&set(designs)
    split={p:partition(p) for p in sorted(selected)}
    genes={label:set(g for p,v in split.items() if v==label for g in p.split('|')) for label in ['development','evaluation']}
    s3=rows(w['Table S3'],5);sample=next(s3)
    out={'schema':'harle-ingestion-audit-v1','workbook_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        'design_pairs':len(designs),'outcome_pairs':len(pairs),'outcome_rows':len(endpoints),'screened_lines':lines,
        'lines_by_cancer_type':{k:sorted(v) for k,v in bytype.items()},'duplicate_pair_line_keys':dup,
        'design_only_pairs':sorted(set(designs)-pairs),'outcome_only_pairs':sorted(pairs-set(designs)),
        'split':split,'split_counts':dict(collections.Counter(split.values())),
        'genes_shared_between_pair_partitions':sorted(genes['development']&genes['evaluation']),
        'example_table_s3_noninteger_count':sample['A-375 R1'],
        'eligible_for_hgsoc_claim':False,'eligible_for_normal_selectivity_claim':False,
        'scope':'Retrospective measured-feedback methods pivot, not blinded discovery; pair split is not gene-disjoint',
        'unresolved':['S3 normalized/noninteger count provenance','473 design versus 472 endpoint pairs','Expression/copy-number provenance','Fair executable published external baseline']}
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workbook',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    r=audit(a.workbook);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['design_pairs','outcome_pairs','outcome_rows','split_counts','design_only_pairs','duplicate_pair_line_keys']}))
