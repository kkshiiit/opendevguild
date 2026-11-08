"""Executable lifecycle and gate requirements from the complete master brief."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import guild


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.task = json.loads((ROOT / 'examples/task.json').read_text())
        self.report = json.loads((ROOT / 'examples/handoff.json').read_text())

    def test_all_six_lifecycle_states_exist(self):
        schema = json.loads((ROOT / 'contracts/handoff.schema.json').read_text())
        self.assertEqual(set(schema['properties']['status']['enum']),
                         {'NOT_STARTED', 'IN_PROGRESS', 'BLOCKED', 'NEEDS_REVIEW', 'VERIFIED', 'FAILED'})

    def test_verified_requires_reviewer_other_than_producer(self):
        self.report['verification']['reviewer'] = self.report['producer']
        errors = guild.check_handoff(ROOT, self.task, self.report)
        self.assertTrue(any('reviewer' in e for e in errors), errors)

    def test_unreviewed_work_can_be_handed_off_without_verified_claim(self):
        self.report['status'] = 'NEEDS_REVIEW'
        self.report['verification'] = None
        self.assertEqual(guild.check_handoff(ROOT, self.task, self.report), [])

    def test_verified_rejects_blocked_gate(self):
        self.report['gates'][0]['status'] = 'BLOCKED'
        self.assertTrue(guild.check_handoff(ROOT, self.task, self.report))

    def test_not_applicable_requires_justification(self):
        self.report['gates'][1]['status'] = 'NOT_APPLICABLE'
        self.report['gates'][1]['justification'] = ''
        self.assertTrue(guild.check_handoff(ROOT, self.task, self.report))

    def test_gate_approval_needs_evidence_and_observation_basis(self):
        self.report['gates'][0]['status'] = 'APPROVED'
        self.report['gates'][0]['evidence'] = []
        self.assertTrue(guild.check_handoff(ROOT, self.task, self.report))

    def test_verified_rejects_unresolved_dependency(self):
        self.task['dependencies'] = [{'task_id': 'prerequisite', 'status': 'blocked', 'artifacts': []}]
        self.report['dependencies'] = copy.deepcopy(self.task['dependencies'])
        self.assertTrue(guild.check_handoff(ROOT, self.task, self.report))

    def test_required_exchange_fields_are_present(self):
        for name in ('task_id', 'objective', 'scope', 'inputs', 'assumptions', 'dependencies',
                     'files_involved', 'action_taken', 'evidence', 'tests', 'risks',
                     'open_issues', 'status'):
            report = copy.deepcopy(self.report)
            del report[name]
            self.assertTrue(guild.check_handoff(ROOT, self.task, report), name)

    def test_duplicate_or_unknown_gates_cannot_replace_required_gate(self):
        self.report['gates'][1] = copy.deepcopy(self.report['gates'][0])
        self.assertTrue(guild.check_handoff(ROOT, self.task, self.report))

    def test_report_cannot_silently_change_authorized_scope(self):
        self.report['scope']['write_paths'] = ['unrelated/']
        self.assertTrue(guild.check_handoff(ROOT, self.task, self.report))

    def test_referenced_yaml_configuration_syntax_is_checked(self):
        import shutil
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'repo'
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('.git', '.venv', 'dist', '__pycache__'))
            config = target / '.github/broken.yml'
            config.write_text('jobs: [unterminated\n', encoding='utf-8')
            errors = guild.validate_project(target)
            self.assertTrue(any('invalid YAML' in error for error in errors), errors)


if __name__ == '__main__':
    unittest.main()
