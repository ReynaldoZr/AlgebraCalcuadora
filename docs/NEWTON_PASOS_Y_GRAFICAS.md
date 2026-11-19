# Recorrido y gráfica de Newton · issues 37 y 38

Reynaldo autorizó completar estas conexiones el 18/11/2026, aprovechando los presentadores que Roberto había preparado. La propuesta reúne #37 y #38 porque la selección gráfica consume exactamente las filas del recorrido. No cambia el núcleo matemático ni la distribución de las tres tarjetas.

## Recorrido para probar

1. Desde IntelliJ ejecutar **Calculadora escritorio** (`gui.py`). Entrar en **Numéricos → Newton-Raphson** y pulsar **Cargar ejemplo**. La carga nunca es automática.
2. Pulsar **Calcular**: exp(-x)-x desde 0 converge a aproximadamente 0.5671432904. El resultado muestra estado, motivo, cambio y comprobación en la función original.
3. La **Vista previa** contiene una etapa por iteración: punto actual, siguiente aproximación, explicación breve, cambio y residuo. Anterior/Siguiente/Reiniciar usan datos guardados. Reproducir empieza solo al pulsarlo, con ritmo fijo de dos segundos.
4. Entrar en **Todos los pasos** para ver condiciones, cada sustitución y la terminación completa. **Mostrar tabla** utiliza toda el área de contenido; permite desplazamiento horizontal/vertical y regresar a los pasos. Los datos indefinidos dicen «No definido», sin convertirlos en cero. El porcentaje siempre lleva %. Las fórmulas conservan la notación y espaciado existentes.
5. Pulsar **Ver gráfica**. Se pausa la reproducción. El panel superior muestra la función, x0, aproximaciones, tangente seleccionada y el corte de esa tangente con y=0. Los botones ‹ y › recorren las filas sin recalcular Newton ni cambiar el formulario.
6. El panel inferior distingue cambio absoluto o porcentaje (eje izquierdo) de residuo (derecho), con sus propios umbrales. No se inventa un número positivo para sustituir ceros en escala logarítmica: esa serie usa escala lineal cuando contiene ceros.
7. **Guardar imagen…** exporta el PNG que se está viendo, con la tangente seleccionada y el tema actual. **Guardar resultado…** conserva el escalar original, sin usar cifras redondeadas de la tabla.

## Comparación opcional

Calcular primero en Bisección la misma expresión literal, por ejemplo `exp(-x)-x`, en [0,1]. Volver a Newton y calcular con criterio absoluto. En la gráfica se habilita **Comparar con última bisección**. Reutiliza esa sesión vigente; no lanza otro solucionador ni solicita reingresar el resultado.

La línea de bisección es una **cota de intervalo**, mientras que Newton muestra **cambio entre iteraciones**: no son el mismo error ni prueban qué método es mejor. No se exige el mismo número de iteraciones o la misma raíz en funciones con varias raíces. Con Newton porcentual, otra función o una bisección editada sin recalcular, la comparación se deshabilita. La igualdad literal es conservadora: expresiones matemáticamente equivalentes escritas de otra forma requieren escribirlas igual para comparar.

## Casos de clase y límites

- Polinomio `x^5-4*x^4+5*x^3-6*x+4`, derivada `5*x^4-16*x^3+15*x^2-6`, x0=-1.25: primera aproximación ≈-1.0679966643 y raíz ≈-1. Todas las iteraciones permanecen en la tabla y el desarrollo.
- **Ciclo cúbico** desde 0: conserva 0↔1 y se identifica como no convergente. El último punto no se etiqueta como raíz.
- **Salto x^10-1** desde 0.5: conserva el salto grande y su posterior recuperación, sin diagnosticar divergencia por la apariencia del dibujo.
- Una raíz inicial muestra el punto y el motivo, sin inventar filas. Un fallo de dominio sin valor evaluado no se dibuja como raíz ni se guarda como un escalar ficticio.
- Las evaluaciones inválidas y algunos saltos alrededor de singularidades interrumpen la curva. Es un muestreo, no una prueba de continuidad ni un detector de todas las asíntotas de funciones arbitrarias.
- El dibujo limita magnitudes a un rango seguro menor que 1e100. Si la trayectoria/errores exceden ese rango, aparece un aviso para consultar la tabla; los datos originales se conservan íntegros. La vista de función cubre la trayectoria completa: un salto grande puede comprimir la zona cercana a la raíz. No se ocultan iteraciones para mejorar la apariencia.
- Newton real con una semilla no promete encontrar todas las raíces ni raíces complejas. Ninguna mejora gráfica cambia esa propiedad.

## Organización y comprobaciones

`newton_presentacion.py` prepara pasos breves y tabla; `qt/catalogo.py` y `panel_numerico.py` conectan ese contrato. `newton_graficas.py` consume registros, `figuras.py` despacha por método y `graficas_qt.py` aplica el tema y exporta a memoria. El controlador Qt guarda únicamente la selección gráfica; QML no resuelve fórmulas.

Tk conserva su flujo anterior de tabla/desarrollo y su barra Matplotlib; abre la figura con la última tangente. La selección dinámica y comparación con otra sesión se ofrecen en la interfaz principal Qt.

Las pruebas incluyen integración real, clase, ceros/fallos/extremos, tangente calculada con sus datos guardados, curvas sin modificar el cálculo, PNG en ambos temas, navegación, tabla completa y controles QML sin utilizar la pantalla personal. Ejecutar la suite completa, el verificador y ambas CI Windows 3.11/3.13 antes de integrar.

La fuente continúa siendo Sesión 22 y Plan semanal 14. **El enunciado definitivo del Programa 9 todavía debe confirmarse**; esta implementación no inventa su rúbrica ni anuncia una versión publicada.
