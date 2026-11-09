# Plugin nativo para Claude Code

[English](claude-code.md) · [Compatibilidad](client-compatibility.md)

Este adaptador se incorpora **después de v0.4.1**. Usá el checkout que contiene
el cambio: el ZIP y tag publicados de 0.4.1 siguen intactos y no incluyen este
adaptador. No se publicó otra release ni se solicitó aprobación de un directorio.
Antes de fusionar, seleccioná la rama del PR `feat/claude-code-native-plugin`;
después, un checkout revisado de main. Descargar la release anterior no alcanza.

## Carga local

Necesitás tu propio Claude Code instalado y una sesión funcional. Codex CLI y su
autenticación no intervienen. Revisá el código y, desde una aplicación temporal,
usá la ruta absoluta del checkout:

```text
claude --version
claude plugin validate /ruta/absoluta/opendevguild
claude --plugin-dir /ruta/absoluta/opendevguild
```

El último comando carga el plugin para esa sesión: no registra un marketplace
global ni sobrescribe configuraciones. Si tu cliente lo admite, agregá `--strict`
a la validación para rechazar advertencias. Son comandos oficiales documentados,
**no pruebas ejecutadas aquí**: no hay ejecutable `claude` ni conector de Claude
disponible en este entorno. No se inventa una versión mínima compatible.

El manifiesto nativo es `.claude-plugin/plugin.json`. El `plugin.json` de la raíz
es otro formato y no se usa para Claude. Se reutiliza `skills/`, con las mismas
42 skills y sus referencias; no se duplican ni se cargan todos sus cuerpos a la
vez. No hacen falta copias manuales adicionales en `.claude/skills/`.

## Elegí una skill

En la sesión nueva, comprobá el inventario disponible y ejecutá:

```text
/opendevguild:scope-guardian Delimitá la corrección del cálculo de descuento en buggy.py. Solo buggy.py y sus pruebas focalizadas están dentro del alcance. Solo lectura: no edites, ejecutes comandos ni uses la red. Informá límites, exclusiones, aceptación y datos faltantes.
```

Las skills del plugin usan `/opendevguild:<nombre>`; las instaladas manualmente,
`/scope-guardian`. No son el mismo namespace. Esperá un informe basado en los
archivos suministrados, no una corrección automática. La afirmación del modelo
de haber usado una skill no prueba la lectura de sus instrucciones.

## Un revisor opcional

Se adapta únicamente `agents/reviewer.md`, con herramientas declaradas `Read`,
`Grep` y `Glob`, modelo heredado y sin precargar skills. Para una revisión
independiente justificada, suministrá objetivo, archivos/diff y evidencia de tests:

```text
Usá opendevguild:reviewer para revisar buggy.py en modo de solo lectura contra el requisito de descuento suministrado. Informá defectos justificados con severidad, ubicación exacta y contraejemplo. No edites, ejecutes comandos ni invoques otro agente.
```

El manifiesto declara el archivo `./agents/reviewer.md`, no una carpeta. No
configura Bash, edición, red/MCP, delegación, hooks ni ajustes globales. Los ocho
perfiles TOML de Codex se conservan y no son subagentes de Claude. Los campos
`permissionMode`, `hooks` y `mcpServers` se ignoran en agentes de plugins; por eso
no se incluyen. Declarar herramientas no es un sandbox del sistema operativo:
Claude debe imponer permisos y privacidad. El revisor no puede ejecutar tests y
debe distinguir evidencia suministrada de verificaciones no ejecutadas.

## Prueba real cuando el cliente esté disponible

Creá un proyecto temporal con datos sintéticos; por ejemplo, este defecto donde
el requisito exige restar el descuento:

```python
def total_after_discount(total, discount):
    return max(0, total + discount)
```

Conservá el checkout del plugin fuera del proyecto. Registrá hashes de archivos
antes/después y cualquier incorporación inesperada. Ejecutá primero un único caso
de alcance, en contexto nuevo y con permisos de lectura impuestos por el host.
`--plugin-dir` no convierte la sesión principal en solo lectura: configurá esos
permisos en tu cliente antes de la prueba.
Guardá versión real de Claude, revisión/ruta, inventario descubierto, eventos de
lectura de instrucciones y herramientas, respuesta y efectos sobre archivos.
Clasificá descubrimiento, activación y comportamiento por separado.
Evitá contaminación por otros plugins o instrucciones heredadas; si no podés
aislarlos, registrá el límite y no atribuyas el resultado a este adaptador. No
borres ni reescribas configuraciones globales para conseguirlo.

Sin eventos observables, la activación sigue `NOT_VERIFIED`. Si falla la sesión
de Claude, detenete y registrá su propio `BLOCKED_BY_AUTH`; no ejecutes Codex ni
transfieras credenciales. La delegación al revisor requiere evidencia separada
de una invocación hija real, no solo Markdown válido.

## Evidencia y límites

- **Offline:** pruebas de política/estructura y empaquetado del adaptador; las
  42 skills compartidas y los perfiles existentes siguen bajo sus validadores.
- **Validador oficial de Claude:** `NOT_RUN`, ejecutable no disponible.
- **Descubrimiento, activación y comportamiento en Claude:** `NOT_RUN`, sin sesión.
- **Delegación y aplicación real de permisos del revisor:** `NOT_RUN`, sin sesión.

El validador local aplica una política mínima del proyecto; no reemplaza al de
Anthropic. Rechaza capacidades no previstas, rutas que escapan, herramientas
adicionales y permisos que Claude ignoraría.
La política también rechaza componentes autodescubiertos como `.mcp.json`,
`settings.json`, `hooks/` y `commands/`, aunque no aparezcan en el manifiesto.
El paquete incluye solo los dos
archivos explícitos del adaptador más las skills compartidas, nunca ajustes,
credenciales, cachés ni estado de `.claude/`. La versión nativa coincide con el
catálogo; deberá incrementarse al publicar una actualización futura. Sin nuevas
dependencias, evaluaciones de modelos ni cambios de configuración global.

Fuentes oficiales consultadas el 2026-11-09 vía Firecrawl, con HTTP 200. El acceso
directo desde este workspace devolvió 403. La adaptación es original:
[manifiesto](https://code.claude.com/docs/en/plugins-reference),
[subagentes](https://code.claude.com/docs/en/sub-agents) y
[distribución/desarrollo local](https://code.claude.com/docs/en/plugin-marketplaces).
