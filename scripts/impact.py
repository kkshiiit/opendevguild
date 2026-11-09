"""Conservative, read-only test planning from changed repository paths.

This suggests a fast local *preflight*, never replaces full CI or runs tests.
It makes no claim about model behavior or measured token savings.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def changed_since(base: str, root: Path = ROOT) -> list[str]:
    """Return all tracked changed paths, including deletions and staged edits."""
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_./~^@{}+\-]*", base) or base.endswith("/"):
        raise ValueError("invalid base revision")
    result = subprocess.run(
        ["git", "diff", "--name-only", "-z", base, "--"],
        cwd=root, capture_output=True, check=False,
    )
    if result.returncode:
        raise ValueError("git diff failed: check that the base exists and this is a Git checkout")
    return sorted(set(x.decode("utf-8", "surrogateescape") for x in result.stdout.split(b"\0") if x))


def normalized_path(value: str) -> str:
    if not value or "\\" in value or "\x00" in value:
        raise ValueError("unsafe path: empty, backslash, or NUL")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or ":" in value or value.startswith("-"):
        raise ValueError("unsafe or absolute path")
    return path.as_posix()


def tests_for_path(path: str) -> tuple[set[str], str]:
    """Return conservative local tests or special marker '*' for full suite."""
    if path in {"AGENTS.md", "catalog.json", "plugin.json", "pyproject.toml", "uv.lock"}:
        return {"*"}, "shared policy or packaging dependency"
    if path.startswith((".github/", "contracts/")):
        return {"*"}, "cross-cutting workflow or evidence schema"
    if path.startswith(".codex/agents/"):
        return {"test_agents.py", "test_protocol.py"}, "custom agent contracts"
    if path.startswith("skills/"):
        parts = path.split("/")
        if len(parts) < 3:
            return {"*"}, "unrecognized skill-level path"
        tests = {"test_protocol.py", "test_routing.py"}
        if "visual" in parts[1] or parts[1] in {
            "material-rendering-engineer", "color-science-engineer",
            "motion-interaction-engineer", "design-to-code-engineer",
            "typography-composition-engineer", "ui-design-system",
        }:
            tests.add("test_visual.py")
        if any(x in parts[1] for x in ("security", "privacy", "supply-chain")):
            tests.add("test_security.py")
        return tests, "skill format and selection; specialist checks as applicable"
    if path.startswith("visual/"):
        return {"test_visual.py"}, "visual fixtures and verification"
    if path.startswith("evaluations/"):
        if path.startswith("evaluations/scenarios/") or path.startswith("evaluations/routing"):
            return {"test_protocol.py", "test_routing.py"}, "routing and scenario fixtures"
        if path.startswith("evaluations/research"):
            return {"test_research.py"}, "research fixtures"
        if path.startswith("evaluations/dependency") or path.startswith("evaluations/security"):
            return {"test_security.py"}, "security evidence"
        return {"*"}, "other evaluation evidence requires full review"
    if path.startswith("scripts/"):
        name = path.removeprefix("scripts/")
        pairs = {
            "impact.py": {"test_impact.py"},
            "client_probe.py": {"test_client_probe.py"},
            "install.py": {"test_installation.py"},
            "research.py": {"test_research.py"},
            "visual.py": {"test_visual.py"},
            "capture_visual.py": {"test_visual.py"},
            "verify_release.py": {"test_release_verification.py"},
            "routing.py": {"test_routing.py"},
            "evaluate.py": {"test_routing.py"},
        }
        if name in pairs:
            return pairs[name], "matching tooling regression suite"
        return {"*"}, "unknown or cross-cutting tooling"
    if path.startswith("tests/") and re.fullmatch(r"test_[a-z0-9_]+\.py", path.removeprefix("tests/")):
        return {path.removeprefix("tests/")}, "modified test module"
    if path.startswith("docs/") or path in {
        "README.md", "README.es.md", "CHANGELOG.md", "LICENSE",
        "NOTICE", "CONTRIBUTING.md", "CONTRIBUTING.es.md",
        "GOVERNANCE.md", "CODE_OF_CONDUCT.md", "SECURITY.md",
    }:
        return {"test_documentation.py"}, "documentation and reference links"
    return {"*"}, "unclassified change; fail closed to full suite"


def select_tests(paths: list[str], available: set[str]) -> dict:
    selected: set[str] = set()
    reasons: dict[str, str] = {}
    full = False
    for raw in sorted(set(paths)):
        path = normalized_path(raw)
        tests, reason = tests_for_path(path)
        reasons[path] = reason
        if "*" in tests:
            full = True
        selected.update(tests - {"*"})
    if full:
        selected = set(available)
    missing = sorted(selected - available)
    if missing:
        raise ValueError("expected test modules missing: " + ", ".join(missing))
    return {
        "kind": "local-preflight-recommendation",
        "changed_paths": sorted(reasons),
        "reasons": reasons,
        "full_suite": full,
        "tests": sorted(selected),
        "commands": (["uv run --frozen python -m unittest discover -s tests -v"]
                     if full else [
                         f"uv run --frozen python -m unittest discover -s tests -p {name} -v"
                         for name in sorted(selected)
                     ]),
        "limitations": [
            "No tests were executed by this planner.",
            "Manual judgment can require additional tests or a full local run.",
            "GitHub CI remains the full acceptance gate; this is not proof of reduced tokens.",
            "--base reads tracked diff paths; pass untracked paths explicitly with --paths.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--base", help="Git revision to diff against working tree")
    source.add_argument("--paths", nargs="+", help="Changed paths relative to repo root")
    args = parser.parse_args(argv)
    try:
        paths = changed_since(args.base) if args.base is not None else args.paths
        available = {p.name for p in (ROOT / "tests").glob("test_*.py")}
        result = select_tests(paths, available)
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
