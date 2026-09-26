"""Minimal sequential policy-gradient search baseline, trained ONLY on an explicit surrogate.

Synthetic demonstration only until real training/holdout calibration exists. Linear scores
are intentionally transparent; the registered comparison must defeat non-RL baselines.
"""
from dataclasses import dataclass
import numpy as np

@dataclass
class Policy:
    features: np.ndarray  # one row per eligible gene, context-dependent features frozen before external results
    weights: np.ndarray
    repair_mask: np.ndarray
    def __post_init__(self):
        self.features = np.asarray(self.features, dtype=float)
        self.weights = np.asarray(self.weights, dtype=float)
        self.repair_mask = np.asarray(self.repair_mask, dtype=bool)
        if self.features.ndim != 2 or self.features.shape[0] != len(self.repair_mask) or self.features.shape[1] != len(self.weights):
            raise ValueError('feature/mask/weight dimension mismatch')
        if not np.all(np.isfinite(self.features)) or not np.all(np.isfinite(self.weights)):
            raise ValueError('nonfinite features')

    def episode(self, ctx, rng, length=3, known_pairs=frozenset()):
        if length not in (2,3): raise ValueError('only pair/triple search')
        selected, grads = [], []
        for _ in range(length):
            legal = np.flatnonzero(self.repair_mask)
            legal = [int(i) for i in legal if i not in selected and
                     all(tuple(sorted((i,j))) not in known_pairs for j in selected)]
            if not legal: raise ValueError('not enough legal genes')
            logits = self.features[legal] @ self.weights
            exps = np.exp(logits - max(logits)); probs = exps / exps.sum()
            choice = int(rng.choice(len(legal), p=probs))
            grads.append(self.features[legal[choice]] - probs @ self.features[legal])
            selected.append(legal[choice])
        perturbation = tuple(sorted(selected))
        return perturbation, float(ctx.reward(perturbation)), np.sum(grads, axis=0)

def train(policy, ctx, episodes, seed=0, learning_rate=0.02, gradient_clip=5.0):
    """REINFORCE with running reward baseline; every outcome is a SIMULATOR call."""
    rng = np.random.default_rng(seed)
    baseline = 0.
    history = []
    for t in range(episodes):
        genes, reward, gradient = policy.episode(ctx, rng)
        advantage = reward - baseline
        step = np.clip(advantage * gradient, -gradient_clip, gradient_clip)
        policy.weights += learning_rate * step
        baseline = .95 * baseline + .05 * reward if t else reward
        history.append((genes, reward))
    return history
