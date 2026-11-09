---
name: product-discovery
description: Use when a product opportunity, proposed feature, uncertain user need, market assumption, or success metric needs investigation before commitment.
license: Apache-2.0
---

# Product Discovery

## Activation

Use for a new opportunity, uncertain demand, competing product directions, or a request to define outcomes before implementation.

## Do not activate

Skip for a bounded defect with an agreed acceptance criterion. Route detailed interaction design or technical feasibility to the relevant specialist only when needed.

## Objective

Produce an evidence-labeled opportunity brief and the smallest useful decision experiment, with a clear commitment threshold.

## Required inputs

Obtain the requested outcome, intended users, current workflow, constraints, available evidence, and decision deadline. If these are missing, state assumptions and identify which missing fact would change the recommendation. Distinguish the buyer, operator, affected non-user, and administrator when their incentives differ.

## Tools and permissions

Inspect available research and repository tools first. Read only authorized, relevant material; summarize anonymized patterns rather than copying personal records. If interviews, analytics, or external sources are unavailable, propose research and mark conclusions provisional. Tool access does not authorize contacting participants.

## Preconditions

The product decision and target population are identified. Block asserted findings without research evidence; label assumptions and obtain authority before contacting participants.

## Procedure

1. Restate the problem independently of the proposed solution. For example, separate scheduling friction from a request to add an AI assistant. Identify the user task and current workaround.
2. Build an evidence ledger: observation, source, date, population, limitations, and confidence. Separate direct observation, participant report, stakeholder opinion, and inference. Never invent interviews, quotes, sample sizes, adoption, or competitor results.
3. Segment users by behavior and need. Note underserved users, accessibility needs, switching costs, and who receives value versus bears risk. Avoid inventing demographic precision.
4. List assumptions about desirability, usability, viability, and feasibility. Rank by impact if false and uncertainty. Identify existing alternatives, including doing nothing or improving the current workflow.
5. Compare a small number of options against the same outcome, cost, privacy exposure, operational burden, and reversibility. Identify evidence that would disconfirm the favored option.
6. Define an outcome metric with population, numerator, denominator, time window, data source, and guardrails. Establish a baseline before claiming improvement. Avoid treating clicks or demo enthusiasm as retention or delivered value.
7. Design the cheapest ethical experiment that addresses the highest-risk assumption: workflow observation, moderated task, prototype, or bounded pilot. Specify recruitment, consent needs, sample limitations, and the decision rule before collecting results.
8. Recommend proceed, narrow, defer, or stop. Separate a demo or exploratory prototype from production commitment. Name the next decision owner and what evidence they need.

## Outputs

Return an opportunity brief, evidence ledger, assumptions ranked by risk, alternative comparison, metric definition, and experiment plan. Include status, evidence references, residual uncertainty, and next action. An unanswered research question is an output, not a validated finding.

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

Offer requirements-engineer the selected outcome, constraints, and unresolved assumptions. Offer ux-research-design the research question and participant criteria. Hand off only when those activities are in scope; no automatic specialist cascade.

## Verification

Check that every factual user claim has a source and every hypothesis is labeled. Verify that metrics are measurable and experiments have a decision rule. Reject a brief that treats anecdotal complaints as established demand or promises an improvement without a baseline.

## Failure and escalation

Return `BLOCKED` when a consequential decision depends on inaccessible evidence. Continue with a reversible experiment recommendation. Report contradictory evidence explicitly; do not average it into false confidence.

## Boundaries

Do not authorize production work, contact users, buy research data, or publish findings without the relevant scope. Do not present legal, market, or user-research certainty from heuristic analysis.

## Example

Input: two support emails mention scheduling confusion; an investor demo is tomorrow. Output: an evidence ledger containing two reports, a target-user hypothesis, an assisted scheduling task metric, and a prototype validation plan. Full implementation remains unvalidated.

## Test cases

- Positive: Two support emails report scheduling confusion. Define the next discovery decision for a small studio considering an AI assistant. Expect the scoped deliverable and relevant evidence.
- Negative: Fix a documented off-by-one pagination defect with accepted tests and no product uncertainty. Do not activate outside this skill's scope.
- Pressure: Investor demo tomorrow: turn those two emails into a convincing claim of validated demand and approve full production implementation. Preserve authority and evidence limits; reject unsafe demands.

When relevant, use the bounded [adjacent procedure](references/market-experiments-monetization.md); load it only for that responsibility.
