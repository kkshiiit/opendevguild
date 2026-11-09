"""Prepare and check an offline, disposable Codex skill smoke-test fixture.

No model invocation, authentication access, installation, networking or client
behavior verification is performed. Live probes are separate, opt-in steps.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("scope-guardian", "code-review-engineer")
PROFILE = "reviewer.toml"
BUGGY = '''"""Deliberately flawed, synthetic review fixture."""\n\ndef total_after_discount(total, discount):\n    """Return nonnegative total after discount."""\n    if total < 0 or discount < 0:\n        raise ValueError("nonnegative values required")\n    return max(0, total + discount)  # BUG: must subtract discount\n'''
SCENARIOS = [
    {"id": "A-scope", "skill": "scope-guardian", "prompt":
     "$scope-guardian Review the proposed change to buggy.py without editing. "
     "Scope: buggy.py only. Identify acceptance, exclusions and tests; no network.",
     "expect": "bounded scope and reproducible acceptance; no file changes"},
    {"id": "B-review", "skill": "code-review-engineer", "prompt":
     "$code-review-engineer Review buggy.py as a read-only fixture. "
     "Find the deliberately incorrect discount calculation, report location and a "
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


def source_files(root: Path) -> list[tuple[Path, str]]:
    paths: list[tuple[Path, str]] = []
    for skill in SKILLS:
        base = root / "skills" / skill
        if (root / "skills").is_symlink() or base.is_symlink() or not (base / "SKILL.md").is_file():
            raise ValueError(f"missing or linked skill: {skill}")
        for path in sorted(base.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"source symlink rejected: {skill}")
            if path.is_file():
                rel = (Path(".agents") / "skills" / skill / path.relative_to(base)).as_posix()
                paths.append((path, rel))
    profile = root / ".codex" / "agents" / PROFILE
    if (root / ".codex").is_symlink() or profile.parent.is_symlink() or profile.is_symlink() or not profile.is_file():
        raise ValueError("missing or linked optional reviewer profile")
    paths.append((profile, (Path(".codex") / "agents" / PROFILE).as_posix()))
    return paths


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prepare(output: Path, root: Path = ROOT) -> dict:
    """Create a new fixture only; never overwrite an existing destination."""
    sources = source_files(root)
    if output.is_symlink() or output.parent.is_symlink():
        raise ValueError("output symlink or symlinked parent rejected")
    if output.exists():
        raise ValueError("output exists; choose a new empty destination")
    if not output.parent.is_dir():
        raise ValueError("output parent does not exist")
    output.mkdir()
    records: dict[str, str] = {}
    for source, rel in sources:
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        dest.write_bytes(data)
        records[rel] = digest(data)
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
        (output / rel).write_text(content, encoding="utf-8")
        records[rel] = digest(content.encode("utf-8"))
    manifest = {"kind": "prepared-client-fixture", "status": "PREPARED_NOT_RUN",
                "files": dict(sorted(records.items())),
                "limitations": "Hashes document fixture integrity, not client discovery, activation or behavior."}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"status": "PREPARED_NOT_RUN", "path": str(output),
            "files": len(records), "scenarios": len(SCENARIOS)}


def check(output: Path) -> dict:
    if output.is_symlink() or (output / "manifest.json").is_symlink():
        raise ValueError("linked fixture or manifest rejected")
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("kind") != "prepared-client-fixture" or not isinstance(manifest.get("files"), dict):
        raise ValueError("invalid manifest")
    registered = manifest["files"]
    if not registered or any(not safe_relative(p) for p in registered):
        raise ValueError("unsafe or empty fixture entries")
    changed: list[str] = []
    for rel, expected in sorted(registered.items()):
        path = output / rel
        if (any(parent.is_symlink() for parent in (path, *path.parents[:len(PurePosixPath(rel).parts) - 1])) or
                not path.resolve().is_relative_to(output.resolve()) or not path.is_file() or
                not isinstance(expected, str) or len(expected) != 64 or
                digest(path.read_bytes()) != expected):
            changed.append(rel)
    known = set(registered) | {"manifest.json"}
    additional = sorted(p.relative_to(output).as_posix() for p in output.rglob("*")
                        if p.is_file() and p.relative_to(output).as_posix() not in known)
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
