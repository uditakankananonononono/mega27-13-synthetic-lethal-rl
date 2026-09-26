import sys, unittest
sys.path.insert(0, 'src')
import numpy as np
from slrl.simulator import Context, DualContext
from slrl.search import candidates, budgeted_random
from slrl.validation import third_order_log_viability, strict_triple_phenotype

class ScaffoldTests(unittest.TestCase):
    def context(self, cancer=True):
        return Context('test', cancer, np.array([0.05, 0.05, 0.05]), np.zeros((3,3)), {(0,1,2): 3.0} if cancer else {}, np.zeros(3))
    def test_triple_specific_synergy(self):
        c = self.context()
        assert c.viability((0,1)) > .8
        assert c.viability((0,1,2)) < .05
        assert c.viability((0,1,2)) < self.context(False).viability((0,1,2))
    def test_repeats_rejected(self):
        with self.assertRaises(ValueError): self.context().viability((0,0))
    def test_dimensionality_rejected(self):
        with self.assertRaises(ValueError): Context('bad', True,np.zeros(3),np.zeros((2,2)),{},np.zeros(3)).validate()
    def test_reward_selectivity(self):
        d = DualContext(self.context(), self.context(False))
        assert d.reward((0,1,2)) > d.reward((0,1))
    def test_known_pair_mask(self):
        assert list(candidates(3, [1,1,1], {(0,1)})) == [(0,2),(1,2)]
    def test_random_budget_unique(self):
        d = DualContext(self.context(), self.context(False))
        picks = budgeted_random(d, candidates(3,[1,1,1]),2,42)
        assert len(set(p for p,_ in picks)) == 2
    def test_third_order_not_pair_effect(self):
        m = {frozenset((0,)):1.,frozenset((1,)):1.,frozenset((2,)):1.,frozenset((0,1)):1.,frozenset((0,2)):1.,frozenset((1,2)):1.,frozenset((0,1,2)):.2}
        assert strict_triple_phenotype(m)
        assert third_order_log_viability(m) < -1
    def test_missing_subset_rejected(self):
        with self.assertRaises(ValueError): third_order_log_viability({frozenset((0,1,2)):.1})
if __name__ == '__main__': unittest.main()
