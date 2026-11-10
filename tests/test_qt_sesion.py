"""Comprueba la sesión nueva sin depender de una pantalla ni de widgets.

Tema: exactitud, todos los métodos y compatibilidad de guardados existentes.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction
import subprocess
import sys
import unittest

from interfaz.biblioteca import validar_registro
from interfaz.qt.catalogo import CATALOGO, ejecutar
from interfaz.qt.presentacion import matriz_visual, token_visual
from interfaz.qt.sesion import Sesion


class PruebasSesionQt(unittest.TestCase):
    """Exige los mismos contratos matemáticos y sesiones vacías al comenzar."""

    def test_entrada_vacia_fracciones_y_deshacer_sin_cambiar_metodo(self):
        """Una edición o limpieza se revierte sin convertir fracciones en float."""
        sesion = Sesion('restar')
        self.assertTrue(all(v == '' for m in sesion.entradas.values() for f in m for v in f))
        sesion.cargar_ejemplo('Con fracciones')
        sesion.calcular()
        self.assertEqual(sesion.presentacion.matriz[0][0], Fraction(1, 6))
        validar_registro(sesion.registro())
        sesion.limpiar()
        self.assertEqual(sesion.clave, 'restar')
        self.assertIsNone(sesion.presentacion)
        sesion.deshacer()
        self.assertTrue(sesion.vigente)
        self.assertEqual(sesion.presentacion.matriz[0][0], Fraction(1, 6))

    def test_catalogo_exacto_completo_y_guardados_validos(self):
        """Cada método exacto ofrece un ejemplo y un procedimiento guardable."""
        for clave in CATALOGO:
            with self.subTest(clave=clave):
                sesion = Sesion(clave)
                sesion.cargar_ejemplo()
                sesion.calcular()
                self.assertTrue(sesion.vigente)
                self.assertTrue(sesion.presentacion.calculo.pasos)
                validar_registro(sesion.registro())

    def test_error_no_borra_ultimo_resultado_y_lu_no_pivotea(self):
        """Se conserva la respuesta anterior y no se presenta PA=LU como A=LU."""
        sesion = Sesion('lu_factorizar')
        sesion.cargar_ejemplo()
        sesion.calcular()
        anterior = sesion.presentacion
        sesion.cargar_ejemplo('Requiere PA=LU')
        with self.assertRaises(ValueError):
            sesion.calcular()
        self.assertIs(sesion.presentacion, anterior)
        self.assertFalse(sesion.vigente)

    def test_producto_conserva_todos_los_pares_y_simplificaciones(self):
        """La vista completa conserva la explicación que ya construye el proyecto."""
        sesion = Sesion('multiplicar')
        sesion.cargar_ejemplo('Con fracciones')
        sesion.calcular()
        pasos = sesion.presentacion.calculo.pasos
        self.assertGreater(len(pasos), len(sesion.presentacion.matriz) * len(sesion.presentacion.matriz[0]))
        self.assertTrue(any('denominador' in p.titulo.lower() for p in pasos))
        self.assertTrue(any(e.par is not None for e in sesion.breves))

    def test_tokens_exactos_no_pierden_cifras(self):
        """QML recibe texto en lugar de números JavaScript para el álgebra exacta."""
        numero = Fraction(123456789012345678901, 7)
        token = token_visual(numero)
        self.assertEqual(Fraction(int(token['arriba']), int(token['abajo'])), numero)
        self.assertEqual(matriz_visual([[Fraction(1, 3)]])[0][0], dict(arriba='1', abajo='3'))
        self.assertEqual(token_visual(('1 + 2', 6)), dict(arriba='1 + 2', abajo='6'))

    def test_consola_y_lanzadores_no_importan_qt_ni_numpy(self):
        """Qt sigue siendo opcional para importar la consola y los lanzadores."""
        codigo = 'import sys; import main, gui, gui_qt; assert not any(k in sys.modules for k in ("PySide6", "numpy", "scipy", "matplotlib"))'
        proceso = subprocess.run([sys.executable, '-c', codigo], capture_output=True, text=True, timeout=20)
        self.assertEqual(proceso.returncode, 0, proceso.stderr)
