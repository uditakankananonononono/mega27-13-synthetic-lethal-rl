"""Openly incomplete cancer-only policy when no healthy perturbation comparator exists.

It must not be called the owner's requested selective-viability RL agent.
"""
import numpy as np

class CancerOnlyPolicy:
    def __init__(self,genes,features,repair_mask,known_pairs=frozenset(),seed=0):
        self.genes=tuple(genes);self.features=np.asarray(features,float)
        self.mask=np.asarray(repair_mask,bool);self.known_pairs=set(known_pairs)
        if self.features.shape[0]!=len(self.genes) or len(self.mask)!=len(self.genes):raise ValueError('dimension mismatch')
        self.weights=np.zeros(self.features.shape[1],float);self.rng=np.random.default_rng(seed)
    def _eligible(self,selected):
        return [i for i in np.flatnonzero(self.mask) if i not in selected and
                all(tuple(sorted((self.genes[int(i)],self.genes[j]))) not in self.known_pairs for j in selected)]
    def episode(self,surrogate,length=3):
        if length not in (2,3):raise ValueError('pair or triple')
        selected=[];grads=[]
        for _ in range(length):
            eligible=self._eligible(selected)
            if not eligible:raise ValueError('no eligible action')
            logits=self.features[eligible] @ self.weights
            exps=np.exp(logits-logits.max());probs=exps/exps.sum()
            chosen=int(self.rng.choice(len(eligible),p=probs))
            grads.append(self.features[eligible[chosen]]-probs@self.features[eligible])
            selected.append(int(eligible[chosen]))
        outcome=surrogate.predict(selected)
        # Cancer-only proxy deliberately lacks a healthy preservation reward.
        reward=1-outcome['predicted_cancer_viability_proxy']-.2*outcome['uncertainty']
        return tuple(sorted(self.genes[i] for i in selected)),reward,np.sum(grads,axis=0),outcome
    def train(self,surrogate,episodes,learning_rate=.01):
        baseline=0;history=[]
        for t in range(episodes):
            names,r,grad,_=self.episode(surrogate)
            self.weights+=learning_rate*np.clip((r-baseline)*grad,-5.,5.)
            baseline=r if t==0 else .95*baseline+.05*r
            history.append((names,float(r)))
        return history
