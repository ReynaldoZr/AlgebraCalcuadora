"""Verifica claridad y conservación de la información del procedimiento.

Tema: vista esencial frente al desarrollo completo, sin cálculos nuevos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import unittest

from interfaz.lenguaje_pasos import explicar_paso
from modulos.procedimientos import Paso


class PruebasLenguajePasos(unittest.TestCase):
    """Protege los datos originales y separa las dos profundidades de explicación."""

    def test_fila_explicada_sin_perder_factor_o_formula(self):
        """La explicación cotidiana acompaña el procedimiento original exacto."""
        paso = Paso('F2 ← F2 − (3/2) F1', 'Creamos un cero debajo del pivote.',
                    [[1, 2], [0, 3]], ((3, '/', 2),))
        breve = explicar_paso(paso)
        completo = explicar_paso(paso, completo=True)
        self.assertIn('múltiplo de otra fila', breve)
        self.assertIn(paso.detalle, completo)
        self.assertIn(breve, completo)
        self.assertEqual(paso.formulas, ((3, '/', 2),))
        self.assertEqual(paso.matriz, [[1, 2], [0, 3]])

    def test_biseccion_explica_decision_y_conserva_intervalo(self):
        """El recorrido explica qué mitad se elige; el desarrollo mantiene la decisión."""
        paso = Paso('Iteración 2', 'Conservamos [xl,xr].')
        self.assertIn('punto medio', explicar_paso(paso))
        self.assertIn('cambia el signo', explicar_paso(paso))
        self.assertIn('[xl,xr]', explicar_paso(paso, completo=True))

    def test_resumen_corto_no_recorta_detalle_completo(self):
        """Acortar una nota en la previa no borra el texto de Todos los pasos."""
        detalle = 'Primera explicación del método. ' * 12
        paso = Paso('Otro procedimiento', detalle)
        self.assertLessEqual(len(explicar_paso(paso)), 150)
        self.assertEqual(explicar_paso(paso, completo=True), detalle.strip())
