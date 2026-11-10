"""Construye un editor desplazable para una matriz de hasta 10x10.

Tema: entrada gráfica de matrices con conversión exacta.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
from tkinter import ttk

from interfaz.datos import convertir_numero
from interfaz.notacion import Notacion
from interfaz.desarrollo import ajustar_barra
from interfaz.pegado import interpretar_matriz, texto_matriz

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

    def __init__(self, padre, nombre, al_cambiar, informar_error, tema):
        """Crea un editor 2x2; recibe callbacks para cambios y errores."""
        super().__init__(padre, style="Tarjeta.TFrame", padding=14)
        self.tema = tema
        self.cargando = True
        self.vistas = []
        self.nombre = nombre
        self.al_cambiar = al_cambiar
        self.informar_error = informar_error
        self.filas = tk.StringVar(self, "2")
        self.columnas = tk.StringVar(self, "2")
        self.celdas = []
        self.variables = []
        cabecera = ttk.Frame(self, style='Interior.TFrame')
        cabecera.pack(fill='x')
        self.etiqueta_nombre = ttk.Label(cabecera, text=f'Matriz {nombre}', style='TarjetaTitulo.TLabel')
        self.etiqueta_nombre.pack(side='left')
        from interfaz.herramientas import menu_botones
        copiar = ttk.Button(cabecera, text='Copiar matriz', command=self.copiar)
        pegar = ttk.Button(cabecera, text='Pegar matriz', command=self.pegar)
        self.herramientas = menu_botones(cabecera, tema, (copiar, pegar))
        self.herramientas.pack(side='right')
        self.tamano = ttk.Button(self, text='2 × 2 · Cambiar', command=self.alternar_dimensiones, padding=(4, 2))
        self.tamano.pack(anchor='w', pady=(6, 0))
        self._crear_dimensiones()
        self._crear_area()
        self.cargar([["", ""], ["", ""]])
        self.filas.trace_add("write", self.al_cambiar)
        self.columnas.trace_add("write", self.al_cambiar)

    def _crear_dimensiones(self):
        """Añade controles de tamaño y un botón para aplicarlos explícitamente."""
        barra = self.barra_dimensiones = ttk.Frame(self, style="Interior.TFrame")
        for columna, (texto, variable) in enumerate((("Filas", self.filas), ("Columnas", self.columnas))):
            ttk.Label(barra, text=texto, style="Tarjeta.TLabel").grid(row=0, column=columna, sticky="w")
            ttk.Spinbox(barra, from_=1, to=LIMITE_CUADRICULA, width=3,
                        textvariable=variable).grid(row=1, column=columna, sticky="w", padx=(0, 12), pady=(4, 0))
        barra.columnconfigure(2, weight=1)
        ttk.Button(barra, text="Aplicar", style="Principal.TButton", command=self.aplicar_tamano).grid(row=0, column=2, rowspan=2, sticky="e")

    def alternar_dimensiones(self):
        """Muestra u oculta Filas/Columnas sin aplicar un tamaño accidentalmente."""
        # El tamaño tiene prioridad; la matriz conserva sus barras si queda menos espacio.
        if self.barra_dimensiones.winfo_manager():
            self.barra_dimensiones.pack_forget()
        else:
            self.barra_dimensiones.pack(side='bottom', fill='x', pady=(12, 0), before=self.area)

    def vaciar(self):
        """Deja las casillas vacías conservando el tamaño aplicado por la persona."""
        self.cargar([[''] * len(self.celdas[0]) for _ in self.celdas])

    def copiar(self):
        """Copia valores válidos al portapapeles únicamente por acción de la persona."""
        try:
            texto = texto_matriz(self.leer())
            self.clipboard_clear()
            self.clipboard_append(texto)
        except (ValueError, tk.TclError) as error:
            self.informar_error(str(error))

    def pegar_texto(self, texto):
        """Valida el bloque completo y lo carga como una sola edición deshacible."""
        matriz = interpretar_matriz(texto, LIMITE_CUADRICULA)
        self.cargar(matriz)

    def pegar(self):
        """Pega una matriz del portapapeles sin alterar casillas si hay errores."""
        try:
            self.pegar_texto(self.clipboard_get())
        except (ValueError, tk.TclError) as error:
            self.informar_error(str(error))

    def _crear_area(self):
        """Crea desplazamiento horizontal y vertical para no recortar las casillas."""
        area = self.area = ttk.Frame(self, style="Interior.TFrame")
        area.pack(fill="both", expand=True, pady=(12, 0))
        area.columnconfigure(0, weight=1)
        area.rowconfigure(0, weight=1)
        self.lienzo = tk.Canvas(area, highlightthickness=0, height=138)
        self.tema.vincular(self.lienzo, bg="tarjeta")
        self.lienzo.grid(row=0, column=0, sticky="nsew")
        for orientacion, fila, columna in (("vertical", 0, 1), ("horizontal", 1, 0)):
            comando = self.lienzo.yview if orientacion == "vertical" else self.lienzo.xview
            barra = ttk.Scrollbar(area, orient=orientacion, command=comando)
            barra.grid(row=fila, column=columna, sticky="ns" if fila == 0 else "ew")
            eje = "x" if orientacion == "horizontal" else "y"
            self.lienzo.configure(**{f"{eje}scrollcommand": lambda inicio, fin, b=barra: ajustar_barra(b, inicio, fin)})
        self.rejilla = ttk.Frame(self.lienzo, style="Interior.TFrame")
        self.ventana_rejilla = self.lienzo.create_window((0, 0), window=self.rejilla, anchor="nw")
        self.rejilla.bind("<Configure>", self._ajustar_desplazamiento)
        self.lienzo.bind("<Configure>", self._ajustar_desplazamiento)

    def _ajustar_desplazamiento(self, evento=None):
        """Actualiza el área desplazable cuando cambian las dimensiones."""
        ancho = self.rejilla.winfo_reqwidth()
        alto = self.rejilla.winfo_reqheight()
        x = max(12, (self.lienzo.winfo_width() - ancho) / 2)
        self.lienzo.coords(self.ventana_rejilla, x, 0)
        self.lienzo.delete("corchete")
        for borde, direccion in ((x - 6, 1), (x + ancho + 5, -1)):
            self.lienzo.create_line(borde + 6 * direccion, 2, borde, 2,
                                   borde, alto - 2, borde + 6 * direccion, alto - 2,
                                   fill=self.tema.colores["texto"], width=2, tags="corchete")
        self.lienzo.configure(scrollregion=(0, 0, max(ancho + 30, self.lienzo.winfo_width()),
                                          max(alto, self.lienzo.winfo_height())))

    def actualizar_tema(self):
        """Actualiza los corchetes del editor al cambiar la paleta."""
        self._ajustar_desplazamiento()

    def cargar(self, matriz):
        """Llena el editor con una matriz sin compartir sus datos mutables."""
        self.cargando = True
        for widget in self.rejilla.winfo_children():
            widget.destroy()
        self.celdas = []
        self.vistas = []
        # Las trazas de dimensiones no deben acceder a casillas ya destruidas.
        self.variables = []
        self.filas.set(str(len(matriz)))
        self.columnas.set(str(len(matriz[0])))
        # Tk necesita conservar las variables mientras existan sus casillas.
        for i, valores in enumerate(matriz):
            fila = []
            vistas_fila = []
            for j, valor in enumerate(valores):
                variable = tk.StringVar(self, str(valor))
                self.variables.append(variable)
                entrada, vista = self._crear_celda(variable, i, j)
                variable.trace_add("write", self.al_cambiar)
                fila.append(entrada)
                vistas_fila.append(vista)
            self.celdas.append(fila)
            self.vistas.append(vistas_fila)
        self.lienzo.xview_moveto(0)
        self.lienzo.yview_moveto(0)
        self.tamano.configure(text=f'{len(matriz)} × {len(matriz[0])} · Cambiar')
        self.cargando = False
        self.al_cambiar()

    def _crear_celda(self, variable, fila, columna):
        """Alterna notación apilada y entrada de texto al enfocar una celda."""
        marco = ttk.Frame(self.rejilla, style="Interior.TFrame", width=64, height=54)
        marco.grid(row=fila + 1, column=columna + 1, padx=3, pady=3)
        marco.grid_propagate(False)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        entrada = ttk.Entry(marco, textvariable=variable, width=7, justify="center")
        entrada.grid(row=0, column=0, sticky="nsew")
        vista = Notacion(marco, self.tema, 54, 15)
        vista.rol_resaltado = "a" if self.nombre == "A" else "b"
        vista.grid(row=0, column=0, sticky="nsew")
        # El lienzo muestra fracciones; Tab y el clic siguen usando una entrada real.
        entrada.bind("<FocusIn>", lambda evento: vista.grid_remove())
        entrada.bind("<FocusOut>", lambda evento: self._mostrar_celda(entrada, vista, variable))
        vista.bind("<Button-1>", lambda evento: entrada.focus_set())
        variable.trace_add("write", lambda *args: self._mostrar_celda(entrada, vista, variable))
        self._mostrar_celda(entrada, vista, variable)
        return entrada, vista

    def _mostrar_celda(self, entrada, vista, variable):
        """Deja visibles las casillas vacías; los valores conservan su notación."""
        self._dibujar_celda(vista, variable)
        if not variable.get().strip() or entrada == entrada.focus_get():
            vista.grid_remove()
        else:
            vista.grid()

    def _dibujar_celda(self, vista, variable):
        """Muestra el valor exacto o el texto pendiente sin ocultar errores."""
        try:
            valor = convertir_numero(variable.get())
        except (ValueError, ZeroDivisionError):
            valor = variable.get()
        vista.master.configure(width=max(64, vista._ancho(valor) + 16))
        vista.mostrar_formula([valor])

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
        self.barra_dimensiones.pack_forget()
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

    def quitar_resaltado(self):
        """Devuelve todas las casillas al aspecto normal."""
        self.etiqueta_nombre.configure(text=f"Matriz {self.nombre}")
        for fila in self.celdas:
            for celda in fila:
                celda.configure(style="TEntry")
        for fila in self.vistas:
            for vista in fila:
                vista.resaltada = False
                vista.contexto = False
                vista.foco_producto = False
                vista.activa = None
                vista.actualizar_tema()

    def resaltar(self, fila, columna):
        """Resalta una posición y la lleva al área visible sin cambiar el foco."""
        self.quitar_resaltado()
        self.etiqueta_nombre.configure(text=f"Matriz {self.nombre} · {self.nombre}[{fila + 1},{columna + 1}]")
        self.celdas[fila][columna].configure(style="Activa.TEntry")
        vista = self.vistas[fila][columna]
        vista.resaltada = True
        vista.actualizar_tema()
        self.lienzo.xview_moveto(columna / len(self.celdas[0]))
        self.lienzo.yview_moveto(fila / len(self.celdas))

    def resaltar_fila(self, fila, par=None):
        """Señala una fila completa y, opcionalmente, el elemento del par activo."""
        posiciones = [(fila, j) for j in range(len(self.celdas[fila]))]
        foco = (fila, par) if par is not None else None
        self._resaltar_grupo(posiciones, foco, f"Fila {fila + 1}")

    def resaltar_columna(self, columna, par=None):
        """Señala una columna completa y, opcionalmente, el elemento del par activo."""
        posiciones = [(i, columna) for i in range(len(self.celdas))]
        foco = (par, columna) if par is not None else None
        self._resaltar_grupo(posiciones, foco, f"Columna {columna + 1}")

    def _resaltar_grupo(self, posiciones, foco, etiqueta):
        """Distingue contexto y par con bordes, manteniendo las entradas intactas."""
        self.quitar_resaltado()
        self.etiqueta_nombre.configure(text=f"Matriz {self.nombre} · {etiqueta}")
        for i, j in posiciones:
            self.celdas[i][j].configure(style="Activa.TEntry")
            vista = self.vistas[i][j]
            vista.resaltada = True
            vista.contexto = (i, j) != foco
            vista.foco_producto = (i, j) == foco
            vista.actualizar_tema()
        fila, columna = foco or posiciones[0]
        self.lienzo.xview_moveto(columna / len(self.celdas[0]))
        self.lienzo.yview_moveto(fila / len(self.celdas))
