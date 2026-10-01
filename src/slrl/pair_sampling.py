"""Two-step pair sampler whose zero-score base is uniform over eligible edges."""
import numpy as np

def distribution(pairs, scores):
    """Orient each edge twice; first-node mass is sum of its edge weights.

    P(g)=sum incident exp(score)/[2 sum_edges exp(score)].
    P(edge|g)=exp(score)/sum incident exp(score).
    Summing both orientations gives P(edge)=exp(score)/sum_edges exp(score).
    """
    scores=np.asarray(scores,float)
    if len(pairs)!=len(scores) or not pairs or not np.isfinite(scores).all():raise ValueError('invalid pairs/scores')
    if len(set(tuple(sorted(p)) for p in pairs))!=len(pairs):raise ValueError('duplicate unordered edge')
    if any(len(p)!=2 or p[0]==p[1] for p in pairs):raise ValueError('invalid edge')
    weights=np.exp(scores-scores.max());genes=sorted({g for p in pairs for g in p})
    incident={g:np.asarray([i for i,p in enumerate(pairs) if g in p],int) for g in genes}
    totals=np.asarray([weights[incident[g]].sum() for g in genes]);first=totals/totals.sum()
    return genes,first,incident,weights

def sample(pairs,scores,rng):
    genes,first,incident,weights=distribution(pairs,scores)
    g=genes[int(rng.choice(len(genes),p=first))];ix=incident[g];p=weights[ix]/weights[ix].sum()
    i=int(rng.choice(ix,p=p));return i,g
