import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('reconciliation',Path(__file__).resolve().parents[1]/'scripts'/'peo1_source_reconciliation.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class SourceReconciliationTests(unittest.TestCase):
    def test_known_sample_is_mapped_without_selecting_pair(self):
        s='^SAMPLE = GSM1\n!Sample_description = A10_A\n!Sample_data_processing = edgeR used\n'
        x='<article><p>duplicates of Adherent Day 10 analyzed with DESeq2</p></article>'
        r=m.reconcile(s,x)
        self.assertEqual(r['samples']['A10_A']['geo_accession'],'GSM1')
        self.assertTrue(r['processing_conflict'])
        self.assertFalse(r['benchmark_eligible'])
        self.assertEqual(r['adherent_pair_selected_by_primary_paper'],'UNRESOLVED')
        self.assertEqual(len(r['missing_workbook_columns']),13)
    def test_duplicate_label_fails_closed(self):
        s='^SAMPLE = GSM1\n!Sample_description = A10_A\n^SAMPLE = GSM2\n!Sample_description = A10_A\n'
        with self.assertRaises(ValueError):m.reconcile(s,'<article/>')
    def test_all_sample_identities_do_not_prove_analysis_eligibility(self):
        s=''.join(f'^SAMPLE = GSM{i}\n!Sample_description = {label}\n' for i,label in enumerate(m.EXPECTED))
        r=m.reconcile(s,'<article/>')
        self.assertEqual(r['missing_workbook_columns'],[])
        self.assertFalse(r['benchmark_eligible'])
