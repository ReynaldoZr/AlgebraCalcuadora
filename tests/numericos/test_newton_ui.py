"""Comprueba adaptador, presentación, tabla y gráficas de Newton con fixtures (#36, #37, #38).

Tema: desarrollo paralelo contra el contrato #33 sin importar módulos inexistentes.
Equipo responsable: Grupo 9.
"""

import math
import unittest

from interfaz.numericos.newton_adaptador import (
    ejemplo_newton, ejecutar_newton_adaptador,
    parametros_vacios_newton, resumen_newton, validar_entrada_newton,
)
from interfaz.numericos.newton_graficas import datos_tangente, figura_newton
from interfaz.numericos.newton_presentacion import (
    COLUMNAS_TABLA_NEWTON, pasos_completos_newton, pasos_previa_newton, tabla_newton,
)
from modulos.procedimientos import Calculo, Paso


def _fixture_newton(registros, valor, convergio=True, motivo='Tolerancia alcanzada.',
                    criterio='absoluto', tolerancia=1e-8, residuo=0.0):
    """Construye un Calculo conforme al contrato propuesto en la issue #33."""
    pasos = tuple(
        Paso(
            f'Iteración {r["i"]}',
            f'x{r["i"]} = {r["xi"]}',
            formulas=((f'x{r["i"] + 1} = {r["x_siguiente"]}',),),
        )
        for r in registros
    )
    filas = tuple(
        (
            r['i'], r['xi'], r['fxi'], r['derivada'],
            r['x_siguiente'], r['error_absoluto'], r['error_porcentual'], r['residuo'],
        )
        for r in registros
    )
    datos = dict(
        metodo='newton',
        convergio=convergio,
        motivo=motivo,
        iteraciones=len(registros),
        residuo=residuo,
        criterio=criterio,
        tolerancia=tolerancia,
        columnas=COLUMNAS_TABLA_NEWTON,
        filas=filas,
        registros=tuple(registros),
    )
    return Calculo(valor, pasos, datos)


