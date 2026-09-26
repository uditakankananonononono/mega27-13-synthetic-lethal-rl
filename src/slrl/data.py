"""Load publicly released single-gene screens without mixing external pair/triple outcomes."""
import csv
import hashlib
import numpy as np

class IntegrityError(ValueError):pass

def check_md5(path, expected):
    d=hashlib.md5()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):d.update(chunk)
    if d.hexdigest().lower()!=expected.lower():raise IntegrityError('checksum mismatch')
    return d.hexdigest()

def read_gene_effect(path, model_ids, genes, min_gene_coverage=.8):
    """Rows=models, columns=gene symbols/IDs. Chronos effect convention is negative=dependent.

    Caller must choose a release and verify checksum/terms first. No result imputation across test lines.
    """
    model_ids=set(model_ids); genes=list(genes)
    if len(genes)<1 or len(set(genes))!=len(genes):raise ValueError('nonempty unique genes')
    with open(path,encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        model_column=reader.fieldnames[0]
        def cols(g):return [c for c in reader.fieldnames[1:] if c==g or c.startswith(g+' (')]
        idx={g:cols(g) for g in genes}
        if any(len(v)!=1 for v in idx.values()):raise ValueError('missing or ambiguous gene labels')
        mat={}
        for row in reader:
            model=row[model_column]
            if model not in model_ids:continue
            arr=np.array([float(row[idx[g][0]]) if row[idx[g][0]] not in ('','NA') else np.nan for g in genes])
            if np.isfinite(arr).mean()>=min_gene_coverage:mat[model]=arr
    return mat

def split_models(models, heldout, disjoint=True):
    models=set(models); heldout=set(heldout)
    if disjoint and not heldout.issubset(models):raise ValueError('holdout model absent')
    return sorted(models-heldout),sorted(heldout)
