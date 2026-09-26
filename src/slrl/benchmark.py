"""Preoutcome benchmark scaffolding. Does not establish empirical hit labels."""
import math
import numpy as np

def average_precision_at_k(order, positives, k):
    """Ranked precision-at-k (NOT AP); positive set must come from held-out source."""
    if k<1:raise ValueError('positive k')
    order=list(order)
    if len(order)!=len(set(order)):raise ValueError('duplicate nominations')
    return sum(item in positives for item in order[:k])/min(k,len(order)) if order else float('nan')

def matched_budget_permutation(model_scores, baseline_scores, n_permutations=9999, seed=0):
    """One-sided paired sign-flip test on held-out context-level scores; >=2 independent contexts."""
    a,b=np.asarray(model_scores,float),np.asarray(baseline_scores,float)
    if a.shape!=b.shape or a.ndim!=1 or len(a)<2 or not np.all(np.isfinite(a-b)):
        raise ValueError('paired independent context scores required')
    diff=a-b; obs=diff.mean(); rng=np.random.default_rng(seed)
    signs=rng.choice([-1,1],size=(n_permutations,len(diff)))
    null=(signs*diff).mean(axis=1)
    return {'mean_delta':float(obs),'one_sided_p':float((1+np.sum(null>=obs))/(n_permutations+1)),
            'n_independent_contexts':len(diff)}

def benjamini_hochberg(pvalues):
    p=np.asarray(pvalues,float)
    if p.ndim!=1 or np.any(~np.isfinite(p)) or np.any((p<0)|(p>1)):raise ValueError('p in [0,1]')
    order=np.argsort(p,kind='stable');q=np.empty(len(p));prev=1.
    for rank in range(len(p)-1,-1,-1):
        ix=order[rank];prev=min(prev,p[ix]*len(p)/(rank+1));q[ix]=prev
    return q
