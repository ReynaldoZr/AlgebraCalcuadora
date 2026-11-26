"""Regresiones matemáticas de la revisión del PR 46.

Tema: presentación fiel de no convergencia, precisión y datos originales.
Equipo responsable: Grupo 9.
"""

from copy import deepcopy
import unittest

from interfaz.metodos_numericos import ejecutar_numerico, parametros_defecto
from interfaz.numericos.newton_presentacion import pasos_completos_newton
from interfaz.operaciones import Presentacion
from interfaz.qt.resumen_tabla import resumen_estructurado
from modulos.numericos.newton import resolver_newton


class PruebasRevisionPresentacion(unittest.TestCase):
    """Comprueba que el resumen y los pasos respetan el estado del núcleo."""

    def test_estancamiento_no_se_anuncia_como_tolerancias_cumplidas(self):
        """Una corrección subdesbordada a cero no demuestra convergencia."""
        c = resolver_newton(lambda x: 1e-300, lambda x: 1e300, 1)
        self.assertFalse(c.datos['convergio'])
        self.assertIn('Estancamiento', c.datos['motivo'])
        pasos = pasos_completos_newton(c)
        self.assertIn('sin convergencia', str(pasos))
        self.assertNotIn('tolerancias cumplidas', str(pasos))
        # Se conservan todas las fórmulas originales, no una sustitución redondeada.
        self.assertEqual(len(pasos), len(c.pasos))
        self.assertEqual(len(c.pasos[1].formulas), 4)

    def test_precision_y_titulos_no_controlan_la_asociacion_de_registros(self):
        """La relación con una fila no depende de interpretar títulos en español."""
        from dataclasses import replace
        c = resolver_newton(lambda x: x*x-2, lambda x: 2*x, 1, tolerancia=1e-12)
        c = replace(c, pasos=tuple(replace(p, titulo='Etapa') for p in c.pasos))
        original = deepcopy(c)
        p = pasos_completos_newton(c)
        self.assertEqual(len(p), len(c.pasos))
        self.assertIn('¿Detener?', str(p))
        self.assertIn('1.414213562', str(p))
        self.assertEqual(c, original)

    def test_ciclo_y_dominio_no_se_etiquetan_como_raices(self):
        """La tabla resumida diferencia último punto y ausencia de punto válido."""
        for f, df, x in [('x^3-2*x+2', '3*x^2-2', '0'), ('log(x)', '1/x', '-1')]:
            p = dict(parametros_defecto('num_newton'), funcion=f, derivada=df, x0=x)
            c = ejecutar_numerico('num_newton', p)
            r = resumen_estructurado('num_newton', Presentacion(c, '', None))
            self.assertEqual(r['filas'][0][0], 'Última aproximación')
            self.assertFalse(r['metodos'][0]['convergio'])
            self.assertTrue(r['advertencias'])
            self.assertEqual(r['metodos'][0]['error_corto'], 'No definido' if c.valor is None else '1.000000')

    def test_biseccion_maximo_y_dos_extremos_mantienen_estado_y_guardado(self):
        """No fuerza éxito al agotar máximo y conserva el valor principal para guardar."""
        p = dict(parametros_defecto('num_biseccion'), funcion='cos(x)-x', a='0', b='1', maximo='1')
        c = ejecutar_numerico('num_biseccion', p)
        r = resumen_estructurado('num_biseccion', Presentacion(c, '', None))
        self.assertFalse(r['metodos'][0]['convergio'])
        self.assertEqual(r['filas'][0][0], 'Última aproximación')
        self.assertTrue(r['advertencias'])
        self.assertEqual(r['metodos'][0]['etiqueta_error'], 'Diferencia con SciPy')
        c = ejecutar_numerico('num_biseccion', dict(p, funcion='x^2-4', a='-2', b='2'))
        r = resumen_estructurado('num_biseccion', Presentacion(c, '', None))
        self.assertIn(['Raíces en extremos', '-2.000000, 2.000000'], r['filas'])
        self.assertTrue(any(f[0] == 'Valor principal para guardar' for f in r['filas']))


if __name__ == '__main__':
    unittest.main()