class PruebasNewtonUI(unittest.TestCase):
    """Verifica #36, #37 y #38 usando exclusivamente fixtures del contrato #33."""

    def test_campos_iniciales_vacios_y_validaciones_36(self):
        """Los campos del ejercicio inician vacíos y rechazan entradas inválidas."""
        vacios = parametros_vacios_newton()
        self.assertEqual(vacios['funcion'], '')
        self.assertEqual(vacios['x0'], '')
        self.assertEqual(vacios['derivada'], '')
        with self.assertRaises(ValueError):
            validar_entrada_newton(vacios)

        ej = ejemplo_newton('exp(-x)-x')
        ej['modo_derivada'] = 'numerica'
        ej['h'] = '-0.01'
        with self.assertRaises(ValueError):
            validar_entrada_newton(ej)

    def test_derivada_numerica_y_resumen_36(self):
        """El resumen evita llamar valor real a una aproximación del solver inyectado."""
        ej = ejemplo_newton('exp(-x)-x')
        calculo = _fixture_newton(
            [dict(i=1, xi=0.0, fxi=1.0, derivada=-2.0, x_siguiente=0.5,
                  error_absoluto=0.5, error_porcentual=100.0, residuo=0.1065306597)],
            valor=0.5671432904,
            convergio=True,
            residuo=1e-10,
        )
        recibido = ejecutar_newton_adaptador(ej, solver=lambda *a, **kw: calculo)
        self.assertEqual(recibido.valor, 0.5671432904)
        texto = resumen_newton(recibido)
        self.assertIn('Convergió', texto)
        self.assertNotIn('valor real', texto.lower())

    def test_previa_pasos_y_tabla_37(self):
        """La tabla conserva columnas, precisión y 'No definido' sin rellenar con cero."""
        calc = _fixture_newton(
            [
                dict(i=1, xi=1.0, fxi=1.0, derivada=1.0, x_siguiente=0.0,
                     error_absoluto=1.0, error_porcentual=None, residuo=0.0),
            ],
            valor=0.0,
            convergio=True,
            criterio='porcentual',
            residuo=0.0,
        )
        previa = pasos_previa_newton(calc)
        self.assertEqual(len(previa), 1)
        completos = pasos_completos_newton(calc)
        self.assertEqual(len(completos), 1)
        tabla = tabla_newton(calc)
        self.assertEqual(len(tabla['columnas']), 8)
        self.assertEqual(tabla['filas'][0][6], 'No definido')

        calc_cero = _fixture_newton([], valor=1.0, convergio=True, motivo='Raíz exacta en x0.', residuo=0.0)
        self.assertEqual(len(pasos_previa_newton(calc_cero)), 1)
        self.assertEqual(tabla_newton(calc_cero)['filas'], [])

    def test_grafica_tangente_escala_segura_y_biseccion_38(self):
        """Genera figura sin pyplot, verifica pendiente/intercepto y maneja residuo cero y discontinuidades."""
        reg = dict(i=1, xi=0.0, fxi=1.0, derivada=-2.0, x_siguiente=0.5,
                   error_absoluto=0.5, error_porcentual=100.0, residuo=0.0)
        tangente = datos_tangente(reg)
        self.assertEqual(tangente, (-2.0, 1.0))

        calc = _fixture_newton([reg], valor=0.5, convergio=False, motivo='Máximo de iteraciones.', residuo=0.0)
        fig = figura_newton(calc, funcion=lambda x: math.exp(-x) - x)
        self.assertEqual(len(fig.axes), 3)
        self.assertEqual(fig.axes[2].get_yscale(), 'linear')

        # Discontinuidad en 1/x no debe lanzar excepción al graficar
        fig_disc = figura_newton(calc, funcion=lambda x: 1.0 / x)
        self.assertEqual(len(fig_disc.axes), 3)

        # Comparación opcional con bisección
        bis = Calculo(0.567, (), dict(filas=[(1, 0, 1, 0.5, 1, 0.1, 0.1, 1, 0.5)]))
        fig_comp = figura_newton(calc, funcion=lambda x: math.exp(-x) - x, comparacion_biseccion=bis)
        self.assertEqual(len(fig_comp.axes), 3)
        sin_funcion = figura_newton(calc)
        self.assertFalse(any('aproximación' in c.get_label().lower()
                             for c in sin_funcion.axes[0].collections))

    def test_derivada_numerica_usa_proveedor_integrado_y_valida_h(self):
        """El adaptador no duplica el cálculo de #34 ni acepta un h indistinguible."""
        from unittest.mock import Mock
        ej = ejemplo_newton()
        ej.update(modo_derivada='numerica', h='1e-5')
        args_reales = validar_entrada_newton(ej)
        self.assertAlmostEqual(args_reales['derivada'](0), -2, places=8)
        derivada = lambda x: -math.exp(-x) - 1
        proveedor = Mock(return_value=derivada)
        args = validar_entrada_newton(ej, proveedor)
        self.assertIs(args['derivada'], derivada)
        self.assertEqual(proveedor.call_args.args[1], 1e-5)
        for valor in ('0', '-1', 'nan', 'inf', '1e-300'):
            with self.subTest(h=valor), self.assertRaises(ValueError):
                validar_entrada_newton(dict(ej, x0='2', h=valor), proveedor)
        with self.assertRaises(ValueError):
            validar_entrada_newton(dict(ej, maximo='10001'), proveedor)

    def test_porcentaje_y_residuo_separan_unidades(self):
        """La tolerancia porcentual no se dibuja sobre el residuo ni una cota absoluta."""
        reg = dict(i=1, xi=0., fxi=1., derivada=-2., x_siguiente=.5,
                   error_absoluto=.5, error_porcentual=100., residuo=.1)
        calc = _fixture_newton([reg], .5, criterio='porcentual', convergio=False)
        fig = figura_newton(calc, lambda x: math.exp(-x) - x)
        self.assertIn('%', fig.axes[1].get_ylabel())
        self.assertEqual(fig.axes[2].get_ylabel(), 'Residuo |f(x)|')
        self.assertFalse(any('Tolerancia' in line.get_label() for line in fig.axes[2].lines))
        with self.assertRaisesRegex(ValueError, 'no es porcentual'):
            figura_newton(calc, comparacion_biseccion=Calculo(.5))


if __name__ == '__main__':
    unittest.main()
