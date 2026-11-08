"""Behavioral regression tests for local tooling; no model quality claims."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'scripts' / 'guild.py'


class ToolingTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), *map(str, args)],
                              capture_output=True, text=True, cwd=ROOT)

    def test_rejects_accepted_handoff_without_required_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = json.loads((ROOT / 'examples/handoff.json').read_text())
            report['evidence'] = []
            path = Path(tmp) / 'report.json'
            path.write_text(json.dumps(report))
            result = self.run_cli('check-handoff', path, '--task', ROOT / 'examples/task.json')
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('evidence', result.stdout)

    def test_rejects_task_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = json.loads((ROOT / 'examples/handoff.json').read_text())
            report['task_id'] = 'different-task'
            path = Path(tmp) / 'report.json'
            path.write_text(json.dumps(report))
            result = self.run_cli('check-handoff', path, '--task', ROOT / 'examples/task.json')
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn('task_id', result.stdout)

    def test_accepts_valid_handoff(self):
        result = self.run_cli('check-handoff', ROOT / 'examples/handoff.json',
                              '--task', ROOT / 'examples/task.json')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_package_is_reproducible_and_excludes_private_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            one, two = Path(tmp) / 'one.zip', Path(tmp) / 'two.zip'
            for target in (one, two):
                result = self.run_cli('package', '--output', target)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(one.read_bytes(), two.read_bytes())
            with zipfile.ZipFile(one) as archive:
                names = archive.namelist()
                self.assertIn('plugin.json', names)
                self.assertIn('LICENSE', names)
                self.assertEqual(sum(n.endswith('/SKILL.md') for n in names), 34)
                self.assertFalse(any(n.startswith(('.git/', '.venv/', 'dist/')) for n in names))
            checksum = one.with_suffix('.zip.sha256').read_text().split()[0]
            self.assertEqual(checksum, hashlib.sha256(one.read_bytes()).hexdigest())

    def test_package_refuses_to_overwrite_existing_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'existing.zip'
            target.write_text('preserve me')
            result = self.run_cli('package', '--output', target)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(target.read_text(), 'preserve me')


if __name__ == '__main__':
    unittest.main()
