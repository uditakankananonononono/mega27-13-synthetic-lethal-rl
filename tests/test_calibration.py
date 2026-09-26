import sys,unittest
sys.path.insert(0,'src')
import numpy as np
from slrl.calibration import normalize_dependency_matrix,holdout_models,shrink_gene_mean
class CalibTests(unittest.TestCase):
 def test_proxy_is_not_viability(self):
  x,m=normalize_dependency_matrix([[0,-1,-3],[.1,-.5,float('nan')]])
  assert list(x[0])==[0,1,2] and not m[1,2]
 def test_holdout_no_leakage(self):
  x=np.array([[1,2],[3,4],[5,6]])
  a,b=holdout_models(x,[1]);assert list(a[:,0])==[1,5] and b[0,0]==3
 def test_single_model_block(self):
  with self.assertRaises(ValueError):shrink_gene_mean([[1,2]])
 def test_missing_gene_uncertainty(self):
  p,u,c=shrink_gene_mean([[1,float('nan')],[2,float('nan')]])
  assert np.isinf(u[1]) and c[1]==0
if __name__=='__main__':unittest.main()
