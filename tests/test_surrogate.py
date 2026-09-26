import sys,unittest
sys.path.insert(0,'src')
import numpy as np
from slrl.surrogate import PriorSurrogate
class SurrogateTests(unittest.TestCase):
 def model(self):return PriorSurrogate(np.array([.1,.2,.3]),np.ones(3,bool),({1},{0,2},{1}),np.array([.1,.1,.1]))
 def test_uncertainty_grows_with_order(self):
  a=self.model().predict((0,));b=self.model().predict((0,1));c=self.model().predict((0,1,2))
  assert a['uncertainty']<b['uncertainty']<c['uncertainty']
  assert c['healthy_viability_status']=='not_measured'
 def test_unsupported_gene_rejected(self):
  m=self.model();m.repair_mask[1]=False
  with self.assertRaises(ValueError):m.predict((0,1))
 def test_no_near_certain_prior(self):
  assert self.model().predict((0,1,2))['prior_interaction_loss']<=.25
if __name__=='__main__':unittest.main()
