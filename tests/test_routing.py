"""Deterministic policy checks; these do not evaluate host semantic activation."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RoutingTests(unittest.TestCase):
    def module(self, name):
        path = ROOT / 'scripts' / f'{name}.py'
        self.assertTrue(path.is_file(), f'Missing executable policy: {path}')
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def fixtures(self):
        return json.loads((ROOT / 'evaluations/routing.json').read_text(encoding='utf-8'))

    def triage(self):
        fixture = self.fixtures()
        case = next(c for c in fixture['cases'] if c['id'] == 'frontend-engineer-single')
        return {**copy.deepcopy(fixture['defaults']), **copy.deepcopy(case['triage'])}

    def predictions(self):
        router, fixture = self.module('routing'), self.fixtures()
        records = []
        for case in fixture['cases']:
            decision = router.route({**copy.deepcopy(fixture['defaults']),
                                     **copy.deepcopy(case['triage'])})
            records.append({'id': case['id'], 'skills': [s['skill'] for s in decision['selected']],
                            'mode': decision['mode'], 'readiness': decision['readiness']})
        return {'kind': 'deterministic-router', 'predictions': records}

    def test_every_skill_has_five_activation_categories(self):
        fixture = self.fixtures()
        catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
        skills = {s for sector in catalog['sectors'].values() for s in sector}
        self.assertEqual(len(fixture['cases']), 170)
        self.assertEqual({c['target'] for c in fixture['cases']}, skills)
        self.assertEqual(len({c['id'] for c in fixture['cases']}), 170)
        for skill in skills:
            self.assertEqual({c['category'] for c in fixture['cases'] if c['target'] == skill},
                             {'positive', 'negative', 'ambiguous', 'multiple', 'single'})

    def test_routing_fixture_exact_selection_readiness_and_mode(self):
        router, fixture = self.module('routing'), self.fixtures()
        for case in fixture['cases']:
            with self.subTest(case=case['id']):
                result = router.route({**copy.deepcopy(fixture['defaults']),
                                       **copy.deepcopy(case['triage'])})
                selected = {item['skill'] for item in result['selected']}
                self.assertEqual(selected, set(case['expected']))
                self.assertFalse(selected.intersection(case['forbidden']))
                self.assertEqual(result['mode'], case['mode'])
                self.assertEqual(result['readiness'], case['readiness'])
                self.assertEqual(result['execution'], 'sequential')
                self.assertTrue(all(s['reason'].strip() for s in result['selected']))
                self.assertLess(len(selected), 34)
                self.assertEqual({s for stage in result['stages'] for s in stage['skills']}, selected)

    def test_high_risk_code_work_gets_relevant_critical_checks(self):
        router, triage = self.module('routing'), self.triage()
        triage['risk'] = 'high'
        triage['verification'] = True
        result = router.route(triage)
        selected = {s['skill'] for s in result['selected']}
        self.assertEqual(result['mode'], 'CRITICAL')
        self.assertTrue({'frontend-engineer', 'security-engineer', 'code-review-engineer'} <= selected)
        self.assertNotIn('database-engineer', selected)
        security_stage = next(i for i, stage in enumerate(result['stages'])
                              if 'security-engineer' in stage['skills'])
        review_stage = next(i for i, stage in enumerate(result['stages'])
                            if 'code-review-engineer' in stage['skills'])
        self.assertLess(security_stage, review_stage)

    def test_planning_readiness_is_distinct_from_collaboration_status(self):
        result = self.module('routing').route(self.triage())
        self.assertIn('readiness', result)
        self.assertNotIn('status', result)

    def test_critical_noncode_privacy_review_uses_scope_check_instead_of_code_review(self):
        router, triage = self.module('routing'), self.triage()
        triage.update({'needs': ['privacy'], 'task': 'review', 'risk': 'high', 'changes': 'none'})
        selected = {s['skill'] for s in router.route(triage)['selected']}
        self.assertEqual(selected, {'privacy-engineer', 'security-engineer', 'scope-guardian'})

    def test_unknown_stack_missing_tools_and_dependencies_do_not_infer_execution(self):
        router, base = self.module('routing'), self.triage()
        variants = [
            {'stack': {'name': 'unknown', 'confirmed': False}},
            {'tools': ['repository_read']},
            {'dependencies': [{'id': 'auth-policy', 'status': 'unresolved'}]},
        ]
        for changes in variants:
            with self.subTest(changes=changes):
                result = router.route({**copy.deepcopy(base), **changes})
                self.assertEqual(result['readiness'], 'blocked')
                self.assertTrue(result['missing_inputs'])
                self.assertNotIn('frontend-engineer', {s['skill'] for s in result['selected']})

    def test_all_ten_dimensions_and_bounded_needs_are_validated(self):
        router, triage = self.module('routing'), self.triage()
        required = ('product', 'task', 'risk', 'complexity', 'stack', 'dependencies',
                    'tools', 'research', 'changes', 'verification')
        for key in required:
            with self.subTest(missing=key):
                invalid = copy.deepcopy(triage)
                del invalid[key]
                with self.assertRaises(ValueError):
                    router.route(invalid)
        for updates in ({'risk': 'urgent'}, {'verification': 'yes'}, {'tools': 'shell'},
                        {'needs': ['not-a-purpose']}, {'needs': ['frontend'] * 7},
                        {'stack': {'name': 'unknown', 'confirmed': 'yes'}},
                        {'dependencies': [{'id': 'x', 'status': 'invented'}]},
                        {'unrecognized_field': 'must not become authority'}):
            with self.subTest(updates=updates):
                with self.assertRaises(ValueError):
                    router.route({**copy.deepcopy(triage), **updates})

    def test_evaluator_reports_actual_exact_matches_and_micro_metrics(self):
        evaluator = self.module('evaluate')
        metrics = evaluator.evaluate(self.fixtures(), self.predictions())
        self.assertEqual(metrics['samples'], 170)
        self.assertEqual(metrics['exact_matches'], 170)
        self.assertEqual(metrics['unnecessary_activations'], 0)
        self.assertEqual(metrics['missed_activations'], 0)
        self.assertEqual(metrics['selection_precision'], 1.0)
        self.assertEqual(metrics['selection_recall'], 1.0)
        self.assertEqual(metrics['mismatches'], [])

    def test_evaluator_detects_extra_missing_and_forbidden_selections(self):
        evaluator, fixture = self.module('evaluate'), self.fixtures()
        predictions = self.predictions()
        record = predictions['predictions'][0]
        expected_skill = record['skills'][0]
        extra = fixture['cases'][0]['forbidden'][0]
        record['skills'] = [extra]
        metrics = evaluator.evaluate(fixture, predictions)
        self.assertEqual(metrics['unnecessary_activations'], 1)
        self.assertEqual(metrics['missed_activations'], 1)
        self.assertEqual(metrics['forbidden_activations'], 1)
        self.assertEqual(metrics['exact_matches'], 169)
        self.assertLess(metrics['selection_precision'], 1)
        self.assertLess(metrics['selection_recall'], 1)
        self.assertIn(expected_skill, metrics['mismatches'][0]['missing'])

    def test_evaluator_rejects_missing_duplicate_or_unmeasured_predictions(self):
        evaluator, fixture = self.module('evaluate'), self.fixtures()
        predictions = self.predictions()
        incomplete = copy.deepcopy(predictions)
        incomplete['predictions'].pop()
        duplicate = copy.deepcopy(predictions)
        duplicate['predictions'].append(copy.deepcopy(duplicate['predictions'][0]))
        unknown = copy.deepcopy(predictions)
        unknown['predictions'][0]['skills'] = ['imaginary-agent']
        for invalid in (incomplete, duplicate, unknown, {'kind': 'estimated', 'predictions': []}):
            with self.subTest(invalid=invalid['kind']):
                with self.assertRaises(ValueError):
                    evaluator.evaluate(fixture, invalid)

    def test_router_and_evaluator_clis_consume_records_without_task_execution(self):
        self.module('routing')
        self.module('evaluate')
        with tempfile.TemporaryDirectory() as temporary:
            triage_path = Path(temporary) / 'triage.json'
            triage_path.write_text(json.dumps(self.triage()), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/routing.py'), str(triage_path)],
                                    capture_output=True, text=True, cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)['mode'], 'FAST')
            prediction_path = Path(temporary) / 'predictions.json'
            prediction_path.write_text(json.dumps(self.predictions()), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/evaluate.py'), str(prediction_path),
                                     '--cases', str(ROOT / 'evaluations/routing.json')],
                                    capture_output=True, text=True, cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)['samples'], 170)


if __name__ == '__main__':
    unittest.main()
