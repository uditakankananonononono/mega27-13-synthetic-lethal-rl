"""Internal same-study cell-line QC, NEVER pair/triple validation or selectivity."""
import argparse,csv,json,sys
import numpy as np
from scipy.stats import spearmanr
sys.path.insert(0,'src')
from slrl.development import build_legacy_cancer_proxy
from slrl.sanger import model_name_map

def main():
 p=argparse.ArgumentParser();p.add_argument('--score',required=True);p.add_argument('--reactome',required=True);p.add_argument('--map',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 held={'ACH-000524','ACH-000696','ACH-001630','ACH-001632'}
 modelmap=model_name_map(a.map)
 r=build_legacy_cancer_proxy(a.score,a.reactome,modelmap,heldout_models=held,max_genes=2000)
 symbols=[f'{s} ({g})' for s,g in zip(r['symbols'],r['genes'])]
 with open(a.score,encoding='utf-8-sig',newline='') as f:rd=csv.DictReader(f);rows={row['']:row for row in rd if row[''] in held}
 out=[]
 for model,row in sorted(rows.items()):
  x=np.array([float(row[s]) if row[s] not in ('','NA') else np.nan for s in symbols]);truth=np.clip(-x,0,2)
  pred=r['surrogate'].cancer_single;valid=np.isfinite(truth)&np.isfinite(pred)&np.isfinite(r['surrogate'].uncertainty)
  out.append({'model':model,'name':modelmap[model],'genes':int(valid.sum()),'spearman':float(spearmanr(truth[valid],pred[valid]).statistic),'mae':float(np.mean(abs(truth[valid]-pred[valid]))),'constant_0.2_mae':float(np.mean(abs(truth[valid]-.2)))})
 result={'scope':'same-study monogenic holdout, not paired/triple or healthy-cell validation','training_models':len(r['development_models']),'selected_gene_count':len(r['genes']),'repair_action_genes':r['repair_action_genes'],'results':out}
 with open(a.output,'w') as f:json.dump(result,f,indent=2)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
