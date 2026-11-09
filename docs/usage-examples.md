# Copyable task examples / Ejemplos copiables

[English quick start](quickstart.md) · [Uso rápido](quickstart.es.md) ·
[Installation](installation.md) · [Instalación](installation.es.md)

These prompts target an application supplied by the user, not OpenDevGuild's own
installation. Replace paths and facts. Codex uses `$name`; Claude Code documents
`/name`; Gemini selection differs—see the [matrix](client-compatibility.md).
No example asserts that its fictional app, SDK or tests have already run.

## 1. Bounded bug fix / Bug acotado

Skill: implementation-engineer. Supply reproduction, relevant source/tests and
existing dirty changes. Expect a small compatible diff, reproduction and outcomes;
verify focused regression plus scope preservation. Missing repository access
blocks implementation; deployment is outside this prompt.

```text
$implementation-engineer Fix duplicate submission only in src/orders and its tests.
Preserve the uncommitted login redesign. Reproduce first, use the current stack,
run relevant tests and return changed paths and actual results. Do not deploy.
```

```text
$implementation-engineer Corregí solo pedidos duplicados en src/orders y sus tests.
Conservá el rediseño de login sin confirmar. Reproducí, respetá el stack y ejecutá
las pruebas pertinentes. Informá rutas y resultados reales. No despliegues.
```

## 2. Code or PR review / Revisión de código o PR

Skill: code-review-engineer. Supply authorized PR/diff or file and acceptance
criteria. Expect severity, location, evidence and recommendations. Reproduce
suspected defects when safe; distinguish static findings from unexecuted tests.
Access to a PR is not inferred and the prompt does not authorize comments or merge.

```text
$code-review-engineer Review the supplied src/checkout.py diff without editing.
Focus on retries, resource authorization and failure recovery. Report justified
findings with locations/evidence and list checks not run. Do not comment or merge.
```

```text
$code-review-engineer Revisá el diff suministrado de src/checkout.py sin editar.
Priorizá reintentos, autorización y recuperación. Fundamentá severidad, ubicación
y recomendación; distinguí tests no ejecutados. No comentes ni fusiones el PR.
```

## 3. Visual directions / Diseño sin validación humana inventada

Skill: visual-art-director. Supply task, current rendered UI, rights-cleared
references and target platforms. Expect two differentiated hypotheses, real
capture conditions and separate-review request. Check keyboard/contrast/layout
and measured performance; human preference remains unknown until humans respond.

```text
$visual-art-director Propose two booking-screen directions using the supplied
content and inspected references. Preserve accessibility and explain tradeoffs.
Render if tools exist; do not invent human preference or self-approve the winner.
```

```text
$visual-art-director Proponé dos direcciones para reservas con el contenido y las
referencias inspeccionadas. Conservá accesibilidad y justificá alternativas.
Renderizá si hay herramientas; no inventes preferencias ni te autoapruebes.
```

## 4. Android plan / Planificar Android

Skill: mobile-engineer. Supply repository/manifests, minimum targets, offline
policy and feature criteria. Expect detected stack, lifecycle/offline/test plan
and missing SDK/device checks. Verify available builds/tests separately; a plan
and mobile web screenshot are not native Android verification.

```text
$mobile-engineer Plan offline bookmarks in this Android repository. Detect the
stack and supported versions first. Cover lifecycle, sync, permissions and tests.
Do not implement yet; mark unavailable emulator/device/signing checks explicitly.
```

```text
$mobile-engineer Planificá marcadores offline en este repositorio Android. Detectá
stack y versiones antes. Cubrí ciclo de vida, sync, permisos y pruebas. No
implementes todavía; declará checks de emulador/dispositivo/firma no disponibles.
```

## 5. Backend tests / Tests de backend

Skill: qa-automation-engineer. Supply endpoint contract, existing runner and
synthetic isolated fixtures. Expect reproducible positive/negative tests and
actual outcomes. Verify assertions catch the known failure; do not weaken tests
to hide product defects or point destructive fixtures at production.

```text
$qa-automation-engineer Add tests for the existing task endpoint: validation,
authorization, duplicate requests and dependency failure. Use the existing runner
and isolated synthetic fixtures. Run them and preserve failures; do not deploy.
```

```text
$qa-automation-engineer Agregá tests del endpoint existente: validación,
autorización, duplicados y fallo de dependencias. Usá el runner actual y fixtures
sintéticos aislados. Ejecutalos y conservá fallos; no despliegues.
```

## 6. Security and licenses / Seguridad y licencias

Start with security-engineer for an authorized trust-boundary review, then request
supply-chain-auditor only for actual dependency/license questions. Supply diff,
data flow, lockfile and use/distribution context. Expect evidence-based risks,
license inventory and uncertainty. Run authorized scanners if available; neither
technical review nor dependency metadata automatically establishes legal compliance.

```text
$security-engineer Review this authorized upload flow and dependency lockfile.
Use read-only checks; never print secrets or run unknown install scripts. Identify
trust-boundary risks and hand concrete license questions to supply-chain-auditor.
Do not claim legal compliance or perform intrusive remote testing.
```

```text
$security-engineer Revisá el flujo de subida y lockfile autorizados, en solo
lectura. No muestres secretos ni ejecutes instaladores desconocidos. Identificá
riesgos y derivá dudas de licencia concretas a supply-chain-auditor. No prometas
cumplimiento legal ni hagas pruebas intrusivas sobre sistemas externos.
```

## 7. Release preparation / Preparar una release

Skill: release-engineer. Supply intended version, exact revision, supported
platforms, release gates and destination. Expect changelog, artifact manifest,
checksums, install evidence and rollback. Verify two-build identity and actual
remote publication separately; missing authority blocks upload.

```text
$release-engineer Prepare a candidate from this revision. Run required checks,
build a reproducible ZIP and checksum, verify installation and document rollback.
Do not upload until the actual owner/destination and publication authority exist.
Report prepared, uploaded and remotely verified states separately.
```

```text
$release-engineer Prepará un candidato desde esta revisión. Ejecutá controles,
generá ZIP reproducible y checksum, verificá instalación y documentá rollback.
No subas nada sin destino y autoridad reales; separá preparado, subido y verificado.
```

## 8. Complex mission / Misión compleja

Skill: mission-control. Supply objective, scope, constraints, budget and test
criteria. Expect minimal specialist selection, dependencies, ownership and
consolidated evidence. Verify combined behavior after independent work; no two
workers should silently edit the same files. CRITICAL does not grant extra access.

```text
$mission-control Add account export within src/export and tests/export. Preserve
existing contracts and user edits. Classify risk; select only relevant specialists,
assign disjoint writes, serialize dependencies and obtain independent review.
Do not access production or publish. Return checks, gates, risks and next action.
```

```text
$mission-control Agregá exportación de cuenta solo en src/export y tests/export.
Conservá contratos y cambios del usuario. Clasificá riesgo, seleccioná especialistas
pertinentes, separá escrituras, ordená dependencias y pedí revisión independiente.
No accedas a producción ni publiques. Informá checks, gates, riesgos y siguiente paso.
```
