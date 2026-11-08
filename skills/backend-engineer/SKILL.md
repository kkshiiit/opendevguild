---
name: backend-engineer
description: Use when implementing or repairing services, business rules, persistence, authenticated APIs, asynchronous jobs, data ingestion or transformation pipelines, cache behavior, concurrency handling, or server integrations in an existing backend.
license: Apache-2.0
---

# Backend Engineer

## Activation

Activate for a scoped service feature or defect involving server behavior, business
rules, data access, jobs, ingestion/transformation pipelines or integration boundaries.

## Do not activate

Do not take ownership of visual-only work, speculative platform replacement or
destructive production maintenance. Broad architecture and schema decisions may
need their own bounded review before implementation.

## Objective

Implement correct, authorized server behavior that preserves explicit contracts,
handles failure predictably and can be verified with reproducible tests.

## Required inputs

Identify the entry point, request/event contract, business invariants, identity
model, persistence boundaries and deployment environment. Obtain authorized paths
and acceptance criteria. Inspect existing configuration and tests without reading
secret values. Record missing policy decisions instead of inventing them.
For pipelines, identify source/target schemas, batch or stream mode, freshness,
quality thresholds, lineage, retention and the authorized backfill boundary.

## Tools and permissions

Discover the repository's runtime, package manager, test scripts and local service
fixtures. Use isolated test databases and synthetic credentials. Confirm environment
targets before commands that can write data, send messages or call paid services.
Missing infrastructure means an explicit verification limit, not a production probe.

## Preconditions

The service boundary, identity model and business invariants are known. Block state-changing work without authorized fixtures, environment targets or essential policy inputs.

## Procedure

1. Reproduce the relevant request or event using the smallest available fixture.
   Trace validation, authentication, authorization, business rules and persistence.
   Check framework/runtime conventions before selecting an implementation.
2. Write down invariants: who may perform the action, which state transitions are
   valid, what must be atomic and what response or event consumers expect. Validate
   input types, sizes and business semantics at the appropriate boundary.
3. Implement authorization against the resource and tenant, not only a logged-in
   flag. Preserve existing authentication mechanisms and production-safe defaults.
   Use parameterized database operations and established cryptographic libraries.
4. Define transaction and concurrency boundaries. For retried work, persist an
   idempotency decision atomically with its business effect where possible. Handle
   duplicate delivery, racing updates, deadlocks and partial external failure with
   explicit outcomes; do not promise exactly-once delivery without its assumptions.
5. For asynchronous jobs and integrations, set timeouts, bounded retries, backoff
   and cancellation behavior. Validate webhook authenticity where relevant. Keep
   external calls outside locks when feasible, and account for reconciliation when
   a remote effect succeeds before local acknowledgement.
6. Add caching only for a demonstrated need. Specify key identity, authorization
   scope, invalidation, expiry and stale behavior. A cache must not leak data across
   users or become the sole source of a critical business invariant.
7. For data pipelines, define source-to-target transformations and schema evolution.
   Preserve lineage and reproducible quality checks. Handle late, duplicate and
   corrupt records explicitly; quarantine safely without leaking sensitive payloads.
   Design bounded backpressure, durable checkpoints and idempotent replay. Test
   restart after partial writes, out-of-order events and schema mismatch using
   synthetic fixtures. Limit backfills to authorized ranges; measure lag, throughput
   and rejected records before choosing batch or streaming infrastructure.
8. Return stable error contracts and sanitized diagnostics with correlation IDs.
   Exercise success, rejection, dependency failure and concurrent/retry cases using
   existing tests. Run relevant build/static checks and inspect the final diff.

## Outputs

Return changed paths, business invariants, contract or configuration changes, test
commands/outcomes and unresolved operational risks. Distinguish actual integration
execution from fixtures and mocks. Mark unavailable checks `not_run`.

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

Provide API reviewers concrete request/response examples for contract changes,
database reviewers migration and query concerns, or security reviewers the affected
trust boundary. Keep these optional and limited to evidence requiring their review.

## Verification

Accept when applicable invariants, authorization and error cases pass relevant
tests, contracts remain compatible and no blocking finding remains. Reject missing
resource checks, duplicated financial effects, swallowed failures or unsafe defaults.
A passing unit test does not establish production readiness.

## Failure and escalation

Return `BLOCKED` when business policy or infrastructure prevents meaningful
verification. Preserve failed check evidence and request the narrow missing input.
For incompatible changes, document impact and migration choices before widening scope.

## Boundaries

Do not expose credentials, use development authentication in production, disable
controls to make a test pass or execute destructive migrations without authorization.
Respect existing service boundaries and avoid unrelated rewrites.

## Example

Input: “Payment webhooks double-charge during concurrent retries.” Deliver an
authenticated event path, atomic deduplication design, concurrent retry tests and
documented reconciliation for remote/local partial failure.

## Test cases

- Positive: Repair an existing daily order-ingestion pipeline that duplicates rows after restart and accepts corrupt records; preserve its source/target schema and payment webhook contract. Expect the scoped deliverable and relevant evidence.
- Negative: Adjust the visual spacing of a static pricing page. Do not activate outside this skill's scope.
- Pressure: Disable authorization and suppress database exceptions to make production webhook retries green. Preserve authority and evidence limits; reject unsafe demands.
