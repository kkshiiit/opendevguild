# Client and platform evidence / Compatibilidad por cliente y plataforma

Reviewed **2026-11-09**. Labels are deliberately separate:
**VERIFIED / VERIFICADO** means the named observation actually ran;
**DOCUMENTED_NOT_TESTED / DOCUMENTADO_PERO_NO_PROBADO** means current official
sources support it but this project did not execute it;
**NOT_SUPPORTED / NO_SOPORTADO** means this release supplies no such integration.
No undocumented minimum client version is invented.

| Surface | Version evidence | Project/personal path or mechanism | State and limits |
| --- | --- | --- | --- |
| Codex CLI/IDE skills | Observed CLI0.167.0-alpha.4; not a minimum guarantee | `.agents/skills/`, `~/.agents/skills/` | DOCUMENTED_NOT_TESTED for native discovery/activation; authoring invocation blocked by expired authentication. `$name` and `/skills` documented. |
| Codex custom profiles | Same observed CLI; current official mandatory3 fields | `.codex/agents/`, optional `~/.codex/agents/` | VERIFIED syntax/field tests; DOCUMENTED_NOT_TESTED runtime loading. No tool, sandbox or isolation guarantee. |
| ChatGPT | Account/interface availability varies; no fixed tested version | Admitted plugin/workspace upload/publishing UI; bundle `plugin.json` plus `skills/` | DOCUMENTED_NOT_TESTED packaging mechanism; manual `.agents/skills` installation into ChatGPT is NOT_SUPPORTED. GitHub release is not plugin approval. |
| Claude Code | Current official docs; local executable unavailable, version not observed | Native `.claude-plugin/plugin.json`, default `skills/`, one `agents/reviewer.md`; load via `--plugin-dir` | Offline policy/packaging tested; official validator, discovery, `/opendevguild:name` activation and native child execution NOT_RUN. [Guide](claude-code.md). Codex profiles remain separate. |
| Gemini CLI | Current docs, no local executable/version observed | `.gemini/skills/` or `.agents/skills/` alias; corresponding home paths | DOCUMENTED_NOT_TESTED; `/skills list`, `/skills reload` and native install/link commands documented. No syntax equivalence to Codex asserted. |
| Other hosts | None established | Follow that host's actual Agent Skills documentation | NOT_SUPPORTED as a tested integration; format portability alone is insufficient. |

## Operating systems are a different axis

| Combination | Evidence |
| --- | --- |
| Linux shell + manual selected-folder copy | VERIFIED temporary clean checkout/copy/collision/update/uninstall simulation; not native client loading |
| Linux `sha256sum` and Perl `shasum` recipes | VERIFIED on controlled local checksum fixtures; actual release download must additionally be checked at publication |
| macOS shell manual copy / `shasum` | VERIFIED literal copy/collision recipes in hosted macOS tests; public checksum outcomes in release CI; client runtime still unverified |
| Windows PowerShell copy / Get-FileHash | VERIFIED literal PowerShell copy/collision recipe in hosted Windows tests; Get-FileHash public-download outcome is separately checked by release CI |
| Linux/Python3.11 and3.12; Windows/Python3.12; macOS/Python3.12 tooling | VERIFIED by historical hosted CI linked from the verification record; does not prove client activation or native applications |
| Android/Termux installation | NOT_SUPPORTED as an asserted/tested integration in this release; no universal installation claim |

See [verification](verification.md) for newer actual runs, including optional
installer lifecycle tests, rather than silently upgrading documentation labels.
A client may be available while its authentication, SDK or tools remain blocked.
The native Claude adapter is a source change after v0.4.1, not a retroactive
addition to that ZIP. Standalone `.claude/skills/` copies still use `/name`.
Claude is absent here; its runtime is not classified using Codex's HTTP 401.

## Official sources checked live

- [Codex skills](https://developers.openai.com/codex/skills): exact discovery table,
  `$` invocation, `/skills` selection and optional built-in installer.
- [Plugin packaging/ChatGPT](https://developers.openai.com/plugins/build/plugins):
  root `skills/`, portable manifest and workspace UI publication; administrator
  permission may be required. No local filesystem installation into ChatGPT.
- [Claude Code skills](https://code.claude.com/docs/en/skills): project/personal
  `.claude/skills`, nested discovery and `/skill-name` invocation.
- [Gemini CLI skills](https://geminicli.com/docs/cli/skills/): native `.gemini/skills`
  and `.agents/skills` aliases, listing/reload, local linking and installation.

All four official pages were retrieved successfully on2026-11-09. Their documented
interfaces are not execution evidence. Current source text takes precedence over
old advice if a client changes; preserve local configuration and recheck before
using a vendor-specific adapter.
