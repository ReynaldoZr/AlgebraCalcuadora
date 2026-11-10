"""Verifica métodos numéricos, errores, límites y contraste con bibliotecas.

Tema: casos conocidos de semana 12, sin interacción con el escritorio del usuario.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction
import importlib.util
import math
import os
import unittest


class PruebasSemana12(unittest.TestCase):
    """Comprueba valores de referencia y condiciones de terminación, no solo fórmulas internas."""

    @classmethod
    def setUpClass(cls):
        """Exige dependencias en CI; una instalación de solo álgebra puede omitir esta unidad."""
        faltan = [n for n in ('numpy', 'scipy', 'matplotlib') if importlib.util.find_spec(n) is None]
        if faltan:
            if os.environ.get('CALCULADORA_EXIGIR_NUMERICOS') == '1':
                raise RuntimeError('Faltan dependencias numéricas: ' + ', '.join(faltan))
            raise unittest.SkipTest('Instala requirements-numericos.txt para probar la semana 12.')

    def test_funciones_admitidas_y_texto_no_ejecutable(self):
        """El lector acepta notación matemática y rechaza atributos, imports y llamadas desconocidas."""
        from modulos.numericos.funciones import crear_funcion
        self.assertAlmostEqual(crear_funcion('sin(pi/2)+x^2')(3), 10)
        for texto in ('__import__("os")', 'x.__class__', '[x for x in (1,2)]', 'True', 'lambda x: x', 'open("algo")', 'sin(x,2)', '1 if x else 2'):
            with self.subTest(texto=texto), self.assertRaises(ValueError):
                crear_funcion(texto)
        for texto in ('1/0', 'sqrt(-1)', 'x^100000', 'exp(10000)'):
            with self.subTest(texto=texto), self.assertRaises(ValueError):
                crear_funcion(texto)(2)

    def test_biseccion_raiz_tabla_y_residuo(self):
        """La raíz de x²−2 respeta tolerancias independientes y conserva todas las filas."""
        from modulos.numericos.biseccion import biseccion
        calculo = biseccion('x^2-2', 1, 2, 1e-6, tolerancia_f=1e-8)
        self.assertTrue(calculo.datos['convergio'])
        self.assertLess(abs(calculo.valor - math.sqrt(2)), 1e-6)
        self.assertLessEqual(calculo.datos['residuo'], 1e-8)
        self.assertLess(calculo.datos['diferencia_scipy'], 1e-6)
        filas = calculo.datos['filas']
        self.assertIsNone(filas[0][7])
        self.assertEqual([f[0] for f in filas], list(range(1, len(filas) + 1)))
        for fila in filas:
            self.assertLessEqual(fila[1], calculo.valor)
            self.assertGreaterEqual(fila[2], calculo.valor)
            self.assertEqual(len(fila), 9)

    def test_biseccion_extremos_cero_y_porcentaje(self):
        """Admite raíces en extremos y xr=0 sin calcular un porcentaje indefinido."""
        from modulos.numericos.biseccion import biseccion
        for a, b in ((1, 3), (-1, 1)):
            c = biseccion('x-1', a, b)
            self.assertTrue(c.datos['convergio'])
            self.assertEqual(c.valor, 1)
            self.assertEqual(c.datos['filas'], [])
        c = biseccion('x', -1, 1, criterio='porcentual')
        self.assertEqual(c.valor, 0)
        self.assertIsNone(c.datos['filas'][0][7])
        c = biseccion('cos(x)-x', 0, 1, 0.01, criterio='porcentual')
        self.assertTrue(c.datos['convergio'])
        self.assertLessEqual(c.datos['filas'][-1][7], 0.01)

    def test_biseccion_errores_y_maximo_no_son_convergencia(self):
        """Las precondiciones fallidas y el agotamiento de iteraciones no anuncian éxito."""
        from modulos.numericos.biseccion import biseccion
        with self.assertRaisesRegex(ValueError, 'cambio de signo'):
            biseccion('x^2+1', -1, 1)
        for a, b, tol in ((2, 1, .1), (0, 1, 0), (0, math.inf, .1), (0, 1, math.nan)):
            with self.assertRaises(ValueError):
                biseccion('x-0.4', a, b, tol)
        with self.assertRaises(ValueError):
            biseccion('1/x', -1, 1)
        c = biseccion('x^2-2', 1, 2, 1e-12, max_iteraciones=2, tolerancia_f=1e-12)
        self.assertFalse(c.datos['convergio'])
        self.assertEqual(len(c.datos['filas']), 2)
        self.assertIn('máximo', c.datos['motivo'])

    def test_error_absoluto_relativo_y_valor_cero(self):
        """250 frente a 248.5 produce error 1.5 y 0.6%; relativo con referencia cero no se inventa."""
        from modulos.numericos.errores import calcular_errores
        c = calcular_errores(250, 248.5)
        self.assertEqual(c.datos['absoluto'], 1.5)
        self.assertAlmostEqual(c.datos['porcentual'], 0.6)
        self.assertIsNone(calcular_errores(0, 1).datos['relativo'])
        self.assertAlmostEqual(calcular_errores(-250, -248.5).datos['porcentual'], 0.6)
        for valor in (True, math.nan, math.inf):
            with self.assertRaises(ValueError):
                calcular_errores(valor, 1)

    def test_propagacion_cubica_y_derivada_central(self):
        """El ejemplo x³ tiene derivada 18.75 y cambio lineal 0.1875."""
        from modulos.numericos.errores import propagacion
        c = propagacion('x^3', 2.5, .01)
        self.assertAlmostEqual(c.datos['derivada'], 18.75, places=6)
        self.assertAlmostEqual(c.valor, .1875, places=7)
        self.assertAlmostEqual(c.datos['cambio'], 2.51 ** 3 - 2.5 ** 3, places=10)
        self.assertEqual(c.datos['cambio_exacto'], '188251/1000000')
        self.assertIsNone(propagacion('sin(x)', 1, .01).datos['cambio_exacto'])
        with self.assertRaises(ValueError):
            propagacion('x^3', 2.5, -.01)
        with self.assertRaises(ValueError):
            propagacion('x', 1, .1, 1e-30)

    def test_simulacion_conserva_todas_las_iteraciones_y_referencia(self):
        """La referencia de interés compuesto coincide con un cálculo independiente Decimal."""
        from modulos.numericos.errores import simulacion
        c = simulacion(1000, .005, 50, 2)
        self.assertEqual(len(c.datos['filas']), 50)
        with localcontext() as contexto:
            contexto.prec = 100
            esperado = Decimal('1000') * Decimal('1.005') ** 50
            self.assertLess(abs(Decimal(c.datos['referencia']) - esperado), Decimal('1e-90'))
        negativo = simulacion(-1.239, 0, 1, 2)
        self.assertEqual(negativo.datos['truncado'], '-1.23')
        self.assertEqual(negativo.datos['redondeado'], '-1.24')

    def test_flotantes_e_inestabilidad(self):
        """Overflow y underflow son intencionales; la reformulación reduce cancelación."""
        from modulos.numericos.errores import inestabilidad, punto_flotante
        filas = dict(punto_flotante().datos['filas'])
        self.assertEqual(filas['Overflow float32'], 'inf')
        self.assertEqual(filas['Underflow float32'], '0.0')
        self.assertEqual(filas['1/10 + 1/5 (Fraction)'], '3/10')
        c = inestabilidad(1e16)
        self.assertEqual(c.datos['directo'], 0)
        self.assertGreater(c.datos['estable'], 0)
        self.assertLess(c.datos['error_estable'], c.datos['error_directo'])

    def test_bases_exactas_y_restos(self):
        """13.625 es 1101.101 en binario; 0.1 tiene un resto tras truncar su expansión."""
        from modulos.numericos.errores import descomponer
        c = descomponer('13.625', 2)
        self.assertEqual(c.valor, '1101.101')
        self.assertEqual(c.datos['resto'], '0')
        self.assertNotEqual(descomponer('0.1', 2, 16).datos['resto'], '0')
        self.assertEqual(descomponer('-13.625', 10).valor, '-13.625')

    def test_comparacion_inversa_sistema_y_condicion(self):
        """Reutiliza las fracciones originales y distingue condición de residuo."""
        from modulos.numericos.comparadores import comparar, hilbert
        a = [[1, 2], [3, 4]]
        original = deepcopy(a)
        c = comparar(a)
        self.assertEqual(c.datos['exacto'], [[-2, 1], [Fraction(3, 2), Fraction(-1, 2)]])
        self.assertLess(c.datos['residuo'], 1e-12)
        self.assertEqual(a, original)
        s = comparar([[2, 1], [1, -1]], [5, 1])
        self.assertEqual(s.datos['exacto'], [[2], [1]])
        self.assertGreater(comparar(hilbert(5)).datos['condicion'], 100000)
        with self.assertRaises(ValueError):
            comparar([[1, 2], [2, 4]])

    def test_figuras_sin_abrir_ventanas(self):
        """Las gráficas construyen ejes exportables sin usar el escritorio del usuario."""
        from interfaz.numericos.graficas import figura_numerica
        from modulos.numericos.biseccion import biseccion
        from modulos.numericos.errores import simulacion
        figura = figura_numerica('num_biseccion', biseccion('cos(x)-x', 0, 1))
        self.assertEqual(len(figura.axes), 2)
        self.assertEqual(len(figura.axes[0].lines[0].get_xdata()), 401)
        self.assertEqual(len(figura_numerica('num_simulacion', simulacion()).axes[0].lines), 2)
