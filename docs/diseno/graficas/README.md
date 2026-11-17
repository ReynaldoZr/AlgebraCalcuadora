# Referencias visuales de gráficas

## Issues asignadas a Reynaldo

| Issue | Vista y alcance |
| --- | --- |
| [#23](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/23) | Bisección interactiva: función e intervalo conectados al error |
| [#24](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/24) | Jacobi: tolerancia, selección de iteraciones y estado final |
| [#25](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/25) | Gauss-Seidel: recorrido del error y avisos de relajación |
| [#26](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/26) | Comparador Jacobi/Gauss-Seidel: dos curvas y recorrido sincronizado |
| [#27](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/27) | Propagación del error: zoom, Δx/Δy y aproximación lineal |
| [#28](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/28) | Redondeo y truncamiento: contraste y valores finales |
| [#29](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/29) | Sistemas: comparar el error por variable y método |
| [#30](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/30) | Inversas: mapa del error por fila y columna |

Orden recomendado: #23 para la base compartida, #24 y #25 para las vistas individuales, y #26 para comparar ambas. #27–#30 pueden avanzar por separado reutilizando esa base. No resolver las ocho en un único PR de implementación.

Propuestas solicitadas por Reynaldo el 17 de noviembre de 2026 para planificar mejoras por gráfica. No representan funcionalidades implementadas ni autorizan cambiar los algoritmos.

La maqueta interactiva se generó con IA y orienta la composición. Sus curvas, escalas o etiquetas pueden ser ilustrativas: la implementación debe usar los cálculos reales. Las otras imágenes se renderizaron por separado con datos de ejemplos del proyecto; tampoco son capturas de una interfaz ya integrada.

Conservar la paleta vigente, la separación cálculo/interfaz, los pasos completos y el ritmo manual de 2 segundos. Alcance de comprobaciones: Windows con Python 3.11 y 3.13. Cada implementación sigue issue → rama → pruebas → PR → revisión humana.

## Bisección interactiva: función e intervalo conectados al error

![Referencia de biseccion](maqueta-biseccion-interactiva.png)

![Referencia de biseccion](06-ventana-dos-graficas.png)

## Jacobi: tolerancia, selección de iteraciones y estado final

![Referencia de jacobi](01-comparacion-iterativos.png)

![Referencia de jacobi](05-no-convergencia.png)

## Gauss-Seidel: recorrido del error y avisos de relajación

![Referencia de gauss_seidel](01-comparacion-iterativos.png)

![Referencia de gauss_seidel](05-no-convergencia.png)

## Comparador Jacobi/Gauss-Seidel: dos curvas y recorrido sincronizado

![Referencia de comparacion](01-comparacion-iterativos.png)

![Referencia de comparacion](05-no-convergencia.png)

## Propagación del error: zoom, Δx/Δy y aproximación lineal

![Referencia de propagacion](02-propagacion.png)

## Redondeo y truncamiento: contraste y valores finales

![Referencia de redondeo](03-redondeo-truncamiento.png)

## Sistemas: comparar el error por variable y método

![Referencia de sistemas](04-sistemas-inversas.png)

## Inversas: mapa del error por fila y columna

![Referencia de inversas](04-sistemas-inversas.png)


