import sys,unittest,tempfile,os
sys.path.insert(0,'src')
from slrl.reactome import load_ncbi_pathways,repair_members,bounded_copathway_edges
class ReactomeTests(unittest.TestCase):
 def test_human_filter_and_edges(self):
  f=tempfile.NamedTemporaryFile('w',delete=False)
  f.write('101\tR-HSA-1\turl\tDNA Repair\tTAS\tHomo sapiens\n102\tR-HSA-1\turl\tDNA Repair\tTAS\tHomo sapiens\n101\tR-MMU-1\turl\tDNA Repair\tTAS\tMus musculus\n')
  f.close()
  try:p,n,g=load_ncbi_pathways(f.name)
  finally:os.unlink(f.name)
  assert repair_members(p,n)=={'101','102'} and bounded_copathway_edges(p,g)=={('101','102')}
 def test_no_dense_umbrella_edges(self):
  assert not bounded_copathway_edges({'X':{'1','2','3'}},{'1','2','3'},max_pathway_size=2)
if __name__=='__main__':unittest.main()
