"""Descriptive full-guide sample similarity for GSE123290; no gene hit calling."""
import argparse, json
import numpy as np
import openpyxl

COLS=['A10_A','A10_B','A10_C','A5_A','A5_B','A5_C','Ctrl_A','Ctrl_B','Ctrl_C','S10_A','S10_B','S5_A','S5_B','S5_C']
def run(path):
    sh=openpyxl.load_workbook(path,read_only=True,data_only=True).active
    rows=sh.iter_rows(values_only=True)
    assert list(next(rows)[:15])==['GeneID']+COLS
    mats={'all':[], 'HGLibA':[], 'HGLibB':[]}
    for row in rows:
        label=row[0]
        try: x=np.asarray(row[1:15],dtype=float)
        except (TypeError,ValueError):continue
        if not isinstance(label,str) or len(x)!=14 or not np.isfinite(x).all() or (x<0).any():continue
        mats['all'].append(x)
        for tag in ('HGLibA','HGLibB'):
            if label.startswith(tag):mats[tag].append(x)
    out={}
    for name, mat in mats.items():
        x=np.asarray(mat)
        log=np.log2(x+1)
        corr=np.corrcoef(log.T)
        best={}
        for i,c in enumerate(COLS):
            candidates=sorted(((float(corr[i,j]),COLS[j]) for j in range(len(COLS)) if i!=j),reverse=True)
            best[c]=[{'sample':t,'pearson_log2_count':v} for v,t in candidates[:4]]
        out[name]={'guide_rows':int(len(x)), 'nearest_samples':best,
                   'declared_day10_replicate_pair_pearson':{f'{COLS[i]}__{COLS[j]}':float(corr[i,j]) for i,j in ((0,1),(0,2),(1,2),(9,10))}}
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workbook',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();r=run(a.workbook)
    r['source']='https://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123290/suppl/'
    r['scope']='Descriptive guide-level count similarity; no sample relabeling, causality, hit calling, or PEO1 transfer benchmark'
    with open(a.output,'w') as f:json.dump(r,f,indent=2)
    for n,v in r.items():
        if isinstance(v,dict):print(n,v['guide_rows'],v['declared_day10_replicate_pair_pearson'])
