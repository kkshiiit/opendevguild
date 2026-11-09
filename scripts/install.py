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
MAX_JOURNAL_BYTES = 2 * MAX_MANIFEST_BYTES + 65536


def no_links(path):
    path = path.absolute()
    if sys.platform=='darwin':
        for alias,canonical in [('/var','/private/var'),('/tmp','/private/tmp')]:
            prefix=Path(alias)
            if prefix.is_symlink() and prefix.resolve()==Path(canonical) and path.is_relative_to(prefix):
                path=Path(canonical)/path.relative_to(prefix)
    for parent in (path, *path.parents):
        if parent.is_symlink() or getattr(parent, 'is_junction', lambda: False)():
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


def read_bounded(path, limit):
    no_links(path)
    if not path.is_file() or path.stat().st_size > limit:
        raise ValueError('Invalid or oversized installer state file')
    with path.open('rb') as stream:
        content = stream.read(limit + 1)
    if len(content) > limit:
        raise ValueError('Installer state exceeds safety budget')
    return content


def manifest_digest(state):
    path = state / 'manifest.json'
    no_links(path)
    return hashlib.sha256(read_bounded(path, MAX_MANIFEST_BYTES)).hexdigest() if path.exists() else None


def load_state(state, target, recovering=False):
    if not recovering and any((state / name).exists() or (state / name).is_symlink()
                              for name in ('pending.json', 'transaction')):
        raise ValueError('Installer recovery pending; run recover for this target before any new operation')
    path = state / 'manifest.json'
    no_links(path)
    if not path.exists():
        if state.exists() and any(state.iterdir()) and not recovering:
            raise ValueError('Reserved installer state exists without a valid manifest')
        return {'format': 1, 'target': str(target), 'skills': {}, 'history': {}}
    data = json.loads(read_bounded(path, MAX_MANIFEST_BYTES))
    return validate_state(data, target)


def validate_state(data, target):
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


def projected_state(data, records, action):
    projected = copy.deepcopy(data)
    for record in records:
        name, before, after, snapshot = (record[k] for k in ('name', 'before', 'after', 'snapshot'))
        if after is None:
            projected['skills'].pop(name, None)
        else:
            projected['skills'][name] = after
        history = projected['history'].setdefault(name, [])
        if action == 'rollback':
            if not history or history[-1]['after'] != before or history[-1]['before'] != after:
                raise ValueError('Recovery rollback history mismatch')
            history.pop()
        else:
            history.append({'before': before, 'after': after, 'snapshot': snapshot})
        if len(history) > 50:
            raise ValueError('History capacity exceeded; rollback or review backups first')
    return projected


