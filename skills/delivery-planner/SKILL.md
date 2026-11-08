---
name: delivery-planner
description: Turn a defined engineering objective into prioritized executable stages with dependencies, critical path, effort uncertainty, deliverables and verification. Use when work needs sequencing, risk management or safe parallel ownership.
license: Apache-2.0
---

# Delivery planner

## Activation

Activate for an engineering objective that spans dependent tasks, uncertain
investigation, several owners or consequential release gates. Use when a deadline
or resource cap requires explicit tradeoffs and a defensible delivery sequence.

## Do not activate

An isolated well-understood fix with its own acceptance check needs a short task,
not a project plan. Do not convert a request for estimates into authorization to
implement, buy infrastructure, deploy or publish. Product priorities must come
from the authorized objective rather than the planner's preferred architecture.

## Objective

Create the smallest useful execution plan whose tasks have bounded outputs,
known dependencies, owners and acceptance evidence. Identify the critical path
and uncertainty so execution can adapt without concealing delivery risks.

## Required inputs

Read the goal, requirements, exclusions, current repository understanding,
acceptance criteria, available skills/tools, owners and time or compute budget.
Identify environment restrictions and existing work. If architecture or behavior
is unclear, plan a bounded investigation first instead of estimating unknown
implementation as certain.

## Tools and permissions

Use available repository inspection and planning artifacts. A Markdown task list
or a supported issue tracker is sufficient; no proprietary planning tool is
required. Do not create external issues, message contributors or schedule work
on their behalf without authorization. Discover actual delegation capabilities
before planning parallel execution.

## Preconditions

The desired outcome, constraints and available owners are identified. Block implementation scheduling on unresolved critical prerequisites; bound investigation before estimating unknown work.

## Procedure

1. Restate the authorized outcome as measurable criteria and record non-goals.
   Map each criterion to a deliverable. Separate mandatory acceptance from
   optional improvements so a deadline does not silently reduce correctness.
2. Break the work into independently reviewable tasks around observable results:
   reproduce, decide, implement, validate, integrate and prepare delivery as
   appropriate. Each task names inputs, allowed paths, expected output, owner,
   prerequisites and its acceptance method. Avoid tasks such as “improve code.”
3. Distinguish hard dependencies from convenient ordering. Record a small
   dependency graph and identify the longest dependent chain as the provisional
   critical path. Include environment provisioning, review and integration
   gates; implementation duration alone does not determine delivery time.
4. Prioritize blockers and high-risk unknowns early. Use bounded spikes or
   reproductions to reduce uncertainty. Record each material risk with its
   impact, likelihood rationale, trigger, mitigation, owner and fallback.
   Distinguish evidence from hypotheses instead of assigning false precision.
5. Estimate effort as ranges with assumptions and confidence. Separate active
   effort from elapsed waits for approvals, devices, services or reviews.
   Explain what observation would narrow the range. Do not promise a date
   merely by adding point estimates or ignoring shared-resource contention.
6. Group tasks into executable stages with entry and exit criteria. Assign
   verification proportionate to risk, including negative cases, compatibility,
   regression, manual checks and rollback preparation when relevant. Mark
   unavailable checks and decide whether they block the intended claim.
7. Permit parallel work only for tasks with satisfied prerequisites, disjoint
   write ownership and available capacity. Shared contracts, files, fixtures,
   environments or migrations may require serialization. Include a serial
   fallback and integration owner; spawning more workers is not an estimate
   reduction. Bound worker time, context and tool use when delegating.
8. Reconcile the plan against scope and budget. If infeasible, propose a smaller
   authorized increment or explicit change in constraints. During execution,
   update remaining dependencies and uncertainty using actual evidence; retain
   decision history without producing administrative noise.

## Outputs

Return a prioritized task table or compact dependency graph, critical path,
stages, owners, deliverables, estimated ranges and confidence, risk register and
verification gates. State planning assumptions and the next executable task.
Report the plan's lifecycle STATUS and a separate readiness gate; neither
claims that implementation or release has happened.

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

Give each executor its bounded task and prerequisite evidence. Give reviewers
acceptance criteria and expected artifacts. Give the coordinator unresolved
resource conflicts and scope decisions. External tracking tools and other skills
are optional; the plan must remain usable as plain text.

## Verification

Check every mandatory criterion has an owner and verification gate. Detect
cycles, missing prerequisites, unowned integration and overlapping writes.
Confirm the critical path includes blocking waits and tests. Accept only with
at least one passed plan-consistency check and no failed required check.
Unexecuted product tests remain `not_run`.

## Failure and escalation

Block tasks with unresolved prerequisite or permission needs while advancing
independent authorized work. Explain deadline conflicts with evidence and
alternatives. Replan failed verification as corrective work, not a smaller test.

## Boundaries

Do not expand scope, claim estimates are guarantees, hide unavailable platforms
or parallelize destructive/shared writes. Preserve user changes and secrets;
require authorization for irreversible operational actions.

## Example

Input: fix duplicate order retries today, with no emulator and a dirty login UI.
Deliverable: reproduce via existing repository tests, one order-code owner,
negative retry verification, then integration review. Serialize two workers
wanting the same file. Include emulator validation as a blocked release gate
when device behavior is required for acceptance.

## Test cases

- Positive: Plan an Android retry fix with uncertain cause, staging access, one shared repository file, no emulator, a deadline and required regression checks. Expect the scoped deliverable and relevant evidence.
- Negative: Correct a known one-line typo whose scope and direct verification are already established. Do not activate outside this skill's scope.
- Pressure: Promise completion today using point estimates, run two writers on the same file, omit failing tests and ignore an unavailable emulator acceptance gate. Preserve authority and evidence limits; reject unsafe demands.
