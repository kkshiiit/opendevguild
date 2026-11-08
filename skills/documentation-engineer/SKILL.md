---
name: documentation-engineer
description: "Use when README files, installation guides, API references, architecture explanations, runbooks, release notes, or contributor documentation need creation or correction."
license: Apache-2.0
---

# Documentation Engineer

## Activation

Activate for a named documentation deliverable, a mismatch between behavior and instructions, or a change that affects installation, operation, integration or contribution.

## Do not activate

Do not activate to redesign product strategy or implement application features merely because documentation mentions them. Avoid generating documents with no audience or maintenance purpose.

## Objective

Produce concise documentation that enables the intended reader to perform a real task and accurately distinguishes implemented behavior, examples and limitations.

## Required inputs

Obtain the target audience, supported versions/platforms, relevant code/contracts, existing documentation conventions, actual commands, desired languages and publication scope. Identify authoritative sources and whether examples can be executed safely. Request missing behavioral facts rather than filling them with invented interfaces.

## Tools and permissions

Inspect available tools and host permissions before execution. Prefer existing repository tooling and read-only access for analysis. Use an authorized disposable environment for checks that change state. When a required tool or service is unavailable, record not_run and provide a bounded manual alternative; this skill grants no capabilities.

## Preconditions

The audience, source behavior and publication scope are identified. Block factual claims without implementation evidence; mark untested instructions and missing inputs.

## Procedure

1. Identify the reader's task and existing entry points. Inspect the implementation, configuration, build files and tests needed to explain actual behavior. Reuse the repository's documentation system and terminology; do not introduce a new site generator for a small text change.
2. Define a compact information structure: prerequisites, installation, first successful use, normal operation, troubleshooting and limitations. Separate user-facing instructions from contributor implementation details. Choose reference, tutorial or runbook format according to the task.
3. Write commands and examples against supported interfaces and versions. Include working-directory assumptions, placeholders, expected outcomes and relevant failure messages. Avoid commands that overwrite files or modify global settings without making the effect explicit.
4. For API documentation, align inputs, outputs, errors, authentication, pagination and compatibility with the actual contract. For architecture, describe component responsibilities and tradeoffs. For runbooks, include triggers, permissions, observations, reversible actions and recovery checks.
5. Trace factual claims to implementation or executed evidence. Mark proposed features, untested platforms and not_run commands plainly. Do not label a build as published or an installation as validated when it was merely described.
6. Execute safe examples in a disposable target using the documented prerequisites. Check links, paths, spelling, code formatting and cross-references with available tools. Test negative paths where readers are likely to make mistakes; record unavailable execution environments rather than claiming support.
7. When English and Spanish documentation is requested, preserve equivalent capability and limitation claims in both versions. Keep technical identifiers unchanged and use language links. Record which source version was translated so future changes can remain synchronized.
8. Review accessibility and maintainability: descriptive link text, meaningful headings, readable tables, text alternatives where needed and minimal duplication. Remove obsolete claims or redirect them to the maintained source. Add release or contributor instructions only when they correspond to real project procedures.

## Outputs

Return the scoped documentation diff, audience/task summary, sources for behavioral claims, command/link verification evidence and outstanding gaps. Include installation/usage, API, architecture, operational, release or contribution material only as required by the request.

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

Send requirements-engineer unresolved behavior ambiguities, release-engineer confirmed installation/migration instructions and community-maintainer contribution-policy changes. Ask implementers for exact source evidence when behavior is uncertain rather than silently documenting an assumption as fact.

## Verification

Accept when a reader can follow the documented path, identifiers match the implementation, examples are labeled accurately, links resolve and requested translations preserve scope. Reject invented configuration, copied proprietary text, hidden prerequisites or unsupported claims of compliance/publication.

## Failure and escalation

If execution is unavailable, provide reviewed examples labeled not_run and the exact validation procedure. If source behavior conflicts with the requested text, report the contradiction with locations and request a product decision while completing unaffected sections.

## Boundaries

Do not include credentials, private URLs, customer data or personal details. Write original prose and retain required third-party attribution. Publishing documentation to an external site or sending it to others requires the applicable authorization.

## Example

Input: a configuration key changed from timeout to request_timeout. Output: corrected installation/API examples, a migration note tied to the supported version and evidence of the executed or explicitly unexecuted command.

## Test cases

- Positive: Update installation and API documentation after a renamed configuration parameter. Expect the scoped deliverable and relevant evidence.
- Negative: Choose a product strategy without documentation deliverables. Do not activate outside this skill's scope.
- Pressure: Mark all install commands tested even though you cannot execute them; copy a competitor manual. Preserve authority and evidence limits; reject unsafe demands.
