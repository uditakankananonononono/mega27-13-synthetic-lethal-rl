"""Frozen curated-only descriptive late-window residuals, no inferential hits."""
import argparse,collections,hashlib,json,sqlite3
from pathlib import Path
import numpy as np
LABEL='sample-line binding per SLKB curation, not independently recovered from primary headers'

def centered_lfc(before,after,control_mask,pseudocount):
    if pseudocount<=0:raise ValueError('positive pseudocount required')
    if np.sum(control_mask)<50:raise ValueError('fewer than 50 eligible negative controls')
    raw=np.log2((after+pseudocount)/(before+pseudocount))
    shift=np.median(raw[control_mask],axis=0)
    return raw-shift,shift

def run(database,mapping):
    db=sqlite3.connect('file:'+str(Path(database).resolve())+'?mode=ro',uri=True)
    design={r[0]:r for r in db.execute('SELECT * FROM cdko_experiment_design')}
    source_mapping=json.loads(Path(mapping).read_text())
    if source_mapping.get('schema')!='thompson-design-mapping-v1':raise ValueError('unverified mapping schema')
    out={}
    for line, in db.execute('SELECT DISTINCT cell_line_origin FROM cdko_sgrna_counts'):
        rs=list(db.execute('SELECT sgRNA_pair_id,guide_1_id,guide_2_id,target_type,T0_counts,TEnd_counts FROM cdko_sgrna_counts WHERE cell_line_origin=? ORDER BY sgRNA_pair_id',(line,)))
        before=np.array([[float(v) for v in r[4].split(';')] for r in rs]);after=np.array([[float(v) for v in r[5].split(';')] for r in rs])
        if before.shape!=(41838,3) or after.shape!=before.shape or not np.isfinite(before).all() or not np.isfinite(after).all():raise ValueError('source count shape')
        eligible=np.all(before>=20,axis=1);control=np.array([r[3]=='Control' for r in rs])&eligible
        singles={};dual=[]
        for i,r in enumerate(rs):
            _,a,b,kind,_,_=r
            if kind=='Single':
                g=b if design[a][3]=='CONTROL' else a
                if g in singles:raise ValueError('ambiguous single')
                singles[g]=i
            if kind=='Dual':dual.append(i)
        groups=collections.defaultdict(list);ex=collections.Counter()
        for i in dual:
            _,a,b,_,_,_=rs[i]
            if a not in singles or b not in singles:ex['missing_exact_single']+=1;continue
            if not(eligible[i] and eligible[singles[a]] and eligible[singles[b]]):ex['baseline_count_below20_any_replicate']+=1;continue
            pair='|'.join(sorted((design[a][3],design[b][3])))
            groups[pair].append((i,singles[a],singles[b]))
        m=source_mapping['by_line'][line]
        if m['counts'].get('sequence_matched')!=len(rs) or m.get('duplicate_construct_keys')!=0 or len(m['dual_rows_missing_exact_single'])!=ex['missing_exact_single']:raise ValueError('mapping/count disagreement')
        lfc={};shifts={}
        for p in [.5,1.,5.]:lfc[p],shifts[p]=centered_lfc(before,after,control,p)
        rows=[]
        for pair,ix in sorted(groups.items()):
            if len(ix)<4:ex['pair_fewer_than_four_eligible_constructs']+=1;continue
            values={}
            for p in [.5,1.,5.]:
                r=np.median([lfc[p][i]-lfc[p][a]-lfc[p][b] for i,a,b in ix],axis=0)
                values[str(p)]={'technical_replicate_median_residuals':r.tolist(),'median_residual':float(np.median(r)),'all_technical_medians_negative':bool(np.all(r<0))}
            primary=values['1.0'];rows.append({'pair':pair,'eligible_constructs':len(ix),'pseudocount_sensitivity':values,'any_technical_sign_changed':any(np.any(np.sign(values[str(p)]['technical_replicate_median_residuals'])!=np.sign(primary['technical_replicate_median_residuals'])) for p in [.5,5.])})
        out[line]={'sample_identity':LABEL,'negative_controls_eligible':int(control.sum()),'control_center_by_pseudocount':{str(k):v.tolist() for k,v in shifts.items()},'exclusions':dict(ex),'descriptive_pairs':len(rows),'pairs_all_three_technical_medians_negative':sum(r['pseudocount_sensitivity']['1.0']['all_technical_medians_negative'] for r in rows),'pairs_with_pseudocount_sign_change':sum(r['any_technical_sign_changed'] for r in rows),'rows':rows}
    return {'schema':'thompson-late-window-description-v1','sample_identity':LABEL,'scope':'D14-conditioned D28 additional guide depletion; descriptive only, no p-values, hit calls, independent validation, healthy-selectivity or discovery','mapping_sha256':hashlib.sha256(Path(mapping).read_bytes()).hexdigest(),'archive_sha256':'05ece8a60b58916fcfb576be1b5a824773b42471f21e2c6b141b81de7da72576','by_line':out,'caveat':'Single and double promoter contexts differ; technical replicates are not independent biological replication; all three negative signs are not calibrated epistasis hits.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--database',required=True);p.add_argument('--mapping',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=run(a.database,a.mapping);Path(a.output).write_text(json.dumps(r,separators=(',',':'))+'\n');print(json.dumps({k:{x:y for x,y in v.items() if x!='rows'} for k,v in r['by_line'].items()},indent=2))
