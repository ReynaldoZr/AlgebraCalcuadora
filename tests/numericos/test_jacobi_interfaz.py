"""Verifica el acceso a Jacobi y sus resultados en la presentación local.

Tema: issue #16, entradas, sesiones, tabla, gráfica y biblioteca.
Equipo responsable: Grupo 9.
"""

import unittest

from interfaz.qt.sesion import Sesion


class PruebasInterfazJacobi(unittest.TestCase):
    """Comprueba contratos visibles con datos conocidos, sin controlar la pantalla."""

    @classmethod
    def setUpClass(cls):
        """Respeta el contrato de bibliotecas opcionales de la unidad numérica."""
        from tests.numericos.test_semana12 import PruebasSemana12
        PruebasSemana12.setUpClass()

    def test_formulario_inicial_vacio_y_ejemplo_explicito(self):
        """Abrir Jacobi deja al usuario elegir los datos y cargar el ejemplo después."""
        s = Sesion('num_jacobi')
        self.assertEqual(s.parametros['vector_b'], '')
        self.assertEqual(s.parametros['inicial'], '')
        self.assertTrue(all(v == '' for f in s.entradas['A'] for v in f))
        s.cargar_ejemplo()
        s.calcular()
        self.assertEqual(len(s.presentacion.calculo.datos['filas']), 11)
        self.assertIn('Residuo', s.presentacion.resumen)
        self.assertIn('Referencia NumPy', s.presentacion.resumen)
        self.assertLess(s.presentacion.calculo.datos['diferencia_referencia'], 0.0001)
        s.limpiar()
        self.assertEqual(s.clave, 'num_jacobi')
        s.deshacer()
        self.assertTrue(s.vigente)

    def test_tabla_completa_y_grafica_del_error(self):
        """Todas las iteraciones se exponen a QML y a la curva de error."""
        from interfaz.qt.presentacion import tabla_visual
        from interfaz.numericos.figuras import figura_numerica
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        s = Sesion('num_jacobi')
        s.cargar_ejemplo()
        s.calcular()
        c = s.presentacion.calculo
        self.assertEqual(len(tabla_visual(c)['filas']), 11)
        fig = figura_numerica('num_jacobi', c)
        self.assertEqual(list(fig.axes[0].lines[0].get_xdata()), list(range(1, 12)))
        self.assertEqual(list(fig.axes[0].lines[0].get_ydata()), [f[-1] for f in c.datos['filas']])
        FigureCanvasAgg(fig).draw()

    def test_guardar_y_recuperar_ejercicio(self):
        """La biblioteca conserva A, b, X₀ y parámetros para recuperar el cálculo."""
        from interfaz.biblioteca import Biblioteca, validar_registro
        s = Sesion('num_jacobi')
        s.cargar_ejemplo()
        s.calcular()
        registro = s.registro()
        validar_registro(registro)
        biblioteca = Biblioteca()
        biblioteca.guardar(registro)
        guardado = biblioteca.listar()[0]
        nueva = Sesion('num_jacobi')
        nueva.entradas = guardado['entradas']
        nueva.parametros.update(guardado['parametros'])
        nueva.calcular()
        self.assertEqual(nueva.presentacion.calculo.valor, s.presentacion.calculo.valor)

    def test_no_convergencia_y_diagonal_invalida(self):
        """Los casos problemáticos muestran el límite o identifican el cero diagonal."""
        s = Sesion('num_jacobi')
        s.cargar_ejemplo('Sin convergencia')
        s.calcular()
        self.assertFalse(s.presentacion.calculo.datos['convergio'])
        self.assertEqual(len(s.presentacion.calculo.datos['filas']), 20)
        self.assertIn('máximo', s.presentacion.resumen)
        s.cargar_ejemplo('Diagonal con cero')
        s.calcular()
        self.assertTrue(s.presentacion.calculo.datos['reordenado'])
        s.parametros['reordenar'] = 'no'
        with self.assertRaisesRegex(ValueError, 'Reordena'):
            s.calcular()

    def test_vector_invalido_y_referencia_singular(self):
        """Valida vectores y conserva el cálculo aunque NumPy no pueda resolver el sistema."""
        from interfaz.metodos_numericos import leer_vector_numerico
        for texto in ('', '1,', 'uno, 2', '1/0, 2'):
            with self.subTest(texto=texto), self.assertRaises(ValueError):
                leer_vector_numerico(texto, 'b')
        s = Sesion('num_jacobi')
        s.entradas['A'] = [['1', '1'], ['1', '1']]
        s.parametros.update(vector_b='2, 2', inicial='1, 1')
        s.calcular()
        self.assertTrue(s.presentacion.calculo.datos['convergio'])
        self.assertIsNone(s.presentacion.calculo.datos['referencia'])
        self.assertIn('Singular', s.presentacion.resumen)


