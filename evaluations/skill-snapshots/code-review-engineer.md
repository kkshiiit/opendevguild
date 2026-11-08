---
name: code-review-engineer
description: Use when a code change, pull request, or patch needs a justified review for correctness, concurrency, security, performance, tests, or scope.
license: Apache-2.0
---

# code-review-engineer

## Activation

A patch or branch needs an independent acceptance decision, or an existing implementation needs a focused defect review. Activate for review requests with identifiable code and expected behavior.

## Do not activate

Do not use as the primary implementation procedure, a general style rewrite, or a substitute for missing product requirements. A review request does not authorize unrelated fixes.

## Objective

Produce a small set of defensible findings and an explicit acceptance recommendation supported by code, reproducible observations, and stated verification limits.

## Required inputs

Obtain the change or base/head comparison, authorized scope, acceptance criteria, affected runtime assumptions, and available test results. If only a snippet exists, review that snippet and label repository-wide conclusions unavailable. Preserve pre-existing changes.

## Tools and permissions

Discover actual read, search, diff and test tools. Inspect Git status and targeted file ranges before reading whole modules. Run local checks only when their effects and dependencies are understood. Without execution, perform static review and mark tests not_run; do not invent a platform review API.

## Procedure

1. Establish the intended behavior and changed surface. Trace callers, contracts, data flow and failure paths far enough to understand observable consequences. Compare against the authorized scope, separating required fixes from optional cleanup.
2. Check logical correctness, boundary values, state transitions, error handling and resource ownership. For concurrent or asynchronous code, examine interleavings, retries, cancellation, transactions and idempotency. Do not assume an unseen lock or transaction exists.
3. Inspect authentication, authorization, untrusted inputs, secret handling and data exposure at touched trust boundaries. Investigate performance only where the change introduces a plausible bottleneck; distinguish measurements from complexity arguments.
4. Assess test coverage against changed risks: success, negative cases, regression, compatibility and failure recovery. A reported green suite is evidence only when its command, environment, revision and result are available.
5. For every candidate finding, construct a trigger and observable impact. Check nearby safeguards and existing conventions. Remove speculative or purely preferential findings; retain uncertainty explicitly when missing context prevents confirmation.
6. Rank confirmed findings: critical for immediately exploitable or catastrophic impact; high for major correctness, security or data-loss risk; medium for material bounded defects; low for minor actionable issues. Include file and line when available, otherwise identify the supplied function or statement without fabricated line numbers.
7. Return accepted only when criteria are supported and no blocking failures remain. Return rejected for demonstrated blockers, or blocked when necessary context or checks are missing. Independently inspect an implementer’s claimed fix before changing the verdict.

## Outputs

Return verdict, scope reviewed, findings ordered by severity, and verification status. Each finding contains location, evidence, triggering condition, consequence and a concrete recommendation. State residual risks, commands actually run, and checks not run; an empty findings list is not proof of exhaustive correctness.

## Handoffs

Offer implementation-engineer a bounded fix with reproduction and acceptance checks, or security-engineer a suspected trust-boundary issue with authorized scope. Supply evidence and dependencies; do not trigger either automatically. Identify self-review when independence is unavailable.

## Verification

A reviewer must be able to reproduce the reasoning from cited code or recorded output. Reject unsupported severity, invented locations, hidden assumptions, unexplained out-of-scope edits and acceptance despite unresolved blocking failures.

## Failure and escalation

If the patch, expected behavior or execution environment is missing, report the exact gap and a focused next check. Escalate contradictory requirements to the owner; deadline pressure does not change the evidence.

## Boundaries

Review only authorized code and environments. Do not expose secrets in findings, run intrusive production checks, rewrite working modules for preference, or weaken tests to obtain approval.

## Example

Input: checkout charges an external gateway, then writes an order; timeout retries have no visible idempotency key. Output: high-severity duplicate-charge and payment/order consistency findings tied to those statements; rejected pending retry and write-failure evidence; unrelated invoice redesign deferred.
