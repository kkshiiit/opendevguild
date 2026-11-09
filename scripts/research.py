"""Bounded local provenance registry; never fetches resources or executes their content."""
import argparse
import datetime
import json
from pathlib import Path
import random
import sqlite3
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
TYPES = ('web_page', 'android_application', 'desktop_program', 'web_application',
         'agent_skill', 'prompt', 'technical_document')
LEVELS = tuple(f'L{i}' for i in range(5))
MAX_BATCH = 1000
MAX_IMPORT_BYTES = 8 * 1024 * 1024
MAX_RECORD_BYTES = 32768


def read_batch(path):
    path = Path(path)
    if path.stat().st_size > MAX_IMPORT_BYTES:
        raise ValueError('Import file exceeds 8 MiB; split it into controlled metadata batches')
    return json.loads(path.read_text(encoding='utf-8'))


def canonical_url(value):
    parts = urlsplit(value)
    if parts.scheme not in ('https', 'http') or not parts.hostname or parts.username or parts.password:
        raise ValueError('Use HTTP(S) source identifiers without credentials; public access requires separate review')
    pairs = parse_qsl(parts.query, keep_blank_values=True)
    if any(k.lower() in ('token', 'access_token', 'api_key', 'secret', 'password', 'key') for k, _ in pairs):
        raise ValueError('Credential-like query parameters must not enter the registry')
    port = parts.port
    host = parts.hostname.lower()
    if port and not ((parts.scheme == 'https' and port == 443) or (parts.scheme == 'http' and port == 80)):
        host += f':{port}'
    return urlunsplit((parts.scheme.lower(), host, parts.path or '/', urlencode(sorted(pairs)), ''))


def validate(record):
    schema = json.loads((ROOT / 'contracts/research.schema.json').read_text(encoding='utf-8'))
    errors = list(Draft202012Validator(schema).iter_errors(record))
    if errors:
        raise ValueError('; '.join(e.message for e in errors))
    if len(json.dumps(record, ensure_ascii=False).encode('utf-8')) > MAX_RECORD_BYTES:
        raise ValueError('Record exceeds 32 KiB metadata budget; retain content externally with provenance')
    canonical_url(record['url'])
    try:
        datetime.date.fromisoformat(record['observed_at'])
    except ValueError as error:
        raise ValueError('observed_at must be a real ISO calendar date') from error
    level = LEVELS.index(record['level'])
    evidence = record['evidence']
    if level >= 1 and not any(e['kind'] == 'provenance' and e['outcome'] == 'observed' for e in evidence):
        raise ValueError('L1 requires recorded provenance observations')
    if level >= 2 and (not record['rubric'] or not record['evaluation_result'] or
                       not any(e['kind'] == 'content' and e.get('inspected') is True for e in evidence)):
        raise ValueError('L2 requires inspected content, rubric and actual evaluation; summaries alone are insufficient')
    if level >= 3 and not any(e['kind'] == 'execution' and e.get('authorized') is True and
                             e['outcome'] == 'passed' for e in evidence):
        raise ValueError('L3 requires authorized executed behavior evidence')
    if level >= 4 and not any(e['kind'] == 'comparison' and e.get('independent') is True and
                             e.get('matched_conditions') is True and e['outcome'] == 'improved' for e in evidence):
        raise ValueError('L4 requires a reproducible matched comparison demonstrating improvement')
    return record


def _connection(db, create=False):
    db = Path(db)
    if db.is_symlink():
        raise ValueError('Registry database itself must not be a symlink')
    # Resolve the explicitly chosen parent, including system aliases such as
    # macOS /var -> /private/var. No directory is inferred from source records.
    db = db.parent.resolve() / db.name
    if not create and not db.is_file():
        raise ValueError('Registry does not exist; import an explicit batch first')
    if create:
        db.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db)
    if create:
        connection.execute('''CREATE TABLE IF NOT EXISTS resources (
            id TEXT PRIMARY KEY, resource_type TEXT NOT NULL, url TEXT NOT NULL,
            version TEXT NOT NULL, content_hash TEXT, level TEXT NOT NULL, record TEXT NOT NULL,
            UNIQUE(resource_type, url, version))''')
        connection.execute('CREATE INDEX IF NOT EXISTS resource_hash ON resources(resource_type, content_hash)')
    return connection


