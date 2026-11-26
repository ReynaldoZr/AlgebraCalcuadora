"""Comprueba Newton propio, fallos numéricos e integración con adaptadores reales.

Tema: issue 33, casos de la Sesión 22 y límites de punto flotante.
Equipo responsable: Grupo 9.
"""

import math
import unittest
from unittest.mock import patch

from modulos.numericos.funciones import crear_funcion
from modulos.numericos.newton import COLUMNAS_NEWTON, contrastar_newton, resolver_newton


class PruebasNewton(unittest.TestCase):
    """Valida resultados y causas de parada, sin depender del solver de referencia."""

    def test_ejemplos_de_clase_y_primer_paso(self):
        """Las raíces conocidas y el primer avance coinciden con la fórmula de Newton."""
        casos = (
            ('exp(-x)-x', '-exp(-x)-1', 0, 0.5671432904097838, 4, 0.5),
            ('x^3-2*x-5', '3*x^2-2', 2, 2.0945514815423265, 3, 2.1),
        )
        for expr, deriv, x0, raiz, cantidad, primero in casos:
            with self.subTest(funcion=expr):
                f = crear_funcion(expr)
                calc = resolver_newton(f, crear_funcion(deriv), x0)
                self.assertTrue(calc.datos['convergio'], calc.datos['motivo'])
                self.assertAlmostEqual(calc.valor, raiz, places=8)
                self.assertEqual(calc.datos['iteraciones'], cantidad)
                self.assertEqual(calc.datos['registros'][0]['x_siguiente'], primero)
                self.assertEqual(calc.datos['residuo'], abs(f(calc.valor)))
                self.assertEqual(calc.datos['columnas'], COLUMNAS_NEWTON)
                self.assertEqual(calc.datos['filas'][-1][4], calc.valor)

    def test_polinomio_profesor_y_residuo_independiente(self):
        """La tolerancia adicional puede exigir más pasos que la tabla de clase."""
        f = crear_funcion('x^5-4*x^4+5*x^3-6*x+4')
        df = crear_funcion('5*x^4-16*x^3+15*x^2-6')
        clase = resolver_newton(f, df, -1.25, tolerancia_f=1e-4)
        protegido = resolver_newton(f, df, -1.25)
        self.assertEqual(clase.datos['iteraciones'], 4)
        self.assertGreater(clase.datos['residuo'], 1e-8)
        self.assertTrue(protegido.datos['convergio'])
        self.assertLess(protegido.datos['residuo'], 1e-8)
        self.assertGreater(protegido.datos['iteraciones'], clase.datos['iteraciones'])

    def test_salto_grande_no_equivale_a_divergencia(self):
        """El salto 0.5→51.65 de la clase no se descarta por un umbral fijo."""
        calc = resolver_newton(lambda x: x ** 10 - 1, lambda x: 10 * x ** 9,
                              .5, tolerancia_f=1e-4)
        self.assertAlmostEqual(calc.datos['registros'][0]['x_siguiente'], 51.65)
        self.assertTrue(calc.datos['convergio'])
        self.assertAlmostEqual(calc.valor, 1, places=7)

    def test_ciclo_y_cambio_de_semilla(self):
        """Conserva el ciclo 0↔1 y la convergencia desde -2 con la misma función."""
        f, df = lambda x: x ** 3 - 2 * x + 2, lambda x: 3 * x ** 2 - 2
        ciclo = resolver_newton(f, df, 0)
        self.assertFalse(ciclo.datos['convergio'])
        self.assertEqual(ciclo.datos['iteraciones'], 2)
        self.assertIn('ciclo', ciclo.datos['motivo'])
        normal = resolver_newton(f, df, -2)
        self.assertTrue(normal.datos['convergio'])
        self.assertAlmostEqual(normal.valor, -1.7692923542386314, places=8)

    def test_raiz_inicial_no_evalua_derivada(self):
        """Un cero inicial termina antes de dividir por una derivada también nula."""
        def no_llamar(x):
            """Falla si se evalúa una derivada innecesaria."""
            raise AssertionError('No debe evaluar la derivada en una raíz inicial.')

        calc = resolver_newton(lambda x: x * x, no_llamar, 0)
        self.assertTrue(calc.datos['convergio'])
        self.assertEqual(calc.datos['filas'], ())
        self.assertEqual(calc.datos['residuo'], 0)

    def test_tolerancias_y_entradas_invalidas(self):
        """Rechaza entradas mal formadas antes de iniciar el algoritmo."""
        base = dict(funcion=lambda x: x, derivada=lambda x: 1, x0=1)
        cambios = (
            dict(funcion='x'), dict(derivada=None), dict(x0=True), dict(x0=math.inf),
            dict(tolerancia=0), dict(tolerancia=-1), dict(tolerancia=math.nan),
            dict(tolerancia_f=0), dict(tolerancia_f=-1), dict(tolerancia_f=math.inf),
            dict(max_iteraciones=True), dict(max_iteraciones=1.5),
            dict(max_iteraciones=0), dict(max_iteraciones=10001), dict(criterio='intervalo'),
        )
        for cambio in cambios:
            with self.subTest(cambio=cambio), self.assertRaises(ValueError):
                resolver_newton(**dict(base, **cambio))

    def test_derivada_nula_y_pequena_con_escala(self):
        """No divide por cero ni rechaza una función escalada cuya corrección sí es válida."""
        fallo = resolver_newton(lambda x: x * x + 1, lambda x: 2 * x, 0)
        self.assertFalse(fallo.datos['convergio'])
        self.assertIn('derivada es cero', fallo.datos['motivo'])
        pequeno = resolver_newton(lambda x: 1e-200 * (x - 1), lambda x: 1e-200, 0)
        self.assertTrue(pequeno.datos['convergio'])
        self.assertEqual(pequeno.valor, 1)
        cociente = resolver_newton(lambda x: 1, lambda x: 1e-320, 0)
        self.assertFalse(cociente.datos['convergio'])
        self.assertIn('Cociente', cociente.datos['motivo'])

    def test_estancamiento_no_es_convergencia(self):
        """Un cambio redondeado a cero no oculta un residuo grande."""
        calc = resolver_newton(lambda x: 1e20 * (x - 1) + 1, lambda x: 1e20, 1)
        self.assertFalse(calc.datos['convergio'])
        self.assertEqual(calc.datos['residuo'], 1)
        self.assertEqual(calc.datos['filas'][0][5], 0)
        self.assertIn('Estancamiento', calc.datos['motivo'])
        subdesbordado = resolver_newton(lambda x: 1e-300, lambda x: 1e300, 1)
        self.assertFalse(subdesbordado.datos['convergio'])
        self.assertIn('Estancamiento', subdesbordado.datos['motivo'])

    def test_porcentaje_cero_e_inequidad_estricta(self):
        """No inventa un porcentaje en cero y respeta error < tolerancia."""
        cero = resolver_newton(lambda x: x, lambda x: 1, 1, criterio='porcentual')
        self.assertTrue(cero.datos['convergio'])
        self.assertIsNone(cero.datos['filas'][0][6])
        frontera = resolver_newton(lambda x: x * x + 1, lambda x: 2 * x, 1,
                                   tolerancia=1, tolerancia_f=10, max_iteraciones=1)
        self.assertFalse(frontera.datos['convergio'])
        self.assertEqual(frontera.datos['filas'][0][5], 1)

    def test_fallos_de_dominio_y_no_finitos_conservan_historial(self):
        """Un intento inválido no reemplaza el último punto que sí pudo evaluarse."""
        inicial = resolver_newton(math.log, lambda x: 1 / x, -1)
        self.assertFalse(inicial.datos['convergio'])
        self.assertIsNone(inicial.datos['residuo'])
        self.assertIsNone(inicial.valor)
        self.assertEqual(inicial.datos['iteraciones'], 0)
        f = lambda x: x ** 3 - 2 * x - 5
        df = lambda x: 10 if x == 2 else math.nan
        fallo = resolver_newton(f, df, 2)
        self.assertEqual(fallo.datos['iteraciones'], 1)
        self.assertEqual(fallo.valor, 2.1)
        self.assertEqual(fallo.datos['residuo'], abs(f(2.1)))
        self.assertIn('iteración 2', fallo.datos['motivo'])
        siguiente = resolver_newton(math.log, lambda x: -1, .5)
        self.assertFalse(siguiente.datos['convergio'])
        self.assertEqual(siguiente.valor, .5)

    def test_maximo_y_porcentaje_sin_mezclar_unidades(self):
        """El límite conserva tabla completa y el porcentaje multiplica por cien."""
        f = lambda x: math.exp(-x) - x
        df = lambda x: -math.exp(-x) - 1
        calc = resolver_newton(f, df, 0, max_iteraciones=1, criterio='porcentual')
        self.assertFalse(calc.datos['convergio'])
        self.assertEqual(calc.datos['filas'][0][6], 100)
        self.assertEqual(calc.datos['iteraciones'], 1)
        self.assertIn('Máximo', calc.datos['motivo'])

    def test_contraste_scipy_opcional_no_reemplaza_resultado(self):
        """SciPy contrasta por separado y un fallo de referencia no borra el cálculo."""
        f = lambda x: math.cos(x) - x
        df = lambda x: -math.sin(x) - 1
        calc = resolver_newton(f, df, 1)
        copia = dict(calc.datos)
        ref = contrastar_newton(calc, f, df)
        self.assertTrue(ref.datos['scipy_convergio'])
        self.assertLess(ref.datos['diferencia_scipy'], 1e-8)
        self.assertEqual(ref.valor, calc.valor)
        self.assertEqual(calc.datos, copia)
        with patch('scipy.optimize.newton', side_effect=RuntimeError('Sin referencia')):
            fallo = contrastar_newton(calc, f, df)
        self.assertIsNone(fallo.datos['scipy'])
        self.assertEqual(fallo.valor, calc.valor)

    def test_adaptadores_reales_consumen_nucleo(self):
        """La preparación de Roberto acepta el contrato real sin cambiar la interfaz."""
        from interfaz.numericos.newton_adaptador import ejemplo_newton, ejecutar_newton_adaptador
        from interfaz.numericos.newton_graficas import figura_newton
        from interfaz.numericos.newton_presentacion import tabla_newton
        parametros = ejemplo_newton()
        calc = ejecutar_newton_adaptador(parametros)
        self.assertTrue(calc.datos['convergio'])
        self.assertEqual(len(tabla_newton(calc)['filas']), calc.datos['iteraciones'])
        fig = figura_newton(calc, crear_funcion(parametros['funcion']))
        self.assertEqual(len(fig.axes), 3)


if __name__ == '__main__':
    unittest.main()
