"""Compare same-name published score variants; never impute filtered scores."""
import argparse,csv,hashlib,json
from pathlib import Path

def load(path):
    with open(path) as f:rs=list(csv.DictReader(f))
    if not rs:raise ValueError('empty score file')
    out={r['']:r for r in rs}
    if len(out)!=len(rs):raise ValueError('duplicate pair keys')
    return out

def compare(full,filtered):
    a,b=load(full),load(filtered)
    if set(a)!=set(b):raise ValueError('pair set mismatch')
    if any(set(a[k])!=set(b[k]) for k in a):raise ValueError('column mismatch')
    missing=0;retained=0;mismatch=[]
    for k,r in b.items():
        for c,v in r.items():
            if not c:continue
            if v=='NA':missing+=1
            else:
                retained+=1
                if v!=a[k][c]:mismatch.append([k,c])
    return {'pairs':len(a),'filtered_missing_cells':missing,'retained_cells':retained,'retained_value_mismatches':mismatch,
            'source_sha256':{Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in [full,filtered]},
            'scope':'Published baseline artifact variant reconciliation only; not independent baseline execution or scientific discovery'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',required=True);p.add_argument('--filtered',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=compare(a.full,a.filtered);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
