"""Run documented file-copy recipes; do not equate copying with AI-client discovery."""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class DocumentationTests(unittest.TestCase):
    def test_front_pages_link_required_guides(self):
        for name,suffix in [('README.md',''),('README.es.md','.es')]:
            content=(ROOT/name).read_text(encoding='utf-8')
            self.assertIn(f'docs/installation{suffix}.md',content[:4500])
            self.assertIn(f'docs/quickstart{suffix}.md',content)
        for name in ('installation.md','installation.es.md'):
            self.assertIn('troubleshooting.md',(ROOT/'docs'/name).read_text(encoding='utf-8'))

    @unittest.skipUnless(shutil.which('sh') and os.name!='nt','POSIX recipe is tested only on POSIX hosts')
    def test_literal_posix_copy_recipe_and_collision_in_both_languages(self):
        for name in ('installation.md','installation.es.md'):
            content=(ROOT/'docs'/name).read_text(encoding='utf-8')
            blocks=re.findall(r'```bash\n(.*?)\n```',content,re.S)
            block=next(b for b in blocks if 'cp -R skills/scope-guardian' in b)
            with tempfile.TemporaryDirectory() as temporary:
                target=Path(temporary)/'project/.agents/skills'
                block=re.sub(r'(?m)^odg_target=.*$',lambda m:'odg_target="'+str(target)+'"',block)
                for attempt in range(2):
                    result=subprocess.run(['sh','-c',block],cwd=ROOT,capture_output=True,text=True)
                    self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                    path=target/'scope-guardian/SKILL.md'
                    self.assertTrue(path.is_file())
                    digest=hashlib.sha256(path.read_bytes()).hexdigest()
                    if attempt==0:before=digest
                    else:self.assertEqual(digest,before)

    @unittest.skipUnless(shutil.which('pwsh'),'PowerShell unavailable')
    def test_literal_powershell_copy_recipe_and_collision_in_both_languages(self):
        for name in ('installation.md','installation.es.md'):
            content=(ROOT/'docs'/name).read_text(encoding='utf-8')
            blocks=re.findall(r'```powershell\n(.*?)\n```',content,re.S)
            block=next(b for b in blocks if 'Copy-Item' in b)
            with tempfile.TemporaryDirectory() as temporary:
                target=Path(temporary)/'project/.agents/skills'
                block=re.sub(r"(?m)^\$odgTarget = '[^']*'",lambda m:"$odgTarget = '"+str(target).replace("'","''")+"'",block)
                script=Path(temporary)/'copy.ps1';script.write_text(block,encoding='utf-8')
                result=subprocess.run(['pwsh','-NoProfile','-File',str(script)],cwd=ROOT,capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                path=target/'scope-guardian/SKILL.md';before=path.read_bytes()
                result=subprocess.run(['pwsh','-NoProfile','-File',str(script)],cwd=ROOT,capture_output=True,text=True)
                self.assertNotEqual(result.returncode,0)
                self.assertEqual(path.read_bytes(),before)


if __name__=='__main__':unittest.main()
