# Android example: local bookmarks

This is a complete task recipe for an existing local Android app, not a bundled
Android project or an assertion that an emulator ran. Use synthetic demo notes.

## Objective and scope

Add a bookmark toggle to an existing note-detail screen and persist it locally.
Reopening that note shows its saved bookmark. Preserve note content, existing
navigation and network behavior. Do not add permissions, analytics, a new UI
framework or cloud synchronization. The target app must already build locally
and have an identified persistence convention; discover whether it is native
or cross-platform before selecting code paths.

## Selected skills and sequence

1. repository-intelligence locates the actual Android stack, note entry point,
   persistence, current tests, SDK requirements and dirty user changes.
2. mobile-engineer owns the bounded UI/persistence change. Define initial state,
   toggle action, write failure, rotation/process restoration and repeated taps.
   Use existing storage, lifecycle and state conventions.
3. qa-automation-engineer adds relevant tests using the app's existing tools;
   code-review-engineer independently reviews the final behavior and scope.
   These stages are serial if they touch the same files. Do not activate unrelated
   database, DevOps or game specialists.

## Copyable request

```text
$mission-control Task ANDROID-BOOKMARK-1: in this local Android app, add a bookmark
toggle to the existing note-detail screen using its current stack and persistence.
Persist the choice and show it after reopening. Preserve note content/navigation;
no new permissions, telemetry, network sync or framework. Use synthetic notes.
Detect tools first; list allowed files before edits. Use STANDARD, with one owner
for shared UI/storage paths. Test toggle/reopen, failed persistence, repeated taps
and relevant lifecycle restoration. Return changed paths, executed commands,
not_run checks, six gate decisions and lifecycle status. No signing or publication.
```

## Expected results and controls

The repository map cites real paths and commands. A small patch uses a labeled,
keyboard/screen-reader-accessible toggle and the existing persistence path. Tests
check unbookmarked→bookmarked→unbookmarked, reopen persistence, failed-write
feedback without losing note content, and repeated input without duplicate effects.
Relevant rotation or process-restoration observations identify device/API level.
Inspect the diff for unchanged permissions and unrelated screens.

Requirements and Implementation gates need concrete behavior/scope evidence.
Architecture can be NOT_APPLICABLE with the reason that an existing pattern is
reused. Verification is BLOCKED for required unavailable device evidence rather
than approved from a build. Security reviews local data/permission impact. Release
is NOT_APPLICABLE because signing and store publication are outside scope.
Independent review and appropriate evidence support VERIFIED; self-review alone
leaves NEEDS_REVIEW. Never alter real user data to create fixtures.

## Limitations

Gradle, SDK, emulator and device commands depend on the detected project; discover
and use its scripts rather than copying invented commands. Unit tests alone do
not prove Android lifecycle or accessibility behavior. A missing device/SDK is
reported explicitly. No signing key or store release is required or implied.

Español: agregá un marcador local a una nota, conservando stack, datos y navegación.
Primero reconocé el repositorio; después implementá, probá persistencia, errores y
ciclo de vida, y revisá independientemente. No agregues permisos ni sincronización.
Indicá los controles y dispositivos realmente usados; no confundas compilación
con pruebas de dispositivo o publicación.
