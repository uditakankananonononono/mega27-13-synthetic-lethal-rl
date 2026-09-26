"""Matched-budget simulator-only sanity check; not external discovery evidence."""
import argparse,json,sys
import numpy as np
sys.path.insert(0,'src')
from slrl.development import build_legacy_cancer_proxy
from slrl.sanger import model_name_map
from slrl.proxy_policy import CancerOnlyPolicy

def score(s,ids):
 out=s.predict(ids)
 return 1-out['predicted_cancer_viability_proxy']-.2*out['uncertainty']

def main():
 p=argparse.ArgumentParser()
 for flag in ('score','reactome','map','output'):p.add_argument('--'+flag,required=True)
 a=p.parse_args(); d=build_legacy_cancer_proxy(a.score,a.reactome,model_name_map(a.map),heldout_models={'ACH-000524','ACH-000696','ACH-001630','ACH-001632'},max_genes=2000)
 eligible=np.flatnonzero(d['surrogate'].repair_mask)
 results=[]
 for seed in range(10):
  # 200 sampled training surrogate calls, then 100 candidate evaluations, for each policy.
  policy=CancerOnlyPolicy(d['genes'],d['features'],d['surrogate'].repair_mask,seed=seed)
  policy.train(d['surrogate'],200)
  names=[]
  for _ in range(100):names.append(policy.episode(d['surrogate'])[0])
  policy_best=max(score(d['surrogate'],tuple(d['genes'].index(g) for g in combo)) for combo in names)
  rng=np.random.default_rng(seed)
  random_names=[tuple(sorted(map(int,rng.choice(eligible,3,replace=False)))) for _ in range(300)]
  random_best=max(score(d['surrogate'],c) for c in random_names)
  results.append({'seed':seed,'policy_best_simulator_reward':policy_best,'random_best_simulator_reward':random_best,'policy_surrogate_calls':300,'random_surrogate_calls':300})
 out={'scope':'same-surrogate reward comparison, fully circular and without external outcomes','results':results,'policy_wins':sum(r['policy_best_simulator_reward']>r['random_best_simulator_reward'] for r in results),'no_independent_validation':True,'normal_viability_not_measured':True}
 with open(a.output,'w') as f:json.dump(out,f,indent=2)
 print(json.dumps({'policy_wins':out['policy_wins'],'mean_policy_best':np.mean([r['policy_best_simulator_reward'] for r in results]),'mean_random_best':np.mean([r['random_best_simulator_reward'] for r in results])},indent=2))
if __name__=='__main__':main()
