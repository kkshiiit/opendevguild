# Installation

[Español](installation.es.md) · [Quick usage](quickstart.md) ·
[Troubleshooting](troubleshooting.md) · [Compatibility evidence](client-compatibility.md)

## Requirements and scope

You need a compatible AI client, a target project and a file manager. Git is
optional. **Python, uv, browser binaries and development dependencies are not
required just to read/use the skill procedures.** Individual app tasks may need
SDKs or tools; the skill must discover and report those separately.

Skills supply procedures. They do not install a model, grant tools/permissions,
start subagents or guarantee correctness. Choose one or two responsibilities
from the [catalog](catalog.md), not the entire catalog.

## 1. Obtain a reviewed source

Without Git, use the repository's **Code → Download ZIP**, then extract it.
That download is a source snapshot, not the separately checksummed release bundle.
For a versioned bundle use [release0.4.0](https://github.com/kkshiiit/opendevguild/releases/tag/v0.4.0)
and download **both** `opendevguild-0.4.0.zip` and its `.zip.sha256` sidecar.
The release page and assets must exist before treating this version as published.
The sidecar detects changed bytes, not publisher identity.

With Git (command executed successfully against the public repository during
onboarding verification):

```text
git clone https://github.com/kkshiiit/opendevguild.git
cd opendevguild
```

`main` may advance. Record the selected commit with `git rev-parse HEAD`; for a
release use its published tag only after confirming it exists. Do not check out
a different revision over uncommitted work. Review the chosen `SKILL.md` first.

### Check the release download

Keep both downloaded files in the same folder. Linux:

```bash
sha256sum -c opendevguild-0.4.0.zip.sha256
```

macOS's standard Perl utility:

```bash
shasum -a 256 -c opendevguild-0.4.0.zip.sha256
```

Windows PowerShell:

```powershell
$expected = (Get-Content .\opendevguild-0.4.0.zip.sha256).Split()[0].ToLowerInvariant()
$actual = (Get-FileHash .\opendevguild-0.4.0.zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw 'SHA-256 mismatch: do not install' }
'SHA-256 matches'
```

Checksum recipes use the native utilities for each platform. The release-event
CI downloads the actual public ZIP and sidecar on Linux, macOS and Windows and
records available native utility results. Consult the final release report for
the observed run; copying alone never proves integrity. Stop on a mismatch.

## 2. Install one skill into a project

For current documented Codex discovery the final path is:

```text
your-app/.agents/skills/scope-guardian/SKILL.md
```

Copy the **folder**, not just `SKILL.md`, so optional assets/references remain
available. Refuse existing destinations, including symbolic links. Do not copy
this library's `AGENTS.md`; it governs contributions to this library.

File-manager path: in your application create `.agents`, then `skills`; copy the
reviewed `scope-guardian` folder there. Enable hidden-file display if needed.
This needs no Python and changes only your application's selected skill folder.

POSIX shell (Linux/macOS), from the OpenDevGuild download/checkout:

```bash
odg_target="/absolute/path/to/your-app/.agents/skills"
mkdir -p "$odg_target"
if [ -e "$odg_target/scope-guardian" ] || [ -L "$odg_target/scope-guardian" ]; then
  printf '%s\n' 'STOP: destination exists; preserve it and review the update guide.'
else
  cp -R skills/scope-guardian "$odg_target/scope-guardian"
fi
test -f "$odg_target/scope-guardian/SKILL.md"
```

Replace the absolute path. Literal copy/collision examples are exercised in
clean temporary Linux and macOS projects by hosted tests; client discovery is
separate and remains subject to the compatibility matrix.

PowerShell (literal Windows copy/collision example tested in hosted CI):

```powershell
$odgTarget = 'C:\path\to\your-app\.agents\skills'
New-Item -ItemType Directory -Force -Path $odgTarget | Out-Null
$odgDestination = Join-Path $odgTarget 'scope-guardian'
if ($null -ne (Get-Item -LiteralPath $odgDestination -Force -ErrorAction SilentlyContinue)) { throw 'STOP: destination exists' }
Copy-Item -LiteralPath '.\skills\scope-guardian' -Destination $odgDestination -Recurse
Test-Path -LiteralPath (Join-Path $odgDestination 'SKILL.md')
```

A `True` file check establishes copying, not client discovery. Test commands in
an empty destination first. The optional [managed installer](installer-reference.md)
adds dry-run, state tracking, collision checks and rollback; it requires Python
and runs only when explicitly invoked. Manual use remains the default.

## 3. Verify discovery and bounded use

Open **your app**, not the OpenDevGuild source checkout, in the client. In Codex
CLI/IDE use `/skills` where supported and inspect the listed skill and source
path. Begin a fresh session if changes are not detected. Invoke:

```text
$scope-guardian Define the scope for fixing the login error. Do not edit files.
Return affected paths, exclusions, acceptance checks and missing information.
```

Supply the actual error and relevant application paths. Expected: a bounded scope
brief with assumptions/unknowns, no unrelated edits. Check the client selected
that installed skill. A model name-dropping a skill is insufficient proof. Native
client loading in the authoring environment remained blocked by expired Codex
CLI authentication; the tested filesystem recipe must not be called a successful
runtime activation. See [matrix](client-compatibility.md).

## 4. Personal use and other clients

Project installation is the default. Personal installation affects multiple
projects and must be your explicit choice. Paths below are documented, not proof
that all clients/platforms were tested:

| Client | Project | Personal, explicit choice | Explicit invocation |
| --- | --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/`; Windows `$env:USERPROFILE\.agents\skills` | `$scope-guardian`; `/skills` selection where available |
| Claude Code | `.claude/skills/` | `~/.claude/skills/`; Windows `$env:USERPROFILE\.claude\skills` | `/scope-guardian` |
| Gemini CLI | `.gemini/skills/` or documented `.agents/skills/` alias | `~/.gemini/skills/` or documented `~/.agents/skills/` alias | `/skills list`, then natural-language task; `/skills reload` after changes |

For Codex the optional built-in `$skill-installer` may accept a reviewed repository
URL, revision and selected paths. Use it only if actually exposed; do not assume
availability or silently install its whole catalog. Gemini documents its own
`gemini skills install <source>` interface; verify scope/consent in that version
before using it. Manual copying avoids uncertain installer defaults.

ChatGPT does **not** discover your computer's `.agents/skills` folder. Use a
currently admitted plugin/workspace mechanism; an administrator may need to
upload/publish a compatible bundle through the Plugins interface. A public GitHub
release is not automatic ChatGPT installation or public plugin-directory approval.
See the [official packaging guide](https://developers.openai.com/plugins/build/plugins).
Android/Termux has no verified installation path in this release; do not infer
support from Linux similarities. Other hosts need their own documented discovery.

## 5. Update, uninstall and rollback safely

1. Obtain/review a newer source separately. Identify the exact installed folders
   and any local edits. Never overwrite an unknown folder, symlink or skill.
2. Compare the installed version with its known original and the proposed update.
   If locally edited or ownership is uncertain, stop for review; preserve both.
3. Move the selected installed folder to a named backup **outside discovery**.
   Keep local edits with it. Copy the new reviewed folder only after the old
   destination is absent. Do not move unrelated skills or application files.
4. Verify discovery and a bounded task. To roll back, preserve the new folder
   outside discovery, then restore the backup to its original location.
5. To uninstall, move only the installed OpenDevGuild folders outside discovery;
   keep backups until you decide to remove them. Remove optional copied agent
   profiles separately. No global configuration edit or destructive Git reset
   is part of these steps.

Manual update/uninstall/rollback was simulated with a synthetic local edit and
retained it. This is file lifecycle evidence, not native-client proof. The optional
installer refuses conflicting edits and supplies a managed rollback path; follow
its [reference](installer-reference.md), including dry-run before changes.

## Optional subagents

The eight `.codex/agents/*.toml` files are separate Codex-specific role guidance.
Review and copy only selected profiles into your app's compatible `.codex/agents/`
if you want them, refusing collisions. They inherit host restrictions; they do
not create tools, isolation or permanent agents. Other clients do not gain Codex
subagents from these files. Installing one skill never requires installing profiles.

[Quick usage](quickstart.md) · [Examples](usage-examples.md) · [Troubleshooting](troubleshooting.md)
