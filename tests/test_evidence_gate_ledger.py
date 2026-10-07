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
  assert len(x['artifact_sha256'])==11

  assert x['observed']['external_mean_rl_hits60'] < x['observed']['external_mean_random_hits60']
  assert x['gates']['current_one_judge_round']=='UNMET'

 def test_descriptive_counts_never_upgrade_gates(self):
  x=build()
  assert x['schema']=='slrl-evidence-gates-v3'
  late=x['observed']['thompson_late_window']
  assert late['technical_median_negative_counts_not_hits']=={'A375':155,'MEWO':416,'RPE1':739}
  assert not late['matched_normal_hgsoc_viability']
  assert not late['independent_biological_validation']
  assert set(x['gates'].values())=={'UNMET'}
