import sys,unittest
sys.path.insert(0,'scripts')
from peo1_similarity_audit import COLS
class SimilaritySchemaTests(unittest.TestCase):
 def test_explicit_inclusion_and_names(self):
  self.assertEqual(len(COLS),14)
  self.assertEqual([COLS[i] for i in (0,1,2,9,10)],['A10_A','A10_B','A10_C','S10_A','S10_B'])
