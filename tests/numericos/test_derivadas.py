"""Comprueba diferencias finitas, representabilidad y proveedor para Newton.

Tema: issue 34, ejemplos y precisión de la Sesión 22.
Equipo responsable: Grupo 9.
"""

import math
import unittest

from modulos.numericos.derivadas import calcular_derivada, crear_derivada


class PruebasDerivadas(unittest.TestCase):
    """Usa derivadas conocidas y casos de cancelación/dominio, sin repetir el algoritmo."""

    def test_ejemplo_cubico_de_clase(self):
        """En x=2, la derivada verdadera es 10 y los dos esquemas tienen distinto error."""
        f = lambda x: x ** 3 - 2 * x - 5
        adelante = calcular_derivada(f, 2, .01, 'adelante')
        central = calcular_derivada(f, 2, .01, 'central')
        self.assertAlmostEqual(adelante.valor, 10.0601, places=9)
        self.assertAlmostEqual(central.valor, 10.0001, places=9)
        self.assertLess(abs(central.valor - 10), abs(adelante.valor - 10))
        self.assertEqual(central.datos['puntos'], (1.99, 2.01))
        self.assertEqual(central.datos['orden_truncamiento'], 2)

    def test_pasos_de_distinto_tamano_y_truncamiento(self):
        """El cúbico aproxima mejor con h moderadamente menor, sin promesa universal."""
        errores = [abs(calcular_derivada(lambda x: x ** 3, 2, h).valor - 12)
                   for h in (.1, .01, .001)]
        self.assertGreater(errores[0], errores[1])
        self.assertGreater(errores[1], errores[2])

    def test_valida_configuracion_y_puntos(self):
        """Rechaza h inválido, booleanos, puntos iguales, no finitos y esquemas desconocidos."""
        for h in (0, -1, math.nan, math.inf, True):
            with self.subTest(h=h), self.assertRaises(ValueError):
                crear_derivada(lambda x: x, h)
        for x, h in ((1e16, 1), (2, 1e-300), (math.inf, .01), (True, .01), (1e308, 1e308)):
            with self.subTest(x=x, h=h), self.assertRaises(ValueError):
                calcular_derivada(lambda x: x, x, h)
        with self.assertRaises(ValueError):
            crear_derivada('x')
        with self.assertRaises(ValueError):
            crear_derivada(lambda x: x, metodo='secante')

    def test_dominio_se_comprueba_en_cada_punto(self):
        """La central necesita x-h válido; la de adelante puede funcionar en ese borde."""
        with self.assertRaisesRegex(ValueError, 'puntos'):
            calcular_derivada(math.sqrt, 0, .01)
        self.assertAlmostEqual(calcular_derivada(math.sqrt, 0, .01, 'adelante').valor, 10)
        proveedor = crear_derivada(math.log, .01)
        self.assertAlmostEqual(proveedor(2), .5, places=4)
        with self.assertRaises(ValueError):
            proveedor(0)

    def test_resultados_no_finitos_y_desbordamiento(self):
        """Un cociente imposible o una evaluación no real no se propagan como derivada válida."""
        for funcion in (lambda x: math.nan, lambda x: math.inf, lambda x: 1j):
            with self.subTest(funcion=funcion), self.assertRaises(ValueError):
                calcular_derivada(funcion, 1, .01)
        with self.assertRaises(ValueError):
            calcular_derivada(math.exp, 710, .01)
        with self.assertRaises(ValueError):
            calcular_derivada(lambda x: 1e308 if x > 0 else -1e308, 0, .01)

    def test_cancelacion_no_se_confunde_con_derivada_exacta(self):
        """Muestras iguales muestran la ambigüedad, incluso si la función es constante."""
        constante = calcular_derivada(lambda x: 3, 2, .01)
        perdida = calcular_derivada(lambda x: 1e16 + x, 0, .1)
        for calc in (constante, perdida):
            self.assertEqual(calc.valor, 0)
            self.assertTrue(calc.datos['advertencias'])
            self.assertIn('puede ser', calc.datos['advertencias'][0])
        pequeno = calcular_derivada(lambda x: math.copysign(1e-300, x), 0, 1e300)
        self.assertEqual(pequeno.valor, 0)
        self.assertIn('subdesbordamiento', pequeno.datos['advertencias'][0])

    def test_proveedor_es_inyectable_sin_nucleo_newton(self):
        """El adaptador real recibe un callable del módulo numérico, sin depender de #33."""
        from interfaz.numericos.newton_adaptador import ejemplo_newton, validar_entrada_newton
        parametros = dict(ejemplo_newton(), modo_derivada='numerica', h='1e-5')
        args = validar_entrada_newton(parametros, proveedor_derivada=crear_derivada)
        self.assertAlmostEqual(args['derivada'](0), -2, places=8)
        # Un consumidor mínimo comprueba el contrato, no implementa el método completo.
        x1 = args['x0'] - args['funcion'](args['x0']) / args['derivada'](args['x0'])
        self.assertAlmostEqual(x1, .5, places=8)


if __name__ == '__main__':
    unittest.main()
