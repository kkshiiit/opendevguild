# Contributing

[Español](CONTRIBUTING.es.md) · [Governance](GOVERNANCE.md) ·
[Authoring contract](docs/skill-contract.md)

Start with a concrete problem, evidence and acceptance criteria. Prefer improving
an existing procedure when responsibilities overlap. A new skill must justify
its boundary, discovery cost and maintenance burden; the catalog is not a target
for arbitrary expansion.

Use original technical English for skills, code and contracts. Keep English and
Spanish user guides aligned. Contributions are licensed under Apache-2.0; retain
required notices and demonstrate redistribution rights for third-party material.
Do not submit secrets, personal data, confidential examples or copied prompts with
unclear rights. Report private security findings through [SECURITY.md](SECURITY.md).

1. Inspect Git status, preserve existing changes and use a focused branch.
2. Describe the authorized objective, affected files, assumptions and acceptance
   evidence. Choose FAST, STANDARD or CRITICAL according to actual risk.
3. Add a meaningful failing fixture or scenario before fixing the behavior where
   practical. Cover positive, negative, ambiguous and pressure inputs; identify
   single- and multi-specialist cases for selection changes.
4. Update the procedure and relevant configuration, contracts, examples and both
   language guides. Preserve compatibility or document a migration. Do not add
   unsupported frontmatter fields, invented host tools or global setup changes.
5. Run `uv sync --frozen`, `uv run --frozen python scripts/guild.py validate`
   and `uv run --frozen python -m unittest discover -s tests -v`. Include the
   actual commands, outcomes and missing environments in the pull request.
6. For behavioral claims, use the [evaluation protocol](evaluations/README.md):
   matched fresh contexts, exact prompts/responses, exposed model/host metadata,
   fixed rubric, side effects and limitations. Structural checks cannot establish
   behavioral benefit. Keep old records tied to their evaluated revisions.
7. Request review with scope, resulting behavior, evidence, risks and open issues.
   The lifecycle reaches NEEDS_REVIEW before VERIFIED. A reviewer decides applicable
   gates using APPROVED, REJECTED, BLOCKED or justified NOT_APPLICABLE.

For fast **local** feedback before the full suite, use the [read-only impact planner](docs/impact-testing.md).
It suggests tests from changed files but does not run them or replace CI.

Maintainers assess correctness, safety, scope, compatibility, context cost,
licensing and evidence. No contribution is accepted automatically. Do not weaken
checks to hide a failure or claim untested platforms. External issue updates,
merges, publication and contributor messages require actual repository authority
and relevant authorization. See the issue templates for minimum useful reports.
