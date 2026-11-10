"""Compara Gauss-Jordan exacto, su recorrido flotante y NumPy.

Tema: semana 12; error, residuo y condicionamiento de matrices casi singulares.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction

import numpy as np

from modulos.eliminacion import reemplazar_fila
from modulos.modulo_matrices import calcular_inversa, identidad
from modulos.modulo_sistemas import resolver_sistema
from modulos.numericos.funciones import formato
from modulos.procedimientos import Calculo, Paso
from modulos.validaciones import validar_cuadrada, validar_vector


def hilbert(orden=5):
    """Construye una Hilbert exacta de orden 1 a 10 para experimentar con su condición."""
    if type(orden) is not int or not 1 <= orden <= 10:
        raise ValueError('El orden de Hilbert debe ser de 1 a 10.')
    return [[Fraction(1, i + j + 1) for j in range(orden)] for i in range(orden)]


def jordan_flotante(aumentada, orden):
    """Aplica Gauss-Jordan con float y pivoteo parcial; reutiliza el reemplazo de filas."""
    matriz = [[float(v) for v in fila] for fila in aumentada]
    if not np.isfinite(matriz).all():
        raise ValueError('La conversión de los datos a float produjo valores no finitos.')
    pasos = []
    for columna in range(orden):
        pivote = max(range(columna, orden), key=lambda i: abs(matriz[i][columna]))
        if matriz[pivote][columna] == 0:
            raise ValueError('La matriz resulta singular en punto flotante.')
        if pivote != columna:
            matriz[columna], matriz[pivote] = matriz[pivote], matriz[columna]
            pasos.append(Paso(f'Intercambio flotante F{columna + 1} ↔ F{pivote + 1}', formulas=filas_formulas(matriz)))
        divisor = matriz[columna][columna]
        matriz[columna] = [v / divisor for v in matriz[columna]]
        pasos.append(Paso(f'Pivote flotante {columna + 1}', f'F{columna + 1} ← F{columna + 1}/({formato(divisor)})', formulas=filas_formulas(matriz)))
        for i in range(orden):
            if i == columna or matriz[i][columna] == 0:
                continue
            factor = matriz[i][columna]
            matriz = reemplazar_fila(matriz, i, columna, factor)
            pasos.append(Paso(f'Eliminación flotante F{i + 1}', f'F{i + 1} ← F{i + 1} − ({formato(factor)})F{columna + 1}', formulas=filas_formulas(matriz)))
    if not np.isfinite(matriz).all():
        raise ValueError('El procedimiento flotante produjo overflow o valores no finitos.')
    return [fila[orden:] for fila in matriz], pasos


def filas_formulas(matriz):
    """Presenta cada fila aproximada como texto, conservando la distinción con Fraction."""
    return tuple((f'F{i + 1}', '=', '[' + ', '.join(formato(v) for v in fila) + ']') for i, fila in enumerate(matriz))


def comparar(matriz, vector_b=None):
    """Devuelve errores frente a Fraction, residuo y cond(A); compara inversa o sistema."""
    orden = validar_cuadrada(matriz)
    pasos = [Paso('Datos originales exactos', matriz=[f[:] for f in matriz])]
    if vector_b is None:
        calculo_exacto = calcular_inversa(matriz)
        exacto = calculo_exacto.valor
        pasos.extend(calculo_exacto.pasos)
        aumentada = [fila[:] + unidad for fila, unidad in zip(matriz, identidad(orden))]
        derecha = np.eye(orden)
    else:
        validar_vector(vector_b, orden)
        sistema = resolver_sistema(matriz, vector_b, 'jordan')
        if sistema.datos['clasificacion'] != 'unica':
            raise ValueError('La comparación requiere un sistema cuadrado con solución única.')
        exacto = [[v] for v in sistema.valor]
        pasos.extend(sistema.pasos)
        aumentada = [fila[:] + [b] for fila, b in zip(matriz, vector_b)]
        derecha = np.array([[float(v)] for v in vector_b])
    pasos.append(Paso('Resultado con fracciones', matriz=exacto))
    flotante, recorrido = jordan_flotante(aumentada, orden)
    pasos.extend(recorrido)
    a = np.array([[float(v) for v in fila] for fila in matriz])
    try:
        referencia = np.linalg.inv(a) if vector_b is None else np.linalg.solve(a, derecha)
        condicion = float(np.linalg.cond(a))
    except np.linalg.LinAlgError:
        raise ValueError('NumPy detectó una matriz singular en la representación flotante.') from None
    filas = []
    for i, fila in enumerate(exacto):
        for j, valor in enumerate(fila):
            # Comparamos con Fraction.from_float para no ocultar el redondeo al convertir la referencia.
            diferencia = abs(Fraction.from_float(flotante[i][j]) - valor)
            error = float(diferencia)
            relativo = float(diferencia / abs(valor)) if valor != 0 else None
            filas.append((f'[{i + 1},{j + 1}]', str(valor), flotante[i][j], float(referencia[i, j]), error, relativo))
    residuo = float(np.max(np.abs(a @ np.array(flotante) - derecha)))
    residuo_numpy = float(np.max(np.abs(a @ referencia - derecha)))
    pasos.append(Paso('Errores, residuo y condicionamiento', 'Un residuo pequeño no garantiza un error pequeño cuando A está mal condicionada.',
                       formulas=((f'cond(A)={formato(condicion)}', f'Residuo propio={formato(residuo)}', f'Residuo NumPy={formato(residuo_numpy)}'),)))
    for fila in filas:
        pasos.append(Paso('Comparación ' + fila[0], formulas=((f'Exacto={fila[1]}', f'Float={formato(fila[2])}', f'NumPy={formato(fila[3])}'),
                          (f'Error absoluto={formato(fila[4])}', f'Error relativo={formato(fila[5])}'))))
    return Calculo(flotante, tuple(pasos), dict(filas=filas, columnas=('Posición', 'Exacto', 'Float propio', 'NumPy', 'Error absoluto', 'Error relativo'),
                   exacto=exacto, residuo=residuo, residuo_numpy=residuo_numpy, condicion=condicion))
