"""Construye un editor desplazable para una matriz de hasta 10x10.

Tema: entrada gráfica de matrices con conversión exacta.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
from tkinter import ttk

from interfaz.datos import convertir_numero

LIMITE_CUADRICULA = 10


def leer_dimension(texto):
    """Devuelve una dimensión entera de 1 a 10 o comunica por qué no es válida."""
    try:
        valor = int(texto.strip())
    except ValueError:
        raise ValueError("Las dimensiones deben ser números enteros de 1 a 10.") from None
    if not 1 <= valor <= LIMITE_CUADRICULA:
        raise ValueError("En la ventana, cada dimensión debe estar entre 1 y 10.")
    return valor


class EditorMatriz(ttk.Frame):
    """Agrupa dimensiones, casillas y desplazamiento de una matriz."""

    def __init__(self, padre, nombre, al_cambiar, informar_error):
        """Crea un editor 2x2; recibe callbacks para cambios y errores."""
        super().__init__(padre, style="Tarjeta.TFrame", padding=18)
        self.nombre = nombre
        self.al_cambiar = al_cambiar
        self.informar_error = informar_error
        self.filas = tk.StringVar(self, "2")
        self.columnas = tk.StringVar(self, "2")
        self.celdas = []
        self.variables = []
        ttk.Label(self, text=f"Matriz {nombre}", style="TarjetaTitulo.TLabel").pack(anchor="w")
        self._crear_dimensiones()
        self._crear_area()
        self.cargar([[0, 0], [0, 0]])
        self.filas.trace_add("write", self.al_cambiar)
        self.columnas.trace_add("write", self.al_cambiar)

    def _crear_dimensiones(self):
        """Añade controles de tamaño y un botón para aplicarlos explícitamente."""
        barra = ttk.Frame(self, style="Tarjeta.TFrame")
        barra.pack(fill="x", pady=(12, 14))
        for columna, (texto, variable) in enumerate((("Filas", self.filas), ("Columnas", self.columnas))):
            ttk.Label(barra, text=texto, style="Tarjeta.TLabel").grid(row=0, column=columna, sticky="w")
            ttk.Spinbox(barra, from_=1, to=LIMITE_CUADRICULA, width=3,
                        textvariable=variable).grid(row=1, column=columna, sticky="w", padx=(0, 12), pady=(4, 0))
        barra.columnconfigure(2, weight=1)
        ttk.Button(barra, text="Aplicar", command=self.aplicar_tamano).grid(row=0, column=2, rowspan=2, sticky="e")

    def _crear_area(self):
        """Crea desplazamiento horizontal y vertical para no recortar las casillas."""
        area = ttk.Frame(self, style="Tarjeta.TFrame")
        area.pack(fill="both", expand=True)
        area.columnconfigure(0, weight=1)
        area.rowconfigure(0, weight=1)
        self.lienzo = tk.Canvas(area, bg="white", highlightthickness=0, height=190)
        self.lienzo.grid(row=0, column=0, sticky="nsew")
        for orientacion, fila, columna in (("vertical", 0, 1), ("horizontal", 1, 0)):
            comando = self.lienzo.yview if orientacion == "vertical" else self.lienzo.xview
            barra = ttk.Scrollbar(area, orient=orientacion, command=comando)
            barra.grid(row=fila, column=columna, sticky="ns" if fila == 0 else "ew")
            eje = "x" if orientacion == "horizontal" else "y"
            self.lienzo.configure(**{f"{eje}scrollcommand": barra.set})
        self.rejilla = ttk.Frame(self.lienzo, style="Tarjeta.TFrame")
        self.lienzo.create_window((0, 0), window=self.rejilla, anchor="nw")
        self.rejilla.bind("<Configure>", self._ajustar_desplazamiento)

    def _ajustar_desplazamiento(self, evento=None):
        """Actualiza el área desplazable cuando cambian las dimensiones."""
        self.lienzo.configure(scrollregion=self.lienzo.bbox("all"))

    def cargar(self, matriz):
        """Llena el editor con una matriz sin compartir sus datos mutables."""
        for widget in self.rejilla.winfo_children():
            widget.destroy()
        self.filas.set(str(len(matriz)))
        self.columnas.set(str(len(matriz[0])))
        self.celdas = []
        # Tk necesita conservar las variables mientras existan sus casillas.
        self.variables = []
        for j in range(len(matriz[0])):
            ttk.Label(self.rejilla, text=str(j + 1), style="Coordenada.TLabel").grid(row=0, column=j + 1)
        for i, valores in enumerate(matriz):
            ttk.Label(self.rejilla, text=str(i + 1), style="Coordenada.TLabel").grid(row=i + 1, column=0, padx=(0, 6))
            fila = []
            for j, valor in enumerate(valores):
                variable = tk.StringVar(self, str(valor))
                self.variables.append(variable)
                entrada = ttk.Entry(self.rejilla, textvariable=variable, width=7, justify="center")
                entrada.grid(row=i + 1, column=j + 1, padx=3, pady=4, ipady=4)
                variable.trace_add("write", self.al_cambiar)
                fila.append(entrada)
            self.celdas.append(fila)
        self.lienzo.xview_moveto(0)
        self.lienzo.yview_moveto(0)

    def aplicar_tamano(self):
        """Redimensiona conservando celdas coincidentes y pide permiso si recorta datos."""
        try:
            filas = leer_dimension(self.filas.get())
            columnas = leer_dimension(self.columnas.get())
        except ValueError as error:
            self.informar_error(str(error))
            return
        anteriores = [[celda.get() for celda in fila] for fila in self.celdas]
        if filas < len(anteriores) or columnas < len(anteriores[0]):
            from tkinter import messagebox
            if not messagebox.askyesno("Cambiar tamaño", "Se quitarán las celdas fuera del nuevo tamaño. ¿Continuar?", parent=self):
                self.filas.set(str(len(anteriores)))
                self.columnas.set(str(len(anteriores[0])))
                return
        matriz = [[anteriores[i][j] if i < len(anteriores) and j < len(anteriores[0]) else "0"
                   for j in range(columnas)] for i in range(filas)]
        self.cargar(matriz)
        self.al_cambiar()

    def leer(self):
        """Devuelve la matriz exacta; ante un error enfoca e identifica su casilla."""
        dimensiones = leer_dimension(self.filas.get()), leer_dimension(self.columnas.get())
        if dimensiones != (len(self.celdas), len(self.celdas[0])):
            raise ValueError(f"En la matriz {self.nombre}, pulsa Aplicar para usar el nuevo tamaño.")
        matriz = []
        for i, fila in enumerate(self.celdas):
            valores = []
            for j, celda in enumerate(fila):
                try:
                    valores.append(convertir_numero(celda.get()))
                except (ValueError, ZeroDivisionError):
                    celda.focus_set()
                    celda.selection_range(0, "end")
                    self.lienzo.xview_moveto(j / len(fila))
                    self.lienzo.yview_moveto(i / len(self.celdas))
                    raise ValueError(f"Revisa {self.nombre}[{i + 1},{j + 1}]: usa un número como 2, 0.5 o 1/3.") from None
            matriz.append(valores)
        return matriz
