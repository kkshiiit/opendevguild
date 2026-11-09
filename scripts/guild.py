"""Local policy, evidence contracts and deterministic packaging (not a runtime)."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tomllib
import zipfile

from jsonschema import Draft202012Validator
from skills_ref import find_skill_md
from skills_ref.errors import ParseError
from skills_ref.validator import validate_metadata
from skills_ref.parser import parse_frontmatter
from strictyaml import dirty_load, YAMLError

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = (
    'Activation', 'Do not activate', 'Objective', 'Required inputs',
    'Tools and permissions', 'Procedure', 'Outputs', 'Handoffs',
    'Verification', 'Failure and escalation', 'Boundaries', 'Example',
    'Preconditions', 'Output format', 'Test cases',
)
# Deliberate source allowlist; never archive the workspace or a Git checkout wholesale.
ROOT_FILES = ('README.md', 'README.es.md', 'LICENSE', 'NOTICE', 'AGENTS.md',
              'CONTRIBUTING.md', 'CONTRIBUTING.es.md', 'SECURITY.md',
              'CODE_OF_CONDUCT.md', 'GOVERNANCE.md', 'CHANGELOG.md', 'pyproject.toml', 'uv.lock',
              'plugin.json', 'catalog.json', '.gitignore', '.gitattributes')
DIRECTORIES = ('.github', 'skills', 'docs', 'contracts', 'examples', 'scripts', 'tests',
               'evaluations', 'visual')
EXTENSIONS = {'.md', '.json', '.py', '.toml', '.lock', '.yml', '.yaml'}
AGENT_NAMES = ('architect', 'product-analyst', 'designer', 'implementer',
               'reviewer', 'qa-specialist', 'security-specialist', 'release-specialist')


def validate_skill(directory):
    """Use official parsing/validation with explicit UTF-8 on every host.

    Upstream's demonstration file wrapper uses the platform default encoding,
    which failed on Windows CP1252. No specification checks are reimplemented.
    """
    path=find_skill_md(directory)
    if path is None:return ['Missing required file: SKILL.md']
    try:metadata,_=parse_frontmatter(path.read_text(encoding='utf-8'))
    except (ParseError,UnicodeError,OSError) as error:return [str(error)]
    return validate_metadata(metadata,directory)


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def schema_errors(root, schema_name, data):
    schema = read_json(root / 'contracts' / schema_name)
    Draft202012Validator.check_schema(schema)
    return [f"{'/'.join(map(str, e.absolute_path)) or '$'}: {e.message}"
            for e in Draft202012Validator(schema).iter_errors(data)]


def safe_relative(value):
    path = PurePosixPath(value)
    return bool(value.strip()) and not path.is_absolute() and '..' not in path.parts \
        and '\\' not in value and ':' not in value


def markdown_prose(content):
    """Exclude verbatim code/transcripts from documentation link checking."""
    lines, fence = [], None
    for line in content.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if match:
            marker, remainder = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not remainder.strip():
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return '\n'.join(lines)


def check_handoff(root, task, report):
    errors = schema_errors(root, 'task.schema.json', task)
    errors += schema_errors(root, 'handoff.schema.json', report)
    if errors:
        return errors
    if report['task_id'] != task['id']:
        errors.append('task_id does not match the authorized task')
    criteria = {c['id']: c for c in task['acceptance_criteria']}
    if len(criteria) != len(task['acceptance_criteria']):
        errors.append('acceptance_criteria contains duplicate IDs')
    for field in ('objective', 'scope', 'dependencies', 'inputs'):
        if report[field] != task[field]:
            errors.append(f'{field} differs from the authorized task')
    for path in report['files_involved']:
        if not safe_relative(path):
            errors.append(f'unsafe artifact path: {path!r}')
    for evidence in report['evidence']:
        if evidence['criterion_id'] not in criteria:
            errors.append('evidence references an unknown criterion_id')
    gate_ids = [g['gate'] for g in report['gates']]
    if len(gate_ids) != len(set(gate_ids)):
        errors.append('duplicate quality gates')
    passed = {e['criterion_id'] for e in report['evidence'] if e['outcome'] == 'passed'}
    for gate in report['gates']:
        if any(ref not in passed for ref in gate['evidence']):
            errors.append('gate evidence must reference passed criteria')
    if report['status'] == 'VERIFIED':
        if any(f['blocking'] and f['status'] == 'open' for f in report['open_issues']):
            errors.append('findings contain an open blocking finding')
        if any(d['status'] != 'ready' for d in task['dependencies']):
            errors.append('required dependency is not ready')
        review = report['verification']
        if review is None:
            errors.append('VERIFIED requires a reviewer record')
        elif review['reviewer'] == report['producer'] or not review['independent']:
            errors.append('reviewer must be independent of the producer')
        elif any(ref not in passed for ref in review['evidence']):
            errors.append('reviewer evidence must reference passed criteria')
        required_gates = {'Requirements', 'Architecture', 'Implementation', 'Verification', 'Security', 'Release'}
        if set(gate_ids) != required_gates:
            errors.append('VERIFIED requires all six quality gates')
        if any(g['status'] not in ('APPROVED', 'NOT_APPLICABLE') for g in report['gates']):
            errors.append('unapproved gate blocks VERIFIED')
        if any(t['outcome'] == 'failed' for t in report['tests']):
            errors.append('failed test blocks VERIFIED')
        for criterion in criteria.values():
            matching = [e for e in report['evidence']
                        if e['criterion_id'] == criterion['id']]
            if criterion['required'] and not any(e['outcome'] == 'passed' for e in matching):
                errors.append(f"evidence missing for required criterion: {criterion['id']}")
            if criterion['required'] and any(e['outcome'] != 'passed' for e in matching):
                errors.append(f"required evidence unresolved: {criterion['id']}")
    return errors


def claude_adapter_files(root):
    """Allowlist native adapter sources without admitting private client state."""
    if root.is_symlink() or getattr(root, 'is_junction', lambda: False)():
        raise ValueError('linked Claude adapter root is not distributable')
    # Claude also auto-discovers these even when the manifest omits them.
    # This adapter deliberately supports skills + one reviewer only.
    for name in ('.mcp.json', '.lsp.json', 'settings.json', 'hooks', 'commands',
                 'workflows', 'monitors', 'output-styles', 'themes'):
        path = root / name
        if path.exists() or path.is_symlink():
            raise ValueError(f'Unreviewed auto-discovered Claude component: {name}')
    files = []
    for name in ('.claude-plugin/plugin.json', 'agents/reviewer.md'):
        path = root / name
        if any(p.is_symlink() or getattr(p, 'is_junction', lambda: False)()
               for p in (path.parent, path)):
            raise ValueError('linked Claude adapter path is not distributable')
        if path.parent.exists() and not path.parent.is_dir():
            raise ValueError('Claude adapter parent must be a directory')
        if path.exists() and not path.is_file():
            raise ValueError('Non-regular Claude adapter file rejected')
        if path.is_file():
            files.append(path)
    return files


def source_files(root):
    """Reject symlinks, including directory links, before inspecting content."""
    if root.is_symlink():
        raise ValueError('symlink source root is not distributable')
    files = []
    for name in ROOT_FILES:
        path = root / name
        if path.is_symlink():
            raise ValueError(f'symlink is not distributable: {name}')
        if path.is_file():
            files.append(path)
    # Include only explicit project profiles, never .codex/auth.json or other state.
    for name in AGENT_NAMES:
        path = root / '.codex' / 'agents' / f'{name}.toml'
        if any(p.is_symlink() for p in (root / '.codex', path.parent, path)):
            raise ValueError('symlink in agent configuration path')
        if path.is_file():
            files.append(path)
    # Explicit native Claude adapter files only, never .claude user settings,
    # credentials, caches or arbitrary .claude-plugin state.
    files.extend(claude_adapter_files(root))
    for name in DIRECTORIES:
        directory = root / name
        if directory.is_symlink():
            raise ValueError(f'symlink is not distributable: {name}')
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob('*')):
            if path.is_symlink():
                raise ValueError(f'symlink is not distributable: {path.relative_to(root)}')
            if '__pycache__' in path.parts:
                continue
            if path.is_file():
                is_visual = path.relative_to(root).parts[0] == 'visual'
                visual_types = {'.html', '.css', '.png', '.webm'} if is_visual else set()
                if path.name.startswith('.') or path.suffix not in EXTENSIONS | visual_types:
                    raise ValueError(f'unreviewed file type: {path.relative_to(root)}')
                files.append(path)
    return sorted(set(files), key=lambda p: p.relative_to(root).as_posix())


def validate_claude_plugin(root, version):
    """Conservative project policy, not Claude's authoritative native validator."""
    errors = []
    try:
        claude_adapter_files(root)
        manifest = read_json(root / '.claude-plugin/plugin.json')
        expected = {'name': 'opendevguild', 'version': version,
                    'author': {'name': 'OpenDevGuild contributors'},
                    'repository': 'https://github.com/kkshiiit/opendevguild',
                    'license': 'Apache-2.0', 'agents': ['./agents/reviewer.md']}
        if not isinstance(manifest, dict) or set(manifest) != set(expected) | {'description'}:
            return ['Claude manifest must use the reviewed minimal field set (no implicit capabilities)']
        for key, value in expected.items():
            if manifest[key] != value:
                errors.append(f'Claude manifest: unexpected {key}')
        if not isinstance(manifest['description'], str) or not manifest['description'].strip():
            errors.append('Claude manifest needs a description')
        # Never resolve untrusted manifest paths. Only the reviewed fixed agent
        # file is inspected, after source_files has guarded its ancestors.
        content = (root / 'agents/reviewer.md').read_text(encoding='utf-8')
        if not content.startswith('---\n'):
            return errors + ['Claude reviewer needs YAML frontmatter']
        header, body = content[4:].split('\n---\n', 1)
        agent = dirty_load(header, allow_flow_style=True).data
        if not isinstance(agent, dict) or set(agent) != {'name', 'description', 'tools', 'model'}:
            errors.append('Claude reviewer must use the reviewed field set; ignored permission overrides are forbidden')
        elif (agent['name'] != 'reviewer' or agent['tools'] != 'Read, Grep, Glob' or
              agent['model'] != 'inherit' or not isinstance(agent['description'], str) or
              not agent['description'].strip()):
            errors.append('Claude reviewer must retain its read-only tools and inherited model')
        if not body.strip():
            errors.append('Claude reviewer needs an actual procedure')
    except (OSError, ValueError, YAMLError) as error:
        errors.append(f'Invalid Claude adapter: {error}')
    return errors


