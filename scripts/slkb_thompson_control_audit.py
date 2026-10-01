"""Inspect selectively extracted curated counts without fitting a model."""
import argparse,collections,json,sqlite3
from pathlib import Path
import numpy as np

def audit(path):
    db=sqlite3.connect('file:'+str(Path(path).resolve())+'?mode=ro',uri=True)
    byline={};names=collections.Counter();invalid=0;negative=0;fractional=0
    for line, in db.execute('SELECT DISTINCT cell_line_origin FROM cdko_sgrna_counts'):
        n,p=db.execute('SELECT count(*),count(DISTINCT gene_pair_id) FROM cdko_sgrna_counts WHERE cell_line_origin=?',(line,)).fetchone();byline[line]={'guide_pair_rows':n,'gene_pair_ids_including_controls':p}
    for t0,n0,te,ne in db.execute('SELECT T0_counts,T0_replicate_names,TEnd_counts,TEnd_replicate_names FROM cdko_sgrna_counts'):
        a=np.array([float(v) for v in t0.split(';')]);b=np.array([float(v) for v in te.split(';')]);names.update(n0.split(';'));names.update(ne.split(';'))
        invalid+=int(len(a)!=len(n0.split(';')) or len(b)!=len(ne.split(';')) or not np.isfinite(a).all() or not np.isfinite(b).all())
        negative+=int((a<0).any() or (b<0).any());fractional+=int((a!=np.floor(a)).any() or (b!=np.floor(b)).any())
    orphan=db.execute('SELECT count(*) FROM cdko_sgrna_counts c LEFT JOIN cdko_experiment_design d ON c.guide_1_id=d.sgRNA_id LEFT JOIN cdko_experiment_design e ON c.guide_2_id=e.sgRNA_id WHERE d.sgRNA_id IS NULL OR e.sgRNA_id IS NULL').fetchone()[0]
    return {'schema':'slkb-thompson-controls-v1','study_pubmed_id':'33637726','guide_design_rows':db.execute('SELECT count(*) FROM cdko_experiment_design').fetchone()[0],
      'original_result_rows':db.execute('SELECT count(*) FROM cdko_original_sl_results').fetchone()[0],'by_line':byline,'replicate_name_occurrences':dict(names),'invalid_count_vectors':invalid,'negative_count_rows':negative,'fractional_noninteger_rows':fractional,'unmatched_guides':orphan,
      'primary_baseline_reproduced':False,'blocking_conflict':'Curated T0 counts are D14, not primary Cas9-negative A375 D7 baseline. A_B/B_A labels do not prove physical guide-orientation swaps.',
      'scope':'Curated count eligibility audit only; no normalization, fitting, benchmark or discovery'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--database',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=audit(a.database);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
