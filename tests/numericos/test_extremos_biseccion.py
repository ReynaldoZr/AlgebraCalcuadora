"""Comprueba raíces en ambos extremos y su presentación reutilizable.

Tema: regresión de la issue #13, resumen, pasos y gráfica de bisección.
Equipo responsable: Grupo 9.
"""

from copy import deepcopy
import unittest

from modulos.numericos.biseccion import biseccion


class PruebasExtremosBiseccion(unittest.TestCase):
    """Usa raíces conocidas y figuras en memoria sin controlar la pantalla."""

    @classmethod
    def setUpClass(cls):
        """Respeta el contrato de dependencias opcionales de la unidad numérica."""
        from tests.numericos.test_semana12 import PruebasSemana12
        PruebasSemana12.setUpClass()

    def test_ambos_extremos_conservan_raices_y_cero_iteraciones(self):
        """x²−4 reconoce −2 y 2, manteniendo un valor principal escalar."""
        c = biseccion('x^2-4', -2, 2)
        self.assertEqual(c.datos['raices_extremos'], (-2, 2))
        self.assertEqual(c.valor, -2)
        self.assertTrue(c.datos['convergio'])
        self.assertEqual(c.datos['filas'], [])
        self.assertEqual(c.datos['residuo'], 0)
        self.assertEqual(c.datos['scipy'], -2)
        self.assertEqual(c.datos['diferencia_scipy'], 0)
        formulas = str([p.formulas for p in c.pasos])
        self.assertIn('f(-2)=(-2)^2-4=0', formulas)
        self.assertIn('f(2)=(2)^2-4=0', formulas)

    def test_un_solo_extremo_y_raiz_interior(self):
        """Los extremos individuales y la tabla de una raíz interior siguen válidos."""
        for a, b in ((1, 3), (-1, 1)):
            with self.subTest(a=a, b=b):
                c = biseccion('x-1', a, b)
                self.assertEqual(c.datos['raices_extremos'], (1,))
                self.assertEqual(c.valor, 1)
                self.assertEqual(c.datos['filas'], [])
        c = biseccion('x^2-2', 1, 2)
        self.assertAlmostEqual(c.valor, 2 ** 0.5, delta=0.0001)
        self.assertTrue(c.datos['filas'])
        with self.assertRaisesRegex(ValueError, 'cambio de signo'):
            biseccion('x^2+1', -1, 1)

    def test_resumen_identifica_ambas_raices_y_el_valor_guardable(self):
        """El texto que reciben consola y ambas interfaces incluye las dos raíces."""
        from interfaz.metodos_numericos import resumen_numerico
        resumen = resumen_numerico('num_biseccion', biseccion('x^2-4', -2, 2))
        self.assertIn('Raíces en los extremos: -2, 2', resumen)
        self.assertIn('Valor principal para guardar: -2', resumen)
        self.assertIn('Iteraciones realizadas: 0', resumen)

    def test_figura_marca_ambas_raices_y_se_renderiza(self):
        """La gráfica muestra los dos puntos con etiquetas y evita una gráfica de error vacía."""
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        from interfaz.numericos.figuras import figura_numerica
        figura = figura_numerica('num_biseccion', biseccion('x^2-4', -2, 2))
        self.assertEqual(len(figura.axes), 1)
        eje = figura.axes[0]
        self.assertEqual(eje.collections[0].get_offsets().tolist(), [[-2, 0], [2, 0]])
        self.assertEqual([t.get_text() for t in eje.texts], ['x=-2', 'x=2'])
        FigureCanvasAgg(figura).draw()

    def test_guardado_y_reapertura_conservan_los_dos_extremos(self):
        """Guardar un ejercicio conserva los parámetros y recalcular recupera ambas raíces."""
        from interfaz.biblioteca import validar_registro
        from interfaz.qt.sesion import Sesion
        sesion = Sesion('num_biseccion')
        sesion.parametros.update(funcion='x^2-4', a='-2', b='2')
        sesion.calcular()
        registro = sesion.registro()
        validar_registro(registro)
        nueva = Sesion('num_biseccion')
        nueva.parametros.update(deepcopy(registro['parametros']))
        nueva.calcular()
        self.assertEqual(nueva.presentacion.calculo.datos['raices_extremos'], (-2, 2))
        resultado = sesion.registro('resultado')
        validar_registro(resultado)
        self.assertEqual(float(resultado['valor']), -2)
        self.assertIn('Raíces en los extremos: -2, 2', resultado['resumen'])

    def test_extremos_no_afirma_agotar_las_raices_interiores(self):
        """El caso con raíz interior adicional mantiene explícito el alcance de la comprobación."""
        c = biseccion('x*(x^2-4)', -2, 2)
        self.assertEqual(c.datos['raices_extremos'], (-2, 2))
        self.assertIn('intervalos adicionales', c.pasos[-1].detalle)

    def test_sustitucion_respeta_los_nombres_de_funciones(self):
        """Reemplaza la variable x sin alterar exp en una fórmula explicada."""
        c = biseccion('exp(x)-1', 0, 1)
        self.assertIn('f(0)=exp((0))-1=0', str([p.formulas for p in c.pasos]))
