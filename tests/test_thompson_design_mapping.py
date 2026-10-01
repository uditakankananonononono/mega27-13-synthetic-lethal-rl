import importlib.util,sqlite3,tempfile,unittest
from pathlib import Path
import openpyxl
s=importlib.util.spec_from_file_location('mapping',Path(__file__).resolve().parents[1]/'scripts'/'thompson_design_mapping.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class MappingTests(unittest.TestCase):
    def test_missing_single_does_not_get_filled_by_lookup(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.db';c=sqlite3.connect(p);c.executescript('CREATE TABLE cdko_experiment_design(sgRNA_id INTEGER,sgRNA_guide_name TEXT,sgRNA_guide_seq TEXT,sgRNA_target_name TEXT,study_origin TEXT); CREATE TABLE cdko_sgrna_counts(sgRNA_pair_id INTEGER,guide_1_id INTEGER,guide_2_id INTEGER,target_type TEXT,T0_counts TEXT,T0_replicate_names TEXT,cell_line_origin TEXT);')
            c.executemany('INSERT INTO cdko_experiment_design VALUES(?,?,?,?,?)',[(1,'A_G1','AAAA_1','A','1'),(2,'B_G1','CCCC_2','B','1'),(3,'FLUC_GRNA_1','GGGG_3','CONTROL','1')]);c.executemany('INSERT INTO cdko_sgrna_counts VALUES(?,?,?,?,?,?,?)',[(1,1,2,'Dual','1;2','BA_D14_R1;BA_D14_R2','A375'),(2,1,3,'Single','1;2','BA_D14_R1;BA_D14_R2','A375')]);c.commit();c.close()
            w=openpyxl.Workbook();s=w.active;s.title='4'
            for _ in range(4):s.append(['header'])
            s.append(['id','oligo','A_G1','AAAA','B_G1','CCCC','origin',1]);s.append(['id2','oligo','A_G1','AAAA','FLUC_GRNA_1','GGGG','origin',2]);xp=Path(d)/'x.xlsx';w.save(xp)
            r=m.audit(p,xp)['by_line']['A375'];self.assertEqual(len(r['dual_rows_missing_exact_single']),1);self.assertEqual(r['counts']['sequence_matched'],2)
