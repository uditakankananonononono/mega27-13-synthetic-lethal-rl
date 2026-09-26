"""Sparse biological network integrity checks; no invented biological edges."""
import numpy as np

def graph_from_edges(genes, edges, repair_genes):
    """Preserves gene order and source edge labels, checks that selected repair genes exist."""
    genes=tuple(genes); index={g:i for i,g in enumerate(genes)}
    if len(index)!=len(genes):raise ValueError('duplicate genes')
    repair=set(repair_genes)
    if not repair.issubset(index):raise ValueError('unmapped repair genes')
    graph=[set() for _ in genes]
    seen=set()
    for a,b in edges:
        if a==b or a not in index or b not in index:continue
        pair=tuple(sorted((a,b)))
        if pair in seen:continue
        seen.add(pair)
        graph[index[a]].add(index[b]);graph[index[b]].add(index[a])
    return graph,np.array([g in repair for g in genes],dtype=bool)

def degree_features(graph, repair_mask):
    """Development-only static structure features, no validation assay data."""
    n=len(graph)
    if len(repair_mask)!=n:raise ValueError('mask size')
    deg=np.array([len(s) for s in graph],float)
    own=np.array([sum(repair_mask[j] for j in s) for s in graph],float)
    return np.column_stack((deg/max(1.,deg.max(initial=0)),own/max(1.,own.max(initial=0)),np.asarray(repair_mask,float)))
