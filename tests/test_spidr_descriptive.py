import sys,unittest
sys.path.insert(0,'scripts')
from spidr_descriptive import ranks,spearman,describe,COLS
class SpidrDescriptionTests(unittest.TestCase):
 def test_tie_ranks(self):self.assertEqual(ranks([4,1,1,2]),[4,1.5,1.5,3])
 def test_rank_direction(self):self.assertAlmostEqual(spearman([1,2,3],[3,2,1]),-1)
 def test_duplicate_rejected(self):
  with self.assertRaises(ValueError):describe([{'pair':'a'}, {'pair':'a'}])
 def test_descriptive_threshold_not_hits(self):
  rows=[dict(pair=str(i),**{c:v for c in COLS}) for i,v in enumerate([-2,-1,1])];x=describe(rows)
  self.assertEqual(x['contexts'][COLS[0]]['source_score_below_minus1_not_hits'],1)
  self.assertNotIn('hits',x)
