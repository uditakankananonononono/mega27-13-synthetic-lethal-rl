import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from thompson_late_window import centered_lfc
class LateWindowTests(unittest.TestCase):
    def test_control_center_is_zero(self):
        a=np.ones((52,3))*100;b=a.copy()*2;m=np.arange(52)<50
        x,shift=centered_lfc(a,b,m,1);np.testing.assert_allclose(np.median(x[m],axis=0),0)
        np.testing.assert_allclose(shift,np.log2(201/101))
    def test_controls_fail_closed(self):
        with self.assertRaises(ValueError):centered_lfc(np.ones((49,3)),np.ones((49,3)),np.ones(49,bool),1)
    def test_formula_known_residual(self):
        a=np.ones((53,3))*100;b=a.copy();b[50]=50;b[51]=50;b[52]=25
        x,_=centered_lfc(a,b,np.arange(53)<50,1)
        np.testing.assert_allclose(x[52]-x[50]-x[51],np.log2(26/101)-2*np.log2(51/101))
