"""Verifica limpieza y finalización del desvanecimiento con un reloj controlado.

Tema: cancelación de capas y temporizadores al navegar y cerrar.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

try:
    import tkinter as tk
    from interfaz.transicion import TransicionVistas
except ImportError:
    tk = None


@unittest.skipIf(tk is None, 'Se necesita Tkinter para importar la transición.')
class PruebasTransicion(unittest.TestCase):
    """Usa capas simuladas para probar el ciclo sin capturar la pantalla."""

    def setUp(self):
        """Prepara una raíz visible, capas registradas y un reloj manual."""
        self.tareas = {}
        self.numero = 0
        self.demoras = []
        self.raiz = Mock()
        self.raiz.winfo_viewable.return_value = True
        self.raiz.winfo_width.return_value = 1120
        self.raiz.winfo_height.return_value = 760
        self.raiz.winfo_rootx.return_value = 20
        self.raiz.winfo_rooty.return_value = 40
        self.raiz.after.side_effect = self.programar
        self.raiz.after_idle.side_effect = lambda funcion: self.programar(0, funcion)
        self.raiz.after_cancel.side_effect = self.tareas.pop
        self.capas = []
        self.fabrica = patch('interfaz.transicion.tk.Toplevel', side_effect=self.crear_capa)
        self.fabrica.start()
        self.addCleanup(self.fabrica.stop)
        self.transicion = TransicionVistas(self.raiz, Mock())
        self.addCleanup(self.transicion.cancelar)

    def crear_capa(self, *args, **kwargs):
        """Registra una capa distinta para comprobar que ninguna queda huérfana."""
        capa = Mock()
        self.capas.append(capa)
        return capa

    def programar(self, demora, funcion):
        """Guarda un callback cancelable sin esperar tiempo real."""
        self.numero += 1
        self.demoras.append(demora)
        self.tareas[self.numero] = funcion
        return self.numero

    def completar(self):
        """Ejecuta el reloj hasta que la transición haya terminado."""
        while self.tareas:
            clave = next(iter(self.tareas))
            self.tareas.pop(clave)()

    def test_desvanece_solo_la_capa_y_la_retira(self):
        """La capa pierde opacidad y se destruye dentro del intervalo breve."""
        self.transicion.iniciar()
        self.completar()
        capa = self.capas[0]
        alfas = [c.args[1] for c in capa.attributes.call_args_list]
        self.assertEqual(alfas[0], 1.0)
        self.assertEqual(alfas[-1], 0)
        self.assertEqual(alfas, sorted(alfas, reverse=True))
        self.assertTrue(150 <= sum(self.demoras) <= 200)
        self.assertIsNone(self.transicion.capa)
        capa.destroy.assert_called_once()
        self.raiz.attributes.assert_not_called()

    def test_repetir_y_cerrar_eliminan_todas_las_capas(self):
        """Cambios rápidos reemplazan la capa y el cierre cancela el último evento."""
        self.transicion.iniciar()
        anterior = self.capas[0]
        self.transicion.iniciar()
        anterior.destroy.assert_called_once()
        self.assertEqual(len(self.tareas), 1)
        self.transicion._al_destruir(SimpleNamespace(widget=self.raiz))
        self.assertFalse(self.tareas)
        self.assertIsNone(self.transicion.capa)
        self.capas[1].destroy.assert_called_once()

    def test_sin_pantalla_visible_no_crea_capa(self):
        """Una ventana retirada o minimizada no inicia un desvanecimiento."""
        self.raiz.winfo_viewable.return_value = False
        self.transicion.iniciar()
        self.assertFalse(self.capas)
        self.assertFalse(self.tareas)

    def test_sin_transparencia_retira_la_capa_sin_bloquear(self):
        """Si la plataforma rechaza alpha, el cambio limpio sigue disponible."""
        capa = Mock()
        capa.attributes.side_effect = tk.TclError('alpha no disponible')
        self.fabrica.stop()
        with patch('interfaz.transicion.tk.Toplevel', return_value=capa):
            self.transicion.iniciar()
        self.assertIsNone(self.transicion.capa)
        self.assertFalse(self.tareas)
        capa.destroy.assert_called_once()
