# Uso rápido

[English](quickstart.md) · [Instalación](installation.es.md) · [Errores frecuentes](troubleshooting.md)

1. Elegí **una** responsabilidad del [catálogo](catalog.md). Para empezar sin
   editar, usá scope-guardian; para código suministrado, code-review-engineer.
2. Instalá su carpeta en la ruta documentada del cliente y verificá descubrimiento.
   Abrí el repositorio de tu app, no esta biblioteca.
3. Indicá objetivo, rutas permitidas, restricciones y aceptación. Invocá la skill
   con la sintaxis que realmente admita ese cliente.
4. Revisá resultado y evidencia. Un plan no es código implementado; formato válido
   no equivale a tests de la app ejecutados. Las herramientas ausentes se declaran.

Ejemplo Codex:

```text
$scope-guardian Delimitá la corrección de pedidos duplicados.
Permitido: src/orders y tests/orders. Conservá el rediseño de login sin confirmar.
No edites ni despliegues. Informá supuestos, rutas afectadas y aceptación.
```

Esperá un informe de alcance que preserve trabajo ajeno y proponga verificaciones
acotadas. Reemplazá rutas y defecto por los reales. El ejemplo no autoriza cambios
de la app; usá un especialista de implementación cuando el alcance esté claro.

Para una tarea de varias etapas:

```text
$mission-control Corregí pedidos duplicados en src/orders y sus pruebas.
Conservá el stack y los cambios ajenos, seleccioná solo especialistas necesarios
y no despliegues. Informá checks ejecutados, review y riesgos pendientes.
```

FAST sirve para tareas pequeñas de bajo riesgo. STANDARD y CRITICAL agregan
controles según riesgo, sin conceder permisos. El ejecutor normalmente entrega
NEEDS_REVIEW; VERIFIED requiere evidencia apropiada y revisión independiente.
Los subagentes son una capacidad opcional, no un requisito para usar skills.

Consultá los [ocho ejemplos completos](usage-examples.md) y la
[matriz](client-compatibility.md). Su presencia no demuestra invocación real.
