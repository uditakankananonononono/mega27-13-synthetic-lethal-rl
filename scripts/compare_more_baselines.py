"""Additional 300-call same-surrogate search controls, never biological validation."""
import argparse,json,sys
import numpy as np
sys.path.insert(0,'src')
from slrl.development import build_legacy_cancer_proxy
from slrl.sanger import model_name_map
from slrl.proxy_policy import CancerOnlyPolicy
from slrl.novelty import load_synlethdb2020

def run():
 p=argparse.ArgumentParser()
 for x in ('score','reactome','map','known-pairs','output'):p.add_argument('--'+x,required=True)
 a=p.parse_args();d=build_legacy_cancer_proxy(a.score,a.reactome,model_name_map(a.map),heldout_models={'ACH-000524','ACH-000696','ACH-001630','ACH-001632'},max_genes=2000)
 s=d['surrogate'];names=d['genes'];eligible=np.flatnonzero(s.repair_mask);name_to_idx={n:i for i,n in enumerate(names)}
 known_all,_,_=load_synlethdb2020(a.known_pairs);eligible_names={names[i] for i in eligible};known={x for x in known_all if set(x)<=eligible_names}
 def legal(t):return len(set(t))==3 and all(tuple(sorted((names[int(t[i])],names[int(t[j])]))) not in known for i,j in ((0,1),(0,2),(1,2)))
 def reward(t):
  out=s.predict(t);return 1-out['predicted_cancer_viability_proxy']-.2*out['uncertainty']
 def sample(rng,mode,leader=None):
  for _ in range(50000):
   if mode=='random':t=rng.choice(eligible,3,replace=False)
   elif mode=='uncertainty':
    # Soft exploration favors low monogenic uncertainty; avoids deterministic repeats.
    w=np.exp(-s.uncertainty[eligible]*5);w/=w.sum();t=rng.choice(eligible,3,replace=False,p=w)
   elif mode=='network':
    first=int(rng.choice(eligible));neighbor=list(set(s.adjacency[first])&set(eligible));
    second=int(rng.choice(neighbor if neighbor else eligible));neighbor2=list((set(s.adjacency[first])|set(s.adjacency[second]))&set(eligible));third=int(rng.choice(neighbor2 if neighbor2 else eligible));t=(first,second,third)
   else:
    t=list(leader);t[int(rng.integers(3))]=int(rng.choice(eligible))
   t=tuple(sorted(map(int,t)))
   if legal(t):return t
  raise RuntimeError('masked action sampler exhausted')
 result=[]
 for seed in range(10):
  records={}
  rl=CancerOnlyPolicy(names,d['features'],s.repair_mask,known_pairs=known,seed=seed)
  history=rl.train(s,200);evals=[rl.episode(s) for _ in range(100)]
  records['rl']={'best':max([r for _,r in history]+[r for _,r,_,_ in evals]),'unique':len({n for n,_ in history}|{n for n,_,_,_ in evals})}
  for method in ('random','greedy','beam','network','uncertainty'):
   rng=np.random.default_rng(seed);scores={};top=[]
   for call in range(300):
    if method in ('greedy','beam') and call>=30:
     if method=='greedy':leader=max(scores,key=scores.get)
     else:
      leaders=sorted(scores,key=scores.get,reverse=True)[:5];leader=leaders[(call-30)%len(leaders)]
     t=sample(rng,method,leader)
    else:t=sample(rng,'random' if method in ('greedy','beam') else method)
    # Duplicate proposals still spend the matching evaluation budget.
    scores[t]=reward(t)
   records[method]={'best':max(scores.values()),'unique':len(scores)}
  result.append({'seed':seed,'methods':records})
 methods=result[0]['methods'];summary={k:{'mean_best':float(np.mean([r['methods'][k]['best'] for r in result])),'mean_unique':float(np.mean([r['methods'][k]['unique'] for r in result])),'wins_vs_rl':sum(r['methods'][k]['best']>r['methods']['rl']['best'] for r in result)} for k in methods}
 out={'scope':'cancer-only 2019 monogenic prior, evaluated by the same arbitrary surrogate; 300 calls/method/seed, circular, no external outcomes','network_control':'neighbor-biased triples; pathway adjacency is prior co-membership, not measured interaction','uncertainty_control':'soft low-uncertainty prior sampling','greedy_control':'30 random starts, then single-gene mutation of best evaluated triple','beam_control':'30 random starts, then rotate mutations among five top evaluated triples','known_pairs_masked':len(known),'seeds':result,'summary':summary,'healthy_viability':'not measured'}
 with open(a.output,'w') as f:json.dump(out,f,indent=2)
 print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
