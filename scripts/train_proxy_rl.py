"""Cancer-only proxy policy experiment; NOT user's requested selective RL model."""
import argparse,json,sys
import numpy as np
sys.path.insert(0,'src')
from slrl.development import build_legacy_cancer_proxy
from slrl.sanger import model_name_map
from slrl.proxy_policy import CancerOnlyPolicy

def main():
 p=argparse.ArgumentParser();p.add_argument('--score',required=True);p.add_argument('--reactome',required=True);p.add_argument('--map',required=True);p.add_argument('--output',required=True);p.add_argument('--episodes',type=int,default=300);a=p.parse_args()
 modelmap=model_name_map(a.map)
 held={'ACH-000524','ACH-000696','ACH-001630','ACH-001632'}
 d=build_legacy_cancer_proxy(a.score,a.reactome,modelmap,heldout_models=held,max_genes=2000)
 policy=CancerOnlyPolicy(d['genes'],d['features'],d['surrogate'].repair_mask,seed=20260926)
 history=policy.train(d['surrogate'],a.episodes,learning_rate=.01)
 out={'scope':'cancer-only monogenic surrogate demonstration, no normal reward and no independent pair/triple validation','development_models':len(d['development_models']),'actions':d['repair_action_genes'],'episodes':a.episodes,'seed':20260926,
      'first_50_mean_reward':float(np.mean([r for _,r in history[:50]])),'last_50_mean_reward':float(np.mean([r for _,r in history[-50:]])),
      'unique_3gene_actions':len(set(t for t,r in history)),'final_policy_weight_l2':float(np.linalg.norm(policy.weights)),
      'heldout_results_not_accessed':True,'healthy_viability_status':'not_measured'}
 with open(a.output,'w') as f:json.dump(out,f,indent=2)
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
