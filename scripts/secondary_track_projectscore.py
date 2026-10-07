"""Frozen secondary track on Project Score. See docs/SECONDARY-TRACK-DEVIATION-1.md. Hypotheses only."""
import csv, gzip, io, json, sys, zipfile, statistics as st
import numpy as np
from scipy.stats import mannwhitneyu
D = sys.argv[1]
models = list(csv.DictReader(gzip.open(f'{D}/model_list_latest.csv.gz', 'rt')))
by_name = {m['model_name'].upper(): m for m in models}
z = zipfile.ZipFile(f'{D}/ess.zip')
def mat(n):
    f = io.TextIOWrapper(z.open('EssentialityMatrices/' + n), encoding='utf8')
    r = csv.reader(f, delimiter='\t'); h = next(r)[1:]
    g, rows = [], []
    for row in r:
        g.append(row[0]); rows.append([float(x) if x not in ('', 'NA', 'NaN') else np.nan for x in row[1:]])
    return h, g, np.array(rows)
cols, genes, L = mat('01_corrected_logFCs.tsv')
_, g2, B = mat('04_binaryDepScores.tsv')
assert genes == g2
common = (np.nanmean(B, axis=1) >= 0.9)
ov = [i for i, c in enumerate(cols) if c.upper() in by_name and by_name[c.upper()]['tissue'] == 'Ovary']
ids = {i: by_name[cols[i].upper()]['model_id'] for i in ov}
hg = {i for i in ov if 'High Grade Ovarian Serous' in by_name[cols[i].upper()]['cancer_type_detail']}
alt = {k: set() for k in ['BRCA1', 'BRCA2', 'RB1', 'TP53', 'CCNE1']}
trunc = {'nonsense', 'frameshift', 'ess_splice'}
want = set(ids.values())
for r in csv.DictReader(gzip.open(f'{D}/mutations_all_latest.csv.gz', 'rt')):
    if r['model_id'] in want and r['gene_symbol'] in alt and r['coding'] == 't':
        if r['effect'] in trunc or (r['gene_symbol'] == 'TP53' and r['effect'] == 'missense'):
            alt[r['gene_symbol']].add(r['model_id'])
zc = zipfile.ZipFile(f'{D}/cnv_summary_20250207.zip')
for r in csv.DictReader(io.TextIOWrapper(zc.open('cnv_summary_20250207.csv'), encoding='utf8')):
    if r['symbol'] == 'CCNE1' and r['model_id'] in want and r['cn_category'] == 'Amplification':
        alt['CCNE1'].add(r['model_id'])
def bh(p):
    p = np.array(p); n = len(p); o = np.argsort(p); q = np.empty(n)
    c = np.minimum.accumulate((p[o] * n / (np.arange(n) + 1))[::-1])[::-1]; q[o] = np.minimum(c, 1); return q
def run(sel, label):
    out = []; info = {}
    for b, a in alt.items():
        A = [i for i in sel if ids[i] in a]; U = [i for i in sel if ids[i] not in a]
        info[b] = (len(A), len(U))
        if len(A) < 3 or len(U) < 3: continue
        for gi, g in enumerate(genes):
            x = L[gi, A]; y = L[gi, U]; x = x[~np.isnan(x)]; y = y[~np.isnan(y)]
            if len(x) < 3 or len(y) < 3: continue
            p = mannwhitneyu(x, y, alternative='two-sided').pvalue
            out.append([b, g, float(np.median(x) - np.median(y)), p, bool(common[gi])])
    if out:
        q = bh([o[3] for o in out])
        for o, qq in zip(out, q): o.append(float(qq))
    hits = [o for o in out if o[5] < 0.1 and o[2] <= -0.3 and not o[4]]
    return {'set': label, 'n_models': len(sel), 'altered_unaltered': info, 'tested_pairs': len(out),
            'hits': sorted(hits, key=lambda o: o[5])[:50], 'n_hits': len(hits), 'all': out}
res = [run(ov, 'ovary'), run(sorted(hg), 'hgsoc-annotated sensitivity')]
json.dump({'protocol': 'SECONDARY-TRACK-PROTOCOL + DEVIATION-1', 'cohort': 'Project Score only (no DepMap, no cross-cohort sign check)',
           'results': [{k: v for k, v in r.items() if k != 'all'} for r in res]}, open('results/secondary-track-projectscore.json', 'w'), indent=1)
with open('results/secondary-track-projectscore-all-pairs.tsv', 'w') as f:
    f.write('set\tbiomarker\tgene\tmedian_diff\tp\tcommon_essential\tq\n')
    for r in res:
        for o in r['all']: f.write(f"{r['set']}\t{o[0]}\t{o[1]}\t{o[2]:.4f}\t{o[3]:.3g}\t{int(o[4])}\t{o[5]:.3g}\n")
for r in res: print(r['set'], r['n_models'], r['altered_unaltered'], 'tested', r['tested_pairs'], 'hits', r['n_hits'], [(h[0], h[1], round(h[2], 2), round(h[5], 3)) for h in r['hits'][:10]])
