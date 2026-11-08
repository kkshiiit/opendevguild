# Visual Intelligence Engine V1

An optional extension to OpenDevGuild, preserving the original 34 specialists.
Eight visual procedures add reference analysis, art direction, color, typography,
material rendering, motion, implementation and independent visual QA. No new
permanent subagents are created. [Español](README.es.md).

## Architecture and evidence

The [source register](sources.json) records live technical research in W3C color
and WCAG, Apple SwiftUI, Android rendering, MDN, typography, perception/Gestalt,
information architecture, HCI, experimental design and Playwright. These sources
inform original procedures; their images and design systems are not bundled.
An attempted preference-testing article returned 404 and was excluded. Human
task evaluation and controlled paired comparison use the retrieved HCI/NIST
guidance; no aesthetic-learning result is inferred from those documents.

- `schemas/` defines reference, human-feedback and correction records.
- `data/development.json` has three actually inspected original reference entries.
- `data/evaluation.json` has one separate-source evaluation reference.
- `fixtures/` contains the original, self-contained HTML source.
- `artifacts/` contains real Chromium PNGs, a WebM recording and capture conditions.
- `antipatterns.json` has twelve contextual signals with evidence requirements,
  user-task impact and legitimate-use counterexamples. None is an absolute ban.
- `benchmarks.json` specifies Android/web/desktop/game cases and three comparison
  arms; all model/native comparisons are explicitly not_run.
- `data/feedback.json` and `data/corrections.json` are empty, validated logs awaiting
  real contributions. No invented human votes or promoted corrections are included.

The library validator checks inspection declarations, rights, artifact/source
hashes, paths and split disjointness. It cannot establish truthfulness or blind
independence. Current analysis is author/agent inspection, not human consensus.
The evaluation source is separate from development, but not a sealed independent
holdout: project authors can access it. Do not tune procedures on its observations.

## Run locally

Core checks need the standard environment; captures and pixel comparisons use the
optional `visual` group. Installing browser binaries is explicit:

```bash
uv sync --frozen --group visual
uv run --frozen playwright install chromium ffmpeg
uv run --frozen python scripts/visual.py validate
uv run --frozen python scripts/visual.py contrast '#536357' '#f5f3ed'
uv run --frozen python scripts/capture_visual.py --output dist/visual-run
uv run --frozen python scripts/visual.py diff visual/artifacts/direction-a-1360.png visual/artifacts/repeat-a.png
```

An existing capture destination is refused, preserving goldens. In this managed
environment, Chromium blocks file-URL navigation: the tool loads our self-contained
HTML via `set_content`, without disabling browser policy or requesting remote data.
Local execution used `--chromium /usr/bin/chromium`; other hosts can use the
Playwright-managed binary. Do not compare goldens across changed browser, OS,
font, viewport, device scale, theme, state or timing without a reviewed baseline.

The pixel tool counts exact RGBA changes and rejects different dimensions. It is
informational: a difference is not inherently a defect, and zero difference does
not establish usability or accessibility. Contrast accepts opaque six-digit sRGB
after composition; it does not treat OKLCH lightness or an uncomposited alpha
value as relative luminance. Use existing browser/color tooling to resolve other
spaces and real backgrounds before measurement.

## Materials

| Classification | Evidence required | Allowed claim |
| --- | --- | --- |
| stylized_glass | Real captures over relevant backgrounds, readability and fallback | Alpha, backdrop blur and graphic highlights |
| simulated_dynamic_glass | Captures plus recording/source-response checks, sampling/displacement model and measured cost | A documented simulation; approximations named |
| native_official | Actual official Apple API on supported Apple SDK/OS, real target evidence and accessibility settings | Native Apple Liquid Glass for that verified target |

The web fixture implements the first two classes. Canvas displacement is an
illustrative approximation, not a physical Fresnel/refraction renderer. Android
RenderEffect (API31+) and AGSL RuntimeShader (Android13+) are distinct mechanisms;
verify target availability. Neither web nor Android may claim native Apple Liquid
Glass. Native Apple examples remain procedural until actually executed there.
Code inspection alone cannot approve material fidelity. CPU draw-call timing is
not GPU presentation, mobile energy use or real-device frame performance.

## Human feedback and validated correction

Use pseudonymous reviewer IDs and consent. Show alternatives with the same task
and conditions, randomize/counterbalance presentation order, conceal authorship
when possible and retain ties, neither, rationale and disagreement. Separate task
errors and accessibility evidence from preference. No arbitrary beauty score is
a definitive quality gate.

```bash
uv run --frozen python scripts/visual.py check-feedback /path/to/human-feedback.json
uv run --frozen python scripts/visual.py check-correction /path/to/correction.json
```

Use the schemas to prepare records. Human alternatives reference known library IDs
(for example `field-editorial-a` and `field-card-b`). A correction records original
design, problem, proposed change, rationale, later result, evaluation and regression.
Promotion eligibility requires independent review, development-only provenance,
actual result artifact paths/hashes and passed regression. The command validates
and reports; it does not rewrite rules or promote opinions automatically. A
maintainer reviews the resulting evidence and commits a bounded procedural change.
This is versioned procedural knowledge, **not model fine-tuning**.

## Integration and limits

Mission Control selects only the needed visual purposes. A small color task does
not load all evaluators. Important art directions get separate visual QA; an art
director cannot independently approve its own proposal. Core UX, UI, accessibility,
frontend/mobile, performance and skill evaluation retain their responsibilities.
Use the existing designer/implementer/reviewer profiles; profile syntax is tested,
but native Codex CLI loading is blocked by expired authentication in this session.

See [results](results.md) for actual measurements and [comparison protocol](BENCHMARKS.md)
for unexecuted three-arm studies. Human preferences, wide-gamut hardware, screen
readers, real mobile energy, native Apple/Android, game runtime and matched agent
benchmarks remain unverified. No aesthetic superiority claim is supported.
