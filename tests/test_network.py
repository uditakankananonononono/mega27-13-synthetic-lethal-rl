import sys,unittest
sys.path.insert(0,'src')
from slrl.network import graph_from_edges,degree_features
class GraphTests(unittest.TestCase):
 def test_dedup_and_scope(self):
  g,m=graph_from_edges(['A','B','C'],[('A','B'),('B','A'),('B','C'),('A','NOTMAPPED')],['A','C'])
  assert [len(x) for x in g]==[1,2,1] and list(m)==[True,False,True]
  assert degree_features(g,m).shape==(3,3)
 def test_missing_repair_gene(self):
  with self.assertRaises(ValueError):graph_from_edges(['A'],[],['B'])
if __name__=='__main__':unittest.main()
