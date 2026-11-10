"""Calcula las operaciones básicas de matrices conservando las entradas.

Tema: operaciones de matrices de los Programas 3 y 5.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction

from modulos.validaciones import validar_matriz, validar_mismo_tamano, validar_producto
from modulos.validaciones import validar_cuadrada
from modulos.eliminacion import reducir
from modulos.modulo_determinantes import calcular_determinante, determinante_reduccion, expandir_cofactores, menor
from modulos.procedimientos import Calculo, ErrorCalculo, Paso


def identidad(orden):
    """Devuelve una identidad nueva de orden entero positivo."""
    if isinstance(orden, bool) or not isinstance(orden, int) or orden < 1:
        raise ValueError("El orden de la identidad debe ser un entero positivo.")
    return [[int(i == j) for j in range(orden)] for i in range(orden)]


def son_iguales(matriz_a, matriz_b):
    """Compara matrices exactas validadas, incluidas sus dimensiones."""
    validar_matriz(matriz_a)
    validar_matriz(matriz_b)
    return matriz_a == matriz_b


def calcular_inversa(matriz, metodo="jordan"):
    """Devuelve Calculo(inversa, pasos, verificación); singularidad produce ErrorCalculo."""
    orden = validar_cuadrada(matriz)
    if metodo == "jordan":
        aumentada = [fila[:] + unidad for fila, unidad in zip(matriz, identidad(orden))]
        # Los pivotes se buscan solo en A; las columnas de I acompañan las operaciones.
        reduccion = reducir(aumentada, reducida=True, columnas_pivote=orden)
        if len(reduccion.pivotes) != orden:
            raise ErrorCalculo(f"La matriz es singular: {len(reduccion.pivotes)} pivotes de {orden}; no tiene inversa.", reduccion.pasos)
        inversa = [fila[orden:] for fila in reduccion.matriz]
        pasos = list(reduccion.pasos)
    elif metodo == "adjunta":
        calculo_det = calcular_determinante(matriz)
        determinante = calculo_det.valor
        if determinante == 0:
            raise ErrorCalculo("La matriz es singular: det(A)=0; no tiene inversa.", calculo_det.pasos)
        pasos = list(calculo_det.pasos)
        cofactores = []
        for i in range(orden):
            fila = []
            for j in range(orden):
                submatriz = menor(matriz, i, j)
                pasos.append(Paso(f"Menor M[{i + 1},{j + 1}]", "Suprimimos la fila y columna indicadas." if submatriz else "El menor vacío de una matriz 1×1 tiene determinante 1.", submatriz or None))
                valor = expandir_cofactores(submatriz, pasos, f"M{i + 1}{j + 1}")
                cofactor = (-1) ** (i + j) * valor
                fila.append(cofactor)
                pasos.append(Paso(f"Cofactor C[{i + 1},{j + 1}]", formulas=((f"(-1)^{i + j + 2}", "×", "(", valor, ")", "=", cofactor),)))
            cofactores.append(fila)
        pasos.append(Paso("Matriz de cofactores", matriz=[f[:] for f in cofactores]))
        adjunta = transponer_matriz(cofactores)
        pasos.append(Paso("adj(A) = Cᵀ", matriz=[f[:] for f in adjunta]))
        inversa = multiplicar_por_escalar(adjunta, Fraction(1) / determinante)
        for i, fila in enumerate(adjunta):
            for j, valor in enumerate(fila):
                pasos.append(Paso(f"Inversa [{i + 1},{j + 1}]", formulas=((valor, "÷", "(", determinante, ")", "=", inversa[i][j]),)))
    else:
        raise ValueError("El método de inversa debe ser jordan o adjunta.")
    producto = producto_matricial(matriz, inversa)
    verificado = son_iguales(producto, identidad(orden))
    pasos.append(Paso("Comprobación A·A⁻¹ = I", "Se cumple" if verificado else "No se cumple", producto))
    return Calculo(inversa, tuple(pasos), dict(verificado=verificado))


def inversa_gauss_jordan(matriz):
    """Devuelve A⁻¹ por [A|I] → [I|A⁻¹], sin construir el desarrollo visual."""
    orden = validar_cuadrada(matriz)
    reduccion = reducir([fila[:] + unidad for fila, unidad in zip(matriz, identidad(orden))],
                        reducida=True, columnas_pivote=orden, registrar=False)
    if len(reduccion.pivotes) != orden:
        raise ValueError("La matriz es singular; no tiene inversa.")
    return [fila[orden:] for fila in reduccion.matriz]


def inversa_adjunta(matriz):
    """Devuelve A⁻¹ por cofactores y adjunta; exige determinante no nulo."""
    return calcular_inversa(matriz, "adjunta").valor


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


def multiplicar_por_escalar(matriz, escalar):
    """Devuelve kA como matriz nueva; admite solo enteros y Fraction exactos."""
    filas, columnas = validar_matriz(matriz)
    if isinstance(escalar, bool) or not isinstance(escalar, (int, Fraction)):
        raise ValueError("El escalar debe ser un entero o una fracción exacta.")
    resultado = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(escalar * matriz[i][j])
        resultado.append(fila)
    return resultado


def transponer_matriz(matriz):
    """Devuelve A transpuesta como filas nuevas; intercambia m×n por n×m."""
    filas, columnas = validar_matriz(matriz)
    resultado = []
    for j in range(columnas):
        fila = []
        for i in range(filas):
            fila.append(matriz[i][j])
        resultado.append(fila)
    return resultado


def producto_matricial(matriz_a, matriz_b):
    """Devuelve AB como matriz nueva, acumulando los productos fila por columna."""
    filas, comunes, columnas = validar_producto(matriz_a, matriz_b)
    resultado = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            acumulado = 0
            for k in range(comunes):
                acumulado += matriz_a[i][k] * matriz_b[k][j]
            fila.append(acumulado)
        resultado.append(fila)
    return resultado
