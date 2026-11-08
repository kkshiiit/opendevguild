# Governance

OpenDevGuild is an independent community project distributed under Apache-2.0.
References to vendors and platforms describe compatibility; they imply no
endorsement, affiliation or delegated authority.

## Authority and responsibilities

The actual repository owner designates maintainers and grants repository access.
Agent role files do not appoint people, create legal authority or confer merge,
release, infrastructure or spending permissions. Do not invent maintainers or
public contact addresses before they exist.

Contributors propose bounded changes with evidence. Maintainers triage scope,
compatibility, safety, licensing and maintenance cost. Reviewers assess changes
against explicit acceptance criteria; an implementer's completion report does not
replace review. A release owner verifies publication destination and required
gates. For security-sensitive changes, use an appropriate independent reviewer
where available and disclose self-review limitations when it is not.

## Decisions

Use an issue or pull request to state the problem, options, consequences,
evidence and proposed owner. Prefer a small compatible correction over an
unrequested redesign. Consequential architectural or public-contract decisions
use ADRs with alternatives and rationale; trivial edits need no ADR.

Record disagreement and seek a decision from the responsible maintainer. There
is no assumed voting quorum, automatic consensus or guarantee of acceptance.
Policy changes require explicit maintainer review and must retain the project's
safety and evidence requirements. Exceptions identify scope, rationale, authority,
risks and verification; they do not silently waive failed checks.

## Review and release controls

Tasks use NOT_STARTED, IN_PROGRESS, BLOCKED, NEEDS_REVIEW, VERIFIED and FAILED.
Requirements, Architecture, Implementation, Verification, Security and Release
gates use APPROVED, REJECTED, BLOCKED or justified NOT_APPLICABLE. Missing evidence
never approves a gate. FAST, STANDARD and CRITICAL select proportionate work;
CRITICAL grants no extra privilege.

Before merge, review original/licensed content, relevant tests, scope, migration
needs, compatibility and documentation. Configure repository protections and
required checks according to actual hosting capabilities. Before public launch,
establish maintainer identities and a working confidential vulnerability-reporting
path under [SECURITY.md](SECURITY.md). Keep embargoed reports private.

A public release needs an authorized owner/destination, reviewed source revision,
required gate evidence, accurate supported-platform claims, package integrity,
installation guidance, release notes and recovery instructions. A GitHub release
and a public plugin listing require separate observed publication evidence.
Never force-push public history or overwrite a remote to bypass a dispute.

## Conduct, access and continuity

Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Collect only contributor data
needed for project operations. Do not publish reporter identities or private
correspondence without authorization. Grant minimum repository permissions;
reassess access when responsibility changes. If maintenance capacity disappears,
document the state and available migration options rather than promising support.

Español: la autoridad surge del dueño y mantenedores reales del repositorio,
no de los nombres de agentes. Los aportes requieren revisión y evidencia; los
cambios importantes documentan alternativas y consecuencias. Publicar necesita
destino autorizado, gates pertinentes, responsables y un canal privado de
seguridad. No hay aceptación automática, afiliación comercial ni soporte
prometido sin capacidad real.
