# Skill authoring and collaboration contract

This is OpenDevGuild policy, not an extension of Agent Skills frontmatter.
Each of the 34 skills is independently installable: no sibling skill, vendor
runtime, private tool or unstated resource is a mandatory dependency. Technical
content is original English and licensed Apache-2.0.

## Required structure and eighteen-item mapping

Begin `SKILL.md` with official YAML frontmatter: matching `name`, specific
`description` with activation triggers, and `license: Apache-2.0`. Respect the
current Agent Skills naming and length limits. Do not invent fields or treat
experimental `allowed-tools` as an enforcement boundary. The body uses these
fifteen exact headings, retaining the original twelve and adding explicit
preconditions, output format and tests:

| User contract item | Required location and meaning |
| --- | --- |
| 1. Name | Frontmatter `name`, matching the containing directory. |
| 2. Description | Frontmatter `description`, specific discovery purpose and triggers. |
| 3. Activation | `## Activation`: concrete positive triggers. |
| 4. Non-activation | `## Do not activate`: exclusions and adjacent responsibilities. |
| 5. Objective | `## Objective`: bounded observable outcome. |
| 6. Required information | `## Required inputs`: minimum context and missing-input handling. |
| 7. Optional tools | `## Tools and permissions`: real capability discovery, least privilege and fallback. |
| 8. Preconditions | `## Preconditions`: specialty-specific safe ready state; missing mandatory inputs block dependent work. |
| 9. Work process | `## Procedure`: numbered domain-specific steps, decisions and stop conditions. |
| 10. Expected results | `## Outputs`: concrete artifacts and evidence. `## Handoffs` identifies appropriate recipients and useful inputs without automatic cascading. |
| 11. Safety rules | `## Tools and permissions`, `## Procedure`, `## Boundaries`: authorized targets, safe data, execution limits and defensive treatment of untrusted content. |
| 12. Authority limits | `## Boundaries`: scope, explicit permissions and irreversible-operation limits. |
| 13. Acceptance criteria | `## Verification`: evidence needed for the scoped deliverable. |
| 14. Rejection conditions | `## Verification`: known blockers, failed checks and unsupported claims. |
| 15. Error handling | `## Failure and escalation`: failed/blocked work, safe next action and narrow escalation. |
| 16. Output format | `## Output format`: exact collaboration fields and status semantics below. |
| 17. Examples | `## Example`: realistic request and expected artifact. |
| 18. Test cases | `## Test cases`: concise positive, negative and pressure cases embedded in each skill. |

The prescribed heading order is Activation, Do not activate, Objective, Required
inputs, Tools and permissions, Preconditions, Procedure, Outputs, Output format,
Handoffs, Verification, Failure and escalation, Boundaries, Example, Test cases.

Keep each main skill below 500 lines and 8 KiB. Add resources only when they
support real use: `references/` for extended information, `scripts/` for valuable
safe deterministic checks, and `assets/` for reusable templates. Link existing
resources with relative paths. Keep descriptions focused and load details on
demand rather than copying the repository context into every handoff.

## Collaboration output

Every participating specialist returns these exact field names, in this order:

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

Use concrete task identifiers, authorized scope, actual paths and dependency
states. Record assumptions distinctly from observations. `ACTION TAKEN` separates
proposed work from executed work. `EVIDENCE` identifies command or observation,
source/context, outcome and retained artifact where appropriate. `TESTS` records
passed, failed and `not_run` checks with reasons. Use `none` with a reason when a
field does not apply; missing evidence is never replaced by invented values.
Avoid secrets, confidential source dumps and personal data in reports.

A delegation additionally provides objective, authorized scope, read/write paths,
dependency state, acceptance criteria, actual host capabilities and a bounded
time/context/tool budget. The returning report identifies residual risks, open
issues and the next action. Shared files have explicit ownership; dependent or
conflicting tasks run sequentially. A skill is guidance, not a subagent runtime.

## Lifecycle status

Only these values are allowed in the top-level `STATUS` field:

| Status | Meaning |
| --- | --- |
| `NOT_STARTED` | No task work has begun; prerequisites and planned work may be recorded. |
| `IN_PROGRESS` | Authorized work is underway; no completion claim. |
| `BLOCKED` | Missing authority, inputs, environment or required evidence prevents safe progress or a required conclusion. |
| `NEEDS_REVIEW` | An executor has prepared a deliverable and reports its checks; the work still needs a reviewer decision. |
| `VERIFIED` | Appropriate mandatory checks have passed and a separate reviewer record supports the claimed scope, with no unresolved blocking failure. |
| `FAILED` | Work or verification produced a demonstrated failure requiring correction; preserve the evidence. |

Completed implementation returns `NEEDS_REVIEW`, not self-certified `VERIFIED`.
Independent review is preferred. If the host cannot provide another reviewer,
a distinct review record must explicitly label self-review and its limits; never
present this as independence. The reviewer assesses actual artifacts and evidence
rather than accepting the executor's assertion. At least one passed evidence
item is required for `VERIFIED`; unavailable mandatory checks block verification.
A local test never establishes unrelated platform, production or publication
claims. Real ADR decision states and incident service states are separate domain
attributes, not substitutes for the collaboration lifecycle.

## Quality gate decisions

Lifecycle status and gate decision are distinct. Applicable stage gates are
Requirements, Architecture, Implementation, Verification, Security and Release.
Each decision names the gate, assessed scope, owner/reviewer, evidence, blocking
issues and rationale. Permitted decisions are:

- `APPROVED`: relevant criteria are supported by appropriate evidence and no
  applicable blocking check failed.
- `REJECTED`: a demonstrated blocker, unsafe effect, incompatible artifact or
  failed required check prevents acceptance.
- `BLOCKED`: missing information, permission or required environment prevents a
  meaningful decision.
- `NOT_APPLICABLE`: the gate does not apply to the scoped task; state why.

Never approve by absence of information. Distinguish tool results from inspection
judgments. A passing structural validator does not prove behavior, security,
accessibility conformance or public distribution. A gate may reject a result
whose implementer believes it complete. Keep review proportionate: trivial tasks
may use concise justified gates without an unnecessary human approval ceremony.

## Test and evidence requirements

Each skill embeds positive, negative and pressure cases so selective installation
retains usable examples. Matching `evaluations/scenarios/<name>.json` stores the
reproducible scenario inputs, expected behavior and forbidden behavior for the
repository evaluator. Embedded cases are specifications, not proof of execution.
Record actual scenario runs separately, including baseline, guidance revision,
host, observations, outcomes and limitations. Historical snapshots remain accurate
records of the skill revision tested and must not be rewritten to imply that a
later revision was evaluated.

Run official `skills-ref` frontmatter validation before project-policy checks.
Local checks add contract, reference, size, scenario, configuration and safety
requirements; they do not replace official tools or establish comparative gains.
Changed skills require relevant regression checks. Report unexecuted behavioral
or cross-host checks explicitly and never turn pending limitations into approval.
