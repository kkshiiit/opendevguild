"""Bounded specialist selection from caller-classified triage; never executes tasks."""
import argparse
import json
from pathlib import Path
import sys


# Purpose -> (skill, ordered stage). These are domain responsibilities, not tools.
PURPOSES = {
    'coordinate': ('mission-control', 0),
    'scope': ('scope-guardian', 1),
    'repository': ('repository-intelligence', 2),
    'delivery': ('delivery-planner', 3),
    'product': ('product-discovery', 2),
    'requirements': ('requirements-engineer', 2),
    'ux': ('ux-research-design', 4),
    'ui': ('ui-design-system', 4),
    'accessibility': ('accessibility-engineer', 4),
    'architecture': ('system-architect', 4),
    'adr': ('architecture-decisions', 4),
    'database': ('database-engineer', 4),
    'api': ('api-contract-engineer', 4),
    'frontend': ('frontend-engineer', 5),
    'backend': ('backend-engineer', 5),
    'mobile': ('mobile-engineer', 5),
    'desktop': ('desktop-engineer', 5),
    'game-design': ('game-design-engineer', 4),
    'gameplay': ('gameplay-engineer', 5),
    'implementation': ('implementation-engineer', 5),
    'review': ('code-review-engineer', 7),
    'test-strategy': ('test-strategy-engineer', 4),
    'test-automation': ('qa-automation-engineer', 6),
    'performance': ('performance-engineer', 7),
    'security': ('security-engineer', 4),
    'privacy': ('privacy-engineer', 4),
    'supply-chain': ('supply-chain-auditor', 4),
    'ci': ('devops-ci-engineer', 8),
    'release': ('release-engineer', 8),
    'observability': ('observability-engineer', 8),
    'incident': ('incident-response-engineer', 1),
    'documentation': ('documentation-engineer', 9),
    'skill-evaluation': ('skill-quality-evaluator', 7),
    'community': ('community-maintainer', 9),
    'visual-direction': ('visual-art-director', 4),
    'visual-reference': ('visual-reference-analyst', 2),
    'color-science': ('color-science-engineer', 4),
    'typography': ('typography-composition-engineer', 4),
    'materials': ('material-rendering-engineer', 5),
    'motion': ('motion-interaction-engineer', 5),
    'design-code': ('design-to-code-engineer', 5),
    'visual-qa': ('visual-qa-auditor', 7),
}
STAGES = {
    0: 'coordination', 1: 'scope-and-containment', 2: 'investigation',
    3: 'delivery-plan', 4: 'design-and-risk-controls', 5: 'implementation',
    6: 'automated-verification', 7: 'independent-review', 8: 'operations',
    9: 'documentation-and-maintenance',
}
PRODUCTS = {'general', 'web', 'backend', 'mobile', 'desktop', 'game', 'data', 'library', 'unknown'}
TASKS = {'analyze', 'plan', 'design', 'implement', 'review', 'test', 'operate',
         'release', 'evaluate', 'maintain', 'investigate', 'discover', 'unknown'}
TOOLS = {'repository_read', 'file_write', 'test_runner', 'subagents', 'browser', 'network'}
PLATFORMS = {'frontend': {'web'}, 'mobile': {'mobile'}, 'desktop': {'desktop'},
             'game-design': {'game'}, 'gameplay': {'game'}}
REQUIRED = {'product', 'task', 'risk', 'complexity', 'stack', 'dependencies',
            'tools', 'research', 'changes', 'verification', 'needs'}


def string_list(value, label, allowed=None, maximum=None):
    if not isinstance(value, list) or any(not isinstance(s, str) or not s.strip() for s in value):
        raise ValueError(f'{label} must be an array of nonempty strings')
    if len(set(value)) != len(value):
        raise ValueError(f'{label} must not contain duplicate values')
    if maximum is not None and len(value) > maximum:
        raise ValueError(f'{label} must have at most {maximum} values')
    if allowed is not None and any(s not in allowed for s in value):
        raise ValueError(f'{label} contains an unsupported value')


def validate_triage(triage):
    if not isinstance(triage, dict):
        raise ValueError('triage must be an object')
    if REQUIRED - triage.keys() or triage.keys() - REQUIRED - {'ambiguities'}:
        raise ValueError('triage must contain exactly the documented dimensions, needs and optional ambiguities')
    enums = {'product': PRODUCTS, 'task': TASKS, 'risk': {'low', 'medium', 'high'},
             'complexity': {'simple', 'medium', 'complex'},
             'research': {'none', 'repository', 'external', 'user'},
             'changes': {'none', 'code', 'docs', 'config'}}
    for field, allowed in enums.items():
        if not isinstance(triage[field], str) or triage[field] not in allowed:
            raise ValueError(f'{field} contains an unsupported value')
    if type(triage['verification']) is not bool:
        raise ValueError('verification must be boolean')
    stack = triage['stack']
    if not isinstance(stack, dict) or set(stack) != {'name', 'confirmed'} \
            or not isinstance(stack['name'], str) or not stack['name'].strip() \
            or type(stack['confirmed']) is not bool:
        raise ValueError('stack requires a nonempty name and boolean confirmed')
    string_list(triage['needs'], 'needs', PURPOSES, maximum=6)
    string_list(triage['tools'], 'tools', TOOLS)
    string_list(triage.get('ambiguities', []), 'ambiguities', maximum=10)
    dependencies = triage['dependencies']
    if not isinstance(dependencies, list) or len(dependencies) > 30:
        raise ValueError('dependencies must be an array with at most 30 entries')
    ids = []
    for dependency in dependencies:
        if not isinstance(dependency, dict) or set(dependency) != {'id', 'status'} \
                or not isinstance(dependency['id'], str) or not dependency['id'].strip() \
                or dependency['status'] not in ('ready', 'unresolved'):
            raise ValueError('dependencies require nonempty id and ready/unresolved status')
        ids.append(dependency['id'])
    if len(set(ids)) != len(ids):
        raise ValueError('dependency IDs must be unique')


