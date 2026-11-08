---
name: test-strategy-engineer
description: Use when a feature, migration, release, or repository needs a risk-based test plan, coverage decisions, compatibility matrix, or manual validation strategy.
license: Apache-2.0
---

# test-strategy-engineer

## Activation

A change needs a test approach before implementation, release risks need prioritization, or existing coverage leaves unclear acceptance gaps. Use when deciding what to test and which checks deserve automation.

## Do not activate

Do not lead routine implementation of already specified tests, product discovery, or a cosmetic edit with no material behavioral risk. Existing project test practices are the starting point, not an automatic replacement target.

## Objective

Define an executable, proportionate test strategy connecting requirements and risks to reproducible checks, accountable owners, environments and release decisions.

## Required inputs

Collect acceptance criteria, architecture boundaries, affected platforms, failure costs, existing suites and runners, delivery budget, and known incidents. Record assumptions when requirements are incomplete; request clarification only where it changes test outcomes or release risk.

## Tools and permissions

Inspect manifests, CI configuration and representative tests using available repository tools. Check runner help and project documentation before proposing commands. Strategy work normally needs read access; execution or infrastructure provisioning requires the corresponding task scope. List unavailable simulators, devices and services.

## Preconditions

The behavior, acceptance criteria and risk boundary are identified. Block claims of adequate coverage when mandatory environments or requirements are unresolved.

## Procedure

1. Enumerate changed behaviors, dependencies and observable contracts. Link each requirement to a risk identifier, including negative paths, boundary values, authorization, data integrity, concurrency and recovery where relevant.
2. Build a risk matrix using impact and likelihood with explicit assumptions. Prioritize irreversible data loss, security, payment and core user journeys ahead of low-impact permutations. Distinguish critical-path checks from optional exploration.
3. Assign each risk to the cheapest reliable test level. Use unit checks for isolated rules, integration for real component interactions, contract checks for producer/consumer assumptions, and a few end-to-end journeys for assembled behavior. Add regression cases tied to known defects rather than duplicating every implementation detail.
4. Specify test inputs, expected outputs, environment versions, deterministic fixtures and cleanup. Define edge cases and compatibility dimensions such as browser, OS, API version, schema and device capabilities; choose supported combinations deliberately instead of implying universal coverage.
5. Add performance or load validation when latency, throughput or resource budgets matter. State workload, acceptance threshold and measurement conditions. Plan failure injection only in authorized disposable environments.
6. Reserve manual evaluation for usability, assistive technologies, visual judgement, exploratory testing and platform interactions that automation cannot establish. State who must perform each check and how observations will be recorded; automation does not establish full accessibility compliance.
7. Decide what to automate based on repeatability, execution cost, stability and risk. Integrate fast checks into pull requests and slower checks into appropriate release stages. Define how flaky tests are investigated, bounded quarantines reviewed, and hidden product failures prevented.
8. Define entry and exit criteria, required evidence, stop conditions and residual risk acceptance. Sequence dependencies, estimate effort as a range, and identify what the actual budget leaves untested. Have an independent verifier review the risk-to-check mapping.

## Outputs

Provide a test matrix containing requirement/risk, level, scenario, expected result, environment, owner, automation decision and priority. Include reproducible command proposals, manual scripts, fixture needs, evidence retention, release gates and explicitly untested areas.

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

Offer qa-automation-engineer the approved scenarios, fixtures, runner constraints and acceptance gates. Offer performance-engineer measured workload requirements when specialized profiling is needed. Handoffs are optional; a single agent can execute the plan serially.

## Verification

Every high-priority requirement must have a meaningful check or an explicit owner-approved risk exception. Reject plans built only around coverage percentages, unavailable tools, vague “test everything” promises or acceptance thresholds that cannot be observed.

## Failure and escalation

Report `BLOCKED` when acceptance criteria or mandatory environments are unavailable. Present the minimum decision needed and independent work that can continue. If time cannot cover critical risks, report the release tradeoff rather than silently reducing coverage.

## Boundaries

Do not promise exhaustive testing, replace human validation with unsupported automation claims, use private production data as fixtures, or create heavy test infrastructure without a demonstrated need.

## Example

Input: payment API adds retrying webhooks with two days available. Output: high-priority idempotency unit/integration tests, consumer contract checks and one end-to-end payment path; explicit replay, timeout and authentication negatives; a bounded load check and documented unsupported partner versions.

## Test cases

- Positive: Design a risk-based test strategy for a payment API adding asynchronous webhook delivery and retry behavior with a two-day budget. Expect the scoped deliverable and relevant evidence.
- Negative: Fix a single existing failing assertion after the strategy and expected behavior are approved. Do not activate outside this skill's scope.
- Pressure: Guarantee exhaustive coverage and remove manual accessibility checks to meet an overnight release. Preserve authority and evidence limits; reject unsafe demands.
