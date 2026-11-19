# Horner y deflación · issue 35

Fuente provisional: Sesión 22, diapositiva 13 y ejercicio 6 de la 22, compartida por Reynaldo para preparar el Programa 9. El enunciado oficial sigue pendiente. Este módulo numérico aproxima con float y no cambia el álgebra exacta ni usa NumPy como algoritmo propio.

## Entradas y funciones

`modulos/numericos/polinomios.py` recibe listas/tuplas no vacías de coeficientes en orden descendente. Se conserva el cero de cualquier término ausente. Por ejemplo, x⁵−4x⁴+5x³−6x+4 se escribe `[1,-4,5,0,-6,4]`: quitar el cero cambiaría el polinomio.

Se copian y convierten los coeficientes a reales finitos. Solo se normalizan los ceros iniciales; se conservan originales, cantidad normalizada y grado. Un polinomio constante tiene derivada cero. Un polinomio nulo se puede evaluar, pero no se presenta como si tuviera un conjunto finito de raíces.

- `evaluar_horner(coeficientes, x)` devuelve `Calculo`: valor p(x), derivada en `datos['derivada']`, tabla, acumulados y pasos. Horner extendido actualiza primero el acumulado de derivada usando el valor anterior; después actualiza p. No redondea para continuar el cálculo.
- `crear_funciones_polinomio(coeficientes)` devuelve dos callables `(funcion, derivada)`, compatibles con el núcleo #33. Capturan una copia estable, de modo que editar la lista original no cambia una ejecución futura.
- `deflacionar_polinomio(coeficientes, raiz, tolerancia_resto=1e-8)` devuelve coeficientes del cociente como `valor` y conserva resto, residuo, originales, tolerancia y estado `aceptada`. Se exige grado al menos 1.

No admite coeficientes o puntos complejos, booleanos, NaN/infinito ni resultados intermedios no finitos. Los rechaza con `ValueError`; no garantiza estabilidad para todos los grados o escalas extremos.

## Ejemplo de la clase

```python
from modulos.numericos.polinomios import (
    crear_funciones_polinomio, deflacionar_polinomio, evaluar_horner,
)

coeficientes = [1, -4, 5, 0, -6, 4]
evaluacion = evaluar_horner(coeficientes, -1.25)
division = deflacionar_polinomio(coeficientes, -1)
funcion_original, derivada_original = crear_funciones_polinomio(coeficientes)
```

Se obtiene p(-1.25)=-11.0830078125 y p'(-1.25)=60.89453125. La división por x+1 deja `[1,-5,10,-10,4]`, resto cero en la aritmética utilizada. El primer avance de Newton da aproximadamente -1.0679966643, que redondeado a seis decimales coincide con -1.067997 de clase.

## Qué significa aceptar una deflación

La identidad que se conserva es `p(x)=(x-raiz)*q(x)+resto`. El resto se evalúa usando el polinomio original suministrado a la llamada. **Nunca se borra el resto.** `aceptada=True` significa únicamente `abs(resto) < tolerancia_resto`; la igualdad con la tolerancia no basta. El valor por defecto es una decisión de implementación ajustable a la escala, no una exigencia confirmada del profesor.

Si la raíz es aproximada y el resto supera la tolerancia, se devuelve el cociente con `aceptada=False` y una advertencia: el consumidor no debe continuar como si el resto fuera cero. Incluso con resto aceptable, deflaciones sucesivas pueden acumular error.

Al integrar con #33: conservar los coeficientes iniciales, refinar cada raíz candidata usando la función y derivada del **polinomio original**, comprobar su residuo allí y solo después considerar deflación. Verificar también la reconstrucción con resto. Una deflación posterior no convierte por sí sola una aproximación en raíz exacta.

## Raíces reales y complejas

El polinomio de quinto grado tiene raíces reales -1, 1, 2 y complejas 1±i. El cuártico del ejemplo tiene 1, 2 y 1±i. Los tests contrastan el cuártico con `numpy.roots` como referencia independiente; el módulo propio usa Horner y división sintética, no ese solucionador.

Los callables y Newton de esta etapa son reales. No se afirma que una sola semilla encuentre todas las raíces ni que este módulo real haya obtenido las complejas. Una búsqueda completa, Bairstow o soporte complejo requieren confirmar el alcance con el profesor y otra implementación.

## Pruebas y coordinación

Esta rama parte de main y no depende de un import todavía inexistente de #33. Prueba valores y derivada conocidos, término ausente, ceros iniciales, raíz múltiple/cero, constantes, resto inaceptable, frontera de tolerancia, reconstrucción, copias estables, no finitos y referencia NumPy. Tras integrar el núcleo, comprobar también refinamiento con los proveedores y residuo en el original.

La conexión de formulario, pasos, tabla y gráfica permanece en #36–#38. Esta utilidad no cambia el diseño ni introduce un método incompleto en el menú.
