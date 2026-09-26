"""Library-partition QC, no gene-level outcome claims."""
import argparse,json
from collections import defaultdict
import numpy as np,openpyxl
p=argparse.ArgumentParser();p.add_argument('--workbook',required=True);p.add_argument('--output',required=True);a=p.parse_args()
w=openpyxl.load_workbook(a.workbook,read_only=True,data_only=True).active
it=w.iter_rows(values_only=True);h=list(next(it)[:15]);parts=defaultdict(list)
for row in it:
 try:v=np.array(row[1:15],float)
 except (TypeError,ValueError):continue
 if not isinstance(row[0],str) or len(v)!=14 or not np.isfinite(v).all() or (v<0).any():continue
 tag='A' if row[0].startswith('HGLibA') else 'B' if row[0].startswith('HGLibB') else 'other';parts[tag].append(v)
out={}
for label,rows in parts.items():
 mat=np.asarray(rows);log=np.log2(mat+1)
 out[label]={'rows':len(rows),'median_counts':dict(zip(h[1:],np.median(mat,axis=0).tolist())),'zero_fraction':dict(zip(h[1:],np.mean(mat==0,axis=0).tolist())),'within_day10_logcount_pearson':{'A10_AB':float(np.corrcoef(log[:,0],log[:,1])[0,1]),'A10_AC':float(np.corrcoef(log[:,0],log[:,2])[0,1]),'A10_BC':float(np.corrcoef(log[:,1],log[:,2])[0,1]),'S10_AB':float(np.corrcoef(log[:,9],log[:,10])[0,1])}}
with open(a.output,'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2)[:3000])
