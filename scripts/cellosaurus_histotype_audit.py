"""Read-only Cellosaurus identity audit; no inferred high-grade serous label."""
import csv,json,time,sys
from urllib.parse import quote
import requests
score,mapfile,out=sys.argv[1:4]
with open(mapfile) as f:m={r['broad_id']:r['ccle_name'] for r in csv.DictReader(f)}
with open(score) as f:
 r=csv.reader(f);next(r);ids=[row[0] for row in r if m.get(row[0],'').endswith('_OVARY')]
records=[]
for ident in ids:
 name=m[ident].removesuffix('_OVARY')
 url='https://api.cellosaurus.org/search/cell-line'
 matches=[]
 for field in ('id','sy'):
  resp=requests.get(url,params={'q':f'{field}:{name}','fields':'id,ac,di,sy','format':'json','rows':100},timeout=12);resp.raise_for_status()
  matches.extend(resp.json()['Cellosaurus']['cell-line-list'])
 matches=list({v['accession-list'][0]['value']:v for v in matches}.values())
 # Exact primary or synonym only: fuzzy search matches do not certify identity.
 exact=[]
 for v in matches:
  names=[x['value'] for x in v.get('name-list',[])]
  if any(x.replace('-','').replace(':','').replace(' ','').upper()==name.replace('-','').replace(':','').replace(' ','').upper() for x in names):exact.append(v)
 # An ambiguous normalized alias is not an identity binding (ES2 is both Ewing and ovarian ES-2).
 if len(exact)==1:
  v=exact[0];accession=v['accession-list'][0]['value'];diseases=[x['label'] for x in v.get('disease-list',[])]
 else:accession=None;diseases=[]
 records.append({'model_id':ident,'ccle_name':m[ident],'exact_cellosaurus_matches':len(exact),'accession':accession,'cellosaurus_url':f'https://www.cellosaurus.org/{accession}' if accession else None,'disease_labels':diseases,'explicit_hgsoc':any('High grade ovarian serous adenocarcinoma'==x for x in diseases) if len(exact)==1 else False})
 time.sleep(.16)
outdata={'scope':'historical Project SCORE 29 ovarian-named models; exact identity match to Cellosaurus name/synonym, Disease label only; no histology inferred from name or site','source':'https://api.cellosaurus.org/','models':records,'explicit_hgsoc_count':sum(v['explicit_hgsoc'] for v in records),'unresolved_exact_match_count':sum(v['exact_cellosaurus_matches']!=1 for v in records)}
with open(out,'w') as f:json.dump(outdata,f,indent=2)
print(json.dumps({'total':len(records),'explicit_hgsoc_count':outdata['explicit_hgsoc_count'],'unresolved_exact_match_count':outdata['unresolved_exact_match_count'],'hgsoc':[x['ccle_name'] for x in records if x['explicit_hgsoc']],'unresolved':[x['ccle_name'] for x in records if x['exact_cellosaurus_matches']!=1]},indent=2))
