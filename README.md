# OpenDevGuild

## Quick start

**0.4.0 development release · Apache-2.0 · [Español](README.es.md)**

OpenDevGuild provides **34 engineering skills and eight visual specialists** for
compatible AI clients. The client supplies the model, tools and permissions;
copying a skill does not start agents, edit your app or grant access automatically.

1. [Download the repository ZIP](https://github.com/kkshiiit/opendevguild/archive/refs/heads/main.zip)
   using **Code → Download ZIP**, or clone:

   ```text
   git clone https://github.com/kkshiiit/opendevguild.git
   ```

2. Extract/open the download. Review `skills/scope-guardian/SKILL.md`. Copy only
   the `scope-guardian` folder into **your application repository's**
   `.agents/skills/`, refusing an existing destination. Do not copy this library's
   `AGENTS.md` or install all 42 skills by default.
3. Open your application in a supported Codex client. Check `/skills` lists the
   installed skill; start a new session if needed. Then try:

   ```text
   $scope-guardian Define the scope for fixing the login error. Do not edit files.
   Identify affected paths, exclusions, acceptance checks and missing information.
   ```

Expect a bounded scope brief, not an automatic fix. If the skill is not listed,
follow [troubleshooting](docs/troubleshooting.md); a model merely repeating its
name does not prove loading. **Using the skill text needs no Python or uv.** Git
is optional when downloading ZIPs. The client has its own installation requirements.

**Start here:** [Installation](docs/installation.md) · [Quick usage](docs/quickstart.md)
· [Client/platform evidence](docs/client-compatibility.md) ·
[Eight copyable task examples](docs/usage-examples.md).

## What is included

| Layer | Responsibility |
| --- | --- |
| Orchestration | Select only needed expertise, order dependencies and set resource limits |
| Specialists | Apply the 42 procedures in the [catalog](docs/catalog.md) |
| Execution | Use a compatible host's actual tools, permissions and optional subagents |
| Verification | Inspect evidence and independently approve, reject or block quality gates |

Modes are FAST, STANDARD and CRITICAL according to task risk; mode grants no
extra authority. Eight optional [.codex/agents](.codex/agents) profiles recommend
specialists. Installing skills and configuring subagents are separate operations;
profile parsing is not proof of runtime loading. See the
[compatibility matrix](docs/client-compatibility.md).

[Visual Intelligence Engine V1](visual/README.md) adds original inspected
references, color/type/material/motion procedures, rendered evidence and independent
visual review. [Actual results](visual/results.md) distinguish measurements from
human preferences. No aesthetic superiority, model fine-tuning, automatic legal
compliance or token-saving guarantee is claimed.

## Installation, maintenance and app work

The [installation guide](docs/installation.md) covers manual download, release
checksum verification, POSIX and PowerShell paths, project/personal choices,
update, uninstall and rollback without losing local edits. The optional local
[managed installer](docs/installer-reference.md) requires Python; ordinary manual
installation does not. No remote shell script or silent global install is required.

[Usage examples](docs/usage-examples.md) cover fixes, review, UI, Android planning,
backend tests, security/licensing, releases and complex missions. Platform recipes:
[Android](examples/android/README.md), [web](examples/web/README.md),
[backend](examples/backend/README.md), [desktop](examples/desktop/README.md),
[games](examples/games/README.md). These describe work on a supplied application;
they do not install OpenDevGuild or prove native SDK execution.

## Contributor validation

Only contributors and validators need Python 3.11+, Git and uv. Review
[provenance](docs/research.md) before synchronizing locked dependencies:

```bash
uv sync --frozen
uv run --frozen python scripts/guild.py validate
uv run --frozen python -m unittest discover -s tests -v
uv run --frozen python scripts/guild.py check-handoff examples/handoff.json --task examples/task.json
uv run --frozen python scripts/guild.py package --output dist/opendevguild-0.4.0.zip
```

Choose a new output path if it exists. Visual browser checks additionally require
the optional visual group and explicit browser installation; see the
[visual guide](visual/README.md). Never interpret structural checks as proof of
all model behaviors. [Verification](docs/verification.md),
[final report](docs/final-report.md) and [evaluation protocol](evaluations/README.md)
retain actual results, failures and unexecuted checks.

## Project information

[Requirements](docs/requirements.md) · [Architecture](docs/design.md) ·
[Workflows](docs/workflows.md) · [Standards](docs/engineering-standards.md) ·
[Roadmap](docs/roadmap.md) · [Releases](docs/releasing.md) · [Changelog](CHANGELOG.md).

[Security](SECURITY.md) · [Contributing](CONTRIBUTING.md) ·
[Governance](GOVERNANCE.md) · [Conduct](CODE_OF_CONDUCT.md) ·
[Apache-2.0](LICENSE) · [Notices](NOTICE).

Independent community project; vendor references describe compatibility, not
affiliation. The official repository is [kkshiiit/opendevguild](https://github.com/kkshiiit/opendevguild).
A source release and acceptance into a public plugin directory are different states.
