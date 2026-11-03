"""Presenta suma y resta en una ventana sin duplicar los algoritmos.

Tema: edición gráfica y explicación de operaciones matriciales.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
from tkinter import ttk

from interfaz.cuadricula import EditorMatriz
from interfaz.formato import formatear_matriz, formatear_procedimiento
from modulos.modulo_matrices import restar_matrices, sumar_matrices
from teoremas.resumen_teoremas import teoremas_matrices

FONDO = "#f3f5f9"
AZUL = "#172a45"
VERDE = "#156b65"


def preparar_estilos(raiz):
    """Configura una apariencia común legible en Windows y Linux."""
    raiz.configure(bg=FONDO)
    estilo = ttk.Style(raiz)
    estilo.theme_use("clam")
    estilo.configure(".", font=("Segoe UI", 10))
    estilo.configure("TFrame", background=FONDO)
    estilo.configure("TLabel", background=FONDO, foreground=AZUL)
    estilo.configure("Titulo.TLabel", font=("Segoe UI", 25, "bold"))
    estilo.configure("Subtitulo.TLabel", foreground="#59677c")
    estilo.configure("Tarjeta.TFrame", background="white")
    estilo.configure("Tarjeta.TLabel", background="white", foreground="#59677c")
    estilo.configure("TarjetaTitulo.TLabel", background="white", font=("Segoe UI", 13, "bold"))
    estilo.configure("Coordenada.TLabel", background="white", foreground="#748095")
    estilo.configure("Estado.TLabel", foreground=VERDE, padding=(0, 8))
    estilo.configure("Error.TLabel", foreground="#a62836", padding=(0, 8))
    estilo.configure("TButton", padding=(10, 7), font=("Segoe UI", 10),
                      background="#e8eef4", foreground=AZUL, bordercolor="#d5dee8")
    estilo.map("TButton", background=[("active", "#dce6f0")])
    estilo.configure("TEntry", fieldbackground="white", bordercolor="#c9d4e2")
    estilo.configure("TSpinbox", fieldbackground="white", bordercolor="#c9d4e2")
    estilo.configure("Vertical.TScrollbar", background="#d3dce8", troughcolor="#f4f6fa", borderwidth=0)
    estilo.configure("Horizontal.TScrollbar", background="#d3dce8", troughcolor="#f4f6fa", borderwidth=0)
    estilo.configure("Principal.TButton", background=VERDE, foreground="white", padding=(24, 10))
    estilo.map("Principal.TButton", background=[("active", "#10534e")])
    estilo.configure("TRadiobutton", background=FONDO, foreground=AZUL, padding=(8, 6))
    estilo.configure("TNotebook", background=FONDO, borderwidth=0)
    estilo.configure("TNotebook.Tab", padding=(18, 8))
    estilo.map("TNotebook.Tab", background=[("selected", "white"), ("!selected", "#e8eef4")])


def escribir_texto(widget, texto):
    """Sustituye el contenido de un área de lectura sin permitir edición."""
    widget.configure(state="normal")
    widget.delete("1.0", "end")
    widget.insert("1.0", texto)
    widget.configure(state="disabled")
    widget.yview_moveto(0)
    widget.xview_moveto(0)


def crear_texto(padre, fuente, alto):
    """Crea un área de lectura con barras horizontal y vertical."""
    marco = ttk.Frame(padre, style="Tarjeta.TFrame")
    marco.pack(fill="both", expand=True)
    marco.rowconfigure(0, weight=1)
    marco.columnconfigure(0, weight=1)
    texto = tk.Text(marco, wrap="none", font=fuente, height=alto, width=10,
                    bg="white", fg=AZUL, relief="flat", padx=12, pady=12,
                    state="disabled", selectbackground="#c5e7e3")
    texto.grid(row=0, column=0, sticky="nsew")
    for eje, orientacion, fila, columna in (("y", "vertical", 0, 1), ("x", "horizontal", 1, 0)):
        comando = texto.yview if eje == "y" else texto.xview
        barra = ttk.Scrollbar(marco, orient=orientacion, command=comando)
        barra.grid(row=fila, column=columna, sticky="ns" if eje == "y" else "ew")
        texto.configure(**{f"{eje}scrollcommand": barra.set})
    return texto


class CalculadoraVentana:
    """Coordina editores, operaciones y estado de la sesión gráfica."""

    def __init__(self, raiz):
        """Construye la ventana; el resultado solo existe dentro de esta sesión."""
        self.raiz = raiz
        self.resultado = None
        self.operacion = tk.StringVar(raiz, "sumar")
        self.estado = tk.StringVar(raiz, "Completa las matrices y pulsa Calcular.")
        raiz.title("Cuaderno de Álgebra Lineal — Matrices")
        raiz.geometry("1280x820")
        raiz.minsize(1120, 760)
        preparar_estilos(raiz)
        self._crear_navegacion()
        self.contenido = ttk.Frame(raiz, padding=(26, 22))
        self.contenido.pack(side="left", fill="both", expand=True)
        self._crear_encabezado()
        self._crear_editores()
        self._crear_acciones()
        self._crear_detalles()
        self.operacion.trace_add("write", self.marcar_cambio)
        raiz.bind("<Control-Return>", self.calcular)
        self.editor_a.celdas[0][0].focus_set()

    def _crear_navegacion(self):
        """Muestra el tema activo y una guía breve de entrada."""
        lateral = tk.Frame(self.raiz, bg=AZUL, width=185)
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)
        tk.Label(lateral, text="CUADERNO\nDE ÁLGEBRA", bg=AZUL, fg="white",
                 justify="left", font=("Segoe UI", 17, "bold")).pack(anchor="w", padx=22, pady=(30, 8))
        tk.Label(lateral, text="Aprende paso a paso", bg=AZUL, fg="#afc2d8").pack(anchor="w", padx=22)
        tk.Label(lateral, text="TEMAS DISPONIBLES", bg=AZUL, fg="#afc2d8",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22, pady=(45, 12))
        tk.Label(lateral, text="  Matrices", bg="#2a405e", fg="white", anchor="w",
                 padx=15, pady=12, font=("Segoe UI", 12, "bold")).pack(fill="x", padx=12)
        tk.Label(lateral, text="NÚMEROS ADMITIDOS\n\nEnteros: 2, -3\nDecimales: 0.5\nFracciones: 1/3",
                 bg=AZUL, fg="#cedaea", justify="left", font=("Segoe UI", 10)).pack(anchor="w", padx=22, pady=(40, 10))
        tk.Label(lateral, text="Ctrl + Enter\npara calcular", bg=AZUL, fg="#afc2d8",
                 justify="left").pack(side="bottom", anchor="w", padx=22, pady=25)

    def _crear_encabezado(self):
        """Presenta la tarea y la selección entre suma y resta."""
        ttk.Label(self.contenido, text="ÁLGEBRA LINEAL  /  OPERACIONES", style="Subtitulo.TLabel").pack(anchor="w")
        ttk.Label(self.contenido, text="Trabajemos con matrices", style="Titulo.TLabel").pack(anchor="w", pady=(6, 4))
        ttk.Label(self.contenido, text="1. Elige el tamaño    2. Completa las casillas    3. Calcula y revisa los pasos",
                  style="Subtitulo.TLabel").pack(anchor="w", pady=(0, 12))
        operaciones = ttk.Frame(self.contenido)
        operaciones.pack(fill="x", pady=(0, 12))
        for texto, valor in (("Sumar  A + B", "sumar"), ("Restar  A − B", "restar")):
            ttk.Radiobutton(operaciones, text=texto, variable=self.operacion, value=valor).pack(side="left", padx=(0, 18))

    def _crear_editores(self):
        """Distribuye las matrices A, B y su resultado en tres tarjetas."""
        tarjetas = ttk.Frame(self.contenido)
        tarjetas.pack(fill="both", expand=True)
        tarjetas.rowconfigure(0, weight=1)
        for columna in range(3):
            tarjetas.columnconfigure(columna, weight=1, uniform="tarjetas")
        self.editor_a = EditorMatriz(tarjetas, "A", self.marcar_cambio, self.mostrar_error)
        self.editor_b = EditorMatriz(tarjetas, "B", self.marcar_cambio, self.mostrar_error)
        self.editor_a.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.editor_b.grid(row=0, column=1, sticky="nsew", padx=8)
        self._crear_resultado(tarjetas)

    def _crear_resultado(self, padre):
        """Crea la vista de resultado y las acciones para reutilizarlo."""
        tarjeta = ttk.Frame(padre, style="Tarjeta.TFrame", padding=18)
        tarjeta.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        ttk.Label(tarjeta, text="Resultado", style="TarjetaTitulo.TLabel").pack(anchor="w")
        self.etiqueta_resultado = ttk.Label(tarjeta, text="Aún no hay un cálculo", style="Tarjeta.TLabel")
        self.etiqueta_resultado.pack(anchor="w", pady=(12, 14))
        self.texto_resultado = crear_texto(tarjeta, ("Consolas", 13), 7)
        escribir_texto(self.texto_resultado, "Tu resultado aparecerá aquí.")
        botones = ttk.Frame(tarjeta, style="Tarjeta.TFrame")
        botones.pack(fill="x", pady=(12, 0))
        self.usar_a = ttk.Button(botones, text="Usar como A", command=lambda: self.reutilizar("A"), state="disabled")
        self.usar_b = ttk.Button(botones, text="Usar como B", command=lambda: self.reutilizar("B"), state="disabled")
        self.usar_a.pack(side="left", padx=(0, 5))
        self.usar_b.pack(side="left")

    def _crear_acciones(self):
        """Añade acciones de cálculo, ejemplo y limpieza y un estado visible."""
        acciones = ttk.Frame(self.contenido)
        acciones.pack(fill="x", pady=(18, 4))
        ttk.Button(acciones, text="Calcular", style="Principal.TButton", command=self.calcular).pack(side="left", padx=(0, 10))
        ttk.Button(acciones, text="Cargar ejemplo", command=self.cargar_ejemplo).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Limpiar", command=self.limpiar).pack(side="left")
        self.etiqueta_estado = ttk.Label(self.contenido, textvariable=self.estado, style="Estado.TLabel", wraplength=850)
        self.etiqueta_estado.pack(fill="x", pady=(0, 8))

    def _crear_detalles(self):
        """Separa los pasos de la operación de los teoremas de consulta."""
        pestañas = ttk.Notebook(self.contenido)
        pestañas.pack(fill="both", expand=True)
        pasos = ttk.Frame(pestañas, style="Tarjeta.TFrame")
        teoria = ttk.Frame(pestañas, style="Tarjeta.TFrame")
        pestañas.add(pasos, text="Procedimiento")
        pestañas.add(teoria, text="Teoremas clave")
        self.texto_pasos = crear_texto(pasos, ("Consolas", 11), 7)
        escribir_texto(self.texto_pasos, "Después de calcular verás cómo se obtuvo cada elemento.")
        texto_teoria = crear_texto(teoria, ("Consolas", 11), 7)
        escribir_texto(texto_teoria, teoremas_matrices().strip())

    def marcar_cambio(self, *argumentos):
        """Distingue el resultado anterior de unas entradas que aún no se calcularon."""
        self.estado.set("Datos modificados. Pulsa Calcular para obtener el nuevo resultado.")
        if hasattr(self, "etiqueta_estado"):
            self.etiqueta_estado.configure(style="Estado.TLabel")
        if self.resultado is not None:
            self.etiqueta_resultado.configure(text="Último cálculo · datos modificados")

    def mostrar_error(self, mensaje):
        """Presenta un error recuperable conservando entradas y último cálculo."""
        self.estado.set(mensaje)
        self.etiqueta_estado.configure(style="Error.TLabel")
        if self.resultado is not None:
            self.etiqueta_resultado.configure(text="Último cálculo · revisa los datos")

    def calcular(self, evento=None):
        """Lee las casillas y llama al mismo cálculo que usa la consola."""
        try:
            matriz_a = self.editor_a.leer()
            matriz_b = self.editor_b.leer()
            if self.operacion.get() == "sumar":
                resultado = sumar_matrices(matriz_a, matriz_b)
                signo = "+"
            else:
                resultado = restar_matrices(matriz_a, matriz_b)
                signo = "-"
        except ValueError as error:
            self.mostrar_error(str(error))
            return "break"
        self.resultado = resultado
        escribir_texto(self.texto_resultado, formatear_matriz(resultado))
        escribir_texto(self.texto_pasos, formatear_procedimiento(matriz_a, matriz_b, resultado, signo))
        self.etiqueta_resultado.configure(text=f"A {signo} B · {len(resultado)} × {len(resultado[0])}")
        self.usar_a.configure(state="normal")
        self.usar_b.configure(state="normal")
        self.etiqueta_estado.configure(style="Estado.TLabel")
        self.estado.set("Cálculo completado. Puedes revisar el procedimiento o reutilizar el resultado.")
        return "break"

    def reutilizar(self, destino):
        """Carga el último resultado como A o B sin pedir que se reescriba."""
        if self.resultado is not None:
            editor = self.editor_a if destino == "A" else self.editor_b
            editor.cargar(self.resultado)
            self.marcar_cambio()

    def cargar_ejemplo(self):
        """Carga un ejemplo 2x2 de suma con enteros y fracciones."""
        self.editor_a.cargar([["1/3", "0.1"], ["-2", "4"]])
        self.editor_b.cargar([["1/6", "0.2"], ["5", "-1"]])
        self.operacion.set("sumar")
        self.marcar_cambio()
        self.editor_a.celdas[0][0].focus_set()

    def limpiar(self):
        """Reinicia datos y resultado de esta sesión gráfica."""
        self.resultado = None
        self.editor_a.cargar([[0, 0], [0, 0]])
        self.editor_b.cargar([[0, 0], [0, 0]])
        self.operacion.set("sumar")
        self.etiqueta_resultado.configure(text="Aún no hay un cálculo")
        escribir_texto(self.texto_resultado, "Tu resultado aparecerá aquí.")
        escribir_texto(self.texto_pasos, "Después de calcular verás cómo se obtuvo cada elemento.")
        self.usar_a.configure(state="disabled")
        self.usar_b.configure(state="disabled")
        self.estado.set("Completa las matrices y pulsa Calcular.")
        self.editor_a.celdas[0][0].focus_set()


def iniciar_ventana():
    """Abre la ventana local y atiende los eventos hasta que se cierre."""
    raiz = tk.Tk()
    CalculadoraVentana(raiz)
    raiz.mainloop()
