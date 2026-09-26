"""Map legacy Project SCORE Broad identifiers to cancer-model names; check subtype externally."""
import csv

def model_name_map(path):
    seen={}
    with open(path,encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f):
            model=row['broad_id'];name=row['canonical_ccle_name']
            if model in seen and seen[model]!=name:raise ValueError('ambiguous model name')
            seen[model]=name
    return seen

def ovarian_named_models(mapping,source_ids):
    return sorted((model,name) for model,name in mapping.items() if model in source_ids and name.endswith('_OVARY'))
