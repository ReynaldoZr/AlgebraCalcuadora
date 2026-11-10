"""Comprueba el catálogo y el uso de consola de los nuevos temas.

Tema: adaptación de resultados y recorrido desde entrada hasta procedimiento.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import io
import unittest
from contextlib import redirect_stdout
from fractions import Fraction
from unittest.mock import patch

from interfaz.datos import convertir_numero
from interfaz.menu_algebra import ejecutar_metodo, formatear_pasos
from interfaz.operaciones import OPERACIONES, calcular_operacion, ejemplo_operacion
from main import main


class PruebasOperaciones(unittest.TestCase):
    """Valida el catálogo completo, orientaciones y errores recuperables en consola."""

    def test_ejemplos_catalogo_y_respuestas_conocidas(self):
        """Cada opción es ejecutable y los métodos devuelven los valores esperados."""
        valores = {'gauss': [2, 1], 'jordan': [2, 1], 'v_suma': [4, 1, 5],
                   'v_resta': [-2, 3, 1], 'v_escalar': [3, 6, 9], 'combinacion': [2, 3],
                   'independencia': False, 'det_reduccion': 1, 'det_cofactores': 1,
                   'det_sarrus': 1, 'inv_jordan': [[-2, 1], [Fraction(3, 2), Fraction(-1, 2)]],
                   'inv_adjunta': [[-2, 1], [Fraction(3, 2), Fraction(-1, 2)]], 'lu_resolver': [1, 1, 2]}
        for clave in OPERACIONES:
            with self.subTest(clave=clave):
                datos, escalar = ejemplo_operacion(clave)
                presentacion = calcular_operacion(clave, datos, convertir_numero(escalar))
                self.assertTrue(presentacion.calculo.pasos)
                if clave in valores:
                    self.assertEqual(presentacion.calculo.valor, valores[clave])
                if clave.startswith('prop_') and clave != 'prop_todas':
                    self.assertTrue(presentacion.calculo.valor[0].cumple)

    def test_consola_gauss_desde_menu_principal_con_todos_los_pasos(self):
        """Lee A y b, resuelve y vuelve sin pedir reingresar datos intermedios."""
        entradas = ['2', '1', '2', '2', '2', '1', '1', '-1', '2', '1', '5', '1', '1', '99', '9']
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas), redirect_stdout(salida):
            main()
        texto = salida.getvalue()
        self.assertIn('Solución única', texto)
        self.assertIn('x1 = 2', texto)
        self.assertIn('x2 = 1', texto)
        self.assertIn('Comprobación en el sistema original', texto)
        self.assertIn('Matriz aumentada', texto)
        self.assertIn('Hasta pronto', texto)

    def test_consola_error_conserva_resultado_y_teoremas_disponibles(self):
        """Una dimensión vectorial inválida no borra la respuesta de la sesión."""
        anterior = [[7]]
        with patch('interfaz.menu_algebra.elegir_matriz', side_effect=[[[1, 2]], [[1]]]):
            with redirect_stdout(io.StringIO()) as salida:
                self.assertIs(ejecutar_metodo('v_suma', anterior), anterior)
        self.assertIn('No se pudo calcular', salida.getvalue())
        with patch('builtins.input', side_effect=['6', '0', '99', '9']), redirect_stdout(io.StringIO()) as salida:
            main()
        self.assertIn('PA=LU', salida.getvalue())

    def test_orientacion_y_formulas_completas(self):
        """b y los vectores exigen su orientación; el texto conserva todas las fórmulas."""
        with self.assertRaisesRegex(ValueError, 'columna'):
            calcular_operacion('gauss', {'A': [[1, 0], [0, 1]], 'b': [[1, 2]]})
        with self.assertRaisesRegex(ValueError, 'fila'):
            calcular_operacion('v_suma', {'A': [[1], [2]], 'B': [[1], [2]]})
        datos, _ = ejemplo_operacion('inv_jordan')
        calculo = calcular_operacion('inv_jordan', datos).calculo
        texto = formatear_pasos(calculo.pasos)
        self.assertIn('c4:', texto)
        self.assertIn('Comprobación A·A⁻¹ = I', texto)
