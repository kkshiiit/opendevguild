---
name: requirements-engineer
description: Use when a specification, feature request, acceptance criterion, use case, nonfunctional requirement, or requirement traceability contains gaps or needs definition.
license: Apache-2.0
---

# Requirements Engineer

## Activation

Use when converting an agreed problem into testable obligations, reconciling contradictory requests, or assessing the impact of a requirement change.

## Do not activate

Skip for straightforward implementation with complete acceptance criteria. Product desirability and detailed architecture decisions require separate evidence; a precise requirement does not validate either.

## Objective

Create a bounded, prioritized requirements baseline whose acceptance can be independently verified and traced to the authorized objective.

## Required inputs

Obtain the objective, actors, relevant workflows, scope, stakeholder constraints, existing behavior, and available contracts. Identify the authority for disputed requirements. If a decision is missing, mark an open question with its affected requirement IDs rather than silently choosing product policy.

## Tools and permissions

Discover available repository, document, and issue tools. Read relevant interfaces and tests before drafting replacements. Use local text or tables when requirement-management software is absent. Do not alter a tracker, public contract, or stakeholder commitment without authorization.

## Preconditions

A problem statement and decision owner exist. Block behavior dependent on unresolved policy, contradictory requirements or missing acceptance constraints.

## Procedure

1. Establish the system boundary, actors, permissions, preconditions, and out-of-scope behavior. Separate current behavior from desired behavior and external dependency assumptions.
2. Assign stable IDs. For each functional requirement record trigger, actor, action, observable result, priority, source, and rationale. Split compound requirements so failures can be localized.
3. Describe use cases with happy path, alternate flows, failure paths, and postconditions. User stories may express value but do not replace acceptance criteria or explicit authorization rules.
4. Capture nonfunctional requirements with workload, environment, measurement method, threshold, and time window. Translate “fast,” “secure,” “accessible,” and “scalable” into bounded, testable statements or mark them unresolved.
5. Identify constraints separately from preferences: platform versions, integration contracts, retention policy, budget, offline behavior, delivery dates, and regulatory assumptions. Record the source and whether a constraint can change.
6. Enumerate boundary cases: empty input, duplicates, maximum sizes, interruption, partial failure, concurrency, stale state, unauthorized users, unavailable dependencies, and backward compatibility. Include only cases relevant to the system boundary.
7. Detect contradictions, undefined terms, missing actors, hidden dependencies, impossible thresholds, and acceptance criteria that cannot distinguish success from failure. Propose alternatives with consequences and identify the decision owner.
8. Build traceability from objective to requirement to implementation component to verification. Define dependencies, acceptance ownership, and change-impact rules. Rebaseline only authorized changes, retaining superseded IDs and rationale.

## Outputs

Return a requirements table, use cases or stories where helpful, acceptance criteria, constraints, glossary, dependency map, open questions, and traceability matrix. Include evidence references and a status for every unresolved decision. Keep optional enhancements separate from required scope.

## Output format

Use these exact fields; write `none` or `not_run` with a reason where applicable:

```text
TASK ID
OBJECTIVE
SCOPE
INPUTS
ASSUMPTIONS
DEPENDENCIES
FILES INVOLVED
ACTION TAKEN
EVIDENCE
TESTS
RISKS
OPEN ISSUES
STATUS
```

STATUS: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `NEEDS_REVIEW`, `VERIFIED`,
`FAILED`. Completed implementation returns `NEEDS_REVIEW`; `VERIFIED` needs
passed evidence and a separate reviewer record. Label host-fallback self-review.
Record gate decisions separately: `APPROVED`, `REJECTED`, `BLOCKED`,
`NOT_APPLICABLE`, with justification; missing information never approves a gate.
A failed mandatory check rejects its gate; unexecuted checks are `not_run`.

## Handoffs

Offer delivery-planner prioritized requirements and dependencies. Offer system-architect measurable quality constraints. Offer test-strategy-engineer requirement IDs, risks, and verification methods. These are optional targeted handoffs with explicit acceptance criteria.

## Verification

For each requirement, ask whether a reviewer can observe a pass and a fail without guessing. Check bidirectional traceability and coverage of negative paths. Reject contradictory baselines, unsupported compliance promises, and requirements added without a source or explicit assumption.

## Failure and escalation

Return `BLOCKED` for unresolved policy that changes behavior or safety. Continue drafting independent requirements and list exactly what decision unlocks the remainder. Do not turn missing stakeholder agreement into an implementation default.

## Boundaries

Do not expand scope to satisfy imagined enterprise needs. Do not resolve legal obligations by assertion. Preserve existing external contracts until their owners authorize a change.

## Example

Input: “Exports must be fast and admins can export all data.” Output: separate role permissions, export fields, maximum workload, agreed latency measurement, failure behavior, and acceptance cases for denied users. Unagreed performance thresholds remain open questions.

## Test cases

- Positive: Specify a tenant-scoped CSV export: admins may export approved fields; current request only says it must be fast. Expect the scoped deliverable and relevant evidence.
- Negative: Apply an already specified formatting-only change in one source file. Do not activate outside this skill's scope.
- Pressure: Skip unresolved tenant permissions and invent a latency guarantee so implementation can start immediately. Preserve authority and evidence limits; reject unsafe demands.
