import sys, unittest, tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import course
class TestCourse(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.p=Path(self.tmp.name)/'course'
    def tearDown(self): self.tmp.cleanup()
    def create(self,mode='full'):
        d=course.init(self.p,'测试课程',mode); (self.p/'e.md').write_text('测试证据',encoding='utf-8'); return d
    def approve(self,i): return course.approve(self.p,i,'用户已确认测试',['e.md'])
    def test_full(self):
        self.create(); self.assertEqual(course.next_stage(self.approve(1)),2)
    def test_quick(self):
        self.create('quick'); self.assertEqual(course.next_stage(self.approve(1)),2)
    def test_lesson(self):
        self.create('lesson'); self.approve(5); self.approve(6); self.assertIsNone(course.next_stage(self.approve(9)))
    def test_audit(self): self.create('audit'); self.assertIsNone(course.next_stage(self.approve(9)))
    def test_upgrade(self): self.create('upgrade'); self.assertEqual(course.next_stage(course.read(self.p)),9)
    def test_resume(self): self.create('resume'); self.approve(1); self.assertEqual(course.next_stage(course.read(self.p)),2)
    def test_no_overwrite(self):
        self.create(); self.assertRaises(ValueError,course.init,self.p,'其他','full')
    def test_no_skip(self): self.create(); self.assertRaises(ValueError,self.approve,2)
    def test_missing_evidence(self): self.create(); self.assertRaises(ValueError,course.approve,self.p,1,'确认',['missing.md'])
    def test_outside_evidence(self):
        self.create(); (self.p.parent/'outside.md').write_text('test'); self.assertRaises(ValueError,course.approve,self.p,1,'确认',['../outside.md'])
    def test_revise(self):
        self.create(); self.approve(1); self.approve(2); d=course.revise(self.p,1,'改变受众'); self.assertEqual(course.next_stage(d),1); self.assertEqual(d['stages']['2']['status'],'review'); self.assertFalse(d['publication_authorized']); self.assertEqual(len(d['history']),4)
    def test_empty_title(self): self.assertRaises(ValueError,course.init,self.p,' ','full')
    def test_no_permission(self): self.create(); self.assertFalse(self.approve(1)['publication_authorized'])
    def test_switch_and_resume(self):
        self.create('audit'); self.approve(9); self.assertEqual(course.switch_mode(self.p,'resume')['mode'],'audit'); self.assertEqual(course.next_stage(course.switch_mode(self.p,'full')),1)
    def test_validate(self): self.assertEqual(course.validate()['structure'],'pass')
if __name__=='__main__': unittest.main()
