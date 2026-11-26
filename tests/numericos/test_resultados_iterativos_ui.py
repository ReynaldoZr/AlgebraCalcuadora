"""Comprueba la presentación estructurada de resultados iterativos (Issue #32).

Tema: tabla por variable, referencia para comparar, redondeo visual y detalles técnicos.
Equipo responsable: Grupo 9.
"""

import unittest

from interfaz.metodos_numericos import (
    ejecutar_numerico, formato_visual, parametros_defecto,
    resumen_iterativo_estructurado, resumen_numerico,
)
from interfaz.qt.resumen_tabla import resumen_estructurado
from interfaz.operaciones import Presentacion
from modulos.procedimientos import Calculo


class PruebasResultadosIterativosUI(unittest.TestCase):
    """Verifica la estructura de resultados sin depender de widgets ni hardcodear dimensiones."""

    def test_caso_profesor_y_etiquetas_referencia(self):
        """El caso 4x4 del profesor muestra ambos métodos, tabla x1..x4 y referencia sin llamarla exacta."""
        a = [[8, -1, 0, 1], [1, 9, -1, 0], [0, -1, 7, 1], [1, 0, 1, 8]]
        params = dict(vector_b='10, -10, 16, 11', inicial='0, 0, 0, 0',
                      epsilon='0.03', maximo='200', reordenar='no')
        calculo = ejecutar_numerico('num_comparar_iterativos', params, {'A': a})
        res = resumen_iterativo_estructurado('num_comparar_iterativos', calculo)
        self.assertTrue(res['activo'])
        self.assertEqual([f[0] for f in res['filas']], ['x₁', 'x₂', 'x₃', 'x₄'])
        self.assertEqual(res['metodos'][0]['iteraciones'], 4)
        self.assertEqual(res['metodos'][1]['iteraciones'], 3)
        self.assertIn('menos iteraciones', res['comparacion_iteraciones'])
        self.assertIn('Referencia para comparar', res['columnas'])
        texto_plano = resumen_numerico('num_comparar_iterativos', calculo)
        self.assertNotIn('valor real', texto_plano.lower())
        self.assertNotIn('solución exacta', texto_plano.lower())
        self.assertIn('Referencia para comparar', texto_plano)

    def test_dimensiones_dinamicas_1_3_y_10(self):
        """La tabla se adapta dinámicamente a n=1, n=3 y n=10."""
        for n in (1, 3, 10):
            a = [[4 if i == j else 0 for j in range(n)] for i in range(n)]
            b_txt = ', '.join('4' for _ in range(n))
            x0_txt = ', '.join('0' for _ in range(n))
            params = dict(vector_b=b_txt, inicial=x0_txt, epsilon='0.001', maximo='50', reordenar='no')
            calculo = ejecutar_numerico('num_comparar_iterativos', params, {'A': a})
            res = resumen_iterativo_estructurado('num_comparar_iterativos', calculo)
            self.assertEqual(len(res['filas']), n)
            self.assertEqual(res['filas'][0][0], 'x₁')

    def test_no_declara_ganador_si_solo_uno_o_ninguno_converge(self):
        """Si un método falla o ambos agotan iteraciones, no declara ganador y deja aviso visible."""
        a = [[1, 5], [7, 1]]
        params = dict(vector_b='11, 15', inicial='0, 0', epsilon='0.0001', maximo='3', reordenar='no')
        calculo = ejecutar_numerico('num_comparar_iterativos', params, {'A': a})
        res = resumen_iterativo_estructurado('num_comparar_iterativos', calculo)
        self.assertEqual(res['comparacion_iteraciones'], '')
        self.assertTrue(res['advertencias'])

    def test_referencia_singular_se_informa_en_advertencias(self):
        """Una matriz singular en NumPy no rompe el resumen y deja aviso visible."""
        a = [[1, 2], [2, 4]]
        params = dict(vector_b='3, 6', inicial='0, 0', epsilon='0.01', maximo='2', reordenar='no')
        calculo = ejecutar_numerico('num_comparar_iterativos', params, {'A': a})
        res = resumen_iterativo_estructurado('num_comparar_iterativos', calculo)
        self.assertFalse(res['referencia_disponible'])
        self.assertTrue(any('Referencia' in a for a in res['advertencias']))
        self.assertEqual(res['filas'][0][-1], 'No disponible')

    def test_formato_visual_notacion_cientifica_y_detalles_precision_completa(self):
        """Los errores pequeños no se muestran como cero y los detalles conservan precisión completa."""
        self.assertEqual(formato_visual(0.0), '0')
        self.assertIn('e-', formato_visual(1.2345e-7))
        a = [[4, -1, 1], [4, -8, 1], [-2, 1, 5]]
        params = dict(vector_b='7, -21, 15', inicial='0, 0, 0', epsilon='1e-8', maximo='200', reordenar='no')
        calculo = ejecutar_numerico('num_jacobi', params, {'A': a})
        res = resumen_iterativo_estructurado('num_jacobi', calculo)
        self.assertTrue(res['activo'])
        self.assertTrue(any('Cambio final' in d['titulo'] for d in res['detalles_tecnicos']))
        self.assertTrue(any('Residuo' in d['titulo'] for d in res['detalles_tecnicos']))

    def test_tabla_universal_para_otros_metodos(self):
        """Newton, bisección, errores y álgebra exacta muestran tabla adaptada y detalles."""
        calc_new = ejecutar_numerico('num_newton', dict(parametros_defecto('num_newton'), funcion='exp(-x)-x', x0='0', derivada='-exp(-x)-1'))
        res_new = resumen_estructurado('num_newton', Presentacion(calc_new, resumen_numerico('num_newton', calc_new), None))
        self.assertTrue(res_new['activo'])
        self.assertTrue(any(f[0] == 'Raíz aproximada' for f in res_new['filas']))

        calc_bis = ejecutar_numerico('num_biseccion', parametros_defecto('num_biseccion'))
        res_bis = resumen_estructurado('num_biseccion', Presentacion(calc_bis, resumen_numerico('num_biseccion', calc_bis), None))
        self.assertTrue(res_bis['activo'])

        calc_err = ejecutar_numerico('num_errores', parametros_defecto('num_errores'))
        res_err = resumen_estructurado('num_errores', Presentacion(calc_err, resumen_numerico('num_errores', calc_err), None))
        self.assertTrue(res_err['activo'])

        pres_exacta = Presentacion(Calculo([[2]], (), {}), 'Suma exacta', [[2]])
        res_suma = resumen_estructurado('sumar', pres_exacta)
        self.assertTrue(res_suma['activo'])

    def test_redondeo_no_oculta_aproximaciones_distintas(self):
        """Aumenta la precisión visible cuando dos valores distintos redondean igual."""
        params = dict(vector_b='1', inicial='0', epsilon='1e-8', maximo='20', reordenar='no')
        calc = ejecutar_numerico('num_comparar_iterativos', params, {'A': [[1]]})
        calc.datos['valor_jacobi'] = [1.00000000001]
        calc.datos['valor_gauss_seidel'] = [1.00000000002]
        res = resumen_iterativo_estructurado('num_comparar_iterativos', calc)
        self.assertEqual(len(set(res['filas'][0][1:])), 3)
        self.assertEqual(calc.datos['valor_jacobi'][0], 1.00000000001)

    def test_causa_de_fallo_y_relajacion_visibles(self):
        """El desbordamiento se informa aun antes de la primera iteración completa."""
        params = dict(vector_b='1e308, 1e308', inicial='0, 0', epsilon='1e-8',
                      maximo='20', reordenar='no')
        calc = ejecutar_numerico('num_comparar_iterativos', params, {'A': [[1e-308, 1], [1, 1e-308]]})
        res = resumen_iterativo_estructurado('num_comparar_iterativos', calc)
        self.assertTrue(any('no finitos' in aviso for aviso in res['advertencias']))
        params.update(vector_b='1', inicial='0', relajacion='1.5')
        calc = ejecutar_numerico('num_gauss_seidel', params, {'A': [[2]]})
        res = resumen_iterativo_estructurado('num_gauss_seidel', calc)
        self.assertTrue(any('Relajación' in aviso for aviso in res['advertencias']))


if __name__ == '__main__':
    unittest.main()
