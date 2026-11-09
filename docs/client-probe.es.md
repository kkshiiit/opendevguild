# Entorno reproducible para probar Codex

[English](client-probe.md) · [Verificación de agentes](agent-verification.md)

Para comparar base/sin skills, versión publicada y candidato, usá el
[protocolo de casos equivalentes](client-comparison.md#español). Reutiliza el
defecto sintético y separa las comprobaciones offline de resultados de modelos.

Esta herramienta **prepara un entorno aislado y comprueba su integridad**, pero no
evalúa todavía el comportamiento del modelo. Es útil mientras Codex CLI remoto
falla con HTTP 401.

Desde la raíz del repositorio OpenDevGuild, elegí una carpeta **nueva**:

    python scripts/client_probe.py prepare --output /tmp/odg-smoke-001
    python scripts/client_probe.py check --fixture /tmp/odg-smoke-001

En Windows PowerShell usá una ruta nueva como $env:TEMP\odg-smoke-001.
El programa no sobrescribe carpetas existentes.
Rechaza enlaces simbólicos en cualquier antecesor del origen, destino y entorno,
y junctions de Windows cuando Python permite identificarlos. Admite únicamente
los alias del sistema macOS `/var` → `/private/var` y `/tmp` → `/private/tmp`.
Los enlaces agregados, incluso rotos, cuentan como cambios. Estos controles
suponen una carpeta local sin escrituras concurrentes; no son un sandbox del SO.

Antes de crear el destino, valida todos los archivos: máximo 1.000 archivos,
1 MiB por archivo, 16 MiB de contenido, 2.000 entradas del entorno (incluidas
carpetas) y 256 KiB de JSON del manifiesto. Recorre como máximo 2.000 entradas
por skill de origen, sin seguir enlaces ni junctions. Rechaza archivos especiales
(como FIFO), claves JSON duplicadas y manifiestos que no sean objetos.
Las rutas relativas admiten hasta 32 componentes y 4.096 bytes UTF-8.
La comprobación aplica los mismos límites. Una entrada inválida o excesiva devuelve
`ERROR` estructurado y código 2; cambios de bytes/archivos o enlaces agregados, `CHANGED` y
código 1; bytes registrados sin cambios, código 0. Un fallo de escritura puede
dejar un entorno nuevo incompleto: revisalo y elegí otra ruta.

Crea dos skills completas (scope-guardian y code-review-engineer) en
.agents/skills, el perfil opcional reviewer en .codex/agents, un archivo Python
con un error intencional, tres casos en scenarios.json y hashes SHA-256 en
manifest.json. No llama modelos, no lee credenciales, no se conecta a Internet
ni cambia configuraciones globales.

## Cuando funcione el login

1. Comprobá que una solicitud real e inofensiva al modelo responda. Una sesión
   guardada no prueba que la autenticación funcione.
2. Abrí una sesión nueva **de solo lectura** con la carpeta de prueba como
   directorio de trabajo. Consultá codex exec --help; el CLI observado aceptaba
   --ephemeral, --ignore-user-config, --sandbox read-only, --json y -C.
3. Consultá /skills o la capacidad real skills/list y conservá los eventos de
   descubrimiento. Copiar archivos no demuestra que Codex los haya cargado.
4. Ejecutá A y B de scenarios.json en contextos separados. C es opcional para
   comprobar activaciones innecesarias. Conservá respuestas y eventos reales.
5. Ejecutá check nuevamente. Si detecta archivos modificados, investigalos;
   archivos intactos no demuestran que la skill funcione.
6. Probá el subagente reviewer solo si el cliente realmente lo permite.

Un HTTP 401 es **BLOCKED: authentication**, no un fallo de la skill. Si hay
respuesta del modelo pero no evidencia de activación, dejá la activación
**NO VERIFICADA**. Que el modelo diga que usó una skill no es prueba suficiente.

Revisá que los registros no contengan secretos antes de compartirlos.
El manifiesto no está firmado: solamente comprueba consistencia de archivos.
El entorno es sintético, no una aplicación de producción. Codex Desktop y CLI
remoto pueden tener configuraciones y sesiones diferentes. Preparar el entorno
no demuestra ahorro de tokens ni mejora de calidad.
