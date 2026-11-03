# Ejemplos para probar y explicar

Ejecuta `python main.py`, entra a Álgebra de matrices y elige suma o resta. Ingresa dimensiones y cada componente por separado. Los siguientes resultados se comprobaron con las pruebas del proyecto.

## Suma rectangular

A = [[1, 2, 3], [4, 5, 6]]

B = [[6, 5, 4], [3, 2, 1]]

A + B = [[7, 7, 7], [7, 7, 7]]

Explicación: cada posición del resultado suma los elementos de esa misma posición. Las dos matrices son de 2 filas y 3 columnas; el resultado también.

## Resta con negativos

A = [[1, -2], [3, 4]]

B = [[5, 1], [-1, 8]]

A - B = [[-4, -3], [4, -4]]

## Fracciones exactas

A = [[1/3, 0.1]]

B = [[1/6, 0.2]]

A + B = [[1/2, 3/10]]

Escribe 0.1 y 0.2 con punto decimal. La aplicación conserva el valor exacto mediante Fraction y presenta 3/10. No utiliza NumPy.

## Datos incorrectos

- Dimensiones: 0, -2, 2.5 y texto deben provocar un nuevo intento.
- Componentes: texto, una casilla vacía y 1/0 deben provocar un nuevo intento.
- Una matriz 1x2 y otra 2x1 no se pueden sumar ni restar; se muestra la diferencia de dimensiones y se regresa al menú.
- Tras obtener un resultado, elige usarlo como A o B de la siguiente operación. No hace falta volver a escribirlo.
