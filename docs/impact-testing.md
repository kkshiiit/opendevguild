# Selective local test preflight (maintainers)

[Español](impact-testing.es.md) · [Contributing](../CONTRIBUTING.md)

`python scripts/impact.py` **suggests** local unit-test modules based on changed
paths. It is a read-only planning tool using the Python standard library. It does
not run tests, call a model, read credentials, change files or measure tokens.

Use it to get faster feedback during a small change. The complete test suite,
validation, dependency/security checks and hosted CI remain required before
acceptance or release. The mapping is conservative; unfamiliar changes and shared
contracts request the full suite instead of silently omitting checks.

## From a checkout

```bash
python scripts/impact.py --base HEAD
python scripts/impact.py --paths skills/visual-art-director/SKILL.md
python scripts/impact.py --paths scripts/research.py docs/research-program.md
```

The output is JSON with changed paths, reasons, `full_suite`, selected `tests`,
copyable `commands` and limitations. Review it before running the commands. A
single research-tool change should select `test_research.py`; changes to a shared
JSON schema, unknown path or GitHub workflow request the complete suite.

`--base` compares the **tracked** working-tree diff (staged and unstaged) to the
specified existing revision. It excludes untracked files; include their paths
using `--paths`. Neither option fetches branches from a remote. Do not pass an
untrusted revision or invent a baseline. An empty diff prints no selected tests;
it is not evidence that the repository is verified.

## Guardrails

- Always inspect `git status` and review the actual scope first.
- The tool plans tests; executing its output is a separate, explicit action.
- Changes to `scripts/guild.py`, contracts, manifests or workflows can affect many
  checks and intentionally trigger the complete suite.
- A selected fast suite is **not** permission to skip full CI or independent
  review. Add other tests when the behavior crosses the simple path map.
- No measured speedup, token savings, correctness or agent improvement is claimed.

Run the tool's own offline tests:

```bash
python -m unittest discover -s tests -p test_impact.py -v
```

Before merging or releasing, retain the established full checks:

```bash
uv run --frozen python scripts/guild.py validate
uv run --frozen python -m unittest discover -s tests -v
```

The planner needs Python 3.11+, but **installing and using an individual Agent
Skill does not**. It is maintainer tooling, not a client plugin or agent runtime.
