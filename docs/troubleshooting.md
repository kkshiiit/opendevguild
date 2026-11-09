# Troubleshooting / Errores frecuentes

[Installation](installation.md) · [Instalación](installation.es.md) ·
[Client evidence](client-compatibility.md)

| Symptom / Síntoma | Check and safe action / Comprobación y acción |
| --- | --- |
| Skill missing / No aparece | Check the exact client path, the complete folder and matching SKILL.md. Open the target app and refresh/start a session. Codex `/skills`; Gemini `/skills list` then `/skills reload`; use only commands supported by that client. |
| Model repeats the name / Repite el nombre | Inspect discovery/source metadata; a plausible response alone does not prove loading. Do not label activation VERIFIED without it. |
| Nested ZIP / ZIP anidado | Extraction may add a repository wrapper folder. The target must be `<discovery>/<name>/SKILL.md`, not `<discovery>/opendevguild/skills/<name>/SKILL.md`. |
| Existing destination / Destino existente | Stop; identify ownership and edits. Back up outside discovery and compare before updating. Never overwrite or delete an unknown skill. |
| Duplicate skill / Skill duplicada | Check project, personal and plugin installs. Keep one intended source or resolve precedence explicitly; do not delete unrelated copies blindly. |
| Hidden folders / Carpetas ocultas | Enable hidden-file display; `.agents` and `.claude` begin with a dot. PowerShell uses explicit paths, not Bash heredocs. |
| Python missing / Falta Python | Manual skill use does not need it. Python/uv are only for optional installer and contributor validators; the AI client's own prerequisites still apply. |
| ChatGPT ignores local files / ChatGPT no ve la carpeta | Local filesystem discovery is not a ChatGPT install mechanism. Use its currently admitted plugin/workspace UI and account permissions. |
| Auth token expired / Token expirado | Use the client's normal sign-in flow. Do not post tokens in issues or copy credentials into this repository. The authoring Codex probe was blocked this way. |
| Unsupported profile / Perfil no soportado | Codex TOML profiles are not portable skills or universal agent definitions. Keep the skill procedure, omit unsupported profiles and use sequential execution. |
| Hash mismatch / Checksum distinto | Stop. Confirm ZIP and sidecar are from the same release, then re-download via the official release page. Do not edit the expected checksum to make it pass. |
| Browser/SDK missing / Falta navegador o SDK | Distinguish infrastructure checks from ordinary skill use. Install task-specific tooling only with appropriate authority; mark unexecuted target tests not_run. |
| No Termux path / Termux sin verificar | This release does not assert tested Android/Termux client installation. Do not treat a mobile-sized web capture as native Android evidence. |

For a useful issue include the client/version, OS, installation scope, selected
skill, sanitized folder layout, expected result and actual error. Exclude tokens,
private project code and personal data. Security reports follow
[SECURITY.md](../SECURITY.md).

Para reportar un error indicá cliente/versión, sistema, alcance de instalación,
skill y estructura de carpetas sin datos sensibles. Conservá cambios locales;
ninguna reparación de documentación exige resetear tu aplicación ni conceder
más permisos al agente.
