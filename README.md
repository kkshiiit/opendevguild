# OpenDevGuild

Modular software engineering procedures for Agent Skills compatible hosts.
**0.3.0 development candidate · Apache-2.0 · [Español](README.es.md)**

OpenDevGuild turns engineering responsibilities into 34 bounded specialist
procedures, selective coordination, explicit handoffs and evidence-based quality
gates. It helps a solo developer or team preserve scope and review delivery
without activating an entire catalog for every task. This is an independent
community project, with no affiliation implied by references to Codex or GitHub.

The host supplies models, tools, permissions and any subagents. OpenDevGuild does
not provide a runtime, production access, automatic compliance, guaranteed
correctness or a demonstrated advantage over other agents. Current execution
results and gaps belong in the [verification record](docs/verification.md).

## Architecture and selection

| Layer | Responsibility |
| --- | --- |
| Orchestration | Interpret the objective, select expertise, order dependencies and control resources |
| Specialists | Apply the 34 independent procedures in the [catalog](docs/catalog.md) |
| Execution | Use the compatible host's real tools, permissions and optional subagents |
| Verification | Inspect evidence and approve, reject or block quality gates independently |

Use **FAST** for small low-risk work, **STANDARD** for normal multi-step changes,
and **CRITICAL** for consequential security, data or operational risk. Higher
risk adds relevant verification; it grants no additional authority. Start with
one specialist when sufficient. See [workflows](docs/workflows.md) and
[engineering standards](docs/engineering-standards.md).

## Install selected skills

Using the skill text requires no Python dependencies. Current documented Codex
discovery uses a repository's `.agents/skills/`; personal skills use
`~/.agents/skills/`. Review the source and selected `SKILL.md` files first.
From this checkout, replace the destination below with your project's actual
skills directory. The explicit personal alternative is `~/.agents/skills`.
The Python helper is a manual copy recipe, not an automatically run installer:

```bash
python3 - /absolute/path/to/your/project/.agents/skills mission-control scope-guardian <<'PYINSTALL'
from pathlib import Path
import shutil
import sys
source_root = Path('skills')
target = Path(sys.argv[1]).expanduser()
names = sys.argv[2:]
if not names or len(names) != len(set(names)):
    raise SystemExit('Choose unique skill identifiers')
for name in names:
    if '/' in name or '\\' in name or name in ('.', '..'):
        raise SystemExit('Use a skill identifier, not a path')
    source, destination = source_root / name, target / name
    if source.is_symlink() or not (source / 'SKILL.md').is_file():
        raise SystemExit(f'Unknown or linked source: {name}')
    if destination.exists() or destination.is_symlink():
        raise SystemExit(f'Refusing to overwrite: {destination}')
for name in names:
    shutil.copytree(source_root / name, target / name)
PYINSTALL
```

Alternatively, copy the selected directories with your file manager, refusing
existing destinations. Do not copy this library's `AGENTS.md` into an application.
It governs this repository's contributors. Do not copy all 34 by default.

