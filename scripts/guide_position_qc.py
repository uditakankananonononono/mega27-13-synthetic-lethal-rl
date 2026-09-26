"""Post-outcome exploratory assay artifact audit, not a hit test."""
import argparse,json,sys
from collections import defaultdict
import numpy as np
sys.path.insert(0,'src')
from slrl.assay import parse_sheet,guide_family,fold_change

def main():
 p=argparse.ArgumentParser();p.add_argument('--workbook',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 singles=defaultdict(lambda:defaultdict(list));controls=defaultdict(list);sizes=defaultdict(list)
 for guides,counts in parse_sheet(a.workbook):
  fam=[guide_family(g) for g in guides];unique=sorted(set(fam)-{'CTRL'})
  if len(unique)!=sum(x!='CTRL' for x in fam):continue
  fc=fold_change(counts)
  sizes[len(unique)].append(fc)
  if not unique:
   controls[tuple(guides)].append(fc)
  if len(unique)==1:
   pos=next(i for i,x in enumerate(fam) if x!='CTRL')
   singles[unique[0]][pos].append(fc)
 result={};range_by_rep=[[],[]]
 for gene,positions in sorted(singles.items()):
  if len(positions)!=3:continue
  medians={str(p):np.median(rows,axis=0).tolist() for p,rows in positions.items()}
  ranges=(np.max(list(medians.values()),axis=0)-np.min(list(medians.values()),axis=0)).tolist()
  for i in (0,1):range_by_rep[i].append(ranges[i])
  result[gene]={'constructs_by_position':{str(p):len(rows) for p,rows in positions.items()},'median_log2fc_by_position':medians,'max_minus_min_log2':ranges}
 ctrl={','.join(g):np.median(v,axis=0).tolist() for g,v in controls.items()}
 size_summary={str(n):{'constructs':len(v),'median_log2fc':np.median(v,axis=0).tolist()} for n,v in sizes.items()}
 out={'scope':'post-outcome GSE154112 guide-position and dummy-guide load artifact QC; no viability or statistical discovery claim','single_gene_position_effects':result,'median_gene_position_range_by_replicate':np.median(range_by_rep,axis=1).tolist(),'max_gene_position_range_by_replicate':np.max(range_by_rep,axis=1).tolist(),'all_dummy_control_constructs':ctrl,'target_load_medians':size_summary}
 with open(a.output,'w') as f:json.dump(out,f,indent=2)
 print(json.dumps({'single_genes':len(result),'median_position_range':out['median_gene_position_range_by_replicate'],'max_position_range':out['max_gene_position_range_by_replicate'],'control_count':len(ctrl),'target_load_medians':size_summary},indent=2))
if __name__=='__main__':main()
