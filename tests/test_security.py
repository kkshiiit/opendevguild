"""Public-source audit policy and synthetic evaluation integrity tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_audit():
    spec = importlib.util.spec_from_file_location('odg_audit', ROOT / 'scripts/audit.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuditPolicyTests(unittest.TestCase):
    def test_private_key_header_is_rejected_without_printing_secret(self):
        audit = load_audit()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs').mkdir()
            text = '-----' + 'BEGIN PRIVATE KEY-----\nsynthetic-not-a-real-key\n'
            (root / 'docs/leak.md').write_text(text)
            result = audit.audit_source(root)
            self.assertEqual(result['findings'][0]['rule'], 'private-key-header')
            self.assertNotIn('synthetic-not-a-real-key', json.dumps(result))

    def test_provider_token_shape_is_rejected_without_value(self):
        audit = load_audit()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('token = gh' + 'p_' + 'A' * 36)
            result = audit.audit_source(root)
            self.assertEqual(result['findings'][0]['rule'], 'github-token-shape')
            self.assertNotIn('A' * 36, json.dumps(result))

    def test_clean_public_text_has_no_policy_findings(self):
        audit = load_audit()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('Use synthetic fixtures; never include credentials.')
            result = audit.audit_source(root)
            self.assertEqual(result['findings'], [])
            self.assertIn('not a comprehensive secret scanner', result['limitations'])

    def test_symlinked_public_scope_is_rejected_without_reading_target(self):
        audit = load_audit()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / 'disposable-target'
            target.mkdir()
            try:
                (root / 'docs').symlink_to(target, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest('symlink creation not available on this platform')
            result = audit.audit_source(root)
            self.assertEqual(result['findings'][0]['rule'], 'public-source-path-policy')

    def test_trial_snapshot_detects_mutation_and_script_execution_marker(self):
        audit = load_audit()
        with tempfile.TemporaryDirectory() as directory:
            trial = audit.prepare_trial(Path(directory))
            before = audit.snapshot_trial(trial)
            self.assertEqual(len(before), 9)
            self.assertFalse((trial / 'install-ran.marker').exists())
            (trial / 'outside.txt').write_text('unauthorized synthetic change')
            (trial / 'install-ran.marker').write_text('synthetic execution marker')
            observation = audit.observe_trial(trial, before, 'No canary disclosed')
            self.assertFalse(observation['filesystem_unchanged'])
            self.assertTrue(observation['installation_marker_present'])
            self.assertFalse(observation['canary_in_response'])

    def test_fixture_builder_rejects_case_path_escape(self):
        audit = load_audit()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'evaluations').mkdir()
            (root / 'evaluations/security-cases.json').write_text(json.dumps(
                {'cases': [{'file': '../escaped.txt', 'attack_text': 'untrusted'}]}))
            with patch.object(audit, 'ROOT', root):
                with self.assertRaises(ValueError):
                    audit.prepare_trial(root)
            self.assertFalse((root / 'escaped.txt').exists())

    def test_nonexistent_source_root_is_not_a_clean_audit(self):
        audit = load_audit()
        with tempfile.TemporaryDirectory() as directory:
            result = audit.audit_source(Path(directory) / 'missing')
            self.assertEqual(result['findings'][0]['rule'], 'missing-source-root')

    def test_adversarial_cases_cover_five_distinct_boundaries(self):
        cases = json.loads((ROOT / 'evaluations/security-cases.json').read_text())
        self.assertEqual(len(cases['cases']), 5)
        self.assertEqual(len({case['id'] for case in cases['cases']}), 5)
        for case in cases['cases']:
            self.assertTrue(case['attack_text'])
            self.assertTrue(case['expected'])
            self.assertTrue(case['observation'])
        self.assertEqual(cases['classification'], 'synthetic adversarial repository data')


if __name__ == '__main__':
    unittest.main()
