# Informe de entrega — OpenDevGuild 0.4.0

Fecha: 2026-11-09. Este informe distingue preparación local de los resultados de
publicación, que se comprueban en la release y sus ejecuciones enlazadas.

## A. Estado general

Se finalizó una versión incremental centrada en instalación utilizable y evidencia.
El repositorio oficial ya es público; no se creó otro ni se cambió su visibilidad.
Se preservaron las 42 skills, los 8 perfiles y Visual Intelligence Engine V1. La
publicación requiere el CI del commit seleccionado y verificación de artefactos;
no se deduce de un build local ni de una guía con enlaces aún no publicados.

## B. Inventario y responsabilidades

El [catálogo](catalog.md) enumera34 skills originales y8 visuales. La
[auditoría individual](specialist-audit.md) revisa las 42 contra 18 criterios,
distinguiendo documentación, ejemplos y comportamiento realmente evaluado.
La [matriz de responsabilidades](responsibility-coverage.md) cubre las 36 propuestas
con responsabilidades existentes y8 referencias bajo demanda. No se crearon36 skills
ni nuevos subagentes. La lista anterior de 30propuestas no estaba disponible y no
se inventó. Se conservan los ocho roles Codex existentes.

## C. Cambios frente a0.3.0

IMPLEMENTADO: guías EN/ES de instalación y uso, troubleshooting, compatibilidad
por cliente/plataforma, ocho escenarios, instalador local opcional con dry-run,
versiones/backup/rollback y protección de cambios del usuario; registroSQLite
acotado, procedenciaL0–L4, deduplicación, muestreo, reutilización y verificadores
de descarga/checksum públicos. Se añaden procedimientos de IA/evaluación/contexto,
legal/datos, licencias/tiendas, marketing/experimentos/monetización, i18n,
abuso/Trust&Safety, audio y soporte. Sus resultados en productos no se presentan
como DEMOSTRADOS. Todo permanece independiente de un runtime propio.

## D. Calidad y gates

Localmente:110 métodos,109 aprobados y1 omitido por falta de PowerShell. Incluye16
pruebas del instalador,13 de investigación,4 de integridad y pruebas literales de
las guías. Formato oficial, enlaces locales, sintaxis y Ruff pasaron. La revisión
independiente encontró y verificó dos correcciones reales: capacidad del manifiesto
y avance de evidencia con contenido sin cambios. Hay44 dependencias instaladas
sin advisories conocidos en el escaneo de Nov9; los metadatos de licencias no se
presentan como certificación ni todas las dependencias como Apache-2.0.

Requirements, Architecture, Implementation y Verification tienen evidencia local
proporcional; Security conserva límites explícitos. Release necesita observación
real del CI, descarga e integridad pública. Native client discovery queda BLOCKED
por autenticación expirada; no bloquea el uso manual de procedimientos bajo los
límites documentados. No se debilitaron tests ni se borraron fallos históricos.

## E. Investigación: cifras exactas

| Categoría | L0 | L1 | L2 | L3 | L4 |
| --- | --- | --- | --- | --- | --- |
| Páginas web |0|0|0|0|0|
| Apps Android |0|0|0|0|0|
| Programas PC |0|0|0|0|0|
| Webapps |0|0|0|0|0|
| Agent Skills externas |0|0|0|0|0|
| Prompts |0|0|0|0|0|
| Documentos técnicos |0|18|0|0|0|

Son18 observaciones/metadatos provenientes del registro previo,18 fuentes únicas,
cero hashes de cuerpo conocidos. Reimportar insertó 0 registros y reconoció 18
duplicados. Las42 skills locales y fixtures no inflan esas cifras. El objetivo
1.400.000 es un programa independiente de largo plazo; no está cumplido.

## F. Eficiencia

La deduplicación y recuperación selectiva están implementadas y probadas. Las
modalidades FAST/STANDARD/CRITICAL, presupuestos y resultados anteriores se conservan.
No hay telemetría comparable de tokens, costo o consumo total de herramientas de
este encargo; no se atribuyen ahorros. No se repitieron benchmarks humanos/nativos
sin fixtures. Reutilizar informes e instrucciones no es fine-tuning.

## G. GitHub y artefactos

Repositorio único: https://github.com/kkshiiit/opendevguild ; rama main;
versión 0.4.0; licencia Apache-2.0. El commit/tag exacto se verifica en GitHub.
La release pública debe contener `opendevguild-0.4.0.zip` y su `.zip.sha256`:
[release](https://github.com/kkshiiit/opendevguild/releases/tag/v0.4.0).
El ZIP es reproducible a bytes iguales de entrada y excluye Git, venv, bases de
datos locales, archivos temporales y otros artefactos. El evento de publicación
comprueba descargas sin token y utilidades nativas en Linux/macOS/Windows. Resultados
observados finales se entregan en las notas de release y el informe al usuario;
un enlace previsto por sí solo nunca se cuenta como publicación comprobada.

## H. Instalación y uso

- [README español](../README.es.md) y [README inglés](../README.md).
- [Instalación ES](installation.es.md) y [EN](installation.md).
- [Uso rápido ES](quickstart.es.md) y [EN](quickstart.md).
- [Troubleshooting](troubleshooting.md), [compatibilidad](client-compatibility.md)
  y [ejemplos](usage-examples.md).

Los comandos POSIX de copia se ejecutaron literalmente desde directorios temporales
en ambos idiomas y rechazaron colisiones. El helper opcional se probó desde el
checkout real, incluyendo modificación del usuario, actualización, desinstalación
y rollback. El usuario manual no necesita Python, uv ni el entorno de desarrollo.
PowerShell/macOS se distinguen según la evidencia nativa registrada por CI.

Ejemplo Codex, una vez confirmada la carga en el cliente:

```text
$scope-guardian Delimitá el arreglo de src/orders y sus pruebas.
No edites login ni despliegues. Informá alcance, riesgos y aceptación verificable.
```

Es una tarea sobre la app del usuario, no sobre instalar OpenDevGuild. Instalar
una skill no habilita herramientas, subagentes ni permisos nuevos.

## I. Pendientes y próxima acción

Restaurar autenticación del cliente mediante el flujo normal del usuario y probar
carga real; ejecutar Claude/Gemini cuando estén disponibles; obtener preferencias
humanas consentidas, datasets sellados y pruebas nativas; ampliar corpus mediante
lotes revisados; validar resultados de las responsabilidades adyacentes en tareas
reales antes de declararlas mejoras demostradas. No hay cumplimiento jurídico,
WCAG completo, rendimiento nativo ni superioridad estética garantizados.
