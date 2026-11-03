# Plan de versiones

La candidata v0.1.0 está implementada y en verificación para su PR. Los demás hitos son propuestas, no funciones ya terminadas ni nuevas fechas de entrega. El plan prioriza reconstruir una base correcta y recuperar progresivamente el contenido del curso. El plan semanal 12 anuncia una defensa del avance en semana 13: el ritmo real se ajustará a esa necesidad.

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
- Crear una etiqueta de Git en el commit entregado y una nota en CHANGELOG.md. No fabricar carpetas «final2», «final_ahora_si» ni copias completas del proyecto por versión.

## Qué anotar en CHANGELOG

Fecha real de publicación, etiqueta, funciones añadidas, errores corregidos, cambios incompatibles y limitaciones conocidas. Antes de publicar, los cambios quedan bajo «Sin publicar». Nunca marcar como completada una función que solo tiene menú o archivo vacío.
