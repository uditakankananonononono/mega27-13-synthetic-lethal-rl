import unittest,numpy as np
from slrl.pair_sampling import distribution,sample
class PairSamplingTests(unittest.TestCase):
    def test_irregular_graph_zero_score_uniform_pair_probability(self):
        pairs=[('A','B'),('A','C'),('A','D'),('B','C')]
        genes,p,incident,w=distribution(pairs,np.zeros(4));edge=np.zeros(4)
        for g,pg in zip(genes,p):edge[incident[g]]+=pg*w[incident[g]]/w[incident[g]].sum()
        np.testing.assert_allclose(edge,np.ones(4)/4)
    def test_nonzero_exact_softmax_probability(self):
        pairs=[('A','B'),('A','C'),('B','C')];scores=np.array([-1000.,0.,2.]);genes,p,incident,w=distribution(pairs,scores);edge=np.zeros(3)
        for g,pg in zip(genes,p):edge[incident[g]]+=pg*w[incident[g]]/w[incident[g]].sum()
        np.testing.assert_allclose(edge,w/w.sum())
    def test_orientation_duplicates_fail(self):
        with self.assertRaises(ValueError):distribution([('A','B'),('B','A')],[0,0])
    def test_sampling_legal(self):
        pairs=[('A','B'),('A','C')];i,g=sample(pairs,[0,0],np.random.default_rng(0));self.assertIn(g,pairs[i])
