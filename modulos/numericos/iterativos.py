"""Resuelve sistemas por Jacobi con validaciones reutilizables.

Tema: Programa 8, aproximaciones sucesivas y dominancia diagonal.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import math

from modulos.numericos.funciones import formato, numero_finito
from modulos.procedimientos import Calculo, Paso


def vector_numerico(vector, dimension, nombre):
    """Convierte un vector de la dimensión indicada a una lista independiente de float."""
    if not isinstance(vector, (list, tuple)) or len(vector) != dimension:
        raise ValueError(f'{nombre} debe tener {dimension} componentes.')
    return [numero_finito(v, f'{nombre}[{i + 1}]') for i, v in enumerate(vector)]


def validar_datos_iterativos(matriz, vector_b, inicial, tolerancia, max_iteraciones):
    """Devuelve copias numéricas de A, B, X₀ y tolerancia tras validar sus condiciones."""
    if not isinstance(matriz, (list, tuple)) or not matriz:
        raise ValueError('A debe ser una matriz cuadrada no vacía.')
    orden = len(matriz)
    a = [vector_numerico(fila, orden, f'Fila {i + 1} de A')
         for i, fila in enumerate(matriz)]
    b = vector_numerico(vector_b, orden, 'B')
    x = vector_numerico(inicial, orden, 'X₀')
    tolerancia = numero_finito(tolerancia, 'Tolerancia')
    if tolerancia <= 0:
        raise ValueError('La tolerancia debe ser positiva.')
    if type(max_iteraciones) is not int or not 1 <= max_iteraciones <= 10000:
        raise ValueError('El máximo debe ser un entero entre 1 y 10000.')
    if any(fila[i] == 0 for i, fila in enumerate(a)):
        raise ValueError('La diagonal contiene un cero. Reordena las ecuaciones antes de iterar.')
    return a, b, x, tolerancia


def dominancia_diagonal(matriz):
    """Indica por fila si la diagonal domina estrictamente a los demás coeficientes."""
    # Escalar cada fila evita desbordar la suma de magnitudes grandes.
    dominante = []
    for i, fila in enumerate(matriz):
        escala = max(abs(v) for v in fila)
        suma = math.fsum(abs(v) / escala for j, v in enumerate(fila) if j != i) if escala else 0
        dominante.append(bool(escala and abs(fila[i]) / escala > suma))
    return tuple(dominante)


def jacobi(matriz, vector_b, inicial, tolerancia=0.0001, max_iteraciones=200):
    """Devuelve Calculo con el último vector, pasos y tabla usando el error máximo absoluto."""
    a, b, x, tolerancia = validar_datos_iterativos(
        matriz, vector_b, inicial, tolerancia, max_iteraciones,
    )
    dominantes = dominancia_diagonal(a)
    aviso = ('La diagonal es estrictamente dominante y garantiza convergencia.'
             if all(dominantes) else
             'Falta dominancia diagonal estricta. La convergencia no está garantizada.')
    datos = dict(
        metodo='Jacobi', matriz=a, vector_b=b, inicial=x[:],
        tolerancia=tolerancia, max_iteraciones=max_iteraciones,
        dominantes=dominantes, convergio=False, filas=[], error=None,
        columnas=('k',) + tuple(f'x{i + 1}' for i in range(len(x))) + ('Error máximo',),
        motivo='Se alcanzó el máximo de iteraciones sin cumplir la tolerancia.',
    )
    pasos = [Paso('Datos de Jacobi', aviso, matriz=[fila[:] + [b[i]] for i, fila in enumerate(a)],
                  separador=len(a), formulas=((f'X₀={x}', f'Tolerancia={formato(tolerancia)}'),))]
    for k in range(1, max_iteraciones + 1):
        # Todos los componentes usan x, que conserva la iteración anterior completa.
        try:
            nuevo = [(b[i] - math.fsum(v * x[j] for j, v in enumerate(fila) if j != i)) / fila[i]
                     for i, fila in enumerate(a)]
            error = max(abs(v - anterior) for v, anterior in zip(nuevo, x))
            if not all(math.isfinite(v) for v in nuevo) or not math.isfinite(error):
                raise OverflowError
        except (OverflowError, ValueError):
            datos['motivo'] = 'La iteración produjo valores no finitos. Se conserva el último vector finito.'
            break
        datos['filas'].append((k, *nuevo, error))
        datos['error'] = error
        pasos.append(Paso(
            f'Iteración {k} de Jacobi', 'Calculamos cada componente con el vector anterior.',
            formulas=tuple((f'x{i + 1}={formato(v)}',) for i, v in enumerate(nuevo))
            + ((f'Error máximo={formato(error)}',),),
        ))
        x = nuevo
        if error < tolerancia:
            datos.update(convergio=True, motivo='La diferencia máxima es menor que la tolerancia.')
            break
    pasos.append(Paso('Terminación de Jacobi', datos['motivo'], formulas=((f'X={x}',),)))
    return Calculo(x[:], tuple(pasos), datos)
