"""Comprueba la estructura y las dimensiones de las matrices.

Tema: condiciones para operar con matrices rectangulares.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction


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
