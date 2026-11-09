# Optional local installer reference

Manual folder copying is the primary installation route and needs no Python.
This optional tool uses Python3.11+ standard library only. It copies reviewed local
files; it never downloads, imports or executes a skill's code, enables agents,
changes global configuration or invokes a model. Client loading is a separate
verification step in the installation guides.

## Explicit destination and file plan

`--target` is the actual discovery directory, **not** a project root. For current
documented Codex repository discovery it is `<project>/.agents/skills`.
No target is chosen implicitly; personal installation is only an explicit choice
of that user's documented discovery directory. `--source` defaults to this checkout.

```text
python scripts/install.py install --source /path/to/opendevguild --target /path/to/project/.agents/skills --skill mission-control --skill scope-guardian --dry-run
python scripts/install.py install --source /path/to/opendevguild --target /path/to/project/.agents/skills --skill mission-control --skill scope-guardian
```

These are Python argument examples; substitute real paths and use the appropriate
Python launcher for your system. The CLI does not depend on Bash. The automated
test suite invokes it with the active interpreter and native temporary paths.
Do not claim a client or OS run solely because this portable syntax parses.

Dry-run validates the proposed operation and prints destination writes,
removals, backup/staging files, sources and manifest/journal paths. It
writes nothing. Backup identifiers are fresh for each invocation, so a later real
run can have different backup directory names than the preview.

Every selected source is inspected before any change. Existing unmanaged skill
directories are refused. Symlinks, path traversal, malformed state, missing
SKILL.md, duplicate identifiers and source/destination overlap are rejected. The
installer is bounded to1000 files/16MiB per skill, a4MiB manifest and50 historical
operations per skill. Reaching a budget blocks rather than pruning history.

## Managed update, uninstall and rollback

```text
python scripts/install.py update --source /path/to/reviewed-new-checkout --target /path/to/project/.agents/skills --skill mission-control --dry-run
python scripts/install.py update --source /path/to/reviewed-new-checkout --target /path/to/project/.agents/skills --skill mission-control
python scripts/install.py rollback --target /path/to/project/.agents/skills --skill mission-control --dry-run
python scripts/install.py rollback --target /path/to/project/.agents/skills --skill mission-control
python scripts/install.py uninstall --target /path/to/project/.agents/skills --skill mission-control --dry-run
python scripts/install.py uninstall --target /path/to/project/.agents/skills --skill mission-control
```

Updates keep previous bytes and source version metadata. Before update, uninstall
or rollback, the current complete file/directory inventory must match its managed
hashes. Modified, added, removed or symlinked entries block the operation. Preserve
your changes separately and reconcile them deliberately; do not edit the manifest
to bypass this guard. Unrelated skills and files are left alone.

Rollback consumes the most recent history record for each selected skill and
restores its previous state. It can restore an uninstalled skill, revert an update,
or undo an initial installation. Repeated rollback walks toward older history;
it does not toggle the last rollback or implement redo.
Snapshots are hash checked before restoration. A tampered snapshot is rejected.

State lives at `<target-parent>/.opendevguild-state/<target-path-hash>/`:
`manifest.json` stores managed hashes, directories, source versions and history;
`backups/<snapshot-id>/` stores prior skill bytes. Keeping it outside the discovery
directory prevents old SKILL.md copies becoming accidentally discovered skills.
Uninstall retains this history to support rollback. Do not delete it until its
contents and retention needs have been reviewed.

## Transaction failures and recovery

All selected replacements are copied into `transaction/staged/` and hash checked
before retiring any installed directory. The next manifest is written and checked
first. Originals are then renamed into the existing snapshot backup area, new
directories are promoted, and every selected destination/backup is checked again.
Atomic replacement of `manifest.json` is the commit point. There is no copy
fallback when a rename fails (for example, an open handle or cross-device move).

A recoverable error before commit compensates **the whole selected batch** by
renaming the originals back, keeping the previous manifest bytes unchanged.
If compensation also fails, originals remain in backups and `pending.json`
blocks install/update/uninstall/rollback. Partial cleanup cannot remove that marker
first. While pending, the stored manifest is recovery evidence, not an assertion
of a consistent installed batch; ordinary manifest loading is refused. After
fixing the I/O problem, inspect and recover the same target:

```text
python scripts/install.py recover --target /path/to/project/.agents/skills --dry-run
python scripts/install.py recover --target /path/to/project/.agents/skills
```

Recovery covers the recorded batch, not a subset selected by `--skill`. It validates
the target, bounded journal, names, snapshot IDs, prior state, reconstructed next
manifest and current files before moving anything. User edits, linked paths,
corrupt metadata or altered backups block recovery instead of being overwritten.
If the active manifest matches the committed batch, recovery only completes
cleanup; it does not undo that batch. A post-commit cleanup failure reports
`WARNING: batch committed; cleanup pending` and retains the marker. New data and
the new manifest remain active; the next ordinary operation stays blocked until
cleanup succeeds. An error reported after successful manifest publication is
reconciled against observed disk state and reported as committed, with a warning.
Recovery dry-run lists the selected skills, compensation directory moves and
generated cleanup paths without changing files.

