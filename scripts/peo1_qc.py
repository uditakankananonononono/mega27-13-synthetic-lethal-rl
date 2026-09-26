"""Descriptive QC of independent PEO1 monogenic guide-count screen; no hits."""
import argparse,csv,json,re
from collections import Counter,defaultdict
import numpy as np
import openpyxl
p=argparse.ArgumentParser();p.add_argument('--workbook',required=True);p.add_argument('--output',required=True);a=p.parse_args()
s=openpyxl.load_workbook(a.workbook,read_only=True,data_only=True).active
it=s.iter_rows(values_only=True);header=list(next(it)[:15]);expected=['GeneID','A10_A','A10_B','A10_C','A5_A','A5_B','A5_C','Ctrl_A','Ctrl_B','Ctrl_C','S10_A','S10_B','S5_A','S5_B','S5_C'];assert header==expected
values=[];genes=[];ids=[];bad=Counter()
for row in it:
 g=row[0]
 if not isinstance(g,str):bad['missing_guide_id']+=1;continue
 try:v=np.array([float(x) for x in row[1:15]])
 except (TypeError,ValueError):bad['bad_numeric']+=1;continue
 if len(v)!=14 or np.any(v<0) or not np.isfinite(v).all():bad['invalid_counts']+=1;continue
 tokens=g.split('|'); gene=tokens[2] if len(tokens)>2 else ''
 if not gene or not re.fullmatch('[A-Za-z0-9_.-]+',gene):bad['ambiguous_symbol']+=1;continue
 ids.append(g);genes.append(gene);values.append(v)
x=np.array(values);gene_count=Counter(genes)
ctrl=np.median(x[:,6:9],axis=1)
passing=(ctrl>=20)&np.array([gene_count[g]>=2 for g in genes])
log=np.log2(x+1)
# Per-sample library depth normalization, ONLY for QC distribution; no candidate ranking here.
depths=x.sum(axis=0);corr=np.corrcoef(log[passing,:].T)
result={'scope':'PEO1 GSE123290 guide-count library QC before condition-specific outcome ranking; no hit or novelty claims','columns':header,'raw_rows':s.max_row-1,'accepted_rows':len(x),'unique_guide_ids':len(set(ids)),'unique_symbols':len(gene_count),'bad':dict(bad),'sample_total_counts':dict(zip(header[1:],map(float,depths))),'sample_zero_fraction':dict(zip(header[1:],map(float,np.mean(x==0,axis=0)))),'sample_median_count':dict(zip(header[1:],map(float,np.median(x,axis=0)))),'sample_logcount_correlations':{header[i+1]+'__'+header[j+1]:float(corr[i,j]) for i in range(14) for j in range(i+1,14)},'baseline_ctrl_median_ge20_and_gene_ge2_guides':int(passing.sum()),'eligible_genes':len(set(g for g,ok in zip(genes,passing) if ok)),'source':'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE123nnn/GSE123290/suppl/'}
with open(a.output,'w') as f:json.dump(result,f,indent=2)
print(json.dumps({k:result[k] for k in ('raw_rows','accepted_rows','unique_guide_ids','unique_symbols','bad','sample_total_counts','baseline_ctrl_median_ge20_and_gene_ge2_guides','eligible_genes')},indent=2))
