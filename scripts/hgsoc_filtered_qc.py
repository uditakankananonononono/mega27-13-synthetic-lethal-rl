"""Development-only subtype-restricted monogenic fit, no interaction inference."""
import argparse,json,sys
sys.path.insert(0,'src')
from slrl.development import build_legacy_cancer_proxy
from slrl.sanger import model_name_map
p=argparse.ArgumentParser()
for n in ('score','reactome','map','identity','output'):p.add_argument('--'+n,required=True)
a=p.parse_args()
j=json.load(open(a.identity));allowed={x['model_id'] for x in j['models'] if x['explicit_hgsoc'] and x['exact_cellosaurus_matches']==1}
held={'ACH-000524','ACH-000696','ACH-001630','ACH-001632'}
d=build_legacy_cancer_proxy(a.score,a.reactome,model_name_map(a.map),heldout_models=held,max_genes=2000,allowed_models=allowed)
out={'scope':'small 2019 Project SCORE HGSOC-identity-restricted MONOGENIC development fit, no pair/triple or normal viability training','source_identity':'https://api.cellosaurus.org/','explicit_hgsoc_total':len(allowed),'development_model_ids':d['development_models'],'heldout_explicit_hgsoc_ids':sorted(held&allowed),'genes':len(d['genes']),'repair_action_genes':d['repair_action_genes'],'network_edges':d['network_edges'],'healthy_viability':'not measured','higher_order_effects':'not identified from these data'}
with open(a.output,'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
