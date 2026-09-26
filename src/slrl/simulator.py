"""Research scaffold: a graph-conditioned surrogate, never empirical viability evidence."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Context:
    name: str
    cancer: bool
    single_loss: np.ndarray
    pair_excess: np.ndarray
    triple_excess: dict
    uncertainty: np.ndarray

    def validate(self):
        n = len(self.single_loss)
        if n < 3 or self.pair_excess.shape != (n, n) or self.uncertainty.shape != (n,):
            raise ValueError('inconsistent gene dimensions')
        if not np.allclose(self.pair_excess, self.pair_excess.T) or np.any(np.diag(self.pair_excess)):
            raise ValueError('pair effects must be symmetric, with zero diagonal')
        if np.any(self.single_loss < 0) or np.any(self.uncertainty < 0):
            raise ValueError('negative losses or uncertainties')
        for genes, effect in self.triple_excess.items():
            if len(genes) != 3 or len(set(genes)) != 3 or any(i < 0 or i >= n for i in genes) or not np.isfinite(effect):
                raise ValueError('invalid triple')

    def viability(self, genes):
        """Multiplicative log-loss surrogate; supplied interaction coefficients are NOT inferred from single knockouts."""
        self.validate()
        ids = tuple(sorted(genes))
        if len(ids) != len(set(ids)) or len(ids) > 3 or any(i < 0 or i >= len(self.single_loss) for i in ids):
            raise ValueError('invalid perturbation')
        loss = sum(self.single_loss[i] for i in ids)
        loss += sum(self.pair_excess[i, j] for ix, i in enumerate(ids) for j in ids[ix + 1:])
        if len(ids) == 3:
            loss += self.triple_excess.get(ids, 0.)
        return float(np.exp(-max(0., loss)))

@dataclass(frozen=True)
class DualContext:
    cancer: Context
    healthy: Context
    def __post_init__(self):
        self.cancer.validate(); self.healthy.validate()
        if len(self.cancer.single_loss) != len(self.healthy.single_loss):
            raise ValueError('gene-space mismatch')

    def reward(self, genes, uncertainty_penalty=0.2, essentiality_penalty=0.5):
        ids = tuple(sorted(genes))
        cancer_loss = 1. - self.cancer.viability(ids)
        healthy_loss = 1. - self.healthy.viability(ids)
        uncertainty = sum(self.cancer.uncertainty[i] + self.healthy.uncertainty[i] for i in ids)
        single_penalty = sum(max(0., 1. - self.cancer.viability((i,)) - 0.5) for i in ids)
        return cancer_loss - healthy_loss - uncertainty_penalty * uncertainty - essentiality_penalty * single_penalty
