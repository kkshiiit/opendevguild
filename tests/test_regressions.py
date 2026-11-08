"""Regression cases for rejectable evidence, untrusted input and distribution safety."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import guild  # noqa: E402


class RegressionTests(unittest.TestCase):
    def fixture(self, parent):
        """Copy public source inputs only, never the workspace or its environment."""
        target = Path(parent) / 'source'
        target.mkdir()
        root_files = (
            'README.md', 'README.es.md', 'LICENSE', 'NOTICE', 'AGENTS.md',
            'CONTRIBUTING.md', 'CONTRIBUTING.es.md', 'SECURITY.md',
            'CODE_OF_CONDUCT.md', 'GOVERNANCE.md', 'CHANGELOG.md', 'pyproject.toml', 'uv.lock',
            'plugin.json', 'catalog.json', '.gitignore',
        )
        for name in root_files:
            source = ROOT / name
            if source.is_file():
                shutil.copy2(source, target / name)
        for name in ('.codex', 'skills', 'docs', 'contracts', 'examples', 'scripts',
                     'tests', 'evaluations', 'visual'):
            shutil.copytree(ROOT / name, target / name,
                            ignore=shutil.ignore_patterns('.git', '.venv', 'dist',
                                                         '__pycache__', '*.pyc'))
        self.assertFalse((target / '.venv').exists())
        return target

    def run_cli(self, root, *args):
        return subprocess.run(
            [sys.executable, str(root / 'scripts/guild.py'), '--root', str(root),
             *map(str, args)], cwd=root, capture_output=True, text=True,
        )

    def report(self):
        return json.loads((ROOT / 'examples/handoff.json').read_text(encoding='utf-8'))

    def check_report(self, report):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'report.json'
            path.write_text(json.dumps(report), encoding='utf-8')
            return self.run_cli(ROOT, 'check-handoff', path,
                                '--task', ROOT / 'examples/task.json')

    def finding(self, status):
        return {
            'severity': 'critical',
            'location': 'src/auth.py:42',
            'evidence': 'An isolated test reproduces unauthorized cross-tenant access.',
            'recommendation': 'Enforce resource ownership and rerun the regression.',
            'blocking': True,
            'status': status,
        }

    def test_malformed_frontmatter_reports_error_without_traceback(self):
        malformed = (
            '---\nname: [unterminated\n---\nBody\n',
            '---\n- a-list-is-not-a-mapping\n---\nBody\n',
            '---\nname: mission-control\nname: duplicate\n---\nBody\n',
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            skill = root / 'skills/mission-control/SKILL.md'
            for content in malformed:
                with self.subTest(content=content):
                    skill.write_text(content, encoding='utf-8')
                    result = self.run_cli(root, 'validate')
                    self.assertEqual(result.returncode, 1)
                    self.assertNotIn('Traceback', result.stdout + result.stderr)
                    self.assertIn('ERROR:', result.stdout)
                    self.assertIn('mission-control', result.stdout)

    def test_catalog_traversal_is_rejected_before_official_validator_reads(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            catalog_path = root / 'catalog.json'
            catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
            first_sector = next(iter(catalog['sectors']))
            catalog['sectors'][first_sector][0] = '../../outside'
            catalog_path.write_text(json.dumps(catalog), encoding='utf-8')
            # Spy prevents any external reads even in the vulnerable implementation.
            with mock.patch.object(guild, 'validate_skill', return_value=[]) as validate:
                errors = guild.validate_project(root)
            self.assertTrue(errors)
            validate.assert_not_called()

    def test_archive_contains_referenced_evaluation_readme(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            output = Path(temporary) / 'distribution.zip'
            result = self.run_cli(root, 'package', '--output', output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with zipfile.ZipFile(output) as archive:
                self.assertIn('evaluations/README.md', archive.namelist())

    def test_extracted_distribution_validates_without_source_environment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            output = Path(temporary) / 'distribution.zip'
            result = self.run_cli(root, 'package', '--output', output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            extracted = Path(temporary) / 'extracted'
            with zipfile.ZipFile(output) as archive:
                archive.extractall(extracted)
            self.assertFalse((extracted / '.venv').exists())
            self.assertFalse((extracted / '.git').exists())
            # Use the active interpreter; the extracted source has no source-checkout
            # imports or environment directory to conceal missing distribution files.
            result = self.run_cli(extracted, 'validate')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepted_report_rejects_open_blocking_finding(self):
        report = self.report()
        report['open_issues'] = [self.finding('open')]
        self.assertEqual(guild.schema_errors(ROOT, 'handoff.schema.json', report), [])
        result = self.check_report(report)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('blocking', result.stdout.lower())

    def test_accepted_report_allows_resolved_blocking_finding(self):
        report = self.report()
        report['open_issues'] = [self.finding('resolved')]
        result = self.check_report(report)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepted_report_rejects_failed_evidence_even_with_a_pass(self):
        report = self.report()
        failure = copy.deepcopy(report['evidence'][0])
        failure['outcome'] = 'failed'
        failure['detail'] = 'A second required check failed; the pass cannot erase it.'
        report['evidence'].append(failure)
        result = self.check_report(report)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_accepted_report_rejects_required_check_not_run(self):
        report = self.report()
        report['evidence'][0]['outcome'] = 'not_run'
        report['evidence'][0]['detail'] = 'Required environment unavailable.'
        result = self.check_report(report)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_accepted_report_rejects_unrun_required_check_even_with_a_pass(self):
        report = self.report()
        unrun = copy.deepcopy(report['evidence'][0])
        unrun['outcome'] = 'not_run'
        unrun['detail'] = 'Second required observation was not collected.'
        report['evidence'].append(unrun)
        result = self.check_report(report)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_verbatim_transcript_links_are_data_but_document_links_are_checked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            document = root / 'docs/verbatim.md'
            document.write_text('```text\n[verbatim](/unavailable-synthetic-file)\n```\n', encoding='utf-8')
            result = self.run_cli(root, 'validate')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            document.write_text('[broken](missing-file.md)\n', encoding='utf-8')
            result = self.run_cli(root, 'validate')
            self.assertEqual(result.returncode, 1)
            self.assertIn('missing-file.md', result.stdout)

    def test_evaluations_ancestor_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            displaced = Path(temporary) / 'external-evaluations'
            (root / 'evaluations').rename(displaced)
            (root / 'evaluations').symlink_to(displaced, target_is_directory=True)
            result = self.run_cli(root, 'validate')
            self.assertEqual(result.returncode, 1)
            self.assertIn('symlink', result.stdout)

    def test_source_directory_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            displaced = Path(temporary) / 'external-docs'
            (root / 'docs').rename(displaced)
            (root / 'docs').symlink_to(displaced, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                guild.source_files(root)

    def test_source_root_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(temporary)
            alias = Path(temporary) / 'linked-root'
            alias.symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                guild.source_files(alias)

    def test_existing_checksum_is_preserved_without_creating_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'distribution.zip'
            checksum = output.with_suffix('.zip.sha256')
            original = 'preserve the existing checksum\n'
            checksum.write_text(original, encoding='utf-8')
            result = self.run_cli(ROOT, 'package', '--output', output)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(output.exists())
            self.assertEqual(checksum.read_text(encoding='utf-8'), original)


if __name__ == '__main__':
    unittest.main()
