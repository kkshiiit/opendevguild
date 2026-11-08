# Compatibility and host integration

Reviewed 2026-11-08. OpenDevGuild provides portable procedures and local validation
assets. It is not a runtime, permissions broker, sandbox, MCP server or guaranteed
scheduler. See [official-source research](research.md) for exact source dates.

## Capability matrix

| Surface | Supported design | Evidence and limitation |
| --- | --- | --- |
| Agent Skills | skills/<name>/SKILL.md with standard frontmatter | Official format validation covers implemented rules; behavior needs separate execution |
| Current documented local Codex | Selective repository .agents/skills or personal ~/.agents/skills; optional .codex/agents profiles | Official paths/fields verified; loading a skill does not spawn an agent |
| Observed workspace CLI | codex-cli 0.167.0-alpha.4 | Version command observed; native profile probe is BLOCKED by expired CLI authentication; no role-loading/execution claim follows from the version |
| Hosted engineering session | Actual bounded subagent delegation and fresh-context smoke samples | Host tools worked; this does not prove users' standalone clients expose identical interfaces |
| Other compatible hosts | Host-specific discovery of portable skill directories | Format portability is a goal; no blanket claim of tested models, operating systems or client versions |
| Sequential host | Apply selected stages serially with explicit handoffs | Self-review is labeled and leaves NEEDS_REVIEW until independent verification is available |
| Portable plugin | Root plugin.json and conventional root skills/ | Schema validity does not prove installation, working discovery or public review acceptance |

Consult the [verification record](verification.md) for actual test outcomes and
current limits and [agent verification](agent-verification.md) for the client probe. Missing SDKs, devices, browser, database, network, signing identity
or credentials remain blocked/unexecuted capabilities. Instructions cannot supply
them or override the host's approval policy.

## Discovery and installation

Repository discovery uses `.agents/skills` from CWD through ancestors to the
repository root. Personal discovery uses `~/.agents/skills`. The canonical
`skills/` here is distribution source, not a second implicit local discovery
path. Copy only selected directories using the README recipe or a file manager;
refuse collisions and preserve local modifications. Symlinked folders are
currently documented, but copied directories avoid platform-specific symlink
behavior. No global configuration edits or automatic personal installation occur.

In supported Codex clients use `$skill-name` explicitly or `/skills` to select.
Implicit matching depends on descriptions and the host. If an official built-in
`$skill-installer` is exposed, provide an actual reviewed repository URL, desired
skill paths and pinned revision using its documented interface. No remote source
or installer availability is assumed here. Manual installation is the fallback.

After copying, inspect the installed name/file, check discovery and invoke a
bounded task in a fresh session if needed. Updating means reviewing a new revision,
backing up only the owned skill folders outside discovery and installing the
replacements without overwriting unknown content. Uninstall by moving those
folders outside discovery, preserving edits. Optional agent files are separate.
Avoid duplicate names from local and plugin installs in the same context.

## Eight optional Codex profiles

Current official docs use standalone TOML files in `.codex/agents/` or
`~/.codex/agents/`. Required fields are `name`, `description` and
`developer_instructions`. The canonical profiles in this repository are:

| Profile | Bounded responsibility | Typical procedures |
| --- | --- | --- |
| architect | Architecture alternatives and component contracts | system-architect, architecture-decisions |
| product-analyst | Requirements, scope and planning | requirements-engineer, scope-guardian, delivery-planner |
| designer | Interaction, visual and accessibility decisions | ux-research-design, ui-design-system, accessibility-engineer |
| implementer | Authorized incremental implementation | Matching platform specialist or implementation-engineer |
| reviewer | Independent evidence-backed findings | code-review-engineer, scope-guardian |
| qa-specialist | Test strategy, automation and regression | test-strategy-engineer, qa-automation-engineer |
| security-specialist | Defensive security, privacy and supply chain | security-engineer, privacy-engineer, supply-chain-auditor |
| release-specialist | Integration, gates and authorized release preparation | devops-ci-engineer, release-engineer, documentation-engineer |

These files supply role guidance, recommended skills, limits, exchange format,
delegation conditions and completion criteria. They do not install skills,
register themselves on other machines, start 34 workers or enforce OS-level
read-only access. Do not copy this repository's AGENTS.md to an application.
Review and copy only compatible selected profile files into the target project's
`.codex/agents/`, refusing existing destinations. Do not alter personal agent or
global Codex configuration implicitly. Native registration is a distinct test
from TOML parsing and from hosted tool delegation.

Custom agents inherit sandbox, approval policy, provider and MCP settings.
Workers may share a filesystem and have the same permissions. Assign disjoint
write paths and prerequisite evidence; serialize shared contracts, files and
migrations. The parent integrates artifacts and checks evidence. A role's
instruction not to edit is a behavioral boundary, not a security sandbox.

Where a user intentionally configures an existing compatible client, the current
documented concurrency setting is:

```toml
[agents]
max_concurrent_threads_per_session = 2
```

This is an illustrative cap on spawned threads excluding the primary, not a
project requirement or install instruction. Preserve existing config. Current
docs describe `agents.enabled` as true by default and `max_threads` as a legacy
alias. Do not add historical experimental flags or invent role registration.
Use serial execution when parallelism has no clear benefit or the host lacks it.

## Portable plugin

The current schema requires `$schema` and `name`; this project also supplies
version, description and Apache-2.0 license metadata. Root `skills/` is discovered
by convention; do not add an unsupported root `skills` property. The retrieved
schema is draft 2020-12, version 1.0.0; its hash and licensing are in
[research](research.md). `.codex-plugin/plugin.json` is a documented legacy
fallback, not another catalog that this project must duplicate.

Client installation, workspace publication, GitHub release and universal public
plugin listing are separate outcomes. Test a package in the intended client
before advertising integrated compatibility. Follow the current platform review
process for a public listing. A valid archive or root manifest does not establish
that any external service accepted it.

## Exchange compatibility and limits

Candidate 0.2.0 reconciles the full collaboration contract. Lifecycle states are
NOT_STARTED, IN_PROGRESS, BLOCKED, NEEDS_REVIEW, VERIFIED and FAILED. Gate decisions
are APPROVED, REJECTED, BLOCKED and justified NOT_APPLICABLE. Modes are FAST,
STANDARD and CRITICAL. Earlier candidate smoke records may contain older output
conventions; they remain historical evidence and are not valid current handoffs.

Recheck official docs before changing adapters, record actual versions and test
results, and keep vendor-specific configuration separate from portable skills.
Security, privacy and accessibility procedures do not confer certification or
legal compliance. Self-review alone cannot establish VERIFIED; independent review
and applicable gate evidence are required.
