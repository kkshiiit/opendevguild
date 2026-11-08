# Web example: scoped form layout correction

This recipe targets an existing local web project. It contains no browser fixture
or completed screenshot test. Use a synthetic account and the current UI stack.

## Objective and scope

On the account-settings form, prevent long validation messages from overlapping
the Save button at a 320 CSS-pixel viewport and 200% text zoom. Keep existing
field validation, request payload, save behavior, navigation and visual identity.
The scope is this form's styles/markup and directly relevant tests; no global
redesign, dependency upgrade or framework replacement.

## Selected skills and sequence

1. repository-intelligence locates the form, styles, error rendering, API calls
   and actual browser/test commands. Record the starting dirty diff.
2. frontend-engineer reproduces the narrow layout and makes the smallest scoped
   correction using current components and CSS conventions.
3. accessibility-engineer checks the affected labels, focus, reflow and announced
   errors. code-review-engineer compares the final diff and observed behavior.
   A simple existing browser regression belongs with the same owner; add
   qa-automation-engineer only if test infrastructure work is actually needed.

## Copyable request

```text
$frontend-engineer Task WEB-FORM-1: correct overlapping validation text and the
Save button in the existing account-settings form at 320 CSS pixels and 200%
text zoom. Preserve current validation, payload, save/navigation behavior, colors
and framework. Scope edits to the form and relevant tests; preserve dirty work.
Use FAST unless investigation shows higher risk. Check long labels, errors,
keyboard focus and one wider viewport with the existing tools. Report exact
observations and not_run checks; do not redesign other screens or deploy.
```

## Expected results and controls

Return a minimal reproduction using a long synthetic message, a bounded
markup/style patch and an appropriate browser or component regression. At narrow
and wider widths, content reflows without overlap, clipped messages or hidden
controls; focus remains visible and field errors stay associated with controls.
Check empty, invalid, pending, recoverable-failure and success states as applicable.
Verify unchanged request payload and duplicate-submit behavior with the existing
fixture. Compare before/after under the same content, viewport and zoom.

Requirements states the layout acceptance precisely. Architecture and Release
may be NOT_APPLICABLE with explicit local-only reasons. Implementation checks the
scoped diff; Verification records actual browser observations and relevant tests;
Security checks that no sensitive data or authorization logic changed. A successful
build cannot approve browser behavior. Independent review supports VERIFIED;
a missing required browser check remains BLOCKED rather than an inferred pass.

## Limitations

No complete WCAG conformance claim follows from the affected-flow checks. Browser
coverage must name real versions/viewports, and a screenshot alone does not prove
functional preservation. Unavailable rendering is not replaced by a fabricated
image. The example does not authorize external account access or deployment.

Español: corregí únicamente el solapamiento del formulario a 320 píxeles CSS y
200% de zoom. Conservá validaciones, payload, guardado y navegación. Probá texto
largo, errores, foco y un ancho mayor con datos sintéticos. Documentá resultados
reales; la compilación o una captura no bastan para verificar funcionamiento.
