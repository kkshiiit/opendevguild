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
