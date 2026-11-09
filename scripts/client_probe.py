"""Prepare and check an offline, disposable Codex skill smoke-test fixture.

No model invocation, authentication access, installation, networking or client
behavior verification is performed. Live probes are separate, opt-in steps.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("scope-guardian", "code-review-engineer")
PROFILE = "reviewer.toml"
MAX_FILES = 1000
MAX_ENTRIES = 2000
MAX_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 16 * 1024 * 1024
MAX_MANIFEST_BYTES = 256 * 1024
BUGGY = '''"""Deliberately flawed, synthetic review fixture."""\n\ndef total_after_discount(total, discount):\n    """Return nonnegative total after discount."""\n    if total < 0 or discount < 0:\n        raise ValueError("nonnegative values required")\n    return max(0, total + discount)\n'''
SCENARIOS = [
    {"id": "A-scope", "skill": "scope-guardian", "prompt":
     "$scope-guardian Review the proposed change to buggy.py without editing. "
     "Scope: buggy.py only. Identify acceptance, exclusions and tests; no network.",
     "expect": "bounded scope and reproducible acceptance; no file changes"},
    {"id": "B-review", "skill": "code-review-engineer", "prompt":
     "$code-review-engineer Review buggy.py as a read-only fixture. "
     "Report any correctness defects with locations and a "
     "counterexample. Do not edit or execute unknown code or use the network.",
     "expect": "detects addition instead of subtraction with a concrete case"},
    {"id": "C-negative", "skill": "none", "prompt":
     "Answer only: what is 2 + 2? Do not inspect files or activate skills.",
     "expect": "short answer; skill nonactivation requires actual client/tool evidence"},
]


def safe_relative(path: str) -> bool:
    rel = PurePosixPath(path)
    return bool(path) and not rel.is_absolute() and '..' not in rel.parts \
        and '\\' not in path and ':' not in path and path == rel.as_posix()


def no_links(path: Path) -> Path:
    """Reject linked ancestors before resolving or touching fixture paths."""
    path = path.absolute()
    # macOS exposes its normal temporary locations through these OS aliases.
    # Permit only these exact system mappings, not arbitrary user-created links.
    if sys.platform == "darwin":
        for alias, canonical in (("/var", "/private/var"), ("/tmp", "/private/tmp")):
            prefix = Path(alias)
            if prefix.is_symlink() and prefix.resolve() == Path(canonical) and path.is_relative_to(prefix):
                path = Path(canonical) / path.relative_to(prefix)
    for part in (path, *path.parents):
        if part.is_symlink() or getattr(part, "is_junction", lambda: False)():
            raise ValueError("symlink or junction in fixture path rejected")
    return path


def entries(directory: Path):
    """Bound metadata traversal and never descend into links or junctions."""
    pending = [directory]
    count = 0
    while pending:
        with os.scandir(pending.pop()) as children:
            for child in children:
                count += 1
                if count > MAX_ENTRIES:
                    raise ValueError("fixture entry budget exceeded")
                path = Path(child.path)
                yield path
                linked = path.is_symlink() or getattr(path, "is_junction", lambda: False)()
                if not linked and child.is_dir(follow_symlinks=False):
                    pending.append(path)


def read_regular(path: Path, limit: int) -> bytes:
    """Preflight file type/size, then bound the actual read as well."""
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("non-regular fixture file rejected")
    if info.st_size > limit:
        raise ValueError("fixture byte budget exceeded")
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("fixture byte budget exceeded")
    return data


def source_files(root: Path) -> list[tuple[Path, str]]:
    root = no_links(root)
    paths: list[tuple[Path, str]] = []
    for skill in SKILLS:
        base = root / "skills" / skill
        no_links(base)
        if (root / "skills").is_symlink() or base.is_symlink() or not (base / "SKILL.md").is_file():
            raise ValueError(f"missing or linked skill: {skill}")
        for path in entries(base):
            if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
                raise ValueError(f"source symlink rejected: {skill}")
            if path.is_file():
                rel = (Path(".agents") / "skills" / skill / path.relative_to(base)).as_posix()
                paths.append((path, rel))
                if len(paths) > MAX_FILES:
                    raise ValueError("fixture file budget exceeded")
            elif not path.is_dir():
                raise ValueError("non-regular source entry rejected")
    profile = root / ".codex" / "agents" / PROFILE
    no_links(profile)
    if (root / ".codex").is_symlink() or profile.parent.is_symlink() or profile.is_symlink() or not profile.is_file():
        raise ValueError("missing or linked optional reviewer profile")
    paths.append((profile, (Path(".codex") / "agents" / PROFILE).as_posix()))
    return paths


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prepare(output: Path, root: Path = ROOT) -> dict:
    """Create a new fixture only; never overwrite an existing destination."""
    sources = source_files(root)
    output = no_links(output)
    if output.exists():
        raise ValueError("output exists; choose a new empty destination")
    if not output.parent.is_dir():
        raise ValueError("output parent does not exist")
    # Read/validate all bounded inputs and serialized metadata before any writes.
    payloads: dict[str, bytes] = {}
    total = 0
    for source, rel in sources:
        data = read_regular(source, min(MAX_FILE_BYTES, MAX_TOTAL_BYTES - total))
        total += len(data)
        payloads[rel] = data
    text_files = {
        "buggy.py": BUGGY,
        "scenarios.json": json.dumps({
            "kind": "prepared-smoke-scenarios-not-executed",
            "cases": SCENARIOS,
            "limits": ["Run only in a permitted read-only client sandbox.",
                       "No actual skill or subagent activation was observed.",
                       "A model's assertion is not independent runtime evidence."],
        }, indent=2) + "\n",
    }
    for rel, content in text_files.items():
        payloads[rel] = content.encode("utf-8")
    if (len(payloads) > MAX_FILES or sum(map(len, payloads.values())) > MAX_TOTAL_BYTES or
            any(len(data) > MAX_FILE_BYTES for data in payloads.values())):
        raise ValueError("fixture payload budget exceeded")
    inventory = set(payloads) | {"manifest.json"}
    for rel in payloads:
        inventory.update(str(p) for p in PurePosixPath(rel).parents if p != PurePosixPath("."))
    if len(inventory) > MAX_ENTRIES:
        raise ValueError("fixture entry budget exceeded")
    records = {rel: digest(data) for rel, data in payloads.items()}
    manifest = {"kind": "prepared-client-fixture", "status": "PREPARED_NOT_RUN",
                "files": dict(sorted(records.items())),
                "limitations": "Hashes document fixture integrity, not client discovery, activation or behavior."}
    metadata = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    if len(metadata) > MAX_MANIFEST_BYTES:
        raise ValueError("fixture manifest budget exceeded")
    output.mkdir()
    for rel, data in payloads.items():
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    (output / "manifest.json").write_bytes(metadata)
    return {"status": "PREPARED_NOT_RUN", "path": str(output),
            "files": len(records), "scenarios": len(SCENARIOS)}


def check(output: Path) -> dict:
    output = no_links(output)
    no_links(output / "manifest.json")
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate manifest key")
            result[key] = value
        return result

    data = read_regular(output / "manifest.json", MAX_MANIFEST_BYTES)
    try:
        manifest = json.loads(data.decode("utf-8"), object_pairs_hook=unique_keys)
    except RecursionError as error:
        raise ValueError("manifest nesting budget exceeded") from error
    if (not isinstance(manifest, dict) or manifest.get("kind") != "prepared-client-fixture" or
            not isinstance(manifest.get("files"), dict)):
        raise ValueError("invalid manifest")
    registered = manifest["files"]
    if not registered or any(not safe_relative(p) for p in registered):
        raise ValueError("unsafe or empty fixture entries")
    if len(registered) > MAX_FILES:
        raise ValueError("fixture file budget exceeded")
    changed: list[str] = []
    total = 0
    for rel, expected in sorted(registered.items()):
        path = output / rel
        if (any(parent.is_symlink() or getattr(parent, "is_junction", lambda: False)()
                for parent in (path, *path.parents[:len(PurePosixPath(rel).parts) - 1])) or
                not path.resolve().is_relative_to(output.resolve()) or not path.is_file() or
                not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected)):
            changed.append(rel)
            continue
        content = read_regular(path, min(MAX_FILE_BYTES, MAX_TOTAL_BYTES - total))
        total += len(content)
        if digest(content) != expected:
            changed.append(rel)
    known = set(registered) | {"manifest.json"}
    additional = sorted(p.relative_to(output).as_posix() for p in entries(output)
                        if (p.is_symlink() or getattr(p, "is_junction", lambda: False)() or
                            not p.is_dir()) and p.relative_to(output).as_posix() not in known)
    return {"status": "CHANGED" if changed or additional else "UNCHANGED",
            "changed": changed, "additional": additional,
            "limits": "This checks file bytes only; it does not prove skills executed or prevent forged manifests."}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    cmd = parser.add_subparsers(dest="command", required=True)
    make = cmd.add_parser("prepare", help="Create isolated offline test files")
    make.add_argument("--output", required=True, type=Path)
    verify = cmd.add_parser("check", help="Check existing fixture file hashes")
    verify.add_argument("--fixture", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        result = prepare(args.output) if args.command == "prepare" else check(args.fixture)
    except (OSError, ValueError, json.JSONDecodeError, TypeError) as exc:
        print(json.dumps({"status": "ERROR", "message": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] != "CHANGED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
