"""Visual-engine policy and measurement regressions, not aesthetic rankings."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import subprocess
import hashlib
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


class VisualEngineTests(unittest.TestCase):
    def correction(self,path='visual/artifacts/direction-a-1360.png'):
        record={k:'Synthetic validator test only' for k in ('problem','proposed_correction','justification','result','evaluation','regression')}
        record.update(id='synthetic-correction',original_design='field-editorial-a',status='validated',author='test-author',reviewer='test-reviewer',review_decision='APPROVED',split='development',regression_status='passed',result_evidence=[{'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'capture_manifest':'visual/artifacts/capture.json'}])
        return record
    def engine(self):
        path = ROOT / 'scripts/visual.py'
        self.assertTrue(path.exists(), 'visual engine is not implemented')
        spec = importlib.util.spec_from_file_location('odg_visual', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_reference_contrast_ratio(self):
        engine = self.engine()
        self.assertAlmostEqual(engine.contrast('#ffffff', '#000000'), 21)
        self.assertAlmostEqual(engine.contrast('#ffffff', '#ffffff'), 1)
        with self.assertRaises(ValueError):
            engine.contrast('oklch(0.5 0.2 30)', '#fff')

    def test_web_cannot_claim_native_apple_glass(self):
        engine = self.engine()
        self.assertTrue(engine.material_errors({'platform': 'web', 'class': 'native_official',
                                               'api': 'backdrop-filter', 'evidence': ['capture']}))
        self.assertEqual(engine.material_errors({'platform': 'web', 'class': 'stylized_glass',
                                                'api': 'backdrop-filter', 'evidence': ['capture']}), [])

    def test_material_fidelity_requires_rendered_evidence(self):
        engine = self.engine()
        self.assertTrue(engine.material_errors({'platform': 'android', 'class': 'simulated_dynamic_glass',
                                               'api': 'RuntimeShader', 'evidence': []}))

    def test_library_rejects_uninspected_or_unlicensed_reference(self):
        engine = self.engine()
        data = json.loads((ROOT / 'visual/data/development.json').read_text())
        item = copy.deepcopy(data[0])
        item['visual_reference']['inspected'] = False
        self.assertTrue(engine.reference_errors(ROOT, item))
        item = copy.deepcopy(data[0]); item['license']['redistribution_allowed'] = False
        self.assertTrue(engine.reference_errors(ROOT, item))

    def test_development_and_evaluation_cannot_share_reference_identity(self):
        engine = self.engine()
        record = json.loads((ROOT / 'visual/data/development.json').read_text())[0]
        self.assertTrue(engine.split_errors([record], [copy.deepcopy(record)]))

    def test_pending_or_self_approved_correction_cannot_be_promoted(self):
        engine = self.engine()
        correction = {'status': 'proposed', 'author': 'designer-a', 'reviewer': 'designer-a',
                      'review_decision': 'APPROVED', 'split': 'development',
                      'regression_status': 'not_run', 'result_evidence': []}
        self.assertTrue(engine.correction_errors(correction))

    def test_holdout_feedback_never_becomes_development_rule(self):
        engine = self.engine()
        correction = {'status': 'validated', 'author': 'designer-a', 'reviewer': 'reviewer-b',
                      'review_decision': 'APPROVED', 'split': 'evaluation',
                      'regression_status': 'passed', 'result_evidence': ['render-01']}
        self.assertTrue(engine.correction_errors(correction))

    def test_valid_feedback_requires_human_and_known_alternatives(self):
        engine = self.engine()
        feedback = {'id': 'pair-1', 'reviewer_kind': 'agent', 'reviewer_id': 'synthetic-test',
                    'alternatives': ['a', 'b'], 'choice': 'a', 'rationale': 'Observed task clarity',
                    'task': 'Find the booking action', 'presentation_order': ['a', 'b'],
                    'blind': True, 'context': {'viewport': [1280, 800]},
                    'consent_to_store': True}
        self.assertTrue(engine.feedback_errors(feedback, {'a', 'b'}))
        feedback['reviewer_kind'] = 'human'; feedback['choice'] = 'unknown'
        self.assertTrue(engine.feedback_errors(feedback, {'a', 'b'}))

    @unittest.skipUnless(importlib.util.find_spec('PIL'), 'optional visual dependencies absent')
    def test_pixel_diff_reports_measured_change_and_rejects_dimension_mismatch(self):
        from PIL import Image
        engine = self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            left, right = Path(temporary)/'left.png', Path(temporary)/'right.png'
            Image.new('RGB', (4, 4), 'white').save(left)
            Image.new('RGB', (4, 4), 'white').save(right)
            self.assertEqual(engine.pixel_diff(left, right)['changed_pixels'], 0)
            image = Image.open(right); image.putpixel((0, 0), (0, 0, 0)); image.save(right)
            self.assertEqual(engine.pixel_diff(left, right)['changed_pixels'], 1)
            Image.new('RGB', (5, 4), 'white').save(right)
            with self.assertRaises(ValueError): engine.pixel_diff(left, right)

    def test_current_visual_library_and_schemas_validate(self):
        self.assertEqual(self.engine().validate_library(ROOT), [])

    def test_important_art_direction_gets_separate_review_but_small_color_change_does_not(self):
        import routing
        defaults=json.loads((ROOT/'evaluations/routing.json').read_text())['defaults']
        result=routing.route({**defaults,'needs':['visual-direction'],'complexity':'medium'})
        self.assertEqual({s['skill'] for s in result['selected']},{'visual-art-director','visual-qa-auditor'})
        result=routing.route({**defaults,'needs':['color-science']})
        self.assertEqual({s['skill'] for s in result['selected']},{'color-science-engineer'})

    def test_antipattern_detection_needs_context_and_visible_evidence(self):
        engine=self.engine()
        self.assertTrue(engine.antipattern_errors({'id':'unnecessary-cards','context':'','evidence':[]},ROOT))
        records=json.loads((ROOT/'visual/data/observations.json').read_text())
        self.assertTrue(records)
        self.assertEqual(engine.antipattern_errors(records[0],ROOT),[])

    def test_cross_environment_pixels_cannot_be_treated_as_controlled_regression(self):
        engine=self.engine()
        self.assertTrue(engine.environment_errors({'browser':'one','viewport':[390,844]},
                                                  {'browser':'two','viewport':[390,844]}))

    def test_correction_cli_rejects_schema_bypass(self):
        record=self.correction();del record['id'];del record['author'];record['problem']=1
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'correction.json';path.write_text(json.dumps(record))
            result=subprocess.run([sys.executable,str(ROOT/'scripts/visual.py'),'check-correction',str(path)],capture_output=True,text=True)
            self.assertEqual(result.returncode,1,result.stdout+result.stderr)
            self.assertNotIn('Traceback',result.stderr)

    def test_correction_requires_manifest_bound_render_not_a_readme(self):
        self.assertTrue(self.engine().correction_errors(self.correction('README.md')))

    def test_known_holdout_image_cannot_be_promoted_by_relabeling_split(self):
        self.assertTrue(self.engine().correction_errors(self.correction('visual/artifacts/holdout.png')))

    @unittest.skipUnless(importlib.util.find_spec('PIL'),'optional visual dependencies absent')
    def test_valid_declared_correction_can_be_checked_without_promoting_it(self):
        self.assertEqual(self.engine().correction_errors(self.correction()),[])
        self.assertEqual(json.loads((ROOT/'visual/data/corrections.json').read_text()),[])

    def test_native_apple_material_requires_matching_api_platform_and_version(self):
        engine=self.engine()
        self.assertTrue(engine.material_errors({'platform':'ios','class':'native_official','api':'AppKit NSGlassEffectView','target_version':'26','evidence':['render']}))
        self.assertTrue(engine.material_errors({'platform':'ios','class':'native_official','api':'SwiftUI glassEffect','evidence':['render']}))

    @unittest.skipUnless(importlib.util.find_spec('PIL'),'optional visual dependencies absent')
    def test_material_pane_metric_excludes_changed_surrounding_pixels(self):
        from PIL import Image
        engine=self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            left,right=Path(temporary)/'left.png',Path(temporary)/'right.png'
            Image.new('RGB',(4,4),'white').save(left)
            image=Image.new('RGB',(4,4),'black')
            for x in (1,2):
                for y in (1,2):image.putpixel((x,y),(255,255,255))
            image.save(right)
            self.assertGreater(engine.pixel_diff(left,right)['changed_pixels'],0)
            self.assertEqual(engine.pixel_diff(left,right,region=[1,1,2,2])['changed_pixels'],0)


if __name__ == '__main__':
    unittest.main()
