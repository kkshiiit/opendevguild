# Native Claude Code plugin

[Español](claude-code.es.md) · [Client evidence](client-compatibility.md)

This adapter is added **after v0.4.1**. Use the checkout containing this change;
the published v0.4.1 ZIP/tag remains unchanged and does not contain this adapter.
No new release or listing in Anthropic's directory is claimed.
Before merge, select the PR branch `feat/claude-code-native-plugin`; after merge,
use a reviewed main checkout. A download of the old release is insufficient.

## Load locally without global installation

Prerequisites: your own installed Claude Code client and its normal functional
session. No Codex executable, account or authentication is involved. Review the
checkout first. From a disposable application directory, use its absolute path:

```text
claude --version
claude plugin validate /absolute/path/to/opendevguild
claude --plugin-dir /absolute/path/to/opendevguild
```

The last command loads the plugin for that session; it does not register a global
marketplace or overwrite your settings. Where supported, `claude plugin validate
/absolute/path/to/opendevguild --strict` also rejects warnings. These are current
official commands, **not commands executed in the authoring environment**: no
`claude` executable or Claude connector was available. No minimum supported
version is invented; check your client's help and record its actual version.

The native manifest is `.claude-plugin/plugin.json`. The existing root
`plugin.json` serves a different host format; it is not the Claude manifest.
Claude's default `skills/` discovery reuses the same 42 original skill folders,
including their references. Availability is not activation: do not load every
instruction body for a trivial task. Do not install duplicate manual copies in
`.claude/skills/` just to use the plugin.

## Select one skill

In the fresh Claude session, inspect the available plugin commands and try:

```text
/opendevguild:scope-guardian Assess the scope for correcting discount arithmetic in buggy.py. Only buggy.py and focused tests are in scope. Read-only: do not edit files, run commands or use the network. State boundaries, exclusions, acceptance checks and missing inputs.
```

Plugin skills use `/opendevguild:<skill-name>`. A manually installed standalone
skill uses `/scope-guardian` instead. These namespaces are different. Expected:
a bounded scope brief grounded in the supplied files, with no unrelated edits.
Do not count a model saying it used a skill as proof of reading its instructions.

## One optional native reviewer

Only `agents/reviewer.md` is adapted. Ask for it when independent review has a
clear benefit, supplying the objective, relevant files/diff and existing test
evidence. It is not required for a single-skill scope task:

```text
Use opendevguild:reviewer for a read-only review of buggy.py against the supplied discount requirement. Return justified findings with severity, exact location and counterexample. Do not edit, run commands or spawn another agent.
```

The manifest declares the **file**, `./agents/reviewer.md`, not an agents
directory. Native YAML frontmatter restricts declared tools to `Read, Grep, Glob`
and inherits the caller's model. No Bash, editing, network/MCP, Agent, hooks or
global settings are configured. The body is self-contained; it preloads no skills.
The original eight Codex TOML profiles are preserved and are not Claude agents.

Plugin subagents ignore `permissionMode`, `hooks` and `mcpServers` frontmatter;
none is shipped. Tool declarations are not an OS sandbox or a credential boundary:
the host still enforces workspace/privacy policy. The reviewer reports execution
checks as `not_run` because it cannot run test commands. Parent-supplied evidence
and self-review conflicts must remain explicit.

## Reproducible check in your authenticated client

Create a new temporary project and use only synthetic inputs. A minimal file is:

```python
def total_after_discount(total, discount):
    return max(0, total + discount)
```

Required behavior is subtraction. Keep the plugin checkout separate from this
application. Record hashes of all fixture files before execution. Run exactly one
scope request first, in a new context, with read-only host permissions.
`--plugin-dir` alone does not make the main session read-only; configure those
permissions in your client before the trial.
Keep the host's unrelated plugins and inherited instructions out of the trial,
or record contamination and do not attribute behavior to this adapter. Do not
delete or rewrite global configuration to obtain that isolation.

Record:

- Exact Claude version, plugin path/revision and discovered skill/agent inventory.
- Actual instruction-read/tool events and response, not only self-reported usage.
- Before/after file hashes and unexpected additions; read-only means no changes.
- Discovery, instruction activation and task behavior as **separate** results.

If discovery or a required read event is unavailable, label it `NOT_VERIFIED`.
If Claude authentication fails, stop and record `BLOCKED_BY_AUTH` for **Claude**;
do not run Codex or transfer credentials. Reviewer dispatch needs its own actual
child invocation and result. No agent should approve its own unobserved activation.

## What was actually checked

| Check | Evidence state |
| --- | --- |
| Native manifest/agent policy, reused skill inventory and selected distribution files | Offline tests; part of ordinary full project CI |
| Official `claude plugin validate` | NOT_RUN: Claude executable unavailable |
| Claude plugin discovery / skill-body activation / behavior | NOT_RUN: no Claude session available |
| Native reviewer dispatch and read-only runtime enforcement | NOT_RUN: no Claude session available |

The project validator enforces a deliberately small supported field set for this
adapter. It is **not** Anthropic's authoritative schema/validator. Unknown hooks,
escaped agent paths, extra tools and ignored permission overrides are rejected by
project policy. Standard auto-discovery locations such as root `.mcp.json`,
`settings.json`, `hooks/` and `commands/` are also refused even if the manifest
omits those fields. Packaging includes the two explicit adapter files and shared
skills, never `.claude/` settings, credentials, caches or arbitrary plugin state.
The native manifest's version matches the project catalog; bump it deliberately
on future published plugin updates. No dependencies or model benchmark added.

## Sources and retrieval limits

Official pages read on 2026-11-09 via Firecrawl (HTTP 200); direct retrieval from
this workspace returned HTTP 403. Original procedural adaptation, no copied
vendor implementation or redistributed documentation:

- [Plugin manifest reference](https://code.claude.com/docs/en/plugins-reference): native path, default skills directory, explicit agent-file paths, validation.
- [Subagents](https://code.claude.com/docs/en/sub-agents): Markdown/YAML format, read-only tool examples, model inheritance, ignored plugin fields.
- [Marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces): namespaces and local development without a marketplace. No marketplace is introduced here.
