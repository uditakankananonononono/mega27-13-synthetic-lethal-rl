"""Build a local study-only database from a provider dump without full import.

Only three INSERT tables with the exact study literal are accepted. All statements
are validated as single INSERTs; no arbitrary external dump statement is executed.
"""
import argparse,collections,json,re,sqlite3,zipfile
from pathlib import Path
TABLES=('cdko_experiment_design','cdko_sgrna_counts','cdko_original_sl_results')

def extract(archive,database,study):
    if not re.fullmatch(r'[0-9]{1,12}',study):raise ValueError('study must be PubMed digits')
    if Path(database).exists():raise ValueError('destination exists; no overwrite')
    z=zipfile.ZipFile(archive);db=sqlite3.connect(database)
    # The fixed source schema was inspected; restrict to CREATE of the three data tables.
    schema=z.read('SQL_Dumps/schemas/SLKB_sqlite3_schema.sql').decode()
    for t in TABLES:
        m=re.search(r'CREATE TABLE '+t+r'\s+\(.*?\);',schema,re.S)
        if not m:raise ValueError('schema mismatch')
        db.execute(m.group())
    count=collections.Counter();needle=("'"+study+"'").encode()
    with z.open('SQL_Dumps/SLKB-sqlite3_dump.sql') as f:
        for line in f:
            if needle not in line:continue
            for t in TABLES:
                prefix=('INSERT INTO '+t+' VALUES(').encode()
                if line.startswith(prefix):
                    text=line.decode().strip()
                    # sqlite execute accepts exactly one statement and rejects extra instructions.
                    db.execute(text);count[t]+=1;break
    db.commit();db.close();return dict(count)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',required=True);p.add_argument('--database',required=True);p.add_argument('--study',required=True);a=p.parse_args();print(json.dumps(extract(a.archive,a.database,a.study)))
