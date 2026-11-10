"""Factoriza A=LU sin permutación y resuelve Ly=b, Ux=y.

Tema: tarea 6; multiplicadores, matrices rectangulares y comprobaciones.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from modulos.eliminacion import reducir
from modulos.modulo_matrices import identidad, producto_matricial, son_iguales
from modulos.modulo_sistemas import resolver_sistema
from modulos.procedimientos import Calculo, ErrorCalculo, Paso
from modulos.validaciones import validar_matriz, validar_vector


def factorizar_lu(matriz):
    """Devuelve Calculo((L,U), pasos, verificado), con L m×m y U m×n."""
    filas, _ = validar_matriz(matriz)
    reduccion = reducir(matriz, intercambiar=False)
    inferior = identidad(filas)
    pasos = list(reduccion.pasos)
    for destino, origen, factor in reduccion.multiplicadores:
        # El mismo factor que creó un cero en U se conserva en L para reconstruir A.
        inferior[destino][origen] = factor
        pasos.append(Paso(f"Registramos l[{destino + 1},{origen + 1}] = {factor}", matriz=[f[:] for f in inferior]))
    producto = producto_matricial(inferior, reduccion.matriz)
    verificado = son_iguales(producto, matriz)
    pasos.extend((Paso("L · Triangular inferior", matriz=[f[:] for f in inferior]),
                  Paso("U · Forma escalonada", matriz=[f[:] for f in reduccion.matriz]),
                  Paso("Comprobación L·U = A", "Se cumple" if verificado else "No se cumple", producto)))
    return Calculo((inferior, reduccion.matriz), tuple(pasos), dict(verificado=verificado))


def resolver_lu(matriz, vector_b):
    """Encadena LU, Ly=b y Ux=y; devuelve x e información de y y verificación."""
    filas, columnas = validar_matriz(matriz)
    validar_vector(vector_b, filas)
    if filas != columnas:
        raise ValueError("Resolver por LU requiere A cuadrada; la factorización sí admite matrices rectangulares.")
    factorizacion = factorizar_lu(matriz)
    inferior, superior = factorizacion.valor
    intermedio = resolver_sistema(inferior, vector_b)
    solucion = resolver_sistema(superior, intermedio.valor)
    pasos = list(factorizacion.pasos) + [Paso("Resolvemos Ly=b")] + list(intermedio.pasos)
    pasos += [Paso("Resolvemos Ux=y")] + list(solucion.pasos)
    if solucion.datos["clasificacion"] != "unica":
        raise ErrorCalculo("La matriz es singular: LU existe, pero este sistema no tiene solución única por sustitución LU. Consulta Gauss-Jordan para su clasificación general.", pasos)
    producto = producto_matricial(matriz, [[v] for v in solucion.valor])
    verificado = producto == [[v] for v in vector_b]
    pasos.append(Paso("Comprobación final A·x = b", "Se cumple" if verificado else "No se cumple", producto))
    return Calculo(solucion.valor, tuple(pasos), dict(L=inferior, U=superior, y=intermedio.valor, verificado=verificado))
