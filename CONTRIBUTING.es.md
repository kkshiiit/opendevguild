# Contribuir

[English](CONTRIBUTING.md) · [Gobernanza](GOVERNANCE.md) ·
[Contrato](docs/skill-contract.md)

Proponé un problema concreto, evidencia y aceptación. Si las responsabilidades
se superponen, mejorá un procedimiento existente. Una nueva skill debe justificar
sus límites, costo de descubrimiento y mantenimiento; el catálogo no se amplía
por cantidad.

Escribí skills, código y contratos originales en inglés técnico. Mantené alineadas
las guías de usuario en inglés y español. Los aportes se licencian bajo Apache-2.0;
conservá atribuciones y comprobá derechos de redistribución. No incluyas secretos,
datos personales, ejemplos confidenciales ni prompts con derechos inciertos.
Los problemas privados siguen [SECURITY.md](SECURITY.md).

1. Inspeccioná Git, preservá cambios existentes y usá una rama acotada.
2. Definí objetivo autorizado, archivos, supuestos y evidencia de aceptación.
   Seleccioná FAST, STANDARD o CRITICAL según el riesgo real.
3. Cuando corresponda, agregá primero un caso que exponga el problema. Cubrí
   entradas positivas, negativas, ambiguas y de presión; identificá selección
   de uno o varios especialistas cuando modifiques el enrutamiento.
4. Actualizá procedimiento, configuración, contratos, ejemplos y ambas guías.
   Preservá compatibilidad o documentá migración. No inventes campos de metadata,
   herramientas del entorno ni cambios de configuración global.
5. Ejecutá `uv sync --frozen`, `uv run --frozen python scripts/guild.py validate`
   y `uv run --frozen python -m unittest discover -s tests -v`. Informá comandos,
   resultados y entornos ausentes reales.
6. Para afirmar cambios de comportamiento, seguí el [protocolo](evaluations/README.md):
   contextos nuevos comparables, prompts y respuestas exactas, metadata disponible,
   rúbrica fija, efectos y límites. El formato válido no demuestra beneficio.
   Conservá los registros históricos asociados a sus revisiones evaluadas.
7. Pedí revisión con alcance, resultado, evidencia, riesgos y preguntas abiertas.
   La tarea pasa por NEEDS_REVIEW antes de VERIFIED. El verificador decide gates
   con APPROVED, REJECTED, BLOCKED o NOT_APPLICABLE justificado.

Para obtener una señal **local** rápida antes de la batería completa, usá el [selector de pruebas de solo lectura](docs/impact-testing.es.md).
Recomienda tests según los cambios, pero no los ejecuta ni reemplaza CI.

El mantenimiento revisa corrección, seguridad, alcance, compatibilidad, contexto,
licencias y evidencia. Ningún aporte se acepta automáticamente. No debilites
controles para ocultar fallos ni afirmes soporte no probado. Actualizar issues,
fusionar, publicar o contactar colaboradores requiere autoridad real y la
autorización pertinente. Las plantillas indican el mínimo útil para reportar.
