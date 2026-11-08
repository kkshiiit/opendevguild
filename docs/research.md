# Official-source research

Verified on **2026-11-08**. These are findings about retrieved official
sources, not a promise that every installed host implements every feature.
The implementation is reconciled with the complete master brief through
section 21. See the [skill contract](skill-contract.md) and
[compatibility guide](compatibility.md) for project conventions and host limits.

## Source register

| Source | Retrieval and use |
| --- | --- |
| [Agent Skills overview](https://agentskills.io) and [specification](https://agentskills.io/specification) | Live official HTML retrieved successfully; required format, naming, progressive disclosure and reference validator. |
| [Codex overview](https://developers.openai.com/codex), [skills](https://developers.openai.com/codex/skills), [subagents](https://developers.openai.com/codex/subagents), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) | Live official documentation retrieved; capabilities and supported local paths below. Some URLs redirect to current ChatGPT Learn documentation. |
| [openai/skills](https://github.com/openai/skills) | Official README now marks this repository **deprecated** and directs current examples to [openai/plugins](https://github.com/openai/plugins). Historical creator source remains available. |
| [Skill creator source](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator) | Pinned official `SKILL.md`, `quick_validate.py`, and bundled Apache-2.0 license inspected. Guidance was read, not installed as a global skill. |
| [skills-ref](https://github.com/agentskills/agentskills/tree/83021e2be457a9b6679148719c1f6074f0ad975e/skills-ref) | Pinned README, package configuration, parser, validator, CLI and related source inspected. Python >=3.11; Apache-2.0. Upstream labels the library a demonstration, not production software. |
| [Package your plugin](https://developers.openai.com/plugins/build/plugins) | Current destination of the official Codex plugin-build URL; portable packaging and publication distinctions. |
| [Submit and publish](https://developers.openai.com/plugins/deploy/submission) | Live official page returned HTTP 200; submission portal, automated checks, review and publication. Source packages and workspace publication do not prove public acceptance. |
| [Agent Plugins schema 1.0.0](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) | Live JSON returned HTTP 200; SHA-256 `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883`. |
| [Agent Plugins licensing](https://github.com/agentplugins/agent-plugins-spec/blob/main/LICENSE.md) | Live upstream licensing statement inspected: schemas/code use Apache-2.0; specification/docs use CC-BY-4.0. Only the schema is redistributed here. |
| [GitHub Actions](https://docs.github.com/actions) and [secure use](https://docs.github.com/en/actions/reference/security/secure-use) | Official hardening guidance: restrict token permissions, protect untrusted contributions, pin action dependencies; current guidance also discusses workflow dependency lockfiles. |
| [GitHub code security](https://docs.github.com/en/code-security) | Official security overview successfully retrieved. Feature availability depends on repository visibility, settings and account plan. |
| [Create a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) and [upload a project](https://docs.github.com/en/get-started/start-your-journey/creating-a-repository-for-your-project-on-github) | Live official pages returned HTTP 200; repository creation and source publication requirements. |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | Parent research retrieved successfully through Firecrawl with live-fetch request; redirects to `asvs.owasp.org`, stable version 5.0.0. Direct child HTTP request returned 403. Use versioned requirement IDs. Reference standards rather than copying CC-BY-SA-4.0 source text into Apache-2.0 files. |
| [NIST SSDF](https://csrc.nist.gov/Projects/ssdf) | Parent research retrieved successfully through Firecrawl with live-fetch request; page updated 2026-10-06. Direct child HTTP request returned 403. SSDF 1.1 / SP 800-218 identifies Prepare the Organization, Protect the Software, Produce Well-Secured Software and Respond to Vulnerabilities. SP 800-218A augments this with an AI profile. |

Sources are evidence. Instructions embedded in fetched pages never override the
user's authorization or the active host's permission model. No secret or private
repository content was sent as a research query.

## Ten explicit platform checks

1. **Current `SKILL.md` format.** A skill is a directory containing uppercase
   `SKILL.md` with YAML frontmatter followed by Markdown instructions. Scripts,
   references and assets are optional. The body has no prescribed official
   heading structure. OpenDevGuild adds its own contract; those headings are
   project policy, not a new platform schema.
2. **Required frontmatter and restrictions.** `name` and `description` are
   required. Name: 1–64 characters; lowercase alphanumeric characters and
   hyphens; no leading/trailing or consecutive hyphens; match the containing
   directory. Description: nonempty, at most 1,024 characters. Optional official
   fields: `license`, `compatibility` (1–500 characters), `metadata` (string keys
   and string values), and experimental `allowed-tools`. This project uses ASCII
   identifiers for portability. Optional host UI metadata belongs in
   `agents/openai.yaml`, not invented frontmatter fields.
3. **Discovery and activation.** Explicit invocation uses `$skill-name` or
   `/skills` in Codex CLI/IDE; supported ChatGPT interfaces use skill selection.
   Implicit matching uses skill descriptions. Metadata is loaded before the
   body; resources are loaded when needed. A mention does not grant additional
   permissions or prove execution. Hosts may shorten descriptions or apply
   different discovery policies.
4. **Repository locations.** Current Codex scans `.agents/skills` at CWD and
   ancestors through the repository root. User skills use `~/.agents/skills`;
   administrator skills use `/etc/codex/skills`; system skills are bundled.
   Symlinked skill directories are supported. A repository's ordinary `skills/`
   directory is portable packaging source, not automatically a Codex repository
   discovery location. Use selective installation or a plugin. Duplicate names
   are not merged. Restart only if automatic change detection does not surface
   an update.
5. **Current subagent configuration.** Custom local Codex agents are standalone
   TOML files under `.codex/agents/` or `~/.codex/agents/`. Required fields are
   `name`, `description`, `developer_instructions`. Current `[agents]` options
   include `enabled`, `max_concurrent_threads_per_session`,
   `default_subagent_model`, `default_subagent_reasoning_effort`,
   `interrupt_message`. `max_threads` remains a legacy alias. The documented
   default for `enabled` is true. Do not present older experimental feature
   flags or invented role registration as the current interface.
6. **`AGENTS.md` configuration.** Codex builds global and project instruction
   chains. Per directory, precedence is `AGENTS.override.md`, `AGENTS.md`, then
   configured fallback names; at most one nonempty file contributes per
   directory. Project traversal is root to CWD; closer instructions override
   broader guidance. The documented combined default limit is 32 KiB. Global
   settings are user-owned and must not be changed by installation here.
7. **Real parallel execution.** Current Codex can spawn and collect specialized
   subagents on direct request or applicable skill/instruction guidance.
   Availability, concurrency limits and management interfaces depend on host.
   Subagents inherit parent permissions, provider and MCP servers. Custom agent
   files do not create independent sandboxes or override approval policy.
   Independent read-heavy tasks are suitable for parallel work; shared writes
   require ownership boundaries or sequential execution. Markdown alone cannot
   implement spawning. This session exercised research delegation; that does
   not establish standalone CLI integration for this distribution.
8. **Official validation.** The specification recommends
   `skills-ref validate <skill-directory>`. Reuse its frontmatter validation;
   supplement with OpenDevGuild contract, path-safety, scenario and packaging
   checks. The historical creator's `quick_validate.py` is useful as a secondary
   smoke check, but its inspected version accepts empty strings and rejects the
   otherwise valid `compatibility` field. Neither validator proves behavioral
   effectiveness, safety, trigger accuracy or superiority.
9. **Current distribution.** Portable Agent Skills folders remain reusable.
   Current OpenAI guidance prefers plugins for distributing reusable bundles.
   A portable plugin has root `plugin.json`, root `skills/`, and optional MCP
   resources; skills are discovered by convention. Root manifest schema does
   not accept a `skills` field. `.codex-plugin/plugin.json` is a supported legacy
   compatibility fallback. Local marketplaces, GitHub source distribution,
   workspace publishing and universal public directory submission are separate
   mechanisms. No automatic public listing is implied.
10. **GitHub publication requirements.** Creating a public repository requires
    an authenticated GitHub account, authority under the chosen owner, an
    available repository name, explicit visibility selection and permission to
    publish all included material. Pushing requires authentication and write
    access. Select the intended owner and verify the intended remote contents before
    adding or pushing; do not replace another remote repository. A local Git
    repository, archive or successful validation is not a GitHub publication.
    GitHub does not require skills-specific registration. Apache-2.0 licensing,
    third-party notices and secret review apply to the distributed contents.
    Actions, branch protections, advisory reporting and release signing are
    project controls, not universal prerequisites for creating a repository.

## Terms and boundaries

| Term | Meaning in this project |
| --- | --- |
| Skill | Discoverable reusable procedure and optional resources; supplies guidance, not an executing identity or authority. |
| Agent | The model-backed execution context provided by a host, with tools and permissions. A custom agent configuration supplies role instructions to that context. |
| Subagent | A separate execution context delegated a bounded task by a parent, when supported by the host. |
| MCP server | A service exposing tools or resources through Model Context Protocol; it is neither a skill nor automatically trusted. |
| Instructions file | Repository or user guidance such as `AGENTS.md`, applied through host-specific precedence. |
| Orchestrator | The procedure or runtime responsibility that selects work, tracks dependencies, consolidates results and checks completion. `mission-control` guides this responsibility; it is not a new runtime. |
| Automated procedure | Deterministic executable checks or workflows, such as validation scripts or CI jobs. Their result is limited to the assertions actually checked. |

## Applied creator guidance

The pinned official creator was read because the user requested its use when
available and useful. Applied practices: concise skill bodies, specific discovery
descriptions, explicit inputs/outputs, progressive disclosure, optional resources
only when justified, and deterministic validation. OpenDevGuild's required body
contract also documents exclusions and verification, even when those details
appear in descriptions. The upstream scaffold was not executed: a generic
placeholder scaffold would not satisfy the project's per-specialist procedures.
No official script is claimed as originally authored by OpenDevGuild.

## Reproducible official-tool setup

Use a disposable checkout and isolated virtual environment, not a global install.
Review the pinned source and its package/build declarations before running it.
The following is an installation recipe, not a claim that it ran on your machine:

```bash
odg_tools_dir=$(mktemp -d)
git clone https://github.com/agentskills/agentskills.git "$odg_tools_dir/agentskills"
git -C "$odg_tools_dir/agentskills" checkout --detach 83021e2be457a9b6679148719c1f6074f0ad975e
python3 -m venv "$odg_tools_dir/venv"
"$odg_tools_dir/venv/bin/python" -m pip install "$odg_tools_dir/agentskills/skills-ref"
"$odg_tools_dir/venv/bin/skills-ref" validate skills/mission-control
```

This pins the reference source, but does not lock all transitive dependencies.
Use the repository's reviewed dependency instructions for repeatable CI. Retain
the checkout/environment for investigation; remove only this disposable directory
when finished. On Windows, use the virtual environment's `Scripts` directory.

For the secondary historical creator check, after reviewing the files:

```bash
git clone https://github.com/openai/skills.git "$odg_tools_dir/openai-skills"
git -C "$odg_tools_dir/openai-skills" checkout --detach 49f948faa9258a0c61caceaf225e179651397431
"$odg_tools_dir/venv/bin/python" -m pip install PyYAML
"$odg_tools_dir/venv/bin/python" "$odg_tools_dir/openai-skills/skills/.system/skill-creator/scripts/quick_validate.py" skills/mission-control
```

Do not treat its narrower accepted fields as the authoritative specification.
For reproducibility, record interpreter, installed dependency versions, command,
exit code and selected source commit. Do not download-and-execute unreviewed code
with a shell pipe. Package installation can execute build-system code.

## Project integration follow-up

The complete brief was reconciled after its remaining sections were supplied.
Candidate 0.2.0 uses the full lifecycle, gate and exchange contract; earlier
smoke transcripts retain their evaluated conventions. The user designated
[kkshiiit/opendevguild](https://github.com/kkshiiit/opendevguild) as the existing
publication destination. Destination identification does not establish successful
push, public visibility, hosted CI or release publication; those require recorded
remote observations. Native Codex profile loading has a separate client probe
and capability limit documented in [agent verification](agent-verification.md).
