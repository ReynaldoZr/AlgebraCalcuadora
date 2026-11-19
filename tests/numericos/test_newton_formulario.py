"""Comprueba el catálogo y persistencia real de Newton desde el formulario.

Tema: issue 36, parámetros, resultados y lectura segura de expresiones.
Elaboración: equipo 9, con apoyo de IA.
"""

from pathlib import Path
import tempfile
import unittest

from interfaz.biblioteca import Biblioteca
from interfaz.metodos_numericos import ejecutar_numerico, opciones_campo, parametros_defecto
from interfaz.qt.sesion import Sesion


class PruebasFormularioNewton(unittest.TestCase):
    """Verifica contratos observables sin acceder a la biblioteca personal."""

    def test_ejercicio_numerico_se_reabre_con_los_mismos_parametros(self):
        """El esquema existente conserva modo, h y tolerancias sin guardar callables."""
        sesion = Sesion('num_newton')
        sesion.cargar_ejemplo()
        sesion.parametros.update(modo_derivada='numerica', h='1e-5')
        sesion.calcular()
        original = sesion.presentacion.calculo.valor
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / 'biblioteca.json'
            Biblioteca(ruta).guardar(sesion.registro(), 'Newton central')
            guardado = Biblioteca(ruta).listar()[0]
        self.assertEqual(guardado['parametros']['h'], '1e-5')
        self.assertEqual(guardado['parametros']['tolerancia_f'], '1e-8')
        copia = Sesion(guardado['operacion'])
        copia.parametros.update(guardado['parametros'])
        copia.calcular()
        self.assertEqual(copia.presentacion.calculo.valor, original)

    def test_expresiones_invalidas_no_evitan_el_analizador_seguro(self):
        """Ambos campos de expresión usan el analizador existente, también la derivada."""
        for nombre in ('funcion', 'derivada'):
            p = dict(parametros_defecto('num_newton'))
            p[nombre] = "__import__('os')"
            with self.subTest(campo=nombre), self.assertRaises(ValueError):
                ejecutar_numerico('num_newton', p)

    def test_criterios_de_newton_no_cambian_los_de_biseccion(self):
        """Cada método conserva sus magnitudes y su conjunto de opciones."""
        self.assertEqual(opciones_campo('num_newton', 'criterio'), ('absoluto', 'porcentual'))
        self.assertEqual(opciones_campo('num_biseccion', 'criterio'), ('intervalo', 'porcentual'))


if __name__ == '__main__':
    unittest.main()
