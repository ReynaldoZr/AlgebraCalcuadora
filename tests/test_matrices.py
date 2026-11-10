"""Comprueba resultados y precondiciones de las operaciones matriciales.

Tema: suma, resta y conservación de entradas.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import unittest
from fractions import Fraction

from modulos.modulo_matrices import (multiplicar_por_escalar, producto_matricial, restar_matrices,
                                     sumar_matrices, transponer_matriz)
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

    def test_escalar_rectangular_con_fracciones_y_signos(self):
        """Multiplica cada entrada de una matriz 2x3 por un racional negativo."""
        matriz = [[Fraction(1, 3), -2, 0], [4, Fraction('0.1'), Fraction(-1, 2)]]
        self.assertEqual(multiplicar_por_escalar(matriz, Fraction(-3, 2)),
                         [[Fraction(-1, 2), 3, 0], [-6, Fraction(-3, 20), Fraction(3, 4)]])

    def test_escalar_cero_e_identidad_sin_compartir_filas(self):
        """Cero e identidad conservan dimensiones y producen listas independientes."""
        original = [[Fraction(1, 3)], [-2], [0]]
        copia = [fila[:] for fila in original]
        for escalar, esperado in ((0, [[0], [0], [0]]), (1, copia)):
            with self.subTest(escalar=escalar):
                resultado = multiplicar_por_escalar(original, escalar)
                self.assertEqual(resultado, esperado)
                self.assertIsNot(resultado, original)
                for fila, anterior in zip(resultado, original):
                    self.assertIsNot(fila, anterior)
                resultado[0][0] = 99
                self.assertEqual(original, copia)

    def test_escalar_rechaza_valores_no_exactos(self):
        """No acepta bool, float, complejos ni texto en el contrato del núcleo."""
        for invalido in (True, False, 0.1, float('nan'), float('inf'), 1j, '2', None):
            with self.subTest(escalar=invalido):
                with self.assertRaisesRegex(ValueError, 'escalar'):
                    multiplicar_por_escalar([[1]], invalido)

    def test_escalar_valida_estructura_de_la_matriz(self):
        """No omite validaciones de A cuando k es cero."""
        for matriz in ([], [[]], [[1], [2, 3]], [[True]], [[0.1]], None):
            with self.subTest(matriz=matriz):
                with self.assertRaises(ValueError):
                    multiplicar_por_escalar(matriz, 0)

    def test_transpuesta_rectangular_exacta(self):
        """Una matriz 2x3 produce 3x2 conservando fracciones, ceros y signos."""
        matriz = [[Fraction(1, 3), -2, 5], [0, 4, Fraction(1, 2)]]
        self.assertEqual(transponer_matriz(matriz), [[Fraction(1, 3), 0], [-2, 4], [5, Fraction(1, 2)]])

    def test_transpuesta_doble_filas_columnas_y_cuadradas(self):
        """La doble transpuesta recupera A, incluidas filas y columnas únicas."""
        for matriz in ([[1]], [[1, -2, 3]], [[1], [-2], [3]], [[1, 2], [3, 4]]):
            with self.subTest(matriz=matriz):
                self.assertEqual(transponer_matriz(transponer_matriz(matriz)), matriz)

    def test_transpuesta_no_comparte_filas_ni_modifica_entrada(self):
        """Editar la salida o una fila de entrada no modifica la otra matriz."""
        matriz = [[1, 2, 3], [4, 5, 6]]
        resultado = transponer_matriz(matriz)
        resultado[0][1] = 99
        self.assertEqual(matriz, [[1, 2, 3], [4, 5, 6]])
        matriz[0][1] = -8
        self.assertEqual(resultado[1], [2, 5])

    def test_transpuesta_valida_matriz(self):
        """La nueva operación respeta las mismas restricciones de datos exactos."""
        for matriz in ([], [[]], [[1], [2, 3]], [[True]], [[0.1]], [['1']], None):
            with self.subTest(matriz=matriz):
                with self.assertRaises(ValueError):
                    transponer_matriz(matriz)

    def test_producto_rectangular_del_curso(self):
        """El ejemplo 2x3 por 3x2 produce el resultado conocido del plan."""
        self.assertEqual(producto_matricial([[1, 2, 3], [4, 5, 6]], [[1, 0], [2, 1], [0, 3]]),
                         [[5, 11], [14, 23]])

    def test_producto_fracciones_signos_y_cancelacion(self):
        """Los productos y su suma conservan exactitud, incluido un resultado cero."""
        self.assertEqual(producto_matricial([[Fraction(1, 3), -2], [0, Fraction('0.1')]],
                                           [[Fraction(3, 2)], [Fraction(1, 4)]]), [[0], [Fraction(1, 40)]])

    def test_producto_identidad_y_cero(self):
        """La identidad correspondiente conserva A y la matriz cero anula el producto."""
        a = [[1, -2, 3], [4, 0, 6]]
        self.assertEqual(producto_matricial([[1, 0], [0, 1]], a), a)
        self.assertEqual(producto_matricial(a, [[1, 0, 0], [0, 1, 0], [0, 0, 1]]), a)
        self.assertEqual(producto_matricial(a, [[0, 0], [0, 0], [0, 0]]), [[0, 0], [0, 0]])

    def test_producto_fila_columna_y_exterior(self):
        """Fila por columna y columna por fila tienen resultados de tamaños distintos."""
        self.assertEqual(producto_matricial([[1, 2, 3]], [[4], [5], [6]]), [[32]])
        self.assertEqual(producto_matricial([[2], [-1]], [[3, 4, 5]]), [[6, 8, 10], [-3, -4, -5]])

    def test_producto_no_es_conmutativo_ni_comparte_filas(self):
        """AB y BA pueden diferir y la salida no permite modificar las entradas."""
        a, b = [[1, 2], [0, 1]], [[1, 0], [3, 1]]
        resultado = producto_matricial(a, b)
        self.assertEqual(resultado, [[7, 2], [3, 1]])
        self.assertNotEqual(resultado, producto_matricial(b, a))
        resultado[0][0] = 99
        self.assertEqual(a, [[1, 2], [0, 1]])
        self.assertEqual(b, [[1, 0], [3, 1]])
        self.assertEqual(resultado[1], [3, 1])

    def test_producto_incompatible_explica_dimensiones(self):
        """Tener el mismo tamaño no basta para poder multiplicar matrices."""
        with self.assertRaisesRegex(ValueError, 'A es 2x3 y B es 2x3'):
            producto_matricial([[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]])

    def test_producto_valida_ambas_entradas(self):
        """No omite matrices vacías, irregulares o elementos no exactos de A/B."""
        for invalida in ([], [[]], [[1], [2, 3]], [[True]], [[0.1]], [['1']], None):
            for a, b in ((invalida, [[1]]), ([[1]], invalida)):
                with self.subTest(a=a, b=b):
                    with self.assertRaises(ValueError):
                        producto_matricial(a, b)
