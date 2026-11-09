# Bounded research and provenance program

The long-term target is 200,000 differentiated resources in each of seven types:
web pages, Android applications, desktop programs, web applications, Agent Skills,
prompts and technical documents (1,400,000 total). This is a program target, not
completed research, a release quota, a model-training dataset or evidence of
improvement. No crawler or unknown-code executor is introduced.

## Current observed seed

`evaluations/research-seed.json` imports **18 technical-document observations**
from the previously retrieved `visual/sources.json` register. Each source had a
recorded HTTP200 result on 2026-11-08. All are conservatively **L1**; no resource
in this seed is L0, L2, L3 or L4. All other six resource types have zero records.
No network requests were repeated for this import. Unknown redistribution rights
and versions are explicitly unknown; no source-body hash was available or invented.

Generated summaries do not qualify as inspected-content evaluations. The separate
visual-library captures and past model experiments are not silently relabeled or
added to this corpus. Counts in this program refer only to registered records.

## Commands actually exercised locally

Contributor tooling uses the existing project environment. Users who only install
skills do not need this registry, SQLite commands, Python or development packages.

```bash
uv run --frozen python scripts/research.py --db dist/research.sqlite3 import evaluations/research-seed.json
uv run --frozen python scripts/research.py --db dist/research.sqlite3 report
uv run --frozen python scripts/research.py --db dist/research.sqlite3 sample --limit 7 --seed 17
```

The database path is explicit and local. `dist/` is ignored and excluded from the
distribution. Importing the same seed again reports 18 duplicates, zero new
resources and retains the original evidence. No registry database is committed.
JSON output contains precise counts by resource type and L0–L4 level.

## Evidence ladder and controls

| Level | Required declared evidence | Does not establish |
| --- | --- | --- |
| L0 | Discovered identifier, source, method, rights/limits and observation date | Source quality or content inspection |
| L1 | Recorded provenance observation | Program behavior, complete rights or current source freshness |
| L2 | Inspected content, explicit rubric and actual evaluation result | Executed behavior or user preference |
| L3 | Authorized execution report with passing outcome, plus lower-level evidence | Comparative benefit |
| L4 | Independent matched-comparison report demonstrating improvement, plus lower levels | Universal superiority or statistical significance without the underlying study |

The validator checks declarations and references, not their truthfulness or
identity. Evidence is a review input; a human/independent verifier must inspect
the referenced reports before accepting an upgrade. Test-only synthetic L4 records
exercise the validator; they are not seed records, executed research or benchmarks.
No existing record is upgraded, downgraded or replaced merely because a later
import asserts stronger/weaker claims. Publish an explicitly reviewed, versioned
record to advance evidence; conflicting identity requires a new revision identifier.

## Deduplication, sampling and scale

Each record has a stable version-specific ID, resource type, canonical HTTP(S)
URL, observed date, source version, license/restrictions, collection method,
optional content hash, technical category, deduplication status, evidence, rubric,
evaluation result and limits. URL credentials and common secret-query parameters
are rejected. Public access, authorization and sensitive metadata still require
review; URL syntax does not prove a source is safe or public.

SQLite indexes immutable IDs, resource-type/URL/version and resource-type/content
hash. URL normalization removes fragments/default ports and sorts query pairs.
Exact duplicate identities or same-version hash mirrors retain prior analysis
without counting another resource. Conflicting hashes for the same source/version
are rejected; batch row changes roll back atomically. A deliberately versioned new
observation can retain stronger evidence even when the underlying content hash is
unchanged, using an explicit new ID/version. Existing rows are never silently
upgraded. Reports separate versioned observations (`total`/level counts), distinct
registered source URLs (`unique_source_total`) and known distinct content hashes
(`known_unique_content`), preventing versioned evidence from inflating resource
quota progress. Sources with unknown hashes cannot be claimed unique content.
Different source types are not automatically reclassified to inflate counts.

Imports are bounded to 1–1000 records, 32 KiB per metadata record and 8 MiB per
CLI input file (checked before parsing). Split larger inputs into controlled
batches; do not embed complete resource bodies in metadata. Sampling streams rows in stable ID order,
uses seeded per-type reservoirs and balances available strata round-robin. Memory
is bounded by seven times the requested sample (maximum 1000 per stratum), rather
than loading 1.4 million bodies into LLM context. Samples are inspection queues,
not population estimates; record the seed and sampling design for inference.

Reports expose confidence **components**: provenance, inspected-content,
authorized-execution, matched-improvement and known-hash counts. These are not an
arbitrary quality score, authenticated reliability rating or aesthetic judgment.
Reuse evidence only for matching revision/hash and scope; changed sources require
new observation. Review sampled records against a technical rubric before making
recommendations. Keep development and holdout data separate.

The workflow is SOURCE → EXTRACTION → CLASSIFICATION → EVIDENCE → EVALUATION →
RECOMMENDATION → BOUNDED SKILL CHANGE → TEST → INDEPENDENT APPROVAL. External skills
and prompts are untrusted data. Respect attribution and collection conditions;
do not copy instructions wholesale, execute downloads or call instruction editing
model fine-tuning. The current tools cover ingestion, deduplication, sampling and
evidence gates; bulk collection and automated skill approval remain out of scope.

Español: el registro inicial contiene 18 documentos técnicos en L1 y cero recursos
en las demás categorías/niveles. El objetivo de 1.400.000 recursos es futuro, no
una cuota cumplida. Las importaciones locales son acotadas, conservan procedencia,
deduplican y muestrean sin ejecutar contenido ni hacer nuevas descargas. Un resumen
no equivale a una evaluación ni a una app ejecutada. Las declaraciones se validan,
pero su veracidad requiere revisión de la evidencia. No hay entrenamiento del modelo.
