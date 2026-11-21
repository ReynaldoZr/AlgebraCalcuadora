"""Ejercita Qt Quick sin capturas ni control de la pantalla de la persona.

Tema: carga QML, teclado, sesiones, tablas, guardados y temporizador.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import importlib.util
import os
from pathlib import Path
import tempfile
from time import monotonic
import unittest


class PruebasQtQuick(unittest.TestCase):
    """Carga componentes reales con una biblioteca aislada y plataforma offscreen."""

    @classmethod
    def setUpClass(cls):
        """Exige Qt en CI; permite ejecutar cálculo y consola sin instalarlo."""
        if importlib.util.find_spec('PySide6') is None:
            if os.environ.get('CALCULADORA_EXIGIR_QT') == '1':
                raise RuntimeError('CI necesita requirements-interfaz.txt.')
            raise unittest.SkipTest('Instala requirements-interfaz.txt para probar Qt Quick.')
        os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
        os.environ.setdefault('QT_QUICK_BACKEND', 'software')
        from PySide6.QtCore import qInstallMessageHandler
        from PySide6.QtQuickControls2 import QQuickStyle
        from PySide6.QtWidgets import QApplication
        QQuickStyle.setStyle('Basic')
        cls.mensajes = []
        cls.anterior = qInstallMessageHandler(lambda tipo, contexto, mensaje: cls.mensajes.append(mensaje))
        cls.app = QApplication.instance() or QApplication([])

    @classmethod
    def tearDownClass(cls):
        """Restaura la salida de Qt al concluir estas pruebas."""
        from PySide6.QtCore import qInstallMessageHandler
        qInstallMessageHandler(cls.anterior)

    def setUp(self):
        """Prepara una ventana de pruebas que nunca aparece en la pantalla real."""
        from interfaz.biblioteca import Biblioteca
        from interfaz.qt.aplicacion import crear_motor
        self.mensajes.clear()
        self.motor, self.control = crear_motor(self.app, Biblioteca())
        self.assertEqual(len(self.motor.rootObjects()), 1, '\n'.join(self.mensajes))
        self.ventana = self.motor.rootObjects()[0]
        self.addCleanup(self.cerrar)

    def cerrar(self):
        """Cancela reproducción y destruye la ventana antes de crear la siguiente."""
        self.control.pausar()
        self.ventana.close()
        self.motor.deleteLater()
        self.app.processEvents()
        fallos = [m for m in self.mensajes if any(p in m for p in (
            'ReferenceError', 'TypeError', 'Binding loop', 'Unable to assign',
            'Cannot assign', 'failed to load component', 'Unexpected token',
        ))]
        self.assertFalse(fallos, '\n'.join(fallos))

    def esperar_calculo(self):
        """Procesa el bucle de pruebas hasta recibir la tarea o fallar con un límite."""
        limite = monotonic() + 30
        while self.control.estado['ocupado'] and monotonic() < limite:
            self.app.processEvents()
        self.assertFalse(self.control.estado['ocupado'], 'La tarea no terminó.')
        self.app.processEvents()

    def buscar_control(self, nombre):
        """Recorre el árbol visual, que incluye los elementos creados por Repeater."""
        pendientes = [self.ventana.contentItem()]
        while pendientes:
            item = pendientes.pop()
            if item.objectName() == nombre:
                return item
            pendientes.extend(item.childItems())
        return None

    def test_temas_y_numericos_tablas_completas_y_sesiones(self):
        """Los nueve métodos numéricos conservan todas sus filas y sus pasos."""
        from interfaz.metodos_numericos import METODOS_NUMERICOS
        self.control.abrirTema('Numéricos')
        for clave in METODOS_NUMERICOS:
            with self.subTest(clave=clave):
                self.control.seleccionar(clave)
                self.control.cargarEjemplo('')
                self.control.calcular()
                self.esperar_calculo()
                self.assertTrue(self.control.estado['vigente'], self.control.estado['mensaje'])
                self.ventana.setProperty('vista', 'pasos')
                self.app.processEvents()
                datos = self.control.sesion.presentacion.calculo
                self.assertEqual(len(self.control.resultado['tabla']['filas']), len(datos.datos.get('filas', [])))
                self.assertEqual(len(self.control.resultado['pasos']), len(datos.pasos))
        self.control.seleccionar('num_biseccion')
        self.assertTrue(self.control.estado['vigente'])
        self.assertEqual(self.control.formulario['camposA'][0]['valor'], 'x^4-5*x^3+0.5*x^2-11*x+10')

    def test_tarjeta_iterativa_minima_detalles_y_metodos_anteriores(self):
        """La tabla y sus detalles funcionan en tamaño mínimo sin ampliar otros métodos."""
        from PySide6.QtCore import QMetaObject
        self.ventana.setWidth(1100)
        self.ventana.setHeight(760)
        self.control.abrirTema('Numéricos')
        self.control.seleccionar('num_comparar_iterativos')
        self.control.cargarEjemplo('')
        self.control.calcular()
        self.esperar_calculo()
        tarjeta = self.buscar_control('resultadoIterativo')
        tabla = self.buscar_control('tablaResumenIterativo')
        self.assertTrue(tarjeta.isVisible())
        self.assertGreater(tabla.height(), 0)
        self.assertGreater(tabla.width(), 0)
        boton = self.buscar_control('verDetallesTecnicos')
        self.assertTrue(QMetaObject.invokeMethod(boton, 'clicked'))
        self.app.processEvents()
        self.assertTrue(self.buscar_control('panelDetallesTecnicos').isVisible())
        self.control.seleccionar('num_biseccion')
        self.control.cargarEjemplo('')
        self.control.calcular()
        self.esperar_calculo()
        self.assertTrue(tarjeta.isVisible())
        self.assertGreater(tabla.height(), 0)

    def test_zoom_logaritmico_y_panel_error_ampliado(self):
        """El zoom conserva límites positivos y aplica al panel lógico de error."""
        from math import log10
        from copy import deepcopy
        self.control.abrirTema('Numéricos')
        self.control.cargarEjemplo('cos(x)-x')
        self.control.calcular()
        self.esperar_calculo()
        original = deepcopy(self.control.sesion.capturar())
        self.control.verGrafica(True)
        self.control.expandirPanelGrafica(1)
        self.assertEqual(set(self.control._base_limites_grafica), {1})
        self.assertEqual(self.control._escalas_grafica[1], 'log')
        base = self.control._base_limites_grafica[1]
        self.control.ajustarZoomGrafica(.7, 0, 0)
        limites = self.control._calcular_limites_zoom()[1]
        self.assertGreater(limites[2], 0)
        self.assertAlmostEqual(log10(limites[3] / limites[2]),
                               .7 * log10(base[3] / base[2]))
        from interfaz.numericos.figuras import figura_numerica
        fig = figura_numerica('num_biseccion', self.control.sesion.presentacion.calculo,
                              panel_expandido=1, zoom={1: limites})
        self.assertEqual(tuple(fig.axes[0].get_ylim()), limites[2:])
        self.control.reiniciarVistaGrafica()
        self.assertFalse(self.control.graficaEstado['zoomActivo'])
        self.assertEqual(self.control.sesion.capturar(), original)

    def test_reproduccion_grafica_manual_pausa_y_series_sin_recalculo(self):
        """Reproducir, ocultar curvas y navegar no cambian el cálculo ni dejan un reloj activo."""
        from copy import deepcopy
        from unittest.mock import patch
        from PySide6.QtCore import QMetaObject
        self.control.abrirTema('Numéricos')
        self.control.seleccionar('num_comparar_iterativos')
        self.control.cargarEjemplo('')
        self.control.calcular()
        self.esperar_calculo()
        original = deepcopy(self.control.sesion.capturar())
        self.control.verGrafica(False)
        self.app.processEvents()
        self.assertFalse(self.control.reloj_grafica.isActive())
        boton = self.buscar_control('graficaReproducir')
        self.assertTrue(boton.isVisible())
        with patch('interfaz.qt.catalogo.ejecutar', side_effect=AssertionError('No recalcular')):
            self.assertTrue(QMetaObject.invokeMethod(boton, 'clicked'))
            self.assertTrue(self.control.reloj_grafica.isActive())
            self.assertEqual(self.control.reloj_grafica.interval(), 2000)
            self.control._avanzar_grafica()
            self.assertEqual(self.control.graficaEstado['indice'], 1)
            self.control.pausarGrafica()
            self.control.alternarSerieGrafica('jacobi')
            self.assertFalse(self.control.graficaEstado['series'][0]['activa'])
        self.assertEqual(self.control.sesion.capturar(), original)
        self.control.seleccionar('num_biseccion')
        self.assertFalse(self.control.reloj_grafica.isActive())

    def test_tabla_resultados_larga_permite_scroll_vertical(self):
        """Una inversa 10×10 conserva sus cien filas sin alargar la tarjeta indefinidamente."""
        self.control.abrirTema('Numéricos')
        self.control.seleccionar('num_inversa')
        self.control.redimensionar('A', 10, 10)
        for i in range(10):
            for j in range(10):
                self.control.editarCelda('A', i, j, '1' if i == j else '0')
        self.control.calcular()
        self.esperar_calculo()
        self.assertEqual(len(self.control.resultado['detalleIterativo']['filas']), 100)
        tabla = self.buscar_control('tablaResumenIterativo')
        self.assertGreater(tabla.property('contentHeight'), tabla.height())
        self.assertLessEqual(tabla.height(), 250)
        tabla.setProperty('contentY', tabla.property('contentHeight') - tabla.height())
        self.assertGreater(tabla.property('contentY'), 0)

    def test_newton_formulario_vacio_modos_y_residuo(self):
        """Newton usa entradas vacías, campos condicionales y proveedor real de derivada."""
        self.control.abrirTema('Numéricos')
        self.control.seleccionar('num_newton')
        for campo in ('funcion', 'x0', 'derivada', 'h'):
            self.assertEqual(self.control.sesion.parametros[campo], '')
        self.assertNotIn('h', [c['clave'] for c in self.control.formulario['camposB']])
        self.control.editarCampo('modo_derivada', 'numerica')
        self.app.processEvents()
        self.assertNotIn('derivada', [c['clave'] for c in self.control.formulario['camposA']])
        self.assertTrue(self.buscar_control('campo_h').isVisible())
        for campo, valor in dict(funcion='exp(-x)-x', x0='0', h='1e-5').items():
            self.control.editarCampo(campo, valor)
        self.control.calcular()
        self.esperar_calculo()
        self.assertTrue(self.control.sesion.presentacion.calculo.datos['convergio'])
        self.assertAlmostEqual(self.control.sesion.presentacion.calculo.valor, .5671432904, places=9)
        self.assertIn('Raíz aproximada', self.control.resultado['resumen'])
        self.control.editarCampo('tolerancia_f', '0')
        self.control.calcular()
        self.esperar_calculo()
        self.assertFalse(self.control.estado['vigente'])
        self.assertTrue(self.control.estado['error'])

    def test_newton_pasos_tabla_grafica_seleccion_y_exportacion(self):
        """Los controles reales usan filas guardadas, sin recalcular ni perder datos."""
        from copy import deepcopy
        from unittest.mock import patch
        from PySide6.QtCore import QMetaObject
        self.control.abrirTema('Numéricos')
        self.control.seleccionar('num_newton')
        self.control.cargarEjemplo('')
        self.control.calcular()
        self.esperar_calculo()
        original = deepcopy(self.control.sesion.capturar())
        c = self.control.sesion.presentacion.calculo
        self.assertEqual(self.control.previa['total'], c.datos['iteraciones'])
        self.assertEqual(len(self.control.resultado['pasos']), len(c.pasos))
        self.control.reproducir()
        self.assertEqual(self.control.reloj.interval(), 2000)
        self.control.verGrafica(False)
        self.app.processEvents()
        self.assertFalse(self.control.reloj.isActive())
        self.assertFalse(self.control._fuente_grafica.imagen.isNull())
        boton = self.buscar_control('tangenteSiguiente')
        self.assertTrue(boton.isVisible())
        self.assertTrue(boton.isEnabled())
        with patch('interfaz.qt.catalogo.ejecutar', side_effect=AssertionError('No recalcular')):
            self.assertTrue(QMetaObject.invokeMethod(boton, 'clicked'))
            self.app.processEvents()
            self.assertEqual(self.control.graficaNewton['indice'], 1)
            self.control.seleccionarIteracionGrafica(99999)
            self.assertEqual(self.control.graficaNewton['indice'], c.datos['iteraciones'] - 1)
            self.control.verGrafica(True)
            self.app.processEvents()
        self.assertEqual(self.control.sesion.capturar(), original)
        with tempfile.TemporaryDirectory() as carpeta:
            destino = Path(carpeta) / 'newton.png'
            with patch('interfaz.qt.controlador.QFileDialog.getSaveFileName', return_value=(str(destino), 'PNG')):
                self.control.guardarGrafica()
            self.assertTrue(destino.read_bytes().startswith(b'\x89PNG'))
        self.ventana.setProperty('vista', 'pasos')
        self.app.processEvents()
        tabla = self.buscar_control('mostrarTabla')
        self.assertTrue(tabla.isVisible())
        self.assertTrue(QMetaObject.invokeMethod(tabla, 'clicked'))
        self.app.processEvents()
        self.assertEqual(tabla.property('text'), 'Volver a los pasos')
        self.assertTrue(QMetaObject.invokeMethod(tabla, 'clicked'))
        self.control.reiniciar()
        self.assertEqual(self.control.previa['indice'], 0)

    def test_newton_comparacion_solo_biseccion_vigente_misma_funcion(self):
        """La comparación no usa datos obsoletos, otra función ni unidades porcentuales."""
        self.control.seleccionar('num_biseccion')
        for campo, valor in dict(funcion='exp(-x)-x', a='0', b='1').items():
            self.control.editarCampo(campo, valor)
        self.control.calcular()
        self.esperar_calculo()
        self.control.seleccionar('num_newton')
        self.control.cargarEjemplo('')
        self.control.calcular()
        self.esperar_calculo()
        self.assertTrue(self.control.graficaNewton['comparable'])
        self.control.verGrafica(False)
        self.control.compararBiseccionGrafica(True)
        self.assertTrue(self.control.graficaNewton['comparar'])
        self.control.editarCampo('criterio', 'porcentual')
        self.control.calcular()
        self.esperar_calculo()
        self.assertFalse(self.control.graficaNewton['comparable'])
        self.control.compararBiseccionGrafica(True)
        self.assertFalse(self.control.graficaNewton['comparar'])
        self.control.editarCampo('criterio', 'absoluto')
        self.control.calcular()
        self.esperar_calculo()
        self.control.seleccionar('num_biseccion')
        self.control.editarCampo('funcion', 'x')
        self.control.seleccionar('num_newton')
        self.assertFalse(self.control.graficaNewton['comparable'])

    def test_newton_guardar_reutilizar_navegar_y_deshacer(self):
        """Guarda el escalar, lo reutiliza en bisección y conserva la sesión al limpiar."""
        self.control.abrirTema('Numéricos')
        self.control.seleccionar('num_newton')
        self.control.cargarEjemplo('')
        self.control.calcular()
        self.esperar_calculo()
        raiz = self.control.sesion.presentacion.calculo.valor
        self.control.guardar('resultado', 'Mi raíz Newton', 'N₁', '')
        registro = self.control.guardados[0]
        self.assertAlmostEqual(float(registro['valor']), raiz)
        self.control.seleccionar('num_biseccion')
        self.control.usarGuardado(registro['id'], False, 'a')
        self.assertAlmostEqual(float(self.control.sesion.parametros['a']), raiz)
        self.control.seleccionar('num_newton')
        self.assertTrue(self.control.estado['vigente'])
        self.assertEqual(self.control.sesion.parametros['funcion'], 'exp(-x)-x')
        self.control.limpiar()
        self.assertEqual(self.control.clave, 'num_newton')
        self.assertEqual(self.control.sesion.parametros['funcion'], '')
        self.control.deshacer()
        self.assertTrue(self.control.estado['vigente'])
        self.assertEqual(self.control.sesion.presentacion.calculo.valor, raiz)

    def test_newton_ciclo_y_dominio_no_se_presentan_como_raiz(self):
        """Los fallos conservan diagnóstico; sin punto evaluado no se guarda un escalar."""
        self.control.abrirTema('Numéricos')
        self.control.seleccionar('num_newton')
        self.control.cargarEjemplo('Ciclo cúbico')
        self.control.calcular()
        self.esperar_calculo()
        self.assertFalse(self.control.sesion.presentacion.calculo.datos['convergio'])
        self.assertIn('Última aproximación', self.control.resultado['resumen'])
        self.assertIn('ciclo', self.control.estado['mensaje'])
        for campo, valor in dict(funcion='log(x)', derivada='1/x', x0='-1').items():
            self.control.editarCampo(campo, valor)
        self.control.calcular()
        self.esperar_calculo()
        self.assertIsNone(self.control.sesion.presentacion.calculo.valor)
        self.control.guardar('resultado', '', '', '')
        self.assertEqual(self.control.guardados, [])
        self.assertIn('No hay una aproximación', self.control.estado['mensaje'])

    def test_teclado_qml_edicion_deshacer_y_limpiar(self):
        """Los botones QML escriben en el cursor y deshacer conserva el método."""
        from PySide6.QtCore import QObject, QMetaObject
        self.control.abrirTema('Numéricos')
        self.app.processEvents()
        entrada = self.buscar_control('campo_funcion')
        self.assertIsNotNone(entrada)
        boton = self.buscar_control('signo_x²')
        self.assertTrue(QMetaObject.invokeMethod(boton, 'clicked'))
        self.assertEqual(self.control.sesion.parametros['funcion'], 'x^2')
        self.assertEqual(entrada.property('cursorPosition'), 3)
        self.assertTrue(QMetaObject.invokeMethod(self.buscar_control('signo_−'), 'clicked'))
        self.assertEqual(self.control.sesion.parametros['funcion'], 'x^2-')
        self.control.deshacer()
        self.assertEqual(self.control.sesion.parametros['funcion'], 'x^2')
        self.control.editarCampo('funcion', 'x^2-2')
        self.control.editarCampo('a', '1')
        self.control.editarCampo('b', '2')
        self.control.calcular()
        self.esperar_calculo()
        self.assertTrue(self.control.estado['vigente'])
        self.assertEqual(self.control.previa['indice'], 0)
        self.assertEqual(self.control.reloj.interval(), 2000)
        self.control.reproducir()
        self.assertTrue(self.control.reloj.isActive())
        self.control.editarCampo('a', '0')
        self.assertFalse(self.control.reloj.isActive())
        self.assertFalse(self.control.estado['vigente'])
        self.control.deshacer()
        self.assertTrue(self.control.estado['vigente'])
        self.control.limpiar()
        self.assertEqual(self.control.clave, 'num_biseccion')
        self.assertEqual(self.control.sesion.parametros['funcion'], '')

    def test_previa_funcion_delimita_exponente(self):
        """El número que sigue al operador vuelve a la línea normal."""
        from PySide6.QtCore import QMetaObject
        self.control.abrirTema('Numéricos')
        self.app.processEvents()
        entrada = self.buscar_control('campo_funcion')
        previa = self.buscar_control('previaFuncion')
        self.assertTrue(QMetaObject.invokeMethod(self.buscar_control('signo_xⁿ'), 'clicked'))
        self.assertEqual(entrada.property('text'), 'x^')
        entrada.setProperty('text', 'x^123')
        entrada.setProperty('cursorPosition', 5)
        self.assertTrue(QMetaObject.invokeMethod(self.buscar_control('signo_+'), 'clicked'))
        entrada.setProperty('text', entrada.property('text') + '45')
        self.assertEqual(previa.property('text'), 'x¹²³+45')
        entrada.setProperty('text', 'x^12.5 + x^-2 + 123456789')
        self.assertEqual(previa.property('text'), 'x^12.5 + x⁻² + 123456789')

    def test_tabla_se_abre_solo_desde_todos_los_pasos(self):
        """La tabla empieza plegada y el botón aparece donde hay filas."""
        from PySide6.QtCore import QMetaObject
        self.control.abrirTema('Numéricos')
        self.control.cargarEjemplo('')
        self.control.calcular()
        self.esperar_calculo()
        boton = self.buscar_control('mostrarTabla')
        tabla = self.buscar_control('tablaPasos')
        pasos = self.buscar_control('listaPasos')
        self.assertFalse(boton.isVisible())
        self.ventana.setProperty('vista', 'pasos')
        self.app.processEvents()
        self.assertTrue(boton.isVisible())
        self.assertFalse(tabla.isVisible())
        alto_pasos = pasos.height()
        self.assertTrue(pasos.isVisible())
        self.assertTrue(QMetaObject.invokeMethod(boton, 'clicked'))
        self.app.processEvents()
        self.assertTrue(tabla.isVisible())
        self.assertFalse(pasos.isVisible())
        self.assertGreater(alto_pasos, 0)
        self.assertAlmostEqual(tabla.height(), alto_pasos, delta=1)
        self.assertEqual(boton.property('text'), 'Volver a los pasos')
        self.assertTrue(QMetaObject.invokeMethod(boton, 'clicked'))
        self.assertFalse(tabla.isVisible())
        self.assertTrue(pasos.isVisible())
        self.assertTrue(QMetaObject.invokeMethod(boton, 'clicked'))
        self.ventana.setProperty('vista', 'calculadora')
        self.app.processEvents()
        self.ventana.setProperty('vista', 'pasos')
        self.app.processEvents()
        self.assertFalse(tabla.isVisible())
        self.control.seleccionar('num_errores')
        self.app.processEvents()
        self.assertFalse(boton.isVisible())

    def test_copiar_ejercicio_guardado_y_abrir_la_copia(self):
        """Desde la calculadora se puede cargar un guardado y recuperar una copia de Biblioteca."""
        from PySide6.QtCore import QMetaObject
        self.control.abrirTema('Numéricos')
        self.control.cargarEjemplo('')
        self.control.calcular()
        self.esperar_calculo()
        self.control.guardar('ejercicio', 'Bisección de práctica', '≈x', 'Ejemplo de clase')
        original = self.control.guardados[0]
        self.control.abrirTema('Matrices')
        cargar = self.buscar_control('cargarEjercicioGuardado')
        self.assertTrue(cargar.isVisible())
        self.assertTrue(QMetaObject.invokeMethod(cargar, 'clicked'))
        self.app.processEvents()
        self.assertTrue(QMetaObject.invokeMethod(self.buscar_control('confirmarCargaEjercicio'), 'clicked'))
        self.esperar_calculo()
        self.assertEqual(self.control.clave, 'num_biseccion')
        self.assertTrue(self.control.estado['vigente'])
        self.ventana.setProperty('pagina', 'biblioteca')
        self.app.processEvents()
        boton = self.buscar_control('copiarEjercicio')
        self.assertFalse(boton.isVisible())
        fila = self.buscar_control('registro_' + original['id'])
        self.assertTrue(QMetaObject.invokeMethod(fila, 'clicked'))
        self.assertTrue(boton.isVisible())
        self.assertTrue(QMetaObject.invokeMethod(boton, 'clicked'))
        copia, guardado = self.control.guardados
        self.assertEqual(guardado, original)
        self.assertNotEqual(copia['id'], original['id'])
        self.assertEqual(copia['nombre'], 'Bisección de práctica (copia)')
        for campo in ('parametros', 'entradas', 'pasos', 'notas', 'simbolo'):
            self.assertEqual(copia[campo], original[campo])

        self.control.editarCampo('funcion', 'x^2-2')
        volver = self.buscar_control('volverDesdeBiblioteca')
        self.assertTrue(volver.isVisible())
        self.assertTrue(QMetaObject.invokeMethod(volver, 'clicked'))
        self.assertEqual(self.ventana.property('pagina'), 'calculadora')
        segunda = self.control.copiarEjercicio(original['id'])
        self.assertEqual(segunda['nombre'], 'Bisección de práctica (copia 2)')
        self.assertTrue(QMetaObject.invokeMethod(cargar, 'clicked'))
        self.app.processEvents()
        lista = self.buscar_control('ejerciciosParaCargar')
        self.assertEqual(lista.property('count'), 3)
        self.assertEqual(lista.property('currentIndex'), 1)
        self.assertTrue(QMetaObject.invokeMethod(self.buscar_control('confirmarCargaEjercicio'), 'clicked'))
        self.esperar_calculo()
        self.assertTrue(self.control.estado['vigente'])
        self.assertEqual(self.ventana.property('pagina'), 'calculadora')
        self.assertEqual(self.control.sesion.parametros['funcion'], copia['parametros']['funcion'])

    def test_guardar_solo_resultado_y_cargarlo_en_el_destino_elegido(self):
        """Una raíz y una matriz se reutilizan desde la lista sin abrir el ejercicio original."""
        from PySide6.QtCore import QObject, QMetaObject
        from interfaz.biblioteca import Biblioteca

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / 'biblioteca.json'
            self.control.biblioteca = Biblioteca(ruta)
            self.control.abrirTema('Numéricos')
            self.control.cargarEjemplo('')
            self.control.calcular()
            self.esperar_calculo()
            valor = str(self.control.sesion.presentacion.calculo.valor)
            guardar = self.buscar_control('guardarResultado')
            self.assertTrue(QMetaObject.invokeMethod(guardar, 'clicked'))
            dialogo = self.ventana.findChild(QObject, 'guardarDialogo')
            self.assertTrue(QMetaObject.invokeMethod(dialogo, 'accept'))
            resultado = Biblioteca(ruta).listar()[0]
            self.assertEqual(resultado['tipo'], 'resultado')
            self.assertEqual(resultado['valor'], valor)
            self.assertEqual(resultado['pasos'], [])
            self.assertNotIn('parametros', resultado)

            self.control.seleccionar('num_errores')
            cargar = self.buscar_control('cargarEjercicioGuardado')
            self.assertTrue(QMetaObject.invokeMethod(cargar, 'clicked'))
            self.app.processEvents()
            destino = self.buscar_control('destinoResultadoGuardado')
            destino.setProperty('currentIndex', 1)
            self.assertTrue(QMetaObject.invokeMethod(self.buscar_control('confirmarCargaEjercicio'), 'clicked'))
            self.assertEqual(self.control.clave, 'num_errores')
            self.assertEqual(self.control.sesion.parametros['aproximado'], valor)

            self.control.abrirTema('Matrices')
            self.control.cargarEjemplo('Con fracciones')
            self.control.calcular()
            self.esperar_calculo()
            self.assertTrue(QMetaObject.invokeMethod(guardar, 'clicked'))
            self.assertTrue(QMetaObject.invokeMethod(dialogo, 'accept'))
            matriz = Biblioteca(ruta).listar()[0]['resultado']
            self.control.limpiar()
            self.assertTrue(QMetaObject.invokeMethod(cargar, 'clicked'))
            self.app.processEvents()
            self.buscar_control('destinoResultadoGuardado').setProperty('currentIndex', 1)
            self.assertTrue(QMetaObject.invokeMethod(self.buscar_control('confirmarCargaEjercicio'), 'clicked'))
            self.assertEqual(self.control.sesion.entradas['B'], matriz)
            self.assertEqual(self.control.sesion.entradas['A'][0][0], '')

    def test_biblioteca_exacta_reapertura_y_promocion_sin_duplicar_historial(self):
        """Se mantiene el formato previo y el registro no duplica un cálculo recuperado."""
        from interfaz.biblioteca import Biblioteca
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / 'biblioteca.json'
            self.control.biblioteca = Biblioteca(ruta)
            self.control.abrirTema('Matrices')
            self.control.cargarEjemplo('Con fracciones')
            self.control.calcular()
            self.esperar_calculo()
            self.control.guardar('ejercicio', 'Mi suma', 'Σ₁', 'Exacta')
            self.control.guardar('resultado', '', '', '')
            self.assertEqual(len(self.control.guardados), 2)
            self.assertEqual(len(self.control.historial), 1)
            almacen = Biblioteca(ruta)
            self.assertEqual(almacen.listar()[1]['resultado'][0][0], '1/2')
            ejercicio = self.control.guardados[1]
            self.control.limpiar()
            self.control.abrirGuardado(ejercicio['id'], False)
            self.esperar_calculo()
            self.assertEqual(len(self.control.historial), 1)
            self.assertTrue(self.control.estado['vigente'])
            self.control.usarGuardado(self.control.guardados[0]['id'], False, 'A')
            self.assertEqual(self.control.sesion.entradas['A'][0][0], '1/2')
            self.assertFalse(self.control.estado['vigente'])

    def test_redimensionar_copiar_pegar_y_ventana_minima(self):
        """La matriz vacía se edita y las acciones permanecen dentro de la ventana."""
        from PySide6.QtCore import QObject, QPointF
        from PySide6.QtGui import QGuiApplication
        self.control.abrirTema('Matrices')
        self.ventana.setWidth(1100)
        self.ventana.setHeight(760)
        self.app.processEvents()
        boton = self.ventana.findChild(QObject, 'calcular')
        punto = boton.mapToScene(QPointF())
        self.assertGreaterEqual(punto.y(), 0)
        self.assertLessEqual(punto.y() + boton.height(), 760)
        self.control.redimensionar('A', 3, 2)
        self.assertEqual(self.control.sesion.entradas['A'], [['', ''], ['', ''], ['', '']])
        QGuiApplication.clipboard().setText('1/3 2\n3 4')
        self.control.pegarMatriz('A')
        self.assertEqual(self.control.sesion.entradas['A'][0][0], '1/3')
        self.control.copiarMatriz('A')
        self.assertIn('1/3', QGuiApplication.clipboard().text())
        self.control.deshacer()
        self.assertEqual(len(self.control.sesion.entradas['A']), 3)

    def test_grafica_y_pdf_reutilizan_datos_y_exportadores(self):
        """La figura se entrega a QML y el PDF conserva todos los pasos del ejercicio."""
        from unittest.mock import patch
        self.control.abrirTema('Numéricos')
        self.control.cargarEjemplo('cos(x)-x')
        self.control.calcular()
        self.esperar_calculo()
        imagenes = []
        self.control.graficaLista.connect(imagenes.append)
        self.control.verGrafica(True)
        self.assertEqual(len(imagenes), 1)
        self.assertFalse(self.control._fuente_grafica.imagen.isNull())
        self.app.processEvents()
        with tempfile.TemporaryDirectory() as carpeta:
            destino = Path(carpeta) / 'ejercicio.pdf'
            with patch('interfaz.qt.controlador.QFileDialog.getSaveFileName', return_value=(str(destino), 'PDF')):
                self.control.exportar('', False)
            self.assertTrue(destino.read_bytes().startswith(b'%PDF-1.4'))
        self.assertIn('cos(x)-x', self.control.sesion.registro()['parametros']['funcion'])
