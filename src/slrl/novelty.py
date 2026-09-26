"""Conservative candidate exclusion registry. A miss is not proof of global novelty."""
import csv

def load_synlethdb2020(path):
    """Versioned human SL registry, all source categories; no use as truth labels."""
    pairs=set(); source_counts={}; row_count=0
    with open(path,encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f):
            row_count += 1
            a,b=row['gene_a.identifier'],row['gene_b.identifier']
            if a and b and a != b: pairs.add(tuple(sorted((a,b))))
            source=row['SL.source'];source_counts[source]=source_counts.get(source,0)+1
    return pairs,source_counts,row_count

def novelty_status(genes, registries):
    """Known pair in any registry -> ineligible. Otherwise only 'not_found_in_searched_sources'."""
    a=tuple(sorted(map(str,genes)))
    if len(a)!=2 or a[0]==a[1]: raise ValueError('pair required')
    return ('already_recorded' if any(a in reg for reg in registries)
            else 'not_found_in_searched_sources')
