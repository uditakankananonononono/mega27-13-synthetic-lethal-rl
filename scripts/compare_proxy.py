"""Matched-budget cancer-only same-surrogate sanity check, not external discovery."""
import argparse,json,sys
import numpy as np
sys.path.insert(0,'src')
from slrl.development import build_legacy_cancer_proxy
from slrl.sanger import model_name_map
from slrl.proxy_policy import CancerOnlyPolicy
from slrl.novelty import load_synlethdb2020

def score(s,ids):
 out=s.predict(ids)
 return 1-out['predicted_cancer_viability_proxy']-.2*out['uncertainty']

def main():
 p=argparse.ArgumentParser()
 for flag in ('score','reactome','map','known-pairs','output'):p.add_argument('--'+flag,required=True)
 a=p.parse_args();d=build_legacy_cancer_proxy(a.score,a.reactome,model_name_map(a.map),heldout_models={'ACH-000524','ACH-000696','ACH-001630','ACH-001632'},max_genes=2000)
 eligible=np.flatnonzero(d['surrogate'].repair_mask); names=d['genes']
 all_known,_,_=load_synlethdb2020(a.known_pairs)
 eligible_names={names[i] for i in eligible}
 known={pair for pair in all_known if pair[0] in eligible_names and pair[1] in eligible_names}
 def legal(indices):
  return all(tuple(sorted((names[int(a)],names[int(b)]))) not in known for a,b in ((indices[0],indices[1]),(indices[0],indices[2]),(indices[1],indices[2])))
 results=[]
 for seed in range(10):
  # 200 sampled training surrogate calls and 100 evaluation calls, each with eligible novelty-masked triples.
  policy=CancerOnlyPolicy(names,d['features'],d['surrogate'].repair_mask,known_pairs=known,seed=seed)
  policy.train(d['surrogate'],200)
  proposals=[policy.episode(d['surrogate'])[0] for _ in range(100)]
  policy_best=max(score(d['surrogate'],tuple(names.index(g) for g in combo)) for combo in proposals)
  rng=np.random.default_rng(seed);random_actions=[]
  while len(random_actions)<300:
   combo=tuple(sorted(map(int,rng.choice(eligible,3,replace=False))))
   if legal(combo):random_actions.append(combo)
  random_best=max(score(d['surrogate'],c) for c in random_actions)
  results.append({'seed':seed,'policy_best_simulator_reward':policy_best,'random_best_simulator_reward':random_best,'policy_surrogate_calls':300,'random_surrogate_calls':300})
 out={'scope':'same-surrogate reward comparison, fully circular and without external outcomes','known_excluded_pairs_in_action_space':len(known),'results':results,'policy_wins':sum(r['policy_best_simulator_reward']>r['random_best_simulator_reward'] for r in results),'no_independent_validation':True,'normal_viability_not_measured':True}
 with open(a.output,'w') as f:json.dump(out,f,indent=2)
 print(json.dumps({'policy_wins':out['policy_wins'],'mean_policy_best':float(np.mean([r['policy_best_simulator_reward'] for r in results])),'mean_random_best':float(np.mean([r['random_best_simulator_reward'] for r in results]))},indent=2))
if __name__=='__main__':main()
