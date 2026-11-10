# Producto matricial AB

Fuente: operaciones de los Programas 3 y 5, recogidas en la issue #2. Si A es m×n y B es n×p, AB tiene tamaño m×p. Las columnas de A deben coincidir con las filas de B; las matrices no necesitan tener el mismo tamaño.

Seleccionar **Producto · AB → Cargar ejemplo → Calcular**:

```text
A (2×3) = [[1, 2, 3], [4, 5, 6]]
B (3×2) = [[1, 0], [2, 1], [0, 3]]
AB (2×2) = [[5, 11], [14, 23]]
```

Cada celda combina una fila con una columna:

```text
R[1,1] = 1×1 + 2×2 + 3×0 = 5
R[1,2] = 1×0 + 2×1 + 3×3 = 11
R[2,1] = 4×1 + 5×2 + 6×0 = 14
R[2,2] = 4×0 + 5×1 + 6×3 = 23
```

El recorrido elige fila y columna, señala cada par A[i,k]/B[k,j], explica su producto (y simplifica fracciones si corresponde), suma los productos y guarda R[i,j]. Cada etapa dura tres segundos o se recorre manualmente. Todos los pasos presenta todo el desarrollo sin esperar. La suma de productos de una celda no es una multiplicación elemento a elemento.

Ejemplo exacto con cancelación: `A = [[1/3, -2]]`, `B = [[3/2], [1/4]]` produce `[[0]]`, porque `1/2 + (-1/2) = 0`.

En consola, elegir la opción 6. Se pueden ingresar A y B nuevas o reutilizar el último resultado. Las dimensiones se validan de nuevo después de reutilizarlo. Un producto incompatible conserva el resultado anterior y permite corregir los datos.

Casos de error: 2×3 por 2×3, dimensiones sin Aplicar en la ventana, celdas vacías, `1/0` o texto no numérico. El núcleo `producto_matricial(A, B)` admite solo enteros/Fraction, valida ambas matrices y devuelve filas independientes.
