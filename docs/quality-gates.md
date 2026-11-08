# Quality gates

Gates are evidence-based decisions, distinct from task lifecycle status. The six
gate identifiers and four decisions are project conventions, not Codex APIs.
The handoff schema represents each gate with its name, status, observation basis,
evidence criterion IDs and justification.

| Gate | Evaluate | Evidence for APPROVED | Reject or block when |
| --- | --- | --- | --- |
| Requirements | Goal, scope, constraints and acceptance are testable | Reviewed requirements and resolved material ambiguities | Contradictory goals, unknown required policy or unverifiable criteria |
| Architecture | Design fits constraints and dependencies | Existing architecture or proportionate decision with alternatives | Unjustified migration, incompatible contracts or missing critical decisions |
| Implementation | Result satisfies authorized scope | Actual diff, ownership check and requirement traceability | Unrelated edits, incomplete behavior or dirty work lost |
| Verification | Relevant checks ran and succeeded | Commands/observations, outcomes and retained failures | Required tests failed or required environments are unavailable |
| Security | Applicable risks were assessed | Threat/data/dependency review and required checks | Open blocking defect, secret exposure or unavailable mandatory scan |
| Release | Delivery conditions hold for the claimed state | Install/artifact identity, compatibility, authority and actual remote evidence when claiming publication | Missing destination/authority, checksum mismatch or unsupported publication claim |

Allowed decisions: `APPROVED`, `REJECTED`, `BLOCKED`, `NOT_APPLICABLE`.
Missing evidence never means approval. `NOT_APPLICABLE` requires a substantive
reason: for example, a read-only documentation review has no deployment action.
Ordinary small tasks may determine such non-applicability automatically; no human
approval ceremony is needed for routine reversible work.

For `APPROVED`, evidence references must name passed criteria, and `basis` must
identify `tool` or `inspection`. This distinguishes observed tool results from
engineering judgments. A `VERIFIED` handoff requires all six gates approved or
justifiably not applicable, passed required criteria, no failed observations,
no open blocking findings, ready prerequisites and an independent reviewer record.
Executors ordinarily hand off as `NEEDS_REVIEW`. Missing required capability
produces `BLOCKED`; a rejected result is represented as `FAILED` with the
corresponding gate decision, never a fabricated approval.

`check-handoff` validates the declared record. It does not authenticate identities,
reproduce observations, enforce file permissions or prove that the reviewer is
independent. Those remain responsibilities of the host and actual verifier. The
serial fallback can record self-review and its evidence, but cannot manufacture
an independent verification record to obtain `VERIFIED`.

Español: los gates son decisiones separadas del estado de la tarea. La ausencia
de información bloquea; no aprueba. Los controles no aplicables se justifican sin
pedir confirmaciones innecesarias. Una entrega puede rechazarse aunque su ejecutor
declare haber terminado. El validador comprueba el registro, no su veracidad.
