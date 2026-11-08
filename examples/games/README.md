# Game example: a bounded dash mechanic

This is a complete design-to-test recipe for an existing local game project,
not a bundled engine demo or an executed playtest. Detect the actual engine and
version; do not assume Godot, Unity, Unreal or a particular language.

## Objective and scope

Prototype a dash for the existing player character: while grounded or airborne,
a valid dash input moves in the latest non-zero facing direction for 0.15 seconds,
then starts a 0.8-second cooldown. Ignore new dash inputs during dash/cooldown.
Collisions still block motion. Pausing freezes dash/cooldown time; death or scene
reset clears transient dash state. Values are prototype hypotheses, not validated
balance. Preserve ordinary movement outside the dash, saves and network behavior;
multiplayer is outside scope unless already essential to the local architecture.

## Selected skills and sequence

1. repository-intelligence identifies engine/version, player ownership, physics
   timing, input, scene reset and available test/export commands.
2. game-design-engineer writes the short mechanic/state specification, feedback,
   tuning hypothesis and a small consent-aware playtest plan. Resolve conflict
   with existing game rules before implementation.
3. gameplay-engineer implements the agreed mechanic using current physics/input
   abstractions and a disposable scene/save fixture. Do not replace the engine.
4. qa-automation-engineer prepares behavior checks in the existing framework;
   code-review-engineer independently checks timing, collision and scope.
   Add performance-engineer only if measured cost warrants investigation.

## Copyable request

```text
$mission-control Task GAME-DASH-1: prototype dash in this existing local game.
Detect engine/version and preserve normal movement, saves and unrelated assets.
Dash uses latest non-zero facing, lasts 0.15 seconds, then has 0.8 seconds cooldown;
ignore repeated dash input until ready, respect collisions, freeze timers on pause,
and clear transient state on death/scene reset. Values are design hypotheses.
Use STANDARD. Specify rules first, then implement in the current stack and test
30/60/144 FPS, repeated inputs, pause/reset and collision behavior where tooling
allows. No live economy, multiplayer service, engine migration or publication.
Report exact observations, not_run checks, gates and a bounded playtest plan.
```

## Expected results and controls

Return a concise design document, explicit ready/dashing/cooldown transitions,
small engine-native patch and executable behavior tests or a repeatable manual
protocol when automation is unavailable. Check dash duration/cooldown within the
engine's stated simulation-step tolerance at representative frame rates; do not
invent a zero-error timing guarantee. Check input without a prior facing update,
wall collision, held/repeated input, pause/resume, death and scene reload. Preserve
baseline ordinary movement and save behavior. Use controlled seeds where relevant
and document remaining nondeterminism.

Requirements resolves rules and tolerance. Architecture justifies reuse of current
player/state boundaries. Implementation checks scoped scripts/scenes/assets.
Verification requires actual behavior evidence; editor launch alone is insufficient.
Security considers untrusted assets and protected data; Release is NOT_APPLICABLE
for this local prototype. Independent review and applicable gate evidence support
VERIFIED for engineering behavior, not proof of fun, balance or retention benefit.

The playtest plan specifies tasks, representative participant criteria, consent,
observed completion/control errors, qualitative questions and a revise/retain rule.
No participant finding is reported until testing actually occurs.

## Limitations

Engine editor, target SDK, input device and profiling availability vary. Mark
unavailable checks not_run and block claims that depend on them. A local prototype
says nothing about network authority or production performance. Do not change a
live game, collect personal player data or delete saves to create test conditions.

Español: diseñá primero las reglas de dash y sus estados; implementá después en
el motor detectado. Probá tiempos, colisiones, entradas repetidas, pausa y reinicio,
con tolerancia explícita y herramientas existentes. Los valores son hipótesis de
balance; la corrección técnica no demuestra diversión ni resultados de playtesting.
