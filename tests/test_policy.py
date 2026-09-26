import sys, unittest
sys.path.insert(0,'src')
import numpy as np
from slrl.simulator import Context, DualContext
from slrl.policy import Policy, train

class PolicyTests(unittest.TestCase):
    def context(self):
        cancer = Context('toy cancer',True,np.full(5,.02),np.zeros((5,5)),{(0,1,2):3.},np.zeros(5))
        healthy = Context('toy normal',False,np.full(5,.02),np.zeros((5,5)),{},np.zeros(5))
        return DualContext(cancer,healthy)
    def policy(self):
        return Policy(np.eye(5),np.zeros(5),np.ones(5,dtype=bool))
    def test_training_is_seeded_and_finite(self):
        a,b=self.policy(),self.policy()
        out1=train(a,self.context(),100,seed=17)
        out2=train(b,self.context(),100,seed=17)
        assert out1 == out2
        assert np.allclose(a.weights,b.weights) and np.all(np.isfinite(a.weights))
    def test_gene_masks(self):
        p=self.policy();p.repair_mask[4]=False
        for _ in range(30):
            genes,_,_=p.episode(self.context(),np.random.default_rng(_))
            assert len(set(genes)) == 3 and 4 not in genes
    def test_excluded_known_pairs(self):
        for seed in range(50):
            genes,_,_=self.policy().episode(self.context(),np.random.default_rng(seed),known_pairs={(0,1)})
            assert not (0 in genes and 1 in genes)
    def test_empty_eligible_space(self):
        p=self.policy();p.repair_mask[:]=False
        with self.assertRaises(ValueError): p.episode(self.context(),np.random.default_rng(1))
if __name__ == '__main__': unittest.main()
