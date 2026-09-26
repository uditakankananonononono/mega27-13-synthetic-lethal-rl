"""Held-out GSE154112 guide-count QC. Counts are NOT direct viability.

Do not load this module's real-data analysis outputs into simulator or policy training.
"""
from collections import defaultdict
import math
import numpy as np

TRIPLE_COLUMNS = ('Plasmid','Cell_D9','Cell_D15_rep1','Cell_D26_rep1','Cell_D15_rep2','Cell_D26_rep2')

def parse_sheet(path, sheet_name='3-way Ovarian cancer'):
    import openpyxl
    wb=openpyxl.load_workbook(path,read_only=True,data_only=True)
    sheet=wb[sheet_name]
    it=sheet.iter_rows(values_only=True)
    next(it)  # title row
    header=next(it)
    labels={str(v).strip():i for i,v in enumerate(header) if v is not None}
    if not set(TRIPLE_COLUMNS).issubset(labels):
        raise ValueError('incorrect assay schema')
    for row in it:
        if not row[0]: continue
        targets=tuple(str(v).rsplit('_',1)[0] for v in row[1:4])
        vals={k:row[labels[k]] for k in TRIPLE_COLUMNS}
        if any(v is None or not isinstance(v,(int,float)) or not math.isfinite(v) or v < 0 for v in vals.values()):
            continue
        yield targets,vals

def fold_change(values, baseline='Cell_D9', endpoint='Cell_D26', pseudo_count=1.):
    """Log2 endpoint/baseline count-per-million; no absolute cell viability inference."""
    if pseudo_count <= 0:raise ValueError('positive pseudocount required')
    return np.array([math.log2((values[f'{endpoint}_rep{rep}']+pseudo_count)/(values[baseline]+pseudo_count)) for rep in (1,2)])

def guide_family(name):
    return 'CTRL' if name.startswith('dummyguide') else name

def summarize_replicates(records):
    """Median per biological replicate across guide constructs, paired with data-QC counts."""
    grouped=defaultdict(list)
    for targets,values in records:
        genes=tuple(sorted(guide_family(g) for g in targets))
        grouped[genes].append(fold_change(values))
    out={}
    for genes,reps in grouped.items():
        x=np.array(reps)
        out[genes]={'guide_constructs':len(x),'median_log2fc_rep1':float(np.median(x[:,0])),
                    'median_log2fc_rep2':float(np.median(x[:,1])),
                    'replicate_disagreement':float(abs(np.median(x[:,0])-np.median(x[:,1])))}
    return out
