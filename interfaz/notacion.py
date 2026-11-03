"""Dibuja fracciones, fórmulas y matrices sin convertirlas a imágenes.

Tema: notación exacta legible en los lienzos de Tkinter.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
from tkinter import font


class Notacion(tk.Canvas):
    """Presenta datos ya calculados con fracciones apiladas y desplazamiento."""

    def __init__(self, padre, tema, alto=120, tamano=17):
        """Crea una superficie que se centra si hay espacio y se desplaza si falta."""
        super().__init__(padre, height=alto, width=80, highlightthickness=0)
        self.tema = tema
        self.fuente = font.Font(self, family="Cambria", size=tamano)
        self.matriz = None
        self.tokens = []
        self.activa = None
        self.bind("<Configure>", self.actualizar_tema)
        self.actualizar_tema()

    def mostrar_formula(self, tokens):
        """Presenta números, signos y pares (numerador, denominador) sin simplificarlos."""
        self.matriz = None
        self.tokens = list(tokens)
        self.activa = None
        self.actualizar_tema()

    def mostrar_matriz(self, matriz, activa=None):
        """Conserva una copia para dibujar la matriz y una posición opcional."""
        self.matriz = [list(fila) for fila in matriz]
        self.tokens = []
        self.activa = activa
        self.actualizar_tema()

    def _partes(self, valor):
        """Separa una fracción literal o exacta sin aproximarla a decimal."""
        if isinstance(valor, tuple):
            return str(valor[0]), str(valor[1])
        if hasattr(valor, "denominator") and valor.denominator != 1:
            return str(valor.numerator), str(valor.denominator)
        return str(valor), None

    def _ancho(self, valor):
        """Mide el espacio requerido por un valor usando su fuente real."""
        arriba, abajo = self._partes(valor)
        return max(self.fuente.measure(arriba), self.fuente.measure(abajo or "")) + 14

    def _numero(self, valor, x, y, color=None):
        """Dibuja un entero o una fracción con barra horizontal centrada."""
        arriba, abajo = self._partes(valor)
        color = color or self.tema.colores["texto"]
        if abajo is None:
            self.create_text(x, y, text=arriba, font=self.fuente, fill=color)
        else:
            distancia = self.fuente.metrics("linespace") * 0.55
            ancho = self._ancho(valor) - 8
            self.create_text(x, y - distancia, text=arriba, font=self.fuente, fill=color)
            self.create_line(x - ancho / 2, y, x + ancho / 2, y, fill=color, width=1.4)
            self.create_text(x, y + distancia, text=abajo, font=self.fuente, fill=color)

    def actualizar_tema(self, evento=None):
        """Redibuja al cambiar el tamaño, el contenido o la paleta."""
        resaltada = getattr(self, "resaltada", False)
        self.configure(bg=self.tema.colores[getattr(self, "rol_resaltado", "acento")]
                       if resaltada else self.tema.colores["tarjeta"])
        self.delete("all")
        if self.matriz is not None:
            self._dibujar_matriz()
        elif self.tokens:
            ancho = sum(self._ancho(valor) for valor in self.tokens) + 24
            x = max(12, (self.winfo_width() - ancho) / 2 + 12)
            alto = max(36, self.fuente.metrics("linespace") * 2.2)
            y = max(alto / 2, self.winfo_height() / 2)
            for valor in self.tokens:
                paso = self._ancho(valor)
                self._numero(valor, x + paso / 2, y,
                             self.tema.colores["sobre_acento"] if resaltada else None)
                x += paso
            self.configure(scrollregion=(0, 0, max(ancho, self.winfo_width()), max(alto, self.winfo_height())))
        else:
            self.configure(scrollregion=(0, 0, self.winfo_width(), self.winfo_height()))

    def _dibujar_matriz(self):
        """Alinea columnas y corchetes con espacio suficiente para cada fracción."""
        filas, columnas = len(self.matriz), len(self.matriz[0])
        anchos = [max(58, max(self._ancho(fila[j]) for fila in self.matriz) + 20)
                  for j in range(columnas)]
        alto_fila = max(52, self.fuente.metrics("linespace") * 2.2)
        ancho, alto = sum(anchos) + 38, filas * alto_fila + 16
        x0 = max(18, (self.winfo_width() - ancho) / 2 + 18)
        y0 = max(8, (self.winfo_height() - alto) / 2 + 8)
        c = self.tema.colores
        for i, fila in enumerate(self.matriz):
            x = x0
            for j, valor in enumerate(fila):
                y = y0 + (i + 0.5) * alto_fila
                if self.activa == (i, j):
                    self.create_rectangle(x + 3, y - alto_fila / 2 + 3,
                                          x + anchos[j] - 3, y + alto_fila / 2 - 3,
                                          fill=c["acento"], outline="")
                self._numero(valor, x + anchos[j] / 2, y,
                             c["sobre_acento"] if self.activa == (i, j) else c["texto"])
                x += anchos[j]
        for borde, direccion in ((x0 - 8, 1), (x0 + sum(anchos) + 8, -1)):
            self.create_line(borde + direccion * 8, y0, borde, y0,
                             borde, y0 + filas * alto_fila,
                             borde + direccion * 8, y0 + filas * alto_fila,
                             fill=c["texto"], width=2)
        self.configure(scrollregion=(0, 0, max(ancho, self.winfo_width()), max(alto, self.winfo_height())))


def crear_icono_matrices(padre, tema, seleccionado=True):
    """Dibuja el icono cuadrado de cuatro casillas aprobado para Matrices."""
    icono = tk.Canvas(padre, width=28, height=28, highlightthickness=0)
    tema.vincular(icono, bg="acento" if seleccionado else "fondo")
    for x, y in ((5, 5), (16, 5), (5, 16), (16, 16)):
        cuadrado = icono.create_rectangle(x, y, x + 7, y + 7, width=1.6, tags="casilla")
        icono.itemconfigure(cuadrado, outline=tema.colores["sobre_acento"])
    icono.actualizar_tema = lambda: icono.itemconfigure("casilla", outline=tema.colores["sobre_acento"])
    return icono
