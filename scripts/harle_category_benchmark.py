"""Measured-feedback retrospective category benchmark; no cell simulation."""
import argparse,collections,hashlib,json
from pathlib import Path
import numpy as np
import openpyxl
from harle_ingestion_audit import canonical,partition,rows

METHODS=['random','fixed_category','ridge_greedy','ridge_ucb','sequential_reinforce']

def softmax(x):
    e=np.exp(x-x.max());return e/e.sum()

def trial(x,y,pairs,dev,ev,method,seed,budget=60,gene_features=None):
    rng=np.random.default_rng(seed)
    n=x[dev].sum(axis=0);s=x[dev].T@y[dev];initial=s/(n+1)
    weights=initial.copy();baseline=float(np.mean(y[dev]));available=list(ev);hits=[];chosen=[]
    if gene_features is None:
        gene_features={g:np.mean([x[i] for i,p in enumerate(pairs) if g in p.split('|')],axis=0) for g in {g for p in pairs for g in p.split('|')}}
    for _ in range(min(budget,len(available))):
        a=np.asarray(available);features=x[a];mean=s/(n+1);grad=None
        if method=='random':j=int(rng.integers(len(a)))
        elif method=='fixed_category':
            score=features@initial;j=int(rng.choice(np.flatnonzero(np.isclose(score,score.max()))))
        elif method in ['ridge_greedy','ridge_ucb']:
            score=features@mean
            if method=='ridge_ucb':score=score+np.sqrt((features**2)@(1/(n+1)))
            if method=='ridge_greedy' and rng.random()<.1:j=int(rng.integers(len(a)))
            else:j=int(rng.choice(np.flatnonzero(np.isclose(score,score.max()))))
        else:
            genes=sorted({g for i in a for g in pairs[i].split('|')});gf=np.asarray([gene_features[g] for g in genes])
            probs=softmax(gf@weights);gi=int(rng.choice(len(genes),p=probs));g=genes[gi]
            legal=np.asarray([j for j,i in enumerate(a) if g in pairs[i].split('|')]);lf=features[legal]
            p=softmax(lf@weights);pick=int(rng.choice(len(legal),p=p));j=int(legal[pick]);grad=gf[gi]-probs@gf+lf[pick]-p@lf
        i=available.pop(j);r=float(y[i]);hits.append(r);chosen.append(i)
        # Only the queried evaluation endpoint is revealed to this trial.
        n+=x[i];s+=x[i]*r
        if grad is not None:
            weights+=.05*np.clip((r-baseline)*grad,-5,5);baseline=.95*baseline+.05*r
    c=np.cumsum(hits)
    return {'hits_at':{str(b):float(c[min(b,len(c))-1]) for b in [10,30,60]},'auc':float(c.mean()),'unique_queries':len(set(chosen)),'queries':len(chosen),'queried_pairs':[pairs[i] for i in chosen],'query_rewards':hits}

def run(path,seeds=20):
    w=openpyxl.load_workbook(path,read_only=True,data_only=True)
    categories=collections.defaultdict(set)
    for r in rows(w['Table S1'],3):
        if r.get('guide_type')=='gene|gene' and isinstance(r.get('sorted_gene_pair'),str):categories[canonical(r['sorted_gene_pair'])].add(r['sgrna_group'])
    sheet=w['Table S5'];it=sheet.iter_rows(values_only=True)
    for _ in range(3):next(it)
    header=next(it);lines=list(header[1:28]);records=[]
    for r in it:
        if isinstance(r[0],str):
            if any(v not in (0,1) for v in r[1:28]):raise ValueError('invalid endpoint')
            records.append((canonical(r[0]),list(r[1:28])))
    records.sort();pairs=[p for p,y in records];y=np.array([v for p,v in records],float)
    cats=sorted({c for p in pairs for c in categories[p]});x=np.array([[int(c in categories[p]) for c in cats] for p in pairs],float)
    if np.any(x.sum(axis=1)!=1):raise ValueError('first-pass categories must be exclusive')
    dev=np.array([i for i,p in enumerate(pairs) if partition(p)=='development']);ev=np.array([i for i,p in enumerate(pairs) if partition(p)=='evaluation'])
    gene_features={g:np.mean([x[i] for i,p in enumerate(pairs) if g in p.split('|')],axis=0) for g in {g for p in pairs for g in p.split('|')}}
    trials=[]
    for line,j in zip(lines,range(len(lines))):
        for seed in range(seeds):
            for method in METHODS:
                t=trial(x,y[:,j],pairs,dev,ev,method,seed,gene_features=gene_features);t.update(line=line,seed=seed,method=method);trials.append(t)
    summary={m:{'mean_hits_60':float(np.mean([t['hits_at']['60'] for t in trials if t['method']==m])), 'mean_auc':float(np.mean([t['auc'] for t in trials if t['method']==m]))} for m in METHODS}
    differences={}
    rng=np.random.default_rng(314159)
    for m in METHODS[:-1]:
        d=np.array([np.mean([t['hits_at']['60'] for t in trials if t['line']==line and t['method']=='sequential_reinforce'])-np.mean([t['hits_at']['60'] for t in trials if t['line']==line and t['method']==m]) for line in lines])
        b=rng.choice(d,(10000,len(d)),replace=True).mean(axis=1)
        differences[m]={'mean_line_difference_hits60':float(d.mean()),'line_bootstrap_95_interval':np.quantile(b,[.025,.975]).tolist(),'lines_rl_better':int((d>0).sum()),'lines_equal':int((d==0).sum()),'lines_rl_worse':int((d<0).sum())}
    return {'schema':'harle-category-benchmark-v1','workbook_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'scope':'Retrospective binary author-hit query retrieval, category-only; not HGSOC, normal selectivity, discovery or published leading-model beat','categories':cats,'development_pairs':len(dev),'evaluation_pairs':len(ev),'lines':len(lines),'seeds':seeds,'budget':60,'summary':summary,'rl_minus_controls':differences,'trials':trials}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--workbook',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=run(a.workbook);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'summary':r['summary'],'rl_minus_controls':r['rl_minus_controls']},indent=2))
