---
name: ui-design-system
description: Use when visual hierarchy, typography, color, spacing, component variants, design tokens, themes, responsive behavior, or interface consistency need definition or refinement.
license: Apache-2.0
---

# UI Design System

## Activation

Use for inconsistent components, new visual patterns, theme requirements, token consolidation, or adapting an established interface across sizes and input methods.

## Do not activate

Skip when the task is limited to a business rule or API defect. Do not create a full component library for one isolated control or replace an existing framework merely to match a preferred aesthetic.

## Objective

Produce a small, coherent visual specification and component contract that can be implemented and checked against real states and screen sizes.

## Required inputs

Obtain the existing design system, brand constraints, relevant screens, interaction flows, target platforms, supported themes, and implementation stack. Ask for missing brand authority only when it affects an irreversible choice; otherwise label a reversible design proposal as provisional.

## Tools and permissions

Discover available design, browser, screenshot, repository, and contrast tools. Inspect the implementation before adding dependencies. If visual rendering is unavailable, deliver explicit tokens and state specifications while recording visual checks as not_run. Do not change shared libraries or purchase assets without scope.

## Preconditions

The target interface, existing stack and visual constraints are known. Block incompatible brand decisions; preserve existing tokens until change scope is established.

## Procedure

1. Inventory existing typography, colors, spacing, layout grids, radii, elevation, iconography, and component variants. Identify actual duplication and inconsistent semantics before introducing abstractions.
2. Define visual hierarchy around primary user tasks. Choose readable type sizes, line heights, measure, and emphasis. Check long labels, localization, dynamic content, and text scaling rather than designing only ideal short content.
3. Separate primitive tokens from semantic tokens and component overrides where reuse justifies it. Define meaningful names, units, fallback values, and ownership. Keep one source of truth and document how tokens reach the existing stack.
4. Specify color roles for text, surface, action, feedback, and focus. Define light, dark, and high-contrast behavior where required. Verify relevant contrast pairs; color alone must not carry state or urgency.
5. Specify each affected component's anatomy, variants, dimensions, content rules, and interaction states: default, hover, focus-visible, pressed, disabled, loading, error, and selected when relevant. Distinguish disabled controls from unavailable actions requiring explanation.
6. Define responsive behavior with content-driven breakpoints, reflow, wrapping, touch targets, keyboard behavior, and overflow rules. Test narrow screens, zoom, long content, and coarse pointer input. Avoid fixed layouts that hide important controls.
7. Add purposeful interaction feedback and motion only when it clarifies state. Define reduced-motion behavior and avoid animation that delays task completion. Compare the bundle and maintenance cost before proposing a visual dependency.
8. Implement or specify the smallest reusable pattern, then check representative screens and states for consistency. Record exceptions with reasons rather than forcing every layout into one component abstraction.

## Outputs

Return a token table or source patch, component/state specification, responsive rules, representative examples, and an evidence-backed review checklist. Include dependency impact, unresolved visual checks, known exceptions, and a migration plan when existing tokens change.

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

Offer frontend-engineer component contracts and tokens. Offer accessibility-engineer the relevant contrast, focus, scaling, and motion states. Offer ux-research-design only unresolved interaction decisions, not a request to rework an already agreed flow.

## Verification

Compare before and after at the same viewport, content, and theme. Check legibility, focus visibility, state coverage, contrast, reflow, and dependency cost. Reject a proposal that documents only the default state or claims visual verification without rendering evidence.

## Failure and escalation

Return `BLOCKED` for conflicting brand requirements that prevent usable output. Provide evidence and bounded alternatives. Mark unavailable screenshots or platform checks as not_run and name the next verification owner.

## Boundaries

Respect the current stack and authorized screens. Do not import unlicensed assets, hide accessibility issues with visual polish, or add a heavy library without a documented need and impact.

## Example

Input: three inconsistent submit buttons and a new dark theme. Output: semantic action tokens, one button contract with focus/loading/error states, dark-theme contrast checks, and examples at narrow and wide widths.

## Test cases

- Positive: Three forms use inconsistent submit buttons and need a dark theme; define the smallest shared token and state model. Expect the scoped deliverable and relevant evidence.
- Negative: Repair a backend authorization condition with no interface change. Do not activate outside this skill's scope.
- Pressure: Install a large UI library for the three buttons and declare visual quality verified without rendering. Preserve authority and evidence limits; reject unsafe demands.

## Visual intelligence integration

For relevant visual work, use only the needed visual specialist: direction, reference analysis, color, typography, material, motion, design-to-code or visual QA. Preserve this specialty ownership. Inspect real renders; important proposals need separate review. Human feedback remains evidence to validate, never automatic rules or model fine-tuning.
