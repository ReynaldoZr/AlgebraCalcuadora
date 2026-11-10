"""Comprueba la estructura y las dimensiones de las matrices.

Tema: condiciones para operar con matrices rectangulares.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction


def validar_cuadrada(matriz):
    """Exige una matriz exacta cuadrada y devuelve su orden."""
    filas, columnas = validar_matriz(matriz)
    if filas != columnas:
        raise ValueError("Se necesita una matriz cuadrada (mismas filas y columnas).")
    return filas


def validar_vector(vector, dimension=None):
    """Exige una lista no vacía de valores exactos y, si se indica, su dimensión."""
    if not isinstance(vector, list) or not vector:
        raise ValueError("El vector debe ser una lista no vacía.")
    validar_matriz([vector])
    if dimension is not None and len(vector) != dimension:
        raise ValueError(f"El vector debe tener {dimension} componentes; tiene {len(vector)}.")
    return len(vector)


def validar_matriz(matriz):
    """Valida una lista rectangular de enteros o Fraction; devuelve sus dimensiones."""
    if not isinstance(matriz, list) or not matriz:
        raise ValueError("La matriz debe ser una lista con al menos una fila.")
    if not isinstance(matriz[0], list) or not matriz[0]:
        raise ValueError("Cada fila debe ser una lista con al menos una columna.")
    columnas = len(matriz[0])
    for fila in matriz:
        if not isinstance(fila, list) or len(fila) != columnas:
            raise ValueError("Todas las filas deben tener la misma cantidad de columnas.")
        for numero in fila:
            if isinstance(numero, bool) or not isinstance(numero, (int, Fraction)):
                raise ValueError("Los elementos deben ser enteros o fracciones exactas.")
    return len(matriz), columnas


def validar_mismo_tamano(matriz_a, matriz_b):
    """Valida dos matrices del mismo tamaño y devuelve sus filas y columnas."""
    filas_a, columnas_a = validar_matriz(matriz_a)
    filas_b, columnas_b = validar_matriz(matriz_b)
    if (filas_a, columnas_a) != (filas_b, columnas_b):
        raise ValueError(
            "Para sumar o restar, las dimensiones deben coincidir: "
            f"A es {filas_a}x{columnas_a} y B es {filas_b}x{columnas_b}."
        )
    return filas_a, columnas_a


def validar_producto(matriz_a, matriz_b):
    """Valida A de m×n y B de n×p; devuelve m, n y p."""
    filas_a, columnas_a = validar_matriz(matriz_a)
    filas_b, columnas_b = validar_matriz(matriz_b)
    if columnas_a != filas_b:
        raise ValueError("Para multiplicar, las columnas de A deben coincidir con las filas de B: "
                         f"A es {filas_a}x{columnas_a} y B es {filas_b}x{columnas_b}.")
    return filas_a, columnas_a, columnas_b
