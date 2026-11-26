# Plan de versiones

## v1.0.0 · 25 de noviembre de 2026

Lanzamiento del Cuaderno de Álgebra con selector de propiedades, entrada de sistemas por pegado, regla de Cramer, verificación LU y criterios de parada para los ejercicios de la guía.

## Antecedente · 21 de noviembre de 2026

Reynaldo eligió **versión 0.9**, registrada como **v0.9.0**, para el avance integrado de la aplicación. La consola y el título de Qt leen la misma constante `main.VERSION`.

Incluye álgebra exacta, biblioteca/guardados, numéricos, Jacobi/Gauss-Seidel, Newton, derivadas numéricas, Horner/deflación y el avance de gráficas integrado en el PR #46. Horner/deflación son utilidades de Python y no tienen pantalla independiente. El alcance detallado de la interfaz está en GRAFICAS_INTERACTIVAS.md.

Las interacciones adicionales de #23–#30 fueron descartadas por Reynaldo y se cierran como no planificadas. No se anuncian como implementadas. El enunciado definitivo del Programa 9 sigue pendiente de confirmación.

Esta denominación identifica la aplicación y no crea una etiqueta ni una release pública. v0.1.0 sigue siendo la publicación histórica inicial. La tabla siguiente conserva el plan original de hitos; no implica que se hayan publicado todas sus versiones.

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
| v0.9.0 | Avance integrado actual, Qt y numéricos con Newton | Identificación acordada el 21/11/2026 |
| v1.0.0 | Integración de requisitos del alcance acordado, informe y defensa | Entrega estable del equipo |

Espacios, bases, dimensión, transformaciones, rango y nulidad tienen lugar reservado en el mapa. Su prioridad se decide con la entrega concreta; no deben introducirse a medias ni anunciarse como completos por estar en el temario. Newton-Raphson ya tiene núcleo e interfaz integrados; su alcance académico definitivo sigue por confirmar.

## Cómo numerar sin confundir

- v0.2.0 → v0.2.1: corrección compatible de un error de esa etapa.
- v0.2.1 → v0.3.0: siguiente bloque de funciones del plan.
- Desde v1.0.0: primer número para cambios incompatibles de contratos, segundo para funciones compatibles y tercero para correcciones compatibles.
- El número de tarea del profesor y la versión del software son datos distintos. En cada entrega se registra qué versión satisface qué tarea.
- Después de la revisión y decisión humana, integrar el PR. Crear la etiqueta en el commit entregado y la nota de publicación en CHANGELOG.md solo con autorización expresa para publicar. La IA deja sus cambios bajo «Sin publicar» y no adelanta esos pasos. No fabricar carpetas «final2», «final_ahora_si» ni copias completas del proyecto por versión.

## Qué anotar en CHANGELOG

Fecha real de publicación, etiqueta, funciones añadidas, errores corregidos, cambios incompatibles y limitaciones conocidas. Antes de publicar, los cambios quedan bajo «Sin publicar». Nunca marcar como completada una función que solo tiene menú o archivo vacío.
