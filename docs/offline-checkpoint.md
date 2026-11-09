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
Native OS and hosted acceptance results must be read from the associated PR/CI;
this local checkpoint does not predict them.

Remaining limitations: no concurrent-writer or OS sandbox guarantee; unsigned
manifests do not authenticate history. Real model activation and reviewer-child
execution remain `BLOCKED_BY_AUTH`; preparing/checking fixtures never upgrades
that status. No new release or token/quality improvement claim.

Next bounded cycle: malformed manifest JSON currently has an uncontrolled error
path, source special entries are silently omitted, and reads lack resource
bounds. Reproduce these offline, add negative tests, then harden parsing and
bounded regular-file inventory without changing the fixture's evidence meaning.