def validate_project(root):
    errors = []
    files = source_files(root)
    catalog = read_json(root / 'catalog.json')
    expected = [name for names in catalog['sectors'].values() for name in names]
    # Reject untrusted identifiers before using any as filesystem paths.
    if not all(isinstance(name, str) and len(name) <= 64 and
               re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) for name in expected):
        return ['catalog contains an unsafe or invalid skill identifier']
    core = [name for sector, names in catalog['sectors'].items() if sector != 'V' for name in names]
    extension = catalog['sectors'].get('V', [])
    if len(core) != 34 or len(extension) != 8 or len(set(expected)) != 42:
        errors.append('catalog must preserve 34 core and 8 visual specialist identifiers')
    actual = sorted(p.name for p in (root / 'skills').iterdir() if p.is_dir())
    if sorted(expected) != actual:
        errors.append('skill directories do not match catalog')
    for name in expected:
        directory = root / 'skills' / name
        official_errors = validate_skill(directory)
        for error in official_errors:
            errors.append(f'{name}: official validation: {error}')
        if official_errors:
            continue
        path = directory / 'SKILL.md'
        if not path.is_file():
            continue
        content = path.read_text(encoding='utf-8')
        metadata, body = parse_frontmatter(content)
        if metadata.get('license') != 'Apache-2.0':
            errors.append(f'{name}: license must be Apache-2.0')
        if len(content.encode('utf-8')) > 8192 or len(content.splitlines()) >= 500:
            errors.append(f'{name}: exceeds context budget (8 KiB / <500 lines)')
        for heading in HEADINGS:
            if f'## {heading}' not in body.splitlines():
                errors.append(f'{name}: missing contract heading: {heading}')
        scenario_path = root / 'evaluations/scenarios' / f'{name}.json'
        if not scenario_path.is_file():
            errors.append(f'{name}: missing scenario')
        else:
            scenario = read_json(scenario_path)
            errors.extend(f'{name}: scenario: {e}' for e in
                          schema_errors(root, 'scenario.schema.json', scenario))
            if scenario.get('skill') != name:
                errors.append(f'{name}: scenario skill mismatch')
    errors += schema_errors(root, 'plugin.schema.json', read_json(root / 'plugin.json'))
    if read_json(root / 'plugin.json')['version'] != catalog['version']:
        errors.append('plugin and catalog versions differ')
    errors += validate_claude_plugin(root, catalog['version'])
    for path in files:
        if path.suffix in ('.yml', '.yaml'):
            try:
                dirty_load(path.read_text(encoding='utf-8'), allow_flow_style=True)
            except YAMLError as error:
                errors.append(f'{path.relative_to(root)}: invalid YAML: {error}')
        if path.suffix == '.toml':
            try:
                tomllib.loads(path.read_text(encoding='utf-8'))
            except tomllib.TOMLDecodeError as error:
                errors.append(f'{path.relative_to(root)}: invalid TOML: {error}')
        if path.suffix != '.md':
            continue
        content = markdown_prose(path.read_text(encoding='utf-8'))
        for target in re.findall(r'\]\(([^)\s]+)(?:\s+[^)]*)?\)', content):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                continue
            target = target.split('#', 1)[0]
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f'{path.relative_to(root)}: broken or external local link: {target}')
    return errors


