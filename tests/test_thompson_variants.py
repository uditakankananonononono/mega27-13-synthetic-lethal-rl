import importlib.util,tempfile,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('variants',Path(__file__).resolve().parents[1]/'scripts'/'thompson_baseline_variant_audit.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class VariantTests(unittest.TestCase):
    def test_missing_not_imputed(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'full.csv';b=Path(d)/'filtered.csv';a.write_text(',x,y\nA:B,1,2\n');b.write_text(',x,y\nA:B,1,NA\n')
            r=m.compare(a,b);self.assertEqual(r['filtered_missing_cells'],1);self.assertEqual(r['retained_cells'],1);self.assertEqual(r['retained_value_mismatches'],[])
    def test_pair_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.csv';b=Path(d)/'b.csv';a.write_text(',x\nA:B,1\n');b.write_text(',x\nB:C,1\n')
            with self.assertRaises(ValueError):m.compare(a,b)
