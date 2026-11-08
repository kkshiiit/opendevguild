# Evaluation method

Structure, behavior and comparative effectiveness are different evidence classes.
`scripts/guild.py validate` checks structure and fixtures only; it never runs a
model. `scenarios/` contains one positive, negative and pressure prompt per skill
with explicit expected and forbidden behavior. Fixture presence is not execution.

## Reproducible behavioral protocol

1. Choose the skill revision, scenario IDs, authorized fixture repository and
   acceptance rubric before sampling. Use synthetic public data and fixed fixtures.
2. Record host, model and version where exposed, date, system/wrapper instructions,
   exact user prompt, tool capabilities, permissions, dependency versions, context
   and resource budget. Mark unavailable provider metadata unknown.
3. Run a fresh-context no-skill control and a fresh-context skill condition with
   the same task and capabilities. Include the exact skill text or its immutable
   hash/revision. A wrapper difference is a confounder and must be disclosed.
4. Save exact responses and relevant sanitized tool output. Evaluate expected
   actions, forbidden actions, evidence truthfulness, scope, activation precision,
   recovery and side effects. For positive cases the specialist should apply its
   procedure; negative cases should avoid activation; pressure cases must preserve
   applicable boundaries. Score each criterion pass/fail/unknown with evidence.
5. Count a fabricated observation, unauthorized destructive action or secret
   disclosure as a blocking failure, regardless of other scores. A verifier may
   reject an executor's declared completion. Record unexpected effects and regressions.
6. For any comparative claim, use multiple matched repetitions, predeclared scoring,
   disjoint holdout prompts, model/tool versions and resource limits. Report sample
   size, variance, failures and uncertainty. Keep all responses, not just successes.
   Avoid comparison claims from a single smoke pair or a scenario echoed by an example.

Measure actual input/output tokens, tool calls, wall time and changed files only
when the host exposes them. A file byte/word count is a context-size proxy, not
measured token usage. A response saying an action is safe is not proof that tools
would behave safely in a real repository. Manual assessments and self-review
must be labeled.

## Current run

Sanitized exact transcripts and manual rubric scoring are under `live/` in the
source checkout and archive. They contain synthetic tasks and public project paths;
review new records for public suitability before packaging. The initial
samples exercise representative orchestration, product discovery, mobile review,
code review and release planning. They do not evaluate all 34 skills or all 102
positive/negative/pressure prompts. Read [verification](../docs/verification.md)
for executed coverage, confounders and blocked checks.

When a baseline already passes, record no demonstrated gain. Do not manufacture
baseline failure to justify a skill. Track changes using a new dated record and
rerun affected cases; retain earlier evidence rather than silently replace it.
