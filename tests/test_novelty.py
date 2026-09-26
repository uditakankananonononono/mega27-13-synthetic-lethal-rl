import sys,unittest,tempfile,os
sys.path.insert(0,'src')
from slrl.novelty import load_synlethdb2020,novelty_status
class RegistryTests(unittest.TestCase):
 def test_all_source_categories_excluded(self):
  with tempfile.NamedTemporaryFile(mode='w',delete=False) as f:
   f.write('gene_a.identifier,gene_b.identifier,SL.source\n101,102,computer analysis\n102,103,CRISPR/CRISPRi\n')
   p=f.name
  try: pairs,sources,n=load_synlethdb2020(p)
  finally: os.unlink(p)
  assert n==2 and len(pairs)==2 and sources['computer analysis']==1
  assert novelty_status(('102','101'),[pairs])=='already_recorded'
  assert novelty_status(('101','103'),[pairs])=='not_found_in_searched_sources'
 def test_not_mistaking_missing_as_novel(self):
  assert novelty_status(('A','B'),[])=='not_found_in_searched_sources'
if __name__=='__main__':unittest.main()