The journal is outside discovery and bounded to twice the 4 MiB manifest budget
plus 64 KiB. Preparing it never enlarges the existing per-skill/history limits.
Staging needs additional free disk space. A failed first install can be retried
after successful compensation; harmless empty generated parent directories may
remain. Journals/manifests are local unsigned records, not proof against a party
that can rewrite the entire installer state. Do not edit them to grant authority.

This is not a crash-safe package manager, concurrent-writer lock or power-loss
durability guarantee. Do not run concurrent installers or edit managed data during
an operation. The tests inject normal I/O errors and a synthetic Python process
interruption; they do not test real power cuts, filesystem corruption, every
filesystem or hostile races. If a process stops, the pending marker can support
recovery **only while the journal, backups and manifest remain intact and agree**.
Multi-directory moves have visible intermediate states; readers are not isolated.

If recovery refuses, stop writers and preserve copies of both the target and
the entire state directory outside skill discovery. Inspect the recorded hashes,
backup inventories and user changes before selecting a consistent pre-commit or
committed state. Keep conflicting user files separately; never delete originals,
clear the pending marker or rewrite the manifest merely to bypass the guard.
Damaged/partially written journal or persistent I/O failures require reviewed
manual recovery; the command deliberately refuses to guess.

## Executed tests

`python -m unittest discover -s tests -p test_installation.py -v` exercises an
actual checkout copy, synthetic version changes, dry-runs, collision preflight,
user-change preservation, unrelated skills, update/uninstall rollback, modified
backups, malformed/traversal state and source/destination symlinks. Cycle 4 adds
copy/write/rename/publication/restoration/cleanup fault injection, four-action
multi-skill compensation, explicit recovery, journal corruption, user edits and
first-install retry. Six regressions failed on the original destructive path.
Platform-specific runs are reported by hosted CI, not assumed from local tests.

Español: este instalador es opcional; copiar carpetas manualmente no requiere
Python. Indicá la carpeta de descubrimiento exacta, revisá `--dry-run` y seleccioná
una o dos skills. Los cambios del usuario bloquean actualización, desinstalación y
rollback en vez de sobrescribirse. Los backups se conservan fuera de descubrimiento.
Consultá la recuperación detallada abajo; no hay garantía ante cortes eléctricos
ni escritores concurrentes.

Manifest capacity is preflighted before any destination/backup mutation. Install
and update reserve the final history slot for uninstall; rollback reduces history
and remains available at capacity. Known macOS system aliases /var and /tmp are
canonicalized only to their standard /private targets; project symlinks stay
rejected. Windows junctions are rejected where the Python runtime exposes them.

## Recuperación y límites

El instalador prepara y verifica todas las copias y el nuevo manifiesto antes de
retirar una skill. Renombra los originales a backups; publica las carpetas nuevas
y finalmente reemplaza el manifiesto. Si falla antes de ese commit, intenta
restaurar **todo el lote** mediante renombrado y conserva los bytes del manifiesto
anterior. Rollback consume el último registro: repetirlo recorre estados anteriores,
no vuelve a aplicar automáticamente lo que se acaba de deshacer.

Si también falla la restauración, conserva originales y `pending.json` y bloquea
las operaciones normales. Corregí el problema de E/S y ejecutá, con tu ruta real:

```text
python scripts/install.py recover --target /ruta/proyecto/.agents/skills --dry-run
python scripts/install.py recover --target /ruta/proyecto/.agents/skills
```

Recupera el lote registrado completo, no una selección de skills. Antes de mover
valida estado, nombres, hashes y backups; cambios del usuario o metadatos alterados
lo bloquean. Si el commit ya ocurrió y solo falló la limpieza, informa una
advertencia, conserva el manifiesto/datos nuevos y `recover` termina únicamente
la limpieza. El marcador pendiente se retira al final. No lo borres para continuar.
Mientras está pendiente, el manifiesto guardado sirve como evidencia de recuperación,
no afirma que el lote instalado sea consistente; su carga normal queda bloqueada.
El dry-run enumera skills, movimientos de compensación y rutas de limpieza.

La preparación necesita espacio adicional. Se conservan límites por skill,
historial y manifiesto; el journal admite hasta dos veces 4 MiB más 64 KiB.
Las pruebas inyectan errores de E/S e interrupción sintética de Python: no prueban
cortes eléctricos reales, corrupción del disco, todos los sistemas de archivos
ni carreras hostiles. No ejecutes instaladores concurrentes ni edites archivos
durante una operación. No hay aislamiento para lectores entre renombrados.

Si `recover` rechaza la recuperación, detené escrituras y preservá copias del
destino y del estado completo fuera del descubrimiento. Revisá hashes, originales
y cambios del usuario antes de elegir un estado consistente. Separá los archivos
en conflicto; no elimines originales ni edites manifiestos para eludir controles.
Un journal incompleto/corrupto o errores persistentes requieren recuperación manual
revisada. El estado no está firmado; no autentica cambios maliciosos de quien puede
reescribirlo entero. La release 0.4.0 conserva su comportamiento original: estas
correcciones corresponden al código posterior en main.
