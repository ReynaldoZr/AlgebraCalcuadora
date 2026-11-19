# Newton-Raphson · núcleo de la issue 33

Fuente: Sesión 22 y Plan semanal 14 del [curso UAM](https://uamvirtual.uam.edu.ni/grado/course/view.php?id=8202&section=14), compartidos por Reynaldo. El Programa 9 sigue provisional: las decisiones siguientes son del equipo, no una rúbrica nueva del profesor.

## Uso y contrato

`modulos/numericos/newton.py` contiene el bucle propio, sin interfaz ni dependencias externas obligatorias. Usa el analizador seguro existente para expresiones, nunca `eval`:

```python
from modulos.numericos.funciones import crear_funcion
from modulos.numericos.newton import resolver_newton

resultado = resolver_newton(
    crear_funcion('exp(-x)-x'),
    crear_funcion('-exp(-x)-1'),
    x0=0,
    tolerancia=0.0001,
    max_iteraciones=200,
)
```

Devuelve aproximadamente 0.5671432904 en cuatro iteraciones. Los adaptadores reales de Roberto pueden consumirlo, pero el núcleo no añade por sí solo una opción al menú: la conexión completa queda en #36–#38.

Firma: `resolver_newton(funcion, derivada, x0, tolerancia=0.0001, max_iteraciones=200, criterio='absoluto', *, tolerancia_f=1e-8)`. Retorno `Calculo`:

- `valor`: último punto finito evaluado correctamente; si falla la función inicial, valor y residuo quedan no definidos. x0 se conserva en los datos.
- `pasos`: datos, sustitución de cada iteración completa y motivo final.
- `datos`: método, x0, ambas tolerancias, máximo, criterio, convergencia, motivo, residuo, iteraciones, columnas, filas, registros y advertencias.
- Filas: `(i, xi, f(xi), derivada, x_siguiente, error_absoluto, error_porcentual, residuo)`. La fila 1 parte de x0 y produce x1. Los registros contienen las mismas magnitudes por clave, usando `fxi` para la función de entrada.

No redondea internamente. Un intento inválido no reemplaza el último resultado evaluado ni se cuenta como fila completa; el motivo identifica el intento. Los contratos de otros métodos no cambian.

## Parada y precisión

Cada paso aplica `x_nuevo=x-f(x)/f'(x)` y evalúa el punto nuevo en la función original. El cambio absoluto es `abs(x_nuevo-x)`; el porcentual es `abs((x_nuevo-x)/x_nuevo)*100`, con tolerancia también en %. En cero o si excede el rango representable, el porcentaje queda no definido.

Como protección contra falso éxito, tanto el cambio elegido como el residuo `abs(f(x_nuevo))` deben ser **menores** que sus tolerancias. El residuo tiene tolerancia independiente `tolerancia_f`, por defecto 1e-8, y no representa error verdadero en x. Si la función evaluada da cero, puede terminar de inmediato, incluso en x0 o con porcentaje no definido. Un cero en punto flotante no prueba igualdad matemática exacta: existe redondeo y posible subdesbordamiento.

Si el punto nuevo es idéntico al anterior y la función sigue no nula, se informa estancamiento antes de aceptar tolerancias: un cociente redondeado a cero no demuestra que Newton haya avanzado.

La tolerancia adicional es una decisión provisional del equipo, ajustable a la escala de la función y pendiente de confirmar con el enunciado. En el polinomio de quinto grado, `tolerancia_f=1e-4` reproduce las cuatro iteraciones de clase; el valor por defecto puede pedir otra. No forzar el conteo redondeando datos. Bisección no cambia.

## Validación y limitaciones

Entrada mal formada lanza `ValueError`: función/derivada no evaluables, números no finitos, tolerancias no positivas, máximo distinto de entero entre 1 y 10000 o criterio desconocido. Los fallos numéricos devuelven `convergio=False`, causa e historial: derivada nula, dominio, cociente no finito, desbordamiento, estancamiento, ciclo exacto de dos puntos o máximo.

No se rechaza una derivada pequeña por un umbral fijo: una función escalada puede tener una corrección válida. Se valida el cociente y el punto. Un salto grande no significa automáticamente divergencia: x¹⁰−1 desde 0.5 puede recuperarse. El máximo limita otros ciclos o comportamientos divergentes no detectados.

Newton no garantiza converger ni encontrar todas las raíces con una semilla. Trabaja con reales; derivada numérica y Horner/deflación pertenecen a #34 y #35. La derivada analítica suministrada debe ser correcta: el núcleo no la obtiene simbólicamente ni certifica su equivalencia.

## Referencia opcional y pruebas

`contrastar_newton(resultado, funcion, derivada)` añade una referencia SciPy por solicitud explícita. Usa tolerancia absoluta 1e-12 y el mismo máximo; sus criterios y conteos no son idénticos. Su residuo, convergencia y diferencia se guardan aparte. No reemplaza el bucle ni modifica el cálculo propio, y un fallo de referencia no lo borra. SciPy se importa solo al pedir el contraste.

Las pruebas cubren raíces y primer paso, residuo, tabla del profesor, salto grande, ciclo, raíz inicial, entradas inválidas, derivada nula/escalada, estancamiento, porcentaje en cero, desigualdad estricta, dominio, valores no finitos, máximo, referencia y consumo desde adaptadores reales.
