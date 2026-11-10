"""Comprueba temporizadores y navegación sin depender de una pantalla.

Tema: reproducción cancelable del procedimiento visual.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import unittest

from interfaz.recorrido import ReproductorPasos


class PruebasRecorrido(unittest.TestCase):
    """Verifica pausa, finalización y reemplazo con un reloj controlado."""

    def setUp(self):
        """Prepara un reloj simulado y un registro de pasos visibles."""
        self.tareas = {}
        self.vistos = []
        self.demoras = []
        self.numero = 0
        self.player = ReproductorPasos(self.programar, self.tareas.pop,
                                      lambda paso, indice, total: self.vistos.append(paso),
                                      lambda: 350, lambda: None)
        self.player.preparar(["uno", "dos", "tres"])

    def programar(self, demora, callback):
        """Registra una tarea pendiente sin ejecutar el tiempo automáticamente."""
        self.numero += 1
        self.demoras.append(demora)
        self.tareas[self.numero] = callback
        return self.numero

    def ejecutar_pendiente(self):
        """Ejecuta el evento pendiente como lo haría el bucle de la ventana."""
        clave = next(iter(self.tareas))
        self.tareas.pop(clave)()

    def test_no_hay_movimiento_hasta_que_se_pida(self):
        """Preparar pasos no inicia una animación ni consume temporizadores."""
        self.assertEqual(self.vistos, [])
        self.assertFalse(self.tareas)

    def test_pausar_y_reanudar_no_salta_pasos(self):
        """La pausa cancela el reloj y reanudar continúa desde el paso siguiente."""
        self.player.reproducir()
        self.assertEqual(self.vistos, ["uno"])
        self.player.pausar()
        self.assertFalse(self.tareas)
        self.player.reproducir()
        self.ejecutar_pendiente()
        self.assertEqual(self.vistos, ["uno", "dos", "tres"])
        self.assertFalse(self.player.activo)
        self.assertFalse(self.tareas)
        self.assertEqual(self.demoras, [350, 350])

    def test_no_se_duplican_temporizadores(self):
        """Reproducir dos veces no crea dos eventos para el mismo recorrido."""
        self.player.reproducir()
        self.player.reproducir()
        self.assertEqual(len(self.tareas), 1)
        self.player.siguiente()
        self.assertEqual(self.vistos, ["uno", "dos"])
        self.assertFalse(self.tareas)

    def test_cambiar_datos_cancela_la_secuencia_anterior(self):
        """Reemplazar la secuencia invalida lo pendiente antes de mostrar otros datos."""
        self.player.reproducir()
        self.player.preparar(["nuevo"])
        self.assertFalse(self.tareas)
        self.player.siguiente()
        self.assertEqual(self.vistos, ["uno", "nuevo"])

    def test_ver_todo_y_reiniciar(self):
        """Completar elimina el reloj y reproducir de nuevo arranca por el primer paso."""
        self.player.reproducir()
        self.player.completar()
        self.assertEqual(self.vistos, ["uno", "tres"])
        self.assertFalse(self.tareas)
        self.player.reproducir()
        self.assertEqual(self.vistos[-1], "uno")

    def test_secuencia_vacia(self):
        """Los controles no hacen nada cuando no hay pasos disponibles."""
        self.player.preparar([])
        self.player.reproducir()
        self.player.siguiente()
        self.player.completar()
        self.assertFalse(self.tareas)
        self.assertEqual(self.vistos, [])

    def test_retroceder_y_reiniciar_pausan_sin_perder_posicion(self):
        """Retroceder y reiniciar cancelan el reloj y respetan el primer paso."""
        self.player.reproducir()
        self.ejecutar_pendiente()
        self.player.anterior()
        self.assertEqual(self.vistos[-1], "uno")
        self.assertFalse(self.tareas)
        self.player.anterior()
        self.assertEqual(self.player.indice, 0)
        self.player.reproducir()
        self.player.reiniciar()
        self.assertEqual(self.player.indice, 0)
        self.assertFalse(self.player.activo)
        self.assertFalse(self.tareas)

    def test_etapas_no_pierden_las_celdas_de_origen(self):
        """Una celda puede tener varias etapas navegables y cancelables."""
        self.player.preparar(['celda'], ['origen', 'operacion', 'destino'])
        self.assertEqual(self.player.pasos, ('celda',))
        self.player.reproducir()
        self.ejecutar_pendiente()
        self.player.anterior()
        self.assertEqual(self.vistos[-1], 'origen')
        self.assertFalse(self.tareas)
        self.player.completar()
        self.assertEqual(self.vistos[-1], 'destino')
