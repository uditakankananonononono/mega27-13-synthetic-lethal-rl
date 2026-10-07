"""Power for the frozen secondary-track test: Mann-Whitney, 0.3 median shift. Simulation, no data."""
import numpy as np, json
from scipy.stats import mannwhitneyu
rng = np.random.default_rng(0)
# per-pair p must reach about BH q<0.1 across ~72k pairs: use p < 1e-4 as a conservative stand-in
out = {}
for sd in (0.3, 0.5):
    for na in (3, 6, 10, 20):
        nu = 25; hit = 0; N = 2000
        for _ in range(N):
            x = rng.normal(-0.3, sd, na); y = rng.normal(0, sd, nu)
            hit += mannwhitneyu(x, y, alternative='two-sided').pvalue < 1e-4
        out[f'sd{sd}_altered{na}'] = hit / N
print(json.dumps(out, indent=1))
json.dump(out, open('results/secondary-track-power.json', 'w'), indent=1)
