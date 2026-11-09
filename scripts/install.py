"""Optional selective local installer. Never downloads or executes skill content."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
HASH = re.compile(r'[0-9a-f]{64}\Z')
MAX_MANIFEST_BYTES = 4 * 1024 * 1024


def no_links(path):
    path = path.absolute()
    if sys.platform=='darwin':
        for alias,canonical in [('/var','/private/var'),('/tmp','/private/tmp')]:
            prefix=Path(alias)
            if prefix.is_symlink() and prefix.resolve()==Path(canonical) and path.is_relative_to(prefix):
                path=Path(canonical)/path.relative_to(prefix)
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise ValueError(f'Symlink path rejected: {parent}')
    return path.resolve()


def relative(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('Invalid managed relative path')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '.' in path.parts:
        raise ValueError('Managed path escapes its skill')
    return value


def inspect(directory):
    no_links(directory)
    if not directory.is_dir():
        raise ValueError(f'Skill directory missing: {directory}')
    files, directories, total = {}, [], 0
    for path in sorted(directory.rglob('*')):
        no_links(path)
        key = relative(path.relative_to(directory).as_posix())
        if path.is_dir():
            directories.append(key)
        elif path.is_file():
            total += path.stat().st_size
            if len(files) >= 1000 or total > 16 * 1024 * 1024:
                raise ValueError('Skill exceeds installer safety budget (1000 files /16MiB)')
            files[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            raise ValueError(f'Non-regular source entry: {path}')
    if 'SKILL.md' not in files:
        raise ValueError(f'Missing SKILL.md: {directory}')
    return {'files': files, 'directories': directories}


def validate_entry(entry):
    if entry is None:
        return
    if not isinstance(entry, dict) or set(entry) != {'files', 'directories', 'version'}:
        raise ValueError('Invalid managed entry')
    if not isinstance(entry['version'], str) or not isinstance(entry['files'], dict) or not isinstance(entry['directories'], list):
        raise ValueError('Invalid managed entry values')
    if 'SKILL.md' not in entry['files'] or len(entry['files']) > 1000:
        raise ValueError('Invalid managed file inventory')
    for key, digest in entry['files'].items():
        relative(key)
        if not isinstance(digest, str) or not HASH.fullmatch(digest):
            raise ValueError('Invalid managed hash')
    for key in entry['directories']:
        relative(key)


def load_state(state, target):
    path = state / 'manifest.json'
    no_links(path)
    if not path.exists():
        if state.exists():
            raise ValueError('Reserved installer state exists without a valid manifest')
        return {'format': 1, 'target': str(target), 'skills': {}, 'history': {}}
    if path.stat().st_size > MAX_MANIFEST_BYTES:
        raise ValueError('Installer manifest exceeds safety budget')
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or set(data) != {'format', 'target', 'skills', 'history'} \
            or data['format'] != 1 or data['target'] != str(target) \
            or not isinstance(data['skills'], dict) or not isinstance(data['history'], dict):
        raise ValueError('Invalid installer manifest or target identity')
    for name in data['skills'].keys() | data['history'].keys():
        if not NAME.fullmatch(name) or len(name) > 64:
            raise ValueError('Invalid managed skill identifier')
        validate_entry(data['skills'].get(name))
        history = data['history'].get(name, [])
        if not isinstance(history, list) or len(history) > 50:
            raise ValueError('Invalid or excessive installer history')
        for change in history:
            if not isinstance(change, dict) or set(change) != {'before', 'after', 'snapshot'}:
                raise ValueError('Invalid history record')
            validate_entry(change['before']); validate_entry(change['after'])
            snapshot = change['snapshot']
            if change['before'] is None:
                if snapshot is not None:
                    raise ValueError('Unexpected snapshot')
            elif not isinstance(snapshot, str) or not re.fullmatch(r'[0-9a-f]{32}', snapshot):
                raise ValueError('Invalid snapshot identifier')
    return data


def assert_current(path, expected):
    no_links(path)
    if expected is None:
        if path.exists():
            raise ValueError(f'Refusing collision with existing skill: {path}')
    else:
        actual = inspect(path)
        if actual != {key: expected[key] for key in ('files', 'directories')}:
            raise ValueError(f'User changes detected; preserved without overwrite: {path}')


def execute(action, source, target, names, dry_run=False):
    source, target = no_links(source), no_links(target)
    if len(set(names)) != len(names) or not names or any(not NAME.fullmatch(n) or len(n) > 64 for n in names):
        raise ValueError('Choose unique kebab-case skill identifiers, never paths')
    if target == source or target.is_relative_to(source / 'skills'):
        raise ValueError('Do not install into the source skill catalog')
    key = hashlib.sha256(str(target).encode('utf-8')).hexdigest()[:16]
    state = no_links(target.parent / '.opendevguild-state' / key)
    data = load_state(state, target)
    operations, plan = [], []
    version = 'unknown'
    if action in ('install', 'update') and (source / 'plugin.json').is_file():
        no_links(source / 'plugin.json')
        version = str(json.loads((source / 'plugin.json').read_text(encoding='utf-8')).get('version', 'unknown'))
    for name in names:
        current = data['skills'].get(name)
        destination = target / name
        assert_current(destination, current)
        if action in ('install','update') and len(data['history'].get(name, [])) >= 49:
            raise ValueError('History budget reached; final slot is reserved for uninstall; rollback remains available')
        incoming = None
        after = None
        if action == 'install':
            if current is not None:
                raise ValueError(f'Skill already managed: {name}; use update')
            incoming = source / 'skills' / name
            after = {**inspect(incoming), 'version': version}
        elif action == 'update':
            if current is None:
                raise ValueError(f'Unmanaged skill: {name}; use install')
            incoming = source / 'skills' / name
            after = {**inspect(incoming), 'version': version}
        elif action == 'uninstall':
            if current is None:
                raise ValueError(f'Unmanaged skill: {name}')
        else:
            history = data['history'].get(name, [])
            if not history:
                raise ValueError(f'No rollback history: {name}')
            change = history[-1]
            if current != change['after']:
                raise ValueError('Current manifest does not match rollback history')
            after = change['before']
            if after is not None:
                incoming = state / 'backups' / change['snapshot']
                assert_current(incoming, after)
        if incoming is not None and (incoming.absolute().is_relative_to(destination) or destination.is_relative_to(incoming.absolute())):
            raise ValueError('Source and destination skill directories overlap')
        snapshot = uuid.uuid4().hex if current is not None else None
        if snapshot:
            backup = no_links(state / 'backups' / snapshot)
            for path in sorted(current['files']):
                plan.append({'operation': 'BACKUP', 'source': str(destination / path), 'path': str(backup / path)})
        before_paths = set(current['files']) if current else set()
        after_paths = set(after['files']) if after else set()
        for path in sorted(before_paths | after_paths):
            operation = 'WRITE' if path in after_paths else 'REMOVE'
            item = {'operation': operation, 'path': str(destination / path)}
            if incoming is not None and path in after_paths:
                item['source'] = str(incoming / path)
            plan.append(item)
        operations.append((name, destination, current, incoming, after, snapshot))
    projected=copy.deepcopy(data)
    for name,destination,before,incoming,after,snapshot in operations:
        if after is None:projected['skills'].pop(name,None)
        else:projected['skills'][name]=after
        history=projected['history'].setdefault(name,[])
        if action=='rollback':history.pop()
        else:history.append({'before':before,'after':after,'snapshot':snapshot})
        if len(history)>50:raise ValueError('History capacity exceeded; rollback or review backups first')
    serialized=json.dumps(projected,indent=2)+'\n'
    if len(serialized.encode('utf-8'))>MAX_MANIFEST_BYTES:
        raise ValueError('Next manifest exceeds safety budget; no files changed, rollback remains available')
    print(json.dumps({'dry_run': dry_run, 'action': action, 'files': plan,
                      'state_directory': str(state), 'manifest_write': str(state / 'manifest.json'),
                      'state_action': 'revert last managed transaction' if action=='rollback' else 'append managed hashes and version history'}, indent=2))
    if dry_run:
        return
    # All selected skills are inspected before any write. Backups are outside
    # discovery, and every replacement is validated against recorded user bytes.
    state.mkdir(parents=True, exist_ok=True)
    for name, destination, before, incoming, after, snapshot in operations:
        if before is not None:
            backup = no_links(state / 'backups' / snapshot)
            backup.parent.mkdir(exist_ok=True)
            shutil.copytree(destination, backup)
            assert_current(backup, before)
        if destination.exists():
            # Scoped, hash-verified managed directory only; never arbitrary paths.
            shutil.rmtree(destination)
        if after is not None:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(incoming, destination)
            data['skills'][name] = after
        else:
            data['skills'].pop(name, None)
    temporary = state / f'manifest-{uuid.uuid4().hex}.json'
    temporary.write_text(serialized, encoding='utf-8')
    os.replace(temporary, state / 'manifest.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('install', 'update', 'uninstall', 'rollback'))
    parser.add_argument('--source', type=Path, default=ROOT)
    parser.add_argument('--target', type=Path, required=True, help='Explicit skill discovery directory, e.g. project/.agents/skills')
    parser.add_argument('--skill', action='append', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        execute(args.action, args.source, args.target, args.skill, args.dry_run)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
