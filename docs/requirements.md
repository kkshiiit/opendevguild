# Requirements traceability

Scope: the complete master brief, sections 0–21, reconciled on 2026-11-08.
This document maps obligations to artifacts and verification methods; artifact
existence alone does not mark a requirement VERIFIED. Actual outcomes belong in
[verification](verification.md) and the final report.

| Brief | Obligation | Implementation and acceptance evidence |
| --- | --- | --- |
| 0 | Professional modular engineering, all disciplines, original work and evidence | [Catalog](catalog.md), bounded skill procedures, [standards](engineering-standards.md), review/evaluation results |
| 1 | Current official research and ten platform checks | [Research register](research.md), [compatibility](compatibility.md), official validator and source pins; distinguish docs from executed integration |
| 2 | Independent safe workspace and non-destructive operations | Git baseline and inspection evidence; no unrelated changes, credentials, force push or global configuration edits |
| 3 | Four conceptual layers and rejectable verification | [Design](design.md), task/handoff contracts, verifier decisions, negative contract tests |
| 4 | Exactly 34 functional specialist identifiers | catalog.json, all skills/<name>/SKILL.md, specialty scenario/review coverage; no placeholders |
| 5 | Eighteen author-contract elements and official frontmatter | [Skill contract](skill-contract.md), per-skill sections/resources, scenarios and official validation |
| 6 | Maintainable useful repository structure | Single canonical skills/ catalog; populated docs, examples, tests and templates only; no empty filler folders |
| 7 | Eight compatible bounded subagent roles or documented limitation | .codex/agents profiles, syntax/field checks, actual delegation evidence and explicit client-loading limits |
| 8 | Selection by product, task, risk, complexity, stack, dependencies and capabilities | Routing contract/procedure, FAST/STANDARD/CRITICAL decision, positive/negative/ambiguous/single/multiple selection fixtures and error report |
| 9 | Complete collaboration exchange and six lifecycle states | Task/handoff schemas and examples, invalid-state and missing-evidence tests, reviewer-backed VERIFIED |
| 10 | Justified engineering practices, no universal architecture | [Engineering standards](engineering-standards.md), bounded design alternatives and specialty procedures |
| 11 | Six evaluation levels | Structure, selection, functional, security, regression and comparative fixtures/results; exact run versus not_run distinction |
| 12 | Six quality gates and four decision values | Requirements/Architecture/Implementation/Verification/Security/Release records, justified NOT_APPLICABLE and blocked missing evidence |
| 13 | English/Spanish user documentation and five complete examples | README pair, contributor pair, [Android](../examples/android/README.md), [web](../examples/web/README.md), [backend](../examples/backend/README.md), [desktop](../examples/desktop/README.md), [game](../examples/games/README.md) recipes |
| 14 | Secure GitHub community automation | Read-only-token CI, reviewed pinned dependencies, tests/scans, issue/PR templates, [security policy](../SECURITY.md); hosted execution independently observed |
| 15 | Apache-2.0 and original material with attribution | LICENSE, NOTICE, dependency/schema provenance, no affiliation or unauthorized trademark claim |
| 16 | Manual/compatible-tool install, repo/personal, update/uninstall/verification | README recipes, [compatibility](compatibility.md), collision refusal, no silent global install, archive inspection |
| 17 | Selective resource use and stop conditions | Bounded orchestration, reused analysis, targeted reads, dependency-aware concurrency; actual usage metrics only where exposed |
| 18 | Verifiable implementation phases | Inspection, eight-skill core, specialists, subagents, quality, integration, docs and publication gates; disclose any process deviation |
| 19 | Honest final acceptance checklist | Verification record and release gate evidence, complete local repository, clean Git after coherent commits, publication only with actual access |
| 20 | Final report A–I | Executive outcome, architecture, inventory/status/tests, subagents, quality, resource measurements, GitHub identity/state, usage and prioritized next steps |
| 21 | Actual implementation, coherent commits and truthful reporting | Working artifacts, executed commands, retained failures and limits, no optimistic substitute for technical checks |

## State and evidence rules

Lifecycle states: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `NEEDS_REVIEW`,
`VERIFIED`, `FAILED`. Gates: `APPROVED`, `REJECTED`, `BLOCKED`,
`NOT_APPLICABLE`. Risk modes: `FAST`, `STANDARD`, `CRITICAL`.
A gate decision is not a task lifecycle state. A valid schema or prepared
comparison scenario is not proof of host behavior, a completed benchmark or a
published release. Historical records remain bound to their original inputs.

Data engineering is covered through a conditional backend pipeline procedure,
database integrity/modeling, privacy and observability; it does not add an
unrequested 35th identifier. Cross-platform and subagent claims require actual
execution evidence or an explicit documented limitation. Current counts of
passing tests, failed checks, blocked operations and publication are intentionally
not duplicated here; consult the verification record.

Español: esta matriz cubre el prompt completo. Vincula obligaciones con artefactos
y métodos de comprobación; no convierte su existencia en aprobación. El registro
de verificación conserva pruebas reales, fallos, límites y estado de publicación.
