import sys,unittest
sys.path.insert(0,'src')
from slrl.development import build_legacy_cancer_proxy
class DevTests(unittest.TestCase):
 def test_small_fixture_blocked(self):
  with self.assertRaises(ValueError):build_legacy_cancer_proxy('missing','missing',{},max_genes=20)
if __name__=='__main__':unittest.main()
