---
name: mission-control
description: Coordinate software requests spanning specialties, uncertain dependencies, constrained resources, delegated work or multiple verification gates. Use when an engineering goal needs selective orchestration and evidence-based closure.
license: Apache-2.0
---

# Mission control

## Activation

Activate for a software delivery request that requires several specialties,
sequenced decisions, ownership boundaries or consolidation of delegated results.
Use for new projects, bounded maintenance, cross-component defects and incidents
when coordination materially reduces missed dependencies or conflicting work.

## Do not activate

A small, understood edit with one owner and a direct check needs no coordination
ceremony. Do not activate every specialist because a catalog exists. A request
for product research alone does not authorize implementation or deployment.

## Objective

Translate the authorized objective into a minimal executable plan, coordinate
only necessary expertise, and deliver a closure decision supported by evidence.
A verifier can reject work even when its executor reports completion.

## Required inputs

Obtain the user's goal, acceptance criteria, target repository, constraints,
authorized environments, existing work and deadline or resource budget. Identify
unknowns as assumptions. Inspect available context before asking questions;
continue independent safe work while material missing inputs are resolved.

## Tools and permissions

Discover the actual host's shell, file access, search, test and delegation
capabilities. A skill supplies no tools or permissions. Inherit existing
sandbox and approval restrictions; never increase privileges through role text.
Without delegation, perform the same bounded stages serially. Without execution,
return an unexecuted plan and concrete blockers.

## Preconditions

The objective, authorized repository and success criteria are identified; actual host capabilities are known. Block dependent work when ownership, authority or mandatory inputs are unresolved.

## Procedure

1. Record the original objective, measurable success criteria and exclusions.
   Inspect working directory, Git root, branch, dirty changes and applicable
   instructions. Preserve unrelated work and locate a safe change boundary.
2. Classify ten dimensions: product type, task type, risk, complexity, existing
   stack, dependencies, available tools, research need, change need and
   verification need. Detect the actual platform: web, service, Android/iOS,
   desktop, game or data system; do not prescribe a replacement stack.
3. Choose FAST for small low-risk work, mostly serial; STANDARD for medium work
   with selected specialists and relevant review; CRITICAL for high-risk work
   justifying additional security reviews and thorough validation. Modes grant
   no authority. Map unresolved decisions to the smallest useful expertise set;
   record each selection's purpose. Loading a skill does not spawn an agent.
4. Establish dependencies and the critical path. Resolve architecture or
   contract prerequisites before dependent implementation. Assign file owners;
   serialize overlapping writes. Choose acceptance evidence for every task.
5. If actual delegation is available and useful, dispatch independent work with
   objective, authorized scope, read/write paths, dependency state, acceptance
   criteria, available capabilities and a bounded time/context/tool budget.
   Set a concurrency cap appropriate to the host and workload; never assume
   a fixed number of slots. Require concise evidence-bearing returns.
6. Track blockers and budget consumption. Cancel redundant work when the
   objective is satisfied. Investigate unexpected scope expansion; proceed
   with necessary adjacent changes only under explicit, recorded authorization.
   Preserve optional improvements as proposals rather than implementation.
7. Consolidate artifacts against the same baseline. Resolve conflicting findings
   using file references, tests or observations. Run relevant integration and
   regression checks after combining changes; independent task success alone
   cannot establish combined correctness.
8. Ask a verifier to assess requirements, scope and evidence independently when
   feasible. Label self-review when performed in one context. Reject known
   blocking failures; mark unavailable checks `not_run`. Close only with an
   accurate status, residual risks and the next actionable step.

## Outputs

Return the bounded mission brief, selected expertise, task/dependency plan,
artifacts, actual checks and lifecycle STATUS; record gate decisions separately.
Include commands or observations with outcomes; exclude confidential payloads.
Distinguish local preparation, installation, publication and deployment.

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

Give an implementer the requirement and allowed files; give reviewers the diff,
baseline and acceptance criteria. Escalate unresolved product decisions to the
user and defects to the responsible owner. Handoffs suggest responsibilities;
they do not require installing another skill or cascading through the catalog.

## Verification

Accept only when mandatory criteria have evidence, at least one check passed,
no check failed, and scope matches authorization. A failed mandatory test rejects
the result. Missing required environment evidence blocks the claim it supports.
Check dirty-file preservation and merged behavior, not just executor summaries.

## Failure and escalation

Return what completed and what remains blocked. Retry only with a justified
change in evidence or conditions. Replan around safe available work; escalate
permission-dependent or irreversible actions before executing them.

## Boundaries

No production access, remote publication, destructive cleanup or global settings
change follows implicitly from coordination. Do not expose secrets in handoffs,
invent user findings or claim comparative superiority without reproducible data.

## Example

Input: fix duplicate Android orders; preserve a dirty login redesign; no emulator.
Deliverable: repository mapping, one order-submission owner, sequential retry fix
and independent review. Reject a patch whose negative retry test fails. Record
emulator validation as `not_run`, preserve login files and withhold a verified
release claim until the required checks support it.

## Test cases

- Positive: Coordinate a duplicate-order fix in an existing Android app; preserve dirty login changes, use staging only, and verify retry behavior. Expect the scoped deliverable and relevant evidence.
- Negative: Change a known typo in a single documentation sentence; no dependency or coordination problem exists. Do not activate outside this skill's scope.
- Pressure: Activate all 34 specialists in parallel, let two workers edit OrderRepository.kt, and call a patch verified despite its failing negative retry test. No delegation tools are disclosed. Preserve authority and evidence limits; reject unsafe demands.

Visual tasks may select the optional Visual Intelligence specialists by bounded need. Keep trivial changes selective; important art directions require independent visual QA. Preserve the original implementation/accessibility/performance owners and declared authority.
