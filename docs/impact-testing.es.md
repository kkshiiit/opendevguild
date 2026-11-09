# Selección de pruebas locales (para colaboradores)

[English](impact-testing.md) · [Cómo contribuir](../CONTRIBUTING.es.md)

`python scripts/impact.py` **recomienda** qué módulos de pruebas ejecutar según
los archivos modificados. Usa solamente la biblioteca estándar de Python y es de
solo lectura: no ejecuta tests, no llama modelos, no lee credenciales, no modifica
archivos y no mide tokens.

Permite obtener resultados preliminares más rápido cuando el cambio es chico.
**La batería completa, la validación, los controles de seguridad y CI siguen
siendo obligatorios antes de integrar o publicar.** Si encuentra cambios no
clasificados o contratos compartidos, recomienda la batería completa.

## Ejemplos desde el repositorio

```bash
python scripts/impact.py --base HEAD
python scripts/impact.py --paths skills/visual-art-director/SKILL.md
python scripts/impact.py --paths scripts/research.py docs/research-program.md
```

El resultado JSON contiene archivos, motivos, `full_suite`, `tests`, comandos
sugeridos y limitaciones. Revisá el resultado y ejecutá los comandos que
correspondan por separado. Un cambio aislado en investigación selecciona
`test_research.py`; cambios en contratos compartidos, workflows o rutas
desconocidas seleccionan toda la batería.

`--base` contempla archivos **versionados** modificados, tanto staged como sin
stage, respecto de la revisión indicada. No incluye archivos nuevos aún sin
seguimiento: pasalos explícitamente con `--paths`. No hay búsquedas remotas.
Una diferencia vacía produce cero recomendaciones, pero **no significa que el
proyecto esté verificado**.

## Límites y controles

- Inspeccioná siempre `git status` y comprobá el alcance real.
- El programa recomienda pruebas: nunca las ejecuta automáticamente.
- Cambios transversales obligan a pasar la batería completa.
- Una recomendación de pruebas rápidas no reemplaza CI, auditoría ni revisión.
- Agregá pruebas manualmente si el comportamiento involucra otros módulos.
- No se afirman ahorros de tokens, mejoras de calidad ni velocidades medidas.

Pruebas offline del selector:

```bash
python -m unittest discover -s tests -p test_impact.py -v
```

Antes de integrar o publicar, ejecutá las comprobaciones completas habituales:

```bash
uv run --frozen python scripts/guild.py validate
uv run --frozen python -m unittest discover -s tests -v
```

El selector necesita Python 3.11+, pero **instalar y usar una Agent Skill
individual no requiere Python**. Es una herramienta para colaborar en el
proyecto, no un runtime de agentes.
