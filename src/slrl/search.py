"""Budget-matched discovery-search reference algorithms; no trained policy yet."""
import numpy as np

def candidates(n, repair_mask, excluded_pairs=frozenset()):
    """Mask excludes established pair hits but keeps possible triple-only combinations separately."""
    if len(repair_mask) != n:
        raise ValueError('gene mask mismatch')
    genes = np.flatnonzero(repair_mask)
    for ix, a in enumerate(genes):
        for b in genes[ix + 1:]:
            if (int(a), int(b)) not in excluded_pairs:
                yield (int(a), int(b))

def budgeted_random(context, gene_sets, budget, seed):
    pool = list(gene_sets)
    rng = np.random.default_rng(seed)
    ids = rng.choice(len(pool), size=min(budget, len(pool)), replace=False)
    return sorted(((pool[int(i)], context.reward(pool[int(i)])) for i in ids), key=lambda x: -x[1])

def budgeted_greedy(context, gene_sets, budget):
    """A reference with the same number of surrogate calls as random; no external-label access."""
    pool = list(gene_sets)
    ranked = sorted(((p, context.reward(p)) for p in pool[:budget]), key=lambda x: -x[1])
    return ranked
