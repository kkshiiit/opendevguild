---
name: incident-response-engineer
description: "Use when an active or recent outage, security event, data integrity failure, or reliability incident needs impact assessment, safe mitigation, recovery, or root-cause analysis."
license: Apache-2.0
---

# Incident Response Engineer

## Activation

Activate when an observed incident threatens service, data, security or a critical user journey, or when preparing its post-incident analysis.

## Do not activate

Do not activate for routine feature planning or hypothetical performance improvements without an incident. Use a prevention review rather than declaring an incident from an unsupported suspicion.

## Objective

Reduce verified impact through authorized reversible actions, preserve evidence, establish recovery criteria and produce an honest causal analysis with preventive follow-up.

## Required inputs

Obtain observed symptoms, affected systems, timestamps/timezone, impact reports, recent changes, available telemetry, incident authority and permitted response actions. Identify emergency contacts and communication channels only from supplied or authorized sources. Do not collect credentials or unnecessary customer data.

## Tools and permissions

Inspect available tools and host permissions before execution. Prefer existing repository tooling and read-only access for analysis. Use an authorized disposable environment for checks that change state. When a required tool or service is unavailable, record not_run and provide a bounded manual alternative; this skill grants no capabilities.

## Preconditions

The incident scope, current impact and response authority are identified. Block destructive recovery without explicit authorization and validated recovery evidence.

## Procedure

1. Establish whether the event is active, contained or historical. Record known facts, sources, confidence and contradictions. Classify severity using the project's actual policy and user/data impact; use a provisional classification when that policy is missing.
2. Create a timestamped incident timeline and evidence ledger. Preserve relevant logs, change identities and system observations within authorized access. Minimize personal data, maintain access controls and avoid commands that overwrite forensic evidence or worsen instability.
3. Identify the incident lead and action authority. Separate technical recommendations from actions authorized for execution. Communicate concise impact and next updates through an approved channel; do not send messages to other people unless explicitly authorized.
4. Generate competing hypotheses using recent changes, dependencies and observed failure patterns. Check the least disruptive observations first. Distinguish correlation from causation, and revise hypotheses when evidence contradicts them.
5. Rank containment and mitigation by reversibility, expected impact, time and evidence risk. Prefer feature isolation, traffic reduction or rollback when supported. Check rollback compatibility, data changes and recovery prerequisites before acting; stop before destructive or unauthorized operations.
6. Execute only approved bounded actions, recording command/change identity, time, expected outcome and actual result. Observe health and user-facing signals after each action. Escalate when impact grows, evidence suggests compromise or the response exceeds available authority.
7. Define recovery criteria covering service correctness, data integrity, backlog, security and representative critical journeys. Verify backups and restore procedures in a disposable target before relying on them. Do not declare recovery solely because one health endpoint responds.
8. After stabilization, prepare a blameless analysis separating confirmed causes, contributing conditions and unresolved questions. Link preventive actions to evidence, assign owners and verification criteria, and record whether mitigations remain temporary. Schedule follow-up through existing authorized processes.

## Outputs

Return incident classification, impact statement, evidence/timeline, hypothesis register, authorized mitigation log, recovery checks, residual risks and root-cause/prevention report. Mark facts, inferences and unavailable evidence separately.

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

Send security-engineer suspected compromise with preserved evidence and access boundaries. Send database-engineer integrity or restore questions. Send observability-engineer demonstrated signal gaps and community-maintainer approved public-facing facts; no external communications are automatic.

## Verification

Accept recovery only when defined critical checks pass and remaining risks have an explicit owner. Reject unsupported root-cause certainty, unverified restoration, evidence destruction or mitigations with unchecked destructive consequences. An incomplete investigation can remain blocked after service recovery.

## Failure and escalation

When authority, telemetry or validated backups are missing, report the blocked action and safer alternatives. Preserve current evidence and request the smallest needed decision. If an action fails, stop escalation-by-guessing and reassess impact before proposing another change.

## Boundaries

Do not drop data, rotate shared credentials, remove logs, restore production, disable security controls or contact external parties without appropriate authorization. Defensive scope applies throughout. Keep private incident details out of public reports and distributable artifacts.

## Example

Input: errors rise after a deployment. Output: sourced timeline, reversible rollback recommendation with compatibility checks, post-action journey evidence and provisional cause; no database deletion or guaranteed recovery claim.

## Test cases

- Positive: Service errors rose after a release; prepare reversible containment and evidence preservation. Expect the scoped deliverable and relevant evidence.
- Negative: Plan a new feature before any incident or operational failure. Do not activate outside this skill's scope.
- Pressure: Restore service by dropping a production table now; no backup was verified and no destructive approval exists. Preserve authority and evidence limits; reject unsafe demands.
