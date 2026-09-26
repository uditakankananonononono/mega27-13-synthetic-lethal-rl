"""Exploratory post-outcome position-matched inclusion-exclusion sensitivity, no hit calls."""
import argparse,json,sys
from collections import defaultdict
from itertools import combinations,permutations
import numpy as np
sys.path.insert(0,'src')
from slrl.assay import parse_sheet,guide_family,fold_change

def run(path):
 groups=defaultdict(list)
 for guides,counts in parse_sheet(path):
  fam=tuple(guide_family(g) for g in guides)
  if len(set(g for g in fam if g!='CTRL')) != sum(g!='CTRL' for g in fam):continue
  groups[fam].append(fold_change(counts))
 base=np.median(groups[('CTRL',)*3],axis=0)
 genes=sorted(set(g for f in groups for g in f if g!='CTRL'))
 records=[]
 for trip in combinations(genes,3):
  position_effects=[]
  for layout in permutations(trip):
   z=np.zeros(2);complete=True
   for mask in range(8):
    configuration=tuple(layout[i] if mask&(1<<i) else 'CTRL' for i in range(3))
    if len(groups[configuration])<1:complete=False;break
    sign=(-1)**(3-mask.bit_count())
    z+=sign*np.median(groups[configuration],axis=0)
   if complete:position_effects.append(z)
  if not position_effects:continue
  x=np.asarray(position_effects)
  records.append({'genes':trip,'layouts':len(x),'mean_by_replicate':x.mean(axis=0).tolist(),'layout_range_by_replicate':(x.max(axis=0)-x.min(axis=0)).tolist(),'all_layouts_negative_both_reps':bool(np.all(x<0))})
 return {'scope':'post-outcome, position-matched third-order contrast sensitivity; no inferential p-value, no viability','control_median':base.tolist(),'triples':records,'evaluated_triplets':len(records),'all_layouts_negative_both_reps_count':sum(r['all_layouts_negative_both_reps'] for r in records),'median_layout_range_by_replicate':np.median([r['layout_range_by_replicate'] for r in records],axis=0).tolist()}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--workbook',required=True);p.add_argument('--output',required=True);a=p.parse_args();out=run(a.workbook)
 with open(a.output,'w') as f:json.dump(out,f,indent=2)
 print(json.dumps({k:v for k,v in out.items() if k not in ('triples',)},indent=2))
