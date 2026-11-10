"""Prueba el uso de consola con entradas controladas.

Tema: recuperación de errores y reutilización de resultados.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import io
import unittest
from contextlib import redirect_stdout
from fractions import Fraction
from unittest.mock import patch

from interfaz.entradas import elegir_matriz, leer_entero_positivo, leer_numero
from main import main


class PruebasConsola(unittest.TestCase):
    """Comprueba recorridos que un estudiante puede realizar desde el menú."""

    def test_reintenta_dimension(self):
        """Continúa tras texto, cero y dimensiones no enteras."""
        with patch('builtins.input', side_effect=['hola', '0', '-2', '2.5', '2']):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(leer_entero_positivo('Filas: '), 2)

    def test_reintenta_numero(self):
        """Rechaza vacíos, texto, infinitos y denominador cero antes de aceptar decimal."""
        with patch('builtins.input', side_effect=['', 'abc', 'nan', 'inf', '1/0', '0.1']):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(leer_numero('Dato: '), Fraction(1, 10))

    def test_copia_ultimo_resultado(self):
        """Permite reutilizar un resultado sin compartir sus filas."""
        anterior = [[Fraction(3, 2)]]
        with patch('builtins.input', return_value='2'):
            with redirect_stdout(io.StringIO()):
                nuevo = elegir_matriz('A', anterior)
        nuevo[0][0] = 99
        self.assertEqual(anterior, [[Fraction(3, 2)]])

    def test_suma_procedimiento_resta_y_reentrada_menu(self):
        """Realiza suma, reutiliza su respuesta en una resta y sale normalmente."""
        entradas = ['x', '1', '0', '1', '1', '1', '1/3', '1', '1', '1/6', '1',
                    '2', '2', '1', '1', '1', '1/6', '2', '3', '9', '1', '3', '9', '9']
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas):
            with redirect_stdout(salida):
                main()
        texto = salida.getvalue()
        self.assertIn('Opción inválida', texto)
        self.assertIn('TEOREMAS CLAVE', texto)
        self.assertIn('R[1,1] = (1/3) + (1/6) = 1/2', texto)
        self.assertIn('Resultado A - B (1x1)', texto)
        self.assertIn('[ 1/3 ]', texto)
        self.assertIn('Hasta pronto.', texto)

    def test_error_dimensiones_no_cierra_programa(self):
        """Las dimensiones incompatibles devuelven al menú sin terminar la app."""
        entradas = ['1', '1', '1', '2', '1', '2', '2', '1', '3', '4', '9', '9']
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas):
            with redirect_stdout(salida):
                main()
        self.assertIn('A es 1x2 y B es 2x1', salida.getvalue())
        self.assertIn('Hasta pronto.', salida.getvalue())

    def test_fin_de_entrada_limpio(self):
        """El cierre del flujo de entrada no produce un traceback."""
        for excepcion in (EOFError, KeyboardInterrupt):
            with self.subTest(excepcion=excepcion.__name__):
                with patch('builtins.input', side_effect=excepcion):
                    with redirect_stdout(io.StringIO()) as salida:
                        main()
                self.assertIn('Sesión terminada', salida.getvalue())

    def test_escalar_reintenta_y_reutiliza_resultado_sin_pedir_b(self):
        """La opción 4 pide solo A y k, explica y reutiliza incluso k igual a cero."""
        entradas = ['1', '4', '1', '2', '1/3', '-2', 'hola', '1/0', '-3/2', '1',
                    '4', '2', '0', '1', '3', '9', '9']
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas) as entrada:
            with redirect_stdout(salida):
                main()
        texto = salida.getvalue()
        self.assertIn('Número inválido', texto)
        self.assertIn('Resultado kA (1x2)', texto)
        self.assertIn('R[1,1] = (-3/2) × (1/3) = -1/2', texto)
        self.assertIn('R[1,2] = (0) × (3) = 0', texto)
        self.assertIn('Hasta pronto.', texto)
        self.assertFalse(any('B[' in llamada.args[0] for llamada in entrada.call_args_list))

    def test_transpuesta_con_error_y_reutilizacion_doble(self):
        """La opción 5 pide solo A, reintenta errores y permite recuperar A con otra transpuesta."""
        entradas = ['1', '5', '1', '3', '1/0', '1/3', '-2', '5', '1',
                    '5', '2', '1', '3', '9', '9']
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas) as entrada:
            with redirect_stdout(salida):
                main()
        texto = salida.getvalue()
        self.assertIn('Número inválido', texto)
        self.assertIn('Resultado Aᵀ (3x1)', texto)
        self.assertIn('A[1,2] = -2 → R[2,1] = -2', texto)
        self.assertIn('Resultado Aᵀ (1x3)', texto)
        self.assertIn('Hasta pronto.', texto)
        self.assertFalse(any('B[' in c.args[0] or 'Escalar k:' in c.args[0] for c in entrada.call_args_list))

    def test_producto_procedimiento_y_reutilizacion(self):
        """La opción 6 explica los pares y permite utilizar el resultado en otra operación."""
        entradas = ['1', '6', '1', '2', '1', '2', '2', '1', '3', '4', '1',
                    '4', '2', '2', '1', '3', '9', '9']
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas):
            with redirect_stdout(salida):
                main()
        texto = salida.getvalue()
        self.assertIn('Resultado AB (1x1)', texto)
        self.assertIn('R[1,1] = (1) × (3) + (2) × (4) = 11', texto)
        self.assertIn('R[1,1] = (2) × (11) = 22', texto)
        self.assertIn('Hasta pronto.', texto)

    def test_producto_incompatible_no_borra_ultimo_resultado(self):
        """Un producto inválido mantiene la respuesta anterior y permite salir."""
        entradas = ['1', '5', '1', '1', '7', '2', '6', '2', '1', '2', '1', '3', '4', '3', '9', '9']
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas):
            with redirect_stdout(salida):
                main()
        texto = salida.getvalue()
        self.assertIn('A es 1x1 y B es 2x1', texto)
        self.assertIn('Último resultado (1x1)\n[ 7 ]', texto)
