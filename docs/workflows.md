# Practical workflows / Flujos prácticos

These are selection examples, not mandatory specialist chains. Read only the
procedures needed for the current task. A simple correction can use one
implementation specialist and one verification step. Record assumptions rather
than turn every task into a full product lifecycle. The lifecycle and six gates
remain explicit; a small task may justify non-applicable architecture or release
work without scheduling unnecessary human approval.

## Bounded bug fix

Use repository-intelligence to locate the entry point, existing conventions and
failing behavior. Set scope with paths and exclusions. Select the matching
implementation specialist, reproduce the defect and verify the fix using the
existing test runner. Use code-review-engineer for an independent check when
available; compare the final diff to authorized scope. Return executed checks,
outcomes and unexecuted checks. Do not add a framework migration to a bug fix.

## New web feature

Use product-discovery only when the problem or user assumptions are uncertain;
requirements-engineer makes acceptance criteria testable. UX, UI and accessibility
specialists address interaction needs when relevant. Set the API contract before
frontend/backend implementations depend on it. These implementations may proceed
in parallel only with stable contracts and disjoint ownership. Review security
and privacy according to affected data and trust boundaries. Verify failure,
loading, authorization and responsive states before release work.

## Mobile or desktop change

Discover the actual framework, target OS versions, device capabilities and build
configuration first. Use mobile-engineer or desktop-engineer rather than assuming
a framework. Plan lifecycle/offline/persistence tests and per-platform acceptance.
Signing, store publication and installer rollout are separate authorized actions;
an absent SDK, device or certificate remains a reported limitation.

## Game prototype and gameplay implementation

Use game-design-engineer to define the core loop, player hypothesis and a bounded
playtest. Use gameplay-engineer after engine/version/platform discovery to implement
the agreed mechanic. Preserve a deterministic reproduction or saved scenario;
measure frame time and allocation when a performance problem is suspected.
Do not treat engine correctness as proof of fun or playtest feedback as invented
user research. Multiplayer adds server authority and adversarial input checks.

## Data ingestion or transformation pipeline

Use requirements-engineer for data freshness, quality and recovery criteria.
database-engineer owns entity/schema constraints, staging, migrations, transactional
boundaries and query plans. backend-engineer owns ingestion, transformations,
idempotent retries, checkpoints, replay, backpressure and job failures in the
existing stack. Define lineage from source to published dataset, schema evolution,
late/duplicate/corrupt records and reproducible quality checks. privacy-engineer
reviews purpose, minimization and retention. observability-engineer defines lag,
throughput, rejected-record metrics and safe alerts. Test restore/replay on
synthetic data before an authorized production change. Record batch versus stream
tradeoffs rather than adding a data platform by default.

## Incident

incident-response-engineer classifies impact and preserves sanitized evidence.
observability-engineer correlates available signals; security-engineer participates
when a security event is suspected. Propose reversible mitigation and recovery,
verify user-visible restoration and record the timeline and uncertainty. Get
authorization for destructive actions. Root-cause analysis follows stabilization;
preventive work goes through ordinary scope and regression checks.

## Selection, exchange and gates

Record product type, task type, risk, complexity, detected stack, dependencies,
available tools, need for research, need for changes and need for verification.
Use descriptions and exclusions to choose the smallest relevant specialist set.
An ambiguous request receives a bounded investigation or explicit assumption;
it does not activate the entire catalog. Compare the expected selection to actual
selection in positive, negative, ambiguous, single-skill and multi-skill cases.
Measure unnecessary activations and missed required specialties when those
fixtures run; fixture presence is not an executed selection result.

| Mode | Typical work | Proportionate controls |
| --- | --- | --- |
| FAST | Small understood change with low impact | Usually one executor, direct checks and compact review; no gratuitous delegation |
| STANDARD | Multi-step change with known boundaries | Relevant specialists, dependency sequencing and applicable independent review |
| CRITICAL | Consequential security, data, operational or compatibility risk | Explicit threat/recovery analysis, stronger relevant tests and independent verification |

The exchange contains task ID, objective, scope, inputs, assumptions,
dependencies, files involved, action taken, evidence, tests, risks, open issues
and lifecycle status. Machine-readable forms use the current project schemas;
these are conventions, not platform tool signatures. Preserve concrete evidence
pointers instead of passing large files into every context.

Lifecycle: NOT_STARTED → IN_PROGRESS → NEEDS_REVIEW → VERIFIED when requirements,
evidence and independent review support it. Missing prerequisites use BLOCKED;
failed work uses FAILED. Resumption records the changed condition. An executor's
completion claim or self-review alone cannot produce VERIFIED.

| Gate | Question |
| --- | --- |
| Requirements | Is required behavior sufficiently clear and testable? |
| Architecture | Is the necessary technical design justified? |
| Implementation | Does the change meet authorized scope and invariants? |
| Verification | Did the applicable tests and observations execute and pass? |
| Security | Were relevant security/privacy/supply-chain risks assessed? |
| Release | Are the intended delivery/publication conditions satisfied? |

Every gate records APPROVED, REJECTED, BLOCKED or NOT_APPLICABLE with a reason.
Distinguish automated tool outcomes from inspection judgments. Absence of
information never approves a gate. Do not turn an out-of-scope publication into
a blocker for a verified local-only patch: mark the release gate's actual scope
and justify non-applicability where appropriate.

## Complete task recipes

Use the [Android](../examples/android/README.md),
[web](../examples/web/README.md), [backend](../examples/backend/README.md),
[desktop](../examples/desktop/README.md) and [game](../examples/games/README.md)
examples for complete objectives, sequences, outputs, controls and limitations.
They are illustrative tasks for an existing local project, not application
fixtures or proof that the corresponding SDKs executed in this repository.

## Resource policy

Start serially for small tasks. Delegate when independent work has a clear benefit,
with an explicit worker/time/context budget and file ownership. Send concise
inputs and evidence pointers, not the whole repository. Stop or reduce parallelism
when dependencies, shared files, rate limits or service contention remove the
benefit. Retry a failed worker only with a changed input or diagnosed transient
failure. Do not claim a token reduction without actual usage measurements.

Español: seleccioná especialistas según el problema concreto. Los ejemplos no
son cadenas obligatorias. Registrá alcance, entradas, dependencias y aceptación;
paralelizá solamente trabajos independientes. Elegí FAST, STANDARD o CRITICAL
según el riesgo, sin ampliar permisos. Las tareas usan NOT_STARTED, IN_PROGRESS,
BLOCKED, NEEDS_REVIEW, VERIFIED y FAILED. Los seis gates usan APPROVED, REJECTED,
BLOCKED o NOT_APPLICABLE justificado. VERIFIED necesita evidencia y revisión
independiente. Un build local no demuestra publicación, compatibilidad en
dispositivos ni cumplimiento normativo.
