import sys,unittest,copy
sys.path.insert(0,'scripts')
from evidence_gate_ledger import build
class EvidenceGateTests(unittest.TestCase):
 def test_real_artifacts_gate_and_hashes(self):
  x=build()
  assert x['observed']['triples_evaluable']==455
  assert x['observed']['bh_q_lt_0_05']==0
  assert x['observed']['greedy_beats_rl_same_surrogate_seeds']==10
  assert set(x['gates'].values())=={'UNMET'}
  assert len(x['artifact_sha256'])==6
