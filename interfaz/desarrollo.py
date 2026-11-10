"""Presenta el desarrollo completo en tarjetas desplazables.

Tema: explicación de resultados exactos ya obtenidos por el núcleo.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
from tkinter import ttk

from interfaz.notacion import Notacion
from interfaz.explicacion import etapas_completas, fraccion_intermedia, operacion_de_paso, terminos_producto


def detallar_paso(paso):
    """Forma equivalencias visuales sin reemplazar el resultado del núcleo."""
    _, _, a, b, resultado, signo = paso
    if signo == "AB":
        return terminos_producto(paso), "Multiplicamos los pares de una fila por una columna y sumamos sus productos."
    if signo == "T":
        fila, columna = paso[:2]
        return [f"A[{columna + 1},{fila + 1}]", "=", a, "→", f"R[{fila + 1},{columna + 1}]", "=", resultado], "Intercambiamos fila y columna; el valor se conserva."
    if signo == "×":
        return detallar_escalar(a, b, resultado)
    tokens = [a, signo]
    tokens.extend(["(", b, ")"] if b < 0 else [b])
    if a.denominator == b.denominator == 1:
        return tokens + ["=", resultado], "Operamos los enteros de esta posición."
    numerador_a, numerador_b, comun = fraccion_intermedia(paso)
    tokens += ["=", (numerador_a, comun), signo]
    tokens.extend(["(", (numerador_b, comun), ")"] if b < 0 else [(numerador_b, comun)])
    numerador = numerador_a + numerador_b if signo == "+" else numerador_a - numerador_b
    tokens += ["=", (numerador, comun)]
    if (numerador, comun) != (resultado.numerator, resultado.denominator):
        tokens += ["=", resultado]
    return tokens, "Usamos denominador común y simplificamos la fracción resultante."


def detallar_escalar(escalar, elemento, resultado):
    """Expone el producto de numeradores y denominadores para una entrada de kA."""
    tokens = [escalar, "×"]
    tokens += ["(", elemento, ")"] if elemento < 0 else [elemento]
    if escalar.denominator != 1 or elemento.denominator != 1:
        operacion, _, numerador, denominador = operacion_de_paso((0, 0, escalar, elemento, resultado, "×"))
        tokens += ["="] + operacion
        if (numerador, denominador) != (resultado.numerator, resultado.denominator):
            tokens += ["=", resultado]
        return tokens, "Multiplicamos numeradores y denominadores; simplificamos si es posible."
    return tokens + ["=", resultado], "Multiplicamos el elemento de A por el mismo escalar k."


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

    def mostrar(self, pasos, resultado, condicion=None):
        """Sustituye las tarjetas por un cálculo completo o vacía la vista."""
        self.pasos = tuple(pasos)
        for hijo in self.cuerpo.winfo_children():
            hijo.destroy()
        if not self.pasos:
            self.aviso.configure(text="Calcula para ver el desarrollo completo.")
            return
        filas, columnas = len(resultado), len(resultado[0])
        condicion = condicion or f"A y B tienen las mismas dimensiones: {filas} × {columnas}."
        self.aviso.configure(text=f"{condicion}  ·  {len(pasos)} pasos")
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
        etapas = etapas_completas(paso, indice)
        origen = ttk.Label(detalle, text=etapas[0].operandos.replace("\n", "  ·  "),
                            style="Coordenada.TLabel", wraplength=640)
        origen.pack(anchor="w", pady=(0, 6))
        etiquetas = [origen]
        for etapa in etapas:
            titulo = etapa.titulo
            if etapa.par is not None:
                titulo += " · " + etapa.operandos.replace("\n", " · ")
            etiqueta = ttk.Label(detalle, text=titulo, style="Coordenada.TLabel", wraplength=640)
            etiqueta.pack(anchor="w", pady=(8, 0))
            etiquetas.append(etiqueta)
            crear_notacion(detalle, self.tema, 56, 16).mostrar_formula(etapa.tokens)
            if etapa.mensaje:
                nota = ttk.Label(detalle, text=etapa.mensaje, style="Tarjeta.TLabel", wraplength=640)
                nota.pack(anchor="w")
                etiquetas.append(nota)
        detalle.bind("<Configure>", lambda evento: self._ajustar_etiquetas(evento.width, *etiquetas))

    def _ajustar_etiquetas(self, ancho, *etiquetas):
        """Mantiene las instrucciones legibles al reducir el ancho de la ventana."""
        for etiqueta in etiquetas:
            etiqueta.configure(wraplength=max(140, ancho - 12))
