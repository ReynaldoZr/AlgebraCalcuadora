"""Calcula determinantes por cofactores, Sarrus y reducción exacta.

Tema: tarea 5; menores, signos de cofactores y operaciones de fila.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from modulos.eliminacion import reducir
from modulos.procedimientos import Calculo, Paso
from modulos.validaciones import validar_cuadrada


def menor(matriz, fila, columna):
    """Devuelve una matriz nueva suprimiendo la fila y columna indicadas (base cero)."""
    return [[valor for j, valor in enumerate(valores) if j != columna]
            for i, valores in enumerate(matriz) if i != fila]


def expandir_cofactores(matriz, pasos=None, nombre="A"):
    """Expande por la primera fila; el menor vacío tiene determinante 1."""
    if not matriz:
        # Esta convención permite calcular la adjunta de una matriz 1×1.
        return 1
    if len(matriz) == 1:
        valor = matriz[0][0]
        if pasos is not None:
            pasos.append(Paso(f"det({nombre}) de orden 1", formulas=((f"det({nombre})", "=", valor),)))
        return valor
    total, terminos = 0, []
    for j, coeficiente in enumerate(matriz[0]):
        signo = (-1) ** j
        if coeficiente == 0:
            if pasos is not None:
                pasos.append(Paso(f"Término {nombre}[1,{j + 1}]", "El coeficiente es cero; su término vale cero.", formulas=((0, "×", f"C[1,{j + 1}]", "=", 0),)))
            terminos.append(0)
            continue
        submatriz = menor(matriz, 0, j)
        etiqueta = f"{nombre}.M1{j + 1}"
        if pasos is not None:
            pasos.append(Paso(f"Menor {etiqueta}", f"Suprimimos fila 1 y columna {j + 1}. Signo (-1)^(1+{j + 1}) = {signo}.", submatriz))
        determinante = expandir_cofactores(submatriz, pasos, etiqueta)
        termino = coeficiente * signo * determinante
        total += termino
        terminos.append(termino)
        if pasos is not None:
            pasos.append(Paso(f"Cofactor y término de {nombre}[1,{j + 1}]", formulas=(
                (f"C[1,{j + 1}]", "=", signo, "×", "(", determinante, ")", "=", signo * determinante),
                (coeficiente, "×", "(", signo * determinante, ")", "=", termino))))
    if pasos is not None:
        tokens = []
        for termino in terminos:
            if tokens:
                tokens.append("+")
            tokens += ["(", termino, ")"]
        pasos.append(Paso(f"Sumamos la expansión de {nombre}", formulas=(tuple(tokens + ["=", total]),)))
    return total


def determinante_cofactores(matriz):
    """Devuelve det(A) mediante expansión propia; requiere A cuadrada."""
    validar_cuadrada(matriz)
    return expandir_cofactores(matriz)


def calcular_determinante(matriz, metodo="reduccion"):
    """Devuelve Calculo(det, pasos, datos) con uno de los tres métodos exigidos."""
    orden = validar_cuadrada(matriz)
    if metodo == "cofactores":
        pasos = [Paso("Expansión por cofactores", "Expandimos por la primera fila de cada menor.", [f[:] for f in matriz])]
        valor = expandir_cofactores(matriz, pasos)
        return Calculo(valor, tuple(pasos))
    if metodo == "sarrus":
        if orden != 3:
            raise ValueError("Sarrus se aplica únicamente a matrices 3×3.")
        positivos, negativos, pasos = [], [], [Paso("Regla de Sarrus", matriz=[f[:] for f in matriz])]
        for j in range(3):
            for signo, terminos, direccion in ((1, positivos, 1), (-1, negativos, -1)):
                valores = [matriz[i][(j + direccion * i) % 3] for i in range(3)]
                producto = valores[0] * valores[1] * valores[2]
                terminos.append(producto)
                pasos.append(Paso(f"Diagonal {'positiva' if signo == 1 else 'negativa'} {j + 1}", formulas=(("(", valores[0], ")", "×", "(", valores[1], ")", "×", "(", valores[2], ")", "=", producto),)))
        valor = sum(positivos) - sum(negativos)
        pasos.append(Paso("Positivas menos negativas", formulas=(("(", *intercalar(positivos), ")", "−", "(", *intercalar(negativos), ")", "=", valor),)))
        return Calculo(valor, tuple(pasos))
    if metodo != "reduccion":
        raise ValueError("Método de determinante no reconocido.")
    reduccion = reducir(matriz)
    producto = 1
    for i in range(orden):
        producto *= reduccion.matriz[i][i]
    valor = (-1) ** reduccion.intercambios * producto
    pasos = list(reduccion.pasos)
    pasos.append(Paso("Determinante de la triangular", "Los reemplazos conservan det; cada intercambio cambia su signo. No se escalaron filas.", formulas=(("det(A)", "=", f"(-1)^{reduccion.intercambios}", "×", *intercalar([reduccion.matriz[i][i] for i in range(orden)], "×"), "=", valor),)))
    return Calculo(valor, tuple(pasos), dict(triangular=reduccion.matriz, intercambios=reduccion.intercambios))


def intercalar(valores, signo="+"):
    """Forma tokens de una suma o producto con todos los valores agrupados."""
    tokens = []
    for valor in valores:
        if tokens:
            tokens.append(signo)
        tokens += ["(", valor, ")"]
    return tokens


def determinante_reduccion(matriz):
    """Devuelve det(A) sin construir pasos, conservando el signo de los intercambios."""
    orden = validar_cuadrada(matriz)
    reduccion = reducir(matriz, registrar=False)
    producto = (-1) ** reduccion.intercambios
    for i in range(orden):
        producto *= reduccion.matriz[i][i]
    return producto


def determinante_sarrus(matriz):
    """Devuelve det(A) por las seis diagonales de una matriz 3×3."""
    return calcular_determinante(matriz, "sarrus").valor
