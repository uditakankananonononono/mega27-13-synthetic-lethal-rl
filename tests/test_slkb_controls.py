import importlib.util,sqlite3,tempfile,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('audit',Path(__file__).resolve().parents[1]/'scripts'/'slkb_thompson_control_audit.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ControlTests(unittest.TestCase):
    def test_d14_curated_vectors_cannot_pass_primary_baseline(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.sqlite';db=sqlite3.connect(p)
            db.executescript('CREATE TABLE cdko_experiment_design(sgRNA_id INTEGER); CREATE TABLE cdko_original_sl_results(id INTEGER); CREATE TABLE cdko_sgrna_counts(guide_1_id INTEGER,guide_2_id INTEGER,gene_pair_id INTEGER,cell_line_origin TEXT,T0_counts TEXT,T0_replicate_names TEXT,TEnd_counts TEXT,TEnd_replicate_names TEXT);')
            db.execute('INSERT INTO cdko_experiment_design VALUES(1)');db.execute('INSERT INTO cdko_experiment_design VALUES(2)');db.execute("INSERT INTO cdko_sgrna_counts VALUES(1,2,3,'RPE1','1;2','D14_1;D14_2','2;3','D28_1;D28_2')");db.commit();db.close()
            r=m.audit(p);self.assertFalse(r['primary_baseline_reproduced']);self.assertEqual(r['invalid_count_vectors'],0);self.assertEqual(r['unmatched_guides'],0)
