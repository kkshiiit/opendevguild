# OpenDevGuild

## Instalación rápida

**Versión de desarrollo 0.4.0 · Apache-2.0 · [English](README.md)**

OpenDevGuild aporta **34 skills de ingeniería y ocho especialistas visuales**.
El cliente compatible aporta modelo, herramientas y permisos. Copiar una skill no
inicia agentes, modifica tu app ni concede acceso automáticamente.

1. Usá **Code → Download ZIP** o [descargá el repositorio](https://github.com/kkshiiit/opendevguild/archive/refs/heads/main.zip).
   Si preferís Git:

   ```text
   git clone https://github.com/kkshiiit/opendevguild.git
   ```

2. Extraé/abrí la descarga. Revisá `skills/scope-guardian/SKILL.md`. Copiá solamente
   la carpeta `scope-guardian` dentro de `.agents/skills/` de **tu aplicación**.
   Si el destino existe, detenete: no sobrescribas. No copies el `AGENTS.md` de esta
   biblioteca ni instales las 42 skills por defecto.
3. Abrí tu aplicación en un cliente Codex compatible. Confirmá que `/skills`
   muestre la instalación; iniciá otra sesión si hace falta. Probá:

   ```text
   $scope-guardian Delimitá la corrección del error de login. No edites archivos.
   Identificá rutas afectadas, exclusiones, comprobaciones y datos faltantes.
   ```

Esperá un informe de alcance, no una corrección automática. Si no aparece en la
lista, consultá [errores frecuentes](docs/troubleshooting.md). Que el modelo repita
el nombre no prueba que la cargó. **Para usar el texto de las skills no necesitás
Python ni uv.** Git es opcional con la descarga ZIP; el cliente tiene sus propios
prerrequisitos.

**Empezá aquí:** [Instalación](docs/installation.es.md) ·
[Uso rápido](docs/quickstart.es.md) · [Compatibilidad comprobada y documentada](docs/client-compatibility.md)
· [Ocho ejemplos copiables](docs/usage-examples.md).

## Qué incluye

| Capa | Responsabilidad |
| --- | --- |
| Orquestación | Seleccionar especialistas, ordenar dependencias y limitar recursos |
| Especialistas | Aplicar los 42 procedimientos del [catálogo](docs/catalog.md) |
| Ejecución | Usar herramientas, permisos y subagentes reales del entorno |
| Verificación | Revisar evidencia y aprobar, rechazar o bloquear gates independientemente |

FAST, STANDARD y CRITICAL ajustan el trabajo según el riesgo, sin aumentar
permisos. Los ocho perfiles opcionales en [.codex/agents](.codex/agents) recomiendan
skills: instalarlas y configurar subagentes son operaciones distintas. La sintaxis
válida de un perfil no demuestra su carga. Consultá la
[matriz de compatibilidad](docs/client-compatibility.md).

[Visual Intelligence Engine V1](visual/README.es.md) agrega referencias originales
inspeccionadas, color, tipografía, materiales, movimiento y revisión visual. Los
[resultados](visual/results.md) distinguen mediciones de preferencias humanas.
No se promete superioridad estética, fine-tuning, cumplimiento legal automático
ni ahorro de tokens sin evidencia.

## Instalación, mantenimiento y trabajo sobre apps

La [guía de instalación](docs/installation.es.md) cubre descarga, checksum,
rutas POSIX/PowerShell, uso por proyecto o personal, actualización, desinstalación
y rollback conservando cambios. El [instalador local opcional](docs/installer-reference.md)
requiere Python; la copia manual no. No se necesita ejecutar scripts remotos ni
instalar globalmente en silencio.

Los [ejemplos](docs/usage-examples.md) cubren bugs, review, UI, planificación
Android, tests backend, seguridad/licencias, releases y misiones complejas.
Recetas específicas: [Android](examples/android/README.md),
[web](examples/web/README.md), [backend](examples/backend/README.md),
[desktop](examples/desktop/README.md), [videojuegos](examples/games/README.md).
Describen trabajo sobre una aplicación suministrada; no instalan OpenDevGuild ni
prueban por sí mismas ejecución de SDKs nativos.

## Validación para colaboradores

Solo mantenimiento y validación requieren Python 3.11+, Git y uv. Revisá las
[fuentes](docs/research.md) antes de instalar dependencias fijadas:

```bash
uv sync --frozen
uv run --frozen python scripts/guild.py validate
uv run --frozen python -m unittest discover -s tests -v
uv run --frozen python scripts/guild.py check-handoff examples/handoff.json --task examples/task.json
uv run --frozen python scripts/guild.py package --output dist/opendevguild-0.4.0.zip
```

Elegí otra salida si ya existe. Las capturas requieren el grupo visual opcional y
la instalación explícita del navegador; seguí la [guía visual](visual/README.es.md).
La estructura válida no demuestra todo comportamiento del agente. El
[registro](docs/verification.md), [informe final](docs/final-report.md) y
[protocolo](evaluations/README.md) conservan resultados, fallos y límites reales.

## Proyecto y comunidad

[Requisitos](docs/requirements.md) · [Arquitectura](docs/design.md) ·
[Flujos](docs/workflows.md) · [Estándares](docs/engineering-standards.md) ·
[Roadmap](docs/roadmap.md) · [Versiones](docs/releasing.md) · [Cambios](CHANGELOG.md).

[Seguridad](SECURITY.md) · [Contribuir](CONTRIBUTING.es.md) ·
[Gobernanza](GOVERNANCE.md) · [Conducta](CODE_OF_CONDUCT.md) ·
[Apache-2.0](LICENSE) · [Avisos](NOTICE).

Proyecto comunitario independiente. Las referencias a proveedores no implican
afiliación. Repositorio oficial: [kkshiiit/opendevguild](https://github.com/kkshiiit/opendevguild).
Publicar código o una release no implica aceptación en un directorio de plugins.
