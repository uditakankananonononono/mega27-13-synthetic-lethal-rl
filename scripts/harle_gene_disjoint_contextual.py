"""Frozen experiment: docs/HARLE-GENE-DISJOINT-CONTEXTUAL-FREEZE.md. Methods result only; no biological claim."""
import argparse,collections,hashlib,io,json,re,sys,zipfile
from pathlib import Path
import numpy as np
import openpyxl
sys.path.insert(0,str(Path(__file__).parent))
from harle_ingestion_audit import canonical,rows

def norm(s):return re.sub(r'[^A-Z0-9]','',str(s).upper())
def gpart(g):return int(hashlib.sha256(('harle-genedisjoint-v1|'+g).encode()).hexdigest()[:8],16)%2

def representation(ess_zip,harle_lines):
    z=zipfile.ZipFile(ess_zip);f=io.TextIOWrapper(z.open('EssentialityMatrices/03_scaledBayesianFactors.tsv'),encoding='utf8')
    head=next(f).rstrip('\n').split('\t')[1:];hl={norm(l) for l in harle_lines}
    keep=[i for i,c in enumerate(head) if norm(c) not in hl];genes=[];rows_=[]
    for line in f:
        p=line.rstrip('\n').split('\t');genes.append(p[0]);rows_.append([float(v) if v not in('','NA','NaN') else np.nan for v in p[1:]])
    M=np.array(rows_)[:,keep];mu=np.nanmean(M,axis=0);sd=np.nanstd(M,axis=0);sd[sd==0]=1
    M=(M-mu)/sd;M=np.nan_to_num(M,nan=0.0)
    U,S,_=np.linalg.svd(M,full_matrices=False);sc=U[:,:8]*S[:8]
    for k in range(8):
        i=int(np.argmax(np.abs(sc[:,k])))
        if sc[i,k]<0:sc[:,k]*=-1
    h=hashlib.sha256(np.round(sc,5).tobytes()).hexdigest()
    return dict(zip(genes,sc)),h,{'columns_total':len(head),'columns_removed_harle_lines':len(head)-len(keep),'genes':len(genes)}

def trial(X,y,dev,ev,seed,budget=60,explore=.1):
    rng=np.random.default_rng(seed);d=X.shape[1]
    A=np.eye(d)+X[dev].T@X[dev];b=X[dev].T@y[dev];avail=list(ev);hits=[]
    for _ in range(min(budget,len(avail))):
        a=np.asarray(avail);theta=np.linalg.solve(A,b);score=X[a]@theta
        j=int(rng.integers(len(a))) if rng.random()<explore else int(rng.choice(np.flatnonzero(np.isclose(score,score.max()))))
        i=avail.pop(j);r=float(y[i]);hits.append(r);A+=np.outer(X[i],X[i]);b+=X[i]*r
    return hits

def rand_trial(y,ev,seed,budget=60):
    rng=np.random.default_rng(seed);a=np.asarray(ev);return [float(y[i]) for i in rng.permutation(a)[:budget]]

