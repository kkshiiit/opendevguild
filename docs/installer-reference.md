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

Dry-run validates the proposed operation and prints every destination write,
removal and backup file, its source when relevant, and the manifest path. It
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

Rollback reverses the most recent operation for each selected skill. It can restore
an uninstalled skill, revert an update, or undo an initial installation. The inverse
is itself retained as history, so another rollback reverses the last rollback.
Snapshots are hash checked before restoration. A tampered snapshot is rejected.

State lives at `<target-parent>/.opendevguild-state/<target-path-hash>/`:
`manifest.json` stores managed hashes, directories, source versions and history;
`backups/<snapshot-id>/` stores prior skill bytes. Keeping it outside the discovery
directory prevents old SKILL.md copies becoming accidentally discovered skills.
Uninstall retains this history to support rollback. Do not delete it until its
contents and retention needs have been reviewed.

This is a local convenience tool, not a permission boundary or crash-safe package
manager. Do not run concurrent installers or edit managed files during an operation.
Backups preserve prior data, but abrupt interruption, disk failure or an external
writer can require manual recovery after inspecting the manifest and snapshots.
The tool does not claim atomicity across a multi-skill filesystem operation.

## Executed tests

`python -m unittest discover -s tests -p test_installation.py -v` exercises an
actual checkout copy, synthetic version changes, dry-runs, collision preflight,
user-change preservation, unrelated skills, update/uninstall rollback, modified
backups, malformed/traversal state and source/destination symlinks. Initial tests
failed before implementation; fourteen methods passed after implementation.
Platform-specific runs are reported by hosted CI, not assumed from local tests.

Español: este instalador es opcional; copiar carpetas manualmente no requiere
Python. Indicá la carpeta de descubrimiento exacta, revisá `--dry-run` y seleccioná
una o dos skills. Los cambios del usuario bloquean actualización, desinstalación y
rollback en vez de sobrescribirse. Los backups se conservan fuera de descubrimiento.
Un fallo de disco o una edición concurrente puede requerir recuperación manual.

Manifest capacity is preflighted before any destination/backup mutation. Install
and update reserve the final history slot for uninstall; rollback reduces history
and remains available at capacity. Known macOS system aliases /var and /tmp are
canonicalized only to their standard /private targets; project symlinks stay
rejected. Abrupt disk failure/concurrent writers still require manual recovery.
