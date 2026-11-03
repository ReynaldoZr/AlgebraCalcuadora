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
