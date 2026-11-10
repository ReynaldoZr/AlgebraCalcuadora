"""Centraliza colores y estilos de la ventana de escritorio.

Tema: presentación azul oscuro y lavanda, con alternativa clara.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from tkinter import ttk

OSCURO = dict(fondo="#10243e", tarjeta="#1a3350", entrada="#142b46",
              texto="#edf2fa", secundario="#b3c2d6", borde="#52708e",
              acento="#a5a6ff", sobre_acento="#10243e", activo="#bbbcff",
              error="#ffabb5", a="#70b7ff", b="#b79aff")
CLARO = dict(fondo="#eef2fa", tarjeta="#ffffff", entrada="#f4f6fc",
             texto="#10243e", secundario="#526580", borde="#9aaec5",
             acento="#6261b8", sobre_acento="#ffffff", activo="#7776ca",
             error="#a8243c", a="#2469a3", b="#704baa")


class Tema:
    """Aplica una paleta a ttk y a los widgets dibujados por la aplicación."""

    def __init__(self, raiz):
        """Prepara el tema oscuro sin modificar datos o cálculos."""
        self.raiz = raiz
        self.oscuro = True
        self.colores = OSCURO.copy()
        self.estilo = ttk.Style(raiz)
        self.estilo.theme_use("clam")
        self.aplicar()

    def vincular(self, widget, **colores):
        """Asocia opciones de un widget Tk con nombres de la paleta."""
        widget.colores_tema = colores
        widget.configure(**{opcion: self.colores[rol] for opcion, rol in colores.items()})
        return widget

    def alternar(self):
        """Cambia la paleta conservando los widgets y su estado."""
        self.oscuro = not self.oscuro
        self.colores = (OSCURO if self.oscuro else CLARO).copy()
        self.aplicar()

    def aplicar(self):
        """Configura estilos y actualiza las superficies ya construidas."""
        c, estilo = self.colores, self.estilo
        estilo.configure(".", font=("Segoe UI", 10), background=c["fondo"], foreground=c["texto"])
        estilo.configure("TFrame", background=c["fondo"])
        estilo.configure("TLabel", background=c["fondo"], foreground=c["texto"])
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 18, "bold"))
        estilo.configure("Subtitulo.TLabel", foreground=c["secundario"])
        estilo.configure("Tarjeta.TFrame", background=c["tarjeta"], borderwidth=1,
                         relief="solid", bordercolor=c["borde"])
        estilo.configure("Interior.TFrame", background=c["tarjeta"])
        for nombre in ("Tarjeta", "Coordenada", "TarjetaTitulo"):
            estilo.configure(f"{nombre}.TLabel", background=c["tarjeta"],
                             foreground=c["secundario"] if nombre == "Coordenada" else c["texto"])
        estilo.configure("TarjetaTitulo.TLabel", font=("Segoe UI", 12, "bold"))
        estilo.configure("Estado.TLabel", foreground=c["acento"])
        estilo.configure("Error.TLabel", foreground=c["error"])
        estilo.configure("TButton", padding=(12, 7), background=c["entrada"],
                         foreground=c["texto"], bordercolor=c["borde"], focusthickness=1)
        estilo.map("TButton", background=[("active", c["tarjeta"])],
                   foreground=[("disabled", c["secundario"])])
        estilo.configure('TarjetaTema.TButton', background=c['entrada'], foreground=c['texto'],
                         borderwidth=0, padding=(2, 5), anchor='w', font=('Segoe UI', 11, 'bold'))
        estilo.map('TarjetaTema.TButton', background=[('active', c['tarjeta'])])
        for nombre in ("Principal.TButton", "Tema.TRadiobutton"):
            estilo.configure(nombre, background=c["acento"], foreground=c["sobre_acento"],
                             padding=(14, 8), font=("Segoe UI", 10, "bold"))
            estilo.map(nombre, background=[("active", c["activo"])],
                       foreground=[("disabled", c["secundario"])])
        estilo.configure("TRadiobutton", padding=(14, 8), background=c["entrada"])
        estilo.map("TRadiobutton", background=[("selected", c["acento"])],
                   foreground=[("selected", c["sobre_acento"])])
        for nombre in ("TEntry", "TSpinbox"):
            estilo.configure(nombre, fieldbackground=c["entrada"], foreground=c["texto"],
                             insertcolor=c["texto"], bordercolor=c["borde"], arrowsize=12)
        estilo.configure("Activa.TEntry", fieldbackground=c["acento"],
                         foreground=c["sobre_acento"], bordercolor=c["acento"])
        estilo.configure('TCombobox', fieldbackground=c['entrada'], foreground=c['texto'],
                         background=c['entrada'], arrowcolor=c['texto'], padding=6)
        estilo.map('TCombobox', fieldbackground=[('readonly', c['entrada'])],
                   foreground=[('readonly', c['texto'])], selectbackground=[('readonly', c['entrada'])],
                   selectforeground=[('readonly', c['texto'])])
        self.raiz.option_add('*TCombobox*Listbox.background', c['entrada'])
        self.raiz.option_add('*TCombobox*Listbox.foreground', c['texto'])
        estilo.configure('Treeview', background=c['tarjeta'], fieldbackground=c['tarjeta'],
                         foreground=c['texto'], rowheight=28, font=('Segoe UI', 10))
        estilo.configure('Treeview.Heading', background=c['entrada'], foreground=c['texto'])
        estilo.map('Treeview', background=[('selected', c['acento'])],
                   foreground=[('selected', c['sobre_acento'])])
        for orientacion in ("Vertical", "Horizontal"):
            estilo.configure(f"{orientacion}.TScrollbar", background=c["borde"],
                             troughcolor=c["fondo"], bordercolor=c["borde"],
                             lightcolor=c["borde"], darkcolor=c["borde"],
                             arrowcolor=c["texto"], borderwidth=0, arrowsize=10)
        estilo.configure("TNotebook", background=c["fondo"], borderwidth=0,
                         bordercolor=c["fondo"], lightcolor=c["fondo"], darkcolor=c["fondo"],
                         tabmargins=(0, 0, 0, 10))
        estilo.configure("TNotebook.Tab", padding=(18, 9), background=c["entrada"],
                         bordercolor=c["borde"], lightcolor=c["borde"], darkcolor=c["borde"])
        estilo.map("TNotebook.Tab", background=[("selected", c["acento"])],
                   foreground=[("selected", c["sobre_acento"])])
        self.raiz.configure(bg=c["fondo"])
        self._actualizar_arbol(self.raiz)

    def _actualizar_arbol(self, widget):
        """Recorre widgets existentes para redibujar también los lienzos."""
        if hasattr(widget, "colores_tema"):
            widget.configure(**{opcion: self.colores[rol]
                                for opcion, rol in widget.colores_tema.items()})
        if hasattr(widget, "actualizar_tema"):
            widget.actualizar_tema()
        for hijo in widget.winfo_children():
            self._actualizar_arbol(hijo)
