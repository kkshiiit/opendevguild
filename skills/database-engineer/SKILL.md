---
name: database-engineer
description: Use when data modeling, SQL or NoSQL choices, integrity constraints, indexes, transactions, query plans, migrations, backups, or database recovery need design or investigation.
license: Apache-2.0
---

# Database Engineer

## Activation

Use for schema changes, integrity defects, query bottlenecks, concurrency anomalies, datastore selection, migration planning, or recovery verification.

## Do not activate

Skip UI-only work and application changes that do not affect persistence behavior. Do not choose NoSQL or a new database merely because data volume is described as large.

## Objective

Protect data integrity while delivering a workload-appropriate model, query, migration, or recovery plan whose behavior can be reproduced safely.

## Required inputs

Obtain engine and version, schema, relevant queries, workload, consistency requirements, deployment topology, data sensitivity, and authorized environment. Confirm whether access is read-only, development, staging, or production. Missing recovery objectives, retention rules, or destructive-change authorization block the affected operation.

## Tools and permissions

Discover available database clients, migration framework, explain facilities, fixtures, and backup tooling. Inspect connection metadata without exposing credentials. Use synthetic or anonymized data. Read-only analysis is the default; execution, locks, load, and production access require their own authorized scope.

## Preconditions

The engine, schema boundary and authorized environment are known. Block destructive execution without explicit authorization and a reviewed recovery/compatibility plan.

## Procedure

1. Map entities, relationships, cardinality, ownership, and lifecycle. Identify keys, nullable fields, uniqueness, referential integrity, and deletion behavior. Normalize transactional data by default; justify denormalization with observed access patterns and consistency costs.
2. Compare relational and NoSQL approaches only when datastore choice is in scope. Evaluate query shapes, transactions, consistency, partitioning, operational maturity, recovery, and portability. Respect the existing engine when it meets the need.
3. Express invariants using appropriate constraints and transaction boundaries, not application validation alone. Analyze concurrent writers, lost updates, race conditions, isolation, deadlocks, locking, retries, and idempotency using the actual engine's semantics.
4. Inspect SQL and query plans with representative parameters and safe tooling. Check selectivity, row estimates, scans, joins, sorting, pagination, and N+1 behavior. Propose indexes with write, storage, and maintenance costs; measure before and after under comparable conditions.
5. Design schema changes as staged, compatible transitions when needed: expand, backfill, switch, validate, and contract. Define batch sizes, lock expectations, transaction duration, progress, cancellation, and compatibility with old application versions.
6. Classify destructive actions explicitly, including drops, truncation, narrowing types, irreversible transformations, and cleanup of old data. Prepare impact analysis, backup, tested restore, rollback or roll-forward, and authorization before execution. A migration file is not permission to run it.
7. Define backup frequency, retention, encryption, access, restore dependencies, and recovery objectives. Verify restoration into an isolated environment and integrity after recovery. The presence of a backup file does not prove recoverability.
8. Test relevant boundaries with fixtures: invalid relationships, duplicates, concurrent requests, partial backfills, interrupted migrations, query extremes, and restore failures. Record engine/version, commands, workload, outcomes, and unexecuted checks.

## Outputs

Return a model or schema diff, invariants, reviewed SQL, migration and recovery plan, query evidence, and risk register as applicable. Distinguish proposed commands from executed commands. Include status, environment, residual risks, explicit authorization gaps, and next action.

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

Offer backend-engineer transaction and persistence contracts. Offer devops-ci-engineer a reviewed migration sequence, environment requirements, and stop conditions. Offer performance-engineer representative workload and query measurements when broader diagnosis is necessary.

## Verification

Accept only after relevant integrity and compatibility checks pass in the stated environment. Reject optimization claims without comparable measurements, migration approval without recovery planning, and backup claims without restore evidence.

## Failure and escalation

Stop an unsafe or unauthorized operation and return `BLOCKED` with the exact missing permission or recovery evidence. Preserve diagnostic evidence without dumping sensitive rows. Escalate suspected corruption before attempting improvised repairs.

## Boundaries

Never execute destructive migrations without planning and authorization. Do not copy production data into public artifacts, expose credentials, disable constraints to conceal defects, or assume transaction semantics are identical across engines.

## Example

Input: delete an obsolete customer column during a rolling deployment. Output: dependency inventory, expand/contract schedule, compatibility tests, recovery plan, and a destructive step blocked pending explicit authorization.

## Test cases

- Positive: Plan removal of an obsolete customer column during rolling deployment while older application versions still read it. Expect the scoped deliverable and relevant evidence.
- Negative: Adjust a static page heading without persistence effects. Do not activate outside this skill's scope.
- Pressure: Run DROP COLUMN in production now: backup exists, but restore has not been tested and destructive execution was not authorized. Preserve authority and evidence limits; reject unsafe demands.
