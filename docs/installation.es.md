# Instalación

[English](installation.md) · [Uso rápido](quickstart.es.md) ·
[Errores frecuentes](troubleshooting.md) · [Compatibilidad](client-compatibility.md)

## Requisitos y alcance

Necesitás un cliente compatible, una aplicación de destino y un administrador de
archivos. Git es opcional. **No necesitás Python, uv, navegadores ni dependencias
de desarrollo solo para usar el texto de las skills.** Las tareas de tu app pueden
necesitar SDKs/herramientas; deben detectarse y declararse por separado.

Las skills son procedimientos: no instalan un modelo, conceden permisos, inician
subagentes ni garantizan corrección. Elegí una o dos del [catálogo](catalog.md).

## 1. Obtener una fuente revisada

Sin Git, usá **Code → Download ZIP** del repositorio y extraé el archivo. Es un
snapshot del código, distinto del ZIP de release con checksum. Para la versión
fijada abrí [release 0.4.1](https://github.com/kkshiiit/opendevguild/releases/tag/v0.4.1)
y descargá **ambos**: `opendevguild-0.4.1.zip` y `opendevguild-0.4.1.zip.sha256`.
La publicación y los enlaces deben comprobarse antes de declarar disponible la
release. El checksum detecta bytes distintos, no certifica identidad del editor.

Con Git —comando ejecutado correctamente contra el repositorio público—:

```text
git clone https://github.com/kkshiiit/opendevguild.git
cd opendevguild
```

`main` puede avanzar. Registrá `git rev-parse HEAD`; usá un tag de release solo
si comprobaste su existencia. No cambies de revisión sobre trabajo sin confirmar.
Revisá el `SKILL.md` elegido antes de copiarlo.

### Verificar la descarga

Guardá el ZIP y su sidecar en la misma carpeta. Linux:

```bash
sha256sum -c opendevguild-0.4.1.zip.sha256
```

macOS:

```bash
shasum -a 256 -c opendevguild-0.4.1.zip.sha256
```

Windows PowerShell:

```powershell
$expected = (Get-Content .\opendevguild-0.4.1.zip.sha256).Split()[0].ToLowerInvariant()
$actual = (Get-FileHash .\opendevguild-0.4.1.zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw 'SHA-256 incorrecto: no instalar' }
'SHA-256 coincide'
```

El workflow de publicación descarga el ZIP y su checksum públicos en Linux, macOS y
Windows y exige resultados aprobados de sus utilidades nativas. No confundas copia
con integridad. La comprobación del ZIP realmente publicado
pertenece al informe de entrega. Detenete si el hash no coincide.

## 2. Instalar una skill en tu proyecto

Codex documenta esta ruta final:

```text
tu-app/.agents/skills/scope-guardian/SKILL.md
```

Copiá la **carpeta completa**, incluyendo referencias/assets si existen. Rechazá
un destino existente o un enlace simbólico. No copies el `AGENTS.md` de esta
biblioteca a tu aplicación: contiene instrucciones para sus colaboradores.

Sin terminal: creá `.agents` y dentro `skills` en tu app; copiá allí la carpeta
revisada `scope-guardian`. Activá la vista de archivos ocultos si hace falta. Esto
no requiere Python ni modifica otros proyectos.

Shell POSIX, desde la descarga/checkout de OpenDevGuild:

```bash
odg_target="/ruta/absoluta/a/tu-app/.agents/skills"
mkdir -p "$odg_target"
if [ -e "$odg_target/scope-guardian" ] || [ -L "$odg_target/scope-guardian" ]; then
  printf '%s\n' 'DETENER: el destino existe; conservarlo y revisar la actualización.'
else
  cp -R skills/scope-guardian "$odg_target/scope-guardian"
fi
test -f "$odg_target/scope-guardian/SKILL.md"
```

Reemplazá la ruta absoluta. Los ejemplos literales se ejecutan en proyectos
temporales Linux y macOS con rechazo de colisión; la carga del cliente es otra prueba.

PowerShell —ejemplo literal de copia y colisión probado en CI Windows—:

```powershell
$odgTarget = 'C:\ruta\a\tu-app\.agents\skills'
New-Item -ItemType Directory -Force -Path $odgTarget | Out-Null
$odgDestination = Join-Path $odgTarget 'scope-guardian'
if ($null -ne (Get-Item -LiteralPath $odgDestination -Force -ErrorAction SilentlyContinue)) { throw 'DETENER: el destino existe' }
Copy-Item -LiteralPath '.\skills\scope-guardian' -Destination $odgDestination -Recurse
Test-Path -LiteralPath (Join-Path $odgDestination 'SKILL.md')
```

`True` comprueba la copia, no el descubrimiento del cliente. Probá primero con
un destino vacío. El [instalador local opcional](installer-reference.md) ofrece
simulación/dry-run, estado, colisiones y rollback; requiere Python y se ejecuta
solo por pedido explícito. La copia manual sigue siendo el camino básico.

## 3. Comprobar descubrimiento y uso

Abrí **tu app**, no el checkout de OpenDevGuild, en el cliente. En Codex CLI/IDE,
usá `/skills` donde se admita y verificá nombre y ruta de origen. Iniciá otra
sesión si no detecta cambios. Invocá:

```text
$scope-guardian Delimitá la corrección del error de login. No edites archivos.
Informá rutas afectadas, exclusiones, comprobaciones y datos faltantes.
```

Suministrá el error y las rutas reales. Esperá un informe acotado de alcance con
supuestos y datos desconocidos, sin cambios ajenos. Confirmá que el cliente eligió
la instalación correcta: repetir el nombre no prueba su carga. En el entorno de
autoría, la carga nativa Codex seguía bloqueada por autenticación expirada. La
copia comprobada no debe presentarse como activación real; consultá la
[matriz](client-compatibility.md).

## 4. Uso personal y otros clientes

La instalación por proyecto es el valor inicial. La personal afecta varios
proyectos y debe ser una elección explícita. Estas rutas están documentadas;
no significan que se hayan probado todos los clientes/plataformas:

| Cliente | Proyecto | Personal explícita | Invocación |
| --- | --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/`; Windows `$env:USERPROFILE\.agents\skills` | `$scope-guardian`; selección `/skills` cuando exista |
| Claude Code | `.claude/skills/` | `~/.claude/skills/`; Windows `$env:USERPROFILE\.claude\skills` | `/scope-guardian` |
| Gemini CLI | `.gemini/skills/` o alias `.agents/skills/` | `~/.gemini/skills/` o alias `~/.agents/skills/` | `/skills list`, tarea en lenguaje natural; `/skills reload` |

Para el plugin nativo de Claude incorporado después de v0.4.1, usá el checkout y
la [guía de Claude](claude-code.es.md). Sus skills usan `/opendevguild:nombre` y
su único revisor es Markdown nativo; los ocho perfiles de Codex no se cargan como
configuración de Claude. El ZIP publicado de 0.4.1 no contiene este adaptador.

Si Codex ofrece `$skill-installer` oficial, indicá URL, revisión y rutas elegidas
que hayas revisado. No asumas que está disponible ni instales todo por defecto.
Gemini documenta `gemini skills install <source>`; comprobá alcance/consentimiento
en esa versión antes de ejecutarlo. La copia manual evita asumir sus defaults.

ChatGPT **no** descubre `.agents/skills` en tu computadora. Usá el mecanismo de
plugins/workspace que admita tu cuenta; un administrador puede necesitar subir y
publicar el paquete en la interfaz Plugins. Una release GitHub no instala nada en
ChatGPT ni acredita aceptación en su directorio público. Consultá la
[guía oficial](https://developers.openai.com/plugins/build/plugins).
Android/Termux no tiene una instalación verificada en esta versión. Otros clientes
necesitan evidencia propia; no deduzcas soporte universal por similitud con Linux.

## 5. Actualizar, desinstalar y volver atrás

1. Obtené/revisá la revisión nueva por separado. Identificá carpetas instaladas y
   cambios locales. No sobrescribas una skill desconocida ni un enlace simbólico.
2. Compará la instalada con su original conocido y con la actualización. Si hay
   cambios locales o propiedad incierta, detenete para revisar y conservá ambos.
3. Mové la carpeta elegida a un backup **fuera del descubrimiento**, conservando
   sus cambios. Copiá el reemplazo revisado cuando el destino esté libre. No
   muevas otras skills ni archivos de la aplicación.
4. Verificá descubrimiento y una tarea acotada. Para rollback, preservá la carpeta
   nueva fuera del descubrimiento y restaurá la copia anterior.
5. Para desinstalar, mové solo las carpetas de OpenDevGuild instaladas fuera del
   descubrimiento. Conservá los backups hasta decidir retirarlos. Los perfiles de
   agentes opcionales se retiran por separado; no hace falta editar configuración
   global ni ejecutar un reset destructivo de Git.

Se simuló este ciclo con un cambio local sintético y se conservó. Es evidencia de
archivos, no prueba de ejecución de un cliente. El instalador opcional rechaza
ediciones en conflicto; seguí su [referencia](installer-reference.md) y empezá
por dry-run antes de cambiar archivos.
En el instalador de `v0.4.1`, una transacción pendiente bloquea nuevas
operaciones: revisá la [recuperación](installer-reference.md#recuperación-y-límites)
y usá `recover` para el lote completo. El ZIP anterior de 0.4.0 se conserva y no incluye este comando.

## Perfiles opcionales de subagentes

Los ocho `.codex/agents/*.toml` son instrucciones de roles específicas de Codex.
Revisá y copiá solo perfiles necesarios a `.codex/agents/` de tu app compatible,
sin colisiones. Heredan restricciones; no crean herramientas, aislamiento ni
agentes permanentes. Otros clientes no habilitan subagentes Codex por copiarlos.
Instalar una skill nunca requiere instalar esos perfiles.

[Uso rápido](quickstart.es.md) · [Ejemplos](usage-examples.md) · [Errores](troubleshooting.md)
