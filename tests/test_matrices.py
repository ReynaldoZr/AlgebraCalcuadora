"""Comprueba resultados y precondiciones de las operaciones matriciales.

Tema: suma, resta y conservación de entradas.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import unittest
from fractions import Fraction

from modulos.modulo_matrices import restar_matrices, sumar_matrices
from modulos.validaciones import validar_matriz


class PruebasMatrices(unittest.TestCase):
    """Verifica ejemplos matemáticos y entradas inválidas del módulo."""

    def test_suma_rectangular(self):
        """Suma un ejemplo conocido de matrices 2x3."""
        self.assertEqual(sumar_matrices([[1, 2, 3], [4, 5, 6]],
                                      [[6, 5, 4], [3, 2, 1]]), [[7, 7, 7], [7, 7, 7]])

    def test_resta_negativos(self):
        """Comprueba signos y orden de operandos en una resta."""
        self.assertEqual(restar_matrices([[1, -2], [3, 4]], [[5, 1], [-1, 8]]),
                         [[-4, -3], [4, -4]])

    def test_fracciones_exactas(self):
        """Mantiene exactos tanto los racionales como los decimales leídos como texto."""
        resultado = sumar_matrices([[Fraction(1, 3), Fraction('0.1')]],
                                   [[Fraction(1, 6), Fraction('0.2')]])
        self.assertEqual(resultado, [[Fraction(1, 2), Fraction(3, 10)]])

    def test_no_altera_entradas_ni_comparte_filas(self):
        """La nueva matriz no modifica ni reutiliza las filas originales."""
        for operacion in (sumar_matrices, restar_matrices):
            with self.subTest(operacion=operacion.__name__):
                matriz_a, matriz_b = [[1, 2]], [[3, 4]]
                resultado = operacion(matriz_a, matriz_b)
                resultado[0][0] = 99
                self.assertEqual(matriz_a, [[1, 2]])
                self.assertEqual(matriz_b, [[3, 4]])

    def test_incompatibles(self):
        """Rechaza matrices con igual número de elementos pero distinta forma."""
        for operacion in (sumar_matrices, restar_matrices):
            with self.subTest(operacion=operacion.__name__):
                with self.assertRaisesRegex(ValueError, 'dimensiones deben coincidir'):
                    operacion([[1, 2]], [[3], [4]])

    def test_estructuras_invalidas(self):
        """Rechaza vacíos, filas desiguales y elementos no admitidos."""
        invalidas = [[], [[]], [[1], [2, 3]], [1], [[True]], [['1']], [[0.1]], None]
        for matriz in invalidas:
            with self.subTest(matriz=matriz):
                with self.assertRaises(ValueError):
                    validar_matriz(matriz)

    def test_inverso_aditivo(self):
        """Una matriz sumada con su opuesta devuelve la matriz cero."""
        self.assertEqual(sumar_matrices([[2, -3]], [[-2, 3]]), [[0, 0]])
