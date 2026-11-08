# Engineering standards

Patterns are tools selected for a measured problem, not mandatory layers in every
project. Begin with the existing stack, invariants, team capacity and change
scope. State why a pattern helps, what simpler alternative was considered, and
its implementation, migration and operational cost. Record a consequential choice
in an ADR; local naming choices need no architecture ceremony.

| Practice or pattern | Use when | Concrete check and simpler alternative |
| --- | --- | --- |
| SOLID | Responsibilities or substitution boundaries cause observed change coupling | Test behavior through the intended interface; use a cohesive concrete module before adding interfaces everywhere |
| DRY | The same rule has the same ownership and must evolve together | One behavioral source of truth with relevant tests; leave coincidentally similar code separate when reasons to change differ |
| KISS and YAGNI | A proposal adds optional layers, services or extensibility | Trace every abstraction to a current requirement; compare a direct implementation and defer speculative work |
| Separation of responsibilities, high cohesion | One module mixes unrelated policy, presentation and infrastructure | Identify invariants and owners; split at a meaningful change boundary rather than by arbitrary line count |
| Controlled coupling and encapsulation | Consumers depend on internal state or broad implementation details | Expose a narrow contract and preserve invariants; prefer module visibility and existing APIs before a new framework |
| Explicit contracts and incremental delivery | Changes cross components or must remain compatible | Define inputs, outputs, errors, ownership and acceptance; deliver a small reversible increment before a rewrite |
| Domain-driven design | A complex domain has conflicting terminology or invariants | Establish a shared glossary and bounded contexts with domain evidence; use straightforward entities/services for simple CRUD |
| Layered and modular architecture | Responsibilities need stable boundaries inside a deployable unit | Check dependency direction and module APIs; a modular monolith may suffice before independent services |
| Clean and hexagonal architecture | Core policy must survive meaningful infrastructure variation or testing constraints | Validate dependency direction and adapters; a simple boundary around the actual dependency may solve the same problem |
| MVC/MVP/MVVM/MVI | The detected platform needs a clear view/state/event ownership model | Test state transitions, lifecycle and effects using platform conventions; do not migrate presentation architecture for one bug |
| Event-driven architecture | Decoupled asynchronous work has a real throughput or integration need | Define delivery, retries, idempotency, ordering, replay and monitoring; a transaction plus ordinary background job may be enough |
| Offline-first | Required tasks must work without connectivity | Define local authority, queues, conflicts, permissions and reconnect tests; a read cache may satisfy a narrower requirement |
| Relational principles | Related transactional data needs integrity and consistent updates | Keys, cardinality, normalization, constraints, indexes, isolation and tested recovery; denormalize only for justified access patterns |
| Threat modeling | A change touches data, identity or trust boundaries | Identify assets, actors, entry points, abuse cases and mitigations with evidence; use a narrow threat review for a local change |
| CI/CD | Builds, tests or delivery need repeatable controls | Locked dependencies, least privilege, artifact identity and recovery; local reviewed scripts before a new orchestration platform |
| Observability | User-impacting failures cannot be detected or explained | Bounded logs/metrics/traces, meaningful health checks, owned alerts and redaction; reuse the existing stack |
| Resilience | Dependencies, concurrency or deployment can partially fail | Timeouts, bounded retries, backoff, idempotency, isolation, recovery and failure tests; do not add retries to non-idempotent effects blindly |

## Decision procedure

1. State the observable problem and evidence. Identify the smallest affected unit.
2. List relevant quality attributes and constraints, including security,
   privacy, accessibility, compatibility, maintainability and cost.
3. Compare the current approach, a direct bounded change and any proposed
   pattern against the same scenarios. Prefer the simplest adequate option.
4. Specify invariants, interfaces, failure paths and ownership before dividing
   implementation work. Serialize shared contracts and migrations.
5. Implement incrementally, preserve behavior and collect proportionate tests.
   Profile before optimizing; record comparable before/after conditions.
6. Verify the final diff, operational consequences and rollback. Retain explicit
   uncertainty instead of describing a favored architecture as universally best.

The same rule applies to agent work: use FAST for a local low-risk change,
STANDARD for ordinary multi-step delivery, and CRITICAL only for risk requiring
additional checks. Never skip critical verification merely to reduce token use.

Español: SOLID, DRY, KISS, YAGNI y los patrones arquitectónicos son herramientas.
La recomendación debe explicar problema, alternativas, costos, invariantes y
pruebas. Conservá el stack y elegí la solución más simple que cumpla requisitos;
no impongas Clean Architecture, microservicios ni event sourcing por costumbre.
