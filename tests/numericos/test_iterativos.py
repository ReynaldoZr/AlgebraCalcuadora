"""Comprueba Jacobi mediante soluciones conocidas y límites de sus datos.

Tema: Programa 8, actualización simultánea, parada y conservación de entradas.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy
from fractions import Fraction
import unittest

from modulos.numericos.iterativos import (
    comparar_iterativos, gauss_seidel, jacobi, reordenar_ecuaciones,
)


class PruebasJacobi(unittest.TestCase):
    """Verifica el núcleo sin dependencias gráficas ni bibliotecas numéricas externas."""

    def setUp(self):
        """Prepara el sistema de referencia del plan semanal 13."""
        self.a = [[4, -1, 1], [4, -8, 1], [-2, 1, 5]]
        self.b = [7, -21, 15]
        self.inicial = [0, 0, 0]

    def test_ejemplo_del_plan_y_tabla_completa(self):
        """El ejemplo converge en once iteraciones a la solución conocida."""
        c = jacobi(self.a, self.b, self.inicial)
        self.assertTrue(c.datos['convergio'])
        self.assertEqual(len(c.datos['filas']), 11)
        self.assertEqual(c.datos['filas'][0], (1, 1.75, 2.625, 3.0, 3.0))
        for valor, esperado in zip(c.valor, [2, 4, 3]):
            self.assertAlmostEqual(valor, esperado, delta=0.0001)
        self.assertEqual([f[0] for f in c.datos['filas']], list(range(1, 12)))
        self.assertEqual(len(c.datos['columnas']), 5)
        self.assertLess(c.datos['error'], 0.0001)
        self.assertTrue(all(c.datos['dominantes']))

    def test_limite_de_una_iteracion_conserva_aproximacion(self):
        """Al agotarse el límite se devuelve el vector y se distingue de convergencia."""
        c = jacobi(self.a, self.b, self.inicial, max_iteraciones=1)
        self.assertFalse(c.datos['convergio'])
        self.assertEqual(c.valor, [1.75, 2.625, 3])
        self.assertIn('máximo', c.datos['motivo'])
        self.assertEqual(c.datos['residuo'], 10)

    def test_residuo_verifica_la_solucion_original(self):
        """El residuo final coincide con Ax−b calculado sobre el sistema original."""
        c = jacobi(self.a, self.b, self.inicial)
        esperado = max(abs(sum(v * x for v, x in zip(fila, c.valor)) - b)
                       for fila, b in zip(self.a, self.b))
        self.assertAlmostEqual(c.datos['residuo'], esperado)
        self.assertLess(c.datos['residuo'], 0.0001)
        self.assertIn('Residuo', str(c.pasos[-1].formulas))

    def test_error_igual_a_tolerancia_termina(self):
        """Acepta el caso límite de igualdad que recomienda el Programa 8."""
        c = jacobi([[2]], [1], [0], tolerancia=0.5, max_iteraciones=1)
        self.assertTrue(c.datos['convergio'])
        self.assertEqual(c.datos['error'], 0.5)
        self.assertEqual(c.datos['residuo'], 0)

    def test_crecimiento_informa_sin_afirmar_divergencia_automatica(self):
        """El aviso conserva las iteraciones aunque después se alcance la tolerancia."""
        c = jacobi([[1, 2], [0.1, 1]], [0, 1], [0, 0], tolerancia=1e-8)
        self.assertTrue(c.datos['convergio'])
        self.assertTrue(c.datos['advertencias'])
        self.assertIn('creció', c.datos['advertencias'][0])
        self.assertIn('creció', c.pasos[-1].detalle)

    def test_residuo_no_finito_se_informa_sin_perder_vector(self):
        """Un residuo no representable no borra la última aproximación finita."""
        c = jacobi([[1e308, 1e308], [1, 1]], [0, 0], [1.5, 1.5], max_iteraciones=1)
        self.assertEqual(c.valor, [-1.5, -1.5])
        self.assertIsNone(c.datos['residuo'])
        self.assertTrue(any('residuo' in aviso for aviso in c.datos['advertencias']))

    def test_todas_las_componentes_usan_el_vector_anterior(self):
        """Un inicio no nulo distingue Jacobi de la actualización inmediata."""
        c = jacobi([[4, 1], [2, 3]], [9, 13], [1, 2], max_iteraciones=1)
        self.assertEqual(c.valor, [1.75, 11 / 3])

    def test_solucion_inicial_y_sistema_unidimensional(self):
        """Una solución inicial correcta termina con diferencia cero."""
        c = jacobi([[2]], [6], [3])
        self.assertTrue(c.datos['convergio'])
        self.assertEqual(c.valor, [3])
        self.assertEqual(c.datos['error'], 0)

    def test_dominancia_es_suficiente_y_no_necesaria(self):
        """Un sistema convergente sin dominancia estricta sigue admitido."""
        c = jacobi([[1, 2], [0.1, 1]], [3, 1.1], [0, 0], tolerancia=1e-8)
        self.assertEqual(c.datos['dominantes'], (False, True))
        self.assertTrue(c.datos['convergio'])
        for v in c.valor:
            self.assertAlmostEqual(v, 1, delta=1e-7)
        self.assertIn('no está garantizada', c.pasos[0].detalle)

    def test_sistema_divergente_agota_maximo(self):
        """Un sistema que diverge no anuncia convergencia ni corta la tabla."""
        c = jacobi([[1, 5], [7, 1]], [11, 15], [0, 0], max_iteraciones=8)
        self.assertFalse(c.datos['convergio'])
        self.assertEqual(len(c.datos['filas']), 8)

    def test_conserva_entradas_y_resultados_independientes(self):
        """Las copias del cálculo no comparten las entradas ni el vector de la tabla."""
        originales = deepcopy((self.a, self.b, self.inicial))
        c = jacobi(self.a, self.b, self.inicial)
        self.assertEqual((self.a, self.b, self.inicial), originales)
        c.valor[0] = 100
        c.datos['matriz'][0][0] = 100
        self.assertEqual((self.a, self.b, self.inicial), originales)
        self.assertNotEqual(c.datos['filas'][-1][1], 100)
        self.assertIn('Fila 1: [4, -1, 1] | b=7', str(c.pasos[0].formulas))

    def test_acepta_fracciones_y_textos_decimales(self):
        """Los números del álgebra exacta pueden convertirse en la unidad aproximada."""
        c = jacobi([[Fraction(1, 2)]], ['1.5'], ['0'])
        self.assertEqual(c.valor, [3])

    def test_rechaza_dimensiones_incompatibles(self):
        """Vacíos, filas irregulares y vectores incorrectos producen mensajes claros."""
        casos = [([], [], []), ([[1, 2]], [1], [0]), ([[1], [2, 3]], [1, 2], [0, 0]),
                 ([[1]], [], [0]), ([[1]], [1], [[0]]), (None, [1], [0])]
        for a, b, x in casos:
            with self.subTest(a=a, b=b, x=x), self.assertRaises(ValueError):
                jacobi(a, b, x)

    def test_rechaza_diagonal_cero(self):
        """Explica el reordenamiento necesario antes de dividir por cero."""
        with self.assertRaisesRegex(ValueError, 'Reordena'):
            jacobi([[0, 1], [1, 2]], [1, 2], [0, 0])

    def test_rechaza_numeros_no_finitos_y_booleanos(self):
        """Valida cada fuente de datos antes de iniciar la iteración."""
        for valor in [True, float('nan'), float('inf'), 1j, 'texto', 10 ** 400]:
            for a, b, x in [([[valor]], [1], [0]), ([[1]], [valor], [0]), ([[1]], [1], [valor])]:
                with self.subTest(valor=valor, a=a, b=b, x=x), self.assertRaises(ValueError):
                    jacobi(a, b, x)

    def test_rechaza_tolerancias_y_maximos_invalidos(self):
        """Las condiciones de parada deben ser positivas y finitas."""
        for tol in [0, -1, True, float('nan'), float('inf')]:
            with self.subTest(tol=tol), self.assertRaises(ValueError):
                jacobi(self.a, self.b, self.inicial, tolerancia=tol)
        for maximo in [0, -1, True, 1.5, '20', 10001]:
            with self.subTest(maximo=maximo), self.assertRaises(ValueError):
                jacobi(self.a, self.b, self.inicial, max_iteraciones=maximo)

    def test_overflow_conserva_el_ultimo_vector_finito(self):
        """El desbordamiento tiene un motivo propio y no introduce NaN en la tabla."""
        c = jacobi([[1e-308, 1e308], [1, 1]], [1, 1], [1, 1])
        self.assertFalse(c.datos['convergio'])
        self.assertEqual(c.valor, [1, 1])
        self.assertEqual(c.datos['filas'], [])
        self.assertIn('no finitos', c.datos['motivo'])

    def test_dominancia_con_valores_grandes_no_desborda(self):
        """La comprobación de dominancia admite coeficientes finitos de gran magnitud."""
        c = jacobi([[1e308, 1e308, 1e308], [0, 1, 0], [0, 0, 1]],
                   [0, 0, 0], [0, 0, 0])
        self.assertEqual(c.datos['dominantes'], (False, True, True))
        self.assertTrue(c.datos['convergio'])


class PruebasGaussSeidel(unittest.TestCase):
    """Verifica Gauss-Seidel, reordenamiento de ecuaciones, relajación y comparación."""

    def setUp(self):
        """Prepara el sistema 3×3 de referencia del plan semanal 13."""
        self.a = [[4, -1, 1], [4, -8, 1], [-2, 1, 5]]
        self.b = [7, -21, 15]
        self.inicial = [0, 0, 0]

    def test_ejemplo_del_plan_actualizacion_inmediata_y_siete_iteraciones(self):
        """La primera iteración da (1.75, 3.5, 3) y converge en siete iteraciones."""
        c = gauss_seidel(self.a, self.b, self.inicial)
        self.assertTrue(c.datos['convergio'])
        self.assertEqual(len(c.datos['filas']), 7)
        self.assertEqual(c.datos['filas'][0][:4], (1, 1.75, 3.5, 3.0))
        for valor, esperado in zip(c.valor, [2, 4, 3]):
            self.assertAlmostEqual(valor, esperado, delta=0.0001)
        self.assertLess(c.datos['residuo'], 0.0001)

    def test_actualizacion_inmediata_con_inicio_no_nulo(self):
        """Usa de inmediato la componente recién calculada en la misma iteración."""
        c = gauss_seidel([[4, 1], [2, 3]], [9, 13], [1, 2], max_iteraciones=1)
        self.assertEqual(c.valor, [1.75, 9.5 / 3])

    def test_reordenar_dos_por_dos_y_conservar_originales(self):
        """Intercambiar filas logra dominancia estricta y mantiene A y B originales."""
        a = [[1, 5], [7, 1]]
        b = [11, 15]
        originales = deepcopy((a, b))
        rj = jacobi(a, b, [0, 0], reordenar=True)
        rgs = gauss_seidel(a, b, [0, 0], reordenar=True)
        self.assertEqual((a, b), originales)
        self.assertTrue(rj.datos['reordenado'])
        self.assertEqual(rj.datos['orden_ecuaciones'], (2, 1))
        self.assertEqual(len(rj.datos['filas']), 7)
        self.assertEqual(len(rgs.datos['filas']), 5)
        for res in (rj, rgs):
            self.assertTrue(res.datos['convergio'])
            self.assertEqual(res.datos['matriz'], a)
            self.assertEqual(res.datos['vector_b'], b)
            self.assertAlmostEqual(res.valor[0], 32 / 17, delta=0.0001)
            self.assertAlmostEqual(res.valor[1], 31 / 17, delta=0.0001)
            self.assertLess(res.datos['residuo'], 0.001)

    def test_reordenar_corrige_diagonal_cero_y_rechaza_imposible(self):
        """Permite continuar si un intercambio quita el cero y rechaza si no existe orden."""
        c = gauss_seidel([[0, 2], [3, 1]], [4, 5], [0, 0], reordenar=True)
        self.assertTrue(c.datos['convergio'])
        self.assertTrue(c.datos['reordenado'])
        self.assertEqual(c.datos['orden_ecuaciones'], (2, 1))
        self.assertAlmostEqual(c.valor[0], 1.0, delta=0.0001)
        self.assertAlmostEqual(c.valor[1], 2.0, delta=0.0001)

        with self.assertRaisesRegex(ValueError, 'diagonal'):
            reordenar_ecuaciones([[0, 1], [0, 2]], [1, 2])

    def test_reordenar_sin_dominancia_estricta_informa_sin_garantia(self):
        """Si quita el cero pero no logra dominancia estricta, informa falta de garantía."""
        c = gauss_seidel([[0, 1], [1, 1]], [2, 3], [0, 0], reordenar=True)
        self.assertTrue(c.datos['reordenado'])
        self.assertFalse(all(c.datos['dominantes']))
        self.assertIn('no está garantizada', c.pasos[0].detalle)

    def test_relajacion_valida_y_rechaza_fuera_de_rango(self):
        """Acepta 0 < λ < 2 como en el ejemplo 11.3 y rechaza extremos inválidos."""
        c = gauss_seidel(
            [[3, -0.1, -0.2], [0.1, 7, -0.3], [0.3, -0.2, 10]],
            [7.85, -19.3, 71.4],
            [0, 0, 0],
            tolerancia=0.0001,
            relajacion=1.05,
        )
        self.assertTrue(c.datos['convergio'])
        for v, esp in zip(c.valor, [3.0, -2.5, 7.0]):
            self.assertAlmostEqual(v, esp, delta=0.0001)
        for invalido in (0, -0.5, 2, 2.5, True, float('nan')):
            with self.subTest(lam=invalido), self.assertRaises(ValueError):
                gauss_seidel(self.a, self.b, self.inicial, relajacion=invalido)

    def test_comparar_iterativos_conserva_tablas_completas(self):
        """El comparador conserva 11 filas de Jacobi, 7 de Gauss-Seidel y distingue ganador."""
        c = comparar_iterativos(self.a, self.b, self.inicial, reordenar=False)
        self.assertEqual(len(c.datos['jacobi']['filas']), 11)
        self.assertEqual(len(c.datos['gauss_seidel']['filas']), 7)
        self.assertEqual(len(c.datos['filas']), 18)
        self.assertIn('Gauss-Seidel necesitó menos iteraciones (7 frente a 11', c.datos['comparacion_iteraciones'])
        self.assertLess(c.datos['diferencia_metodos'], 0.0002)

    def test_comparar_iterativos_distingue_limite_de_iteraciones(self):
        """Con límite insuficiente conserva las tablas y no anuncia convergencia."""
        c = comparar_iterativos([[1, 5], [7, 1]], [11, 15], [0, 0], max_iteraciones=6, reordenar=False)
        self.assertFalse(c.datos['convergio'])
        self.assertEqual(len(c.datos['jacobi']['filas']), 6)
        self.assertEqual(len(c.datos['gauss_seidel']['filas']), 6)
        self.assertIn('Ninguno', c.datos['comparacion_iteraciones'])
