"""Prueba los nuevos temas con widgets reales de escritorio.

Tema: sesiones independientes, procedimiento completo e invalidación de pasos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import unittest

from tests import test_ventana as ventana_pruebas


class PruebasPanelAlgebra(unittest.TestCase):
    """Comprueba interacción y errores, reutilizando la preparación de Tk existente."""

    @classmethod
    def setUpClass(cls):
        """Exige la misma disponibilidad gráfica que las otras pruebas de interfaz."""
        ventana_pruebas.PruebasVentana.setUpClass()

    def setUp(self):
        """Crea una sesión y cancela todos sus temporizadores al terminar."""
        import tkinter as tk
        from interfaz.ventana import CalculadoraVentana
        self.raiz = tk.Tk()
        self.raiz.withdraw()
        from interfaz.biblioteca import Biblioteca
        self.app = CalculadoraVentana(self.raiz, Biblioteca())
        self.addCleanup(self.cerrar_sesion)

    def cerrar_sesion(self):
        """Procesa avisos de estilos y cancela temporizadores antes de destruir Tk."""
        self.raiz.update_idletasks()
        self.app.cerrar()

    def test_temas_ejemplos_y_sesiones_independientes(self):
        """Los seis temas calculan y volver conserva cada sesión y las matrices básicas."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        basico = self.app.resultado
        for tema in ('Sistemas', 'Vectores', 'Determinantes', 'Inversas', 'LU', 'Propiedades'):
            panel = self.app.abrir_tema(tema)
            panel.cargar_ejemplo()
            panel.calcular()
            self.assertTrue(panel.vigente, panel.estado.get())
            self.assertIsNotNone(panel.presentacion)
            panel.reproductor.siguiente()
            self.assertIn('1/', panel.titulo_paso.cget('text'))
        self.assertEqual(self.app.resultado, basico)
        sistema = self.app.abrir_tema('Sistemas')
        self.assertEqual(sistema.presentacion.calculo.valor, [2, 1])
        self.assertEqual(len(self.app.paneles_algebra), 6)

    def test_limpiar_deshacer_y_metodo_no_cambian_seleccion(self):
        """La resta de vectores conserva el método al limpiar y deshacer."""
        panel = self.app.abrir_tema('Vectores')
        panel.seleccionar('v_resta')
        panel.cargar_ejemplo()
        panel.calcular()
        panel.limpiar()
        self.assertEqual(panel.clave, 'v_resta')
        self.assertIsNone(panel.presentacion)
        panel.deshacer()
        self.assertEqual(panel.clave, 'v_resta')
        self.assertEqual(panel.presentacion.calculo.valor, [-2, 3, 1])
        self.assertTrue(panel.vigente)
        panel.seleccionar('v_escalar')
        panel.deshacer()
        self.assertEqual(panel.clave, 'v_escalar')
        self.assertFalse(panel.vigente)
        self.assertFalse(panel.reproductor.pasos)

    def test_todos_los_pasos_usa_ancho_completo_y_conserva_formulas(self):
        """La vista amplia conserva cada fórmula y separa [A|I], también al cambiar colores."""
        from interfaz.notacion import Notacion
        panel = self.app.abrir_tema('Inversas')
        panel.cargar_ejemplo()
        panel.calcular()
        panel.vistas.select(panel.pagina_pasos)
        panel._cambiar_vista()
        self.assertEqual(panel.completa.pasos, panel.presentacion.calculo.pasos)
        visibles = [p for p in self.app.pestanas.tabs() if self.app.pestanas.tab(p, 'state') != 'hidden']
        self.assertEqual(visibles, [str(panel), str(panel.pagina_pasos)])
        self.assertEqual(self.app.pestanas.select(), str(panel.pagina_pasos))
        pendientes = [panel.completa.cuerpo]
        formulas, separadores = [], []
        while pendientes:
            widget = pendientes.pop(0)
            if isinstance(widget, Notacion):
                if widget.tokens:
                    formulas.append(widget.tokens)
                if widget.separador is not None:
                    separadores.append(widget.separador)
            pendientes[0:0] = widget.winfo_children()
        self.assertEqual(formulas, [list(f) for p in panel.completa.pasos for f in p.formulas])
        self.assertTrue(separadores)
        self.assertTrue(all(c == 2 for c in separadores))
        self.app.alternar_tema()
        self.assertTrue(panel.vigente)

    def test_singularidad_conserva_resultado_y_muestra_proceso_detenido(self):
        """Una inversa singular conserva entradas, cancela el reloj y deja revisar los pasos."""
        panel = self.app.abrir_tema('Inversas')
        panel.cargar_ejemplo()
        panel.calcular()
        anterior = panel.presentacion
        panel.alternar_recorrido()
        panel.editores['A'].cargar([[1, 2], [2, 4]])
        panel.marcar_cambio()
        panel.calcular()
        self.assertIs(panel.presentacion, anterior)
        self.assertFalse(panel.vigente)
        self.assertIsNone(panel.reproductor.pendiente)
        self.assertIn('singular', panel.estado.get())
        panel.vistas.select(panel.pagina_pasos)
        panel._cambiar_vista()
        self.assertEqual(panel.completa.pasos, panel.pasos_fallo)
        self.assertIn('detenido', panel.completa.aviso.cget('text'))

    def test_atajo_y_reutilizacion_se_dirigen_al_tema_visible(self):
        """Ctrl+Enter calcula el tema visible y reutilizar copia resultados sin compartir filas."""
        panel = self.app.abrir_tema('Sistemas')
        panel.cargar_ejemplo()
        self.app._calcular_visible()
        self.assertEqual(panel.presentacion.calculo.valor, [2, 1])
        self.assertIsNone(self.app.resultado)
        panel.reutilizar()
        self.assertEqual(panel.editores['A'].leer(), [[2], [1]])
        self.assertEqual(panel.presentacion.matriz, [[2], [1]])
        self.assertFalse(panel.vigente)

    def test_distribucion_original_y_controles_en_tamano_minimo(self):
        """Cada tema mantiene tres tarjetas, dos vistas y botones dentro de la ventana."""
        self.raiz.geometry('1120x760')
        self.raiz.deiconify()
        for tema in ('Sistemas', 'Vectores', 'Determinantes', 'Inversas', 'LU', 'Propiedades'):
            with self.subTest(tema=tema):
                panel = self.app.abrir_tema(tema)
                panel.cargar_ejemplo()
                panel.calcular()
                self.raiz.update()
                for boton in (panel.anterior, panel.reproducir, panel.siguiente, panel.reiniciar, panel.menu_resultado):
                    self.assertTrue(boton.winfo_ismapped())
                    self.assertLessEqual(boton.winfo_rooty() + boton.winfo_height(), self.raiz.winfo_rooty() + self.raiz.winfo_height())
                    self.assertLessEqual(boton.winfo_rootx() + boton.winfo_width(), self.raiz.winfo_rootx() + self.raiz.winfo_width())
                self.assertEqual(panel.editores['A'].grid_info()['column'], 0)
                self.assertEqual(panel.vista_matriz.master.master.grid_info()['column'], 2)
                self.assertEqual(sum(self.app.pestanas.tab(p, 'state') != 'hidden' for p in self.app.pestanas.tabs()), 2)
        self.app.mostrar_matrices()
        self.raiz.update()
        self.assertEqual(self.app.pestanas.select(), str(self.app.contenido))
