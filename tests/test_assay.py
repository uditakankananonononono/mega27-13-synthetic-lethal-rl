import sys,unittest
sys.path.insert(0,'src')
from slrl.assay import fold_change,summarize_replicates
class AssayTests(unittest.TestCase):
 def test_growth_depletion_not_viability(self):
  x=fold_change({'Cell_D9':99,'Cell_D26_rep1':49,'Cell_D26_rep2':24})
  assert len(x)==2 and x[0]<0 and x[1]<x[0]
 def test_control_aggregate(self):
  x=summarize_replicates([(('dummyguide_1','CDK4_1','TOP1_1'),{'Cell_D9':99,'Cell_D26_rep1':49,'Cell_D26_rep2':48}),
     (('TOP1_2','dummyguide_2','CDK4_2'),{'Cell_D9':99,'Cell_D26_rep1':54,'Cell_D26_rep2':52})])
  assert x[('CDK4','CTRL','TOP1')]['guide_constructs']==2
 def test_reject_bad_pseudocount(self):
  with self.assertRaises(ValueError):fold_change({'Cell_D9':1},pseudo_count=0)
if __name__=='__main__':unittest.main()
