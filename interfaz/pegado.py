"""Convierte bloques pegados en matrices exactas antes de tocar las casillas.

Tema: entrada de filas desde texto, hojas de cálculo y listas entre corchetes.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import re

from interfaz.datos import convertir_numero
from modulos.validaciones import validar_matriz


def interpretar_matriz(texto, limite=10):
    """Acepta filas por salto de línea/; y columnas por espacios, tabuladores o comas."""
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError('No hay una matriz para pegar.')
    balance = 0
    for caracter in texto:
        balance += int(caracter == '[') - int(caracter == ']')
        if balance < 0:
            raise ValueError('Los corchetes de la matriz no están completos.')
    if balance:
        raise ValueError('Los corchetes de la matriz no están completos.')
    texto = re.sub(r'\]\s*,\s*\[', '\n', texto.strip())
    texto = texto.replace('[', '').replace(']', '').replace(';', '\n')
    filas = [fila.strip() for fila in texto.splitlines() if fila.strip()]
    if len(filas) > limite:
        raise ValueError(f'Se admiten hasta {limite} filas.')
    matriz = []
    for indice, fila in enumerate(filas, 1):
        columnas = fila.split(',') if ',' in fila else fila.split()
        if not columnas or len(columnas) > limite:
            raise ValueError(f'La fila {indice} debe tener de 1 a {limite} columnas.')
        try:
            matriz.append([convertir_numero(valor.strip()) for valor in columnas])
        except (ValueError, ZeroDivisionError):
            raise ValueError(f'Número no válido en la fila {indice}. Usa fracciones o decimales con punto.') from None
    validar_matriz(matriz)
    return matriz


def texto_matriz(matriz):
    """Copia una matriz como filas tabuladas que conservan las fracciones exactas."""
    validar_matriz(matriz)
    return '\n'.join('\t'.join(str(v) for v in fila) for fila in matriz)
