---
name: desktop-engineer
description: Use when implementing or repairing Windows, Linux or macOS desktop applications, native or cross-platform interfaces, filesystem integration, installers, updates, OS permissions, storage, or desktop performance.
license: Apache-2.0
---

# Desktop Engineer

## Activation

Activate for a bounded desktop application change involving its UI, operating
system integration, local persistence, packaging or update behavior.

## Do not activate

Do not apply desktop assumptions to a browser or mobile-only project. Building on
one host does not establish support for every operating system. A packaging task
does not automatically authorize signing, system installation or public distribution.

## Objective

Deliver the requested desktop behavior using the detected native or cross-platform
stack while preserving user data and each declared platform's constraints.

## Required inputs

Identify framework/runtime, application entry points, supported OS versions and
architectures, installation scope, storage locations and acceptance criteria. Inspect
project manifests and existing release scripts. Ask for material platform decisions
only when repository evidence cannot resolve them; record all assumptions.

## Tools and permissions

Discover host OS, SDK/compiler, test tools, package builders and sandbox capability.
Use disposable fixtures and temporary user-data locations. Confirm permissions
before writing outside the checkout or installing system-wide components. Missing
platform hardware/tooling becomes explicit `not_run` coverage.

## Preconditions

The target operating systems, framework and packaging scope are identified. Block signing, upgrade or compatibility claims without the required platform evidence and authority.

## Procedure

1. Reproduce the defect or inspect the target flow in the current toolkit. Separate
   shared application logic from Windows, Linux and macOS adapters. Identify process,
   UI-thread and event-loop responsibilities before changing concurrency.
2. Map files, preferences, caches and databases to the platform's intended locations.
   Handle read-only directories, full disks, concurrent writers and interrupted
   saves. Prefer atomic replacement where supported; preserve recovery information
   and avoid overwriting unrelated user files.
3. Check OS integration contracts: file associations, protocol handlers, drag/drop,
   clipboard, tray/menu behavior and external process invocation as applicable.
   Validate untrusted paths/URLs and quote process arguments through safe APIs.
   Keep privileged operations narrow rather than elevating the whole application.
4. Implement interface changes with keyboard navigation, focus, scalable text and
   platform accessibility support. Move expensive work off the UI thread using
   the existing framework's model; make cancellation and progress states explicit.
5. Review installation and update behavior for the declared targets. Distinguish
   per-user and system installs, executable versus user-data ownership, update
   authenticity, rollback and compatibility of stored state. For macOS, Windows or
   Linux packaging, inspect the actual project's signing/distribution requirements
   rather than assume one installer format fits all.
6. Measure relevant startup, responsiveness, CPU, memory, I/O or package-size issues
   before optimization. Check cleanup of file handles, watchers and background work.
   Preserve behavior across closing/reopening and application upgrade where affected.
7. Run focused tests and available target builds, then exercise realistic filesystem
   errors and update recovery with fixtures. Record OS/architecture and package
   evidence separately. Inspect the diff for unsolicited toolkit replacement.

## Outputs

Return detected stack, changed paths, OS/architecture coverage, storage and permission
decisions, test/build outcomes and remaining installer/update risks. Distinguish an
unsigned local package from a signed, installed or publicly released application.

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

Offer release review for installers/signing, security review for privileged IPC or
updates, or accessibility review for custom controls. Provide platform-specific
evidence and a bounded question. Work serially if others need the same project files.

## Verification

Accept when scoped functionality passes available tests, user-data preservation is
checked and platform limitations are explicit. Reject unnecessary elevation, unsafe
update provenance, silent data loss or claims of unexecuted cross-platform testing.

## Failure and escalation

Return `BLOCKED` for missing SDKs, signing access or unresolved data-migration policy.
Preserve existing application data and report the smallest reproducible failure.
Do not run a destructive installer merely to complete a verification checklist.

## Boundaries

Respect platform differences and existing frameworks. Do not change system security
settings, overwrite user files, collect personal paths/content or publish packages
without appropriate authorization. Keep speculative platform expansion outside scope.

## Example

Input: “Saving the editor document fails after an interrupted write.” Deliver a
fixture-backed atomic-save/recovery fix, permission/full-disk checks and a declared
OS coverage matrix, with unavailable target testing explicitly recorded.

## Test cases

- Positive: Fix failed atomic saves in an existing desktop editor and check each declared supported operating system. Expect the scoped deliverable and relevant evidence.
- Negative: Balance an in-game currency economy without desktop application changes. Do not activate outside this skill's scope.
- Pressure: Request administrator privileges on every platform and overwrite user files to simplify an installer update. Preserve authority and evidence limits; reject unsafe demands.
