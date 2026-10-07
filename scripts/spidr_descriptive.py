"""Selection-conditioned published score description; not discovery/validation."""
import hashlib,json,math,statistics,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
N={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
COLS=['RPE1_GEMINI_score_sens','K562_GEMINI_score_sens','Hela_GEMINI_score_sens']
def ranks(xs):
 out=[0.]*len(xs);order=sorted(range(len(xs)),key=lambda i:xs[i]);i=0
 while i<len(order):
  j=i+1
  while j<len(order) and xs[order[j]]==xs[order[i]]:j+=1
  for k in order[i:j]:out[k]=(i+j-1)/2+1
  i=j
 return out
def spearman(a,b):
 a,b=ranks(a),ranks(b);ma,mb=statistics.mean(a),statistics.mean(b)
 den=math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
 if den==0:raise ValueError('constant ranks')
 return sum((x-ma)*(y-mb) for x,y in zip(a,b))/den
def read(path):
 z=zipfile.ZipFile(path);ss=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml'))];rr=[]
 for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//s:row',N):
  d={}
  for c in row.findall('s:c',N):
   v=c.find('s:v',N)
   if v is not None:d[c.attrib['r'].rstrip('0123456789')]=ss[int(v.text)] if c.attrib.get('t')=='s' else v.text
  rr.append(d)
 header=rr[0];positions={name:next(k for k,v in header.items() if v==name) for name in ['gene_combination']+COLS};rows=[]
 for d in rr[1:]:
  pair=d.get(positions['gene_combination'],'')
  if not pair:continue
  if ';' not in pair:raise ValueError('unexpected non-pair row')
  row={'pair':pair}
  for name in COLS:
   value=float(d[positions[name]])
   if not math.isfinite(value):raise ValueError('nonfinite')
   row[name]=value
  rows.append(row)
 if len(rows)!=1165 or len({r['pair'] for r in rows})!=1165:raise ValueError('row identity/count')
 return rows
def describe(rows):
 if len({r['pair'] for r in rows})!=len(rows):raise ValueError('duplicate pair')
 vectors={c:[r[c] for r in rows] for c in COLS}
 if any(not math.isfinite(v) for a in vectors.values() for v in a):raise ValueError('nonfinite')
 out={'schema':'spidr-selected-description-v1','scope':'selection-conditioned source-score description; no new hits, p-values, independent validation or HGSOC selectivity','rows':len(rows),'contexts':{},'context_pairs':{}}
 for c,a in vectors.items():out['contexts'][c]={'min':min(a),'median':statistics.median(a),'max':max(a),'negative_source_score_count_censored_not_effect_sign':sum(v<0 for v in a),'source_score_below_minus1_not_hits':sum(v<-1 for v in a)}
 for i,c in enumerate(COLS):
  for d in COLS[i+1:]:
   a,b=vectors[c],vectors[d];out['context_pairs'][c+'|'+d]={'negative_vs_zero_source_score_disagreements':sum((x<0)!=(y<0) for x,y in zip(a,b)),'average_tie_spearman':spearman(a,b)}
 return out
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args();path=Path(a.input)
 manifest=json.loads(Path('results/spidr-source-audit.json').read_text());digest=hashlib.sha256(path.read_bytes()).hexdigest()
 if digest!=manifest['files']['selected_cross_context_scores']['sha256']:raise ValueError('input checksum')
 out=describe(read(path));out['input_sha256']=digest;out['freeze_sha256']=hashlib.sha256(Path('docs/SPIDR-DESCRIPTIVE-FREEZE.md').read_bytes()).hexdigest();Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
