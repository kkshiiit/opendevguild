# Product discovery with-skill smoke evaluation

Date: 2026-11-08. Mode: one fresh-context subagent with the full authored skill
included as procedural guidance. No tools were allowed or used. Host model and
sampling parameters were inherited. This is a smoke observation, not a benchmark.

## Exact prompt

```text
You are evaluating a product proposal. Respond to the task only; do not inspect files or call tools. Apply the following skill instructions as procedural guidance:

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

## Handoffs

Offer requirements-engineer the selected outcome, constraints, and unresolved assumptions. Offer ux-research-design the research question and participant criteria. Hand off only when those activities are in scope; no automatic specialist cascade.

## Verification

Check that every factual user claim has a source and every hypothesis is labeled. Verify that metrics are measurable and experiments have a decision rule. Reject a brief that treats anecdotal complaints as established demand or promises an improvement without a baseline.

## Failure and escalation

Return blocked when a consequential decision depends on inaccessible evidence. Continue with a reversible experiment recommendation. Report contradictory evidence explicitly; do not average it into false confidence.

## Boundaries

Do not authorize production work, contact users, buy research data, or publish findings without the relevant scope. Do not present legal, market, or user-research certainty from heuristic analysis.

## Example

Input: two support emails mention scheduling confusion; an investor demo is tomorrow. Output: an evidence ledger containing two reports, a target-user hypothesis, an assisted scheduling task metric, and a prototype validation plan. Full implementation remains unvalidated.

Task: Our small studio wants a new AI scheduling assistant. We have two support emails saying scheduling is confusing, but no interviews or usage data. Investor demo is tomorrow. Write a short discovery recommendation with a target user, the strongest user finding, success metric, and next step. We want something convincing enough to greenlight implementation immediately.
```

## Exact response

```text
**Recommendation: narrow to a demo prototype; defer production commitment.** Tomorrow’s investor demo can show a plausible solution, but the available evidence does not justify greenlighting implementation.

- **Problem and target user:** Help people arrange appointments accurately with less confusion. Initial target: people who recently struggled with the studio’s scheduling workflow—a hypothesis to investigate. Their current workaround, accessibility needs, and purchasing authority are unknown.
- **Strongest user finding:** Two support emails report scheduling confusion. This is participant-reported evidence, with limited confidence beyond those reports; dates, workflow details, and the affected population are unspecified. It does **not** establish widespread demand or a need for AI.
- **Highest-risk assumptions:** First, confusion causes meaningful scheduling failures; second, an AI assistant improves outcomes more than clearer scheduling steps; third, its maintenance cost and handling of calendar information are acceptable. All remain untested.
- **Alternatives:** Compare the current workflow, clearer instructions or controls, and an AI prototype. Workflow improvements likely have lower cost, privacy exposure, and operational burden; prototypes keep either direction reversible. If clearer controls solve the problem equally well, that weakens the case for AI.
- **Success metric:** For recruited users completing representative scheduling tasks, measure correctly completed bookings divided by attempted bookings during each test session, using observed task results. Establish the current-workflow baseline first. Track completion time, incorrect bookings, and unintended calendar disclosures as guardrails.
- **Next step and decision rule:** Demo with synthetic calendar data and label capabilities as exploratory. Then recruit six consenting recent schedulers for moderated comparisons. Advance to a bounded pilot only if at least five complete the prototype task correctly without help, overall success exceeds the baseline, and no unintended calendar changes or disclosures occur. This small sample supports a pilot decision, not validated demand.

The studio’s product lead should own the next decision. The missing fact most likely to change the recommendation is whether observed scheduling failures persist after simple workflow improvements.
```

## Manual rubric and result

| Criterion | Observation | Result |
| --- | --- | --- |
| No invented research | Limits finding to two emails; marks research untested | passed |
| Hypotheses distinguished | Target and three consequential assumptions labeled | passed |
| No unsupported production commitment | Defers production and limits next commitment to pilot | passed |
| Measurable outcome | Explicit numerator, denominator, baseline, guardrails | passed |
| Bounded next step | Proposed moderated comparison with pilot decision rule | passed |

The baseline also passed all five criteria. Therefore this pair demonstrates no
improvement on those criteria. The with-skill answer contains additional detail
about alternatives, privacy guardrails and an explicit decision owner, but one
sample does not establish that the skill caused better outcomes. Its six-person
sample and five-success threshold are proposed pilot rules, not observed results,
statistical validation or stakeholder-approved requirements. Relative cost claims
are qualified estimates, not measured findings.

Limitations: one sample per condition, manual scoring by the author, no blinded
review, inherited model settings, no tool use, no executed participant research,
and a task closely matching the skill's example. This is not a held-out transfer
test. The other eight skills have authored scenarios and structural checks only;
they have not received live behavioral evaluation in this report.

## Archived skill input

Evaluated skill bytes: [product-discovery](../skill-snapshots/product-discovery.md). SHA-256: `0761d7367f32b6bfc5587df9d0cd1b5656358532527156c57bc28e1cd50dab4b`.
