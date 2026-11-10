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
        from interfaz.biblioteca import Biblioteca
        self.app = CalculadoraVentana(self.raiz, Biblioteca())
        self.app.mostrar_matrices()
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
        self.assertTrue(all(celda.get() == '' for fila in self.app.editor_a.celdas for celda in fila))
        self.assertEqual(str(self.app.usar_a.cget("state")), "disabled")

    def test_pasos_revelan_resultado_sin_recalcular(self):
        """Un paso resalta operandos y revela una celda manteniendo la respuesta exacta."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.assertFalse(self.app.reproductor.activo)
        self.app.reproductor.siguiente()
        self.assertEqual(self.app.resultado, [[Fraction(1, 2), Fraction(3, 10)], [3, 3]])
        self.assertEqual(self.app.vista_resultado.matriz, [["·", "·"], ["·", "·"]])
        self.assertEqual(self.app.editor_a.celdas[0][0].cget("style"), "Activa.TEntry")
        self.assertIn("Paso 1 de 4", self.app.progreso.cget("text"))
        self.assertEqual(self.app.formula_previa.tokens, [Fraction(1, 3), "+", Fraction(1, 6)])
        self.assertIn("A[1,1]", self.app.resumen.cget("text"))
        while self.app.reproductor.secuencia[self.app.reproductor.indice].fase != "guardar":
            self.app.reproductor.siguiente()
        self.assertEqual(self.app.vista_resultado.matriz, [[Fraction(1, 2), "·"], ["·", "·"]])
        self.assertEqual(self.app.formula_previa.tokens, ["R[1,1]", "=", Fraction(1, 2)])
        self.app.reproductor.anterior()
        self.assertEqual(self.app.vista_resultado.matriz, [["·", "·"], ["·", "·"]])
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
        self.assertEqual(self.app.reproductor.demora(), 2000)
        self.app.ver_todo()
        self.app._cambiar_pestana()
        self.assertFalse(self.app.reproductor.activo)
        self.assertEqual(self.app.lateral.winfo_manager(), '')
        self.app.alternar_tema()
        self.app.alternar_tema()
        self.app.pestanas.select(self.app.contenido)
        self.app._cambiar_pestana()
        self.assertEqual(self.app.editor_a.leer(), entrada)
        self.assertIs(self.app.resultado, resultado)
        self.assertEqual(self.app.lateral.winfo_manager(), '')

    def test_deshacer_limpieza_y_carga_como_acciones_completas(self):
        """Deshacer restaura el cálculo limpiado y revierte una carga de ejemplo."""
        self.app.cargar_ejemplo()
        self.app.deshacer()
        self.assertTrue(all(celda.get() == '' for fila in self.app.editor_a.celdas for celda in fila))
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
        """El tamaño mínimo deja accesibles Cambiar y los menús compactos."""
        self.raiz.geometry("1120x760")
        self.raiz.deiconify()
        self.raiz.update()
        controles = [self.app.boton_todo, self.app.boton_reiniciar, self.app.progreso,
                     self.app.menu_resultado, self.app.editor_a.tamano, self.app.editor_b.tamano]
        for editor in (self.app.editor_a, self.app.editor_b):
            editor.alternar_dimensiones()
            controles.extend(hijo for marco in editor.winfo_children()
                             for hijo in marco.winfo_children() if hijo.winfo_class() == "TSpinbox")
        self.raiz.update()
        for control in controles:
            with self.subTest(control=str(control)):
                self.assertTrue(control.winfo_ismapped())
                self.assertLessEqual(control.winfo_rooty() + control.winfo_height(),
                                     control.master.winfo_rooty() + control.master.winfo_height())
                self.assertLessEqual(control.winfo_rootx() + control.winfo_width(),
                                     control.master.winfo_rootx() + control.master.winfo_width())
        self.app.operacion.set('escalar')
        self.raiz.update()
        entrada = self.app.entrada_escalar
        self.assertTrue(entrada.winfo_ismapped())
        self.assertFalse(self.app.editor_b.winfo_ismapped())
        self.assertLessEqual(entrada.winfo_rooty() + entrada.winfo_height(),
                             self.app.tarjeta_escalar.winfo_rooty() + self.app.tarjeta_escalar.winfo_height())
        self.app.operacion.set('transponer')
        self.raiz.update()
        self.assertTrue(self.app.tarjeta_transpuesta.winfo_ismapped())
        self.assertFalse(self.app.editor_b.winfo_ismapped())
        self.assertFalse(self.app.entrada_escalar.winfo_ismapped())
        self.app.operacion.set('multiplicar')
        self.raiz.update()
        self.assertTrue(self.app.editor_a.winfo_ismapped())
        self.assertTrue(self.app.editor_b.winfo_ismapped())
        self.assertFalse(self.app.usar_b.winfo_ismapped())
        self.assertTrue(self.app.menu_resultado.winfo_ismapped())
        self.raiz.withdraw()

    def test_escalar_ignora_b_y_recorre_matriz_rectangular(self):
        """kA usa solo A, aunque B tenga datos inválidos y otra forma."""
        self.app.editor_b.cargar([['no es un número']])
        self.app.editor_b.filas.set('10')
        self.app.editor_a.cargar([['1/3', -2, 0]])
        self.app.operacion.set('escalar')
        self.app.escalar.set('-3/2')
        self.app.calcular()
        self.assertEqual(self.app.resultado, [[Fraction(-1, 2), 3, 0]])
        self.assertEqual(self.app.editor_b.winfo_manager(), '')
        self.assertEqual(self.app.tarjeta_escalar.winfo_manager(), 'grid')
        self.assertEqual(self.app.formula_previa.tokens, [Fraction(-3, 2), '×', '(', -2, ')', '=', 3])
        for _ in self.app.reproductor.secuencia:
            self.app.reproductor.siguiente()
        self.assertEqual(self.app.vista_resultado.matriz, self.app.resultado)
        self.assertEqual(len(self.app.desarrollo.pasos), 3)
        self.assertIn('k = -3/2', self.app.desarrollo.aviso.cget('text'))
        self.assertNotIn('A y B', self.app.resumen.cget('text'))

    def test_escalar_invalido_conserva_ultimo_calculo(self):
        """Errores de k son recuperables y no sustituyen una respuesta válida."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        anterior = self.app.resultado
        self.app.operacion.set('escalar')
        for invalido in ('', 'hola', '1/0', 'nan', 'inf'):
            with self.subTest(k=invalido):
                self.app.escalar.set(invalido)
                self.app.calcular()
                self.assertIn('Revisa el escalar k', self.app.estado.get())
                self.assertIs(self.app.resultado, anterior)
                self.assertEqual(self.app.escalar.get(), invalido)
                self.assertFalse(self.app.reproductor.pasos)
        self.app.escalar.set('0.1')
        self.app.calcular()
        self.assertEqual(self.app.resultado, [[Fraction(1, 30), Fraction(1, 100)], [Fraction(-1, 5), Fraction(2, 5)]])

    def test_escalar_edicion_deshacer_y_retorno_a_suma(self):
        """Cambiar k detiene el reloj; deshacer recupera kA y volver conserva B."""
        self.app.cargar_ejemplo()
        b = self.app.editor_b.leer()
        self.app.operacion.set('escalar')
        self.app.escalar.set('0')
        self.app.calcular()
        self.assertEqual(self.app.resultado, [[0, 0], [0, 0]])
        self.app.alternar_recorrido()
        self.app.escalar.set('2')
        self.assertIsNone(self.app.reproductor.pendiente)
        self.assertFalse(self.app.reproductor.pasos)
        self.app.deshacer()
        self.assertEqual(self.app.escalar.get(), '0')
        self.assertTrue(self.app.vigente)
        self.assertEqual(len(self.app.reproductor.pasos), 4)
        self.app.operacion.set('sumar')
        self.assertEqual(self.app.editor_b.leer(), b)
        self.assertEqual(self.app.editor_b.winfo_manager(), 'grid')
        self.assertEqual(self.app.tarjeta_escalar.winfo_manager(), '')
        self.app.deshacer()
        self.assertEqual(self.app.operacion.get(), 'sumar')
        self.assertEqual(self.app.tarjeta_escalar.winfo_manager(), '')
        self.assertFalse(self.app.vigente)
        self.assertFalse(self.app.reproductor.pasos)

    def test_ejemplo_escalar_limpieza_y_reutilizacion(self):
        """El ejemplo de kA, sus equivalencias y deshacer limpieza conservan la sesión."""
        from interfaz.desarrollo import detallar_paso
        self.app.operacion.set('escalar')
        self.app.cargar_ejemplo()
        self.app.calcular()
        esperado = [[Fraction(-1, 2), Fraction(-3, 20)], [3, -6]]
        self.assertEqual(self.app.resultado, esperado)
        tokens, _ = detallar_paso(self.app.desarrollo.pasos[0])
        self.assertEqual(tokens, [Fraction(-3, 2), '×', Fraction(1, 3), '=', ('(-3) × 1', '2 × 3'), '=', (-3, 6), '=', Fraction(-1, 2)])
        self.app.ver_todo()
        self.app.alternar_tema()
        self.assertEqual(self.app.resultado, esperado)
        self.app.limpiar()
        self.app.deshacer()
        self.assertEqual(self.app.operacion.get(), 'escalar')
        self.assertEqual(self.app.escalar.get(), '-3/2')
        self.assertEqual(self.app.resultado, esperado)
        self.app.reutilizar('A')
        self.assertEqual(self.app.editor_a.leer(), esperado)
        self.assertEqual(self.app.resultado, esperado)
        self.assertFalse(self.app.vigente)

    def test_etapas_escalar_se_revelan_en_orden_y_reinician(self):
        """La cuenta se desarrolla antes de guardar y cada etapa conserva sus orígenes."""
        self.app.operacion.set('escalar')
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.app.reproductor.siguiente()
        self.assertIn('Escalar k = -3/2', self.app.resumen.cget('text'))
        self.assertIn('Elemento A[1,1] = 1/3', self.app.resumen.cget('text'))
        self.assertIn('A[1,1]', self.app.editor_a.etiqueta_nombre.cget('text'))
        self.assertIn('R[1,1]', self.app.titulo_resultado.cget('text'))
        self.app.reproductor.siguiente()
        self.assertEqual(self.app.formula_previa.tokens[0], ('(-3) × 1', '2 × 3'))
        self.app.reproductor.siguiente()
        self.assertIn('entre 3', self.app.resumen.cget('text'))
        self.assertEqual(self.app.vista_resultado.matriz[0][0], '·')
        self.app.reproductor.siguiente()
        self.assertEqual(self.app.vista_resultado.matriz[0][0], Fraction(-1, 2))
        self.app.reiniciar_recorrido()
        self.assertEqual(self.app.vista_resultado.matriz[0][0], '·')
        self.assertFalse(self.app.reproductor.activo)
        self.assertEqual(self.app.reproductor.demora(), 2000)

    def test_transpuesta_rectangular_ignora_b_y_k(self):
        """Solo lee A y genera etapas con origen y destino intercambiados."""
        self.app.editor_a.cargar([['1/3', -2, 5], [0, 4, '1/2']])
        self.app.editor_b.cargar([['incorrecto']])
        self.app.escalar.set('1/0')
        self.app.operacion.set('transponer')
        self.app.calcular()
        esperado = [[Fraction(1, 3), 0], [-2, 4], [5, Fraction(1, 2)]]
        self.assertEqual(self.app.resultado, esperado)
        self.assertEqual(self.app.tarjeta_transpuesta.winfo_manager(), 'grid')
        self.assertEqual(self.app.tarjeta_escalar.winfo_manager(), '')
        self.assertEqual(self.app.editor_b.winfo_manager(), '')
        self.assertIn('3 × 2', self.app.etiqueta_resultado.cget('text'))
        # La tercera celda de R procede de la segunda columna de la primera fila de A.
        for _ in range(7):
            self.app.reproductor.siguiente()
        self.assertIn('A[1,2]', self.app.editor_a.etiqueta_nombre.cget('text'))
        self.assertIn('R[2,1]', self.app.titulo_resultado.cget('text'))
        self.assertEqual(self.app.vista_resultado.matriz[1][0], '·')
        self.app.reproductor.siguiente()
        self.assertEqual(self.app.formula_previa.tokens, ['A[1,2]', '→', 'R[2,1]'])
        self.app.reproductor.siguiente()
        self.assertEqual(self.app.vista_resultado.matriz[1][0], -2)
        self.app.reproductor.completar()
        self.assertEqual(self.app.vista_resultado.matriz, esperado)
        self.app.ver_todo()
        self.assertEqual(self.app.desarrollo.pasos[2], (1, 0, -2, None, -2, 'T'))

    def test_transpuesta_deshacer_reutilizar_y_volver(self):
        """El resultado reutilizado cambia de tamaño y Deshacer recupera la operación anterior."""
        self.app.cargar_ejemplo()
        b = self.app.editor_b.leer()
        self.app.operacion.set('transponer')
        self.app.cargar_ejemplo()
        self.app.calcular()
        original = self.app.editor_a.leer()
        transpuesta = self.app.resultado
        self.app.reutilizar('A')
        self.assertEqual(self.app.editor_a.leer(), transpuesta)
        self.app.calcular()
        self.assertEqual(self.app.resultado, original)
        self.app.limpiar()
        self.app.deshacer()
        self.assertEqual(self.app.operacion.get(), 'transponer')
        self.assertEqual(self.app.resultado, original)
        self.app.operacion.set('sumar')
        self.assertEqual(self.app.editor_b.leer(), b)
        self.app.deshacer()
        self.assertEqual(self.app.operacion.get(), 'sumar')
        self.assertFalse(self.app.vigente)
        self.assertFalse(self.app.reproductor.pasos)

    def test_limpiar_y_deshacer_conservan_operacion_seleccionada(self):
        """Limpiar y restaurar datos mantienen cada formulario y su cálculo válido."""
        for operacion in ('sumar', 'restar', 'escalar', 'transponer', 'multiplicar'):
            with self.subTest(operacion=operacion):
                self.app.operacion.set(operacion)
                self.app.cargar_ejemplo()
                self.app.operacion.set(operacion)
                self.app.calcular()
                esperado = self.app.resultado
                self.app.limpiar()
                self.assertEqual(self.app.operacion.get(), operacion)
                self.assertIsNone(self.app.resultado)
                self.assertFalse(self.app.reproductor.pasos)
                self.app.deshacer()
                self.assertEqual(self.app.operacion.get(), operacion)
                self.assertEqual(self.app.resultado, esperado)
                self.assertTrue(self.app.vigente)

    def test_desarrollo_dibuja_cada_formula_sin_ampliar_recorrido_breve(self):
        """El desarrollo incluye pares y denominador común sin omitir fórmulas."""
        from interfaz.explicacion import etapas_completas
        from interfaz.notacion import Notacion
        self.app.operacion.set('multiplicar')
        self.app.editor_a.cargar([[Fraction(1, 2), Fraction(-1, 3)]])
        self.app.editor_b.cargar([[1], [1]])
        self.app.calcular()
        paso = self.app.desarrollo.pasos[0]
        esperadas = [list(e.tokens) for e in etapas_completas(paso, 0)]
        pendientes = [self.app.desarrollo.cuerpo.winfo_children()[0]]
        formulas = []
        while pendientes:
            widget = pendientes.pop(0)
            if isinstance(widget, Notacion):
                formulas.append(widget.tokens)
            pendientes[0:0] = widget.winfo_children()
        self.assertEqual(formulas, esperadas)
        self.assertFalse(any(e.fase == 'denominador' for e in self.app.reproductor.secuencia))

    def test_transpuesta_valida_a_y_su_tamano_aplicado(self):
        """La entrada unaria no omite errores de A ni dimensiones sin aplicar."""
        self.app.operacion.set('transponer')
        self.app.editor_a.filas.set('3')
        self.app.calcular()
        self.assertIn('pulsa Aplicar', self.app.estado.get())
        self.app.editor_a.filas.set('2')
        self.app.editor_a.celdas[0][0].delete(0, 'end')
        self.app.calcular()
        self.assertIn('A[1,1]', self.app.estado.get())
        self.assertIsNone(self.app.resultado)

    def test_producto_rectangular_contexto_pares_y_guardado(self):
        """Señala fila/columna y cada par, sin revelar la celda hasta terminar la suma."""
        self.app.operacion.set('multiplicar')
        self.app.cargar_ejemplo()
        self.app.calcular()
        self.assertEqual(self.app.resultado, [[5, 11], [14, 23]])
        self.assertEqual(self.app.formula_previa.tokens, ['Fila 1 de A', '·', 'Columna 2 de B', '=', 11])
        self.app.reproductor.siguiente()
        self.assertTrue(all(v.resaltada for v in self.app.editor_a.vistas[0]))
        self.assertTrue(all(f[0].resaltada for f in self.app.editor_b.vistas))
        self.assertFalse(self.app.editor_a.vistas[1][0].resaltada)
        self.app.reproductor.siguiente()
        self.assertTrue(self.app.editor_a.vistas[0][0].foco_producto)
        self.app.reproductor.siguiente()
        self.assertTrue(self.app.editor_a.vistas[0][1].foco_producto)
        self.assertTrue(self.app.editor_b.vistas[1][0].foco_producto)
        self.assertIn('A[1,2] = 2', self.app.resumen.cget('text'))
        while self.app.reproductor.secuencia[self.app.reproductor.indice].fase != 'sumar':
            self.app.reproductor.siguiente()
        self.assertEqual(self.app.formula_previa.tokens, [1, '+', 4, '+', 0, '=', 5])
        self.assertEqual(self.app.vista_resultado.matriz[0][0], '·')
        self.app.reproductor.siguiente()
        self.assertEqual(self.app.vista_resultado.matriz[0][0], 5)
        self.app.reproductor.anterior()
        self.assertEqual(self.app.vista_resultado.matriz[0][0], '·')
        self.app.reproductor.completar()
        self.assertEqual(self.app.vista_resultado.matriz, self.app.resultado)
        self.app.ver_todo()
        self.assertEqual(self.app.desarrollo.pasos[1][2:4], ((1, 2, 3), (0, 1, 3)))

    def test_producto_errores_conservan_resultado_y_validan_b(self):
        """Rechaza incompatibilidad, tamaño sin aplicar y celda inválida sin perder datos."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        anterior = self.app.resultado
        self.app.operacion.set('multiplicar')
        self.app.editor_a.cargar([[1, 2, 3]])
        self.app.editor_b.cargar([[1, 2, 3]])
        self.app.calcular()
        self.assertIn('columnas de A', self.app.estado.get())
        self.assertIs(self.app.resultado, anterior)
        self.app.editor_b.cargar([[1], [2], [3]])
        self.app.editor_b.filas.set('2')
        self.app.calcular()
        self.assertIn('pulsa Aplicar', self.app.estado.get())
        self.app.editor_b.filas.set('3')
        self.app.editor_b.celdas[0][0].delete(0, 'end')
        self.app.calcular()
        self.assertIn('B[1,1]', self.app.estado.get())
        self.app.editor_b.celdas[0][0].insert(0, '1')
        self.app.escalar.set('1/0')
        self.app.calcular()
        self.assertEqual(self.app.resultado, [[14]])
        self.app.editor_a.cargar([[2], [-1]])
        self.app.editor_b.cargar([[3, 4, 5]])
        self.app.calcular()
        self.app.reproductor.completar()
        self.assertEqual(self.app.resultado, [[6, 8, 10], [-3, -4, -5]])

    def test_producto_deshacer_reutilizar_y_editar_cancelan(self):
        """El historial guarda A/B y el resultado; editar detiene el recorrido de pares."""
        self.app.operacion.set('multiplicar')
        self.app.cargar_ejemplo()
        self.app.calcular()
        b = self.app.editor_b.leer()
        self.app.reutilizar('B')
        self.app.calcular()
        self.assertIn('A es 2x3 y B es 2x2', self.app.estado.get())
        self.app.deshacer()
        self.assertEqual(self.app.editor_b.leer(), b)
        self.assertTrue(self.app.vigente)
        self.app.alternar_recorrido()
        self.app.editor_b.celdas[0][0].delete(0, 'end')
        self.assertIsNone(self.app.reproductor.pendiente)
        self.assertFalse(any(v.resaltada for fila in self.app.editor_b.vistas for v in fila))
        self.app.deshacer()
        self.assertTrue(self.app.vigente)
        self.assertEqual(self.app.resultado, [[5, 11], [14, 23]])
        self.assertFalse(self.app.reproductor.activo)
