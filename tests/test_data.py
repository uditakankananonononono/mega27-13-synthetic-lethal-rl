import sys,tempfile,os,hashlib,unittest
sys.path.insert(0,'src')
import numpy as np
from slrl.data import check_md5,IntegrityError,read_gene_effect,split_models
class DataTests(unittest.TestCase):
 def setUp(self):
  f=tempfile.NamedTemporaryFile(mode='w',delete=False);f.write('ModelID,A (1),B (2)\nCANCER,-0.9,-0.2\nNORMAL,-0.1,-0.3\n');f.close();self.path=f.name
 def tearDown(self):os.unlink(self.path)
 def test_integrity(self):
  with open(self.path,'rb') as f:d=hashlib.md5(f.read()).hexdigest()
  assert check_md5(self.path,d)==d
  with self.assertRaises(IntegrityError):check_md5(self.path,'0'*32)
 def test_selection_and_sign(self):
  x=read_gene_effect(self.path,['CANCER'],['A','B']);assert list(x)==['CANCER'] and x['CANCER'][0]<0
 def test_no_ambiguous_gene(self):
  with self.assertRaises(ValueError):read_gene_effect(self.path,['CANCER'],['A','MISSING'])
 def test_holdout(self):
  assert split_models(['A','B','C'],['C'])==(['A','B'],['C'])
  with self.assertRaises(ValueError):split_models(['A'],['B'])
if __name__=='__main__':unittest.main()
