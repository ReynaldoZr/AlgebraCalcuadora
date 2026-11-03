"""Calcula suma y resta de matrices sin modificar los datos originales.

Tema: operaciones de matrices de los Programas 3 y 5.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from modulos.validaciones import validar_mismo_tamano


def sumar_matrices(matriz_a, matriz_b):
    """Recibe matrices del mismo tamaño y devuelve una nueva matriz A + B."""
    filas, columnas = validar_mismo_tamano(matriz_a, matriz_b)
    resultado = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(matriz_a[i][j] + matriz_b[i][j])
        resultado.append(fila)
    return resultado


def restar_matrices(matriz_a, matriz_b):
    """Recibe matrices del mismo tamaño y devuelve una nueva matriz A - B."""
    filas, columnas = validar_mismo_tamano(matriz_a, matriz_b)
    resultado = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(matriz_a[i][j] - matriz_b[i][j])
        resultado.append(fila)
    return resultado
