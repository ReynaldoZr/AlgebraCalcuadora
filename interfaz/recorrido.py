"""Coordina pasos visuales con un temporizador proporcionado por la ventana.

Tema: explicación de operaciones ya calculadas, sin repetir algoritmos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""


class ReproductorPasos:
    """Controla reproducción, pausa y avance manual de una secuencia."""

    def __init__(self, programar, cancelar, mostrar, demora, informar):
        """Recibe callbacks de temporizador, dibujo, velocidad y estado."""
        self.programar = programar
        self.cancelar = cancelar
        self.mostrar = mostrar
        self.demora = demora
        self.informar = informar
        self.pasos = ()
        self.indice = -1
        self.activo = False
        self.pendiente = None

    def preparar(self, pasos):
        """Cancela la secuencia anterior y prepara una nueva sin reproducirla."""
        self.pausar()
        self.pasos = tuple(pasos)
        self.indice = -1
        self.informar()

    def pausar(self):
        """Detiene el temporizador sin perder el paso actual."""
        self.activo = False
        if self.pendiente is not None:
            self.cancelar(self.pendiente)
            self.pendiente = None
        self.informar()

    def siguiente(self):
        """Muestra un paso más manualmente, sin dejar un temporizador activo."""
        self.pausar()
        self._avanzar()
        self.informar()

    def anterior(self):
        """Retrocede un paso en pausa sin programar otro temporizador."""
        self.pausar()
        if self.pasos and self.indice > 0:
            self.indice -= 1
            self.mostrar(self.pasos[self.indice], self.indice, len(self.pasos))
        self.informar()

    def reiniciar(self):
        """Muestra el primer paso y deja la reproducción detenida."""
        self.pausar()
        if self.pasos:
            self.indice = 0
            self.mostrar(self.pasos[0], 0, len(self.pasos))
        self.informar()

    def _avanzar(self):
        """Presenta el siguiente dato de la secuencia si todavía queda alguno."""
        if self.indice + 1 < len(self.pasos):
            self.indice += 1
            self.mostrar(self.pasos[self.indice], self.indice, len(self.pasos))

    def reproducir(self):
        """Inicia o reanuda; al llegar al final permite volver a empezar."""
        if self.activo or not self.pasos:
            return
        if self.indice == len(self.pasos) - 1:
            self.indice = -1
        self.activo = True
        self._tick()

    def _tick(self):
        """Avanza sin bloquear la ventana y programa únicamente el próximo paso."""
        self.pendiente = None
        if not self.activo:
            return
        self._avanzar()
        if self.indice < len(self.pasos) - 1:
            self.pendiente = self.programar(self.demora(), self._tick)
        else:
            self.activo = False
        self.informar()

    def completar(self):
        """Detiene la reproducción y muestra el último paso de la secuencia."""
        self.pausar()
        if self.pasos:
            self.indice = len(self.pasos) - 1
            self.mostrar(self.pasos[self.indice], self.indice, len(self.pasos))
        self.informar()
