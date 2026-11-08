# Custom-agent configuration and verification

The eight requested roles live in the repository's `.codex/agents/` directory.
They are **Codex agent profiles**, separate from the portable Agent Skills in
`skills/`. The profiles contain only the currently documented mandatory fields:
`name`, `description`, and `developer_instructions`. They do not configure a
model, tool server, sandbox, approval policy, credentials or provider.

| Profile | Bounded responsibility |
| --- | --- |
| `architect` | Architecture alternatives, interfaces and consequential decisions |
| `product-analyst` | Product assumptions, requirements and scope traceability |
| `designer` | UX/UI, interaction states, design consistency and accessibility |
| `implementer` | Small changes in the detected project/platform stack |
| `reviewer` | Independent correctness, evidence and scope review |
| `qa-specialist` | Risk-based tests and regression evidence |
| `security-specialist` | Authorized security, privacy and dependency review |
| `release-specialist` | Build/release gates, artifact integrity and publication readiness |

Each profile supplies an objective, responsibilities, optional recommended skills,
limits, result contract, delegation conditions and completion criteria. Skill
names are recommendations, not load directives. A role activates only applicable
available skills; an absent skill is reported as a limitation. This avoids making
all 34 skills mandatory for every task or installing 34 permanent agents.

The result contract has 13 fields: TASK ID, OBJECTIVE, SCOPE, INPUTS, ASSUMPTIONS,
DEPENDENCIES, FILES INVOLVED, ACTION TAKEN, EVIDENCE, TESTS, RISKS, OPEN ISSUES,
STATUS. Lifecycle values are `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`,
`NEEDS_REVIEW`, `VERIFIED`, `FAILED`. Author checks end at `NEEDS_REVIEW`;
independent review of the required evidence precedes an orchestrator-confirmed
`VERIFIED` transition. Tool outcomes and inspection judgments are labeled
separately. A confident self-review is not independent verification.

Delegation requires actual host support, permission from the assigned task and a
clear benefit within the worker/time/context budget. Child tasks carry input and
acceptance requirements and explicit read/write ownership. Dependent work and
shared writes run sequentially. Profiles inherit the main session's permissions;
these instructions do not create an isolated filesystem or stronger sandbox.
Sequential execution retains the same criteria when subagents are unavailable.

## Verified checks

On 2026-11-08, the attached environment reported `codex-cli 0.167.0-alpha.4`.
`codex exec --help` confirmed these actual flags: `--ephemeral`,
`--ignore-user-config`, `--sandbox read-only`, `--json`, and `-C`/`--cd`.
`--ignore-user-config` skips the user configuration file; authentication still
uses the host's normal mechanism. No secret files or authentication values were
read for this check and no global configuration was changed.

The following local static check ran successfully:

```bash
uv run --frozen python -m unittest discover -s tests -p test_agents.py -v
```

Four tests check the exact requested role set, TOML parsing and mandatory field
set, the 13-field/lifecycle contract, and real/selective recommended skill names.
The tests first failed when the profiles did not exist and passed after they
were created. These checks detect configuration omissions and unsupported
permission overrides; they do **not** prove that a client loaded the roles or
that a subagent behaves correctly.

## Bounded client-loading probe

Static configuration syntax and actual runtime loading are distinct results.
A loading probe has not yet been recorded in this document. The coordinating
agent may run one bounded read-only client session and append its observed
result. Do not run multiple model sessions merely to repeat a successful load.

From the repository root, after confirming the local client supports the flags:

```bash
codex exec --ephemeral --ignore-user-config --sandbox read-only --json -C . \
  'Report the custom-agent names and descriptions exposed by your actual delegation interface. Do not read profile files to substitute for runtime discovery, do not spawn children, do not modify files, and do not inspect credentials or use external services. If custom roles are not exposed, report that limitation. Do not claim child execution.'
```

This command invokes the configured model service and therefore is an integration
probe, not an offline test. It must use the main session's authorized environment
and ordinary authentication without reading credential values. A result showing
loaded custom names establishes discovery in that client/session only. It does
not establish child execution, permission isolation, useful parallelism, every
role's behavior or compatibility with other client versions. If the model cannot
inspect loaded role names, retain that uncertainty rather than replacing it with
a file read and calling it runtime verification.

For a later child-execution test, use an authorized disposable fixture, one
read-only task, a concrete expected artifact/observation, a bounded worker budget
and independent evidence review. Record the actual child/tool result separately
from a model's assertion that it spawned a role.

## Español

Los ocho perfiles de `.codex/agents/` son configuraciones de agentes de Codex;
las skills portables se distribuyen por separado. Las pruebas TOML comprueban
estructura y contratos, pero no demuestran carga ni ejecución real. Cada agente
hereda los permisos de la sesión principal, carga sólo las skills pertinentes y
requiere una revisión independiente antes de declarar `VERIFIED`. Si el entorno
no admite subagentes, el mismo procedimiento se ejecuta en secuencia. Una prueba
real del cliente debe registrar su resultado y sus límites sin leer secretos ni
modificar la configuración global.
