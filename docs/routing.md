# Deterministic specialist routing / Enrutamiento determinista

`scripts/routing.py` selects a small, ordered set of responsibilities from **explicit
caller-classified triage**. It does not parse the meaning of arbitrary requests,
load skills, spawn agents, run tools or publish anything. A human or host agent
must first interpret the request, establish authorization and classify the inputs.
Bad classifications remain a limitation; this procedure is not a semantic classifier.

## Input and decision policy

Call `route(triage) -> dict` from Python, or pass one JSON object to:

```bash
python scripts/routing.py /absolute/path/to/triage.json
```

The ten required classification dimensions are:

| Dimension | Accepted values and effect |
| --- | --- |
| `product` | `general`, `web`, `backend`, `mobile`, `desktop`, `game`, `data`, `library`, `unknown`; platform-specific needs require a matching product |
| `task` | `analyze`, `plan`, `design`, `implement`, `review`, `test`, `operate`, `release`, `evaluate`, `maintain`, `investigate`, `discover`, `unknown`; unknown tasks require clarification |
| `risk` | `low`, `medium`, `high`; high risk selects CRITICAL controls |
| `complexity` | `simple`, `medium`, `complex`; affects resource mode |
| `stack` | Object with nonempty `name` and boolean `confirmed`; code changes require confirmed repository evidence |
| `dependencies` | Array of unique `{ "id": "policy", "status": "ready" }` records; `unresolved` blocks dependent selection |
| `tools` | Explicit available capabilities: `repository_read`, `file_write`, `test_runner`, `subagents`, `browser`, `network`; names describe host observations and grant no powers |
| `research` | `none`, `repository`, `external`, `user`; selects relevant investigation and checks required capability availability |
| `changes` | `none`, `code`, `docs`, `config`; nonempty changes require read/write capability, code needs a confirmed stack |
| `verification` | Boolean indicating requested executable verification; requires `test_runner`, adds relevant change review for code/config changes |

An additional required `needs` array supplies **at most six unique domain purposes**.
This is the bounded specialty assessment supplied by the caller, not a keyword
match against raw request text. Supported values map directly to the corresponding
catalog responsibilities:

```text
coordinate scope repository delivery product requirements ux ui accessibility
architecture adr database api frontend backend mobile desktop game-design gameplay
implementation review test-strategy test-automation performance security privacy
supply-chain ci release observability incident documentation skill-evaluation community
```

Optional `ambiguities` is an array of up to ten nonempty unresolved questions.
Unknown fields, malformed types, unsupported values, duplicate needs/dependencies
and missing dimensions are rejected with an error. A valid object with unresolved
information produces a **blocked recommendation**, rather than an invalid-input error.

Example triage for a small, already scoped frontend fix:

```json
{
  "product": "web",
  "task": "implement",
  "risk": "low",
  "complexity": "simple",
  "stack": {"name": "Detected existing TypeScript frontend", "confirmed": true},
  "dependencies": [],
  "tools": ["repository_read", "file_write", "test_runner"],
  "research": "none",
  "changes": "code",
  "verification": false,
  "needs": ["frontend"],
  "ambiguities": []
}
```

`verification: false` avoids selecting an additional verification specialist; it
does not remove the selected skill's own verification obligations. Capability
presence is an input assertion, not an executed environment probe.

## Resource modes and sequencing

- **FAST:** low risk, simple work, at most one explicit need; sequential execution.
- **STANDARD:** remaining non-high-risk work; selected specialists and relevant review.
- **CRITICAL:** high declared risk; security controls precede dependent implementation.
  Code/configuration changes, implementation work or an explicit code-review need
  get code review. Non-code work gets scope/authorization verification rather than
  an unrelated code review. CRITICAL never authorizes dangerous actions.

All recommendations currently use `execution: sequential`. Independent review is
an ordered responsibility; this script does not promise a separate execution context.
The host decides actual delegation and must label self-review when appropriate.

The output uses planning `readiness: ready|blocked`, separate from collaboration lifecycle status. It includes `mode`, `selected` skills with reasons, ordered
`stages`, `missing_inputs` and limitations. Stage order covers coordination,
scope/containment, investigation, planning, design/risk controls, implementation,
automation, review, operations and documentation. Dependencies supplied here are
readiness gates; this small procedure does not invent a distributed scheduler.

If scope is ambiguous, a dependency is unresolved, implementation stack is
unconfirmed or required capability is unavailable, only a minimal investigation
is selected: repository analysis when reading is available, requirements
clarification otherwise. The original work stays blocked. No all-34 activation
or assumed browser, emulator, signing, network or subagent capability occurs.

See the [measured routing evaluation procedure](evaluation-runner.md). Its 170
fixtures test this policy under explicit triage, **not host natural-language
discovery or the behavioral quality of skill execution**.

## Español

Este procedimiento recibe una clasificación explícita del solicitante: producto,
tarea, riesgo, complejidad, stack confirmado, dependencias, herramientas disponibles,
investigación, cambios y verificación. `needs` limita la selección a seis
responsabilidades identificadas; no interpreta automáticamente lenguaje natural.
El comando anterior solamente lee JSON y devuelve una recomendación.

FAST corresponde a trabajo simple y de bajo riesgo; STANDARD cubre el resto del
trabajo ordinario; CRITICAL agrega controles justificados por riesgo alto. Todos
los planes son secuenciales. Las ambigüedades, dependencias pendientes o capacidades
ausentes bloquean la tarea y seleccionan una investigación mínima. Ningún modo
otorga permisos ni ejecuta cambios. Las métricas de fixtures deterministas no
demuestran activación semántica ni eficacia comparativa de las skills.
