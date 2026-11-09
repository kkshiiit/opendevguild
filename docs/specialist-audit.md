# Individual specialist audit

Date: 2026-11-09. Scope: all 42 existing SKILL.md bodies and their current scenario
contracts, with particular inspection of responsibility, numbered technical steps,
bounds and rejection behavior. This is a documented-procedure audit, not 42 live
functional evaluations or legal/platform certification. No skill is replaced.

## Method and eighteen criteria

D = explicitly documented instruction; I = illustrative/synthetic example, not an
executed real-product example; M = missing contract location. D is not a passed
behavioral test. The table enumerates each criterion rather than using file existence
as approval. Context/input form describes required information; it does not claim
a separate domain-specific machine input schema for every specialty. Independent
verification describes the required reviewer, not proof that such review occurred.

1. Responsibility.
2. Description.
3. Activate.
4. Do not activate.
5. Context.
6. Procedure.
7. Tools.
8. Limits.
9. Risks.
10. Safety.
11. Input form.
12. Output form.
13. Example.
14. Negative.
15. Accept.
16. Reject.
17. Independent verification.
18. Result documentation.

| Skill | C1–C18 | Procedure evidence and scoped finding |
| --- | --- | --- |
| [accessibility-engineer](../skills/accessibility-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Keyboard, reader tasks, scaling and error recovery are concrete; reader/device combinations still require actual execution. |
| [api-contract-engineer](../skills/api-contract-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Schema/error, authorization, idempotency and webhook boundaries are explicit; no live consumer conformance follows from contract text. |
| [architecture-decisions](../skills/architecture-decisions/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Alternative drivers and supersession preserve decision context; do not conflate ADR accepted state with verified task state. |
| [backend-engineer](../skills/backend-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Atomic retries, tenant checks and pipeline checkpoints are concrete; applied ML/retrieval need separate evidence boundaries. |
| [code-review-engineer](../skills/code-review-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Findings require trigger, impact and location; unseen safeguards cannot be assumed or invented. |
| [color-science-engineer](../skills/color-science-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Separates OKLCH exploration from composited sRGB contrast; real display and background coverage remains bounded. |
| [community-maintainer](../skills/community-maintainer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Contribution rights and triage controls are present; user support/community evidence gets a bounded reference. |
| [database-engineer](../skills/database-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Expand/backfill/switch, constraints and restore are specified; production destructive migration still needs authority. |
| [delivery-planner](../skills/delivery-planner/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Critical path, uncertainty and bounded ownership are explicit; estimates are not measured execution time. |
| [design-to-code-engineer](../skills/design-to-code-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Semantic components and actual captures are required; reference appearance alone cannot approve behavior. |
| [desktop-engineer](../skills/desktop-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | OS-specific storage/install/update distinctions are present; a web screenshot is not native desktop coverage. |
| [devops-ci-engineer](../skills/devops-ci-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Trust boundaries, immutable dependencies and rollback are explicit; no deployment permission is inferred. |
| [documentation-engineer](../skills/documentation-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Examples must execute and bilingual claims align; new onboarding tests complement rather than replace this procedure. |
| [frontend-engineer](../skills/frontend-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Real states, cancellation and focus are covered; localization receives a technical edge-case reference. |
| [game-design-engineer](../skills/game-design-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Sources/sinks, progression and playtest limits already cover game economy; no new economy skill is justified. |
| [gameplay-engineer](../skills/gameplay-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Engine lifecycle, save and multiplayer checks are concrete; audio ownership/accessibility gets a reference. |
| [implementation-engineer](../skills/implementation-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Small compatible diffs and boundary regressions are specified; working components are not rewritten by default. |
| [incident-response-engineer](../skills/incident-response-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Evidence preservation and reversible mitigation precede root cause; no unapproved destructive recovery. |
| [material-rendering-engineer](../skills/material-rendering-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Honest material classes, APIs and real capture/recording requirements are explicit; native targets remain unrun. |
| [mission-control](../skills/mission-control/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Ten triage dimensions, ownership and gates are present; modes do not grant tools or authority. |
| [mobile-engineer](../skills/mobile-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Stack/lifecycle/offline and signing separation are concrete; store-policy evidence remains product-specific. |
| [motion-interaction-engineer](../skills/motion-interaction-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Interruption, reduced motion and clock/trace distinctions are explicit; stills cannot verify dynamics. |
| [observability-engineer](../skills/observability-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | SLI definitions, cardinality, alert action and overhead form a bounded reliability procedure. |
| [performance-engineer](../skills/performance-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Equivalent baselines, percentiles and confounders are required; no speed claim from intuition. |
| [privacy-engineer](../skills/privacy-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Purpose/retention/deletion and vendor flows are covered; jurisdiction/data-rights questions need a reference and owner. |
| [product-discovery](../skills/product-discovery/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Problems, falsifiable hypotheses and metrics are present; commercial/channel/entitlement decisions need a reference. |
| [qa-automation-engineer](../skills/qa-automation-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Observable outcomes, isolated fixtures and failure retention are explicit; tests cannot be weakened to conceal defects. |
| [release-engineer](../skills/release-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Artifact installation and actual remote receipts are separate gates; prepared is not published. |
| [repository-intelligence](../skills/repository-intelligence/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Targeted filenames/history and initial read-only mapping preserve context and unrelated changes. |
| [requirements-engineer](../skills/requirements-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Stable IDs, boundary cases and traceability are concrete; ambiguous policy cannot become a fabricated requirement. |
| [scope-guardian](../skills/scope-guardian/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Necessary support versus optional expansion and explicit exceptions are distinguished; scope remains evidence-based. |
| [security-engineer](../skills/security-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Threat/data boundaries and synthetic repros are present; fraud/moderation policy needs specialized control and appeal handling. |
| [skill-quality-evaluator](../skills/skill-quality-evaluator/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Matched controls and side effects are specified; AI/ML/retrieval/context-specific pitfalls get a reference. |
| [supply-chain-auditor](../skills/supply-chain-auditor/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Actual locks, provenance, hooks and advisories are covered; legal compatibility/store policy needs a separate decision table. |
| [system-architect](../skills/system-architect/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Alternatives, quality scenarios, migrations and bottlenecks are explicit; no universal microservice/Clean prescription. |
| [test-strategy-engineer](../skills/test-strategy-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Risk-to-cheapest-reliable-test mapping and manual boundaries are specified; no coverage from fixture names alone. |
| [typography-composition-engineer](../skills/typography-composition-engineer/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Content extremes, glyphs, semantic order and rights are considered; machine approval is not human localization. |
| [ui-design-system](../skills/ui-design-system/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Tokens, state contracts and responsive exceptions are concrete; does not supply brand/customer authority. |
| [ux-research-design](../skills/ux-research-design/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Observed versus heuristic journeys and consented validation are distinct; invented participants remain forbidden. |
| [visual-art-director](../skills/visual-art-director/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Two directions and separate review are required; an art director cannot approve its own proposal as independent. |
| [visual-qa-auditor](../skills/visual-qa-auditor/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Regions, context and rendered material checks avoid absolute style prohibitions; no arbitrary beauty score. |
| [visual-reference-analyst](../skills/visual-reference-analyst/SKILL.md#procedure) | D D D D D D D D D D D D I D D D D D | Inspection/rights/hash provenance is explicit; public visibility alone does not authorize redistribution. |

## Findings and disposition

- All42 procedures have explicit contract locations for the 18 criteria; missing locations: 0. Current largest main file: 7987 bytes. This is a context-size proxy, not token use.
- Examples are intentionally synthetic and labeled as such. They are authentic project-authored scenarios, not fabricated observations of real customers or production apps.
- Common safety/output boilerplate is repeated for independently installable skills. Domain procedures differ; replacing them with mandatory sibling-skill imports would break selective use. No cosmetic bulk rewrite was warranted.
- Gaps are additional responsibility boundaries: legal/data rights, AI/retrieval/context, marketing/monetization, localization, abuse/appeals, audio and support. Eight on-demand references supply bounded procedures without creating new skill/subagent identities.
- The source already covers data pipelines, game economy/balance, observability/SRE, integrations and accessibility/visual evaluation. Their remaining gap is broader executable evidence, not another job title.
- All new reference procedures are IMPLEMENTED as documentation and negative/acceptance cases, not DEMONSTRATED improvements. Parent project checks establish links/structure; full model/domain/device execution remains pending unless separately recorded.
- Historical smoke/benchmark outcomes remain bound to their actual inputs. None establishes that every current skill satisfies activation, safety or usefulness in every task.

## Required follow-up evidence

Keep routing-policy cases separate from natural-language host activation. Run domain-specific fixtures and independent judgments for changed high-risk procedures before claiming performance, legal compliance, prediction quality or user preference. New references do not silently waive existing six gates.

The related responsibility matrix is [responsibility-coverage.md](responsibility-coverage.md). The mentioned earlier set of 30 proposals was not supplied in this turn or available source; it is not reconstructed or counted.
