"""Convierte la figura numérica existente a una imagen para Qt Quick.

Tema: adaptador gráfico opcional, independiente del algoritmo de bisección.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from io import BytesIO

from PySide6.QtGui import QImage
from matplotlib.backends.backend_agg import FigureCanvasAgg

from interfaz.numericos.figuras import figura_numerica


def imagen_grafica(clave, calculo, oscuro=True):
    """Dibuja las mismas curvas y datos en memoria, sin archivos temporales ni Tk."""
    figura = figura_numerica(clave, calculo)
    fondo, texto = ('#001233', '#e8ecf4') if oscuro else ('#dad7cd', '#344e41')
    figura.set_facecolor(fondo)
    for eje in figura.axes:
        eje.set_facecolor(fondo)
        eje.tick_params(colors=texto)
        for etiqueta in (eje.xaxis.label, eje.yaxis.label, eje.title):
            etiqueta.set_color(texto)
        for borde in eje.spines.values():
            borde.set_color(texto)
    memoria = BytesIO()
    FigureCanvasAgg(figura).print_png(memoria)
    return QImage.fromData(memoria.getvalue(), 'PNG')
