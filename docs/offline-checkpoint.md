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
controlled parser errors. Preparation preflights payloads and serialized metadata
before creating output. The exact bounds and failure semantics are in the
[English](client-probe.md) and [Spanish](client-probe.es.md) user guides.

Independent review identified an additional deeply nested JSON failure; the fix
translates it to structured `ERROR`/exit 2 and a real CLI regression covers it.
The previous actual repository fixture still passes `UNCHANGED`, preserving
compatibility with existing generated manifests. The focused suite has 26 tests;
25 passed locally, one native-Windows junction test skipped. Native Windows
and full hosted acceptance must be recorded from this cycle's PR/CI.

Next priority: prepare frozen, matched base/no-skill, released OpenDevGuild and
candidate conditions using existing client/scenario assets. Include success,
failure, hostile third-party instructions, scope preservation and unnecessary
activation, with identical prompts/tools/budgets and no invented model outputs.
Keep actual model runs `BLOCKED_BY_AUTH`; no retry is needed until the environment
changes. Do not turn fixture integrity or a deterministic router into a live
behavior benchmark. No new release is needed for these isolated tool corrections.
