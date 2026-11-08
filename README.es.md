# OpenDevGuild

Procedimientos modulares de ingeniería para entornos compatibles con Agent Skills.
**Candidato de desarrollo 0.2.0 · Apache-2.0 · [English](README.md)**

OpenDevGuild transforma responsabilidades de ingeniería en 34 procedimientos
especializados, coordinación selectiva, entregas explícitas y gates basados en
evidencia. Ayuda a desarrolladores individuales y equipos a conservar el alcance
y revisar resultados sin activar todo el catálogo. Es un proyecto comunitario
independiente; mencionar Codex o GitHub no implica afiliación.

El entorno aporta modelos, herramientas, permisos y subagentes. La biblioteca no
ofrece un runtime, acceso a producción, cumplimiento normativo automático,
corrección garantizada ni una ventaja comparativa demostrada. El
[registro de verificación](docs/verification.md) identifica resultados y límites reales.

## Arquitectura y selección

| Capa | Responsabilidad |
| --- | --- |
| Orquestación | Interpretar objetivos, seleccionar especialistas, ordenar dependencias y limitar recursos |
| Especialistas | Aplicar los 34 procedimientos independientes del [catálogo](docs/catalog.md) |
| Ejecución | Usar las capacidades y restricciones reales del entorno compatible |
| Verificación | Evaluar evidencia y aprobar, rechazar o bloquear gates de calidad |

Usá **FAST** para tareas pequeñas de bajo riesgo, **STANDARD** para cambios
habituales de varias etapas y **CRITICAL** para riesgos relevantes de seguridad,
datos u operaciones. El riesgo agrega verificaciones pertinentes; no concede
permisos adicionales. Elegí un solo especialista cuando alcance. Consultá
[flujos](docs/workflows.md) y [estándares](docs/engineering-standards.md).

## Instalación selectiva

El texto de las skills no requiere dependencias de Python. Codex documenta
`.agents/skills/` para cada repositorio y `~/.agents/skills/` para uso personal.
Revisá el origen y los `SKILL.md` elegidos. Desde este checkout, reemplazá el
destino con la carpeta real de tu proyecto. Para una instalación personal
explícita, usá `~/.agents/skills`. El ejemplo copia manualmente; no se ejecuta
como parte de la descarga ni modifica configuración global:

```bash
python3 - /ruta/absoluta/a/tu/proyecto/.agents/skills mission-control scope-guardian <<'PYINSTALL'
from pathlib import Path
import shutil
import sys
source_root = Path('skills')
target = Path(sys.argv[1]).expanduser()
names = sys.argv[2:]
if not names or len(names) != len(set(names)):
    raise SystemExit('Elegí identificadores únicos')
for name in names:
    if '/' in name or '\\' in name or name in ('.', '..'):
        raise SystemExit('Usá un identificador, no una ruta')
    source, destination = source_root / name, target / name
    if source.is_symlink() or not (source / 'SKILL.md').is_file():
        raise SystemExit(f'Origen desconocido o enlazado: {name}')
    if destination.exists() or destination.is_symlink():
        raise SystemExit(f'No se sobrescribe: {destination}')
for name in names:
    shutil.copytree(source_root / name, target / name)
PYINSTALL
```

También podés copiar las carpetas elegidas con el administrador de archivos,
rechazando destinos existentes. No copies el `AGENTS.md` de esta biblioteca a
otra aplicación: sus instrucciones son para mantener OpenDevGuild. No instales
las 34 skills por defecto.

