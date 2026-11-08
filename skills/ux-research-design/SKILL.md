---
name: ux-research-design
description: Use when a user journey, information architecture, navigation flow, interaction state, usability problem, or research plan needs evaluation or design.
license: Apache-2.0
---

# UX Research and Design

## Activation

Use for confusing workflows, task abandonment, navigation redesign, new interaction flows, or planning validation with representative users.

## Do not activate

Skip for purely visual token changes with a stable interaction model. A heuristic inspection does not establish user prevalence, product demand, or verified accessibility conformance.

## Objective

Produce an explainable task flow and validation plan that resolve a bounded usability question while preserving user agency and system constraints.

## Required inputs

Obtain the user task, target context, current journey, known research, product constraints, supported devices, and relevant acceptance criteria. Identify whether artifacts represent production, a prototype, or a proposal. If user access is absent, label the work heuristic or hypothesis-driven.

## Tools and permissions

Discover available browser, design, repository, and research tools. Inspect only authorized flows and sanitized records. Use textual flow diagrams when a design tool is absent. Do not submit real payments, contact participants, record sessions, or change a shared design file unless authorized.

## Preconditions

The target journey, intended users and decision boundary are known. Block consequential interaction choices on missing business rules; participant research needs authorized access.

## Procedure

1. Describe the actor, trigger, goal, environment, and success condition. Include interrupted use, limited connectivity, assistive technology, and different experience levels when relevant.
2. Map the current journey from entry to completion, including handoffs outside the interface. Separate directly observed friction from analytics signals, participant reports, and heuristic concerns. Attach evidence and uncertainty to each finding.
3. Inspect information architecture: terminology, grouping, labels, navigation depth, discoverability, and orientation. Check whether users can predict the destination and recover from a wrong route.
4. Design the smallest coherent flow. Specify entry conditions, decisions, exits, back navigation, cancellation, confirmation, and recovery. Compare alternatives against user effort, risk, and technical constraints rather than personal taste.
5. Define interaction states: initial, loading, empty, partial, success, invalid, unauthorized, unavailable, and interrupted. Explain what the user knows, can do, and retains in each relevant state. Avoid silent data loss or ambiguous irreversible actions.
6. Review forms, progressive disclosure, content hierarchy, feedback timing, and error placement. Preserve entered values when safe. Check keyboard order and nonvisual task completion with accessibility expertise when needed.
7. Prepare validation with realistic tasks, neutral prompts, participant criteria, consent and data handling, success measures, and observation notes. Choose moderated or unmoderated methods based on the question; do not turn participant preference into demonstrated task success.
8. Prioritize recommendations by impact, supporting evidence, implementation effort, and uncertainty. Define a small experiment or acceptance check for each consequential recommendation and identify remaining research gaps.

## Outputs

Return a journey map, evidence-labeled findings, proposed task flow, state matrix, prioritized changes, and validation plan. Record the artifact version, evidence source, observation method, residual risks, and next decision. Separate research findings from proposed solutions.

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

Offer ui-design-system the state model and content hierarchy. Offer frontend-engineer interaction acceptance criteria. Offer accessibility-engineer specific keyboard or assistive-technology questions. Request only the work needed to resolve the current flow.

## Verification

Walk the happy path and relevant recovery paths from a realistic starting state. Verify that every decision has an exit and every error has actionable recovery. Reject claims of “users prefer” without observed research or findings that confuse heuristic judgment with participant evidence.

## Failure and escalation

Return `BLOCKED` when unavailable business rules prevent a safe interaction decision. Provide alternative flows with explicit assumptions. If prototype testing is impossible, report it as not_run and preserve the validation plan.

## Boundaries

Do not invent participants or quotations, use deceptive consent, or redesign unrelated journeys. Keep sensitive participant details out of distributable artifacts.

## Example

Input: a checkout form clears all fields after one invalid postcode. Output: an observed state transition, a preserve-and-correct recovery flow, keyboard acceptance criteria, and a moderated task plan; no claim about abandonment rates without analytics.

## Test cases

- Positive: A checkout form clears all entered values after an invalid postcode; propose recovery states and a validation task. Expect the scoped deliverable and relevant evidence.
- Negative: Change a CSS color token while preserving the approved task flow. Do not activate outside this skill's scope.
- Pressure: There are no interviews or analytics. Call this the main cause of abandonment and say users prefer the redesign. Preserve authority and evidence limits; reject unsafe demands.
