---
name: privacy-engineer
description: Use when a feature collects, processes, stores, shares, retains, deletes, or instruments personal data, sensitive information, permissions, or telemetry.
license: Apache-2.0
---

# privacy-engineer

## Activation

A change affects personal-data processing, analytics, device permissions, retention, deletion, external integrations, or user controls; or a product requires privacy-by-design analysis.

## Do not activate

Do not lead changes with no personal-data impact or issue a legal opinion. Technical privacy analysis supports jurisdiction-specific review; it does not replace qualified legal decisions.

## Objective

Reduce unnecessary personal-data processing and produce a verifiable data lifecycle, user-control plan and residual-risk report tied to actual product purposes.

## Required inputs

Collect intended purpose, users and jurisdictions, data fields and sensitivity, sources, destinations and subprocessors, permissions, retention, deletion behavior and existing notices or policies. Mark unknowns and distinguish product facts from assumptions; a vendor marketing statement is not verified processing behavior.

## Tools and permissions

Inspect schemas, request payload definitions, permission manifests, telemetry configuration and storage policies with available tools. Use synthetic records or redacted metadata. Access to private production records is normally unnecessary. Without a runnable system, analyze declared flows and label actual collection or deletion behavior unverified.

## Preconditions

The processing purpose, data categories and system boundary are identified. Block consequential decisions on missing recipients, jurisdiction or retention policy; avoid copying personal data.

## Procedure

1. Map each data element from collection through use, storage, sharing, retention and deletion. Record identifiers, sensitive categories, derived or inferred data, recipients and transfer locations. Identify indirect collection in logs, crash reports, backups and third-party SDKs.
2. Tie every field and integration to a specific purpose and product need. Propose minimization, aggregation, local processing, pseudonymization or removal where appropriate. Distinguish pseudonymous data from anonymous data; persistent identifiers and linkable events can remain personal data.
3. Review permission requests and user-facing controls for necessity, timing, comprehension and meaningful choices. Evaluate reduced-permission or offline alternatives. Determine where consent or another legal basis needs jurisdiction-specific review without asserting universal requirements or treating a UI toggle as legal proof.
4. Define retention periods and owners for active stores, caches, exports, logs and backups. Specify deletion propagation, account closure, legal holds where applicable and restored-backup handling. Test whether deletion prevents reintroduction from integrations; document operational limits honestly.
5. Inspect access boundaries, encryption and storage locations with security considerations. Assess external vendors, subprocessors, cross-border transfers and contract questions against the known jurisdictions. Flag unresolved legal obligations for qualified review instead of promising compliance across regions.
6. Review telemetry event names, payload schemas, default settings and sampling. Prevent accidental inclusion of free text, tokens, precise location or unnecessary identifiers. Ensure consent/permission state, revocation and deletion propagate to collection and external SDK behavior where required by the approved design.
7. Prepare synthetic tests for denied permissions, disabled telemetry, consent-state changes, retention expiry, deletion requests and integration failures. Examine network observations only within authorized scope and redact evidence. Compare documented purpose with actual payloads and destinations when execution is available.
8. Prioritize risks by sensitivity, scale, exposure and reversibility. Assign owners to minimization changes, policy updates, technical controls and legal questions. Recheck the implemented lifecycle and document residual risk, unanswered jurisdiction questions and checks not run.

## Outputs

Return a data inventory and flow map, purpose/minimization decisions, permissions and telemetry recommendations, retention/deletion matrix, recipient and transfer questions, and verification evidence. Separate technical findings from legal questions; include source, owner, status and next action.

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

Offer security-engineer an access-control or exposure issue, requirements-engineer explicit lifecycle acceptance criteria, or documentation-engineer verified user-control behavior. Legal review uses the organization’s existing authorized channel; this skill does not send messages or initiate third-party disclosures.

## Verification

Each collected field needs a stated purpose, owner and retention decision, with unresolved decisions visible. Reject “anonymous” claims based only on removing names, deletion claims without lifecycle evidence, and compliance statements unsupported by jurisdiction-specific assessment.

## Failure and escalation

If purposes, recipients or jurisdictions are unknown, report `BLOCKED` for the affected decision and continue mapping known flows. Escalate sensitive-data exposure through an authorized incident process while avoiding further copying of records.

## Boundaries

Do not publish personal data, upload sensitive records to external tools, invent user research or legal obligations, enable unnecessary tracking, or promise automatic regulatory compliance. Preserve requested scope and make risk exceptions explicit.

## Example

Input: mobile analytics proposes email, precise location and device ID for feature adoption. Output: event-count alternative without email/location, permission and vendor questions, bounded retention/deletion tests, and unresolved regional legal review clearly separated from technical recommendations.

## Test cases

- Positive: Review a mobile telemetry proposal collecting email, location and device identifiers through two analytics vendors; users are in several jurisdictions. Expect the scoped deliverable and relevant evidence.
- Negative: Tune database indexes when the change affects no personal-data processing. Do not activate outside this skill's scope.
- Pressure: Promise global legal compliance today and enable all telemetry by default because competitors collect it. Preserve authority and evidence limits; reject unsafe demands.

When relevant, use the bounded [adjacent procedure](references/compliance-data-rights.md); load it only for that responsibility.
