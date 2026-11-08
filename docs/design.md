# OpenDevGuild design

Implementation baseline: 2026-11-08, reconciled with the complete master brief
through section 21. The project keeps one canonical skill catalog and small,
inspectable tooling rather than introducing another agent runtime.

## Goal and boundaries

Deliver 34 original, independently installable Agent Skills under Apache-2.0,
selective orchestration, compatible optional subagent profiles, explicit exchange
contracts, six quality gates and reproducible evaluation assets. Serve individual
developers through professional teams without forcing a stack or simulating
corporate titles. Execution, credentials, sandboxing and scheduling belong to the
host. No automatic compliance, production access or comparative superiority is
implied by a procedure or a successful structural check.

## Four layers

| Layer | Responsibility | Implementation |
| --- | --- | --- |
| A: orchestration | Classify, scope, select, sequence, budget and consolidate | mission-control, routing procedure and task contracts |
| B: specialists | Perform concrete bounded domain work | One canonical skills/<identifier>/SKILL.md per specialty |
| C: execution | Use real tools, isolation boundaries and available workers | Compatible host; eight optional .codex/agents profiles |
| D: verification | Assess evidence and approve, reject or block gates | Independent review where possible, official validator, policy tests and scenario rubric |

A skill is a discoverable procedure; an agent is an execution context. Loading
one does not spawn the other. Parallel execution requires available host support,
satisfied dependencies and disjoint write ownership. A serial fallback preserves
the same acceptance criteria and labels self-review when independence is absent.

## Repository decisions

Keep canonical skill sources under `skills/`; selectively copy them to the host's
repository or personal discovery location. This avoids maintaining duplicate
catalogs under `.agents/skills/`. Keep concise common contracts in documentation
and independently usable instructions in every skill. References, scripts and
assets are added only when they support a real repeated task. Do not create empty
sector directories or repetitive scaffold files to mimic a large framework.

The optional JSON exchange and routing formats are OpenDevGuild conventions,
not Codex APIs. Python tooling performs deterministic checks and packaging; the
official `skills-ref` validates the Agent Skills format. Existing host tools do
implementation work. A portable root plugin manifest prepares distribution
without claiming client installation, public listing or GitHub publication.

## Collaboration and verification

The task lifecycle uses `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `NEEDS_REVIEW`,
`VERIFIED`, `FAILED`. Completion moves work to review; appropriate inspectable
evidence and an independent reviewer support VERIFIED. Self-review leaves work
NEEDS_REVIEW. The exchange records task ID, objective, scope,
inputs, assumptions, dependencies, files involved, action taken, evidence, tests,
risks, open issues and status. Review findings retain severity, location,
evidence and recommendation; known blockers cannot disappear into a summary.

Quality gates cover Requirements, Architecture, Implementation, Verification,
Security and Release. Each decision is `APPROVED`, `REJECTED`, `BLOCKED` or
`NOT_APPLICABLE` with a reason. Tool results and inspection judgments remain
distinct. An unavailable required environment blocks its claim; absence of
information never approves a gate. A trivial edit may justify non-applicable
gates without requiring a human approval meeting.

## Resource policy

FAST favors a small sequential task and direct verification. STANDARD selects
only relevant specialists and review. CRITICAL adds controls justified by actual
security, data, compatibility or operational risk. Mode never grants permissions.
Reuse current repository analysis, perform targeted searches and load references
on demand. Give workers bounded excerpts and evidence pointers. Stop when
required evidence is sufficient; repeat expensive checks only after relevant
changes or failures. Token savings require measured usage, not file-size claims.

## Delivery and acceptance

Proceed through inspection, core, specialists, optional subagents, quality,
integration, documentation and publication. Before catalog-wide acceptance,
verify the eight core procedures: mission-control, scope-guardian,
repository-intelligence, delivery-planner, requirements-engineer,
system-architect, code-review-engineer and skill-quality-evaluator. Existing
work predating receipt of the complete brief is reconciled through explicit
checks rather than retroactively claiming a phase order that was not observed.

Release acceptance requires valid metadata, working relative resources, complete
contracts, evaluated selection, meaningful functional/security/regression assets,
verified or explicitly limited host integration, usable examples, bilingual user
guides, licensing and honest evidence. Current results and open gates live in the
[verification record](verification.md), not in this design. See
[requirements](requirements.md), [standards](engineering-standards.md) and
[release procedure](releasing.md).
