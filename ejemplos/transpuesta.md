# Transpuesta de una matriz

Parte de la issue #2 y de las operaciones de la tarea 5. Las filas de A pasan a columnas de Aᵀ. Una entrada A[i,j] se coloca en R[j,i], conservando su valor exacto.

Seleccionar **Transpuesta · Aᵀ → Cargar ejemplo → Calcular**:

```text
A (2×3) = [[1/3, -2, 5], [0, 4, 1/2]]
Aᵀ (3×2) = [[1/3, 0], [-2, 4], [5, 1/2]]
```

Ejemplo de traslado: `A[1,2] = -2 → R[2,1] = -2`. El recorrido visita las posiciones del resultado por filas. Cada posición tiene Identificar, Ubicar y Guardar, con tres segundos por etapa o avance manual. No hay multiplicación ni simplificación del número.

La consola ofrece **5. Transponer una matriz**. Solo pide A, que puede ser nueva o el último resultado. Para comprobar `(Aᵀ)ᵀ = A`, reutilizar la transpuesta como A y volver a calcular.

Casos pequeños:

- `[[1, 2, 3]]` se convierte en `[[1], [2], [3]]`.
- `[[1], [-2]]` se convierte en `[[1, -2]]`.
- `[[1/3]]` conserva su valor y tamaño, en filas nuevas.

Se rechazan datos inválidos de A o dimensiones que no se hayan aplicado. B y el escalar k se conservan al cambiar de modo, pero no se solicitan ni se validan para Aᵀ. El resultado se desplaza si no cabe completo en su tarjeta.
