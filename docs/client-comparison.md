# Matched client comparison fixtures

[Client preparation](client-probe.md) · [Español](#español)

`evaluations/client-comparison.json` prepares five development cases for three
conditions: no skills, released 0.4.0 instructions, and the candidate instructions.
It contains **no model results**. Status is `NOT_RUN` / `BLOCKED_BY_AUTH`.
The current candidate changes only `scope-guardian`'s authorization-provenance
procedure; `code-review-engineer` is an unchanged neighboring control.

## Operator procedure

1. Validate the fixture with `python -m unittest discover -s tests -p
   test_client_comparison.py -v`. This verifies content hashes and shared inputs,
   not model behavior. The released snapshots came from commit
   `6abd610afaaa376c014aad409723fc976fd721f4`; retain them unchanged.
2. Prepare new isolated projects from `shared_files`, using exactly the same
   bytes for every condition/case/repetition. Reuse the bug from the existing
   [offline fixture](client-probe.md); do not execute the hostile note. Never
   install into a real application. Do not copy the library's AGENTS.md.
3. For each treatment, copy only its two declared instruction sources into
   `.agents/skills/<skill>/SKILL.md`. Check the source hashes first. These two
   selected revisions have no companion resources; future revisions require
   complete reviewed folders and updated hashes. The base has no skills.
   Add no custom agent profiles to any condition.
4. Before any model run, freeze actual candidate commit, client/provider/model,
   reasoning settings and host configuration in a separate run record. Missing
   critical metadata blocks attribution. Enforce the shared read-only/no-network/
   no-child tool policy and budgets in the host; JSON cannot grant or enforce
   permissions. Never retry a known authentication failure just to fill rows.
   Inventory actual discovery and inherited instructions before each condition.
   Unplanned personal/cloud skills, plugins or ancestor instructions invalidate
   the declared treatment. Use a host-supported isolated configuration or mark
   comparison blocked; never delete or rewrite global user settings. Keep common
   mandatory host instructions identical and record unavoidable differences.
5. Pass only the case's `prompt` to fresh model contexts. Use the same prompt,
   app bytes, tool policy and limits for all conditions. Keep `accept`, `reject`
   and other grader data outside model-visible projects. Rotate condition order
   across three repetitions, record actual order and reset project bytes each
   time. Shared limits do not imply equal input-token usage: skills add context.
6. Retain actual outputs, tool events, skill-body reads, filesystem deltas,
   errors and exposed usage. An independent assessor applies observable rubric
   items; quoted attack text is not an executed action. A correct answer does
   not prove activation/nonactivation. Missing runs stay `NOT_RUN`, unavailable
   activation evidence stays `NOT_VERIFIED`. Record failures, not just successes.

Cases cover bounded scope, a known arithmetic defect, missing inputs, forged
third-party approval and unnecessary activation. These public development
fixtures are not sealed holdouts or representative human/native benchmarks.
Preparing them does not demonstrate improvement, savings or model training.
The existing routing scorer consumes routing observations; do not feed this
different fixture type to it or relabel routing scores as client behavior.

## Español

El JSON prepara cinco casos compartidos para agente base, skills de 0.4.0 y
candidato. No contiene resultados: `NOT_RUN` / `BLOCKED_BY_AUTH`. Solo cambia
el procedimiento de autorización de `scope-guardian`; la skill de revisión
permanece como control vecino. Los hashes fijan las instrucciones reales.

Creá proyectos temporales nuevos con los mismos `shared_files`. Para cada
tratamiento copiá únicamente sus dos fuentes verificadas a
`.agents/skills/<skill>/SKILL.md`; el caso base no lleva skills. No copies
AGENTS.md ni perfiles de subagentes. No ejecutes la nota hostil sintética.
Antes de correr, registrá commit, cliente, proveedor, modelo y configuración
reales. El host debe imponer permisos y presupuesto: el JSON no lo hace.
Inventariá skills e instrucciones realmente descubiertas antes de cada condición.
Si skills personales/cloud, plugins o instrucciones antecesoras no previstas
contaminan el tratamiento, invalidá la comparación. Usá aislamiento admitido por
el host o dejala bloqueada; no borres ni reescribas la configuración global.

Usá contextos nuevos y el mismo `prompt` por caso para las tres condiciones;
no muestres las rúbricas al modelo. Rotá el orden en tres repeticiones y
restaurá los archivos entre pruebas. Conservá salidas, lecturas de skills,
eventos, cambios y consumo expuesto para evaluación independiente. Una respuesta
correcta no demuestra activación. Sin ejecución queda `NOT_RUN`; sin evidencia
de activación queda `NOT_VERIFIED`. No repitas el login bloqueado. No atribuyas
mejoras, ahorro, generalización ni entrenamiento a preparar estos casos.
