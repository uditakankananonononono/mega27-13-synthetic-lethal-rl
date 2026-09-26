import sys, unittest
sys.path.insert(0, 'scripts')
from position_injection_diagnostic import summarize_shift_thresholds

class InjectionTests(unittest.TestCase):
    def test_known_shift_and_strict_boundary(self):
        r = summarize_shift_thresholds([{'genes':['A','B','C'], 'layout_contrasts':[[0.3,-1], [-.4,-.2]]}], (0., .3, .5))
        self.assertAlmostEqual(r['triples'][0]['uniform_shift_needed_strictly_more_than_log2'], .3)
        self.assertEqual([r['shift_grid'][str(s)]['all_layouts_negative_both_reps'] for s in (0., .3, .5)], [0,0,1])
        self.assertEqual(r['shift_grid']['0.5']['mean_layout_negative_both_reps'], 1)
    def test_zero_shift_existing_negative(self):
        r = summarize_shift_thresholds([{'genes':['A','B','C'], 'layout_contrasts':[[-.2,-.3], [-1,-.1]]}], (0.,))
        self.assertEqual(r['shift_grid']['0.0']['all_layouts_negative_both_reps'], 1)
    def test_bad_replicates_rejected(self):
        with self.assertRaises(ValueError): summarize_shift_thresholds([{'genes':['A','B','C'], 'layout_contrasts':[[1]]}])
