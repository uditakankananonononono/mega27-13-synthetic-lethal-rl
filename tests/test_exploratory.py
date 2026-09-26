import sys,unittest
sys.path.insert(0,'src')
import numpy as np
from slrl.exploratory import third_order_from_groups
from itertools import combinations
class ContrastTests(unittest.TestCase):
 def groups(self):
  t=('A','B','C');return {tuple(x):np.tile([-.3*len(x),-.3*len(x)],(8,1)) for n in range(4) for x in combinations(t,n)}
 def test_no_interaction(self):
  x=third_order_from_groups(self.groups(),('A','B','C'),bootstrap=20)
  assert abs(x['mean_log2_excess'])<1e-9
 def test_triple_only(self):
  groups=self.groups();groups[('A','B','C')]-=2.
  x=third_order_from_groups(groups,('A','B','C'),bootstrap=20)
  assert abs(x['mean_log2_excess']+2)<1e-9 and x['replicate_direction_agrees']
 def test_required_subset(self):
  g=self.groups();del g[('A','C')]
  assert third_order_from_groups(g,('A','B','C'),bootstrap=20) is None
 def test_four_guides(self):
  g=self.groups();g[()]=g[()][:2]
  assert third_order_from_groups(g,('A','B','C'),bootstrap=20) is None
if __name__=='__main__':unittest.main()
