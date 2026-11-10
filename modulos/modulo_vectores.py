"""Opera vectores y reutiliza sistemas para combinación e independencia.

Tema: operaciones en Rⁿ y tareas 3 y 4.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from modulos.modulo_matrices import multiplicar_por_escalar, restar_matrices, sumar_matrices, transponer_matriz
from modulos.modulo_sistemas import resolver_sistema
from modulos.procedimientos import Calculo, Paso
from modulos.validaciones import validar_matriz, validar_vector


def sumar_vectores(vector_a, vector_b):
    """Devuelve u+v reutilizando la suma de matrices fila."""
    validar_vector(vector_a)
    validar_vector(vector_b, len(vector_a))
    return sumar_matrices([vector_a], [vector_b])[0]


def restar_vectores(vector_a, vector_b):
    """Devuelve u−v reutilizando la resta de matrices fila."""
    validar_vector(vector_a)
    validar_vector(vector_b, len(vector_a))
    return restar_matrices([vector_a], [vector_b])[0]


def escalar_vector(vector, escalar):
    """Devuelve kv reutilizando el producto de una matriz por escalar."""
    validar_vector(vector)
    return multiplicar_por_escalar([vector], escalar)[0]


def matriz_de_vectores(vectores):
    """Recibe una lista de vectores y los dispone como columnas de A."""
    validar_matriz(vectores)
    # Los coeficientes multiplican columnas: Ac=b usa una columna por vector.
    return transponer_matriz(vectores)


def combinacion_lineal(vectores, objetivo):
    """Resuelve Ac=b; devuelve coeficientes particulares, parámetros y pertenencia."""
    matriz = matriz_de_vectores(vectores)
    calculo = resolver_sistema(matriz, objetivo, "jordan")
    datos = dict(calculo.datos, pertenece=calculo.datos["clasificacion"] != "sin_solucion")
    inicio = Paso("Vectores como columnas", "Buscamos coeficientes c tales que Ac=b.", matriz)
    return Calculo(calculo.valor, (inicio,) + calculo.pasos, datos)


def independencia_lineal(vectores):
    """Resuelve Ac=0 y devuelve L.I./L.D. con una relación no trivial si existe."""
    matriz = matriz_de_vectores(vectores)
    calculo = resolver_sistema(matriz, [0] * len(matriz), "jordan")
    independiente = not calculo.datos["libres"]
    relacion = None if independiente else calculo.datos["base"][0][:]
    datos = dict(calculo.datos, independiente=independiente, relacion=relacion)
    diagnostico = Paso("L.I." if independiente else "L.D.", "Solo existe la solución trivial." if independiente else "Hay variables libres: la relación mostrada es no trivial y produce el vector cero.", [[v] for v in relacion] if relacion is not None else None)
    return Calculo(independiente, calculo.pasos + (diagnostico,), datos)
