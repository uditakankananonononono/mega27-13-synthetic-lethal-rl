"""Derive a conservative project gate ledger from committed artifacts, not memory.

This is not a biological discovery test. Missing validation is never inferred from
absence of a file; it is an explicit current project status requiring fresh audit.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILES={
 'assay':'results/gse154112-exploratory-contrasts.json',
 'shift':'results/gse154112-position-injection-diagnostic.json',
 'proxy':'results/cancer-only-proxy-five-controls.json',
 'identity':'results/hgsoc-identity-filtered-monogenic-qc.json',
 'peo1':'results/peo1-guide-qc.json',
 'similarity':'results/peo1-sample-similarity-audit.json',
 'harle':'results/harle-category-benchmark.json',
 'harle_integrity':'results/harle-benchmark-integrity.json',
 'corrected':'results/harle-corrected-integrity.json',
 'peo1_mapping':'results/peo1-source-reconciliation.json',
}

def build(root=ROOT):
    d={k:json.loads((root/v).read_text()) for k,v in FILES.items()}
    sha={k:hashlib.sha256((root/v).read_bytes()).hexdigest() for k,v in FILES.items()}
    a,s,p,i,q,t=(d[k] for k in ('assay','shift','proxy','identity','peo1','similarity'))
    rows=a['rows']
    assert len(rows)==a['all_455_triples_evaluable']==s['n']==455
    assert a['source']=='GSE154112' and 'not cell viability' in a['outcome_type']
    assert sum(r['guide_bootstrap_bh_q']<0.05 for r in rows)==0
    assert s['shift_grid']['0.0']['all_layouts_negative_both_reps']==0
    assert all(s['shift_grid'][k]['all_layouts_negative_both_reps']<=s['shift_grid'][v]['all_layouts_negative_both_reps'] for k,v in zip(('0.0','0.5','1.0','2.0'),('0.5','1.0','2.0','4.0')))
    assert len(p['seeds'])==10 and all(v['methods']['greedy']['best']>v['methods']['rl']['best'] and v['methods']['beam']['best']>v['methods']['rl']['best'] for v in p['seeds'])
    assert p['healthy_viability']=='not measured' and i['healthy_viability']=='not measured'
    assert i['higher_order_effects']=='not identified from these data' and i['explicit_hgsoc_total']==10
    assert q['raw_rows']==t['all']['guide_rows']==119461 and q['accepted_rows']<=q['raw_rows']
    h=d['harle'];hi=d['harle_integrity'];hc=d['corrected'];pm=d['peo1_mapping']
    assert h['lines']==27 and h['seeds']==20 and len(h['trials'])==2700
    assert h['summary']['random']['mean_hits_60']>h['summary']['sequential_reinforce']['mean_hits_60']
    assert hi['table_s4_s5_label_mismatches']==[] and hi['all_traces_unique']
    assert hc['original_trials_reproduced_exactly']==2700 and hc['corrected_minus_random_hits60']<0
    assert len(pm['samples'])==14 and not pm['benchmark_eligible']
    return {'schema':'slrl-evidence-gates-v2', 'artifact_sha256':sha,
      'observed':{'assay':'GSE154112 OVCAR8-ADR guide-count growth depletion; no matched normal',
       'triples_evaluable':len(rows),'bh_q_lt_0_05':0,
       'all_layouts_negative_both_reps':0,
       'historical_explicit_hgsoc_models':i['explicit_hgsoc_total'],
       'development_only_proxy_seeds':len(p['seeds']),
       'greedy_beats_rl_same_surrogate_seeds':p['summary']['greedy']['wins_vs_rl'],
       'beam_beats_rl_same_surrogate_seeds':p['summary']['beam']['wins_vs_rl'],
       'peo1_guide_rows':q['raw_rows'], 'peo1_qc':'stop; no gene ranking',
       'peo1_columns_source_mapped':len(pm['samples']),
       'external_measured_methods_benchmark':'Harle pan-cancer retrospective; not HGSOC or matched normal',
       'external_methods_lines':h['lines'],'external_methods_trials':len(h['trials']),
       'external_mean_random_hits60':h['summary']['random']['mean_hits_60'],
       'external_mean_rl_hits60':h['summary']['sequential_reinforce']['mean_hits_60'],
       'corrected_policy_minus_random_hits60':hc['corrected_minus_random_hits60'],
       'judge_submission':'deferred; prepared packet not submitted'},
      'gates':{
       'corrected_multi_model_hgsoc_pair_or_triple_discovery':'UNMET',
       'matched_nonmalignant_perturbation_viability':'UNMET',
       'independent_measured_external_benchmark_beat':'UNMET',
       'validated_new_biological_discovery':'UNMET',
       '120_independent_datasets':'UNMET',
       '40_independently_executed_external_tools':'UNMET',
       'current_one_judge_round':'UNMET',
       '50_plus_substantive_text_body_page_paper':'UNMET'},
      'requirement_history':{'prior_ten_judge_rounds':'Superseded by parent-relayed September 28 one-round limit; zero completed current rounds'},
      'warning':'Assay has two D26 biological replicates and a post-outcome exploratory guide bootstrap. No measured cell viability, normal selectivity, multi-model interaction, external benchmark win, or new biological discovery is established. Engineering tests cannot fill these gates.'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);x=p.parse_args()
    Path(x.output).write_text(json.dumps(build(),indent=2)+'\n')
