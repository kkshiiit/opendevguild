# V1 executed results and limits

Date: 2026-11-08. This is a development implementation with real rendered
evidence, not an independent aesthetic benchmark or a trained model.

## Observed evidence

Original HTML fixtures were loaded into actual Chromium 156.0.8078.79 using
Playwright. File-URL navigation was blocked by browser policy; self-contained
`set_content` rendering worked without disabling policy or accessing external
pages. The initial recording attempt lacked Playwright FFmpeg; the explicit
official browser-tool install resolved it. Partial runs were preserved outside
the distribution; only the completed capture is included.

The completed remeasurement took **5.029 seconds** on this machine. Conditions,
source/image hashes, browser/platform, fonts policy, viewports and observations
are in [capture.json](artifacts/capture.json). Captures include two directions at
1360px and 390px, a separate evaluation fixture, dark and interactive states,
styled glass and simulated sampled glass. The recording is
[material-motion.webm](artifacts/material-motion.webm).

| Observation | Actual result | What it establishes |
| --- | --- | --- |
| Horizontal overflow | None in four direction/viewport combinations | Those four layouts fit the tested viewport |
| Repeat capture | 0 / 1,871,360 exact RGBA pixels changed | Stable same-run capture under those conditions |
| Material response inside pane | 13,490 / 13,520 pixels changed in ROI [308,1080,208,65] | Source change visibly reaches the simulated pane |
| Frozen-pane negative experiment | 0 pane pixels changed while 49,936 surrounding pixels changed | The revised pane metric rejects the original full-page false positive |
| Local request interaction | Status changed; no external request sent | The supplied local form interaction executed |
| Reduced motion | Animation remained stopped | The tested preference path preserves a stable state |
| Recorded dynamics | 34 Canvas draw calls observed during recording phase | Actual updating occurred; not a GPU/energy benchmark |
| Selected text/control token pairs | Six ratios 5.752–14.480, threshold 4.5 | Those opaque sRGB pairs pass that threshold |
| Canvas draw-call timing | Median 0.100 ms over 32 samples | CPU API-call timing on this run only |

Token contrast pairs are a partial check, not complete rendered contrast analysis
over all backgrounds or full WCAG compliance. Keyboard evidence observes a focused
control, not a full assistive-technology evaluation. Pixel change is not physical
optical fidelity, usability or preference. Native targets and wide-gamut displays
were not exercised.

## Library and review

Four original references were actually opened with the image viewer: three
development entries and one separate-source evaluation entry. The narrow capture
was also inspected. Direction B's repeated cards are recorded as a **candidate**
antipattern with region, task context and a legitimate grouping counterexample;
no confirmed user penalty or AI authorship is inferred.

Independent read-only review found four validator/measurement gaps: schema bypass,
non-render/holdout correction evidence, surrounding-pixel contamination and native
API/platform mismatch. Regression tests cover the fixes. The reviewer reran all
**19 visual tests**, malformed input probes and the frozen-pane negative experiment;
no remaining blocker was reported within that scope. Full project tests and hosted
CI are reported in the [project verification record](../docs/verification.md).

The dependency scan then identified39 advisory entries affecting Pillow12.3.0.
The visual group was upgraded to Pillow13.0.0, all19 visual tests passed again,
and the installed44-package advisory scan reported zero known vulnerabilities.
Before/after scanner JSON is retained under evaluations/. No advisory was ignored
or suppressed to obtain that result. Current pixel measurements were rechecked
with the corrected decoder; capture timing remains the original run observation.

Human feedback and validated correction logs remain empty. No actual person has
provided a stored preference or approved a reusable correction. Schema validation
cannot authenticate a human or prove an observation truthful. Promotion remains a
reviewed procedural change, never automatic incorporation or model fine-tuning.

## Unexecuted comparisons

The four [three-arm scenarios](BENCHMARKS.md) are prepared. No matched three-arm implementation comparison, native Android/Apple/desktop/game run, blinded human
preference study, mobile battery measurement or model-token comparison was run.
The two authored web directions are engineering fixtures, not model-generated
benchmark arms. No improved aesthetics, superiority or token reduction is claimed.

Español: hay capturas, grabación y mediciones reales, con cuatro fallos de
validación corregidos mediante regresiones. No hay votos humanos ni correcciones
promovidas. Las comparaciones entre agentes y las pruebas nativas siguen sin
ejecutar. Ninguna medición de píxeles se presenta como una prueba de belleza.

## Bounded three-condition advisory sample

[Exact records](advisory-comparison.json) contain one fresh-context response each
for a base agent, current core UI guidance and core plus visual QA guidance. All
received the same two images and capture record; only assigned guidance/condition
wrappers differed. The three predeclared factual checks concerned unsupported
native Apple, Android performance and human-preference claims. All three
conditions rejected all three claims. Parent-agent manual scoring supports no
advantage, statistical inference or aesthetic conclusion. Captions already reveal
expected answers, and core guidance contains optional extension hooks that were
instructed not to be used. This is an advisory sanity check, not any of the four
implementation benchmarks, an independent human study or a quality ranking.
