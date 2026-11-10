"""Dibuja gráficas numéricas en un diálogo Tk con la paleta del proyecto.

Tema: función e incertidumbre en bisección, propagación y errores de iteración.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from interfaz.numericos.figuras import figura_numerica


def abrir_grafica(padre, clave, calculo, tema):
    """Abre una figura con herramientas de navegación y guardado de imagen por el usuario."""
    ventana = tk.Toplevel(padre)
    ventana.title('Gráfica del ejercicio · Numéricos')
    ventana.geometry('980x720')
    figura = figura_numerica(clave, calculo)
    figura.set_facecolor(tema.colores['fondo'])
    for eje in figura.axes:
        eje.set_facecolor(tema.colores['tarjeta'])
        eje.tick_params(colors=tema.colores['texto'])
        for etiqueta in (eje.xaxis.label, eje.yaxis.label, eje.title):
            etiqueta.set_color(tema.colores['texto'])
    lienzo = FigureCanvasTkAgg(figura, master=ventana)
    barra = NavigationToolbar2Tk(lienzo, ventana, pack_toolbar=False)
    barra.pack(side='bottom', fill='x')
    lienzo.get_tk_widget().pack(fill='both', expand=True)
    lienzo.draw()
