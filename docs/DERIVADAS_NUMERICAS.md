# Derivadas numéricas · issue 34

Fuente provisional: Plan semanal 14 y Sesión 22, diapositiva 17 y ejercicio 7, compartidos por Reynaldo. El enunciado oficial del Programa 9 sigue pendiente. No modifica propagación, bisección ni el álgebra exacta.

## Qué hace cada función

`modulos/numericos/derivadas.py` contiene dos funciones públicas sin interfaz ni dependencias externas:

- `calcular_derivada(funcion, x, h=1e-5, metodo='central')`: devuelve un `Calculo` con el valor aproximado, pasos, muestras, esquema y avisos.
- `crear_derivada(funcion, h=1e-5, metodo='central')`: devuelve un callable que acepta x y entrega la aproximación. Es compatible con el núcleo de #33 y con `proveedor_derivada` del adaptador preparado por Roberto. No ejecuta Newton.

El método `adelante` usa `[f(x+h)-f(x)]/h`; el `central`, `[f(x+h)-f(x-h)]/(2h)`. En condiciones de suavidad adecuadas, los órdenes del error de truncamiento son O(h) y O(h²), respectivamente. Esto no garantiza igual precisión para toda función o cualquier h.

```python
from modulos.numericos.derivadas import calcular_derivada, crear_derivada
from modulos.numericos.funciones import crear_funcion

funcion = crear_funcion('x^3-2*x-5')
adelante = calcular_derivada(funcion, 2, h=0.01, metodo='adelante')
central = calcular_derivada(funcion, 2, h=0.01)
derivada_para_newton = crear_derivada(funcion, h=1e-5)
```

En x=2, la derivada analítica es 10: adelante da aproximadamente 10.0601 y central 10.0001. La central reduce aquí el truncamiento; no se deriva simbólicamente ni se elige un h óptimo.

## Validación y precisión

Se exige función evaluable, x finito y h positivo/finito. Los puntos x+h y, para central, x-h deben ser finitos y distintos de x en punto flotante. Se comprueba el dominio en ambos puntos, el denominador, la diferencia y el cociente. Una evaluación o magnitud no representable produce `ValueError` con diagnóstico: se evita entregar NaN/infinito como derivada válida. Esta implementación no promete resolver todos los casos extremos mediante reescalado automático.

Un h menor reduce truncamiento solo hasta que redondeo y cancelación dominan. El valor 1e-5 es un ajuste inicial, no una garantía universal ni una tolerancia de Newton. Se mantiene el h nominal de la fórmula; los puntos representados pueden tener error de redondeo aun siendo distinguibles.

Si ambas muestras coinciden, se muestra una advertencia: podría ser derivada local cero o pérdida de precisión. No se rechaza automáticamente una función constante ni se certifica una derivada exacta. Si un cociente no nulo matemáticamente se subdesborda a cero, también se advierte. Consultar `calculo.datos['advertencias']` y los pasos para el diagnóstico.

El callable devuelve solo el valor y valida los puntos en **cada evaluación**, no solo en x0. Si produce cero, Newton debe informar que no puede dividir por una derivada nula y permitir revisar h/función; el diagnóstico detallado se obtiene con `calcular_derivada`.

## Integración sin depender del compañero

La rama nace de main y no necesita que #33 ya esté integrado. Las pruebas usan derivadas analíticas conocidas y el adaptador real con el proveedor inyectado; no introducen un solver ficticio en producción. Tras integrar #33 y #34 se debe ejecutar el cúbico desde x0=2 con central h=1e-5 y comparar raíz, residuo e iteraciones con la derivada analítica bajo las mismas tolerancias. La conexión completa al menú sigue siendo parte de #36–#38.

Pruebas: valores de clase, varios h moderados, h no distinguible, dominios, valores no finitos, desbordamiento, muestras iguales, subdesbordamiento y contrato de proveedor. Cada PR conserva las comprobaciones completas y Windows 3.11/3.13.
