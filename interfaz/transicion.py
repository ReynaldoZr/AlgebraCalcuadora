"""Revela una vista ya preparada con un desvanecimiento breve.

Tema: transición de pestañas sin mostrar su construcción ni bloquear Tk.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk

DURACION_MS = 180
FOTOGRAMAS = 9


class TransicionVistas:
    """Cubre el redibujado con una capa transitoria y después la desvanece."""

    def __init__(self, raiz, tema):
        """Asocia la transición al cliente de esta ventana, sin tocar su opacidad."""
        self.raiz = raiz
        self.tema = tema
        self.capa = None
        self.pendiente = None
        raiz.bind("<Configure>", self._redimensionar, add="+")
        raiz.bind("<Destroy>", self._al_destruir, add="+")

    def iniciar(self):
        """Oculta el redibujado y espera al siguiente ciclo de presentación."""
        self.cancelar()
        if not self.raiz.winfo_viewable():
            return
        try:
            self.capa = tk.Toplevel(self.raiz, takefocus=False)
            self.capa.withdraw()
            self.capa.overrideredirect(True)
            self.capa.transient(self.raiz)
            self.capa.attributes("-alpha", 1.0)
            self.tema.vincular(self.capa, bg="fondo")
            self._ajustar_geometria()
            self.capa.deiconify()
            self.capa.lift(self.raiz)
            # La capa se dibuja antes de dejar que se acomode la nueva página.
            self.capa.update_idletasks()
            self.pendiente = self.raiz.after_idle(self._preparar)
        except tk.TclError:
            # Algunos gestores de ventanas no admiten transparencia.
            self.cancelar()

    def _preparar(self):
        """Termina la geometría debajo de la capa antes de revelar el contenido."""
        self.pendiente = None
        if self.capa is None:
            return
        self.raiz.update_idletasks()
        self.pendiente = self.raiz.after(16, lambda: self._desvanecer(1))

    def _desvanecer(self, fotograma):
        """Reduce la opacidad solo de la capa; nunca la de la calculadora."""
        self.pendiente = None
        if self.capa is None:
            return
        if not self.raiz.winfo_viewable():
            self.cancelar()
            return
        try:
            self.capa.attributes("-alpha", max(0, 1 - fotograma / FOTOGRAMAS))
            if fotograma >= FOTOGRAMAS:
                self.cancelar()
            else:
                self.pendiente = self.raiz.after(DURACION_MS // FOTOGRAMAS,
                                                 lambda: self._desvanecer(fotograma + 1))
        except tk.TclError:
            self.cancelar()

    def _ajustar_geometria(self):
        """Limita la capa al área cliente de la ventana de la calculadora."""
        ancho, alto = self.raiz.winfo_width(), self.raiz.winfo_height()
        x, y = self.raiz.winfo_rootx(), self.raiz.winfo_rooty()
        self.capa.geometry(f"{ancho}x{alto}{x:+d}{y:+d}")

    def _redimensionar(self, evento):
        """Acompaña un movimiento o cambio de tamaño durante la transición."""
        if evento.widget == self.raiz and self.capa is not None:
            self._ajustar_geometria()

    def cancelar(self):
        """Retira capa y temporizador al repetir un cambio, editar o cerrar."""
        try:
            if self.pendiente is not None:
                self.raiz.after_cancel(self.pendiente)
            if self.capa is not None:
                self.capa.destroy()
        except tk.TclError:
            pass
        self.pendiente = None
        self.capa = None

    def _al_destruir(self, evento):
        """Cancela recursos aunque la raíz se cierre fuera del botón de la app."""
        if evento.widget == self.raiz:
            self.cancelar()
