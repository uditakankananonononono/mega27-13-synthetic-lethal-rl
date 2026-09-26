"""Predeclared validation contrasts; q-values and assay controls belong in the experiment analysis."""
import math

def third_order_log_viability(measurements):
    """3-way interaction net of all main and pair effects; keys are frozensets of gene IDs."""
    genes = set().union(*measurements)
    if len(genes) != 3 or any(v <= 0 or not math.isfinite(v) for v in measurements.values()):
        raise ValueError('three genes and positive finite normalized viability required')
    a, b, c = sorted(genes)
    subsets = [frozenset(x) for x in ((a,), (b,), (c,), (a,b), (a,c), (b,c), (a,b,c))]
    if set(measurements) != set(subsets):
        raise ValueError('all seven nonempty subsets required; no imputation')
    log = {s: math.log(measurements[s]) for s in subsets}
    return log[frozenset((a,b,c))] - sum(log[frozenset(p)] for p in ((a,b),(a,c),(b,c))) + sum(log[frozenset((i,))] for i in (a,b,c))

def strict_triple_phenotype(measurements, survival=0.8, failure=0.3):
    third_order_log_viability(measurements)
    return (all(value >= survival for subset, value in measurements.items() if len(subset) < 3)
            and next(value for subset, value in measurements.items() if len(subset) == 3) <= failure)
