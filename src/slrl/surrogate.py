"""A constrained, explicitly prior-driven prototype surrogate.

Single-gene dependency cannot determine higher-order effects. It is *not* a
trained cancer-vs-healthy simulator; healthy branch must be measured later.
"""
from dataclasses import dataclass
from itertools import combinations
import numpy as np

@dataclass
class PriorSurrogate:
    cancer_single: np.ndarray
    repair_mask: np.ndarray
    adjacency: tuple
    uncertainty: np.ndarray
    max_pair_prior: float=.1
    max_triple_prior: float=.05
    def __post_init__(self):
        n=len(self.cancer_single)
        if len(self.repair_mask)!=n or len(self.adjacency)!=n or len(self.uncertainty)!=n:raise ValueError('dimension mismatch')
        if np.any(~np.isfinite(self.cancer_single)) or np.any(self.uncertainty<0):raise ValueError('invalid inputs')
    def predict(self, genes):
        genes=tuple(sorted(genes))
        if len(genes) not in (1,2,3) or len(set(genes))!=len(genes) or not all(self.repair_mask[i] for i in genes):
            raise ValueError('only distinct repair-network genes')
        pairs=list(combinations(genes,2))
        edge_count=sum(b in self.adjacency[a] for a,b in pairs)
        # Prior is intentionally capped and inspectable; it is not empirical pair/triple fit.
        prior=min(self.max_pair_prior,.01*edge_count)
        if len(genes)==3:prior+=min(self.max_triple_prior,.005*edge_count)
        loss=sum(self.cancer_single[i] for i in genes)+prior
        uncertainty=sum(self.uncertainty[i] for i in genes)+len(pairs)*self.max_pair_prior
        if len(genes)==3:uncertainty+=self.max_triple_prior
        return {'predicted_cancer_viability_proxy':float(np.exp(-max(0,loss))),
                'uncertainty':float(uncertainty),'prior_interaction_loss':float(prior),
                'healthy_viability_status':'not_measured'}
