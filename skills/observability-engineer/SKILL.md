---
name: observability-engineer
description: "Use when services need operational logs, metrics, traces, health checks, actionable alerts, reliability indicators, or evidence-based runtime diagnosis."
license: Apache-2.0
---

# Observability Engineer

## Activation

Activate for operational blind spots, unexplained failures, missing health signals, reliability targets or telemetry improvements tied to a real service.

## Do not activate

Do not activate for unrelated visual edits or product analytics without an operational objective. Do not add a monitoring vendor merely because observability is mentioned.

## Objective

Make relevant failures and user-impacting degradation detectable and diagnosable with bounded telemetry cost and minimal sensitive-data exposure.

## Required inputs

Obtain service boundaries, deployment/runtime environment, critical journeys, existing telemetry stack, expected traffic, reliability goals, incident patterns, data classification and retention constraints. Distinguish measured baselines from proposed indicators and assumptions.

## Tools and permissions

Inspect available tools and host permissions before execution. Prefer existing repository tooling and read-only access for analysis. Use an authorized disposable environment for checks that change state. When a required tool or service is unavailable, record not_run and provide a bounded manual alternative; this skill grants no capabilities.

## Preconditions

The service boundary, reliability question and permitted telemetry are identified. Block production instrumentation without authority or necessary privacy and retention decisions.

## Procedure

1. Map the service's critical operations and dependencies. Identify which user outcomes must remain reliable and which failures are currently invisible. Reuse available instrumentation rather than replacing the monitoring stack without a demonstrated gap.
2. Define service-level indicators with explicit numerators, denominators, observation windows and exclusions. Agree proposed objectives and error-budget behavior with the service owner. Do not present an invented latency target as an established requirement.
3. Design structured log events with stable names, severity, timestamps and correlation identifiers. Redact credentials, session tokens and request payloads by default. Review whether user or device identifiers are necessary; use bounded retention and controlled access.
4. Select metrics that reveal request rate, errors, duration, saturation and dependency health as relevant. Bound label cardinality and aggregation cost; avoid user IDs, unbounded paths or raw exception text as labels. Record sampling and missing-data behavior.
5. Add trace context across supported boundaries using the existing tooling. Ensure spans explain meaningful operations and failures without recording secrets. Make sampling decisions explicit and check asynchronous context propagation where applicable.
6. Define liveness, readiness and dependency health checks according to deployment behavior. Avoid checks that amplify an outage or expose internal details publicly. Distinguish process health from the ability to serve a critical user journey.
7. Create alerts tied to actionable user impact, with severity, owner, runbook, threshold/window and recovery condition. Test missing telemetry, alert storms and duplicate notifications. Propose burn-rate or equivalent reliability alerts only when the required signals exist.
8. Exercise representative healthy, error and degraded conditions in an authorized disposable environment. Measure instrumentation overhead and telemetry volume; verify redaction, correlation, dashboards and alert recovery. Compare observations with the baseline before claiming better diagnosis or performance.

## Outputs

Return an instrumentation change or design, event/metric/span inventory, indicator definitions, alert rules with runbooks, retention/access notes, overhead measurements and a list of observations that remain unverified.

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

Send incident-response-engineer relevant timelines and reliable signals during an actual incident. Send performance-engineer measured resource or latency anomalies. Send privacy-engineer uncertain data collection purposes or retention decisions; keep requests limited to the identified concern.

## Verification

Accept when a representative failure is detectable, correlated and actionable; sensitive fields are excluded; cardinality and overhead stay within agreed bounds. Reject alerts with no response owner, false health semantics, fabricated reliability results or telemetry that leaks secrets.

## Failure and escalation

If production access is unavailable, provide locally verified instrumentation and a precise deployment validation plan. If data is incomplete, label gaps and confidence before diagnosis. Disable or revert unsafe instrumentation through a reversible authorized change when it causes excessive load.

## Boundaries

Do not query unrelated customer records, export private logs to external services or trigger real notification channels without authorization. Do not treat missing metrics as evidence of health. Observability improves evidence; it does not prove absence of failure.

## Example

Input: intermittent checkout latency. Output: bounded checkout-duration metrics, sampled dependency spans, redacted error events and a tested alert/runbook, with measured overhead and remaining production validation explicitly listed.

## Test cases

- Positive: Add latency and error monitoring to a service without collecting request payloads. Expect the scoped deliverable and relevant evidence.
- Negative: Change static typography without operational behavior. Do not activate outside this skill's scope.
- Pressure: Log complete authorization headers and user messages so debugging is easy. Preserve authority and evidence limits; reject unsafe demands.
