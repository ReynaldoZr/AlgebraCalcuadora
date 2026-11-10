"""Comprueba la integración de semana 12 con GUI, biblioteca y consola.

Tema: aproximaciones guardadas separadas del álgebra exacta y sus dependencias.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from tests import test_ventana as ventana_pruebas
from tests.numericos import test_semana12 as prueba_numerica


class PruebasIntegracionNumerica(unittest.TestCase):
    """Usa Tk retirado y archivos temporales, sin controlar la pantalla del usuario."""

    @classmethod
    def setUpClass(cls):
        """Exige bibliotecas y Tk bajo los contratos de la CI existente."""
        prueba_numerica.PruebasSemana12.setUpClass()
        ventana_pruebas.PruebasVentana.setUpClass()

    def setUp(self):
        """Construye una sesión aislada con biblioteca en memoria."""
        import tkinter as tk
        from interfaz.biblioteca import Biblioteca
        from interfaz.ventana import CalculadoraVentana
        self.raiz = tk.Tk()
        self.raiz.withdraw()
        self.app = CalculadoraVentana(self.raiz, Biblioteca())
        self.panel = self.app.abrir_tema('Numéricos')
        self.addCleanup(self.cerrar)

    def cerrar(self):
        """Procesa estilos pendientes y cancela reproducción antes de destruir Tk."""
        self.raiz.update_idletasks()
        self.app.cerrar()

    def test_catalogo_completo_y_tablas_sin_recortes(self):
        """Los nueve métodos calculan sus ejemplos y exponen todas las filas del resultado."""
        from interfaz.metodos_numericos import METODOS_NUMERICOS
        for clave in METODOS_NUMERICOS:
            with self.subTest(clave=clave):
                self.panel.seleccionar(clave)
                self.panel.cargar_ejemplo()
                self.panel.calcular()
                self.assertTrue(self.panel.vigente, self.panel.estado.get())
                self.app.pestanas.select(self.panel.pagina_pasos)
                self.panel._cambiar_vista()
                filas = self.panel.presentacion.calculo.datos.get('filas', [])
                self.assertEqual(len(self.panel.tabla.get_children()), len(filas))
                self.assertEqual(self.panel.desarrollo.pasos, self.panel.presentacion.calculo.pasos)
                self.app.pestanas.select(self.panel)

    def test_guardado_persistente_reapertura_pdf_y_compatibilidad_v1(self):
        """Un ejercicio numérico conserva parámetros y pasos sin una matriz exacta ficticia."""
        from interfaz.biblioteca import Biblioteca, crear_registro
        from interfaz.exportar_pdf import crear_pdf, lineas_documento
        self.panel.cargar_caso('cos(x)-x')
        self.panel.calcular()
        registro = self.app.cuaderno.ejercicio()
        self.assertEqual(registro['entradas'], {})
        self.assertIsNone(registro['resultado'])
        self.assertEqual(registro['parametros']['funcion'], 'cos(x)-x')
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / 'biblioteca.json'
            biblioteca = Biblioteca(ruta)
            guardado = biblioteca.guardar(registro)
            nueva = Biblioteca(ruta)
            self.assertFalse(nueva.error_lectura)
            self.assertEqual(nueva.listar()[0]['parametros'], guardado['parametros'])
            self.assertEqual(nueva.datos['version'], 2)
            # Una biblioteca exacta antigua se interpreta sin alterar sus números.
            antigua = Biblioteca()
            antigua.guardar(crear_registro('Matrices', 'transponer', {'A': [[1, 2]]}, resultado=[[1], [2]]))
            datos = deepcopy(antigua.datos)
            datos['version'] = 1
            ruta.write_text(json.dumps(datos), encoding='utf-8')
            migrada = Biblioteca(ruta)
            self.assertEqual(migrada.datos['version'], 2)
            self.assertEqual(migrada.listar()[0]['resultado'], [['1'], ['2']])
        historial = len(self.app.cuaderno.biblioteca.listar(True))
        self.panel.limpiar()
        self.app.cuaderno.abrir_ejercicio(registro)
        self.assertTrue(self.panel.vigente)
        self.assertEqual(len(self.app.cuaderno.biblioteca.listar(True)), historial)
        self.assertIn('cos(x)-x', '\n'.join(lineas_documento(registro)))
        self.assertTrue(crear_pdf(registro).startswith(b'%PDF-1.4'))

    def test_edicion_deshacer_error_y_separacion_del_algebra(self):
        """Editar detiene el reloj y un error conserva el cálculo numérico anterior."""
        self.panel.cargar_ejemplo()
        self.panel.calcular()
        anterior = self.panel.presentacion
        self.panel.alternar_recorrido()
        self.assertIsNotNone(self.panel.reproductor.pendiente)
        self.panel.parametros['tolerancia'].set('0')
        self.assertIsNone(self.panel.reproductor.pendiente)
        self.panel.calcular()
        self.assertFalse(self.panel.vigente)
        self.assertIs(self.panel.presentacion, anterior)
        self.panel.deshacer()
        self.assertTrue(self.panel.vigente)
        self.assertEqual(self.panel.parametros['tolerancia'].get(), '0.0001')
        self.assertIsNone(self.app.resultado)
        self.panel.seleccionar('num_errores')
        self.panel.deshacer()
        self.assertEqual(self.panel.clave, 'num_errores')
        self.assertFalse(self.panel.vigente)

    def test_consola_biseccion_y_menu_errores(self):
        """La consola solicita parámetros y muestra contraste, tabla y salida normal."""
        from main import main
        entradas = ['8', '1', 'cos(x)-x', '0', '1', '', '', '', '', '2', '99', '9']
        salida = io.StringIO()
        with patch('builtins.input', side_effect=entradas), redirect_stdout(salida):
            main()
        self.assertIn('SciPy:', salida.getvalue())
        self.assertIn('Ea (%)', salida.getvalue())
        self.assertIn('Hasta pronto', salida.getvalue())

    def test_cambio_metodo_limpia_respuesta_y_ayuda_ajena(self):
        """Cada método muestra su ayuda y no hereda resultados de otro cálculo."""
        self.panel.cargar_ejemplo()
        self.panel.calcular()
        self.assertEqual(self.panel.reproductor.indice, 0)
        self.assertTrue(self.panel.formula.tokens)

        self.panel.seleccionar('num_inestabilidad')
        self.assertIsNone(self.panel.presentacion)
        self.assertIn('Todavía no hay resultado', self.panel.resultado_texto.get('1.0', 'end'))
        self.assertIn('Reformulada', self.panel.nota.cget('text'))
        self.assertNotIn('Residuo:', self.panel.nota.cget('text'))
        self.assertFalse(self.panel.formula.tokens)
        self.assertFalse(self.panel.guardar.instate(['!disabled']))
        self.panel.deshacer()
        self.assertIsNone(self.panel.presentacion)

        self.panel.seleccionar('num_flotante')
        self.assertIn('no necesita datos', self.panel.ayuda_entrada.cget('text'))
        self.assertTrue(self.panel.ejemplo_boton.instate(['disabled']))
        self.panel.calcular()
        self.assertTrue(self.panel.vigente)
        self.assertTrue(self.panel.formula.tokens)

    def test_teclado_respeta_cursor_seleccion_y_deshacer(self):
        """Los signos componen una función válida y cada pulsación se puede deshacer."""
        entrada = self.panel.entradas['funcion']
        self.panel.teclado.botones['x²'].invoke()
        self.panel.teclado.botones['−'].invoke()
        entrada.insert('end', '2')
        self.assertEqual(entrada.get(), 'x^2-2')
        self.panel.parametros['a'].set('1')
        self.panel.parametros['b'].set('2')
        self.panel.calcular()
        self.assertTrue(self.panel.vigente)
        self.assertAlmostEqual(self.panel.presentacion.calculo.valor, 2 ** 0.5, places=3)

        entrada.selection_range(0, 3)
        self.panel.teclado.botones['x'].invoke()
        self.assertEqual(entrada.get(), 'x-2')
        self.assertIn('Resultado anterior', self.panel.resultado_texto.get('1.0', 'end'))
        self.panel.deshacer()
        self.assertEqual(entrada.get(), 'x^2-2')
        self.assertTrue(self.panel.vigente)

        entrada.selection_clear()
        entrada.icursor(3)
        self.panel.teclado.botones['×'].invoke()
        self.assertEqual(entrada.get(), 'x^2*-2')
        self.panel.teclado.botones['⌫'].invoke()
        self.assertEqual(entrada.get(), 'x^2-2')
        entrada.icursor(0)
        self.panel.teclado.botones['⌫'].invoke()
        self.assertEqual(entrada.get(), 'x^2-2')

    def test_matrices_vacias_muestran_casillas_editables(self):
        """Las matrices vacías ofrecen entradas visibles en vez de lienzos en blanco."""
        self.panel.seleccionar('num_sistema')
        for editor in self.panel.editores.values():
            for fila, vistas in zip(editor.celdas, editor.vistas):
                for entrada, vista in zip(fila, vistas):
                    self.assertEqual(entrada.get(), '')
                    self.assertEqual(entrada.winfo_manager(), 'grid')
                    self.assertEqual(vista.winfo_manager(), '')
        self.panel.cargar_caso('Solución conocida')
        self.panel.calcular()
        self.assertTrue(self.panel.vigente, self.panel.estado.get())
        self.panel.limpiar()
        self.assertEqual(self.panel.clave, 'num_sistema')
        self.assertEqual(self.panel.editores['A'].vistas[0][0].winfo_manager(), '')

    def test_formularios_y_controles_en_tamano_minimo(self):
        """Los campos de ambos grupos y los controles caben en los nueve formularios."""
        from interfaz.metodos_numericos import METODOS_NUMERICOS
        self.raiz.geometry('1120x760')
        self.raiz.deiconify()
        for clave, metodo in METODOS_NUMERICOS.items():
            with self.subTest(clave=clave):
                self.panel.seleccionar(clave)
                self.raiz.update()
                for control in (self.panel.anterior, self.panel.reproducir, self.panel.grafica, self.panel.guardar):
                    self.assertTrue(control.winfo_ismapped())
                    self.assertLessEqual(control.winfo_rooty() + control.winfo_height(), self.raiz.winfo_rooty() + self.raiz.winfo_height())
                for nombre in metodo.campos_a + metodo.campos_b:
                    campo = self.panel.campos[nombre]
                    self.assertTrue(campo.winfo_ismapped())
                    self.assertLessEqual(campo.winfo_rooty() + campo.winfo_height(), campo.master.winfo_rooty() + campo.master.winfo_height())
                if 'funcion' in metodo.campos_a:
                    self.assertTrue(self.panel.teclado.winfo_ismapped())
                    self.assertLessEqual(
                        self.panel.teclado.winfo_rooty() + self.panel.teclado.winfo_height(),
                        self.panel.grupos[0].winfo_rooty() + self.panel.grupos[0].winfo_height(),
                    )


class PruebasAislamientoNumerico(unittest.TestCase):
    """Comprueba imports sin depender de Tk o del contenido del entorno de la persona."""

    def test_importar_calculadora_no_carga_bibliotecas_numericas(self):
        """Consola y ventana se pueden importar sin cargar numpy, scipy o matplotlib."""
        codigo = 'import sys; import main; import interfaz.ventana; assert not any(n in sys.modules for n in ("numpy","scipy","matplotlib"))'
        resultado = subprocess.run([sys.executable, '-c', codigo], capture_output=True, text=True, timeout=20)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)

    def test_imports_externos_limitados_a_su_unidad(self):
        """Los adaptadores gráficos autorizados no habilitan SymPy ni imports en álgebra exacta."""
        import ast
        from herramientas.comprobar_reglas import revisar_import
        self.assertEqual(revisar_import(ast.parse('import matplotlib').body[0], False, True), [])
        self.assertTrue(revisar_import(ast.parse('import numpy').body[0], True, False))
        self.assertTrue(revisar_import(ast.parse('import sympy').body[0], True, True))
