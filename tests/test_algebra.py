"""Comprueba resultados conocidos, límites y conservación del álgebra exacta.

Tema: tareas 1 a 6; sistemas, vectores, determinantes, inversas, LU y propiedades.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy
from fractions import Fraction as F
import random
import unittest

from modulos.eliminacion import reducir
from modulos.modulo_determinantes import calcular_determinante, determinante_cofactores, determinante_reduccion, determinante_sarrus
from modulos.modulo_lu import factorizar_lu, resolver_lu
from modulos.modulo_matrices import calcular_inversa, identidad, inversa_adjunta, inversa_gauss_jordan, producto_matricial
from modulos.modulo_sistemas import resolver_sistema
from modulos.modulo_vectores import combinacion_lineal, escalar_vector, independencia_lineal, restar_vectores, sumar_vectores
from teoremas.verificadores import PROPIEDADES, verificar_propiedad, verificar_todas


class PruebasAlgebra(unittest.TestCase):
    """Valida soluciones exactas y contratos de datos independientes de la interfaz."""

    def test_sistemas_unica_intercambio_y_fracciones(self):
        """Ambos métodos intercambian pivote cero y comprueban el sistema original."""
        for metodo in ('gauss', 'jordan'):
            calculo = resolver_sistema([[0, 2], [3, 1]], [1, 2], metodo)
            self.assertEqual(calculo.valor, [F(1, 2), F(1, 2)])
            self.assertEqual(calculo.datos['clasificacion'], 'unica')
            self.assertTrue(calculo.datos['verificado'])
            self.assertEqual(calculo.datos['pivotes'], (0, 1))
            self.assertTrue(any('↔' in p.titulo for p in calculo.pasos))

    def test_sistemas_infinitas_parametros_y_columnas_sin_pivote(self):
        """La solución general resuelve Ax=b para cualquier combinación de parámetros."""
        for metodo in ('gauss', 'jordan'):
            a, b = [[0, 1, 2, 0], [0, 2, 4, 0]], [3, 6]
            calculo = resolver_sistema(a, b, metodo)
            self.assertEqual(calculo.datos['clasificacion'], 'infinitas')
            self.assertEqual(calculo.datos['pivotes'], (1,))
            self.assertEqual(calculo.datos['libres'], (0, 2, 3))
            self.assertEqual(calculo.valor, [0, 3, 0, 0])
            self.assertTrue(calculo.datos['verificado'])
            for coeficientes in ([2, -3, 4], [F(1, 2), 0, -1]):
                vector = [v + sum(t * base[j] for t, base in zip(coeficientes, calculo.datos['base'])) for j, v in enumerate(calculo.valor)]
                self.assertEqual(producto_matricial(a, [[v] for v in vector]), [[3], [6]])

    def test_inconsistente_y_sistema_nulo(self):
        """Una contradicción no genera soluciones y la matriz cero libera todas las variables."""
        for metodo in ('gauss', 'jordan'):
            inconsistente = resolver_sistema([[1, 1], [2, 2]], [1, 3], metodo)
            self.assertIsNone(inconsistente.valor)
            self.assertEqual(inconsistente.datos['clasificacion'], 'sin_solucion')
            cero = resolver_sistema([[0, 0, 0]], [0], metodo)
            self.assertEqual(cero.datos['libres'], (0, 1, 2))
            self.assertEqual(cero.datos['base'], identidad(3))
            self.assertTrue(cero.datos['verificado'])

    def test_sistema_sobredeterminado_y_errores(self):
        """Admite más ecuaciones que incógnitas y rechaza b incompatible o valores inexactos."""
        calculo = resolver_sistema([[1], [2], [3]], [2, 4, 6])
        self.assertEqual(calculo.valor, [2])
        for a, b in (([[1, 2]], [1, 2]), ([[1.0]], [1]), ([[True]], [1]), ([[1]], [False])):
            with self.assertRaises(ValueError):
                resolver_sistema(a, b)

    def test_rref_identidad_y_copias(self):
        """La reducción no comparte filas con las entradas ni entre instantáneas."""
        a = [[1, 2, 3], [2, 4, 6]]
        original = deepcopy(a)
        reduccion = reducir(a, True)
        self.assertEqual(reduccion.matriz, [[1, 2, 3], [0, 0, 0]])
        reduccion.matriz[0][0] = 9
        self.assertEqual(a, original)
        self.assertEqual(reduccion.pasos[0].matriz, original)

    def test_vectores_operaciones_y_dimension(self):
        """Las operaciones de vectores reutilizan matrices y preservan entradas."""
        u, v = [F(1, 2), -2], [F(1, 3), 4]
        self.assertEqual(sumar_vectores(u, v), [F(5, 6), 2])
        self.assertEqual(restar_vectores(u, v), [F(1, 6), -6])
        self.assertEqual(escalar_vector(u, F(-3, 2)), [F(-3, 4), 3])
        self.assertEqual(u, [F(1, 2), -2])
        with self.assertRaises(ValueError):
            sumar_vectores(u, [1])
        with self.assertRaises(ValueError):
            escalar_vector(u, False)

    def test_combinacion_pertenencia_y_no_pertenencia(self):
        """Obtiene coeficientes y distingue un objetivo fuera del espacio generado."""
        vectores = [[1, 0, 1], [0, 1, 1]]
        calculo = combinacion_lineal(vectores, [2, 3, 5])
        self.assertTrue(calculo.datos['pertenece'])
        self.assertEqual(calculo.valor, [2, 3])
        self.assertFalse(combinacion_lineal(vectores, [2, 3, 6]).datos['pertenece'])

    def test_independencia_y_relacion_no_trivial(self):
        """L.D. ofrece un testigo no nulo que satisface Ac=0, incluso k>n."""
        self.assertTrue(independencia_lineal([[1, 0], [0, 1]]).valor)
        for vectores in ([[1, 2], [2, 4]], [[0, 0]], [[1], [2], [3]]):
            calculo = independencia_lineal(vectores)
            self.assertFalse(calculo.valor)
            relacion = calculo.datos['relacion']
            self.assertTrue(any(relacion))
            self.assertEqual([sum(c * v[j] for c, v in zip(relacion, vectores)) for j in range(len(vectores[0]))], [0] * len(vectores[0]))

    def test_determinantes_conocidos_y_todos_los_metodos(self):
        """Los tres métodos coinciden con el ejemplo del profesor y los intercambios."""
        a = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
        for metodo in ('cofactores', 'reduccion', 'sarrus'):
            self.assertEqual(calcular_determinante(a, metodo).valor, 1)
        self.assertEqual(determinante_cofactores([[7]]), 7)
        self.assertEqual(determinante_reduccion([[0, 2], [3, 1]]), -6)
        self.assertEqual(determinante_reduccion([[0, 1], [0, 2]]), 0)
        with self.assertRaises(ValueError):
            determinante_sarrus([[1]])
        with self.assertRaises(ValueError):
            determinante_cofactores([[1, 2]])

    def test_determinantes_fraccionarios_y_muestras_independientes(self):
        """Cofactores y reducción coinciden en matrices pequeñas con ceros y signos."""
        azar = random.Random(47)
        for orden in range(1, 5):
            for _ in range(12):
                a = [[F(azar.randint(-4, 4), azar.randint(1, 3)) for _ in range(orden)] for _ in range(orden)]
                self.assertEqual(determinante_reduccion(a), determinante_cofactores(a))
                if orden == 3:
                    self.assertEqual(determinante_sarrus(a), determinante_cofactores(a))

    def test_inversas_ejemplo_profesor_uno_por_uno_y_singular(self):
        """Ambos métodos coinciden, también en orden 1, y rechazan singularidad."""
        a, esperado = [[1, 2], [3, 4]], [[-2, 1], [F(3, 2), F(-1, 2)]]
        for metodo in ('jordan', 'adjunta'):
            calculo = calcular_inversa(a, metodo)
            self.assertEqual(calculo.valor, esperado)
            self.assertTrue(calculo.datos['verificado'])
            self.assertEqual(calcular_inversa([[F(2, 3)]], metodo).valor, [[F(3, 2)]])
            with self.assertRaisesRegex(ValueError, 'singular'):
                calcular_inversa([[1, 2, 3], [4, 5, 6], [7, 8, 9]], metodo)
        self.assertEqual(inversa_gauss_jordan([[0, 1], [1, 2]]), [[-2, 1], [1, 0]])
        self.assertEqual(inversa_adjunta(a), esperado)

    def test_lu_rectangular_saltos_y_singular_sin_permutar(self):
        """L es m×m, U es m×n y LU=A, incluso con columnas iniciales nulas."""
        for a in ([[2, 1, 1], [4, -6, 0], [-2, 7, 2]], [[1, 2], [3, 4], [5, 6]],
                  [[1, 2, 3], [2, 4, 6]], [[0, 1, 2], [0, 3, 4]], [[0], [0]]):
            original = deepcopy(a)
            calculo = factorizar_lu(a)
            l, u = calculo.valor
            self.assertEqual((len(l), len(l[0])), (len(a), len(a)))
            self.assertEqual(producto_matricial(l, u), a)
            self.assertTrue(calculo.datos['verificado'])
            self.assertEqual(a, original)
        with self.assertRaisesRegex(ValueError, 'PA = LU'):
            factorizar_lu([[0, 1], [1, 0]])
        with self.assertRaisesRegex(ValueError, 'PA = LU'):
            factorizar_lu([[1, 1, 0], [1, 1, 1], [0, 1, 1]])

    def test_lu_solucion_encadena_y_y_x(self):
        """La doble sustitución produce la solución conocida y comprueba Ax=b."""
        a = [[2, 1, 1], [4, -6, 0], [-2, 7, 2]]
        calculo = resolver_lu(a, [5, -2, 9])
        self.assertEqual(calculo.valor, [1, 1, 2])
        self.assertEqual(calculo.datos['y'], [5, -12, 2])
        self.assertTrue(calculo.datos['verificado'])
        with self.assertRaisesRegex(ValueError, 'singular'):
            resolver_lu([[1, 2], [2, 4]], [1, 2])
        with self.assertRaisesRegex(ValueError, 'cuadrada'):
            resolver_lu([[1, 2]], [3])

    def test_verificadores_ambos_miembros_y_no_aplicable(self):
        """Las propiedades calculan sus dos lados y singularidad no equivale a éxito."""
        a, b, c = [[1, 2], [3, 4]], [[0, 1], [1, 1]], identidad(2)
        copia = deepcopy((a, b, c))
        resultados = verificar_todas(a, b, c, 3)
        self.assertEqual(len(resultados), len(PROPIEDADES))
        for resultado in resultados:
            if resultado.cumple is not None:
                self.assertTrue(resultado.cumple, resultado.propiedad)
                self.assertEqual(resultado.izquierda, resultado.derecha)
            else:
                self.assertTrue(resultado.motivo)
        self.assertEqual((a, b, c), copia)
        self.assertIsNone(verificar_propiedad('inversa_identidad', [[1, 2], [2, 4]]).cumple)
        self.assertIsNone(verificar_propiedad('transpuesta_suma', [[1, 2]], [[1]]).cumple)
        self.assertTrue(verificar_propiedad('det_triangular', [[2, 1], [0, 3]]).cumple)
        self.assertTrue(verificar_propiedad('metodo_sarrus', [[1, 2, 3], [0, 1, 4], [5, 6, 0]]).cumple)
