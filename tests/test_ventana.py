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
        self.addCleanup(self.raiz.destroy)
        self.app = CalculadoraVentana(self.raiz)
        self.raiz.update_idletasks()

    def test_ejemplo_suma_exacta_y_procedimiento(self):
        """El ejemplo produce fracciones exactas y pasos coherentes."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.assertEqual(self.app.resultado, [[Fraction(1, 2), Fraction(3, 10)], [3, 3]])
        self.assertIn("R[1,1] = (1/3) + (1/6) = 1/2", self.app.texto_pasos.get("1.0", "end"))
        self.assertIn("1/2", self.app.texto_resultado.get("1.0", "end"))

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