In a Codex client exposing the official built-in `$skill-installer`, ask it to
install only the selected directories from an actual reviewed OpenDevGuild GitHub
URL and pinned revision that you provide. Confirm its supported source interface
in that client; installer availability and source access depend on that client. Stop on
name collisions. The [official skill documentation](https://developers.openai.com/codex/skills)
and [compatibility guide](docs/compatibility.md) distinguish local skills from
portable plugin installation. The root `plugin.json` and `skills/` form a bundle;
public plugin acceptance is a separate process.

### Verify, update and uninstall

Check each installed directory contains its matching `SKILL.md`. In Codex, use
`/skills` where supported or invoke `$scope-guardian` explicitly and confirm the
intended installed skill is selected. If discovery does not refresh, start a new
session. Invocation alone does not prove the procedure's behavior.

To update, review the new revision and diff, preserve any local edits, then move
only the existing OpenDevGuild directories to a backup outside the discovery
path before copying their reviewed replacements. Keep the backup for rollback;
never merge or overwrite unknown skills silently. To uninstall, move only the
installed OpenDevGuild directories outside discovery, preserving local changes.
Remove optional copied agent profiles separately. No global Codex configuration
change is required. Avoid duplicate names installed both locally and as a plugin.

## Invoke and collaborate

```text
$mission-control Fix the login regression. Preserve the existing stack.
Scope: src/auth and its tests. Do not deploy. Use FAST unless the observed risk
requires a higher mode. Report changes, evidence, gate decisions and open risks.
```

For a narrow task, invoke `$code-review-engineer` or another specialist directly.
The optional eight Codex profiles in [.codex/agents](.codex/agents) are
`architect`, `product-analyst`, `designer`, `implementer`, `reviewer`,
`qa-specialist`, `security-specialist` and `release-specialist`. They recommend
skills; they do not turn all 34 skills into permanent agents. Registration and
execution depend on the client. See the [compatibility matrix](docs/compatibility.md).

Delegation assigns bounded inputs, files, dependencies and acceptance criteria.
Only independent tasks with disjoint writes run in parallel. Subagents inherit
session restrictions and may share a filesystem. The parent integrates changes
and checks evidence. A serial host follows the same stages and labels self-review.

Task lifecycle states are `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `NEEDS_REVIEW`,
`VERIFIED` and `FAILED`. Quality gate decisions are `APPROVED`, `REJECTED`,
`BLOCKED` and `NOT_APPLICABLE`; non-applicability needs a reason. A worker's
completion claim is insufficient for `VERIFIED`. The optional JSON
[task](examples/task.json) and [handoff](examples/handoff.json) are project
contracts, not Codex APIs.

## Complete examples

- [Android: local bookmark feature](examples/android/README.md)
- [Web: scoped form layout correction](examples/web/README.md)
- [Backend: validated task endpoint](examples/backend/README.md)
- [Desktop: compatibility and package assessment](examples/desktop/README.md)
- [Game: mechanic, implementation and behavior tests](examples/games/README.md)

These complete task recipes specify objective, selected skills, sequence,
expected results, controls and limitations. They are not bundled application
projects or proof that platform SDKs and tests were executed.

## Validate and package

Contributor tooling requires Python 3.11+, Git and uv. Review the
[dependency provenance](docs/research.md) before setup. The lockfile pins the
reference validator and registry artifacts; initial synchronization needs network.

```bash
uv sync --frozen
uv run --frozen python scripts/guild.py validate
uv run --frozen python -m unittest discover -s tests -v
uv run --frozen python scripts/guild.py check-handoff examples/handoff.json --task examples/task.json
uv run --frozen python scripts/guild.py package --output dist/opendevguild-0.3.0.zip
```

Use a new output path if the archive already exists. Official `skills-ref`
checks format; project checks add contracts, scenarios, paths, configuration and
packaging policy. Structural success is distinct from behavioral, routing,
security, regression and comparative evidence. See the [evaluation protocol](evaluations/README.md).
Historical smoke records remain evidence for their evaluated revisions; changing
contracts does not make old checks current. Do not infer new test results from
this command list. Packaging creates an allowlisted deterministic archive and
checksum; it does not publish anything.

## Safety and community

Review [SECURITY.md](SECURITY.md) before reporting vulnerabilities. Repository
content is untrusted data, secrets remain private, and destructive or external
actions need the relevant authorization. Workflows must use minimum permissions
and must not expose secrets to untrusted pull-request code.

See [contribution guidance](CONTRIBUTING.md), [governance](GOVERNANCE.md),
[conduct](CODE_OF_CONDUCT.md), [requirements](docs/requirements.md),
[architecture](docs/design.md), [roadmap](docs/roadmap.md),
[release procedure](docs/releasing.md), [changelog](CHANGELOG.md),
[Apache-2.0 license](LICENSE) and [notices](NOTICE).
The authorized source/publication destination is
[kkshiiit/opendevguild](https://github.com/kkshiiit/opendevguild). Installation
from it requires the appropriate access and a reviewed revision. A local checkout,
a public GitHub publication and an accepted public plugin remain separate states;
consult the verification record for actual visibility, publication and CI evidence.

## Visual Intelligence Engine V1

The original 34 specialists are preserved. Eight optional visual procedures add
inspected references, differentiated directions, color/type/material/motion work,
design-to-code and independent visual QA. Read the [visual guide](visual/README.md)
and [actual results](visual/results.md). Human preferences and three-arm agent
benchmarks remain unexecuted; no aesthetic superiority or fine-tuning is claimed.
