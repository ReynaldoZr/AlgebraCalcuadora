# Cómo añadir una función sin rehacer la calculadora

## Receta para cada cambio

1. Crear una tarea pequeña: qué hará, fuente de clase, entradas, resultado y condiciones de aceptación.
2. Localizar el módulo en ESTRUCTURA.md. Buscar funciones existentes antes de escribir otras.
3. Acordar el nombre y el retorno de la función. Registrar si usa aritmética exacta o aproximada.
4. Implementar el cálculo sin entrada/salida de pantalla. Validar sus precondiciones.
5. Añadir ejemplos con respuesta conocida y errores relevantes.
6. Conectar la operación al menú del tema y mostrar errores recuperables sin cerrar la aplicación.
7. Añadir teorema o comprobación si lo exige el enunciado.
8. Actualizar documentación afectada y abrir un PR vinculado a la issue con el resultado verificable; comprobar la CI del último commit.
9. Si trabaja una IA, entregar el PR abierto y detenerse antes de integrar o publicar. Reynaldo u otro humano autorizado decide después de revisar; seguir [FLUJO_IA.md](FLUJO_IA.md).

## Ejemplo de cambio pequeño

**Tarea:** multiplicar matrices rectangulares.

- Fuente: Programa 3 y Programa 5.
- Cálculo: producto_matricial(A, B) en modulos/modulo_matrices.py.
- Entrada: A de m×n y B de n×p. Salida: matriz de m×p.
- Validación: no vacías, rectangulares y columnas de A iguales a filas de B.
- Interfaz: opción Producto; leer matrices, llamar función y mostrar dimensiones.
- Ejemplo del profesor: A=[[1,2,3],[4,5,6]], B=[[1,0],[2,1],[0,3]]; resultado [[5,11],[14,23]].
- Errores: 2×3 por 2×3 debe rechazarse con explicación de dimensiones.
- Conservación: comprobar que A y B no cambian.
- Reutilización futura: inversa, verificadores y LU llaman a esta función.

## Pruebas que sí aportan

Las pruebas comprueban resultados matemáticos y comportamientos observables. Para Gauss/Gauss-Jordan: solución única, infinitas, inconsistente, matriz rectangular y pivote que exige intercambio. Para inversa: invertible, singular y producto con la inversa. Para LU: producto LU=A y rechazo del caso que requiere permutación. Para bisección: raíz conocida, raíz en extremo, intervalo sin cambio de signo y terminación por límites.

También se revisarán las entradas vacías, texto en campos numéricos, dimensiones inválidas y recuperación del menú. No escribir pruebas que solo repitan la implementación.

## Condición para dar una operación por terminada

Para la IA, estar lista para revisión significa entregar el cambio y sus comprobaciones en un PR abierto. No significa que esté integrado o publicado. El cierre definitivo depende de la revisión y decisión humana.

El cálculo funciona, su entrada y salida están documentadas, aparece donde corresponde, maneja datos incorrectos, tiene comprobación apropiada y ambos integrantes pueden explicarla con un ejemplo. En Métodos Numéricos debe indicarse si hubo convergencia o por qué se detuvo.

## Si el cambio exige tocar mucho

Separar corrección matemática de cambio de estructura. Mantener las funciones públicas que ya usan otros módulos o adaptar sus llamadas en un cambio coherente y documentado. Una reorganización grande merece una tarea distinta con explicación de qué problema resuelve; no se mezcla con añadir un botón o una operación pequeña.