def run(workbook,ess_zip,seeds=20):
    w=openpyxl.load_workbook(workbook,read_only=True,data_only=True)
    categories=collections.defaultdict(set);pair_design=set()
    for r in rows(w['Table S1'],3):
        if r.get('guide_type')=='gene|gene' and isinstance(r.get('sorted_gene_pair'),str):
            c=canonical(r['sorted_gene_pair']);categories[c].add(r['sgrna_group']);pair_design.add(c)
    # lines are read from the S5 header only; the representation is built BEFORE any S5 data row is read
    it=w['Table S5'].iter_rows(values_only=True)
    for _ in range(3):next(it)
    header=next(it);lines=list(header[1:28])
    u,rep_hash,rep_info=representation(ess_zip,lines)
    records=[]
    for r in it:
        if isinstance(r[0],str):
            if any(v not in(0,1) for v in r[1:28]):raise ValueError('invalid endpoint')
            records.append((canonical(r[0]),list(r[1:28])))
    records.sort();pairs=[p for p,_ in records];Y=np.array([v for _,v in records],float)
    ok=[i for i,p in enumerate(pairs) if all(g in u for g in p.split('|')) and len(categories[p])==1]
    def kind(p):
        ps={gpart(g) for g in p.split('|')};return 'dev' if ps=={0} else 'ev' if ps=={1} else 'mixed'
    dev=np.array([i for i in ok if kind(pairs[i])=='dev']);ev=np.array([i for i in ok if kind(pairs[i])=='ev'])
    cats=sorted({c for p in pairs for c in categories[p]});oh=lambda p:np.array([float(c in categories[p]) for c in cats])
    genes=sorted(u);perm=np.random.default_rng(20261008).permutation(len(genes));shuf={g:u[genes[perm[i]]] for i,g in enumerate(genes)}
    def feats(p,rep):
        a,b_=[rep[g] for g in p.split('|')];return np.concatenate([a+b_,np.abs(a-b_),oh(p)])
    Xc=np.array([oh(p) for p in pairs]);Xx=np.array([feats(p,u) for p in pairs]);Xs=np.array([feats(p,shuf) for p in pairs])
    arms={'random':None,'category_greedy':Xc,'contextual_greedy':Xx,'shuffled_contextual':Xs}
    res={m:{} for m in arms}
    for j,line in enumerate(lines):
        for m,X in arms.items():
            res[m][line]=[(rand_trial(Y[:,j],ev,s) if X is None else trial(X,Y[:,j],dev,ev,s)) for s in range(seeds)]
    def H(m,line,b):return float(np.mean([np.sum(t[:b]) for t in res[m][line]]))
    rng=np.random.default_rng(314159);out={}
    for b in (60,30,10):
        out[f'H{b}']={m:float(np.mean([H(m,l,b) for l in lines])) for m in arms}
    def diff(a,c,b=60):
        d=np.array([H(a,l,b)-H(c,l,b) for l in lines]);bs=rng.choice(d,(10000,len(d)),replace=True).mean(axis=1)
        return {'mean':float(d.mean()),'ci95':np.quantile(bs,[.025,.975]).tolist(),'lines_better':int((d>0).sum()),'lines_equal':int((d==0).sum()),'lines_worse':int((d<0).sum())}
    D={'contextual_minus_random':diff('contextual_greedy','random'),'contextual_minus_category_greedy':diff('contextual_greedy','category_greedy'),
       'contextual_minus_shuffled':diff('contextual_greedy','shuffled_contextual'),'category_greedy_minus_random':diff('category_greedy','random'),
       'shuffled_minus_random':diff('shuffled_contextual','random')}
    c1=D['contextual_minus_random'];c2=D['contextual_minus_category_greedy']
    conds={'delta_gt_0':c1['mean']>0,'ci_lower_gt_0':c1['ci95'][0]>0,'majority_lines_gt_random':c1['lines_better']>=14,'beats_category_greedy_ci':c2['mean']>0 and c2['ci95'][0]>0}
    return {'schema':'harle-gene-disjoint-contextual-v1','freeze_doc_sha256':hashlib.sha256(Path('docs/HARLE-GENE-DISJOINT-CONTEXTUAL-FREEZE.md').read_bytes()).hexdigest(),
      'workbook_sha256':hashlib.sha256(Path(workbook).read_bytes()).hexdigest(),'essentiality_zip_sha256':hashlib.sha256(Path(ess_zip).read_bytes()).hexdigest(),
      'representation_sha256':rep_hash,'representation_info':rep_info,'dev_pairs':len(dev),'eval_pairs':len(ev),'lines':len(lines),'seeds':seeds,'budget':60,
      'mean_hits':out,'differences':D,'success_conditions':conds,'USEFUL':all(conds.values()),
      'scope':'Methods result on lung/pancreas/melanoma benchmark; not HGSOC, not matched-normal, no discovery or published-model beat.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workbook',required=True);p.add_argument('--ess-zip',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    r=run(a.workbook,a.ess_zip);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['representation_sha256','representation_info','dev_pairs','eval_pairs','mean_hits','differences','success_conditions','USEFUL']},indent=2))
