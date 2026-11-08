# Backend example: validated task creation endpoint

This is a complete API task for an existing local service, not a runnable server
fixture bundled here. The service must already provide authentication, tenant
context, persistence and a test framework. Use its existing implementation stack.

## Objective and contract

Implement `POST /tasks` for an authorized member of the active tenant. Accept
JSON containing only `title`, a string trimmed to 1–120 characters. Reject malformed
JSON, missing/blank/oversized titles, wrong types and unknown fields with the
service's consistent validation error format and HTTP 400. Missing authentication
returns 401; a caller disallowed by the existing membership policy receives 403.
Do not create a new authentication system or trust a caller-supplied tenant ID.

On success, persist one task in the server-selected tenant and return HTTP 201
with its generated `id` and normalized `title`. Preserve current identifiers,
error conventions and transaction facilities. A persistence failure must not
return a successful creation. Scope includes endpoint/service code, the smallest
necessary compatible persistence addition, the contract and tests.

## Selected skills and sequence

1. repository-intelligence finds route registration, auth/tenant resolution,
   validation, persistence and isolated test fixtures.
2. api-contract-engineer expresses the concrete request, response, errors and
   authorization cases in the project's existing contract format.
3. backend-engineer implements the agreed contract and relevant transaction/error
   behavior; qa-automation-engineer adds meaningful endpoint/integration tests.
4. code-review-engineer checks correctness, tenant isolation and scope. Request
   database-engineer only if a consequential schema/migration decision emerges.

## Copyable request

```text
$mission-control Task BACKEND-TASK-1: implement POST /tasks in this existing local
service, using its authenticated tenant context and framework. JSON accepts only
title: trim to 1–120 characters. Return 201 with generated id/title; 400 for
invalid JSON/title/unknown fields, 401 without authentication and 403 when the
existing membership policy denies creation. Persist under the server-selected
tenant; no caller tenant override. Use STANDARD, synthetic isolated fixtures,
existing contracts/tools and bounded file ownership. Test valid/invalid input,
authorization, tenant isolation and storage failure. No production migration,
new auth framework or deployment. Return evidence, gates and open issues.
```

## Expected results and controls

Return the contract, focused implementation and executable tests in the detected
project. Include exact-boundary titles, whitespace-only, array/number/null titles,
unknown `tenant_id`, missing identity, denied membership, cross-tenant isolation,
and storage failure without a 201 or partial inconsistent write. Confirm returned
ID/title match the persisted record and diagnostics contain no credentials.

Requirements and Architecture assess contract and use of existing boundaries;
Implementation reviews scope/invariants; Verification requires observed endpoint
and integration outcomes; Security evaluates authorization/input/secret risks.
Release is NOT_APPLICABLE for this local task with justification. A destructive
schema change or absent tenant policy blocks the affected work until resolved.
Independent review plus evidence supports VERIFIED; writing test files alone does
not demonstrate they passed.

## Limitations

Commands depend on the actual language/framework and isolated database. No claim
of production readiness, universal security, load capacity or cross-service
compatibility follows from these cases. Retry/idempotency behavior beyond the
stated endpoint contract requires a separate explicit decision. Production data,
external service credentials and public endpoint probing are outside scope.

Español: implementá un endpoint de tareas con título validado, autenticación y
tenant existentes. Probá límites, entradas inválidas, permisos, aislamiento y
fallo de almacenamiento en fixtures locales. Usá el contrato concreto y el stack
actual; no inventes autenticación ni ejecutes migraciones de producción.
