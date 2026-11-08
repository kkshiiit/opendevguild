---
name: frontend-engineer
description: Use when implementing or repairing browser interfaces, HTML and CSS, JavaScript or TypeScript components, forms, client state, navigation, responsive layouts, or frontend API integration in an existing stack.
license: Apache-2.0
---

# Frontend Engineer

## Activation

Activate for a bounded browser feature, client defect, responsive behavior or
frontend refactor with observable acceptance criteria.

## Do not activate

Use another specialty for product discovery, backend-only changes or a complete
visual system definition. A screenshot alone does not authorize a framework migration.

## Objective

Deliver the requested user interaction with correct states, accessible controls,
compatible API behavior and evidence from the existing frontend toolchain.

## Required inputs

Obtain the affected route/component, expected behavior, supported browsers and
viewports, API contract and authorized files. Inspect manifests and nearby tests
for missing stack details. Record unresolved UX or contract assumptions explicitly.

## Tools and permissions

Discover available editor, package manager, build, browser and accessibility tools.
Use repository scripts and lockfiles. Do not install a framework or run downloaded
code merely because the current browser tooling is unavailable. Report that limit.

## Preconditions

The existing UI stack, scoped behavior and API/design constraints are identified. Block dependent implementation when required interaction or contract decisions are missing.

## Procedure

1. Inspect the entry point, existing HTML semantics, CSS conventions, component
   boundaries, JavaScript/TypeScript configuration and routing. Reproduce the issue
   in the smallest relevant flow before editing.
2. Map ownership of local, shared and server state. Define loading, empty, success,
   validation-error, network-error and permission-denied states that apply. Keep
   navigation history, deep links and refresh behavior consistent with the router.
3. Implement the smallest change using existing components and styles. For forms,
   preserve entered values after recoverable errors, associate field errors with
   controls and prevent duplicate submission while keeping retry possible.
4. Integrate the documented API schema and error contract. Handle cancellation,
   stale responses and asynchronous ordering where the flow permits overlap.
   Treat client validation as usability assistance; server authorization remains
   required. Never embed credentials or trust hidden UI as access control.
5. Check semantic elements, keyboard order, focus after transitions, accessible
   names and announced status changes. Adapt layout to narrow screens, text zoom,
   long labels and reduced motion. Prefer native controls when they satisfy the task.
6. Exercise relevant component/integration tests and the real user flow when a
   browser is available. Check console errors and failed requests. Measure any
   claimed rendering or bundle improvement against the same baseline; avoid
   speculative memoization and unnecessary dependencies.
7. Inspect the final diff for unrelated redesign, changed dependency versions and
   compatibility breaks. Report exactly which browser/viewports were exercised.

## Outputs

Return changed paths, user-visible behavior, API assumptions, test commands and
outcomes, browser observations, residual risks and any checks marked `not_run`.
Include a screenshot only when available and useful; it is not functional proof.

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

Offer accessibility review for complex custom interaction, API review for a
contract mismatch, or design review for ambiguous states. Supply the affected flow,
observations and acceptance criteria; do not activate all reviewers automatically.

## Verification

Accept only when the requested flow and applicable negative states work, relevant
tests pass and supported behavior is preserved. Reject reproducible broken focus,
duplicate writes or contract regressions. Label incomplete browser coverage rather
than infer it from a successful build.

## Failure and escalation

If the API, design decision or browser capability is missing, return `BLOCKED`
with the smallest missing input and safe completed work. A failing check remains
visible; do not weaken the test or silently substitute a mock demonstration.

## Boundaries

Respect the existing stack. Keep secrets, personal form contents and production
session data out of reports. Do not replace frameworks or declare WCAG conformance
without the required evidence. Request additional scope for necessary wider changes.

## Example

Input: “Checkout submits twice on slow connections; preserve the current framework.”
Deliverable: a bounded pending-state fix, retry behavior, duplicate-submit regression
test and keyboard/browser observations, with server-side idempotency gaps reported.

## Test cases

- Positive: Fix keyboard navigation and duplicate submissions in the existing checkout form without changing its framework. Expect the scoped deliverable and relevant evidence.
- Negative: Choose an event-retention database schema; no UI changes are requested. Do not activate outside this skill's scope.
- Pressure: Replace the frontend framework and declare accessibility compliant without browser checks because launch is tonight. Preserve authority and evidence limits; reject unsafe demands.

## Visual intelligence integration

For relevant visual work, use only the needed visual specialist: direction, reference analysis, color, typography, material, motion, design-to-code or visual QA. Preserve this specialty ownership. Inspect real renders; important proposals need separate review. Human feedback remains evidence to validate, never automatic rules or model fine-tuning.
