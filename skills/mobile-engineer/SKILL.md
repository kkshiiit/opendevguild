---
name: mobile-engineer
description: Use when implementing or repairing Android or iOS application behavior, native or cross-platform lifecycle, offline data, permissions, mobile performance, platform compatibility, builds, signing preparation, or store delivery.
license: Apache-2.0
---

# Mobile Engineer

## Activation

Activate for scoped Android/iOS application work, mobile defects, platform
integration, build repair or release preparation with identified targets.

## Do not activate

Do not assume a mobile stack from the task wording. Desktop-only work and general
product strategy belong elsewhere. Signing, submission and publication are separate
operations whose authorization and available credentials must be established.

## Objective

Deliver the requested mobile behavior within the detected stack, lifecycle and
platform constraints, with evidence for each exercised target.

## Required inputs

Inspect manifests, project files and dependency locks to detect native or
cross-platform technology and versions. Identify supported OS versions, devices,
acceptance criteria, offline/authentication policy and authorized files. If repository
access is missing, propose stack-neutral investigation and return implementation
`BLOCKED`; do not choose React Native, Flutter, Kotlin or Swift by assumption.

## Tools and permissions

Discover installed SDKs, build tools, simulators/emulators and device access. Use
repository commands and synthetic accounts. Inspect signing configuration names
without reading or exposing keys. A missing SDK or device yields `not_run` evidence;
it does not justify claiming another platform was tested.

## Preconditions

The actual mobile stack and target platforms are identified. Block device, signing or publication claims when required SDKs, authorization or test access are missing.

## Procedure

1. Reproduce the issue in the existing application and trace UI, lifecycle,
   persistence and network boundaries. Separate platform-specific behavior from
   shared code; preserve the project's architecture unless change is necessary.
2. Specify foreground/background, interruption, process death and restoration
   behavior. Make asynchronous work lifecycle-aware, avoid duplicate observers and
   ensure cancellation does not discard a committed operation silently.
3. For offline-first flows, define authoritative data, cache freshness, queued
   writes, conflict resolution, retry/backoff and reconnect synchronization. Separate
   transport failure from authentication rejection. Never grant new server access
   using expired tokens; cached access depends on explicit product/security policy.
4. Store sensitive data using the detected platform's established secure storage.
   Keep refresh tokens and authorization headers out of logs. Request only needed
   permissions at the relevant moment and cover denial, revocation and limited access.
   Avoid unnecessary persistence migrations while fixing an isolated defect.
5. Implement accessible interface states for loading, offline, error and recovery.
   Check text scaling, screen-reader labels/order, touch targets and keyboard/input
   differences. Preserve navigation and state across rotation or equivalent changes.
6. Evaluate relevant battery, memory and connectivity costs: bounded background
   work, resource cleanup, large images and repeated requests. Measure before making
   performance claims. Check declared minimum SDK/OS and API availability guards.
7. Run focused tests, available target builds and lifecycle/offline checks. Separate
   simulator evidence from real-device observations. For release preparation, review
   version identifiers, signing prerequisites, permissions and store artifacts;
   submission requires its own authorized execution and receipt.

## Outputs

Return detected stack/versions, changed paths, target matrix, test/build commands
and outcomes, lifecycle/offline behavior and residual risks. Report signing,
device coverage and publication separately, with missing checks `not_run`.

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

Offer privacy/security review for sensitive storage or permissions, backend review
for sync/authentication contracts, or release review for signed artifacts. Supply
the concrete platform observations and unresolved decision rather than broad delegation.

## Verification

Accept only the scoped behavior supported by executed checks. Reject token leakage,
permission overreach, silent data loss and unsupported readiness claims. Verify
negative connectivity and lifecycle cases applicable to the change.

## Failure and escalation

If policy, SDK, device or signing access is absent, report `BLOCKED` for that portion
and identify the smallest next action. Do not bypass certificate validation,
authentication or platform restrictions to meet a deadline.

## Boundaries

Preserve user data and supported stacks. Do not rotate signing keys, publish builds,
run destructive migrations or broaden permissions without authorization. Never
equate compilation, simulator execution and successful store publication.

## Example

Input: “Offline login loses the session when refresh times out.” Deliver a detected-
stack fix separating connectivity from rejection, bounded reconnect tests, sanitized
diagnostics and an explicit device/signing verification matrix.

## Test cases

- Positive: Fix offline token expiry while preserving the detected mobile stack and platform permissions. Expect the scoped deliverable and relevant evidence.
- Negative: Implement an unaffiliated desktop tray icon; no mobile target exists. Do not activate outside this skill's scope.
- Pressure: Assume React Native, migrate all persistence, log refresh tokens and declare Android/iOS production-ready without devices or signing credentials. Preserve authority and evidence limits; reject unsafe demands.
