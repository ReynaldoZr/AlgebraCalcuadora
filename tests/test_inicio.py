"""Comprueba navegación, conservación de sesiones y herramientas compactas.

Tema: inicio por unidades y menú plegable sin cálculos involuntarios.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
import unittest

from interfaz.biblioteca import Biblioteca
from interfaz.ventana import CalculadoraVentana
from tests import test_ventana as pruebas_ventana


class PruebasInicio(unittest.TestCase):
    """Usa una biblioteca en memoria y ventanas propias de las pruebas."""

    @classmethod
    def setUpClass(cls):
        """Exige el mismo soporte de Tk que las demás pruebas gráficas."""
        pruebas_ventana.PruebasVentana.setUpClass()

    def setUp(self):
        """Construye la sesión en Inicio sin abrir archivos personales."""
        self.raiz = tk.Tk()
        self.raiz.withdraw()
        self.app = CalculadoraVentana(self.raiz, Biblioteca())
        self.addCleanup(self.cerrar)

    def cerrar(self):
        """Procesa los avisos de estilo pendientes antes de destruir la sesión de prueba."""
        self.raiz.update_idletasks()
        self.app.cerrar()

    def test_inicio_no_calcula_y_todas_las_tarjetas_abren_su_tema(self):
        """El inicio no calcula ocultamente y las tarjetas conducen al tema rotulado."""
        self.assertTrue(self.app.navegacion.en_inicio)
        self.app._calcular_visible()
        self.assertIsNone(self.app.resultado)
        for nombre, boton in self.app.navegacion.tarjetas.items():
            boton.invoke()
            self.assertEqual(self.app.tema_seleccionado, nombre)
            self.assertFalse(self.app.navegacion.en_inicio)
            self.assertEqual(self.app.lateral.winfo_manager(), '')
            self.app.navegacion.mostrar_inicio()
        self.assertFalse(self.app.cuaderno.biblioteca.listar(True))

    def test_volver_al_inicio_pausa_y_conserva_matrices_y_sistemas(self):
        """Navegar conserva operación, entradas, resultados y todos los pasos."""
        self.app.mostrar_matrices()
        self.app.operacion.set('multiplicar')
        self.app.cargar_ejemplo()
        self.app.calcular()
        resultado = self.app.resultado
        self.app.alternar_recorrido()
        self.app.navegacion.mostrar_inicio()
        self.assertIsNone(self.app.reproductor.pendiente)
        panel = self.app.abrir_tema('Sistemas')
        panel.seleccionar('jordan')
        panel.cargar_ejemplo()
        panel.calcular()
        presentacion = panel.presentacion
        self.app.navegacion.mostrar_inicio()
        self.app.mostrar_matrices()
        self.assertIs(self.app.resultado, resultado)
        self.assertEqual(self.app.selector_operacion.get(), 'Producto · AB')
        self.assertIs(self.app.abrir_tema('Sistemas').presentacion, presentacion)
        self.assertEqual(panel.clave, 'jordan')

    def test_biblioteca_y_menu_no_borran_la_sesion(self):
        """Biblioteca funciona desde Inicio; cerrar el menú mantiene los datos."""
        self.app.mostrar_biblioteca()
        self.assertEqual(self.app.pestanas.select(), str(self.app.cuaderno.vista))
        self.app._calcular_visible()
        self.assertFalse(self.app.cuaderno.biblioteca.listar(True))
        self.app.navegacion.alternar_menu()
        self.assertEqual(self.app.lateral.winfo_manager(), 'place')
        self.app.navegacion.elegir('Matrices')
        self.assertEqual(self.app.lateral.winfo_manager(), '')
        self.assertTrue(all(celda.get() == '' for fila in self.app.editor_a.celdas for celda in fila))
        self.assertEqual(self.app.pestanas.tab(self.app.cuaderno.vista, 'state'), 'hidden')

    def test_tamano_oculto_se_aplica_solo_al_confirmar(self):
        """Cambiar abre dimensiones; Aplicar conserva datos y actualiza el resumen."""
        self.app.mostrar_matrices()
        editor = self.app.editor_a
        editor.cargar([[1, 2], [3, 4]])
        self.assertEqual(editor.barra_dimensiones.winfo_manager(), '')
        editor.alternar_dimensiones()
        editor.filas.set('3')
        self.assertEqual(len(editor.celdas), 2)
        editor.aplicar_tamano()
        self.assertEqual(editor.leer(), [[1, 2], [3, 4], [0, 0]])
        self.assertEqual(editor.tamano.cget('text'), '3 × 2 · Cambiar')
        self.assertEqual(editor.barra_dimensiones.winfo_manager(), '')

    def test_menu_resultado_respeta_estado_y_reutiliza_sin_perder_resultado(self):
        """Las acciones ocultas conservan las validaciones de los botones anteriores."""
        self.app.mostrar_matrices()
        self.assertTrue(self.app.usar_a.instate(['disabled']))
        self.app.cargar_ejemplo()
        self.app.calcular()
        resultado = self.app.resultado
        self.app.usar_a.invoke()
        self.assertEqual(self.app.editor_a.leer(), resultado)
        self.assertIs(self.app.resultado, resultado)

    def test_formularios_vacios_hasta_cargar_ejemplo(self):
        """Los temas no rellenan un ejercicio; cargar y limpiar son decisiones explícitas."""
        self.app.mostrar_matrices()
        self.assertEqual(self.app.escalar.get(), '')
        for nombre in ('Sistemas', 'Vectores', 'Determinantes', 'Inversas', 'LU', 'Propiedades'):
            panel = self.app.abrir_tema(nombre)
            for clave in panel.claves:
                panel.seleccionar(clave)
                self.assertTrue(all(c.get() == '' for e in panel.editores.values() for f in e.celdas for c in f))
            self.assertEqual(panel.escalar.get(), '')
        numerico = self.app.abrir_tema('Numéricos')
        from interfaz.metodos_numericos import METODOS_NUMERICOS
        for clave in METODOS_NUMERICOS:
            numerico.seleccionar(clave)
            self.assertEqual(numerico.parametros['funcion'].get(), '')
            self.assertEqual(numerico.parametros['x'].get(), '')
        numerico.seleccionar('num_biseccion')
        numerico.cargar_ejemplo()
        self.assertTrue(numerico.parametros['funcion'].get())
        numerico.limpiar()
        self.assertEqual(numerico.parametros['funcion'].get(), '')
        self.assertEqual(numerico.parametros['a'].get(), '')
        self.assertEqual(numerico.parametros['tolerancia'].get(), '0.0001')

    def test_ritmo_fijo_dos_segundos_en_todos_los_paneles(self):
        """Matrices, álgebra y numéricos comparten un ritmo fijo de dos segundos."""
        self.assertEqual(self.app.reproductor.demora(), 2000)
        self.assertEqual(self.app.abrir_tema('Sistemas').reproductor.demora(), 2000)
        self.assertEqual(self.app.abrir_tema('Numéricos').reproductor.demora(), 2000)
