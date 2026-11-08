# Desktop example: compatibility and packaging assessment

This recipe assesses an existing desktop application; it is not a bundled
installer or evidence of Windows, Linux or macOS execution.

## Objective and scope

Determine whether the current application can produce a per-user package for
its declared Windows, Linux and macOS targets. Identify actual supported OS and
CPU versions, packaging commands, storage locations, update/signing prerequisites
and gaps. Produce at most an unsigned local package for the available host using
the existing tooling. No system-wide installation, publication, signing-key
creation, production update or toolkit migration is authorized.

## Selected skills and sequence

1. repository-intelligence reads manifests, native adapters, release scripts and
   documented platform requirements without executing unknown installers.
2. desktop-engineer maps shared/platform code, data paths, permissions, install
   scope, file associations, update authenticity and stored-state compatibility.
3. release-engineer reviews package identity, checksums, installation/recovery
   criteria and the distinction between local build and published artifacts.
4. code-review-engineer checks the evidence matrix and any bounded script fix.
   Add security review only for a concrete privileged/update trust concern.

## Copyable request

```text
$desktop-engineer Task DESKTOP-PACKAGE-1: assess this local application's declared
Windows/Linux/macOS compatibility and per-user packaging with its existing stack.
Find actual OS/CPU support, build commands, data paths and signing/update needs.
Use STANDARD. You may create an unsigned package for the available host in a new
local output path after inspecting the build script. Do not install system-wide,
sign, publish, change global settings or overwrite user data. Return an OS/CPU
matrix separating source inspection, build, install and runtime evidence; mark
unavailable targets not_run and propose the smallest gap-closing steps.
```

## Expected results and controls

Deliver a table per OS/architecture with declared minimum version, toolchain,
package format, storage permissions, signing/notarization requirements where
applicable, and exact observed versus unexecuted checks. If a local package is
built, retain its source revision, command, artifact path and checksum. Inspect
contents for secrets and workspace files. Distinguish unsigned, signed,
installed, launched, upgraded and publicly released states.

In a disposable user-data target, where supported and authorized, exercise first
launch, denied/read-only storage, interrupted save and close/reopen. Describe
upgrade/rollback compatibility and preservation of user data; do not run an
installer destructively to satisfy the checklist. Other platforms remain
unexecuted, not supported by inference from the available host.

Requirements and Architecture assess the intended packaging scope and existing
platform strategy. Implementation may be NOT_APPLICABLE for a read-only report.
Verification reflects actual observations; Security reviews package provenance
and permissions. Release evaluates local package readiness only, with public
publication separately NOT_APPLICABLE or BLOCKED according to the requested task.
Independent review is required before lifecycle VERIFIED.

## Limitations

Signing, notarization and store rules depend on the actual distribution channel
and current platform documentation. An unsupported host/SDK blocks that target's
claim. This recipe does not authorize an account, certificate, package manager,
update feed or remote release. Do not advertise all three platforms from one build.

Español: analizá compatibilidad y empaquetado por sistema y arquitectura. Separá
inspección, build, instalación, ejecución, firma y publicación. Generá solamente
el paquete local autorizado; preservá datos y configuración. Las plataformas sin
herramientas quedan sin probar y no heredan compatibilidad de otro sistema.
