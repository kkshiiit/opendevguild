# Quick usage

[Español](quickstart.es.md) · [Install first](installation.md) · [Troubleshooting](troubleshooting.md)

1. Select **one** responsibility from the [catalog](catalog.md). For a first safe
   session, use scope-guardian; for a supplied code review, code-review-engineer.
2. Install the folder into your client's documented project path and verify it
   appears in discovery. Open your application repository, not this library.
3. Supply the objective, allowed paths, constraints and available acceptance test.
   Invoke the skill explicitly in the syntax that client supports.
4. Review the result and actual evidence. A proposed plan is not implemented code;
   a passing format check is not an executed app test. Missing tools remain blocked.

Codex example:

```text
$scope-guardian Define scope for fixing duplicate order submission.
Allowed: src/orders and tests/orders. Preserve the uncommitted login redesign.
Do not edit or deploy. Return assumptions, affected paths and acceptance checks.
```

Expected: a scope brief that preserves unrelated work and identifies a bounded
verification path. Supply your actual paths and defect; do not blindly apply the
fictional example to a different repository. No app changes are authorized by this
example. For code work use a matching implementation skill after scope is clear.

For a multi-step request:

```text
$mission-control Fix duplicate order submission within src/orders and its tests.
Use the existing stack, preserve unrelated edits, select only needed specialists,
and do not deploy. Return executed checks, review findings and remaining risks.
```

FAST suits small low-risk tasks; STANDARD and CRITICAL add risk-appropriate
controls without granting privileges. An executor ordinarily returns NEEDS_REVIEW;
VERIFIED requires appropriate evidence and independent review. Subagents are
optional client capabilities, not a prerequisite to use skills.

See [eight complete prompt examples](usage-examples.md) and the
[client matrix](client-compatibility.md) for syntax differences. No live invocation
is claimed merely because these examples are present.