class PruebasInterfazComparacionIterativos(unittest.TestCase):
    """Comprueba Gauss-Seidel, reordenamiento y comparación en la interfaz."""

    @classmethod
    def setUpClass(cls):
        """Respeta el contrato de bibliotecas opcionales de la unidad numérica."""
        from tests.numericos.test_semana12 import PruebasSemana12
        PruebasSemana12.setUpClass()

    def test_comparador_tabla_completa_y_grafica_doble(self):
        """Conserva 11 filas de Jacobi y 7 de Gauss-Seidel y dibuja ambas curvas."""
        from interfaz.qt.presentacion import tabla_visual
        from interfaz.numericos.figuras import figura_numerica
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        s = Sesion('num_comparar_iterativos')
        s.cargar_ejemplo('Diagonal dominante')
        s.calcular()
        c = s.presentacion.calculo
        self.assertEqual(len(tabla_visual(c)['filas']), 18)
        self.assertIn('Gauss-Seidel necesitó menos iteraciones', s.presentacion.resumen)
        self.assertIn('Referencia NumPy', s.presentacion.resumen)
        fig = figura_numerica('num_comparar_iterativos', c)
        self.assertEqual(len(fig.axes[0].lines), 2)
        self.assertEqual(list(fig.axes[0].lines[0].get_xdata()), list(range(1, 12)))
        self.assertEqual(list(fig.axes[0].lines[1].get_xdata()), list(range(1, 8)))
        FigureCanvasAgg(fig).draw()

    def test_casos_reordenar_diagonal_cero_y_sin_convergencia(self):
        """Comprueba los tres casos obligatorios en Gauss-Seidel y comparador."""
        for clave in ('num_gauss_seidel', 'num_comparar_iterativos'):
            with self.subTest(clave=clave):
                s = Sesion(clave)
                s.cargar_ejemplo('Reordenar 2×2')
                s.calcular()
                self.assertTrue(s.presentacion.calculo.datos['reordenado'])
                self.assertIn('Reordenadas', s.presentacion.resumen)

                s.cargar_ejemplo('Diagonal con cero')
                s.calcular()
                self.assertTrue(s.presentacion.calculo.datos['convergio'])

                s.cargar_ejemplo('Sin convergencia')
                s.calcular()
                self.assertFalse(s.presentacion.calculo.datos['convergio'])

    def test_guardar_y_recuperar_comparador(self):
        """La biblioteca conserva los datos de Gauss-Seidel y del comparador."""
        from interfaz.biblioteca import Biblioteca, validar_registro
        for clave in ('num_gauss_seidel', 'num_comparar_iterativos'):
            with self.subTest(clave=clave):
                s = Sesion(clave)
                s.cargar_ejemplo()
                s.calcular()
                registro = s.registro()
                validar_registro(registro)
                bib = Biblioteca()
                bib.guardar(registro)
                guardado = bib.listar()[0]
                nueva = Sesion(clave)
                nueva.entradas = guardado['entradas']
                nueva.parametros.update(guardado['parametros'])
                nueva.calcular()
                self.assertEqual(nueva.presentacion.calculo.valor, s.presentacion.calculo.valor)

    def test_desbordamiento_muestra_el_motivo_de_ambos_metodos(self):
        """La tarjeta informa valores no finitos sin confundirlos con agotar el máximo."""
        s = Sesion('num_comparar_iterativos')
        s.entradas['A'] = [['1e-308', '1e308'], ['1', '1']]
        s.parametros.update(vector_b='1, 1', inicial='1, 1', reordenar='no')
        s.calcular()
        c = s.presentacion.calculo
        for metodo in ('jacobi', 'gauss_seidel'):
            self.assertEqual(c.datos[metodo]['filas'], [])
            self.assertEqual(c.datos[metodo]['inicial'], [1, 1])
        self.assertIn('Parada Jacobi: La iteración produjo valores no finitos',
                      s.presentacion.resumen)
        self.assertIn('Parada Gauss-Seidel: La iteración produjo valores no finitos',
                      s.presentacion.resumen)

    def test_jacobi_ofrece_reordenar_y_conserva_opcion_guardada(self):
        """Jacobi también permite corregir la diagonal desde el formulario y la biblioteca."""
        from interfaz.qt.catalogo import campos_de
        s = Sesion('num_jacobi')
        self.assertIn('reordenar', campos_de(s.clave, 1))
        s.cargar_ejemplo('Reordenar 2×2')
        s.calcular()
        self.assertTrue(s.presentacion.calculo.datos['reordenado'])
        self.assertEqual(len(s.presentacion.calculo.datos['filas']), 7)
        self.assertEqual(s.registro()['parametros']['reordenar'], 'si')
