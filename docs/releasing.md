# Release procedure / Procedimiento de versiones

A local candidate, installed package, GitHub release and accepted public plugin
are separate states. Use an actual authorized owner/destination; do not create an
organization, publish a repository or submit a plugin as a side effect of packaging.
The user-authorized destination is [kkshiiit/opendevguild](https://github.com/kkshiiit/opendevguild),
an existing repository. Its actual visibility, push/release and CI evidence must
be recorded after execution; naming the target here does not publish it.

1. Review the complete [requirements](requirements.md), current
   [verification gaps](verification.md), intended support claims and release owner.
   Classify the work FAST, STANDARD or CRITICAL by risk, not desired publicity.
2. Keep versions aligned in pyproject.toml, plugin.json, catalog.json, README
   examples and changelog. The earlier 0.2.0 candidate changed provisional exchange
   conventions to the complete lifecycle and gate contract. Preserve 0.1.0 history;
   do not reinterpret its old handoffs as new-format VERIFIED results. Document
   migration and refresh the lockfile intentionally when metadata/dependencies change.
3. Check the candidate source revision and starting Git state. Run documented
   validation and the full relevant suite from a reviewed checkout. Run affected
   routing, functional, defensive security, regression and integration cases.
   Comparative claims additionally require matched controls and sufficient repeated
   observations. Retain failed/unexecuted checks and exact evidence.
4. Record Requirements, Architecture, Implementation, Verification, Security and
   Release gate decisions. Allowed values: APPROVED, REJECTED, BLOCKED,
   NOT_APPLICABLE with a reason. Missing evidence blocks a relevant gate. Independent
   review and inspectable evidence are required for lifecycle VERIFIED; self-review
   alone leaves NEEDS_REVIEW. A release preparation task can be VERIFIED while the
   distinct public publication task remains BLOCKED.
5. Build a new artifact path using the documented command:

   ```bash
   uv run --frozen python scripts/guild.py package --output dist/opendevguild-0.4.1.zip
   ```

   Repeat to a second new path and compare ZIP SHA-256 values. Inspect names,
   source revision, contents, notices and sensitive-data exclusions. A checksum
   detects changed bytes, not publisher identity. Sign only through an authorized
   available identity; do not imply a signature exists when none was produced.
6. Exercise installation and a representative task from the artifact in an
   isolated target. Verify collision refusal, selected skill discovery and retained
   local modifications during update/uninstall. Test each claimed platform/client
   or narrow the claim; one host's tests do not establish universal compatibility.
7. For this authorized release use only the existing public kkshiiit/opendevguild
   repository. Do not change visibility, create alternatives or replace history. Set
   maintainers, a confidential security-report path and appropriate review controls.
   Use the [official source-import guide](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github).
8. Create the intended remote/release only when authorized for the concrete reviewed
   content. Record actual branch, tag, commit, URL, remote CI run and artifact
   identities. Keep local results distinct from hosted CI. Do not force-push,
   overwrite an existing remote or infer a destination from an accessible account.
9. If a public plugin listing is requested, use the
   [official submission process](https://developers.openai.com/plugins/deploy/submission).
   Record actual platform review and publication outcomes. A GitHub release or
   local installation does not prove acceptance into a public directory.

Rollback uses the previous reviewed tag/archive. Preserve local edits and move
only the owned OpenDevGuild directories outside discovery before restoring a
reviewed version. Agent profiles are separate; never reset application changes
or rewrite global configuration. For a bad public release, document impact and
remediation; retain prior evidence and avoid rewriting history to conceal it.

Español: revisá requisitos y evidencia reales, mantené versiones coherentes y
registrá los seis gates. VERIFIED necesita revisión independiente; una tarea de
preparación puede verificarse aunque publicar siga bloqueado. Generá artefactos
nuevos, comprobá contenido, hashes e instalación y limitá el soporte a lo probado.
Publicar requiere dueño, destino y autorización reales. Conservá versiones y
cambios locales para volver atrás sin borrar trabajo de la aplicación.

## Maintenance prerelease 0.4.1

Base: `b4bbb18523afd4be83937572c04457925cb95961`, including merged PRs #3–#9.
Scope: aligned release metadata/lock, current EN/ES download/recovery guidance,
changelog, notes and a separate publisher. Existing 0.4.0 tags, notes, workflow,
artifacts and historical verification records must remain unchanged.

Acceptance: full official/project/profile/visual validation, lint, unittest and
source/dependency audit; independent review; green PR and merged-main CI;
two byte-identical archives from the frozen source; extracted inventory and
installer fault/recovery tests; actual anonymous downloads with native checks on
Linux, Windows and macOS; public documentation URLs and preserved 0.4.0 identity.
Real model/client/child activation is `NOT_RUN` / `BLOCKED_BY_AUTH`, not a gate
silently approved by filesystem tests. No remote login retry is required.

After reviewing/merging and observing main CI, create a NEW annotated `v0.4.1`
tag at that exact commit, rebuild from its clean export and record the ZIP hash.
Dispatch the new workflow **from the tag**, supplying the actual values:

```text
gh workflow run publish-v0.4.1.yml --repo kkshiiit/opendevguild --ref v0.4.1 -f source_sha=REVIEWED_40_HEX_COMMIT -f archive_sha256=VERIFIED_64_HEX_SHA256
```

The placeholders must be replaced; invalid values fail closed. The publisher
requires the dispatch/tag/source commit to agree, successful main CI for that
SHA, matching versions, two equal builds and the independently supplied hash.
Both code and release notes come from the explicit reviewed commit. Publication
uploads only the ZIP and checksum as a new prerelease; it never clobbers assets.
Repository-token publication does not trigger another release-event workflow,
so three explicit native jobs download anonymously and compare the expected hash.
Record their actual results in the GitHub release; planned links are not evidence.

Español: esta versión empaqueta realmente las correcciones de main. Congelá el
commit aprobado, creá un tag nuevo y reconstruí desde ese tag. Ejecutá el workflow
desde `v0.4.1` con SHA y hash reales; verifica las descargas sin sesión y los tres
jobs nativos antes de declarar PUBLICADA. Conservá íntegra la versión anterior.
