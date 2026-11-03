"""Convierte las entradas numéricas de consola y ventana.

Tema: lectura exacta de enteros, decimales y fracciones.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction


def convertir_numero(texto):
    """Recibe texto numérico y devuelve Fraction; rechaza valores inválidos."""
    # Pasar por float introduciría redondeo antes de obtener la fracción.
    return Fraction(texto.strip())
