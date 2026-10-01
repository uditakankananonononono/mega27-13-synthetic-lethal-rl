import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from harle_category_benchmark import trial,METHODS
class BenchmarkTests(unittest.TestCase):
    def test_budget_unique_feedback_and_no_input_mutation(self):
        pairs=['A|B','A|C','B|C','B|D','C|D','A|D'];x=np.eye(2)[[0,1,0,1,0,1]];y=np.array([0,1,0,1,0,1.]);before=y.copy()
        for m in METHODS:
            a=trial(x,y,pairs,np.array([0,1]),np.array([2,3,4,5]),m,0,3)
            self.assertEqual(a['queries'],3);self.assertEqual(a['unique_queries'],3)
            self.assertEqual(a,trial(x,y,pairs,np.array([0,1]),np.array([2,3,4,5]),m,0,3))
        np.testing.assert_array_equal(before,y)
    def test_unrevealed_label_cannot_change_first_query(self):
        pairs=['A|B','A|C','B|C','B|D','C|D','A|D'];x=np.eye(2)[[0,1,0,1,0,1]];y=np.array([0,1,0,1,0,1.])
        for m in METHODS:
            a=trial(x,y,pairs,np.array([0,1]),np.array([2,3,4,5]),m,5,1)
            z=y.copy();z[2:]=1-z[2:]
            b=trial(x,z,pairs,np.array([0,1]),np.array([2,3,4,5]),m,5,1)
            self.assertEqual(a['queried_pairs'],b['queried_pairs'])
