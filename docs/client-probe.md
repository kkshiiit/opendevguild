# Offline Codex activation fixture

[Español](client-probe.es.md) · [Agent verification](agent-verification.md)

This is an **offline preparation and integrity tool**, not a model benchmark. It
is useful while the remote Codex CLI is blocked by HTTP 401 authentication.

From the OpenDevGuild repository root, choose a **new** directory:

    python scripts/client_probe.py prepare --output /tmp/odg-smoke-001
    python scripts/client_probe.py check --fixture /tmp/odg-smoke-001

On Windows PowerShell, use a new path such as $env:TEMP\odg-smoke-001.
The destination must not already exist; the tool refuses overwrites.
Source, destination and fixture paths reject symbolic links in every ancestor
and Windows junctions where exposed by the Python runtime. The exact macOS
system aliases `/var` → `/private/var` and `/tmp` → `/private/tmp` are permitted.
Added links, including dangling links, count as fixture changes. These checks
assume a local directory without concurrent writers; they are not an OS sandbox.

The fixture contains two complete Agent Skills (scope-guardian and
code-review-engineer) in .agents/skills, an optional reviewer profile in
.codex/agents, a synthetic Python defect, three prompts in scenarios.json, and
file SHA-256 values in manifest.json. The tool does **not** call models, inspect
credentials, connect to the network or modify global configuration.

## After authentication works

1. Confirm that a harmless real Codex model request works, not only that
   a saved login exists. Check the relevant Codex CLI version and environment.
2. Open a fresh read-only session rooted in the fixture; consult
   codex exec --help for supported flags. The observed CLI accepted
   --ephemeral, --ignore-user-config, --sandbox read-only, --json and -C.
3. Use /skills or the actual skills/list capability and preserve its observed
   discovery entries. File copies alone do not prove client loading.
4. Run A and B from scenarios.json in separate fresh contexts. C is an optional
   negative-activation case. Record exact outputs and actual tool events locally.
5. Run the offline check command again. A change is a finding; unchanged bytes
   do not prove functional correctness.
6. Test reviewer delegation only if the host actually exposes that role.

HTTP 401 means **BLOCKED: authentication**, not a failed skill. If the model
responds but there is no observable skill/tool activation evidence, record its
response separately and keep activation **NOT_VERIFIED**. A model saying it used
a skill is not independent proof.

Review any client logs for secrets before sharing or publishing. The manifest
is not signed and may be forged; this tool verifies byte-level consistency only.
A fixture is not a production app. Codex Desktop and remote CLI can have
different authentication and runtime configurations. No claims of improved
behavior, tokens or agent quality result from preparing the fixture.
