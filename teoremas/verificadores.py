"""Comprueba ambos miembros de las propiedades exigidas en las tareas 5 y 6.

Tema: operaciones, transpuesta, inversa, determinantes y equivalencia de métodos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from dataclasses import dataclass
from fractions import Fraction

from modulos.eliminacion import reemplazar_fila
from modulos.modulo_determinantes import determinante_cofactores, determinante_reduccion, determinante_sarrus
from modulos.modulo_matrices import (identidad, inversa_adjunta, inversa_gauss_jordan,
                                     multiplicar_por_escalar, producto_matricial, sumar_matrices,
                                     transponer_matriz)
from modulos.validaciones import validar_cuadrada

PROPIEDADES = {
    "transpuesta_doble": "(Aᵀ)ᵀ = A",
    "transpuesta_suma": "(A+B)ᵀ = Aᵀ+Bᵀ",
    "transpuesta_escalar": "(kA)ᵀ = kAᵀ",
    "transpuesta_producto": "(AB)ᵀ = BᵀAᵀ",
    "distributividad": "A(B+C) = AB+AC",
    "asociatividad": "(AB)C = A(BC)",
    "inversa_doble": "(A⁻¹)⁻¹ = A",
    "inversa_producto": "(AB)⁻¹ = B⁻¹A⁻¹",
    "inversa_transpuesta": "(Aᵀ)⁻¹ = (A⁻¹)ᵀ",
    "inversa_identidad": "A·A⁻¹ = I",
    "det_transpuesta": "det(Aᵀ) = det(A)",
    "det_producto": "det(AB) = det(A)·det(B)",
    "det_inversa": "det(A⁻¹) = 1/det(A)",
    "det_escalar": "det(kA) = kⁿ det(A)",
    "fila_intercambio": "Intercambiar F1 y F2 cambia el signo de det",
    "fila_reemplazo": "F2 ← F2 − kF1 conserva det",
    "fila_escalar": "F1 ← kF1 multiplica det por k",
    "det_triangular": "det(T) = producto de su diagonal",
    "metodos_determinante": "Cofactores = reducción",
    "metodo_sarrus": "Sarrus = reducción (3×3)",
    "metodos_inversa": "Inversa por Gauss-Jordan = inversa por adjunta",
}


@dataclass(frozen=True)
class Verificacion:
    """Conserva ambos miembros; cumple=None significa propiedad no aplicable."""

    propiedad: str
    izquierda: object = None
    derecha: object = None
    cumple: bool | None = None
    motivo: str = ""


def efecto_fila(matriz, tipo, escalar):
    """Construye una copia con intercambio, reemplazo o escalado de filas."""
    orden = validar_cuadrada(matriz)
    multiplicar_por_escalar(matriz, escalar)
    if tipo != "escalar" and orden < 2:
        raise ValueError("Esta propiedad necesita al menos dos filas.")
    nueva = [fila[:] for fila in matriz]
    if tipo == "intercambio":
        nueva[0], nueva[1] = nueva[1], nueva[0]
    elif tipo == "reemplazo":
        nueva = reemplazar_fila(nueva, 1, 0, escalar)
    else:
        nueva[0] = [escalar * valor for valor in nueva[0]]
    return nueva


def producto_diagonal(matriz):
    """Devuelve el producto diagonal solo si A es triangular superior o inferior."""
    orden = validar_cuadrada(matriz)
    superior = all(matriz[i][j] == 0 for i in range(orden) for j in range(i))
    inferior = all(matriz[i][j] == 0 for i in range(orden) for j in range(i + 1, orden))
    if not superior and not inferior:
        raise ValueError("La matriz ingresada no es triangular.")
    producto = 1
    for i in range(orden):
        producto *= matriz[i][i]
    return producto


def verificar_propiedad(nombre, matriz_a, matriz_b=None, matriz_c=None, escalar=2):
    """Calcula ambos lados usando funciones del proyecto; informa precondiciones fallidas."""
    if nombre not in PROPIEDADES:
        raise ValueError("Propiedad desconocida.")
    a, b, c, k = matriz_a, matriz_b, matriz_c, escalar
    t, p, s, e = transponer_matriz, producto_matricial, sumar_matrices, multiplicar_por_escalar
    inv, det = inversa_gauss_jordan, determinante_reduccion
    evaluaciones = {
        "transpuesta_doble": lambda: (t(t(a)), [fila[:] for fila in a]),
        "transpuesta_suma": lambda: (t(s(a, b)), s(t(a), t(b))),
        "transpuesta_escalar": lambda: (t(e(a, k)), e(t(a), k)),
        "transpuesta_producto": lambda: (t(p(a, b)), p(t(b), t(a))),
        "distributividad": lambda: (p(a, s(b, c)), s(p(a, b), p(a, c))),
        "asociatividad": lambda: (p(p(a, b), c), p(a, p(b, c))),
        "inversa_doble": lambda: (inv(inv(a)), [fila[:] for fila in a]),
        "inversa_producto": lambda: (inv(p(a, b)), p(inv(b), inv(a))),
        "inversa_transpuesta": lambda: (inv(t(a)), t(inv(a))),
        "inversa_identidad": lambda: (p(a, inv(a)), identidad(validar_cuadrada(a))),
        "det_transpuesta": lambda: (det(t(a)), det(a)),
        "det_producto": lambda: (det(p(a, b)), det(a) * det(b)),
        "det_inversa": lambda: (det(inv(a)), Fraction(1) / det(a)),
        "det_escalar": lambda: (det(e(a, k)), k ** validar_cuadrada(a) * det(a)),
        "fila_intercambio": lambda: (det(efecto_fila(a, "intercambio", k)), -det(a)),
        "fila_reemplazo": lambda: (det(efecto_fila(a, "reemplazo", k)), det(a)),
        "fila_escalar": lambda: (det(efecto_fila(a, "escalar", k)), k * det(a)),
        "det_triangular": lambda: (det(a), producto_diagonal(a)),
        "metodos_determinante": lambda: (determinante_cofactores(a), det(a)),
        "metodo_sarrus": lambda: (determinante_sarrus(a), det(a)),
        "metodos_inversa": lambda: (inv(a), inversa_adjunta(a)),
    }
    try:
        # Cada función pendiente calcula ambos miembros solo de la propiedad elegida.
        izquierda, derecha = evaluaciones[nombre]()
    except ValueError as error:
        return Verificacion(PROPIEDADES[nombre], motivo=str(error))
    return Verificacion(PROPIEDADES[nombre], izquierda, derecha, izquierda == derecha)


def verificar_todas(matriz_a, matriz_b=None, matriz_c=None, escalar=2):
    """Evalúa el catálogo completo sin pedir reentrada de los resultados intermedios."""
    return [verificar_propiedad(nombre, matriz_a, matriz_b, matriz_c, escalar) for nombre in PROPIEDADES]