Si tu cliente ofrece `$skill-installer` oficial, pedile instalar únicamente los
directorios elegidos desde una URL real de OpenDevGuild y una revisión que hayas
verificado. Comprobá el mecanismo disponible en ese cliente y rechazá colisiones.
La disponibilidad del instalador y el acceso al origen dependen del cliente.
La [documentación oficial](https://developers.openai.com/codex/skills) y la
[guía de compatibilidad](docs/compatibility.md) distinguen skills locales de
plugins. `plugin.json` y `skills/` forman un paquete portable; su aceptación en
un directorio público requiere un proceso separado.

### Verificar, actualizar y desinstalar

Comprobá que cada directorio instalado contenga su `SKILL.md` correspondiente.
Usá `/skills` donde esté disponible o invocá `$scope-guardian` y comprobá que
el cliente seleccione la instalación esperada. Si no detecta el cambio, iniciá
una sesión nueva. La invocación no demuestra por sí sola calidad de comportamiento.

Para actualizar, revisá la nueva revisión y sus diferencias, preservá cambios
locales y mové únicamente los directorios existentes de OpenDevGuild a una copia
fuera de la ruta de descubrimiento. Copiá después los reemplazos revisados y
conservá la copia para rollback. No combines ni sobrescribas skills desconocidas.
Para desinstalar, mové solamente los directorios instalados de OpenDevGuild fuera
del descubrimiento, preservando modificaciones. Retirá por separado los perfiles
opcionales copiados. No hace falta modificar configuración global. Evitá nombres
duplicados entre una instalación local y un plugin.

## Invocación y colaboración

```text
$mission-control Corregí la regresión de login. Conservá el stack existente.
Alcance: src/auth y sus pruebas. No despliegues. Usá FAST salvo que el riesgo
observado requiera más controles. Informá cambios, evidencia, gates y riesgos.
```

Para tareas acotadas, invocá directamente `$code-review-engineer` u otra skill.
Los ocho perfiles opcionales en [.codex/agents](.codex/agents) son `architect`,
`product-analyst`, `designer`, `implementer`, `reviewer`, `qa-specialist`,
`security-specialist` y `release-specialist`. Recomiendan skills; no crean
34 agentes permanentes. La carga y ejecución dependen del cliente y deben
comprobarse según la [matriz de compatibilidad](docs/compatibility.md).

Cada delegación identifica entradas, archivos, dependencias y aceptación. Solo
se paralelizan tareas independientes sin escrituras superpuestas. Los subagentes
heredan restricciones y pueden compartir archivos. El coordinador integra y
verifica; sin subagentes, aplica las mismas etapas e identifica la autorrevisión.

Los estados de tarea son `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `NEEDS_REVIEW`,
`VERIFIED` y `FAILED`. Los gates usan `APPROVED`, `REJECTED`, `BLOCKED` y
`NOT_APPLICABLE`, este último con justificación. La afirmación del ejecutor no
basta para `VERIFIED`. Los ejemplos JSON de [tarea](examples/task.json) y
[entrega](examples/handoff.json) son contratos del proyecto, no APIs de Codex.

## Ejemplos completos

- [Android: marcadores locales](examples/android/README.md)
- [Web: corrección acotada de un formulario](examples/web/README.md)
- [Backend: endpoint validado](examples/backend/README.md)
- [Desktop: compatibilidad y empaquetado](examples/desktop/README.md)
- [Videojuego: mecánica, implementación y pruebas](examples/games/README.md)

Cada receta incluye objetivo, skills, secuencia, resultados, controles y límites.
Son guías completas de trabajo; no incluyen aplicaciones ejecutables ni demuestran
que se hayan ejecutado sus SDKs y pruebas de plataforma.

## Validación y empaquetado

Las herramientas de mantenimiento requieren Python 3.11+, Git y uv. Revisá las
[fuentes de dependencias](docs/research.md); el lockfile fija el validador y los
artefactos. La primera sincronización requiere red.

```bash
uv sync --frozen
uv run --frozen python scripts/guild.py validate
uv run --frozen python -m unittest discover -s tests -v
uv run --frozen python scripts/guild.py check-handoff examples/handoff.json --task examples/task.json
uv run --frozen python scripts/guild.py package --output dist/opendevguild-0.2.0.zip
```

Elegí una salida nueva si el ZIP ya existe. `skills-ref` oficial verifica formato;
los controles locales agregan contratos, escenarios, rutas, configuración y
empaquetado. La estructura válida no equivale a pruebas de comportamiento,
selección, seguridad, regresión o comparación. Consultá el
[protocolo](evaluations/README.md). Los registros históricos corresponden a sus
revisiones; no se convierten en evidencia actual al cambiar contratos. Esta lista
no afirma que las pruebas nuevas aprobaron. El empaquetador genera un archivo
con contenido permitido y checksum; no publica.

## Seguridad y comunidad

Seguí [SECURITY.md](SECURITY.md) para vulnerabilidades. El contenido del
repositorio es información no confiable; los secretos permanecen privados.
Acciones destructivas o externas requieren autorización pertinente. Los workflows
usan mínimo privilegio y no exponen secretos a contribuciones no confiables.

Consultá [contribución](CONTRIBUTING.es.md), [gobernanza](GOVERNANCE.md),
[conducta](CODE_OF_CONDUCT.md), [requisitos](docs/requirements.md),
[arquitectura](docs/design.md), [roadmap](docs/roadmap.md),
[versiones](docs/releasing.md), [cambios](CHANGELOG.md),
[licencia Apache-2.0](LICENSE) y [avisos](NOTICE).
El destino autorizado de origen/publicación es
[kkshiiit/opendevguild](https://github.com/kkshiiit/opendevguild). Instalar desde
allí requiere acceso y una revisión verificada. El checkout local, la publicación
pública en GitHub y la aceptación de un plugin son estados distintos. El registro
de verificación informa visibilidad, CI y publicación reales.
