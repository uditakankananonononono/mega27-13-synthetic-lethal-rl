import sys,unittest
sys.path.insert(0,'src')
from slrl.benchmark import average_precision_at_k,matched_budget_permutation,benjamini_hochberg
class BenchmarkTests(unittest.TestCase):
 def test_precision(self):assert average_precision_at_k(['A','B','C'],{'A','C'},2)==.5
 def test_duplicate_reject(self):
  with self.assertRaises(ValueError):average_precision_at_k(['A','A'],{'A'},2)
 def test_need_independent_context(self):
  with self.assertRaises(ValueError):matched_budget_permutation([.8],[.2])
 def test_paired_seed(self):
  a=matched_budget_permutation([.8,.9,.7],[.1,.3,.2],99,42)
  b=matched_budget_permutation([.8,.9,.7],[.1,.3,.2],99,42)
  assert a==b and a['mean_delta']>0
 def test_bh(self):
  assert list(benjamini_hochberg([.01,.5,.02]))==[.03,.5,.03]
if __name__=='__main__':unittest.main()
