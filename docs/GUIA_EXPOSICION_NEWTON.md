# Dónde estudiar el avance de Newton

Esta guía reúne lo implementado para preparar la exposición. Las fuentes disponibles son Sesión 22 y Plan semanal 14; el enunciado definitivo del Programa 9 debe confirmarse. El mapa describe código existente, no requisitos nuevos del profesor.

## 1. Empieza por el cálculo de Newton

Archivo: [modulos/numericos/newton.py](../modulos/numericos/newton.py).

En IntelliJ busca `def resolver_newton`. Lee en este orden:

1. `_validar`: revisa función, derivada, punto inicial, tolerancias y máximo.
2. `resolver_newton`: evalúa el punto inicial; si ya es raíz en la aritmética usada, termina sin inventar iteraciones.
3. `_avance`: aplica `x_nuevo = x - f(x) / f'(x)` y comprueba que las evaluaciones y el nuevo punto sean válidos.
4. El bucle de `resolver_newton`: guarda cada iteración, mide el cambio, comprueba el residuo y decide si continúa.
5. `_paso_explicado` y `_terminar`: conservan fórmulas, valores, estado y motivo de parada.

La explicación general puede ser: «Partimos de un valor inicial y usamos la función y su derivada para acercarnos a una raíz. Después de cada avance comprobamos cuánto cambió x y qué tan cerca de cero queda la función».

Para entender los parámetros: x0 es el punto de partida; tolerancia controla el cambio absoluto o porcentual; tolerancia_f controla por separado el residuo; max_iteraciones limita las repeticiones. Son tolerancias positivas porque representan márgenes de aceptación. Cero impediría cumplir una desigualdad estricta y una cantidad negativa no sirve como margen para magnitudes no negativas. Un máximo de 200 permite terminar antes.

Guía detallada: [NEWTON_NUCLEO.md](NEWTON_NUCLEO.md). Incluye ciclo, estancamiento, derivada nula y límites. No afirmar que Newton siempre converge o que una semilla encuentra todas las raíces.

## 2. Después, la derivada numérica

Archivo: [modulos/numericos/derivadas.py](../modulos/numericos/derivadas.py).

- `calcular_derivada`: aproxima la pendiente con muestras cercanas; conserva valores y explicación.
- `crear_derivada`: entrega esa aproximación como una función que Newton puede utilizar.
- `h` es la separación entre muestras. No es la tolerancia de parada. Hacerlo cada vez menor no asegura más precisión por el redondeo de la computadora.

El módulo admite diferencia hacia adelante y central. El modo numérico del formulario utiliza el proveedor central existente. Guía: [DERIVADAS_NUMERICAS.md](DERIVADAS_NUMERICAS.md).

## 3. Horner y deflación para polinomios

Archivo: [modulos/numericos/polinomios.py](../modulos/numericos/polinomios.py).

- `_recorrer` y `evaluar_horner`: recorren los coeficientes para evaluar el polinomio y su derivada.
- `crear_funciones_polinomio`: prepara ambas funciones para usarlas con Newton.
- `deflacionar_polinomio`: divide por `(x - raiz)` y devuelve el cociente conservando el resto. Si el resto supera la tolerancia, no se acepta como una división sin resto.

Para x⁵−4x⁴+5x³−6x+4 se usa `[1, -4, 5, 0, -6, 4]`. El cero conserva el término x² que falta. Estas utilidades se estudian y utilizan desde Python; no tienen una pantalla independiente de Horner/deflación en el menú actual.

Guía y ejemplo completo: [HORNER_Y_DEFLACION.md](HORNER_Y_DEFLACION.md).

## 4. Cómo llegan los datos desde la calculadora

Archivo: [interfaz/numericos/newton_adaptador.py](../interfaz/numericos/newton_adaptador.py).

`validar_entrada_newton` lee y valida los campos; `ejecutar_newton_adaptador` llama al cálculo; `resumen_newton` prepara el resultado. El adaptador no escribe otro algoritmo de Newton. Función y derivada usan el analizador seguro, sin `eval`.

El registro del menú y el despacho están en [interfaz/metodos_numericos.py](../interfaz/metodos_numericos.py), buscando `num_newton`. Uso: [NEWTON_FORMULARIO.md](NEWTON_FORMULARIO.md).

## 5. Pasos, tabla y gráfica

- [newton_presentacion.py](../interfaz/numericos/newton_presentacion.py): `etapas_newton` prepara la vista breve; `pasos_completos_newton` conserva todo el desarrollo; `tabla_newton` entrega todas las filas.
- [newton_graficas.py](../interfaz/numericos/newton_graficas.py): `datos_tangente` toma los valores de una iteración; `figura_newton` dibuja función, tangente, aproximaciones, cambio y residuo.
- [controlador.py](../interfaz/qt/controlador.py): `verGrafica` y `seleccionarIteracionGrafica` conectan los controles con esos datos. Seleccionar una tangente no ejecuta Newton otra vez.

La interfaz muestra los resultados producidos por Python. El cambio de x y el residuo no son el mismo error. El residuo pequeño comprueba la función, pero no certifica por sí solo el error verdadero de x. Detalles y limitaciones: [NEWTON_PASOS_Y_GRAFICAS.md](NEWTON_PASOS_Y_GRAFICAS.md).

## 6. Recorrido para ensayar en la calculadora

1. Ejecuta **Calculadora escritorio** desde IntelliJ: abre `gui.py`.
2. **Numéricos → Newton-Raphson → Cargar ejemplo → Calcular**. Para `exp(-x)-x` desde 0, el resultado es aproximadamente **0.5671432904**, con cuatro iteraciones usando los ajustes del ejemplo.
3. Explica el resultado y el residuo; muestra la vista previa, **Todos los pasos** y **Mostrar tabla**. Comprueba que la última aproximación coincida.
4. En **Ver gráfica**, usa ‹/› para mostrar cómo la tangente produce el siguiente x. Después señala el cambio y el residuo en sus ejes separados.
5. Prueba **Ciclo cúbico**: conserva el motivo de no convergencia. Prueba **Salto x^10-1**: un salto grande puede recuperarse; no basta mirar la curva para decir que diverge.

Como segundo ejercicio, usa el polinomio anterior con derivada `5*x^4-16*x^3+15*x^2-6` y x0=-1.25. La primera aproximación es ≈-1.0679966643 y la raíz obtenida ≈-1. La tolerancia del residuo puede cambiar cuántas iteraciones necesita; no forzar el conteo redondeando datos.

## 7. Dónde revisar las pruebas

En [tests/numericos/](../tests/numericos/): `test_newton.py`, `test_derivadas.py`, `test_polinomios.py` y `test_newton_recorrido.py`. Las de formulario, navegación, gráfica y exportación Qt están también en [tests/test_qt_interfaz.py](../tests/test_qt_interfaz.py).

Para estudiar, primero entiende el flujo y los ejemplos. Después usa las pruebas para ver qué ocurre con una entrada inválida, derivada cero, un ciclo o el máximo agotado. Una prueba aprobada respalda el caso comprobado; no demuestra que toda función arbitraria vaya a converger.
