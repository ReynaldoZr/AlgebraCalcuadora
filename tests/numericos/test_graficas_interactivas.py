"""Comprueba las mejoras de gráficas interactivas para las issues #23 a #30.

Tema: renderizado headless, escalas seguras, selección de filas, toggles y temas.
Equipo responsable: Grupo 9.
"""

import unittest

from matplotlib.backends.backend_agg import FigureCanvasAgg

from interfaz.metodos_numericos import ejecutar_numerico, parametros_defecto
from interfaz.numericos.figuras import datos_grafica_interactiva, figura_numerica
from modulos.numericos.comparadores import hilbert


class PruebasGraficasInteractivas(unittest.TestCase):
    """Verifica #23-#30 en ambos temas sin abrir ventanas ni alterar algoritmos."""

    def _renderizar(self, fig):
        """Dibuja la figura en memoria para comprobar que Matplotlib no falla."""
        FigureCanvasAgg(fig).draw()

    def test_23_biseccion_apilada_criterios_y_cero_iteraciones(self):
        """Bisección muestra dos paneles, criterio porcentual separado y 0 iteraciones sin inventar error."""
        p = parametros_defecto('num_biseccion')
        calc = ejecutar_numerico('num_biseccion', p)
        for oscuro in (False, True):
            fig = figura_numerica('num_biseccion', calc, oscuro=oscuro, iteracion_seleccionada=2)
            self.assertEqual(len(fig.axes), 2)
            self._renderizar(fig)

        fig_exp = figura_numerica('num_biseccion', calc, oscuro=True, panel_expandido=0)
        self.assertEqual(len(fig_exp.axes), 1)

        p_pct = dict(p, criterio='porcentual', tolerancia='0.5')
        calc_pct = ejecutar_numerico('num_biseccion', p_pct)
        fig_pct = figura_numerica('num_biseccion', calc_pct, iteracion_seleccionada=1)
        self.assertIn('%', fig_pct.axes[1].get_ylabel())

        p_ext = dict(p, funcion='x^2-4', a='-2', b='2')
        calc_ext = ejecutar_numerico('num_biseccion', p_ext)
        fig_ext = figura_numerica('num_biseccion', calc_ext)
        self.assertEqual(len(fig_ext.axes), 1)
        info_ext = datos_grafica_interactiva('num_biseccion', calc_ext)
        self.assertFalse(info_ext['reproducible'])

    def test_24_jacobi_tolerancia_cero_seguro_y_seleccion(self):
        """Jacobi muestra tolerancia, maneja error cero sin log(0) y expone vector de fila."""
        a = [[4, -1, 1], [4, -8, 1], [-2, 1, 5]]
        params = dict(vector_b='7, -21, 15', inicial='0, 0, 0', epsilon='0.0001', maximo='200', reordenar='no')
        calc = ejecutar_numerico('num_jacobi', params, {'A': a})
        fig = figura_numerica('num_jacobi', calc, oscuro=True, iteracion_seleccionada=3)
        self.assertEqual(len(fig.axes), 1)
        self._renderizar(fig)
        info = datos_grafica_interactiva('num_jacobi', calc, iteracion_seleccionada=3)
        self.assertEqual(info['total'], 11)
        self.assertIn('X≈', info['detalle'])

        calc_cero = ejecutar_numerico(
            'num_jacobi',
            dict(vector_b='6', inicial='3', epsilon='0.0001', maximo='10', reordenar='no'),
            {'A': [[2]]},
        )
        fig_cero = figura_numerica('num_jacobi', calc_cero)
        self.assertEqual(fig_cero.axes[0].get_yscale(), 'linear')
        self._renderizar(fig_cero)

    def test_25_gauss_seidel_relajacion_y_reordenamiento(self):
        """Gauss-Seidel muestra relajación lambda, orden y estilo propio."""
        a = [[1, 5], [7, 1]]
        params = dict(vector_b='11, 15', inicial='0, 0', epsilon='0.0001', maximo='200', relajacion='1.1', reordenar='si')
        calc = ejecutar_numerico('num_gauss_seidel', params, {'A': a})
        fig = figura_numerica('num_gauss_seidel', calc, oscuro=False, iteracion_seleccionada=1)
        self.assertIn('λ=', fig.axes[0].get_title())
        self.assertIn('Reordenadas', fig.axes[0].get_title())
        self._renderizar(fig)

    def test_26_comparador_longitudes_reales_y_toggles(self):
        """Comparador conserva longitudes 11 vs 7, permite ocultar curvas y sincroniza selección."""
        a = [[4, -1, 1], [4, -8, 1], [-2, 1, 5]]
        params = dict(vector_b='7, -21, 15', inicial='0, 0, 0', epsilon='0.0001', maximo='200', reordenar='no')
        calc = ejecutar_numerico('num_comparar_iterativos', params, {'A': a})
        fig = figura_numerica('num_comparar_iterativos', calc, iteracion_seleccionada=9)
        self.assertEqual(len(fig.axes[0].lines[0].get_xdata()), 11)
        self.assertEqual(len(fig.axes[0].lines[1].get_xdata()), 7)

        info = datos_grafica_interactiva('num_comparar_iterativos', calc, iteracion_seleccionada=9)
        self.assertIn('finalizada', info['detalle'])

        fig_oculta = figura_numerica('num_comparar_iterativos', calc, visibles={'jacobi': False, 'gauss_seidel': True})
        self.assertEqual(len(fig_oculta.axes[0].lines), 1)  # Solo GS en lines; tolerancia en collections
        self._renderizar(fig_oculta)

    def test_27_propagacion_zoom_delta_cero_y_dominio(self):
        """Propagación enfoca x y x+Δx, maneja Δx=0 y discontinuidades de dominio."""
        for expr, x, delta in (('x^3', '2.5', '0.01'), ('x^3', '2.5', '0'), ('-x^2', '1', '0.1'), ('sqrt(x)', '0.02', '0.05')):
            p = dict(parametros_defecto('num_propagacion'), funcion=expr, x=x, delta=delta)
            calc = ejecutar_numerico('num_propagacion', p)
            fig = figura_numerica('num_propagacion', calc, oscuro=True)
            self._renderizar(fig)

    def test_28_simulacion_toggles_y_casos_borde(self):
        """Simulación soporta 1 iteración, tasa cero y alternancia de curvas."""
        for iters, tasa in (('50', '0.005'), ('1', '0.005'), ('10', '0')):
            p = dict(parametros_defecto('num_simulacion'), iteraciones=iters, tasa=tasa)
            calc = ejecutar_numerico('num_simulacion', p)
            fig = figura_numerica('num_simulacion', calc, visibles={'redondeo': True, 'truncamiento': False})
            self._renderizar(fig)

    def test_29_sistemas_barras_con_variables_y_referencia_fraction(self):
        """Sistemas etiqueta x1..xn y compara Float propio y NumPy frente a Fraction."""
        a = hilbert(5)
        b = [[sum(f)] for f in a]
        calc = ejecutar_numerico('num_sistema', {}, {'A': a, 'b': b})
        fig = figura_numerica('num_sistema', calc, oscuro=False)
        etiquetas = [t.get_text() for t in fig.axes[0].get_xticklabels()]
        self.assertEqual(etiquetas, ['x₁', 'x₂', 'x₃', 'x₄', 'x₅'])
        self._renderizar(fig)

    def test_30_inversas_mapa_dinamico_y_log_seguro(self):
        """Inversas genera mapa n×n dinámico, tolera ceros con escala segura y permite LogNorm positivo."""
        ident = [[1, 0], [0, 1]]
        calc_id = ejecutar_numerico('num_inversa', {}, {'A': ident})
        fig_id = figura_numerica('num_inversa', calc_id, mostrar_log=True)
        self._renderizar(fig_id)

        calc_h = ejecutar_numerico('num_inversa', {}, {'A': hilbert(5)})
        fig_h = figura_numerica('num_inversa', calc_h, oscuro=True, mostrar_log=True)
        self.assertIn('5×5', fig_h.axes[0].get_title())
        self._renderizar(fig_h)


if __name__ == '__main__':
    unittest.main()
