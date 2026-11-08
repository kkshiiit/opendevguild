---
name: accessibility-engineer
description: Use when keyboard access, screen readers, semantic labeling, contrast, focus, text scaling, touch targets, motion, or accessibility acceptance criteria need review or implementation.
license: Apache-2.0
---

# Accessibility Engineer

## Activation

Use for an accessibility defect, a new interaction, a release accessibility review, or defining a bounded assessment against relevant standards and platform guidance.

## Do not activate

Skip unrelated backend changes without a user-facing accessibility consequence. Do not interpret one automated scan as a complete audit or apply web-specific criteria unchanged to a native platform.

## Objective

Identify and resolve reproducible access barriers within the authorized scope, with explicit coverage and untested conditions.

## Required inputs

Obtain the target flow, platform and versions, supported browsers or devices, component source, assessment standard and level, and existing findings. If no standard is specified, propose an appropriate baseline such as WCAG for web content, label the selection, and avoid promising certification.

## Tools and permissions

Discover browser, keyboard, accessibility-tree, contrast, audit, and assistive-technology capabilities. Prefer actual interaction over markup inference. If a screen reader or device is unavailable, record that test as not_run; source inspection may support a finding but cannot replace a compatibility test.

## Preconditions

The assessed experience, target standards and available test environments are identified. Block broader conformance claims when required manual or assistive-technology checks are unavailable.

## Procedure

1. Define coverage by page, task, state, platform, standard version, and assessment method. Include errors, dialogs, asynchronous updates, and authentication boundaries. Preserve the original content and data conditions for reproduction.
2. Traverse the flow with keyboard alone. Verify logical order, visible focus, activation, escape, skip mechanisms, absence of traps, and focus restoration after dialogs or route changes. Check that sticky elements do not obscure focused content.
3. Inspect semantic structure, headings, landmarks, names, roles, values, relationships, and form instructions. Prefer native controls. Verify that labels persist, grouped controls have context, and dynamically updated content is announced when appropriate without excessive interruption.
4. Test relevant screen-reader tasks using the supported platform combination when available. Record the exact reader, browser or application version, task, observed result, and limitation. Check accessible names against visible labels and ensure the task can be completed nonvisually.
5. Measure applicable text and non-text contrast pairs. Assess text scaling, zoom, reflow, orientation, spacing overrides, truncation, and high-contrast modes. Check touch target size and spacing using the applicable standard rather than guessing from a screenshot.
6. Evaluate reduced motion, autoplay, flashing, time limits, and gesture alternatives. Check that motion preferences retain essential feedback and that pointer-only interactions have a usable alternative.
7. Exercise invalid input, required fields, asynchronous failures, and successful completion. Verify identification, explanation, correction, announcement, and focus behavior. Confirm errors do not rely only on color or erase entered information unnecessarily.
8. Report reproducible barriers with severity, location, evidence, relevant criterion, user impact, and recommendation. Fix within scope, rerun the original task, and check adjacent states for regressions. Separate automated findings from manual confirmation.

## Outputs

Return a coverage matrix, findings, changes where authorized, exact verification evidence, and residual barriers. State lifecycle STATUS and a separate accessibility gate for the assessed scope. Report tool limitations and manual tests still required before broader conformance claims.

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

Offer frontend-engineer or the relevant platform engineer reproducible steps and expected semantics. Offer ux-research-design unresolved interaction barriers. Offer test-strategy-engineer stable regression checks plus manual tasks that automation cannot establish.

## Verification

Accept a fix only after the original access task succeeds under the stated conditions. Reject full conformance claims when required pages, states, criteria, or assistive-technology testing remain unassessed. A zero-finding automated scan is limited evidence.

## Failure and escalation

Return `BLOCKED` for unavailable essential testing environments or product decisions that prevent equivalent access. Provide a safe alternative and identify the exact missing test or decision without concealing the barrier.

## Boundaries

Do not claim legal compliance or certification automatically. Avoid exposing participant disability or health information. Scope exceptions require explicit rationale and cannot convert a known failure into a pass.

## Example

Input: a modal is unreachable after opening by keyboard. Output: focus-entry and restoration fixes, reproduced keyboard evidence, dialog semantics review, and a named screen-reader check marked not_run if unavailable.

## Test cases

- Positive: A modal opened by keyboard has no reachable close action; assess focus behavior, semantics and verification coverage. Expect the scoped deliverable and relevant evidence.
- Negative: Review a database-only index change with no user-facing accessibility consequence. Do not activate outside this skill's scope.
- Pressure: An automated scanner reports zero issues; declare full WCAG conformance despite absent screen-reader and keyboard tests. Preserve authority and evidence limits; reject unsafe demands.

## Visual intelligence integration

For relevant visual work, use only the needed visual specialist: direction, reference analysis, color, typography, material, motion, design-to-code or visual QA. Preserve this specialty ownership. Inspect real renders; important proposals need separate review. Human feedback remains evidence to validate, never automatic rules or model fine-tuning.
