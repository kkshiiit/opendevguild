"""Research records are provenance assertions, never fabricated empirical results."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ResearchTests(unittest.TestCase):
    def engine(self):
        path = ROOT / 'scripts/research.py'
        self.assertTrue(path.exists(), 'registry not implemented')
        spec = importlib.util.spec_from_file_location('research_registry', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def record(self):
        return {'id':'test-doc-v1','resource_type':'technical_document','url':'https://example.org/docs#intro',
                'observed_at':'2026-11-09','version':'v1','license':'unknown',
                'restrictions':['Reference only; no redistribution rights asserted'],
                'collection_method':'manual metadata observation','content_sha256':None,
                'level':'L1','technical_category':'testing','deduplication':'unprocessed',
                'evidence':[{'kind':'provenance','reference':'synthetic-test-observation','outcome':'observed'}],
                'rubric':{},'evaluation_result':None,'limitations':['Synthetic unit-test fixture']}

    def test_level_requires_matching_evidence_not_a_summary(self):
        engine = self.engine()
        for level in ('L2','L3','L4'):
            record=self.record();record['level']=level
            with self.subTest(level=level), self.assertRaises(ValueError):engine.validate(record)

    def test_complete_declared_evidence_can_pass_without_claiming_real_execution(self):
        record=self.record();record.update(level='L4',rubric={'criterion':'Synthetic test-only acceptance'},
                                          evaluation_result='Synthetic declaration, not a project benchmark')
        record['evidence'] += [
            {'kind':'content','reference':'synthetic-content','outcome':'observed','inspected':True},
            {'kind':'execution','reference':'synthetic-run','outcome':'passed','authorized':True},
            {'kind':'comparison','reference':'synthetic-comparison','outcome':'improved',
             'independent':True,'matched_conditions':True}]
        self.assertEqual(self.engine().validate(record),record)

    def test_url_credentials_and_unsafe_schemes_are_rejected(self):
        engine=self.engine()
        for url in ('file:///private/file','https://name:password@example.org/','https://example.org/?token=secret'):
            record=self.record();record['url']=url
            with self.subTest(url=url),self.assertRaises(ValueError):engine.validate(record)

    def test_canonical_url_deduplicates_without_double_counting(self):
        engine=self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            db=Path(temporary)/'registry.sqlite3';a=self.record();b=copy.deepcopy(a)
            b.update(id='alias',url='https://EXAMPLE.org:443/docs#other')
            outcome=engine.import_batch(db,[a,b])
            self.assertEqual(outcome['inserted'],1)
            self.assertEqual(outcome['duplicates'],1)
            self.assertEqual(engine.report(db)['total'],1)

    def test_content_hash_reuses_prior_analysis_and_prevents_downgrade(self):
        engine=self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            db=Path(temporary)/'registry.sqlite3';a=self.record();a['content_sha256']='a'*64
            engine.import_batch(db,[a]);b=copy.deepcopy(a)
            b.update(id='mirror',url='https://example.net/mirror',level='L0',evidence=[])
            self.assertEqual(engine.import_batch(db,[b])['duplicates'],1)
            self.assertEqual(engine.report(db)['by_level']['L1'],1)

    def test_explicit_new_version_retains_stronger_evidence_for_same_content(self):
        engine=self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            db=Path(temporary)/'registry.sqlite3';a=self.record();a['content_sha256']='a'*64
            engine.import_batch(db,[a]);b=copy.deepcopy(a)
            b.update(id='test-doc-v2',version='v2',level='L2',rubric={'criterion':'Synthetic content review'},
                     evaluation_result='Synthetic test-only declaration')
            b['evidence'].append({'kind':'content','reference':'synthetic-reviewed-content',
                                  'outcome':'observed','inspected':True})
            self.assertEqual(engine.import_batch(db,[b])['inserted'],1)
            report=engine.report(db)
            self.assertEqual(report['total'],2)
            self.assertEqual(report['by_level']['L1'],1)
            self.assertEqual(report['by_level']['L2'],1)
            self.assertEqual(report['unique_source_total'],1)
            self.assertEqual(report['known_unique_content'],1)

    def test_conflicting_identity_is_atomic_and_preserves_original(self):
        engine=self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            db=Path(temporary)/'registry.sqlite3';a=self.record();engine.import_batch(db,[a])
            b=copy.deepcopy(a);b['url']='https://example.net/other'
            with self.assertRaises(ValueError):engine.import_batch(db,[{**a,'id':'another','version':'v2'},b])
            self.assertEqual(engine.report(db)['total'],1)

    def test_stronger_evidence_is_not_silently_merged(self):
        engine=self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            db=Path(temporary)/'registry.sqlite3';a=self.record();engine.import_batch(db,[a]);b=copy.deepcopy(a)
            b.update(level='L0',evidence=[])
            result=engine.import_batch(db,[b]);self.assertEqual(result['duplicates'],1)
            self.assertEqual(engine.report(db)['by_level']['L1'],1)

    def test_sampling_is_seeded_stratified_and_bounded(self):
        engine=self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            db=Path(temporary)/'registry.sqlite3'
            records=[{**self.record(),'id':f'item-{i}','url':f'https://example.org/{i}',
                      'resource_type':'web_page' if i%2 else 'technical_document'} for i in range(8)]
            engine.import_batch(db,records)
            a=engine.sample(db,4,17);self.assertEqual(a,engine.sample(db,4,17))
            self.assertEqual(len(a),4);self.assertEqual(len({r['resource_type'] for r in a}),2)
            with self.assertRaises(ValueError):engine.sample(db,1001,17)

    def test_batch_limit_and_malformed_input_fail_before_creating_database(self):
        engine=self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            db=Path(temporary)/'registry.sqlite3'
            with self.assertRaises(ValueError):engine.import_batch(db,[self.record()]*1001)
            self.assertFalse(db.exists())

    def test_cli_batch_reader_rejects_oversized_input_before_parsing(self):
        engine=self.engine()
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'large.json'
            with path.open('wb') as stream:stream.truncate(8*1024*1024+1)
            with self.assertRaises(ValueError):engine.read_batch(path)

    def test_metadata_records_cannot_hide_large_content_bodies(self):
        record=self.record();record['limitations']=['x'*32769]
        with self.assertRaises(ValueError):self.engine().validate(record)

    def test_actual_seed_has_only_documented_provenance_levels(self):
        engine=self.engine();records=json.loads((ROOT/'evaluations/research-seed.json').read_text())
        self.assertEqual(len(records),len(json.loads((ROOT/'visual/sources.json').read_text())))
        for record in records:
            engine.validate(record);self.assertEqual(record['level'],'L1')


if __name__=='__main__':unittest.main()
