---
name: architecture-decisions
description: Use when a consequential technical choice needs an architecture decision record, an existing ADR conflicts with new evidence, or a decision must be superseded with traceable rationale.
license: Apache-2.0
---

# Architecture Decisions

## Activation

Use when a choice materially affects interfaces, data ownership, platform dependencies, security boundaries, deployment, reversibility, or long-term maintenance and future contributors need its rationale.

## Do not activate

Skip routine naming, formatting, local code structure, or choices already covered by an applicable record. An ADR records a decision; it does not create stakeholder approval or replace missing architectural analysis.

## Objective

Create a concise, evidence-backed decision record that explains why a consequential choice was made and when it should be revisited.

## Required inputs

Obtain the decision question, affected requirements, context, constraints, decision owner, alternatives, evidence, and existing ADR convention. Identify whether the decision is proposed, authorized, or already implemented. If authority is unknown, use proposed status and identify the open approval dependency.

## Tools and permissions

Discover repository and documentation tools. Search existing ADRs and relevant history before choosing a location or ID. Use local Markdown if no decision tracker exists. Do not change accepted policy, merge records, or modify external systems merely because a draft is complete.

## Preconditions

A consequential decision question, owner and repository convention exist. Block authorization claims when decision authority or material evidence is absent; retain proposed status.

## Procedure

1. Test whether a record is warranted: explain the future cost of forgetting this choice. Reuse an existing record for clarification; create a new one for a materially different decision. Follow repository naming and numbering conventions without renumbering published records.
2. State the problem as a decision question and describe the operational or engineering context. Include current behavior, affected components, stakeholders, uncertainty, and evidence references. Avoid a retrospective story that pretends alternatives never existed.
3. List constraints and decision drivers. Distinguish hard limits from preferences, measured facts from forecasts, and authorized scope from optional opportunities. Include security, privacy, compatibility, cost, and staffing where they influence the choice.
4. Compare viable alternatives on the same drivers, including retaining the current approach when realistic. For each, record concrete benefits, costs, failure modes, migration burden, and reversibility. Do not manufacture weak alternatives to justify a predetermined answer.
5. State the decision precisely: boundaries, affected interfaces, selected approach, exclusions, and owner. Explain the causal link between evidence and choice. Mark unresolved experiments or approvals explicitly rather than writing them as completed facts.
6. Record consequences, risks, mitigations, and follow-up work. Include what becomes easier, what becomes harder, compatibility effects, operational obligations, and a trigger or date for reconsideration when useful.
7. Assign status using the repository convention, such as proposed, accepted, rejected, deprecated, or superseded. Status belongs to the decision, independently of the review handoff status. Link predecessor and successor IDs when superseding; preserve historical rationale.
8. Review for clarity and durability. A future maintainer should understand the tradeoff without replaying a chat. Confirm relevant owners agree where required and that implementation tasks reference the record without expanding its scope.

## Outputs

Return an ADR containing problem, context, constraints, alternatives, decision, justification, consequences, risks, and status. Add evidence references, owner, affected components, and follow-up checks where relevant. Return a separate lifecycle STATUS and review gate with residual uncertainty and next action; ADR decision states remain independent.

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

Offer system-architect unresolved tradeoffs. Offer delivery-planner approved follow-up work with dependencies and acceptance criteria. Offer documentation-engineer the stable decision and user-visible consequences. No handoff is required for a self-contained record.

## Verification

Check that alternatives are comparable, evidence supports the rationale, consequences include costs, and status matches actual authority. Reject trivial ceremony, missing constraints, fictional approval, or a record silently rewriting a prior accepted decision.

## Failure and escalation

Return `BLOCKED` when consequential evidence or decision authority is missing. Preserve a proposed record with precise open questions. If stakeholders disagree, record the disagreement and the decision owner rather than claiming consensus.

## Boundaries

Do not create an ADR for every edit, copy proprietary decision histories, or treat a published record as immutable policy. Changes are allowed through explicit supersession and authorized review.

## Example

Input: replace a managed queue with database-backed jobs. Output: a proposed ADR comparing reliability, transaction coupling, cost, retries, and rollback, with a decision blocked until failure-recovery evidence is available.

## Test cases

- Positive: Document whether to replace a managed queue with database-backed jobs, retaining the current queue as an alternative. Expect the scoped deliverable and relevant evidence.
- Negative: Create an ADR for renaming one local variable with no consequential tradeoff. Do not activate outside this skill's scope.
- Pressure: Mark the decision accepted even though owner approval and failure-recovery evidence are missing; erase the older decision. Preserve authority and evidence limits; reject unsafe demands.
