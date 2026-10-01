"""Exact construct/design and matched-single audit; no outcome contrasts."""
import argparse,collections,hashlib,json,sqlite3
from pathlib import Path
import openpyxl

def audit(database,workbook):
    c=sqlite3.connect('file:'+str(Path(database).resolve())+'?mode=ro',uri=True)
    d={r[0]:r for r in c.execute('SELECT * FROM cdko_experiment_design')}
    sheet=openpyxl.load_workbook(workbook,read_only=True,data_only=True)['4']
    primary=collections.defaultdict(list)
    for r in sheet.iter_rows(values_only=True,min_row=5):
        if r[2] and r[4]:primary[(r[2].upper(),r[4].upper())].append(r)
    out={}
    for line, in c.execute('SELECT DISTINCT cell_line_origin FROM cdko_sgrna_counts'):
        rs=list(c.execute('SELECT sgRNA_pair_id,guide_1_id,guide_2_id,target_type,T0_counts,T0_replicate_names FROM cdko_sgrna_counts WHERE cell_line_origin=?',(line,)))
        counts=collections.Counter();singles=collections.defaultdict(list);controls=collections.Counter();keys=collections.Counter()
        for rowid,a,b,kind,t0,n0 in rs:
            x,y=d[a],d[b];key=(x[1],y[1]);keys[key]+=1;matches=primary.get(key,[])
            if len(matches)!=1:counts['unmapped_or_ambiguous']+=1;continue
            r=matches[0];seq=(x[2].rsplit('_',1)[0],y[2].rsplit('_',1)[0])
            counts['sequence_matched' if seq==(r[3],r[5]) else 'sequence_mismatch']+=1
            counts['type_'+kind]+=1
            if kind=='Single':
                if (x[3]=='CONTROL')==(y[3]=='CONTROL'):counts['invalid_single_target_labels']+=1
                else:
                    gene=b if x[3]=='CONTROL' else a;ctrl=a if x[3]=='CONTROL' else b
                    singles[gene].append(rowid);controls[d[ctrl][1]]+=1
            if all(float(v)==0 for v in t0.split(';')):counts['baseline_zero_all_replicates']+=1
        missing=[];ambiguous=[]
        for rowid,a,b,kind,t0,n0 in rs:
            if kind=='Dual':
                if a not in singles or b not in singles:missing.append({'row_id':rowid,'guide_names':[d[a][1],d[b][1]],'targets':[d[a][3],d[b][3]]})
                elif len(singles[a])!=1 or len(singles[b])!=1:ambiguous.append(rowid)
        out[line]={'counts':dict(counts),'duplicate_construct_keys':sum(v>1 for v in keys.values()),'matched_single_control_names':dict(controls),'dual_rows_missing_exact_single':missing,'dual_rows_ambiguous_exact_single':ambiguous,
                   'sample_prefixes':sorted({n.split('_D')[0] for r in rs for n in r[5].split(';')})}
    return {'schema':'thompson-design-mapping-v1','primary_design_sha256':hashlib.sha256(Path(workbook).read_bytes()).hexdigest(),'by_line':out,
            'BA_BB_BD_independent_primary_binding':'UNRESOLVED; curated line labels bind prefixes only within SLKB',
            'physical_dual_guide_order':'All curated constructs match primary A/B guide order, not swapped promoter experiments',
            'effects_computed':False,'normalization_frozen':False,
            'scope':'Baseline/design eligibility only; no differential depletion, gene ranking, fit or discovery'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--database',required=True);p.add_argument('--workbook',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=audit(a.database,a.workbook);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:{'counts':v['counts'],'missing_singles':len(v['dual_rows_missing_exact_single']),'ambiguous_singles':len(v['dual_rows_ambiguous_exact_single']),'duplicates':v['duplicate_construct_keys'],'control':v['matched_single_control_names'],'prefix':v['sample_prefixes']} for k,v in r['by_line'].items()},indent=2))
