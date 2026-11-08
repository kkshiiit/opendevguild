# Visual Intelligence Engine V1

Extensión opcional de OpenDevGuild: conserva las 34 skills originales y agrega
ocho procedimientos visuales, sin crear ocho subagentes permanentes.
[Guía técnica en inglés](README.md).

Incluye dirección visual, análisis de referencias, color, tipografía/composición,
materiales, movimiento, implementación y QA visual independiente. Mission Control
selecciona solamente lo pertinente. Una propuesta importante necesita una revisión
separada: su director de arte no puede aprobarla unilateralmente.

La biblioteca inicial contiene tres referencias de desarrollo y una de evaluación,
con fuente original, licencia Apache-2.0, hashes e inspección real. Las imágenes
son capturas de nuestros propios fixtures, no recursos de terceros redistribuidos.
Las fuentes técnicas externas se registran como referencias. La separación de
datasets se valida por identidad, imagen y fuente; el conjunto de evaluación no
es un holdout sellado e independiente del autor.

```bash
uv sync --frozen --group visual
uv run --frozen playwright install chromium ffmpeg
uv run --frozen python scripts/visual.py validate
uv run --frozen python scripts/capture_visual.py --output dist/visual-run
uv run --frozen python scripts/visual.py contrast '#536357' '#f5f3ed'
```

El destino de captura debe estar vacío. No actualices imágenes de referencia para
ocultar regresiones. Compará condiciones iguales de navegador, sistema, fuentes,
viewport, escala, tema y estado. El contador de píxeles indica cambios, no belleza.
El contraste requiere colores sRGB opacos ya compuestos sobre el fondo real;
la luminosidad OKLCH no sustituye el cálculo WCAG.

Los materiales se distinguen como vidrio estilizado, vidrio dinámico simulado y
material nativo oficial. El ejemplo web muestra transparencia/blur y una simulación
Canvas con desplazamiento de píxeles. No implementa Liquid Glass nativo de Apple
ni demuestra fidelidad física, consumo móvil o rendimiento GPU. Hay capturas y una
grabación reales; la aprobación no se basa solamente en leer código.

Los doce antipatrones tienen contexto, evidencia necesaria, impacto y usos
legítimos. No prohíben tarjetas, gradientes, redondeo o vidrio de forma absoluta.
Tampoco permiten inferir que una interfaz fue generada por IA por su apariencia.

Para aportar preferencias humanas, utilizá el esquema de feedback y los IDs de
referencias conocidas. Registrá tarea, condiciones, orden de presentación, elección
(también empate o ninguna), razones, consentimiento y un ID seudónimo. El comando
`python scripts/visual.py check-feedback archivo.json` valida el registro; no
inventa participantes ni convierte preferencias en una puntuación definitiva.

Las correcciones registran original, problema, propuesta, justificación, resultado,
evaluación y regresión. `check-correction archivo.json` exige revisión independiente,
evidencia posterior con hash y regresión aprobada para habilitar una promoción
manual. No incorpora opiniones automáticamente, no reutiliza holdouts como reglas
y **no realiza fine-tuning**. Ambos logs empiezan vacíos porque no hubo aportes
humanos ni correcciones validadas.

El [informe de resultados](results.md) distingue mediciones de juicios. Los
[escenarios comparativos](BENCHMARKS.md) preparan tres brazos —agente base, núcleo
OpenDevGuild y extensión visual— para Android, web, escritorio y videojuegos.
Esas comparaciones siguen sin ejecutar; no hay superioridad estética demostrada.
