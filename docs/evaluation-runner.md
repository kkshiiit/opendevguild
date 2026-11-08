# Routing evaluation runner / Ejecutor de evaluación de selección

`scripts/evaluate.py` scores **supplied measured predictions** against the expected
sets in [routing fixtures](../evaluations/routing.json). It never calls a model,
executes task text or substitutes expected answers for observations. Use
`evaluate(fixture, observations) -> dict`, or:

```bash
python scripts/evaluate.py /absolute/path/to/predictions.json --cases evaluations/routing.json
```

## Fixture and observation records

The compact fixture contains shared `defaults` plus 210 cases: positive, negative,
ambiguous, multiple-specialist and single-specialist cases for **each of 42 skills**.
Each case supplies `id`, `target`, `category`, a contextual `request`, triage overrides,
`expected`, `forbidden`, `mode` and `readiness`. Merge defaults and overrides before
calling the router. The request is explanatory data; the deterministic router does
not claim to understand it. Expected and forbidden sets are manually authored policy
expectations. Five multiple-specialist cases also exercise CRITICAL routing.

Observation format:

```json
{
  "kind": "deterministic-router",
  "predictions": [
    {
      "id": "frontend-engineer-single",
      "skills": ["frontend-engineer"],
      "mode": "FAST",
      "readiness": "ready"
    }
  ]
}
```

This single record illustrates the format; the default suite requires all 210
unique case IDs. `host-observations` is a second accepted provenance label for
actual recorded host selections. The evaluator does not attest that a caller's
label or observation is truthful. Preserve host/model, exact inputs, tool availability,
timestamps and original outputs separately when conducting host experiments.

Missing, duplicate or unknown case IDs, unknown/duplicate skill names, invalid
modes/readiness values and unsupported provenance labels are errors. Missing observations
are not counted as successes. No test of skill content execution is implied.

## Metrics

For every case, compare the predicted skill **set** with the expected set:

- True positives: selected and expected skills.
- Unnecessary activations: selected skills absent from the expected set.
- Missed activations: expected skills absent from the selection.
- Forbidden activations: selected skills explicitly excluded by the fixture.
- Selection precision: TP / (TP + unnecessary activations).
- Selection recall: TP / (TP + missed activations).
- Exact match: skill set, resource mode and ready/blocked planning readiness all match.

Precision/recall are micro-averages over skill decisions, not averages of case
scores. A zero denominator produces JSON `null`, never an invented perfect score.
Mismatches list extra, missing and forbidden skills plus mode/readiness agreement.
The CLI exits 1 for an invalid input or any mismatch and 0 for a fully matching
set. These metrics apply to the supplied cases; authored regression fixtures are
not a holdout benchmark and cannot support superiority claims.

## Reproduce deterministic measurements

From the repository root, capture predictions produced by the executable policy:

```bash
odg_predictions_path=$(mktemp)
python - "$odg_predictions_path" <<'PY'
import json
from pathlib import Path
import sys
sys.path.insert(0, 'scripts')
from routing import route

fixture = json.loads(Path('evaluations/routing.json').read_text())
records = []
for case in fixture['cases']:
    decision = route({**fixture['defaults'], **case['triage']})
    records.append({
        'id': case['id'],
        'skills': [item['skill'] for item in decision['selected']],
        'mode': decision['mode'],
        'readiness': decision['readiness'],
    })
Path(sys.argv[1]).write_text(json.dumps({
    'kind': 'deterministic-router', 'predictions': records
}, indent=2) + '\n')
PY
python scripts/evaluate.py "$odg_predictions_path" --cases evaluations/routing.json
```

This produces deterministic procedure observations only. The evaluator reads
them; it does not generate fake model responses. The unit suite exercises all
210 cases and additionally corrupts a prediction to prove that extra/missing
activations lower precision/recall and produce a mismatch:

```bash
uv run --frozen python -m unittest discover -s tests -p test_routing.py -v
```

## Español

El ejecutor compara predicciones observadas con 210 casos: cinco categorías de
activación por cada skill. Rechaza registros faltantes, duplicados o inválidos.
Mide coincidencias exactas, activaciones innecesarias, omisiones, selecciones
prohibidas, precisión y recuperación. Un denominador vacío devuelve `null`.

El ejemplo reproduce decisiones del procedimiento determinista sobre una
clasificación ya suministrada. No genera respuestas de modelos ni demuestra
comprensión de solicitudes libres, calidad funcional, ahorro de tokens o ventaja
comparativa. Las observaciones reales de un host deben conservar su evidencia y
contexto; el evaluador no certifica que los datos proporcionados sean verdaderos.
