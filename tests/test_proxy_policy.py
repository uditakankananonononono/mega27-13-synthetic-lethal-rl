import sys,unittest
sys.path.insert(0,'src')
import numpy as np
from slrl.surrogate import PriorSurrogate
from slrl.proxy_policy import CancerOnlyPolicy
class ProxyTests(unittest.TestCase):
 def test_scoped_training(self):
  genes=('A','B','C','D');features=np.eye(4);mask=np.ones(4,bool)
  s=PriorSurrogate(np.array([.1,.2,.3,.4]),mask,({1},{0,2},{1,3},{2}),np.full(4,.3))
  a=CancerOnlyPolicy(genes,features,mask,{('A','B')},7)
  b=CancerOnlyPolicy(genes,features,mask,{('A','B')},7)
  h1=a.train(s,40);h2=b.train(s,40)
  assert h1==h2 and np.allclose(a.weights,b.weights)
  assert all(not {'A','B'}.issubset(set(names)) for names,_ in h1)
 def test_no_healthy_viability_claim(self):
  genes=('A','B','C');mask=np.ones(3,bool)
  s=PriorSurrogate(np.array([.1,.2,.3]),mask,({1},{0,2},{1}),np.full(3,.2))
  p=CancerOnlyPolicy(genes,np.eye(3),mask,seed=9)
  assert p.episode(s)[3]['healthy_viability_status']=='not_measured'
if __name__=='__main__':unittest.main()
