# Offline development checkpoint — 2026-11-09

Baseline: `44d1450c7a1ff357c45712317a995bc064be2adf`, including merged
PRs #3 and #4. Preserve their test planner and client fixture. Release `v0.4.0`
is immutable and unchanged. No login retries or credential inspection occurred.

## Cycle 1: fixture filesystem boundaries

Reproduced before editing: an added dangling link produced `UNCHANGED`; a link
in an output ancestor allowed preparation outside the apparent destination.
Four new negative tests initially failed, then passed after the correction.
Source, output and fixture ancestors now reject symbolic links and exposed
Windows junctions; the two exact macOS temporary-directory aliases are allowed.
Added dangling links are reported as `CHANGED`. User guides were updated EN/ES.

Local evidence: 11 targeted tests passed; the full suite ran 134 tests, with
133 passed and one skipped because local PowerShell is unavailable. Official
format/project validation, visual metadata validation, fatal-error lint and
diff whitespace checks passed. Independent focused review found no blocker.
Merged as [PR #5](https://github.com/kkshiiit/opendevguild/pull/5), main commit
`9c9c051ac94bd2fa2f61540bb3a5f684da0d75e8`. All five hosted validation/Chromium
jobs passed on the [PR](https://github.com/kkshiiit/opendevguild/actions/runs/42560497079)
and [merged main](https://github.com/kkshiiit/opendevguild/actions/runs/42560608854).

Remaining limitations: no concurrent-writer or OS sandbox guarantee; unsigned
manifests do not authenticate history. Real model activation and reviewer-child
execution remain `BLOCKED_BY_AUTH`; preparing/checking fixtures never upgrades
that status. No new release or token/quality improvement claim.

## Cycle 2: bounded regular-file inventory and manifest errors

Reproduced malformed top-level JSON causing an uncontrolled `AttributeError` and
source FIFOs silently omitted from the copied inventory. Added byte/file/entry
budgets, regular-file checks, no-follow traversal, duplicate-key detection and
controlled parser errors. Relative paths are limited to 32 components and
4,096 UTF-8 bytes before constructing ancestor checks. Preparation preflights payloads and serialized metadata
before creating output. The exact bounds and failure semantics are in the
[English](client-probe.md) and [Spanish](client-probe.es.md) user guides.

Independent review identified an additional deeply nested JSON failure; the fix
translates it to structured `ERROR`/exit 2 and a real CLI regression covers it.
The previous actual repository fixture still passes `UNCHANGED`, preserving
compatibility with existing generated manifests. The focused suite has 28 tests;
27 passed locally, one native-Windows junction test skipped. Native Windows
and full hosted acceptance passed in
[PR #6 CI](https://github.com/kkshiiit/opendevguild/actions/runs/42561177866).
Merged main is `7f44d17b8a6fce07e1ffa60d0cd3c7b50f4838d6`;
[main CI](https://github.com/kkshiiit/opendevguild/actions/runs/42561379809)
also passed all five validation/Chromium jobs. Local full suite: 151 tests,
149 passed, two skipped (PowerShell and native Windows). Native job success
does not imply every optional check ran; retain each tool's skip conditions.

## Cycle 3: scope authority and matched comparison inputs

`scope-guardian` now requires approval provenance and rejects third-party claims
of owner authorization without discarding applicable host-recognized instructions.
Its scenario expectations include this boundary. Existing positive, negative,
input/output and rejection criteria remain; no new skill or permanent agent.

Prepared [five matched cases](client-comparison.md) for no-skill, immutable
0.4.0 instruction snapshots and candidate conditions. Prompts, app bytes, budgets,
tool policy and rubric are shared. The arithmetic fixture reuses `client_probe`.
Hash tests and isolated materialization check the inputs; **no model runs occurred**.
The public cases are development fixtures, not hidden holdouts. Runtime identity
and candidate commit remain unset until a real run can freeze them. Outcomes stay
`NOT_RUN` / `BLOCKED_BY_AUTH`; proposed instruction benefit is not demonstrated.
Local validation: 156 tests, 154 passed and two skipped (local PowerShell and
native Windows junction); all five comparison-input tests passed. Official
format/project and visual metadata checks, fatal Python lint and conservative
public-source audit passed. Independent review confirmed the released snapshot
bytes and no blocker; its contamination-control recommendation is in the
operator protocol. Branch: `feat/scope-authority-comparison-cases`; consult its
PR/main workflow evidence for hosted acceptance and the final merge commit.

Next: when client authentication changes, freeze runtime/candidate identities,
execute the same cases in fresh contexts with actual read/tool/side-effect logs,
and obtain independent grading. While blocked, audit another concrete high-impact
procedure boundary against the existing contract; do not expand the catalog or
retry login. The roadmap, frozen snapshots and historic results remain preserved.
No new release is needed for these isolated changes.

## Cycle 4: installer transaction safety

Baseline: `a2e6de30408eff183430197784dbb732a7a9fe29`; remote main matched
before changes. Branch: `fix/transactional-skill-installer`. Scope is the optional
installer, its tests and necessary EN/ES documentation. Skills, profiles,
dependencies and immutable release `v0.4.0` are unchanged.

Six new regressions failed on the old implementation before it was modified:
partial replacement copy, second-skill copy failure and manifest publication
failure for install/update/uninstall/rollback. They demonstrated altered/missing
installed bytes alongside the old manifest. All are now passing.

The whole batch is staged and hash checked; the next manifest is prepared before
originals move into retained backups. Publication is the commit point. Pre-commit
errors compensate the batch with renames and preserve exact old manifest bytes.
Failed compensation preserves originals and a delete-last pending marker that
blocks new operations. `recover` validates the entire recorded batch before
moving anything and resumes compensation or committed cleanup as appropriate.
See [English/Spanish recovery](installer-reference.md#transaction-failures-and-recovery).

Local evidence: 39 installer methods passed, including four-action multi-skill
publication faults, partial copy/write, promotion/retirement/restoration failures,
restoration retry, partial cleanup, tampered journals/backups, user edits, budgets,
first-install retry and a synthetic Python interruption. Full local suite:
179 methods, 177 passed, two platform skips (PowerShell and native Windows
junction). Official format/project and visual validation, fatal Python lint
and whitespace checks passed. Independent inspection/focused review found no
scoped blocker. Hosted native CI and final integration must be observed in the
associated PR/main workflow; local checks do not predict those results.

Hosted evidence: [PR #8](https://github.com/kkshiiit/opendevguild/pull/8)
at implementation commit `a5fc04f53217558fb031f085d2026c4c79b3948f` passed
[all five CI jobs](https://github.com/kkshiiit/opendevguild/actions/runs/42586466111):
Linux/Python 3.11 and 3.12, Windows/Python 3.12, macOS/Python 3.12 and Chromium.
Release integrity is intentionally skipped because no release is published.
The PR records final integration and merged-main workflow evidence; the extra
checkpoint-only commit does not alter the tested installer implementation.

Limits: pending state invalidates ordinary manifest loading; visible directory
swaps are not isolated. No power-loss/fsync, arbitrary filesystem, hostile-race
or concurrent-writer guarantee. Journals are bounded but unsigned; damaged state
or persistent restoration errors can require reviewed manual recovery. The tests
do not establish real power-cut durability. Empty generated parents may remain.
Rollback consumes history rather than providing redo; documentation now agrees.

Next: confirm final PR and merged-main native CI, then keep the recovery protocol
and retained fault cases as the checkpoint. Any later offline defect should be
reproduced and scoped separately. CLI authentication and model/subagent behavior
remain `BLOCKED_BY_AUTH`; no login retry or activation benchmark was attempted.
