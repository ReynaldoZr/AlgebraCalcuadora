"""Comprueba biblioteca, recuperación, pegado e historial con widgets de prueba.

Tema: integración de herramientas de estudio sin automatizar la pantalla de la persona.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy
from fractions import Fraction as F
import unittest
from unittest.mock import Mock, patch

from tests import test_ventana as ventana_pruebas


class PruebasGuardados(unittest.TestCase):
    """Trabaja con una biblioteca en memoria y ventanas retiradas, sin tocar archivos personales."""

    @classmethod
    def setUpClass(cls):
        """Comprueba la disponibilidad de Tk con la misma regla de CI del proyecto."""
        ventana_pruebas.PruebasVentana.setUpClass()

    def setUp(self):
        """Construye una sesión aislada y un almacén que no escribe en el disco real."""
        import tkinter as tk
        from interfaz.biblioteca import Biblioteca
        from interfaz.ventana import CalculadoraVentana
        self.raiz = tk.Tk()
        self.raiz.withdraw()
        self.biblioteca = Biblioteca()
        self.app = CalculadoraVentana(self.raiz, self.biblioteca)
        self.cuaderno = self.app.cuaderno
        self.addCleanup(self.cerrar)

    def cerrar(self):
        """Cancela reproducción y procesa estilos pendientes antes de destruir la sesión."""
        self.raiz.update_idletasks()
        self.app.cerrar()

    def test_transpuestas_guardadas_y_abrir_no_duplica_historial(self):
        """Se guardan dos resultados distintos, y abrir conserva el ejercicio completo."""
        self.app.operacion.set('transponer')
        self.app.editor_a.cargar([[F(1, 3), -2, 5]])
        self.app.calcular()
        ejercicio = self.cuaderno.ejercicio()
        uno = self.biblioteca.guardar(ejercicio)
        dos = self.biblioteca.guardar(self.cuaderno.matriz('Resultado'))
        self.assertEqual((uno['nombre'], dos['nombre']), ('Transpuesta 1', 'Transpuesta 2'))
        self.assertEqual(uno['simbolo'], 'Aᵀ')
        self.assertEqual(len(self.biblioteca.listar(True)), 1)
        self.app.operacion.set('restar')
        with self.assertRaises(ValueError):
            self.cuaderno.ejercicio()
        self.cuaderno.abrir_ejercicio(uno)
        self.assertEqual(self.app.operacion.get(), 'transponer')
        self.assertEqual(self.app.resultado, [[F(1, 3)], [-2], [5]])
        self.assertEqual(len(self.biblioteca.listar(True)), 1)
        self.assertTrue(uno['pasos'])

    def test_guardar_resultado_directo_conserva_calculadora_y_atajos(self):
        """El botón guarda en la misma biblioteca sin navegar ni reemplazar A."""
        self.app.operacion.set('transponer')
        self.app.editor_a.cargar([[F(1, 3), -2]])
        self.app.calcular()
        pagina = self.app.pestanas.select()
        entrada = self.app.editor_a.leer()
        resultado = deepcopy(self.app.resultado)
        with patch.object(self.cuaderno, 'dialogo_nombre') as dialogo:
            self.app.guardar_resultado.invoke()
        registro = dialogo.call_args.args[0]
        self.assertEqual(dialogo.call_args.kwargs, {'permanecer': True})
        ventana, aviso = Mock(), Mock()
        self.cuaderno._confirmar_guardado(registro, 'Mi transpuesta', 'Para otro cálculo', False,
                                         ventana, aviso, 'T₂', permanecer=True)
        self.assertEqual(self.app.pestanas.select(), pagina)
        self.assertEqual(self.app.editor_a.leer(), entrada)
        self.assertEqual(self.app.resultado, resultado)
        self.assertTrue(self.app.vigente)
        guardado = self.biblioteca.listar()[0]
        self.assertEqual((guardado['tipo'], guardado['nombre'], guardado['simbolo']), ('matriz', 'Mi transpuesta', 'T₂'))
        self.assertEqual(guardado['resultado'], [['1/3'], ['-2']])
        self.assertIn('guardado', self.app.estado.get())
        self.app.usar_a.invoke()
        self.assertEqual(self.app.editor_a.leer(), resultado)
        self.assertEqual(str(self.app.guardar_resultado.cget('state')), 'disabled')

    def test_guardar_resultado_en_otro_tema_y_mantener_reutilizacion(self):
        """Los temas nuevos guardan la respuesta exacta y mantienen Usar resultado como A."""
        panel = self.app.abrir_tema('Inversas')
        panel.cargar_ejemplo()
        panel.calcular()
        pagina = self.app.pestanas.select()
        resultado = deepcopy(panel.presentacion.matriz)
        with patch.object(self.cuaderno, 'dialogo_nombre') as dialogo:
            panel.guardar_resultado.invoke()
        registro = dialogo.call_args.args[0]
        self.assertEqual(registro['simbolo'], 'A⁻¹')
        self.cuaderno._confirmar_guardado(registro, '', '', False, Mock(), Mock(), permanecer=True)
        self.assertEqual(self.app.pestanas.select(), pagina)
        self.assertEqual(self.biblioteca.listar()[0]['nombre'], 'Inversa por Gauss-Jordan 1')
        self.assertTrue(panel.vigente)
        panel.reutilizar_boton.invoke()
        self.assertEqual(panel.editores['A'].leer(), resultado)
        self.assertEqual(str(panel.guardar_resultado.cget('state')), 'disabled')

    def test_iconos_de_temas_y_matrices_tres_por_tres(self):
        """Matrices tiene nueve casillas en tres filas/columnas; los demás temas tienen símbolo."""
        icono = self.app.icono_matrices
        coordenadas = [icono.coords(i) for i in icono.find_withtag('casilla')]
        self.assertEqual(len(coordenadas), 9)
        self.assertEqual(len({c[0] for c in coordenadas}), 3)
        self.assertEqual(len({c[1] for c in coordenadas}), 3)
        for boton in self.app.botones_temas:
            self.assertTrue(boton.icono_tema.find_withtag('trazo'))
        panel = self.app.abrir_tema('Vectores')
        self.app._cambiar_pestana()
        vector = next(b for b in self.app.botones_temas if b.cget('text') == 'Vectores')
        self.assertTrue(vector.icono_tema.seleccionado)
        self.assertFalse(icono.seleccionado)
        self.app.alternar_tema()
        self.assertEqual(icono.itemcget(icono.find_withtag('casilla')[0], 'outline'), self.app.tema.colores['acento'])
        self.app.pestanas.select(panel.pagina_pasos)
        self.app._cambiar_pestana()
        self.assertEqual(self.app.lateral.winfo_manager(), '')
        self.app.pestanas.select(panel)
        self.app._cambiar_pestana()
        self.assertEqual(vector.marco_tema.winfo_manager(), 'pack')
        self.assertEqual(vector.pack_info()['side'], 'left')

    def test_ejercicio_jordan_con_parametros_y_busqueda(self):
        """Un ejercicio con infinitas soluciones se recupera con su método, entradas y pasos."""
        panel = self.app.abrir_tema('Sistemas')
        panel.seleccionar('jordan')
        self.cuaderno.aplicar_caso('Infinitas soluciones')
        panel.calcular()
        guardado = self.biblioteca.guardar(self.cuaderno.ejercicio(), 'Práctica de parámetros', 'Revisar variable libre')
        self.assertEqual(panel.presentacion.calculo.datos['clasificacion'], 'infinitas')
        panel.limpiar()
        self.cuaderno.abrir_ejercicio(guardado)
        self.assertEqual(panel.clave, 'jordan')
        self.assertEqual(panel.presentacion.calculo.datos['clasificacion'], 'infinitas')
        self.assertEqual(len(self.biblioteca.listar(True)), 1)
        vista = self.cuaderno.vista
        vista.busqueda.set('variable libre')
        self.assertEqual(len(vista.arbol.get_children()), 1)
        vista.arbol.selection_set(guardado['id'])
        vista.seleccionar()
        self.assertIn('Práctica', vista.titulo.cget('text'))
        vista.ver_desarrollo()
        self.assertEqual(len(vista.detalle.pasos), len(guardado['pasos']) + 1)

    def test_matriz_guardada_se_carga_en_otro_tema_y_se_puede_deshacer(self):
        """Guardar A no requiere calcular y cargar una copia en otro tema es deshacible."""
        self.app.editor_a.cargar([[1, 2], [3, 4]])
        guardado = self.biblioteca.guardar(self.cuaderno.matriz('A'), 'Mi matriz inicial')
        panel = self.app.abrir_tema('Inversas')
        antes = [[c.get() for c in f] for f in panel.editores['A'].celdas]
        self.cuaderno.usar_matriz(guardado)
        self.assertEqual(panel.editores['A'].leer(), [[1, 2], [3, 4]])
        panel.deshacer()
        self.assertEqual([[c.get() for c in f] for f in panel.editores['A'].celdas], antes)
        self.assertEqual(guardado['resultado'], [['1', '2'], ['3', '4']])

    def test_pegar_es_una_edicion_y_un_bloque_erroneo_no_altera_celdas(self):
        """Pegar valida el bloque antes de cargar y Deshacer recupera el cálculo anterior."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        anterior = self.app.editor_a.leer()
        self.app.editor_a.pegar_texto('1/3\t2\n-3\t4')
        self.assertEqual(self.app.editor_a.leer(), [[F(1, 3), 2], [-3, 4]])
        self.assertFalse(self.app.vigente)
        with self.assertRaises(ValueError):
            self.app.editor_a.pegar_texto('1 2\n3')
        self.assertEqual(self.app.editor_a.leer(), [[F(1, 3), 2], [-3, 4]])
        self.app.deshacer()
        self.assertEqual(self.app.editor_a.leer(), anterior)
        self.assertTrue(self.app.vigente)

    def test_biblioteca_se_abre_desde_cualquier_tema_y_no_calcula_con_el_atajo(self):
        """Biblioteca está accesible desde la cabecera sin ocupar una pestaña en cada tema."""
        vista = self.cuaderno.vista
        for tema in ('Sistemas', 'Inversas', 'LU'):
            panel = self.app.abrir_tema(tema)
            self.assertEqual(self.app.pestanas.tab(vista, 'state'), 'hidden')
            self.assertEqual(self.app.pestanas.tabs().index(str(panel)), 0)
            self.assertEqual(self.app.pestanas.tabs().index(str(panel.pagina_pasos)), 1)
        self.app.mostrar_biblioteca()
        self.assertEqual(self.app.pestanas.select(), str(vista))
        self.app._calcular_visible()
        self.assertFalse(self.biblioteca.listar(True))
        self.assertFalse(panel.vigente)
        self.app.mostrar_matrices()
        self.assertEqual(self.app.pestanas.tab(vista, 'state'), 'hidden')

    def test_error_del_historial_no_impide_resultado_valido(self):
        """Un disco no disponible conserva el cálculo y explica el fallo de guardado."""
        self.app.cargar_ejemplo()
        with patch.object(self.biblioteca, '_confirmar', side_effect=OSError('Sin espacio')):
            self.app.calcular()
        self.assertTrue(self.app.vigente)
        self.assertEqual(self.app.resultado[0][0], F(1, 2))
        self.assertIn('No se pudo guardar el historial', self.app.estado.get())

    def test_propiedad_con_nombre_especifico_y_sin_resultado_matricial(self):
        """El nombre automático identifica la igualdad y no ofrece guardar un resultado inexistente."""
        panel = self.app.abrir_tema('Propiedades')
        panel.seleccionar('prop_transpuesta_doble')
        panel.cargar_ejemplo()
        panel.calcular()
        registro = self.biblioteca.guardar(self.cuaderno.ejercicio())
        self.assertIn('(Aᵀ)ᵀ = A', registro['nombre'])
        self.cuaderno._crear_menu()
        for indice in range(self.cuaderno.menu.index('end') + 1):
            if self.cuaderno.menu.type(indice) == 'command' and self.cuaderno.menu.entrycget(indice, 'label') == 'Guardar matriz resultado…':
                self.assertEqual(self.cuaderno.menu.entrycget(indice, 'state'), 'disabled')
                break
        else:
            self.fail('Falta la acción de resultado del menú.')

    def test_historial_recupera_instantanea_y_puede_convertirse_en_guardado(self):
        """Cambiar casillas después de calcular no modifica el elemento del historial."""
        self.app.cargar_ejemplo()
        self.app.calcular()
        registro = self.biblioteca.listar(True)[0]
        copia = deepcopy(registro)
        self.app.editor_a.cargar([[99]])
        self.assertEqual(self.biblioteca.listar(True)[0], copia)
        vista = self.cuaderno.vista
        vista.modo.set('Historial')
        vista.arbol.selection_set(registro['id'])
        with patch.object(self.cuaderno, 'dialogo_nombre') as dialogo:
            vista.guardar_historial()
        dialogo.assert_called_once_with(copia)
        self.cuaderno.abrir_ejercicio(registro)
        self.assertEqual(self.app.editor_a.leer(), [[F(1, 3), F(1, 10)], [-2, 4]])
