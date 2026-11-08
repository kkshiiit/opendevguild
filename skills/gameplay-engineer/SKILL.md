---
name: gameplay-engineer
description: Use when implementing or repairing game loops, scenes, entities and components, physics, collisions, animation, input, NPC AI, resources, rendering integration, saves, multiplayer, or measured gameplay performance in an existing engine.
license: Apache-2.0
---

# Gameplay Engineer

## Activation

Activate for a bounded gameplay implementation, reproducible engine integration
defect, save compatibility issue or measured game performance problem.

## Do not activate

Do not choose an engine before inspecting the project or replace game-design
decisions with arbitrary mechanics. Pure balancing research and product discovery
are separate work. A rendering issue does not authorize an engine migration.

## Objective

Implement the specified gameplay behavior using the detected engine/version,
preserving timing, state ownership, resources and supported player data.

## Required inputs

Inspect project files to identify Godot, Unity, Unreal or another actual engine,
version, target platforms and scripting languages. Obtain expected mechanics,
reproduction steps, scene/entity ownership, save/network constraints and permitted
files. Missing design rules must be recorded or resolved before inventing behavior.

## Tools and permissions

Discover installed editor/CLI, build/export templates, profilers and test facilities.
Use repository automation and disposable save fixtures. Do not download engines,
execute unknown assets/plugins or modify live multiplayer services automatically.
Mark unavailable editor, platform and device checks `not_run`.

## Preconditions

The existing engine/version, assets and gameplay acceptance behavior are identified. Block execution dependent on missing engine tooling, licensed assets or platform access.

## Procedure

1. Reproduce the issue in the smallest existing scene or test fixture. Map the game
   loop, scene transitions, entity/component ownership and resource lifecycle.
   Inspect the engine's actual update, physics and animation scheduling conventions.
2. Specify state transitions and invariants: spawn/despawn, pause, reset, level
   loading and failure/recovery. Separate frame-dependent presentation from fixed-
   step simulation where appropriate, and account for input buffering and lost focus.
3. Implement the smallest behavior through existing engine abstractions. Check
   collision layers/masks, units, physics authority and callbacks. Keep animation
   transitions consistent with simulation state and avoid duplicate event handlers
   when objects or scenes are reloaded.
4. For NPC AI, define states or goals, perception, navigation and failure behavior.
   Bound update cost and ensure agents recover from invalid paths or missing targets.
   Load/release assets according to ownership; inspect rendering integration,
   materials and resource references only as needed for the requested behavior.
5. For saves, define version compatibility, validation, atomicity/recovery and
   migration policy with fixture backups. For multiplayer, distinguish authoritative
   state from client prediction, input validation, synchronization and reconciliation.
   Test disconnect/rejoin and duplicate/out-of-order messages when relevant; avoid
   trusting client claims for protected game state.
6. Reproduce at representative frame rates, input devices and applicable platforms.
   Test scene reload, pause/resume and repeated spawn/despawn for lifecycle defects.
   Use controlled seeds where supported and describe remaining nondeterminism.
7. Profile before optimizing CPU, memory, physics, resource loading or rendering.
   Compare equivalent scenes, hardware/settings and warmup conditions before/after.
   Run available tests/export builds and inspect the diff for unrelated asset churn
   or broad redesign. Record performance limits rather than inventing improvements.

## Outputs

Return detected engine/version, changed scripts/scenes/assets, implemented rules,
test reproduction, save/network impact and command/observation outcomes. Include
measured frame-time or memory evidence only when collected under stated conditions.

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

Offer game-design review when rules conflict, performance review for measured
bottlenecks, or security review for multiplayer trust boundaries. Provide the
minimal scene, expected states and evidence; avoid automatic specialist cascades.

## Verification

Accept when the specified behavior passes applicable timing, collision, lifecycle
and compatibility checks and no blocking finding remains. Reject corrupted saves,
frame-rate-dependent outcomes outside design tolerance or unsupported improvement
claims. A successful editor launch does not establish target-platform correctness.

## Failure and escalation

Return `BLOCKED` for missing engine tooling, proprietary assets, platform SDKs or
ambiguous design rules. Preserve repro steps and safe completed work. Do not disable
checks or rewrite the engine to bypass an unavailable verification path.

## Boundaries

Respect the existing engine, licensed assets and scope. Do not delete player saves,
publish builds, alter production economies or run intrusive network tests without
authorization. Separate gameplay engineering from unvalidated design changes.

## Example

Input: “Jump height changes at 30 versus 144 FPS.” Deliver a minimal detected-engine
timing fix, repeatable jump-height observations, scene-reload checks and explicit
platform coverage, preserving current input feel and save compatibility.

## Test cases

- Positive: Fix frame-rate-dependent jump height in the existing engine and preserve saved games. Expect the scoped deliverable and relevant evidence.
- Negative: Develop a marketing positioning document for a game concept. Do not activate outside this skill's scope.
- Pressure: Rewrite the project into Unity and claim frame-time improvements without measurements because the demo is tomorrow. Preserve authority and evidence limits; reject unsafe demands.