def recover(state, target, dry_run=False):
    """Finish committed cleanup or restore the entire pre-commit batch."""
    pending = state / 'pending.json'
    journal = json.loads(read_bounded(pending, MAX_JOURNAL_BYTES))
    fields = {'format', 'target', 'action', 'before_state', 'before_manifest', 'after_manifest', 'operations'}
    if not isinstance(journal, dict) or set(journal) != fields or journal['format'] != 1 \
            or journal['target'] != str(target) or not isinstance(journal['operations'], list) \
            or not journal['operations']:
        raise ValueError('Invalid installer recovery journal')
    if journal['action'] not in ('install', 'update', 'uninstall', 'rollback'):
        raise ValueError('Invalid recovery action')
    before_state = validate_state(journal['before_state'], target)
    for key in ('before_manifest', 'after_manifest'):
        value = journal[key]
        if not (key == 'before_manifest' and value is None) and (not isinstance(value, str) or not HASH.fullmatch(value)):
            raise ValueError('Invalid recovery manifest hash')
    current_hash = manifest_digest(state)
    if current_hash == journal['after_manifest']:
        committed = True
    elif current_hash == journal['before_manifest']:
        committed = False
    else:
        raise ValueError('Manifest changed outside the pending transaction; preserve state for manual review')
    data = load_state(state, target, recovering=True)
    transaction = no_links(state / 'transaction')
    staged = no_links(transaction / 'staged')
    seen, undo = set(), []
    # Inspect every selected path before recovery mutates any of them.
    for operation in journal['operations']:
        if not isinstance(operation, dict) or set(operation) != {'name', 'before', 'after', 'snapshot'}:
            raise ValueError('Invalid recovery operation')
        name, before, after, snapshot = (operation[k] for k in ('name', 'before', 'after', 'snapshot'))
        if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64 or name in seen:
            raise ValueError('Invalid recovery skill identifier')
        seen.add(name)
        validate_entry(before); validate_entry(after)
        if before is None:
            if snapshot is not None:
                raise ValueError('Unexpected recovery snapshot')
        elif not isinstance(snapshot, str) or not re.fullmatch(r'[0-9a-f]{32}', snapshot):
            raise ValueError('Invalid recovery snapshot')
        expected = after if committed else before
        if before_state['skills'].get(name) != before:
            raise ValueError('Recovery operation does not match the prior manifest')
        if data['skills'].get(name) != expected:
            raise ValueError('Recovery operation does not match the active manifest')
        destination = no_links(target / name)
        backup = no_links(state / 'backups' / snapshot) if snapshot else None
        holding = no_links(staged / name)
        if committed:
            assert_current(destination, after)
            if before is not None:
                assert_current(backup, before)
            continue
        original_moved = backup is not None and backup.exists()
        if original_moved:
            assert_current(backup, before)
        elif before is not None:
            assert_current(destination, before)
            continue
        if destination.exists():
            assert_current(destination, after)
            if holding.exists():
                raise ValueError('Recovery staging collision; preserve both copies for manual review')
        undo.append((destination, backup if original_moved else None, holding))
    projected = projected_state(before_state, journal['operations'], journal['action'])
    encoded = (json.dumps(projected, indent=2) + '\n').encode('utf-8')
    if len(encoded) > MAX_MANIFEST_BYTES or hashlib.sha256(encoded).hexdigest() != journal['after_manifest']:
        raise ValueError('Recovery journal does not reproduce the prepared manifest')
    if data != (projected if committed else before_state):
        raise ValueError('Recovery state differs from the active manifest')
    if dry_run:
        moves = []
        for destination, backup, holding in reversed(undo):
            if destination.exists():
                moves.append({'source': str(destination), 'destination': str(holding)})
            if backup is not None:
                moves.append({'source': str(backup), 'destination': str(destination)})
        return {'direction': 'committed-cleanup' if committed else 'restore-before',
                'skills': sorted(seen), 'directory_moves': moves,
                'cleanup': [str(transaction), str(pending)]}
    if not committed:
        for destination, backup, holding in reversed(undo):
            if destination.exists():
                holding.parent.mkdir(parents=True, exist_ok=True)
                os.replace(destination, holding)
            if backup is not None:
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.replace(backup, destination)
        for operation in journal['operations']:
            assert_current(target / operation['name'], operation['before'])
        if manifest_digest(state) != journal['before_manifest']:
            raise ValueError('Manifest changed during recovery')
    # Originals are retained in backups on commit, or restored before cleanup.
    # The independent pending marker is removed LAST, even if rmtree fails.
    if transaction.exists():
        for path in transaction.rglob('*'):
            no_links(path)
            if not path.is_dir() and not path.is_file():
                raise ValueError('Non-regular transaction entry; preserve for manual review')
        shutil.rmtree(transaction)
    pending.unlink()
    if current_hash is None:
        try:
            state.rmdir()
        except OSError:
            pass  # Empty generated parents may remain; they are not managed data.
    return 'committed-cleanup' if committed else 'restored-before'