def package(root, output):
    checksum = output.with_suffix(output.suffix + '.sha256')
    if output.exists() or output.is_symlink() or checksum.exists() or checksum.is_symlink():
        raise ValueError('refusing to overwrite an existing artifact or checksum')
    errors = validate_project(root)
    if errors:
        return errors
    files = source_files(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    # ZIP_STORED removes dependence on the host zlib version.
    with output.open('xb') as stream:
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as archive:
            for path in files:
                info = zipfile.ZipInfo(path.relative_to(root).as_posix(), (1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    with checksum.open('x', encoding='utf-8') as stream:
        stream.write(f'{digest}  {output.name}\n')
    print(f'Built {output.name}; SHA256 {digest}')
    return []


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('validate', help='official format checks plus OpenDevGuild policy')
    handoff = commands.add_parser('check-handoff', help='validate a report against its task')
    handoff.add_argument('report', type=Path)
    handoff.add_argument('--task', type=Path, required=True)
    build = commands.add_parser('package', help='build a local distributable; never publish')
    build.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate':
            errors = validate_project(args.root)
        elif args.command == 'check-handoff':
            errors = check_handoff(args.root, read_json(args.task), read_json(args.report))
        else:
            errors = package(args.root, args.output)
        if errors:
            for error in errors:
                print(f'ERROR: {error}')
            return 1
        print('PASS: structural checks only; behavioral quality requires scenario evaluation')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
