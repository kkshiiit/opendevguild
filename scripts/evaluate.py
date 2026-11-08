"""Score supplied routing observations; never fabricate or execute model responses."""
import argparse
import json
from pathlib import Path
import sys


def evaluate(fixture, observations):
    if not isinstance(fixture, dict) or not isinstance(fixture.get('cases'), list) \
            or not fixture['cases']:
        raise ValueError('cases must be a nonempty fixture array')
    cases = {}
    known = set()
    for case in fixture['cases']:
        if not isinstance(case, dict) or not isinstance(case.get('id'), str) \
                or not case['id'].strip() or case['id'] in cases:
            raise ValueError('fixture case IDs must be nonempty and unique')
        for field in ('expected', 'forbidden'):
            values = case.get(field)
            if not isinstance(values, list) or any(not isinstance(s, str) or not s.strip() for s in values) \
                    or len(set(values)) != len(values):
                raise ValueError(f'case {case["id"]} needs unique {field} skill names')
        if set(case['expected']) & set(case['forbidden']):
            raise ValueError('expected and forbidden skills must not overlap')
        if case.get('mode') not in ('FAST', 'STANDARD', 'CRITICAL') \
                or case.get('readiness') not in ('ready', 'blocked'):
            raise ValueError('fixture mode/readiness is invalid')
        cases[case['id']] = case
        known.update(case['expected'])
        known.update(case['forbidden'])
    if not isinstance(observations, dict) or observations.get('kind') not in (
            'deterministic-router', 'host-observations'):
        raise ValueError('observations must identify deterministic-router or host-observations provenance')
    predictions = observations.get('predictions')
    if not isinstance(predictions, list):
        raise ValueError('observations require a predictions array')
    indexed = {}
    for prediction in predictions:
        if not isinstance(prediction, dict) or set(prediction) != {'id', 'skills', 'mode', 'readiness'}:
            raise ValueError('prediction requires exactly id, skills, mode and readiness')
        identifier = prediction['id']
        if not isinstance(identifier, str) or identifier not in cases or identifier in indexed:
            raise ValueError('prediction IDs must be known and unique')
        skills = prediction['skills']
        if not isinstance(skills, list) or any(not isinstance(s, str) or s not in known for s in skills) \
                or len(set(skills)) != len(skills):
            raise ValueError('predicted skills must be known, unique names')
        if prediction['mode'] not in ('FAST', 'STANDARD', 'CRITICAL') \
                or prediction['readiness'] not in ('ready', 'blocked'):
            raise ValueError('prediction mode/readiness is invalid')
        indexed[identifier] = prediction
    if set(indexed) != set(cases):
        raise ValueError('predictions must cover every case exactly once; missing observations are not successes')

    true_positive = false_positive = false_negative = forbidden_hits = 0
    mismatches = []
    for identifier, case in cases.items():
        prediction = indexed[identifier]
        expected, actual = set(case['expected']), set(prediction['skills'])
        extra, missing = actual - expected, expected - actual
        forbidden = actual & set(case['forbidden'])
        true_positive += len(actual & expected)
        false_positive += len(extra)
        false_negative += len(missing)
        forbidden_hits += len(forbidden)
        if extra or missing or prediction['mode'] != case['mode'] or prediction['readiness'] != case['readiness']:
            mismatches.append({'id': identifier, 'extra': sorted(extra), 'missing': sorted(missing),
                               'forbidden': sorted(forbidden),
                               'mode_matches': prediction['mode'] == case['mode'],
                               'readiness_matches': prediction['readiness'] == case['readiness']})
    precision_denominator = true_positive + false_positive
    recall_denominator = true_positive + false_negative
    return {
        'kind': observations['kind'], 'samples': len(cases),
        'exact_matches': len(cases) - len(mismatches),
        'true_positive_activations': true_positive,
        'unnecessary_activations': false_positive, 'missed_activations': false_negative,
        'forbidden_activations': forbidden_hits,
        'selection_precision': true_positive / precision_denominator if precision_denominator else None,
        'selection_recall': true_positive / recall_denominator if recall_denominator else None,
        'mismatches': mismatches,
        'limitations': 'Metrics score supplied observations against these fixtures; they do not establish semantic activation or comparative skill effectiveness.',
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('predictions', type=Path, help='Measured records; never generated by this evaluator')
    parser.add_argument('--cases', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'evaluations/routing.json')
    args = parser.parse_args(argv)
    try:
        result = evaluate(json.loads(args.cases.read_text(encoding='utf-8')),
                          json.loads(args.predictions.read_text(encoding='utf-8')))
    except (OSError, ValueError, TypeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 1 if result['mismatches'] else 0


if __name__ == '__main__':
    sys.exit(main())