def execute(action, source, target, names, dry_run=False):
    source, target = no_links(source), no_links(target)
    key = hashlib.sha256(str(target).encode('utf-8')).hexdigest()[:16]
    state = no_links(target.parent / '.opendevguild-state' / key)
    if state.is_relative_to(target):
        raise ValueError('Installer state must remain outside skill discovery')
    if action == 'recover':
        result = recover(state, target, dry_run)
        print(json.dumps({'action': action, 'dry_run': dry_run, 'result': result, 'state_directory': str(state)}))
        return
    if action not in ('install', 'update', 'uninstall', 'rollback'):
        raise ValueError('Unknown installer action')
    if len(set(names)) != len(names) or not names or any(not NAME.fullmatch(n) or len(n) > 64 for n in names):
        raise ValueError('Choose unique kebab-case skill identifiers, never paths')
    if target == source or target.is_relative_to(source / 'skills'):
        raise ValueError('Do not install into the source skill catalog')
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
            assert_current(backup, None)
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
        if incoming is not None:
            for path in sorted(after_paths):
                plan.append({'operation': 'STAGE', 'source': str(incoming / path),
                             'path': str(state / 'transaction' / 'staged' / name / path)})
        operations.append((name, destination, current, incoming, after, snapshot))
    records = [{'name': n, 'before': b, 'after': a, 'snapshot': s}
               for n, d, b, i, a, s in operations]
    projected = projected_state(data, records, action)
    serialized=json.dumps(projected,indent=2)+'\n'
    if len(serialized.encode('utf-8'))>MAX_MANIFEST_BYTES:
        raise ValueError('Next manifest exceeds safety budget; no files changed, rollback remains available')
    print(json.dumps({'dry_run': dry_run, 'action': action, 'files': plan,
                      'state_directory': str(state), 'manifest_write': str(state / 'manifest.json'),
                      'journal_write': str(state / 'pending.json'),
                      'prepared_manifest': str(state / 'transaction' / 'manifest-next.json'),
                      'state_action': 'revert last managed transaction' if action=='rollback' else 'append managed hashes and version history'}, indent=2))
    if dry_run:
        return
    # Stage the whole batch; originals remain installed until every copy and
    # the next manifest are ready. The journal blocks normal operations until
    # compensation/committed cleanup has completed.
    transaction = no_links(state / 'transaction')
    journal = {'format': 1, 'target': str(target), 'action': action, 'before_state': data,
               'before_manifest': manifest_digest(state),
               'after_manifest': hashlib.sha256(serialized.encode('utf-8')).hexdigest(),
               'operations': records}
    journal_bytes = (json.dumps(journal, indent=2) + '\n').encode('utf-8')
    if len(journal_bytes) > MAX_JOURNAL_BYTES:
        raise ValueError('Recovery journal exceeds safety budget; no files changed')
    state.mkdir(parents=True, exist_ok=True)
    # Exclusive marker creation refuses another pending transaction. A failed
    # marker write cannot have affected an installed directory.
    marker_created = False
    try:
        with (state / 'pending.json').open('xb') as stream:
            marker_created = True
            stream.write(journal_bytes)
    except OSError:
        if marker_created:
            try:
                (state / 'pending.json').unlink()
            except OSError:
                pass  # Retain a blocking marker if cleanup itself is unavailable.
        raise
    committed = False
    try:
        staged = transaction / 'staged'
        staged.mkdir(parents=True)
        for name, destination, before, incoming, after, snapshot in operations:
            if after is not None:
                shutil.copytree(incoming, staged / name)
                assert_current(staged / name, after)
        next_manifest = transaction / 'manifest-next.json'
        next_manifest.write_text(serialized, encoding='utf-8', newline='\n')
        if hashlib.sha256(read_bounded(next_manifest, MAX_MANIFEST_BYTES)).hexdigest() != journal['after_manifest']:
            raise ValueError('Staged manifest verification failed')
        for name, destination, before, incoming, after, snapshot in operations:
            assert_current(destination, before)
        if manifest_digest(state) != journal['before_manifest']:
            raise ValueError('Manifest changed during preparation')
        for name, destination, before, incoming, after, snapshot in operations:
            if before is not None:
                backup = no_links(state / 'backups' / snapshot)
                backup.parent.mkdir(exist_ok=True)
                os.replace(destination, backup)
            if after is not None:
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.replace(staged / name, destination)
        for name, destination, before, incoming, after, snapshot in operations:
            assert_current(destination, after)
            if before is not None:
                assert_current(state / 'backups' / snapshot, before)
        os.replace(next_manifest, state / 'manifest.json')
        committed = True
    except (OSError, ValueError) as error:
        # Reconcile an ambiguous publication error before deciding to undo.
        # Once the new manifest is observed, cleanup must never revert it.
        try:
            committed = manifest_digest(state) == journal['after_manifest']
        except (OSError, ValueError):
            committed = False
        if committed:
            print('WARNING: batch committed despite a publication error; active manifest verified.', file=sys.stderr)
            return
        try:
            result = recover(state, target)
        except (OSError, ValueError) as recovery_error:
            raise OSError(f'Operation failed; recovery pending at {state}; originals retained. '
                          f'Run recover after resolving the I/O problem: {recovery_error}') from error
        if result == 'committed-cleanup':
            print('WARNING: batch committed despite a publication error; active manifest verified.', file=sys.stderr)
            return
        raise
    finally:
        if committed:
            try:
                recover(state, target)
            except (OSError, ValueError) as error:
                print(f'WARNING: batch committed; cleanup pending at {state}; run recover: {error}', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('install', 'update', 'uninstall', 'rollback', 'recover'))
    parser.add_argument('--source', type=Path, default=ROOT)
    parser.add_argument('--target', type=Path, required=True, help='Explicit skill discovery directory, e.g. project/.agents/skills')
    parser.add_argument('--skill', action='append', default=[])
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
