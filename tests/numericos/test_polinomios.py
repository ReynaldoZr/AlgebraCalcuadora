"""Comprueba Horner, términos ausentes, deflación y referencias de polinomios.

Tema: issue 35 y ejemplos de la Sesión 22, sin depender de Newton pendiente.
Equipo responsable: Grupo 9.
"""

import math
from fractions import Fraction
import unittest

from modulos.numericos.polinomios import (
    crear_funciones_polinomio, deflacionar_polinomio, evaluar_horner,
)


class PruebasPolinomios(unittest.TestCase):
    """Verifica valores conocidos y reconstrucción con resto, sin sustituir el algoritmo."""

    def test_polinomio_de_clase_con_termino_ausente(self):
        """Conserva el cero de x² y coincide con p y p' analíticos en -1.25."""
        coeficientes = [1, -4, 5, 0, -6, 4]
        calc = evaluar_horner(coeficientes, -1.25)
        self.assertEqual(calc.valor, -11.0830078125)
        self.assertEqual(calc.datos['derivada'], 60.89453125)
        self.assertEqual(calc.datos['grado'], 5)
        self.assertEqual(calc.datos['coeficientes'][3], 0)
        self.assertEqual(coeficientes, [1, -4, 5, 0, -6, 4])
        self.assertEqual(len(calc.datos['filas']), 6)

    def test_deflacion_de_raiz_conocida_y_reconstruccion(self):
        """Dividir entre x+1 deja el cuártico de clase y conserva la identidad original."""
        original = [1, -4, 5, 0, -6, 4]
        calc = deflacionar_polinomio(original, -1)
        self.assertEqual(calc.valor, (1, -5, 10, -10, 4))
        self.assertEqual(calc.datos['resto'], 0)
        self.assertTrue(calc.datos['aceptada'])
        for x in (-2, -.3, 0, 1, 2, 3):
            p = evaluar_horner(original, x).valor
            q = evaluar_horner(calc.valor, x).valor
            self.assertAlmostEqual(p, (x + 1) * q + calc.datos['resto'], places=10)

    def test_resto_grande_no_se_descarta(self):
        """Una aproximación insuficiente conserva el resto y no autoriza deflación sin él."""
        calc = deflacionar_polinomio([2, 3, 5], .5)
        self.assertEqual(calc.valor, (2, 4))
        self.assertEqual(calc.datos['resto'], 7)
        self.assertFalse(calc.datos['aceptada'])
        self.assertIn('No descartar', calc.datos['motivo'])
        self.assertEqual(evaluar_horner([2, 3, 5], 2).valor,
                         (2 - .5) * evaluar_horner(calc.valor, 2).valor + 7)
        self.assertFalse(deflacionar_polinomio([1, 0], .1, tolerancia_resto=.1).datos['aceptada'])

    def test_ceros_iniciales_constantes_y_raiz_cero(self):
        """Normaliza ceros iniciales sin borrar términos ausentes ni confundir grado."""
        calc = evaluar_horner([0, 0, 1, -4, 4], 2)
        self.assertEqual(calc.datos['coeficientes'], (1, -4, 4))
        self.assertEqual(calc.datos['ceros_iniciales'], 2)
        self.assertEqual(calc.valor, 0)
        self.assertEqual(calc.datos['derivada'], 0)
        for coef in ([7], [0, 0, 0]):
            constante = evaluar_horner(coef, 5)
            self.assertEqual(constante.datos['derivada'], 0)
            with self.assertRaises(ValueError):
                deflacionar_polinomio(coef, 0)
        self.assertEqual(deflacionar_polinomio([1, 0, 0], 0).valor, (1, 0))

    def test_validacion_y_limites_de_representacion(self):
        """No admite coeficientes/puntos complejos o no finitos ni continúa tras overflow."""
        for coef in ([], (), '1,2', [True, 1], [math.nan, 2], [1j, 1], [math.inf]):
            with self.subTest(coef=coef), self.assertRaises(ValueError):
                evaluar_horner(coef, 2)
        for x in (True, math.inf, math.nan, 1j):
            with self.subTest(x=x), self.assertRaises(ValueError):
                evaluar_horner([1, 2], x)
        with self.assertRaises(ValueError):
            evaluar_horner([1e308, 1], 2)
        for tol in (0, -1, math.inf, True):
            with self.subTest(tolerancia=tol), self.assertRaises(ValueError):
                deflacionar_polinomio([1, 0], 0, tol)

    def test_proveedores_independientes_y_copia_de_entrada(self):
        """Los callables sirven al contrato Newton y no cambian si se edita la lista original."""
        coeficientes = [1, -4, 5, 0, -6, 4]
        f, df = crear_funciones_polinomio(coeficientes)
        coeficientes[0] = 99
        self.assertEqual(f(-1.25), -11.0830078125)
        self.assertEqual(df(-1.25), 60.89453125)
        for raiz in (-1, 1, 2):
            self.assertEqual(f(raiz), 0)
        # Primer avance comprobado sin añadir otro bucle de Newton al módulo.
        self.assertAlmostEqual(-1.25 - f(-1.25) / df(-1.25),
                               float(Fraction(-16649, 15589)), places=12)

    def test_referencia_numpy_incluye_complejas_sin_atribuirlas_a_newton_real(self):
        """NumPy contrasta todas las raíces del cuártico; el proveedor propio sigue siendo real."""
        import numpy as np
        coeficientes = [1, -5, 10, -10, 4]
        referencias = list(np.roots(coeficientes))
        for esperada in (1, 2, 1 + 1j, 1 - 1j):
            self.assertLess(min(abs(raiz - esperada) for raiz in referencias), 1e-10)
        f, _ = crear_funciones_polinomio(coeficientes)
        self.assertEqual(f(1), 0)
        self.assertEqual(f(2), 0)
        with self.assertRaises(ValueError):
            f(1 + 1j)


if __name__ == '__main__':
    unittest.main()
