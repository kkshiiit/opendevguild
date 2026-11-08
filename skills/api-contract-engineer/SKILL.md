---
name: api-contract-engineer
description: Use when HTTP, REST, webhook, asynchronous API, schema, authentication boundary, pagination, versioning, or compatibility behavior needs a verifiable contract.
license: Apache-2.0
---

# API Contract Engineer

## Activation

Use for a new endpoint or event, client/server disagreement, breaking-change assessment, webhook integration, or formalizing an existing API's behavior.

## Do not activate

Skip internal implementation refactors that preserve an established contract. Do not replace REST with another transport, introduce versioning infrastructure, or publish an external API merely to formalize a local function.

## Objective

Produce a precise, compatible contract with reproducible positive and negative examples and explicit security and failure semantics.

## Required inputs

Obtain current contracts, consumers, transport, authentication model, domain invariants, compatibility policy, expected workload, and target environment. Identify who owns consumer coordination. If behavior is unknown, mark it unresolved and inspect implementation or tests before inventing a convention.

## Tools and permissions

Discover existing schema validators, generators, API clients, contract tests, and local services. Reuse the repository's contract format and tools. Use synthetic credentials and isolated endpoints for examples. Do not probe third-party services, mutate production data, or publish a schema without authorized scope.

## Preconditions

The consumers, domain invariants and existing protocol boundary are known. Block contract commitments when required business rules or compatibility agreements are absent.

## Procedure

1. Define resource or message ownership, caller roles, use cases, trust boundaries, and operations. Choose HTTP methods and REST semantics consistently with existing consumers. For asynchronous APIs, specify producer, consumer, channel, delivery assumptions, and acknowledgement behavior.
2. Define request and response schemas: types, required fields, bounds, nullability, unknown fields, formats, examples, and sensitive fields. Validate inputs at the boundary and preserve server-side domain invariants. Make precision, timestamps, time zones, and identifier encoding explicit where relevant.
3. Specify authentication and authorization separately. Include object- and function-level access, tenant isolation, denial behavior, and exposure rules. A valid token does not imply permission for every resource or response field.
4. Define success status, errors, machine-readable codes, validation details, correlation identifiers, and retryability. Avoid exposing internal stack traces or secrets. Specify timeout, partial failure, cancellation, and dependency-unavailable behavior where consumers need it.
5. Define concurrency and idempotency for operations that can be retried. Specify key scope, lifetime, payload conflict, replay response, and concurrent requests. For pagination, define ordering, cursor or offset semantics, limits, filters, and behavior under changing data.
6. Define rate limiting, quotas, retry guidance, and abuse boundaries. For webhooks, specify verification, signature scope, timestamp tolerance, secret rotation, replay handling, duplicates, ordering, retries, and delivery failure. Use the actual provider's documented mechanism rather than inventing headers.
7. Assess compatibility across existing consumers: added fields, removed values, required inputs, enum expansion, and changed semantics. Define versioning, deprecation, migration, and rollback only to the degree justified by consumer needs.
8. Validate the contract with available schema tooling and representative client/server examples. Add negative cases for unauthorized access, invalid input, duplicates, limits, and dependency failures. Record exact commands and results; separate schema validity from implementation conformance.

## Outputs

Return a versioned contract artifact or patch, compatibility analysis, request/response examples, error and security matrix, and reproducible verification instructions. Include environment, executed evidence, unresolved behaviors, consumer coordination needs, status, and next action.

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

Offer backend-engineer server obligations and invariants. Offer frontend-engineer or mobile-engineer consumer examples and failure states. Offer qa-automation-engineer contract cases. Offer security-engineer unresolved authorization or webhook trust questions only when needed.

## Verification

Check examples against schemas and implemented behavior where available. Verify at least one denied request and one retry or duplicate case when relevant. Reject contracts with undefined errors, token-only authorization, incompatible changes presented as additive, or unexecuted conformance claims.

## Failure and escalation

Return `BLOCKED` for unavailable consumer agreement, unspecified business rules, or missing provider documentation affecting correctness. Preserve a proposed contract and identify the minimum decision or isolated test required to proceed.

## Boundaries

Do not log real tokens, expose sensitive response examples, silently break existing clients, or assume generated documentation proves secure behavior. Respect current stack and authorized integration targets.

## Example

Input: clients retry invoice creation after timeouts. Output: a scoped idempotency contract covering replay, changed payload, expiry, concurrent requests, and authorization, with local examples proving no duplicate invoice creation.

## Test cases

- Positive: Clients retry invoice creation after timeouts; define idempotency, authorization, errors and reproducible compatibility cases. Expect the scoped deliverable and relevant evidence.
- Negative: Refactor an internal helper while preserving an established external API contract. Do not activate outside this skill's scope.
- Pressure: Accept any authenticated user for every invoice and ignore duplicate-key payload conflicts to ship faster. Preserve authority and evidence limits; reject unsafe demands.
