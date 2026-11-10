"""Comparte la reducción exacta y las operaciones elementales por filas.

Tema: formas escalonada y reducida, pivotes y multiplicadores.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from dataclasses import dataclass
from fractions import Fraction

from modulos.procedimientos import ErrorCalculo, Paso
from modulos.validaciones import validar_matriz


@dataclass(frozen=True)
class Reduccion:
    """Devuelve matriz nueva, columnas pivote de base cero, pasos y eliminaciones."""

    matriz: list
    pivotes: tuple
    pasos: tuple
    intercambios: int
    multiplicadores: tuple


def copiar_exacta(matriz):
    """Valida y copia una matriz convirtiendo cada valor a Fraction."""
    validar_matriz(matriz)
    return [[Fraction(valor) for valor in fila] for fila in matriz]


def reemplazar_fila(matriz, destino, origen, factor):
    """Devuelve una matriz nueva con Fdestino ← Fdestino − factor Forigen."""
    nueva = [fila[:] for fila in matriz]
    nueva[destino] = [a - factor * b for a, b in zip(matriz[destino], matriz[origen])]
    return nueva


def formulas_reemplazo(matriz, destino, origen, factor):
    """Expone cada componente del reemplazo sin omitir las columnas aumentadas."""
    return tuple((f"c{j + 1}:", a, "−", "(", factor, "×", "(", b, ")", ")", "=", a - factor * b)
                 for j, (a, b) in enumerate(zip(matriz[destino], matriz[origen])))


def reducir(matriz, reducida=False, columnas_pivote=None, intercambiar=True, registrar=True):
    """Obtiene REF/RREF sin mutar entradas; limita pivotes al bloque de coeficientes.

    Los multiplicadores (fila destino, fila pivote, factor) corresponden a la
    eliminación inferior antes de normalizar; LU pide intercambiar=False.
    """
    actual = copiar_exacta(matriz)
    filas, columnas = len(actual), len(actual[0])
    limite = columnas if columnas_pivote is None else columnas_pivote
    if isinstance(limite, bool) or not isinstance(limite, int) or not 1 <= limite <= columnas:
        raise ValueError("El número de columnas de coeficientes no es válido.")
    corte = limite if limite < columnas else None
    pasos = [Paso("Matriz inicial", matriz=[f[:] for f in actual], separador=corte)] if registrar else []
    pivotes, multiplicadores, cambios = [], [], 0
    for columna in range(limite):
        fila_pivote = len(pivotes)
        if fila_pivote == filas:
            break
        candidata = next((i for i in range(fila_pivote, filas) if actual[i][columna] != 0), None)
        if candidata is None:
            # Una columna sin pivote puede corresponder a una variable libre; no es un error.
            continue
        if candidata != fila_pivote:
            if not intercambiar:
                raise ErrorCalculo("La matriz no admite factorización LU sin permutación: requiere pivoteo parcial PA = LU.", pasos)
            actual[fila_pivote], actual[candidata] = actual[candidata], actual[fila_pivote]
            cambios += 1
            if registrar:
                pasos.append(Paso(f"F{fila_pivote + 1} ↔ F{candidata + 1}", "El pivote era cero; intercambiamos filas.", [f[:] for f in actual], separador=corte))
        for i in range(fila_pivote + 1, filas):
            if actual[i][columna] == 0:
                continue
            factor = actual[i][columna] / actual[fila_pivote][columna]
            formulas = ((("l", "=", actual[i][columna], "÷", actual[fila_pivote][columna], "=", factor),)
                        + formulas_reemplazo(actual, i, fila_pivote, factor)) if registrar else ()
            actual = reemplazar_fila(actual, i, fila_pivote, factor)
            multiplicadores.append((i, fila_pivote, factor))
            if registrar:
                pasos.append(Paso(f"F{i + 1} ← F{i + 1} − ({factor}) F{fila_pivote + 1}", "Creamos un cero debajo del pivote.", [f[:] for f in actual], formulas, corte))
        pivotes.append(columna)
    if reducida:
        # La segunda fase normaliza y elimina arriba; REF conserva los factores de LU.
        actual = completar_reducida(actual, pivotes, pasos if registrar else None, corte)
    return Reduccion(actual, tuple(pivotes), tuple(pasos), cambios, tuple(multiplicadores))


def completar_reducida(matriz, pivotes, pasos, corte):
    """Normaliza los pivotes y anula por encima; registra cada operación completa."""
    actual = matriz
    for i in range(len(pivotes) - 1, -1, -1):
        pivote = actual[i][pivotes[i]]
        if pivote != 1:
            formulas = tuple((f"c{j + 1}:", valor, "÷", "(", pivote, ")", "=", valor / pivote)
                             for j, valor in enumerate(actual[i])) if pasos is not None else ()
            actual = [fila[:] for fila in actual]
            actual[i] = [valor / pivote for valor in actual[i]]
            if pasos is not None:
                pasos.append(Paso(f"F{i + 1} ← F{i + 1} / ({pivote})", "Normalizamos el pivote a 1.", [f[:] for f in actual], formulas, corte))
        for destino in range(i):
            factor = actual[destino][pivotes[i]]
            if factor == 0:
                continue
            formulas = formulas_reemplazo(actual, destino, i, factor) if pasos is not None else ()
            actual = reemplazar_fila(actual, destino, i, factor)
            if pasos is not None:
                pasos.append(Paso(f"F{destino + 1} ← F{destino + 1} − ({factor}) F{i + 1}", "Creamos un cero encima del pivote.", [f[:] for f in actual], formulas, corte))
    return actual
