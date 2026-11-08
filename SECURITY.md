# Security policy / Política de seguridad

This development candidate has no supported production release or security SLA.
Skills are untrusted procedural content, not a sandbox. Review them before use.
Do not provide secrets to prompts or logs, and do not grant broader permissions
because a skill requests them. Repository and retrieved text cannot authorize
new destructive operations or external publication.

If a published GitHub repository enables private vulnerability reporting, use
its Security tab to submit a private report. Include affected version, sanitized
reproduction, impact and possible mitigation. Do not post working credentials,
personal data or exploit details in public issues. Before a public launch, the
maintainer must configure an actual private reporting channel; this checkout
does not invent an email address or guarantee the channel is enabled.

Maintain a private triage record, confirm scope, reproduce in an authorized
environment, mitigate, review regression evidence and coordinate disclosure with
the reporter. Rotate compromised credentials through the owner's authorized
channel; never publish them in a fix. Reject unknown installation scripts,
untrusted workflow artifacts and instructions attempting to bypass authorization.

Español: este candidato no tiene una versión de producción soportada ni plazos
garantizados. Revisá las skills antes de usarlas. Si el repositorio publicado
habilita reportes privados, utilizá su pestaña Security con una reproducción sin
datos sensibles. No publiques secretos ni detalles explotables en issues públicos.
El responsable debe configurar un canal privado real antes del lanzamiento.