def route(triage):
    """Return an ordered recommendation from explicit classifications, without I/O."""
    validate_triage(triage)
    needs, tools = triage['needs'], set(triage['tools'])
    mode = 'CRITICAL' if triage['risk'] == 'high' else (
        'FAST' if triage['risk'] == 'low' and triage['complexity'] == 'simple'
        and len(needs) <= 1 else 'STANDARD')
    missing = list(triage.get('ambiguities', []))
    if triage['product'] == 'unknown' or triage['task'] == 'unknown' or not needs:
        missing.append('Confirm product, task and at least one bounded specialty need.')
    for need in needs:
        if need in PLATFORMS and triage['product'] not in PLATFORMS[need]:
            missing.append(f'Confirm a compatible product target for {need}.')
    if triage['changes'] == 'code' and not triage['stack']['confirmed']:
        missing.append('Inspect repository evidence to confirm the implementation stack.')
    if triage['changes'] != 'none' and 'file_write' not in tools:
        missing.append('Authorized file_write capability is unavailable.')
    if triage['changes'] != 'none' and 'repository_read' not in tools:
        missing.append('Repository inspection capability is unavailable for the proposed change.')
    if triage['verification'] and 'test_runner' not in tools:
        missing.append('Requested executable verification lacks an available test_runner.')
    for dependency in triage['dependencies']:
        if dependency['status'] == 'unresolved':
            missing.append(f"Resolve dependency: {dependency['id']}.")
    if triage['research'] == 'repository' and 'repository_read' not in tools:
        missing.append('Repository research lacks repository_read capability.')
    if triage['research'] == 'external' and 'network' not in tools:
        missing.append('External research lacks network capability.')

    chosen = {}

    def add(purpose, reason):
        skill, order = PURPOSES[purpose]
        if skill in chosen:
            chosen[skill]['reason'] += ' ' + reason
        else:
            chosen[skill] = {'skill': skill, 'reason': reason, 'order': order}

    if missing:
        purpose = 'repository' if 'repository_read' in tools else 'requirements'
        add(purpose, 'Minimal investigation or clarification only; requested work remains blocked.')
    else:
        for need in needs:
            add(need, f'Caller explicitly identified the {need} responsibility for this task.')
        if 'visual-direction' in needs and (triage['complexity'] != 'simple' or triage['risk'] == 'high'):
            add('visual-qa', 'Important visual directions require a separate reviewer; the art director cannot self-approve.')
        if triage['research'] in ('repository', 'external'):
            add('repository', f"Caller requested {triage['research']} investigation using available capabilities.")
        elif triage['research'] == 'user':
            add('product', 'Caller requested user/problem research; no participant findings are assumed.')
        if triage['verification'] and triage['changes'] in ('code', 'config'):
            add('review', 'Requested verification of a code/configuration change needs independent review.')
        if mode == 'CRITICAL':
            add('security', 'High declared risk requires security controls before dependent work.')
            if triage['changes'] in ('code', 'config') or triage['task'] == 'implement' or 'review' in needs:
                add('review', 'High-risk implementation or review requires an independent change review.')
            else:
                add('scope', 'High-risk non-code work needs explicit scope and authorization verification.')

    ordered = sorted(chosen.values(), key=lambda item: (item['order'], item['skill']))
    stages = []
    for order in sorted({item['order'] for item in ordered}):
        stages.append({'name': STAGES[order],
                       'skills': [item['skill'] for item in ordered if item['order'] == order]})
    return {
        'readiness': 'blocked' if missing else 'ready', 'mode': mode,
        'execution': 'sequential',
        'selected': [{'skill': item['skill'], 'reason': item['reason']} for item in ordered],
        'stages': stages, 'missing_inputs': missing,
        'limitations': ['Caller-supplied classifications are not natural-language activation evidence.',
                        'Recommendations grant no tools, permissions, spawning or publication authority.'],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('triage', type=Path, help='Explicit structured triage JSON; no task text is executed')
    args = parser.parse_args(argv)
    try:
        result = route(json.loads(args.triage.read_text(encoding='utf-8')))
    except (OSError, ValueError, TypeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
