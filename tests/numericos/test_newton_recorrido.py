"""Verifica pasos y figuras conectados al núcleo real de Newton (#37 y #38).

Tema: coherencia de datos, casos de clase, discontinuidades y exportación.
Equipo responsable: Grupo 9.
"""

from copy import deepcopy
import math
import unittest

from matplotlib.backends.backend_agg import FigureCanvasAgg

from interfaz.metodos_numericos import ejecutar_numerico, parametros_defecto
from interfaz.numericos.figuras import figura_numerica
from interfaz.numericos.newton_graficas import datos_tangente, figura_newton
from interfaz.numericos.newton_presentacion import etapas_newton, tabla_newton
from interfaz.qt.sesion import Sesion
from modulos.numericos.newton import resolver_newton


class PruebasRecorridoNewton(unittest.TestCase):
    """Contrasta la presentación con resultados conocidos sin tocar datos personales."""

    def calcular(self, **cambios):
        """Ejecuta el mismo adaptador usado por el formulario con parámetros explícitos."""
        return ejecutar_numerico('num_newton', dict(parametros_defecto('num_newton'), **cambios))

    def test_exponencial_tabla_previa_y_tangente_coinciden(self):
        """El último renglón, el resumen y el gráfico proceden del mismo cálculo."""
        s = Sesion('num_newton')
        s.cargar_ejemplo()
        s.calcular()
        c = s.presentacion.calculo
        original = deepcopy(c)
        self.assertAlmostEqual(c.valor, .5671432904097838, places=12)
        tabla = tabla_newton(c)
        self.assertEqual(len(tabla['filas']), c.datos['iteraciones'])
        self.assertEqual(float(tabla['filas'][-1][4]), c.valor)
        self.assertAlmostEqual(float(tabla['filas'][-1][-1]), abs(math.exp(-c.valor) - c.valor))
        self.assertEqual(len(s.breves), c.datos['iteraciones'])
        self.assertIn('residuo', s.breves[0].detalle)
        for indice, reg in enumerate(c.datos['registros']):
            m, b = datos_tangente(reg)
            self.assertAlmostEqual(m * reg['xi'] + b, reg['fxi'])
            self.assertAlmostEqual(-b / m, reg['x_siguiente'])
            fig = figura_numerica('num_newton', c, iteracion_seleccionada=indice)
            self.assertTrue(any(f'i={reg["i"]}' in l.get_label() for l in fig.axes[0].lines))
        self.assertEqual(c, original)

    def test_polinomio_de_clase_sin_perder_operaciones(self):
        """La secuencia real desde -1.25 conserva todas las iteraciones y fórmulas."""
        c = self.calcular(funcion='x^5-4*x^4+5*x^3-6*x+4',
                          derivada='5*x^4-16*x^3+15*x^2-6', x0='-1.25')
        self.assertAlmostEqual(c.valor, -1, places=10)
        self.assertAlmostEqual(c.datos['registros'][0]['x_siguiente'], -1.0679966643, places=9)
        self.assertEqual(len(etapas_newton(c)), c.datos['iteraciones'])
        self.assertEqual(len(tabla_newton(c)['filas']), c.datos['iteraciones'])
        self.assertGreater(sum(len(p.formulas) for p in c.pasos), c.datos['iteraciones'])
        FigureCanvasAgg(figura_numerica('num_newton', c)).draw()

    def test_raiz_inicial_dominio_y_porcentaje_indefinido(self):
        """Cero iteraciones no inventa una fila ni una raíz para un punto inválido."""
        for funcion, derivada, x0, esperado in [('x', '1', '0', 0), ('log(x)', '1/x', '-1', None)]:
            c = self.calcular(funcion=funcion, derivada=derivada, x0=x0)
            self.assertEqual(c.valor, esperado)
            self.assertEqual(tabla_newton(c)['filas'], [])
            self.assertEqual(len(etapas_newton(c)), 1)
            fig = figura_numerica('num_newton', c)
            FigureCanvasAgg(fig).draw()
            if esperado is None:
                self.assertFalse(any('Raíz' in obj.get_label() for obj in fig.axes[0].collections))
        c = self.calcular(funcion='x', derivada='1', x0='1', criterio='porcentual')
        self.assertEqual(tabla_newton(c)['filas'][0][6], 'No definido')
        fig = figura_numerica('num_newton', c)
        self.assertIn('%', fig.axes[1].get_ylabel())
        self.assertEqual(fig.axes[2].get_yscale(), 'linear')
        FigureCanvasAgg(fig).draw()

    def test_ciclo_salto_grande_y_maximo_conservan_estado(self):
        """La figura distingue el ciclo del salto que sí termina convergiendo."""
        s = Sesion('num_newton')
        for caso, converge in [('Ciclo cúbico', False), ('Salto x^10-1', True)]:
            s.cargar_ejemplo(caso)
            s.calcular()
            c = s.presentacion.calculo
            self.assertEqual(c.datos['convergio'], converge)
            fig = figura_numerica('num_newton', c, iteracion_seleccionada=99999)
            etiquetas = [obj.get_label() for obj in fig.axes[0].collections]
            self.assertIn('Raíz aproximada' if converge else 'Última aproximación (sin converger)', etiquetas)
            FigureCanvasAgg(fig).draw()
        c = self.calcular(maximo='1')
        self.assertFalse(c.datos['convergio'])
        self.assertEqual(len(tabla_newton(c)['filas']), 1)

    def test_discontinuidad_y_extremos_no_rompen_el_render(self):
        """Los segmentos inválidos se interrumpen y el límite gráfico queda explícito."""
        c = resolver_newton(lambda x: 1 / x, lambda x: -1 / x ** 2, 0, max_iteraciones=2)
        fig = figura_newton(c, lambda x: 1 / x)
        curva = next(l for l in fig.axes[0].lines if l.get_label() == 'f(x)')
        self.assertTrue(any(math.isnan(y) for y in curva.get_ydata()))
        FigureCanvasAgg(fig).draw()
        extremo = resolver_newton(lambda x: x, lambda x: 1., 1e308)
        fig = figura_newton(extremo, lambda x: x)
        self.assertTrue(any('rango gráfico seguro' in t.get_text() for t in fig.axes[0].texts))
        FigureCanvasAgg(fig).draw()
        self.assertIsNone(datos_tangente(dict(xi=1e308, fxi=1., derivada=1e308)))

    def test_comparacion_rechaza_funcion_distinta_y_porcentajes(self):
        """Una cota de bisección solo se superpone a cambio absoluto de la misma función."""
        c = self.calcular()
        p = dict(parametros_defecto('num_biseccion'), funcion=c.datos['funcion'], a='0', b='1')
        b = ejecutar_numerico('num_biseccion', p)
        fig = figura_numerica('num_newton', c, comparacion_biseccion=b)
        self.assertTrue(any('criterio distinto' in l.get_label() for l in fig.axes[1].lines))
        FigureCanvasAgg(fig).draw()
        b.datos['funcion'] = 'x'
        with self.assertRaisesRegex(ValueError, 'misma función'):
            figura_numerica('num_newton', c, comparacion_biseccion=b)
        c = self.calcular(criterio='porcentual')
        with self.assertRaisesRegex(ValueError, 'no es porcentual'):
            figura_numerica('num_newton', c, comparacion_biseccion=b)


if __name__ == '__main__':
    unittest.main()
