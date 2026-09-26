"""Development-only monogenic fit from legacy Project SCORE and Reactome.

The independent combinatorial GSE154112 data NEVER enter this builder.
"""
import csv
import numpy as np
from .calibration import normalize_dependency_matrix,shrink_gene_mean
from .reactome import load_ncbi_pathways,repair_members,bounded_copathway_edges
from .network import graph_from_edges,degree_features
from .surrogate import PriorSurrogate


def build_legacy_cancer_proxy(score_csv,reactome_tsv,model_map,heldout_models=frozenset(),max_genes=2000):
    if not 2000<=max_genes:raise ValueError('at least 2000 measured genes required')
    paths,names,mapped=load_ncbi_pathways(reactome_tsv)
    repair=repair_members(paths,names)
    with open(score_csv,encoding='utf-8-sig',newline='') as f:
        reader=csv.reader(f);header=next(reader)
        gene_cols=[]
        for i,g in enumerate(header[1:],1):
            if g.endswith(')') and ' (' in g:
                sym,entrez=g.rsplit(' (',1);entrez=entrez[:-1]
                if entrez in mapped:gene_cols.append((i,sym,entrez))
        repair_cols=[x for x in gene_cols if x[2] in repair]
        # deterministic fixed order: repair + next Entrez-numbered genes; duplicates removed
        chosen=[];seen=set()
        for item in repair_cols+gene_cols:
            if item[2] not in seen:
                chosen.append(item);seen.add(item[2])
                if len(chosen)==max_genes:break
        if len(chosen)<2000:raise ValueError('insufficient gene coverage')
        rows=[];ids=[]
        for row in reader:
            model=row[0]
            if model in heldout_models or model not in model_map or not model_map[model].endswith('_OVARY'):continue
            nums=[]
            for i,_,_ in chosen:
                try:nums.append(float(row[i]))
                except (ValueError,IndexError):nums.append(float('nan'))
            rows.append(nums);ids.append(model)
    if len(ids)<3:raise ValueError('insufficient ovarian training models')
    x,valid=normalize_dependency_matrix(rows)
    mean,uncertainty,counts=shrink_gene_mean(x)
    allowed=counts>=max(2,len(ids)//2)
    members=[x[2] for x in chosen]
    edges=bounded_copathway_edges(paths,members,max_pathway_size=80)
    graph,repair_mask=graph_from_edges(members,edges,repair & set(members))
    # Unmeasured genes never enter actions, and uncertainty remains high elsewhere.
    repair_mask &= allowed
    surrogate=PriorSurrogate(mean,repair_mask,tuple(graph),uncertainty)
    features=degree_features(graph,repair_mask)
    return {'surrogate':surrogate,'features':features,'genes':members,'symbols':[x[1] for x in chosen],
            'development_models':ids,'repair_action_genes':int(repair_mask.sum()),
            'network_edges':len(edges),'coverage':counts.tolist(),
            'note':'Legacy monogenic cancer-only proxy, no observed healthy viability or interaction training'}
