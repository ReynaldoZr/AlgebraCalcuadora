"""Presenta el desarrollo completo en tarjetas desplazables.

Tema: explicación de resultados exactos ya obtenidos por el núcleo.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
from tkinter import ttk

from interfaz.notacion import Notacion


def detallar_paso(paso):
    """Forma equivalencias visuales sin reemplazar el resultado del núcleo."""
    _, _, a, b, resultado, signo = paso
    tokens = [a, signo]
    tokens.extend(["(", b, ")"] if b < 0 else [b])
    if a.denominator == b.denominator == 1:
        return tokens + ["=", resultado], "Operamos los enteros de esta posición."
    # Euclides obtiene el mínimo denominador común solo para la explicación.
    divisor, resto = a.denominator, b.denominator
    while resto:
        divisor, resto = resto, divisor % resto
    comun = a.denominator * b.denominator // divisor
    numerador_a = a.numerator * (comun // a.denominator)
    numerador_b = b.numerator * (comun // b.denominator)
    tokens += ["=", (numerador_a, comun), signo]
    tokens.extend(["(", (numerador_b, comun), ")"] if b < 0 else [(numerador_b, comun)])
    numerador = numerador_a + numerador_b if signo == "+" else numerador_a - numerador_b
    tokens += ["=", (numerador, comun)]
    if (numerador, comun) != (resultado.numerator, resultado.denominator):
        tokens += ["=", resultado]
    return tokens, "Usamos denominador común y simplificamos la fracción resultante."


def crear_notacion(padre, tema, alto=120, tamano=17):
    """Añade un lienzo matemático con barras para fórmulas o matrices extensas."""
    marco = ttk.Frame(padre, style="Interior.TFrame")
    marco.pack(fill="both", expand=True)
    marco.columnconfigure(0, weight=1)
    marco.rowconfigure(0, weight=1)
    vista = Notacion(marco, tema, alto, tamano)
    vista.grid(row=0, column=0, sticky="nsew")
    for eje, orientacion, fila, columna in (("x", "horizontal", 1, 0), ("y", "vertical", 0, 1)):
        barra = ttk.Scrollbar(marco, orient=orientacion,
                              command=vista.xview if eje == "x" else vista.yview)
        barra.grid(row=fila, column=columna, sticky="ew" if eje == "x" else "ns")
        vista.configure(**{f"{eje}scrollcommand": lambda inicio, fin, b=barra: ajustar_barra(b, inicio, fin)})
    return vista


def ajustar_barra(barra, inicio, fin):
    """Muestra el desplazamiento únicamente cuando el contenido no cabe."""
    barra.set(inicio, fin)
    if float(inicio) <= 0 and float(fin) >= 1:
        barra.grid_remove()
    else:
        barra.grid()


class Desarrollo(ttk.Frame):
    """Ocupa la pestaña de pasos con todas las posiciones y el resultado final."""

    def __init__(self, padre, tema):
        """Construye un área desplazable sin bindings globales de rueda."""
        super().__init__(padre)
        self.tema = tema
        self.pasos = ()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.aviso = ttk.Label(self, text="Calcula para ver el desarrollo completo.", style="Estado.TLabel")
        self.aviso.grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.lienzo = tk.Canvas(self, highlightthickness=0)
        tema.vincular(self.lienzo, bg="fondo")
        self.lienzo.grid(row=1, column=0, sticky="nsew")
        barra = ttk.Scrollbar(self, command=self.lienzo.yview)
        barra.grid(row=1, column=1, sticky="ns")
        self.lienzo.configure(yscrollcommand=barra.set)
        self.cuerpo = ttk.Frame(self.lienzo)
        self.ventana = self.lienzo.create_window(0, 0, window=self.cuerpo, anchor="nw")
        self.lienzo.bind("<Configure>", self._redimensionar)
        self.cuerpo.bind("<Configure>", self._ajustar_region)
        self._vincular_rueda(self.lienzo)

    def _redimensionar(self, evento):
        """Hace que las tarjetas usen todo el ancho disponible."""
        self.lienzo.itemconfigure(self.ventana, width=evento.width)

    def _ajustar_region(self, evento=None):
        """Actualiza el recorrido vertical al construir tarjetas."""
        self.lienzo.configure(scrollregion=self.lienzo.bbox("all"))

    def _rueda(self, evento):
        """Desplaza los pasos con rueda en Windows y Linux."""
        unidades = (-1 if evento.num == 4 else 1) if evento.num in (4, 5) else (-1 if evento.delta > 0 else 1)
        self.lienzo.yview_scroll(unidades * 3, "units")
        return "break"

    def _vincular_rueda(self, widget):
        """Limita la rueda a esta vista para no interferir con las entradas."""
        for evento in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            widget.bind(evento, self._rueda)
        for hijo in widget.winfo_children():
            self._vincular_rueda(hijo)

    def mostrar(self, pasos, resultado):
        """Sustituye las tarjetas por un cálculo completo o vacía la vista."""
        self.pasos = tuple(pasos)
        for hijo in self.cuerpo.winfo_children():
            hijo.destroy()
        if not self.pasos:
            self.aviso.configure(text="Calcula para ver el desarrollo completo.")
            return
        filas, columnas = len(resultado), len(resultado[0])
        self.aviso.configure(text=f"A y B tienen las mismas dimensiones: {filas} × {columnas}.  ·  {len(pasos)} pasos")
        for indice, paso in enumerate(pasos):
            self._tarjeta(indice, paso)
        final = ttk.Frame(self.cuerpo, style="Tarjeta.TFrame", padding=16)
        final.pack(fill="x", pady=(2, 12), padx=(0, 4))
        ttk.Label(final, text="Resultado final", style="TarjetaTitulo.TLabel").pack(anchor="w")
        crear_notacion(final, self.tema, min(240, filas * 66 + 28)).mostrar_matriz(resultado)
        self._vincular_rueda(self.cuerpo)
        self.lienzo.yview_moveto(0)

    def _tarjeta(self, indice, paso):
        """Presenta coordenada, equivalencias y explicación de una posición."""
        tarjeta = ttk.Frame(self.cuerpo, style="Tarjeta.TFrame", padding=(16, 10))
        tarjeta.pack(fill="x", pady=(0, 10), padx=(0, 4))
        cabecera = ttk.Frame(tarjeta, style="Interior.TFrame")
        cabecera.pack(side="left", padx=(0, 26), anchor="center")
        ttk.Label(cabecera, text=f"Paso {indice + 1}", style="TarjetaTitulo.TLabel").pack(anchor="w")
        ttk.Label(cabecera, text=f"Fila {paso[0] + 1} · Columna {paso[1] + 1}",
                  style="Coordenada.TLabel").pack(anchor="w", pady=(8, 0))
        detalle = ttk.Frame(tarjeta, style="Interior.TFrame")
        detalle.pack(side="left", fill="both", expand=True)
        tokens, explicacion = detallar_paso(paso)
        crear_notacion(detalle, self.tema, 60, 16).mostrar_formula(tokens)
        ttk.Label(detalle, text=explicacion, style="Tarjeta.TLabel").pack(anchor="w", pady=(3, 0))
