"""Comprueba recorridos reales de la ventana con los cálculos existentes.

Tema: resultados exactos, errores de entrada y conservación de datos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import os
import unittest
from fractions import Fraction
from unittest.mock import patch

try:
    import tkinter as tk
except ImportError:
    tk = None


class PruebasVentana(unittest.TestCase):
    """Ejercita widgets reales; en CI se exige una pantalla o Xvfb."""

    @classmethod
    def setUpClass(cls):
        """Comprueba que haya Tk y pantalla; CI no admite omitir estos casos."""
        try:
            if tk is None:
                raise RuntimeError("Tkinter no está disponible")
            raiz = tk.Tk()
            raiz.withdraw()
            raiz.destroy()
        except (RuntimeError, tk.TclError if tk else RuntimeError) as error:
            if os.environ.get("CALCULADORA_EXIGIR_GUI") == "1":
                raise RuntimeError("CI debe ejecutar las pruebas gráficas con Tk y pantalla") from error
            raise unittest.SkipTest("Se necesita Tk y una pantalla; en Linux usar xvfb-run.") from error

    def setUp(self):
        """Construye una sesión gráfica nueva sin interferir con la ventana del usuario."""
        from interfaz.ventana import CalculadoraVentana
        self.raiz = tk.Tk()
        self.raiz.withdraw()
        self.addCleanup(self.cerrar_sesion)
        self.app = CalculadoraVentana(self.raiz)
        self.addCleanup(self.app.reproductor.pausar)
        self.raiz.update_idletasks()

    def cerrar_sesion(self):
        """Procesa avisos de estilo pendientes antes de destruir el intérprete Tk."""
        self.raiz.update_idletasks()
        self.raiz.destroy()

    def test_ejemplo_suma_exacta_y_procedimiento(self):
        """El ejemplo produce fracciones exactas y pasos coherentes."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.assertEqual(self.app.resultado, [[Fraction(1, 2), Fraction(3, 10)], [3, 3]])
        self.assertEqual(self.app.desarrollo.pasos[0][2:5], (Fraction(1, 3), Fraction(1, 6), Fraction(1, 2)))
        self.assertEqual(len(self.app.desarrollo.pasos), 4)
        self.assertEqual(self.app.vista_resultado.matriz, self.app.resultado)
        self.assertEqual(self.app.formula_previa.tokens, [Fraction(1, 10), "+", Fraction(1, 5), "=", Fraction(3, 10)])

    def test_resta_rectangular(self):
        """La ventana resta matrices 1x3 con signos correctos."""
        self.app.editor_a.cargar([[1, -2, "1/2"]])
        self.app.editor_b.cargar([[5, 1, "1/4"]])
        self.app.operacion.set("restar")
        self.app.calcular()
        self.assertEqual(self.app.resultado, [[-4, -3, Fraction(1, 4)]])

    def test_celda_invalida_conserva_datos_y_resultado(self):
        """Una corrección fallida no borra el cálculo anterior ni los datos escritos."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        anterior = self.app.resultado
        celda = self.app.editor_a.celdas[0][1]
        for invalido in ("", "hola", "1/0", "nan", "inf"):
            with self.subTest(invalido=invalido):
                celda.delete(0, "end")
                celda.insert(0, invalido)
                self.app.calcular()
                self.assertIn("A[1,2]", self.app.estado.get())
                self.assertIs(self.app.resultado, anterior)
                self.assertEqual(celda.get(), invalido)
        celda.delete(0, "end")
        celda.insert(0, "0.1")
        self.app.calcular()
        self.assertIn("completado", self.app.estado.get())

    def test_dimensiones_incompatibles(self):
        """Las matrices incompatibles dejan un mensaje y no crean un resultado."""
        self.app.editor_a.cargar([[1, 2]])
        self.app.editor_b.cargar([[3], [4]])
        self.app.calcular()
        self.assertIsNone(self.app.resultado)
        self.assertIn("A es 1x2 y B es 2x1", self.app.estado.get())

    def test_reutilizacion_no_comparte_datos(self):
        """Reutilizar un resultado como entrada no permite cambiar la respuesta guardada."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.app.reutilizar("A")
        self.app.editor_a.celdas[0][0].delete(0, "end")
        self.app.editor_a.celdas[0][0].insert(0, "99")
        self.assertEqual(self.app.resultado[0][0], Fraction(1, 2))
        self.assertIn("datos modificados", self.app.etiqueta_resultado.cget("text"))

    def test_dimension_pendiente_no_se_ignora(self):
        """Cambiar un tamaño requiere aplicarlo antes de calcular."""
        self.app.editor_a.filas.set("3")
        self.app.calcular()
        self.assertIn("pulsa Aplicar", self.app.estado.get())
        self.assertEqual(len(self.app.editor_a.celdas), 2)

    def test_ampliar_conserva_datos(self):
        """Al ampliar una matriz se conservan datos y se añaden ceros."""
        self.app.editor_a.cargar([["1/3", "texto pendiente"]])
        self.app.editor_a.filas.set("3")
        self.app.editor_a.aplicar_tamano()
        self.assertEqual(self.app.editor_a.celdas[0][0].get(), "1/3")
        self.assertEqual(self.app.editor_a.celdas[0][1].get(), "texto pendiente")
        self.assertEqual(self.app.editor_a.celdas[2][1].get(), "0")

    def test_cancelar_reduccion_conserva_celdas(self):
        """Cancelar un recorte restaura dimensiones y conserva todas las celdas."""
        self.app.editor_a.filas.set("1")
        with patch("tkinter.messagebox.askyesno", return_value=False):
            self.app.editor_a.aplicar_tamano()
        self.assertEqual(self.app.editor_a.filas.get(), "2")
        self.assertEqual(len(self.app.editor_a.celdas), 2)

    def test_limite_grafico_y_dimension_invalida(self):
        """No construye una cuadrícula fuera de sus límites documentados."""
        for invalida in ("0", "-2", "11", "2.5", "abc"):
            with self.subTest(invalida=invalida):
                self.app.editor_a.filas.set(invalida)
                self.app.editor_a.aplicar_tamano()
                self.assertEqual(len(self.app.editor_a.celdas), 2)
        self.app.editor_a.filas.set("10")
        self.app.editor_a.columnas.set("10")
        self.app.editor_a.aplicar_tamano()
        self.assertEqual(len(self.app.editor_a.celdas), 10)
        self.assertEqual(len(self.app.editor_a.celdas[0]), 10)

    def test_limpiar_borra_memoria_de_sesion(self):
        """Limpiar restablece entradas y deshabilita reutilizar una respuesta vieja."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.app.limpiar()
        self.assertIsNone(self.app.resultado)
        self.assertEqual(self.app.editor_a.leer(), [[0, 0], [0, 0]])
        self.assertEqual(str(self.app.usar_a.cget("state")), "disabled")

    def test_pasos_revelan_resultado_sin_recalcular(self):
        """Un paso resalta operandos y revela una celda manteniendo la respuesta exacta."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.assertFalse(self.app.reproductor.activo)
        self.app.reproductor.siguiente()
        self.assertEqual(self.app.resultado, [[Fraction(1, 2), Fraction(3, 10)], [3, 3]])
        self.assertEqual(self.app.vista_resultado.matriz, [[Fraction(1, 2), "·"], ["·", "·"]])
        self.assertEqual(self.app.editor_a.celdas[0][0].cget("style"), "Activa.TEntry")
        self.assertIn("Paso 1 de 4", self.app.progreso.cget("text"))
        self.assertEqual(self.app.formula_previa.tokens, [Fraction(1, 3), "+", Fraction(1, 6), "=", Fraction(1, 2)])
        self.app.ver_todo()
        self.assertEqual(self.app.vista_resultado.matriz, self.app.resultado)
        self.assertEqual(self.app.pestanas.select(), str(self.app.pagina_pasos))
        self.assertEqual(self.app.desarrollo.pasos[-1][:2], (1, 1))

    def test_editar_detiene_animacion_y_descarta_pasos(self):
        """Editar mientras se reproduce cancela eventos y exige un cálculo nuevo."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.app.alternar_recorrido()
        self.assertIsNotNone(self.app.reproductor.pendiente)
        self.app.editor_a.celdas[0][0].delete(0, "end")
        self.assertIsNone(self.app.reproductor.pendiente)
        self.assertFalse(self.app.reproductor.pasos)
        self.assertEqual(self.app.vista_resultado.matriz, self.app.resultado)
        self.assertEqual(str(self.app.boton_reproducir.cget("state")), "disabled")

    def test_cargar_y_reutilizar_cancelan_sin_acceder_a_celdas_destruidas(self):
        """Reconstruir un editor con resultado previo no deja callbacks ni widgets obsoletos."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.app.alternar_recorrido()
        self.app.reutilizar("A")
        self.assertFalse(self.app.reproductor.pasos)
        self.assertEqual(self.app.editor_a.leer()[0][0], Fraction(1, 2))
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.app.operacion.set("restar")
        self.assertFalse(self.app.reproductor.pasos)

    def test_pestanas_y_tema_conservan_la_sesion(self):
        """Abrir el desarrollo y cambiar colores no cambia entradas ni resultados."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        entrada = self.app.editor_a.leer()
        resultado = self.app.resultado
        self.app.alternar_recorrido()
        self.assertEqual(self.app.reproductor.demora(), 3000)
        self.app.ver_todo()
        self.app._cambiar_pestana()
        self.assertFalse(self.app.reproductor.activo)
        self.assertEqual(int(self.app.lateral.cget("width")), 68)
        self.app.alternar_tema()
        self.app.alternar_tema()
        self.app.pestanas.select(self.app.contenido)
        self.app._cambiar_pestana()
        self.assertEqual(self.app.editor_a.leer(), entrada)
        self.assertIs(self.app.resultado, resultado)
        self.assertEqual(int(self.app.lateral.cget("width")), 200)

    def test_deshacer_limpieza_y_carga_como_acciones_completas(self):
        """Deshacer restaura el cálculo limpiado y revierte una carga de ejemplo."""
        self.app.cargar_ejemplo()
        self.app.deshacer()
        self.assertEqual(self.app.editor_a.leer(), [[0, 0], [0, 0]])
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.app.limpiar()
        self.app.deshacer()
        self.assertEqual(self.app.resultado, [[Fraction(1, 2), Fraction(3, 10)], [3, 3]])
        self.assertTrue(self.app.vigente)
        self.assertEqual(len(self.app.reproductor.pasos), 4)

    def test_deshacer_edicion_cancela_reloj_y_restaura_calculo(self):
        """Revertir una edición recupera el cálculo vigente sin reactivar movimiento."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.app.alternar_recorrido()
        self.app.editor_a.celdas[0][0].delete(0, "end")
        self.app.deshacer()
        self.assertEqual(self.app.editor_a.leer()[0][0], Fraction(1, 3))
        self.assertTrue(self.app.vigente)
        self.assertFalse(self.app.reproductor.activo)
        self.assertIsNone(self.app.reproductor.pendiente)

    def test_desarrollo_largo_y_resultado_anterior(self):
        """Construye todos los pasos de una matriz grande y avisa si quedan obsoletos."""
        self.app.editor_a.cargar([[1] * 10 for _ in range(10)])
        self.app.editor_b.cargar([[2] * 10 for _ in range(10)])
        self.app.calcular()
        self.assertEqual(len(self.app.desarrollo.pasos), 100)
        self.assertEqual(self.app.desarrollo.pasos[-1][4], 3)
        self.app.editor_a.celdas[9][9].delete(0, "end")
        self.assertIn("entradas cambiaron", self.app.desarrollo.aviso.cget("text"))
        self.assertFalse(self.app.reproductor.pasos)

    def test_equivalencias_de_fracciones_y_resta_negativa(self):
        """El desarrollo conserva equivalencias exactas y agrupa signos negativos."""
        from interfaz.desarrollo import detallar_paso
        tokens, _ = detallar_paso((0, 0, Fraction(1, 3), Fraction(1, 6), Fraction(1, 2), "+"))
        self.assertEqual(tokens, [Fraction(1, 3), "+", Fraction(1, 6), "=", (2, 6), "+", (1, 6), "=", (3, 6), "=", Fraction(1, 2)])
        tokens, _ = detallar_paso((0, 0, Fraction(1, 3), Fraction(-1, 6), Fraction(1, 2), "-"))
        self.assertEqual(tokens[-1], Fraction(1, 2))
        self.assertIn((-1, 6), tokens)
        self.assertEqual(tokens.count("("), tokens.count(")"))

    def test_controles_accesibles_en_tamano_minimo(self):
        """El tamaño mínimo deja a la vista controles de tamaño y navegación."""
        self.raiz.geometry("1120x760")
        self.raiz.deiconify()
        self.raiz.update()
        controles = [self.app.boton_todo, self.app.boton_reiniciar, self.app.progreso,
                     self.app.usar_a, self.app.usar_b]
        for editor in (self.app.editor_a, self.app.editor_b):
            controles.extend(hijo for marco in editor.winfo_children()
                             for hijo in marco.winfo_children() if hijo.winfo_class() == "TSpinbox")
        for control in controles:
            with self.subTest(control=str(control)):
                self.assertTrue(control.winfo_ismapped())
                self.assertLessEqual(control.winfo_rooty() + control.winfo_height(),
                                     control.master.winfo_rooty() + control.master.winfo_height())
                self.assertLessEqual(control.winfo_rootx() + control.winfo_width(),
                                     control.master.winfo_rootx() + control.master.winfo_width())
        self.raiz.withdraw()
