"""Post-outcome empirical shift diagnostic for GSE154112, not assay power or hits.

An injected shift applies to all D26 triple constructs in both biological replicates.
It is not a simulation of gene editing, biological variance or cell viability.
"""
import argparse
import json
from collections import defaultdict
from itertools import combinations, permutations
import sys
import numpy as np
sys.path.insert(0, 'src')
from slrl.assay import fold_change, guide_family, parse_sheet


def summarize_shift_thresholds(records, shifts=(0., .5, 1., 2., 4.)):
    """Contrast is linear in a uniform triple-only log2-count shift.

    Positive thresholds quantify how much an existing triple contrast must be
    moved before the descriptive all-layouts/both-replicates sign gate passes.
    """
    per_triple = []
    for r in records:
        effects = np.asarray(r['layout_contrasts'], dtype=float)
        if effects.ndim != 2 or effects.shape[1] != 2 or not len(effects) or not np.isfinite(effects).all():
            raise ValueError('expected finite position-by-two-replicate contrasts')
        # strict negativity: equality at the boundary does not pass
        threshold = float(np.max(effects))
        mean_threshold = float(np.max(np.mean(effects, axis=0)))
        per_triple.append({'genes': list(r['genes']), 'layouts': len(effects),
                           'uniform_shift_needed_strictly_more_than_log2': max(0., threshold),
                           'mean_layout_shift_needed_strictly_more_than_log2': max(0., mean_threshold),
                           'already_all_layouts_negative': bool(np.all(effects < 0)),
                           'already_mean_layout_negative_both_reps': bool(np.all(np.mean(effects,axis=0) < 0))})
    return {'triples': per_triple, 'n': len(per_triple),
            'shift_grid': {str(s): {
                'all_layouts_negative_both_reps': sum(float(r['uniform_shift_needed_strictly_more_than_log2']) < s if s else r['already_all_layouts_negative'] for r in per_triple),
                'mean_layout_negative_both_reps': sum(float(r['mean_layout_shift_needed_strictly_more_than_log2']) < s if s else r['already_mean_layout_negative_both_reps'] for r in per_triple)} for s in shifts},
            'median_shift_threshold_log2': float(np.median([r['uniform_shift_needed_strictly_more_than_log2'] for r in per_triple]))}


def run(path):
    grouped = defaultdict(list)
    for guides, counts in parse_sheet(path):
        fam = tuple(guide_family(g) for g in guides)
        if len(set(g for g in fam if g != 'CTRL')) != sum(g != 'CTRL' for g in fam):
            continue
        grouped[fam].append(fold_change(counts))
    medians = {k: np.median(v, axis=0) for k, v in grouped.items()}
    genes = sorted(set(g for fam in medians for g in fam if g != 'CTRL'))
    records = []
    for triple in combinations(genes, 3):
        layouts = []
        for layout in permutations(triple):
            contrast = np.zeros(2)
            for mask in range(8):
                configuration = tuple(layout[i] if mask & (1 << i) else 'CTRL' for i in range(3))
                if configuration not in medians:
                    break
                contrast += (-1)**(3-mask.bit_count()) * medians[configuration]
            else:
                layouts.append(contrast.tolist())
        if layouts:
            records.append({'genes': triple, 'layout_contrasts': layouts})
    return summarize_shift_thresholds(records)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--workbook', required=True); p.add_argument('--output', required=True)
    a = p.parse_args(); out = run(a.workbook)
    out.update(source='GSE154112', source_url='https://ftp.ncbi.nlm.nih.gov/geo/series/GSE154nnn/GSE154112/suppl/',
               scope='post-outcome empirical uniform triple-only log2-CPM shift sensitivity; not biological power, not viability or hit discovery')
    with open(a.output, 'w') as f: json.dump(out, f, indent=2)
    print(json.dumps({k: v for k, v in out.items() if k != 'triples'}, indent=2))
