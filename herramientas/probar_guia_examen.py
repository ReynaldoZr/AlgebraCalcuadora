"""Prueba ejercicios representativos de la guía final (Unidades I, II y IV).

Tema: verificación integral usando los mismos adaptadores de la calculadora.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from interfaz.metodos_numericos import ejecutar_numerico, parametros_defecto
from interfaz.qt.catalogo import ejecutar
from modulos.modulo_matrices import producto_matricial


def _como_texto(matriz):
    """Convierte una matriz numérica a cadenas exactas como las recibe la interfaz."""
    return [[str(v) for v in fila] for fila in matriz]


def _verificar_sistema_exacto(a, b, solucion):
    """Comprueba Ax = b en aritmética exacta Fraction."""
    for fila, bi in zip(a, b):
        total = sum(Fraction(coef) * val for coef, val in zip(fila, solucion))
        assert total == Fraction(bi[0]), f'Ax != b: {total} != {bi[0]}'


def probar_unidad_1():
    """Ejecuta y verifica ejercicios clave de sistemas, escalonada y vectores (1-60)."""
    a1 = [[1, 2, 1], [4, -2, -1], [2, -1, 3]]
    b1 = [[-6], [-4], [19]]
    pres1, _ = ejecutar('jordan', {'escalar': '1'}, {'A': _como_texto(a1), 'b': _como_texto(b1)})
    assert pres1.calculo.datos['clasificacion'] == 'unica'
    _verificar_sistema_exacto(a1, b1, pres1.calculo.valor)

    # Ej. 14: forma escalonada reducida
    a14 = [[1, 2, 4, 8], [2, 4, 6, 8], [3, 6, 9, 12]]
    pres14, _ = ejecutar('forma_escalonada', {'escalar': '1'}, {'A': _como_texto(a14)})
    assert pres14.matriz is not None

    # Ej. 17 (infinitas) y Ej. 23 (inconsistente)
    a17 = [[0, 0, 0, 1, 1], [1, 2, 3, 4, 5], [0, 1, 1, 1, 1], [0, 0, 1, 2, 3]]
    b17 = [[2], [10], [3], [4]]
    pres17, _ = ejecutar('jordan', {'escalar': '1'}, {'A': _como_texto(a17), 'b': _como_texto(b17)})
    assert pres17.calculo.datos['clasificacion'] == 'infinitas'

    a23 = [[1, 2, 3, 1], [2, 4, 6, 2], [1, 2, 3, 1]]
    b23 = [[4], [8], [5]]
    pres23, _ = ejecutar('jordan', {'escalar': '1'}, {'A': _como_texto(a23), 'b': _como_texto(b23)})
    assert pres23.calculo.datos['clasificacion'] == 'inconsistente'

    # Ej. 31 (Av), Ej. 39 (combinación), Ej. 48 (independencia)
    pres31, _ = ejecutar('multiplicar', {'escalar': '1'}, {
        'A': _como_texto([[1, 2, 0], [-1, 3, 2], [2, 0, -1]]),
        'B': _como_texto([[2], [-1], [3]]),
    })
    assert pres31.matriz == [[0], [1], [1]]

    pres48, _ = ejecutar('independencia', {'escalar': '1'}, {
        'A': _como_texto([[1, 1, 1], [-1, 1, 0], [0, 2, 1]]),
    })
    assert pres48.calculo.datos['independientes'] is False


def probar_unidad_2():
    """Ejecuta y verifica determinantes, inversas, Cramer y LU (61-100)."""
    # Ej. 69 y 70: determinantes
    pres69, _ = ejecutar('det_sarrus', {'escalar': '1'}, {'A': _como_texto([[3, 4, 1], [1, 1, 2], [2, 2, 1]])})
    assert pres69.calculo.valor == 3

    pres70, _ = ejecutar('det_reduccion', {'escalar': '1'}, {
        'A': _como_texto([[1, 0, 0, 3], [0, -1, 0, 4], [2, 3, 0, 0], [1, 5, -2, 6]]),
    })
    assert pres70.calculo.valor != 0

    # Ej. 79 (3x3), Ej. 80 (adjunta) y Ej. 86 (5x5)
    for clave, mat in (
        ('inv_jordan', [[2, 1, 1], [1, 3, 2], [1, 0, 0]]),
        ('inv_adjunta', [['1/2', '1/2', '0'], ['0', '1/2', '1/2'], ['1/2', '0', '1']]),
        ('inv_jordan', [[1, 0, 1, 2, 1], [2, 1, 0, 1, 1], [1, 2, 1, 0, 1], [0, 1, 2, 1, 2], [1, 0, 1, 1, 1]]),
    ):
        pres, _ = ejecutar(clave, {'escalar': '1'}, {'A': _como_texto(mat)})
        a_frac = [[Fraction(v) for v in fila] for fila in mat]
        prod = producto_matricial(a_frac, pres.matriz)
        n = len(a_frac)
        assert prod == [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]

    # Ej. 93: Cramer
    a93 = [[2, 1, 1], [3, -2, -3], [8, 2, 5]]
    b93 = [[6], [5], [11]]
    pres93, _ = ejecutar('cramer', {'escalar': '1'}, {'A': _como_texto(a93), 'b': _como_texto(b93)})
    _verificar_sistema_exacto(a93, b93, pres93.calculo.valor)

    # Ej. 96: LU con factores dados
    pres96, _ = ejecutar('lu_factores', {'escalar': '1'}, {
        'A': _como_texto([[2, -6, 4], [-4, 8, 0], [0, -4, 6]]),
        'L': _como_texto([[1, 0, 0], [-2, 1, 0], [0, 1, 1]]),
        'U': _como_texto([[2, -6, 4], [0, -4, 8], [0, 0, -2]]),
        'b': _como_texto([[2], [-4], [6]]),
    })
    _verificar_sistema_exacto([[2, -6, 4], [-4, 8, 0], [0, -4, 6]], [[2], [-4], [6]], pres96.calculo.valor)


def probar_unidad_4():
    """Ejecuta y verifica bases, errores, Maclaurin, bisección, Newton e iterativos (101-131)."""
    # Ej. 101a, 106, 107, 108
    c101 = ejecutar_numerico('num_bases', dict(parametros_defecto('num_bases'), modo_base='descomponer', numero='1101011', base='2', cifras='0'))
    assert abs(c101.valor - 107) < 1e-12

    c106 = ejecutar_numerico('num_propagacion', dict(parametros_defecto('num_propagacion'), funcion='x^3', x='2.5', delta='0.01'))
    assert c106.datos['estimacion'] > 0

    c107 = ejecutar_numerico('num_errores', dict(parametros_defecto('num_errores'), verdadero='10000', aproximado='9999'))
    assert abs(c107.datos['porcentual'] - 0.01) < 1e-9

    c108 = ejecutar_numerico('num_maclaurin', dict(parametros_defecto('num_maclaurin'), x='0.5', verdadero='1.648721', epsilon='0.05', maximo='20'))
    assert c108.datos['convergio']

    # Ej. 109 y 114: Bisección
    c109 = ejecutar_numerico('num_biseccion', dict(parametros_defecto('num_biseccion'), funcion='x^3-2*x-5', a='2', b='3', criterio='porcentual', tolerancia='0.01', parada='cambio', maximo='200'))
    assert abs(c109.datos['residuo']) < 1e-3

    c114 = ejecutar_numerico('num_biseccion', dict(parametros_defecto('num_biseccion'), funcion='x^3-x-2', a='1', b='2', criterio='porcentual', tolerancia='1.5', parada='cambio', maximo='6'))
    assert len(c114.datos['filas']) <= 6

    # Ej. 117, 119, 121: Newton-Raphson
    for expr, der, x0 in (
        ('x^3-x-2', '3*x^2-1', '1.5'),
        ('exp(-x)-x', '-exp(-x)-1', '0'),
        ('x^5-4*x^4+5*x^3-6*x+4', '5*x^4-16*x^3+15*x^2-6', '-1.25'),
    ):
        cn = ejecutar_numerico('num_newton', dict(parametros_defecto('num_newton'), funcion=expr, derivada=der, x0=x0, criterio='porcentual', tolerancia='0.01', parada='cambio', maximo='50'))
        assert cn.datos['convergio'], f'Newton no convergió en {expr}'

    # Ej. 126-127 y 130-131: Jacobi y Gauss-Seidel porcentual
    c126 = ejecutar_numerico(
        'num_comparar_iterativos',
        dict(vector_b='27, -61.5, -21.5', inicial='0, 0, 0', error_iterativo='porcentual', epsilon='5', maximo='50', reordenar='no'),
        {'A': [[10, 2, -1], [-3, -6, 2], [1, 1, 5]]},
    )
    assert c126.datos['convergio']

    c130 = ejecutar_numerico(
        'num_comparar_iterativos',
        dict(vector_b='7, -21, 15', inicial='0, 0, 0', error_iterativo='porcentual', epsilon='1', maximo='50', reordenar='no'),
        {'A': [[4, -1, 1], [4, -8, 1], [-2, 1, 5]]},
    )
    assert c130.datos['convergio']


def main():
    """Ejecuta la batería de la guía y reporta cada unidad verificada."""
    for nombre, prueba in (
        ('Unidad I (sistemas, escalonada, vectores)', probar_unidad_1),
        ('Unidad II (determinantes, inversas, Cramer, LU)', probar_unidad_2),
        ('Unidad IV (bases, errores, Maclaurin, bisección, Newton, iterativos)', probar_unidad_4),
    ):
        prueba()
        print(f'OK · {nombre}')
    print('Todos los ejercicios de muestra de la guía pasaron correctamente.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
