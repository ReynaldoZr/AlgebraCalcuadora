"""Agrupa acciones secundarias sin duplicar su validación o comportamiento.

Tema: menús compactos de la interfaz de escritorio.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
from tkinter import ttk


def menu_botones(padre, tema, botones):
    """Crea un menú que respeta el estado habilitado de los botones existentes."""
    acceso = ttk.Menubutton(padre, text='⋯', width=3)
    menu = tk.Menu(acceso, tearoff=False)
    tema.vincular(menu, bg='tarjeta', fg='texto', activebackground='acento', activeforeground='sobre_acento')

    def actualizar():
        """Consulta el estado actual al abrir el menú, no al construir la ventana."""
        menu.delete(0, 'end')
        for boton in botones:
            menu.add_command(label=boton.cget('text'), command=boton.invoke,
                             state='disabled' if boton.instate(['disabled']) else 'normal')

    menu.configure(postcommand=actualizar)
    acceso.configure(menu=menu)
    acceso.menu_acciones = menu
    return acceso
