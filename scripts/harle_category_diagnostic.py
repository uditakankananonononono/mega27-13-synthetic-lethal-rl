"""Post-outcome diagnostic of category shift and untrained pair sampling bias."""
import argparse,collections,json
from pathlib import Path
import numpy as np,openpyxl
from harle_ingestion_audit import rows,canonical,partition

def audit(path,trace):
 w=openpyxl.load_workbook(path,read_only=True,data_only=True);cats={}
 for r in rows(w['Table S1'],3):
  if r.get('guide_type')=='gene|gene' and isinstance(r.get('sorted_gene_pair'),str):cats[canonical(r['sorted_gene_pair'])]=r['sgrna_group']
 it=w['Table S5'].iter_rows(values_only=True)
 for _ in range(3):next(it)
 header=next(it);data=[r for r in it if isinstance(r[0],str)]
 rates={}
 for part in ['development','evaluation']:
  rates[part]={}
  for c in sorted(set(cats.values())):
   d=[r for r in data if cats[canonical(r[0])]==c and partition(r[0])==part];y=np.asarray([r[1:28] for r in d],float)
   rates[part][c]={'pairs':len(d),'hits':int(y.sum()),'pair_line_observations':int(y.size),'hit_fraction':float(y.mean())}
 ev=[canonical(r[0]) for r in data if partition(r[0])=='evaluation'];degree=collections.Counter(g for p in ev for g in p.split('|'));ng=len(degree)
 probs={p:sum(1/degree[g] for g in p.split('|'))/ng for p in ev}
 mass={c:sum(probs[p] for p in ev if cats[p]==c) for c in sorted(set(cats.values()))}
 uniform={c:sum(cats[p]==c for p in ev)/len(ev) for c in mass}
 trials=json.loads(Path(trace).read_text())['trials'];freq={}
 for method in sorted({t['method'] for t in trials}):
  count=collections.Counter(cats[p] for t in trials if t['method']==method for p in t['queried_pairs'])
  freq[method]={c:n/sum(count.values()) for c,n in sorted(count.items())}
 return {'scope':'Post-outcome methodological diagnostic, not an explanation proved causal or a biological discovery','category_rates':rates,'untrained_uniform_first_gene_pair_probability':{'sum':sum(probs.values()),'min':min(probs.values()),'max':max(probs.values()),'max_to_min':max(probs.values())/min(probs.values()),'category_mass':mass},'uniform_pair_category_mass':uniform,'observed_query_category_fraction':freq,'next_change':'Use degree-corrected first-gene and partner base measures to make zero-score policy uniform over eligible pairs. Freeze before rerun; rerun is post-outcome development, not untouched validation.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--workbook',required=True);p.add_argument('--trace',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=audit(a.workbook,a.trace);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
