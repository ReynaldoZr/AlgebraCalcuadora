# Multiplicar una matriz por un escalar

Parte de la issue #2, tareas 3 y 5: cada entrada de A se multiplica por el mismo número k. Se conserva el tamaño; k puede ser negativo, cero, entero o una fracción exacta. El escalar no representa una segunda matriz.

## Ejemplo de la ventana

Seleccionar **Escalar · kA → Cargar ejemplo → Calcular**:

```text
A = [[1/3, 1/10], [-2, 4]]
k = -3/2
kA = [[-1/2, -3/20], [3, -6]]
```

Primer paso: `(-3/2) × (1/3) = -3/6 = -1/2`. La vista previa muestra una igualdad; Todos los pasos presenta las cuatro posiciones y sus equivalencias. Se pueden recorrer con los controles existentes.

## Cero e identidad

Con `A = [[1/3, -2, 0]]`:

- k = 0 produce `[[0, 0, 0]]`.
- k = 1 produce `[[1/3, -2, 0]]` en una lista independiente.
- k = 0.1 produce `[[1/30, -1/5, 0]]` exactamente, sin redondeo.

En la consola, entrar a Álgebra de matrices y elegir la opción 4. Se pide A (nueva o último resultado), después k y si se desea ver el procedimiento. La opción 3 conserva su función de mostrar el último resultado.

## Errores recuperables

El escalar `1/0`, vacío o texto no numérico debe rechazarse sin borrar A o el último resultado. En la ventana se enfoca k; en consola se reintenta. Las dimensiones nuevas de A se aplican antes de calcular. Los datos de B se conservan al cambiar de modo y no participan en kA.

Desde Python: `multiplicar_por_escalar(A, k)` acepta enteros/Fraction; rechaza float y bool para mantener el contrato exacto del núcleo.
