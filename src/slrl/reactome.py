"""Version-pinned Reactome pathway association loader; CC0 source data."""
import csv
from collections import defaultdict

def load_ncbi_pathways(path):
    pathways=defaultdict(set);names={};mapping=set()
    with open(path,encoding='utf-8') as f:
        for row in csv.reader(f,delimiter='\t'):
            if len(row)<6 or row[5]!='Homo sapiens' or not row[0].isdigit():continue
            gene,accession=row[0],row[1]
            pathways[accession].add(gene)
            names[accession]=row[3].strip();mapping.add(gene)
    return pathways,names,mapping

def repair_members(pathways,names):
    """One named umbrella pathway; repair membership is a tiny portion of full network."""
    hits=[key for key,name in names.items() if name=='DNA Repair' and key.startswith('R-HSA-')]
    if len(hits)!=1:raise ValueError('ambiguous/missing human DNA Repair root')
    return pathways[hits[0]]

def bounded_copathway_edges(pathways,genes,max_pathway_size=150):
    """Do not make an all-to-all edge from broad umbrella pathways."""
    genes=set(genes);edges=set()
    for members in pathways.values():
        common=sorted(members&genes)
        if not 2<=len(common)<=max_pathway_size:continue
        for i,a in enumerate(common):
            edges.update((a,b) for b in common[i+1:])
    return edges
