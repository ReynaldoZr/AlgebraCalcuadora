# Plan de versiones

Actualización 4 de noviembre: el hito de semana 12 ya tiene implementación local en `feat/semana-12-numericos`, pendiente de revisión humana y autorización de subida. No cambia la versión publicada ni se añade una etiqueta de release. Consulte [SEMANA_12.md](SEMANA_12.md).

El usuario autorizó completar localmente los cálculos de tareas 1 a 6: los hitos matemáticos hasta LU/verificadores tienen ahora implementación local en `feat/3-algebra-tareas-1-a-6`, pendiente de comprobación y revisión humana antes de publicar. Los números de la tabla continúan siendo propuestas; no se han publicado esas versiones. Semana 12 queda fuera de esta ampliación. Véase [cobertura actual](ALGEBRA_TAREAS_1_A_6.md).

v0.1.0 contiene la primera implementación, con 16 pruebas locales aprobadas y cuatro combinaciones de CI comprobadas. Su publicación se identifica por la etiqueta v0.1.0 y el PR #5. Los demás hitos son propuestas, no funciones ya terminadas ni nuevas fechas de entrega. El plan prioriza reconstruir una base correcta y recuperar progresivamente el contenido del curso. El plan semanal 12 anuncia una defensa del avance en semana 13: el ritmo real se ajustará a esa necesidad.

La interfaz de la issue #8 ya se integró en main mediante el PR #10 por decisión de Roberto. Escalar, transpuesta y producto matricial de la issue #2 se preparan en la rama local con consola, interfaz, procedimientos y pruebas. El hito v0.2.0 aún necesita revisión humana e integración; no está publicado. El número de la siguiente entrega se decidirá al autorizar su publicación, sin cambiar ahora main.VERSION ni renumerar las issues matemáticas existentes.

| Hito interno | Resultado revisable | Relación con el curso |
|---|---|---|
| v0.1.0 | Arranque, menú local, entrada validada, formato y suma/resta de matrices | Base pequeña con la que ambos aprenden el flujo |
| v0.2.0 | Escalar, producto, transpuesta y reutilización de resultados | Parte de tareas 3 y 5 |
| v0.3.0 | Gauss, clasificación y comprobación Ax=b | Tarea 1 |
| v0.4.0 | Gauss-Jordan, pivotes, variables libres y solución general | Tarea 2 |
| v0.5.0 | Vectores, combinación lineal e independencia | Tareas 3 y 4 |
| v0.6.0 | Determinantes e inversas por los métodos exigidos | Tarea 5 |
| v0.7.0 | Verificadores completos y LU sin permutación | Tarea 6 y correcciones globales |
| v0.8.0 | Errores y bisección, comparación con bibliotecas autorizadas | Tarea 7 orientada en plan 12 |
| v1.0.0 | Integración de requisitos del alcance acordado, informe y defensa | Entrega estable del equipo |

Espacios, bases, dimensión, transformaciones, rango y nulidad tienen lugar reservado en el mapa. Su prioridad se decide con la entrega concreta; no deben introducirse a medias ni anunciarse como completos por estar en el temario. Newton-Raphson está previsto en el sílabo para después.

## Cómo numerar sin confundir

- v0.2.0 → v0.2.1: corrección compatible de un error de esa etapa.
- v0.2.1 → v0.3.0: siguiente bloque de funciones del plan.
- Desde v1.0.0: primer número para cambios incompatibles de contratos, segundo para funciones compatibles y tercero para correcciones compatibles.
- El número de tarea del profesor y la versión del software son datos distintos. En cada entrega se registra qué versión satisface qué tarea.
- Después de la revisión y decisión humana, integrar el PR. Crear la etiqueta en el commit entregado y la nota de publicación en CHANGELOG.md solo con autorización expresa para publicar. La IA deja sus cambios bajo «Sin publicar» y no adelanta esos pasos. No fabricar carpetas «final2», «final_ahora_si» ni copias completas del proyecto por versión.

## Qué anotar en CHANGELOG

Fecha real de publicación, etiqueta, funciones añadidas, errores corregidos, cambios incompatibles y limitaciones conocidas. Antes de publicar, los cambios quedan bajo «Sin publicar». Nunca marcar como completada una función que solo tiene menú o archivo vacío.
