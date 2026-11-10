"""Comprueba el significado de las etapas sin necesitar widgets ni pantalla.

Tema: equivalencias exactas, signos y destino de resultados.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction
import unittest

from interfaz.explicacion import construir_etapas, etapas_completas, etapas_de_paso


class PruebasExplicacion(unittest.TestCase):
    """Verifica explicaciones con respuestas conocidas de las tres operaciones."""

    def test_desarrollo_producto_explica_denominador_signos_y_reduccion(self):
        """El escrito amplía la suma fraccionaria y el recorrido breve queda intacto."""
        paso = (0, 0, (Fraction(1, 3), Fraction(-1, 6)), (1, 1), Fraction(1, 6), 'AB')
        breve = etapas_de_paso(paso, 0)
        completo = etapas_completas(paso, 0)
        denominador = next(e for e in completo if e.fase == 'denominador')
        self.assertEqual(denominador.tokens, ((2, 6), '+', '(', (-1, 6), ')', '=', ('2 + (-1)', 6), '=', (1, 6)))
        self.assertEqual(completo[-1].tokens, ('R[1,1]', '=', Fraction(1, 6)))
        self.assertEqual(etapas_de_paso(paso, 0), breve)
        cero = etapas_completas((0, 0, (Fraction(1, 3), Fraction(-1, 3)), (1, 1), 0, 'AB'), 0)
        self.assertEqual(cero[-2].tokens, ((0, 3), '=', 0))
        self.assertIn('entre 3', cero[-2].mensaje)

    def test_producto_fraccional_expande_y_simplifica(self):
        """kA presenta el producto literal, su fracción intermedia y la reducción."""
        paso = (0, 0, Fraction(-3, 2), Fraction(1, 3), Fraction(-1, 2), '×')
        etapas = etapas_de_paso(paso, 0)
        self.assertEqual([e.fase for e in etapas], ['identificar', 'operar', 'simplificar', 'guardar'])
        self.assertEqual(etapas[1].tokens, (('(-3) × 1', '2 × 3'), '=', (-3, 6)))
        self.assertIn('entre 3', etapas[2].mensaje)
        self.assertEqual(etapas[-1].tokens, ('R[1,1]', '=', Fraction(-1, 2)))

    def test_suma_sin_reduccion_no_inventa_simplificacion(self):
        """Una fracción irreducible pasa de la operación a su destino."""
        paso = (1, 2, Fraction(1, 10), Fraction(1, 5), Fraction(3, 10), '+')
        etapas = etapas_de_paso(paso, 5)
        self.assertEqual([e.fase for e in etapas], ['identificar', 'operar', 'guardar'])
        self.assertEqual(etapas[1].tokens, ((1, 10), '+', (2, 10), '=', (3, 10)))
        self.assertIn('A[2,3]', etapas[0].operandos)
        self.assertIn('B[2,3]', etapas[0].operandos)
        self.assertEqual(etapas[-1].tokens[0], 'R[2,3]')

    def test_resta_de_negativo_conserva_signos(self):
        """La resta agrupa el negativo y muestra los numeradores equivalentes."""
        paso = (0, 0, Fraction(1, 3), Fraction(-1, 6), Fraction(1, 2), '-')
        etapas = etapas_de_paso(paso, 0)
        self.assertEqual(etapas[1].tokens, ((2, 6), '-', '(', (-1, 6), ')', '=', (3, 6)))
        self.assertEqual(etapas[-1].tokens[-1], Fraction(1, 2))

    def test_cero_y_enteros_tienen_explicacion_valida(self):
        """Cero puede simplificarse sin dividir entre cero; enteros no lo necesitan."""
        cero = etapas_de_paso((0, 0, 0, Fraction(1, 3), Fraction(0), '×'), 0)
        self.assertIn('entre 3', cero[2].mensaje)
        enteros = etapas_de_paso((0, 0, -2, -5, 10, '×'), 0)
        self.assertEqual([e.fase for e in enteros], ['identificar', 'operar', 'guardar'])
        self.assertEqual(enteros[1].tokens, (-2, '×', '(', -5, ')', '=', 10))

    def test_secuencia_conserva_orden_y_resultados_originales(self):
        """Cada celda termina de guardarse antes de comenzar la siguiente."""
        pasos = [(0, 0, 1, 2, 3, '+'), (0, 1, 3, 2, 1, '-')]
        copia = pasos[:]
        etapas = construir_etapas(pasos)
        self.assertEqual([e.posicion for e in etapas], [0, 0, 0, 1, 1, 1])
        self.assertEqual(etapas[2].fase, 'guardar')
        self.assertEqual(etapas[3].fase, 'identificar')
        self.assertEqual(pasos, copia)
        self.assertEqual(construir_etapas([]), ())

    def test_transpuesta_identifica_origen_distinto_del_destino(self):
        """R[2,1] procede de A[1,2], sin operación ni simplificación numérica."""
        etapas = etapas_de_paso((1, 0, Fraction(-2, 3), None, Fraction(-2, 3), 'T'), 2)
        self.assertEqual([e.fase for e in etapas], ['identificar', 'ubicar', 'guardar'])
        self.assertIn('Origen A[1,2] = -2/3', etapas[0].operandos)
        self.assertEqual(etapas[1].tokens, ('A[1,2]', '→', 'R[2,1]'))
        self.assertEqual(etapas[-1].tokens, ('R[2,1]', '=', Fraction(-2, 3)))

    def test_producto_senala_pares_y_suma_sin_guardar_antes(self):
        """Fila por columna tiene un producto por par, suma y destino al final."""
        etapas = etapas_de_paso((0, 1, (1, 2, 3), (0, 1, 3), 11, 'AB'), 1)
        self.assertEqual([e.fase for e in etapas], ['identificar', 'multiplicar', 'multiplicar', 'multiplicar', 'sumar', 'guardar'])
        self.assertEqual([e.par for e in etapas], [None, 0, 1, 2, None, None])
        self.assertIn('A[1,3] = 3', etapas[3].operandos)
        self.assertIn('B[3,2] = 3', etapas[3].operandos)
        self.assertEqual(etapas[-2].tokens, (0, '+', 2, '+', 9, '=', 11))
        self.assertEqual(etapas[-1].tokens, ('R[1,2]', '=', 11))

    def test_producto_fraccional_simplifica_cada_termino(self):
        """Las fracciones de cada par se explican antes de sumarlas con sus signos."""
        paso = (0, 0, (Fraction(1, 3), -2), (Fraction(3, 2), Fraction(1, 4)), Fraction(0), 'AB')
        etapas = etapas_de_paso(paso, 0)
        reducciones = [e for e in etapas if e.fase == 'simplificar']
        self.assertEqual([e.tokens[-1] for e in reducciones], [Fraction(1, 2), Fraction(-1, 2)])
        self.assertEqual(etapas[-2].tokens, (Fraction(1, 2), '+', '(', Fraction(-1, 2), ')', '=', 0))
