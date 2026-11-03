"""Comprueba los límites por ámbito del verificador de reglas.

Tema: imports con alias, cálculo puro y excepción numérica.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import ast
import unittest

from herramientas.comprobar_reglas import revisar_import


class PruebasReglas(unittest.TestCase):
    """Evita que la comprobación dependa del nombre local de una biblioteca."""

    def test_rechaza_bibliotecas_y_aliases_en_algebra(self):
        """Detecta imports externos aunque sus nombres locales sean distintos."""
        fuentes = ['import numpy as np', 'from scipy import linalg as calculos',
                   'import torch', 'from builtins import print as mostrar',
                   'from modulos import numericos', 'from . import numericos',
                   'import interfaz.formato']
        for fuente in fuentes:
            with self.subTest(fuente=fuente):
                self.assertTrue(revisar_import(ast.parse(fuente).body[0], True, False))

    def test_permite_fraction_en_algebra(self):
        """Acepta la herramienta estándar de fracciones autorizada."""
        nodo = ast.parse('from fractions import Fraction').body[0]
        self.assertEqual(revisar_import(nodo, True, False), [])

    def test_excepcion_numerica_no_habilita_interfaz(self):
        """SciPy se permite en la unidad numérica, pero la interfaz sigue separada."""
        nodo = ast.parse('from scipy.optimize import bisect').body[0]
        self.assertEqual(revisar_import(nodo, True, True), [])
        nodo = ast.parse('import interfaz').body[0]
        self.assertTrue(revisar_import(nodo, True, True))
