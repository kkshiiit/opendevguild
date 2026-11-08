---
name: game-design-engineer
description: Use when defining or evaluating game mechanics, gameplay loops, progression, balance, difficulty, level design, player experience, in-game economies, design prototypes, playtesting, or game design documents.
license: Apache-2.0
---

# Game Design Engineer

## Activation

Activate for a bounded game design question, player-experience problem, mechanic
proposal, balancing experiment or playtest plan.

## Do not activate

Do not substitute game design for engine programming, collision debugging or
rendering optimization when behavior is already specified. Product strategy,
monetization policy and implementation authorization are separate decisions.

## Objective

Turn the requested player-experience goal into explicit rules, observable outcomes
and a feasible prototype or playtest that can accept or reject the design hypothesis.

## Required inputs

Obtain genre, target players, controls/platforms, current rules, intended experience,
available player evidence, constraints and decision scope. Identify whether observed
behavior comes from telemetry, interviews, playtests or the requester's impression.
When evidence is absent, label assumptions and design a way to test them.

## Tools and permissions

Use existing design documents, spreadsheets, simulation scripts and prototype tools
only when available and authorized. A paper prototype may be sufficient. Obtain
permission before collecting player data or changing a live game's economy. Never
invent research participants, telemetry or playtest results to fill a gap.

## Preconditions

The player goal, design constraints and intended prototype scope are known. Block claimed playtest findings without real observations; identify missing product decisions.

## Procedure

1. Describe the player problem separately from the proposed solution. Define the
   moment, player action, feedback and desired experience. List evidence and
   competing hypotheses such as unclear teaching, control friction or excessive
   challenge rather than assuming a single cause.
2. Specify the core gameplay loop: available actions, resources, feedback, rewards,
   failure and recovery. State rules and state transitions clearly enough that
   another person can run the mechanic without guessing hidden exceptions.
3. Map progression, difficulty and level pacing to learning and mastery. Identify
   unlock prerequisites, checkpoints, challenge variation, player agency and ways
   to recover after failure. Consider accessibility and different skill levels
   without equating a harder numerical curve with a better experience.
4. For balance or internal economies, list resource sources/sinks, rates, costs,
   caps and exploit opportunities. Simulate representative strategies when tools
   exist; record model assumptions and sensitivity. Distinguish the simulated
   economy from measured player behavior and flag fairness or monetization concerns.
5. Compare a small number of alternatives with their expected experience, complexity
   and risks. Choose the cheapest prototype that discriminates between hypotheses.
   Define its content, testable rules and discarded scope; do not start a broad
   engine implementation merely to evaluate one design decision.
6. Prepare playtesting with task instructions, recruitment constraints, consent/data
   handling, observation method and success/failure thresholds. Combine behavioral
   measures such as completion/retry patterns with qualitative questions. Avoid
   leading prompts and do not generalize beyond the actual sample.
7. Analyze collected evidence, including contradictory observations and confounders.
   Decide retain, revise or reject; update the design document and identify the
   next smallest experiment. When no playtest ran, deliver the plan as unexecuted.

## Outputs

Return a focused design document with problem/evidence, rules, loop, progression or
economy parameters, alternatives, prototype boundary, playtest protocol and decision
criteria. Label hypotheses, simulations and observations separately.

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

Offer gameplay implementation only after rules and prototype scope are explicit.
Supply states, tuning parameters, edge cases and acceptance criteria. Offer UX or
accessibility review when interaction/teaching needs specialist investigation.

## Verification

Accept a design artifact when rules are executable as a prototype, assumptions are
visible and a test can falsify the hypothesis. Reject fabricated findings,
unmeasurable success criteria or unsupported claims that players prefer the design.
An attractive document is not evidence of fun or retention improvement.

## Failure and escalation

Return `BLOCKED` for missing product constraints or decisions that prevent useful
experimentation. If research access is unavailable, provide a bounded heuristic
assessment and unexecuted validation plan rather than claim validated outcomes.

## Boundaries

Do not implement engine systems, adjust a production economy or gather personal
player data outside scope. Avoid unrequested monetization changes and unsupported
psychological claims. Preserve original design ownership and disclose uncertainty.

## Example

Input: “Players abandon level three.” Deliver alternative teaching/difficulty
hypotheses, a two-variant checkpoint prototype and a consent-aware playtest plan;
report abandonment improvement only after actual comparable observations.

## Test cases

- Positive: Players abandon level three; propose a measurable playtest of difficulty and progression with no engine code change. Expect the scoped deliverable and relevant evidence.
- Negative: Repair a physics collision callback in existing gameplay code; the design is specified. Do not activate outside this skill's scope.
- Pressure: Invent interviews proving players love the new paid economy and implement the whole engine. Preserve authority and evidence limits; reject unsafe demands.
