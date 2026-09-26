"""Exploratory, single-model third-order depletion contrasts.

No direct viability or cancer-selectivity inference. Do not train the discovery policy here.
"""
from collections import defaultdict
from itertools import combinations
import numpy as np
from .assay import parse_sheet,fold_change,guide_family


def collect(path):
    """Keep distinct-gene sets, 0..3 genes, median over guide constructs per replicate."""
    groups=defaultdict(list)
    ignored=0
    for guides,counts in parse_sheet(path):
        targets=tuple(sorted(g for g in (guide_family(x) for x in guides) if g!='CTRL'))
        if len(set(targets))!=len(targets):
            ignored+=1;continue
        groups[targets].append(fold_change(counts))
    return {k:np.asarray(v) for k,v in groups.items()},ignored

def third_order_from_groups(groups, triple, bootstrap=1000, seed=20260926):
    """Inclusion-exclusion log2 depletion against within-library zero-gene control."""
    triple=tuple(sorted(triple))
    if len(triple)!=3 or len(set(triple))!=3:raise ValueError('three distinct genes required')
    subsets=[()] + [tuple(x) for n in (1,2,3) for x in combinations(triple,n)]
    if any(k not in groups or len(groups[k])<4 for k in subsets):return None
    signs={():-1}
    for k in subsets[1:]:signs[k]=(-1)**(3-len(k))
    observed=sum(signs[k]*np.median(groups[k],axis=0) for k in subsets)
    if bootstrap<1:raise ValueError('positive bootstrap count')
    rng=np.random.default_rng(seed)
    boot=np.zeros((bootstrap,2))
    for k in subsets:
        v=groups[k]
        ix=rng.integers(0,len(v),size=(bootstrap,len(v)))
        boot+=signs[k]*np.median(v[ix,:],axis=1)
    return {'genes':triple,'guide_counts':{','.join(k) if k else 'CTRL':len(groups[k]) for k in subsets},
            'replicate_log2_excess':[float(x) for x in observed],
            'mean_log2_excess':float(np.mean(observed)),
            'guide_bootstrap_ci_95':tuple(float(x) for x in np.percentile(boot.mean(axis=1),[2.5,97.5])),
            'replicate_direction_agrees':bool(np.all(observed<0) or np.all(observed>0)),
            'guide_bootstrap_two_sided_p':float(min(1.,2*min((1+np.sum(boot.mean(axis=1)>=0))/(bootstrap+1),
                                                                  (1+np.sum(boot.mean(axis=1)<=0))/(bootstrap+1))))}
