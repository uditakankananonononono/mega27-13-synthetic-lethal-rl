import sys,unittest,tempfile,os
sys.path.insert(0,'src')
from slrl.sanger import model_name_map,ovarian_named_models
class SangerTests(unittest.TestCase):
 def test_name_mapping(self):
  f=tempfile.NamedTemporaryFile('w',delete=False)
  f.write('ccle_name,canonical_ccle_name,broad_id\nA_OVARY,A_OVARY,ACH-1\nB_OVARY,B_LARGE_INTESTINE,ACH-2\n')
  f.close()
  try:m=model_name_map(f.name)
  finally:os.unlink(f.name)
  assert ovarian_named_models(m,{'ACH-1','ACH-2'})==[('ACH-1','A_OVARY')]
if __name__=='__main__':unittest.main()
