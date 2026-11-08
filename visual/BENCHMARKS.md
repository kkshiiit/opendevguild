# Three-arm comparison protocol

Register task, fixture revision, allowed tools, host/model, context/time budget,
platform/SDK/device, font/render conditions, acceptance criteria and scoring before
running an arm. Conditions: base agent; OpenDevGuild core only; core plus selected
Visual Intelligence procedures. Preserve failures and all outputs. Repetitions,
randomization and task blocks are required for comparative inference.

| Target | Reproducible task | Acceptance and measurements | Current execution |
| --- | --- | --- | --- |
| Web | Implement the same visit-booking content and local confirmation behavior, with two distinct directions | Keyboard/form behavior, no overflow at 390/1360px, stated contrast criteria, component consistency, real captures, timing and human pairs | Authored fixture rendered; model arms not_run |
| Android | In an authorized detected-stack fixture, implement a local offline visit list and readable reconnect state | Lifecycle/offline tests, text scaling, touch/reader checks, Android version guards, device frame/energy measurements, screenshots/recording | not_run: no native fixture/device execution supplied |
| Desktop | Implement local maintenance settings with keyboard-first operation and enlarged text | Focus, persistence, platform-specific packaging, theme/scaling captures and startup/resource measurements | A separate web holdout exists; native desktop arms not_run |
| Game | Implement a pause menu over a deterministic moving scene with low-motion fallback | Input/state preservation, readable HUD/menu, engine-specific frame timings, source-sampled material behavior and player task checks | not_run: no engine runtime supplied |

For native cases, supply an authorized minimal platform/engine fixture and lock its
revision before running any arm. Do not silently substitute a mobile web viewport
for Android or HTML for desktop-native/game execution. Current JSON scenario IDs
and requirements are executable study inputs once those capabilities are provided;
they are not fabricated native results.

For each result, report correctness, failed tests, confirmed visual defects with
regions, accessibility/performance findings and scope changes. Record wall time,
tools and token usage only where exposed. Gather actual blinded paired human
preferences under matched task conditions; include rationale, ties, neither and
participant/task variability. Do not merge these dimensions into an arbitrary
beauty score. Human preference does not override functional or accessibility gates.

Keep development and evaluation sources separate. Do not tune rules on evaluation
records. Archive original directions and corrections with identity and regression
evidence. The initial dataset is tiny, authored and accessible to project authors;
it cannot support broad independent comparisons. No three-arm result or human
rating is currently present in `benchmarks.json`.

Español: los escenarios preparan comparaciones, no las dan por ejecutadas. Antes
de cada brazo fijá tarea, entorno, herramientas y criterios; conservá fallos y
compará condiciones equivalentes. No sustituyas plataformas nativas por un viewport
web ni inventes preferencias, tokens o mejoras.