def import_batch(db, records):
    if not isinstance(records, list) or not 1 <= len(records) <= MAX_BATCH:
        raise ValueError('Provide a batch of 1–1000 records')
    for record in records:
        validate(record)
    result = {'inserted': 0, 'duplicates': 0, 'retained_existing': [], 'policy': 'No implicit evidence upgrades or record replacement'}
    connection = _connection(db, create=True)
    try:
        with connection:
            for record in records:
                url = canonical_url(record['url'])
                existing = connection.execute('SELECT url, version, content_hash, resource_type FROM resources WHERE id=?',
                                              (record['id'],)).fetchone()
                if existing:
                    identity = (url, record['version'], record['content_sha256'], record['resource_type'])
                    if tuple(existing) != identity:
                        raise ValueError(f"Conflicting immutable resource ID: {record['id']}")
                    result['duplicates'] += 1
                    result['retained_existing'].append(record['id'])
                    continue
                duplicate = connection.execute('SELECT id,content_hash FROM resources WHERE resource_type=? AND url=? AND version=?',
                                               (record['resource_type'], url, record['version'])).fetchone()
                if duplicate and duplicate[1] != record['content_sha256']:
                    raise ValueError('Same URL/version has conflicting content identity; register an explicit new version')
                if not duplicate and record['content_sha256']:
                    duplicate = connection.execute('SELECT id,content_hash FROM resources WHERE resource_type=? AND content_hash=? AND version=?',
                                                   (record['resource_type'], record['content_sha256'], record['version'])).fetchone()
                if duplicate:
                    result['duplicates'] += 1
                    result['retained_existing'].append(duplicate[0])
                    continue
                saved = dict(record, url=url, deduplication='unique')
                connection.execute('INSERT INTO resources VALUES (?,?,?,?,?,?,?)',
                                   (record['id'], record['resource_type'], url, record['version'],
                                    record['content_sha256'], record['level'], json.dumps(saved, sort_keys=True)))
                result['inserted'] += 1
    finally:
        connection.close()
    return result


def report(db):
    connection = _connection(db)
    try:
        by_type = {kind: 0 for kind in TYPES}
        by_level = {level: 0 for level in LEVELS}
        matrix = {kind: {level: 0 for level in LEVELS} for kind in TYPES}
        for kind, level, count in connection.execute('SELECT resource_type,level,COUNT(*) FROM resources GROUP BY resource_type,level'):
            by_type[kind] += count; by_level[level] += count; matrix[kind][level] = count
        hashed = connection.execute('SELECT COUNT(*) FROM resources WHERE content_hash IS NOT NULL').fetchone()[0]
        unique_by_type = {kind: 0 for kind in TYPES}
        for kind, count in connection.execute('SELECT resource_type,COUNT(DISTINCT url) FROM resources GROUP BY resource_type'):
            unique_by_type[kind] = count
        unique_content = connection.execute('SELECT COUNT(*) FROM (SELECT resource_type,content_hash FROM resources WHERE content_hash IS NOT NULL GROUP BY resource_type,content_hash)').fetchone()[0]
        return {'total': sum(by_type.values()), 'by_type': by_type, 'by_level': by_level, 'matrix': matrix,
                'unique_source_total': sum(unique_by_type.values()), 'unique_sources_by_type': unique_by_type,
                'known_unique_content': unique_content,
                'confidence_components': {'provenance_evidence_records': sum(by_level[x] for x in LEVELS[1:]),
                                          'content_evaluated_records': sum(by_level[x] for x in LEVELS[2:]),
                                          'authorized_execution_records': sum(by_level[x] for x in LEVELS[3:]),
                                          'matched_improvement_records': by_level['L4'], 'content_hash_known': hashed},
                'long_term_target': {kind: 200000 for kind in TYPES},
                'limitations': 'total/by_level count versioned observations; unique_source_total counts registered source identities without version inflation. Neither authenticates truth, rights or project improvement.'}
    finally:
        connection.close()


def sample(db, limit, seed):
    if type(limit) is not int or not 1 <= limit <= MAX_BATCH:
        raise ValueError('Sample size must be 1–1000')
    connection = _connection(db)
    randomizer = random.Random(seed)
    reservoirs = {kind: [] for kind in TYPES}; seen = dict.fromkeys(TYPES, 0)
    try:
        for kind, encoded in connection.execute('SELECT resource_type,record FROM resources ORDER BY id'):
            seen[kind] += 1
            pool = reservoirs[kind]
            if len(pool) < limit:
                pool.append(encoded)
            else:
                index = randomizer.randrange(seen[kind])
                if index < limit:
                    pool[index] = encoded
        for pool in reservoirs.values():
            randomizer.shuffle(pool)
        selected = []
        while len(selected) < limit:
            progressed = False
            for kind in TYPES:
                if reservoirs[kind] and len(selected) < limit:
                    selected.append(json.loads(reservoirs[kind].pop())); progressed = True
            if not progressed:
                break
        return selected
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, required=True, help='Explicit local SQLite database, normally under ignored dist/')
    commands = parser.add_subparsers(dest='command', required=True)
    importer = commands.add_parser('import'); importer.add_argument('records', type=Path)
    commands.add_parser('report')
    sampler = commands.add_parser('sample'); sampler.add_argument('--limit', type=int, default=20); sampler.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    try:
        if args.command == 'import':
            result = import_batch(args.db, read_batch(args.records))
        elif args.command == 'report':
            result = report(args.db)
        else:
            result = sample(args.db, args.limit, args.seed)
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.exit(1, f'ERROR: {error}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':main()
