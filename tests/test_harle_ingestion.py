import importlib.util
from pathlib import Path
import unittest
s=importlib.util.spec_from_file_location('harle',Path(__file__).resolve().parents[1]/'scripts'/'harle_ingestion_audit.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class IngestionTests(unittest.TestCase):
    def test_unordered_identity(self):self.assertEqual(m.canonical('B|A'),'A|B')
    def test_split_is_orientation_invariant(self):self.assertEqual(m.partition('B|A'),m.partition('A|B'))
    def test_invalid_pair_rejected(self):
        with self.assertRaises(ValueError):m.canonical('A|A')
