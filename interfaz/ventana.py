"""Compone la calculadora y su desarrollo completo en pestañas internas.

Tema: sesión gráfica local de suma y resta, sin duplicar el núcleo.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from contextlib import contextmanager
from copy import deepcopy
import tkinter as tk
from tkinter import ttk

from interfaz.cuadricula import EditorMatriz
from interfaz.desarrollo import Desarrollo, crear_notacion
from interfaz.notacion import crear_icono_matrices
from interfaz.recorrido import ReproductorPasos
from interfaz.tema import Tema
from modulos.modulo_matrices import restar_matrices, sumar_matrices
from teoremas.resumen_teoremas import teoremas_matrices


class CalculadoraVentana:
    """Coordina las entradas y la revisión visual de resultados exactos."""

    def __init__(self, raiz):
        """Construye la sesión sin reproducir ni calcular automáticamente."""
        self.raiz = raiz
        self.resultado = None
        self.datos_calculo = None
        self.vigente = False
        self.reproductor = None
        self._cargando = True
        self.historial = []
        self.instantanea = None
        self.operacion = tk.StringVar(raiz, "sumar")
        self.estado = tk.StringVar(raiz, "Completa las matrices y pulsa Calcular.")
        raiz.title("Cuaderno de Álgebra Lineal — Matrices · Local")
        ancho = min(1440, raiz.winfo_screenwidth() - 80)
        alto = min(900, raiz.winfo_screenheight() - 90)
        raiz.geometry(f"{ancho}x{alto}")
        raiz.minsize(1120, 760)
        self.tema = Tema(raiz)
        self._crear_navegacion()
        self._crear_pestanas()
        self._crear_encabezado()
        self._crear_editores()
        self._crear_acciones()
        self._crear_previa()
        self._crear_desarrollo()
        self.reproductor = ReproductorPasos(
            raiz.after, raiz.after_cancel, self._mostrar_paso,
            lambda: 3000, self._actualizar_controles,
        )
        self.operacion.trace_add("write", self.marcar_cambio)
        raiz.protocol("WM_DELETE_WINDOW", self.cerrar)
        raiz.bind("<Control-Return>", self.calcular)
        self._cargando = False
        self.instantanea = self._capturar()
        self._actualizar_controles()

    def _crear_navegacion(self):
        """Muestra Matrices con su icono cuadrado y espacio para futuros temas."""
        self.lateral = tk.Frame(self.raiz, width=200)
        self.tema.vincular(self.lateral, bg="fondo")
        self.lateral.pack(side="left", fill="y")
        self.lateral.pack_propagate(False)
        self.marca = tk.Label(self.lateral, text="▦  CUADERNO DE\n    ÁLGEBRA", justify="left",
                              font=("Segoe UI", 13, "bold"))
        self.tema.vincular(self.marca, bg="fondo", fg="texto")
        self.marca.pack(anchor="w", padx=16, pady=(24, 36))
        self.titulo_temas = tk.Label(self.lateral, text="TEMAS", font=("Segoe UI", 10, "bold"))
        self.tema.vincular(self.titulo_temas, bg="fondo", fg="secundario")
        self.titulo_temas.pack(anchor="w", padx=18, pady=(0, 14))
        self.tema_activo = tk.Frame(self.lateral, padx=10, pady=9)
        self.tema.vincular(self.tema_activo, bg="acento")
        self.tema_activo.pack(fill="x", padx=10)
        crear_icono_matrices(self.tema_activo, self.tema).pack(side="left")
        self.nombre_tema = tk.Label(self.tema_activo, text="Matrices", font=("Segoe UI", 11, "bold"))
        self.tema.vincular(self.nombre_tema, bg="acento", fg="sobre_acento")
        self.nombre_tema.pack(side="left", padx=8)
        self.nota_temas = tk.Label(self.lateral, text="Más temas se añadirán aquí", wraplength=170,
                                   font=("Segoe UI", 9, "italic"), justify="left")
        self.tema.vincular(self.nota_temas, bg="fondo", fg="secundario")
        self.nota_temas.pack(side="bottom", padx=16, pady=24)

    def _crear_pestanas(self):
        """Crea dos vistas internas que comparten la misma sesión."""
        self.zona = ttk.Frame(self.raiz, padding=(0, 12, 16, 12))
        self.zona.pack(side="left", fill="both", expand=True)
        self.pestanas = ttk.Notebook(self.zona)
        self.pestanas.pack(fill="both", expand=True)
        self.contenido = ttk.Frame(self.pestanas, padding=(18, 8))
        self.pagina_pasos = ttk.Frame(self.pestanas, padding=(18, 8))
        self.pestanas.add(self.contenido, text="▦  Calculadora")
        self.pestanas.add(self.pagina_pasos, text="☷  Todos los pasos")
        self.pestanas.bind("<<NotebookTabChanged>>", self._cambiar_pestana)
        self.boton_tema = ttk.Button(self.zona, text="☀  Modo claro", command=self.alternar_tema)
        self.boton_tema.place(relx=1, x=-18, y=0, anchor="ne")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(1, weight=1)
        self.contenido.rowconfigure(3, weight=1)

    def _crear_encabezado(self):
        """Presenta suma y resta con las acciones de ejemplo y consulta existentes."""
        marco = ttk.Frame(self.contenido)
        marco.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(marco, text="Álgebra lineal  /  Matrices", style="Subtitulo.TLabel").pack(anchor="w")
        ttk.Label(marco, text="Operaciones con matrices", style="Titulo.TLabel").pack(anchor="w", pady=(6, 12))
        barra = ttk.Frame(marco)
        barra.pack(fill="x")
        for texto, valor in (("Suma", "sumar"), ("Resta", "restar")):
            ttk.Radiobutton(barra, text=texto, value=valor, variable=self.operacion).pack(side="left")
        ttk.Button(barra, text="Cargar ejemplo", command=self.cargar_ejemplo).pack(side="left", padx=18)
        ttk.Button(barra, text="Teoremas", command=self.ver_teoremas).pack(side="right")

    def _crear_editores(self):
        """Distribuye A, B y el resultado de solo lectura en tres tarjetas."""
        tarjetas = ttk.Frame(self.contenido)
        tarjetas.grid(row=1, column=0, sticky="nsew")
        tarjetas.rowconfigure(0, weight=1)
        for columna in range(3):
            tarjetas.columnconfigure(columna, weight=1, uniform="matrices")
        self.editor_a = EditorMatriz(tarjetas, "A", self.marcar_cambio, self.mostrar_error, self.tema)
        self.editor_b = EditorMatriz(tarjetas, "B", self.marcar_cambio, self.mostrar_error, self.tema)
        self.editor_a.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self.editor_b.grid(row=0, column=1, sticky="nsew", padx=6)
        tarjeta = ttk.Frame(tarjetas, style="Tarjeta.TFrame", padding=14)
        tarjeta.grid(row=0, column=2, sticky="nsew", padx=(6, 0))
        ttk.Label(tarjeta, text="Resultado", style="TarjetaTitulo.TLabel").pack(anchor="w")
        self.etiqueta_resultado = ttk.Label(tarjeta, text="Solo lectura · Aún no hay un cálculo", style="Coordenada.TLabel")
        self.etiqueta_resultado.pack(anchor="w", pady=(4, 8))
        botones = ttk.Frame(tarjeta, style="Interior.TFrame")
        botones.pack(side="bottom", fill="x", pady=(12, 0))
        self.usar_a = ttk.Button(botones, text="Usar como A", command=lambda: self.reutilizar("A"), state="disabled")
        self.usar_b = ttk.Button(botones, text="Usar como B", command=lambda: self.reutilizar("B"), state="disabled")
        self.usar_a.pack(side="left", expand=True)
        self.usar_b.pack(side="left", expand=True)
        self.vista_resultado = crear_notacion(tarjeta, self.tema, 138, 16)
        self.vista_resultado.mostrar_formula(["Sin resultado"])

    def _crear_acciones(self):
        """Añade cálculo, limpieza, deshacer y mensajes recuperables."""
        marco = ttk.Frame(self.contenido)
        marco.grid(row=2, column=0, sticky="ew", pady=(12, 10))
        for texto, comando, estilo in (("▶  Calcular", self.calcular, "Principal.TButton"),
                                       ("Limpiar", self.limpiar, "TButton")):
            ttk.Button(marco, text=texto, command=comando, style=estilo).pack(side="left", padx=(0, 10))
        self.boton_deshacer = ttk.Button(marco, text="↶  Deshacer", command=self.deshacer, state="disabled")
        self.boton_deshacer.pack(side="left", padx=(0, 16))
        self.etiqueta_estado = ttk.Label(marco, textvariable=self.estado, style="Estado.TLabel", wraplength=470)
        self.etiqueta_estado.pack(side="left", fill="x", expand=True)

    def _crear_previa(self):
        """Ofrece tres puntos clave y un ejemplo, reservando el detalle a otra pestaña."""
        tarjeta = ttk.Frame(self.contenido, style="Tarjeta.TFrame", padding=14)
        tarjeta.grid(row=3, column=0, sticky="nsew")
        ttk.Label(tarjeta, text="Vista previa del procedimiento", style="TarjetaTitulo.TLabel").pack(anchor="w")
        self.progreso = ttk.Label(tarjeta, text="", style="Coordenada.TLabel")
        self.progreso.pack(side="bottom", anchor="w", pady=(5, 0))
        interior = ttk.Frame(tarjeta, style="Interior.TFrame")
        interior.columnconfigure(0, weight=1)
        interior.columnconfigure(1, weight=1)
        interior.rowconfigure(0, weight=1)
        self.resumen = ttk.Label(interior, text="Calcula para ver los puntos clave.\n\nEnteros: 2, −3  ·  Decimales: 0.5  ·  Fracciones: 1/3",
                                  style="Tarjeta.TLabel", wraplength=410, justify="left")
        self.resumen.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        ejemplo = ttk.Frame(interior, style="Interior.TFrame")
        ejemplo.grid(row=0, column=1, sticky="nsew")
        self.coordenada_previa = ttk.Label(ejemplo, text="Ejemplo del cálculo", style="Coordenada.TLabel")
        self.coordenada_previa.pack(anchor="center")
        self.formula_previa = crear_notacion(ejemplo, self.tema, 85, 18)
        barra = ttk.Frame(tarjeta, style="Interior.TFrame")
        barra.pack(side="bottom", fill="x", pady=(6, 0))
        self.boton_anterior = ttk.Button(barra, text="‹ Anterior", command=lambda: self.reproductor.anterior())
        self.boton_reproducir = ttk.Button(barra, text="▶ Reproducir", style="Principal.TButton", command=self.alternar_recorrido)
        self.boton_siguiente = ttk.Button(barra, text="Siguiente ›", command=lambda: self.reproductor.siguiente())
        self.boton_reiniciar = ttk.Button(barra, text="↶ Reiniciar", command=self.reiniciar_recorrido)
        self.boton_todo = ttk.Button(barra, text="Abrir todos los pasos ↗", command=self.ver_todo)
        for boton in (self.boton_anterior, self.boton_reproducir, self.boton_siguiente, self.boton_reiniciar):
            boton.pack(side="left", padx=(0, 6))
        self.boton_todo.pack(side="right")
        interior.pack(fill="both", expand=True, pady=(8, 6))

    def _crear_desarrollo(self):
        """Prepara una vista amplia con desplazamiento y retorno sin borrar entradas."""
        ttk.Label(self.pagina_pasos, text="Desarrollo completo", style="Titulo.TLabel").pack(anchor="w", pady=(0, 6))
        self.subtitulo_pasos = ttk.Label(self.pagina_pasos, text="Suma y resta de matrices", style="Subtitulo.TLabel")
        self.subtitulo_pasos.pack(anchor="w", pady=(0, 12))
        pie = ttk.Frame(self.pagina_pasos)
        pie.pack(side="bottom", fill="x", pady=(12, 0))
        ttk.Button(pie, text="‹  Volver a calculadora", command=lambda: self.pestanas.select(self.contenido)).pack(side="left")
        ttk.Label(pie, text="Desplázate para revisar desarrollos largos", style="Subtitulo.TLabel").pack(side="right")
        self.desarrollo = Desarrollo(self.pagina_pasos, self.tema)
        self.desarrollo.pack(fill="both", expand=True)

    def _cambiar_pestana(self, evento=None):
        """Libera espacio lateral en el desarrollo y pausa movimientos ocultos."""
        ampliada = self.pestanas.select() == str(self.pagina_pasos)
        if self.reproductor is not None:
            self.reproductor.pausar()
        self.lateral.configure(width=68 if ampliada else 200)
        for widget in (self.marca, self.titulo_temas, self.nombre_tema, self.nota_temas):
            if ampliada:
                widget.pack_forget()
        if not ampliada:
            self.marca.pack(anchor="w", padx=16, pady=(24, 36), before=self.tema_activo)
            self.titulo_temas.pack(anchor="w", padx=18, pady=(0, 14), before=self.tema_activo)
            self.nombre_tema.pack(side="left", padx=8)
            self.nota_temas.pack(side="bottom", padx=16, pady=24)

    def alternar_tema(self):
        """Cambia solo los colores, preservando entradas y desarrollo."""
        self.tema.alternar()
        self.boton_tema.configure(text="☀  Modo claro" if self.tema.oscuro else "☾  Modo oscuro")

    def ver_teoremas(self):
        """Conserva la consulta teórica existente en una ventana de solo lectura."""
        ventana = tk.Toplevel(self.raiz)
        ventana.title("Teoremas de matrices")
        ventana.geometry("760x430")
        texto = tk.Text(ventana, wrap="word", font=("Segoe UI", 11), padx=20, pady=20)
        self.tema.vincular(texto, bg="tarjeta", fg="texto")
        texto.pack(fill="both", expand=True)
        texto.insert("1.0", teoremas_matrices().strip())
        texto.configure(state="disabled")

    def _actualizar_controles(self):
        """Sincroniza progreso y disponibilidad con el cálculo vigente."""
        reproductor = self.reproductor
        disponibles = reproductor is not None and bool(reproductor.pasos)
        for boton in (self.boton_anterior, self.boton_reproducir, self.boton_siguiente,
                      self.boton_reiniciar, self.boton_todo):
            boton.configure(state="normal" if disponibles else "disabled")
        self.boton_reproducir.configure(text="Ⅱ Pausar" if disponibles and reproductor.activo else "▶ Reproducir")
        if disponibles:
            self.boton_anterior.configure(state="normal" if reproductor.indice > 0 else "disabled")
            self.boton_siguiente.configure(state="normal" if reproductor.indice < len(reproductor.pasos) - 1 else "disabled")
            self.progreso.configure(text=f"Paso {max(0, reproductor.indice + 1)} de {len(reproductor.pasos)} · 3 segundos por paso")
        else:
            self.progreso.configure(text="Ctrl + Enter para calcular · El recorrido comienza cuando lo solicitas")
        self.boton_deshacer.configure(state="normal" if self.historial else "disabled")

    def _pasos_calculo(self):
        """Devuelve posiciones y valores del último resultado, sin recalcularlo."""
        if self.datos_calculo is None:
            return []
        a, b, signo = self.datos_calculo
        return [(i, j, a[i][j], b[i][j], valor, signo)
                for i, fila in enumerate(self.resultado) for j, valor in enumerate(fila)]

    def _presentar_calculo(self):
        """Actualiza ambas vistas a partir del resultado guardado."""
        if self.resultado is None:
            self.vista_resultado.mostrar_formula(["Sin resultado"])
            self.formula_previa.mostrar_formula([])
            self.resumen.configure(text="Calcula para ver los puntos clave.\n\nEnteros: 2, −3 · Decimales: 0.5 · Fracciones: 1/3")
            self.coordenada_previa.configure(text="Ejemplo del cálculo")
            self.etiqueta_resultado.configure(text="Solo lectura · Aún no hay un cálculo")
            self.desarrollo.mostrar([], None)
        else:
            pasos = self._pasos_calculo()
            self.vista_resultado.mostrar_matriz(self.resultado)
            self.desarrollo.mostrar(pasos, self.resultado)
            filas, columnas = len(self.resultado), len(self.resultado[0])
            self.resumen.configure(text=f"① A y B tienen dimensiones {filas} × {columnas}.\n\n② Operamos los elementos de la misma posición.\n\n③ Conservamos las fracciones exactas.")
            self._mostrar_formula(pasos[min(1, len(pasos) - 1)])
            signo = self.datos_calculo[2]
            self.etiqueta_resultado.configure(text=f"A {signo} B · {filas} × {columnas} · Solo lectura" if self.vigente else "Último cálculo · datos modificados")
            self.subtitulo_pasos.configure(text=f"{'Suma' if signo == '+' else 'Resta'} de matrices · A {signo} B")
            if not self.vigente:
                self.desarrollo.aviso.configure(text="Último cálculo · Las entradas cambiaron. Vuelve a calcular para actualizar.")
        self.reproductor.preparar(self._pasos_calculo() if self.vigente else ())
        for boton in (self.usar_a, self.usar_b):
            boton.configure(state="normal" if self.resultado is not None else "disabled")

    def _mostrar_formula(self, paso):
        """Muestra solo una igualdad importante en la vista previa."""
        fila, columna, a, b, resultado, signo = paso
        tokens = [a, signo] + (["(", b, ")"] if b < 0 else [b]) + ["=", resultado]
        self.formula_previa.mostrar_formula(tokens)
        self.coordenada_previa.configure(text=f"Fila {fila + 1} · Columna {columna + 1}")

    def _mostrar_paso(self, paso, indice, total):
        """Resalta operandos y revela posiciones sin alterar el resultado guardado."""
        fila, columna = paso[:2]
        self.editor_a.resaltar(fila, columna)
        self.editor_b.resaltar(fila, columna)
        columnas = len(self.resultado[0])
        parcial = [[valor if i * columnas + j <= indice else "·" for j, valor in enumerate(valores)]
                   for i, valores in enumerate(self.resultado)]
        self.vista_resultado.mostrar_matriz(parcial, (fila, columna))
        self._mostrar_formula(paso)

    def alternar_recorrido(self):
        """Alterna reproducción y pausa sin recalcular las matrices."""
        if self.reproductor.activo:
            self.reproductor.pausar()
        else:
            self.reproductor.reproducir()

    def reiniciar_recorrido(self):
        """Vuelve al primer paso en pausa, sin arrancar movimiento automático."""
        self.reproductor.reiniciar()

    def ver_todo(self):
        """Abre la pestaña amplia y muestra el resultado entero en la calculadora."""
        self.reproductor.pausar()
        if self.resultado is not None:
            self.vista_resultado.mostrar_matriz(self.resultado)
        self.editor_a.quitar_resaltado()
        self.editor_b.quitar_resaltado()
        self.pestanas.select(self.pagina_pasos)

    def _invalidar_recorrido(self):
        """Cancela temporizadores y marca como anterior el cálculo visible."""
        self.vigente = False
        if self.reproductor is not None:
            self.reproductor.preparar(())
            self.editor_a.quitar_resaltado()
            self.editor_b.quitar_resaltado()
            if self.resultado is not None:
                self.vista_resultado.mostrar_matriz(self.resultado)
                self.etiqueta_resultado.configure(text="Último cálculo · datos modificados")
                self.desarrollo.aviso.configure(text="Último cálculo · Las entradas cambiaron. Vuelve a calcular para actualizar.")

    def _capturar(self):
        """Copia entradas, dimensiones pendientes y último cálculo para deshacer."""
        entradas = []
        for editor in (self.editor_a, self.editor_b):
            entradas.append(([[celda.get() for celda in fila] for fila in editor.celdas],
                             editor.filas.get(), editor.columnas.get()))
        return deepcopy(dict(entradas=entradas, operacion=self.operacion.get(), resultado=self.resultado,
                             datos=self.datos_calculo, vigente=self.vigente, estado=self.estado.get()))

    def _recordar(self):
        """Conserva hasta cincuenta estados anteriores de esta sesión."""
        if self.instantanea is not None:
            self.historial.append(self.instantanea)
            self.historial = self.historial[-50:]

    @contextmanager
    def _edicion(self):
        """Agrupa la carga o limpieza como una sola acción deshacible."""
        self._recordar()
        self._cargando = True
        self._invalidar_recorrido()
        try:
            yield
        finally:
            self._cargando = False
            self.instantanea = self._capturar()
            self._actualizar_controles()

    def marcar_cambio(self, *argumentos):
        """Invalida pasos viejos y registra modificaciones sin leer widgets destruidos."""
        if self._cargando or any(getattr(self, nombre, None) is not None and
                                getattr(self, nombre).cargando for nombre in ("editor_a", "editor_b")):
            return
        nueva = self._capturar()
        if self.instantanea and (nueva["entradas"], nueva["operacion"]) == (self.instantanea["entradas"], self.instantanea["operacion"]):
            return
        self._recordar()
        self._invalidar_recorrido()
        self.estado.set("Datos modificados. Pulsa Calcular para actualizar.")
        self.etiqueta_estado.configure(style="Estado.TLabel")
        self.instantanea = self._capturar()
        self._actualizar_controles()

    def deshacer(self):
        """Restaura la acción anterior con sus entradas y cálculo conservado."""
        if not self.historial:
            return
        anterior = self.historial.pop()
        self._cargando = True
        self._invalidar_recorrido()
        for editor, (matriz, filas, columnas) in zip((self.editor_a, self.editor_b), anterior["entradas"]):
            editor.cargar(matriz)
            editor.filas.set(filas)
            editor.columnas.set(columnas)
        self.operacion.set(anterior["operacion"])
        self.resultado, self.datos_calculo = anterior["resultado"], anterior["datos"]
        self.vigente = anterior["vigente"]
        self.estado.set(anterior["estado"])
        self.etiqueta_estado.configure(style="Estado.TLabel")
        self._presentar_calculo()
        self._cargando = False
        self.instantanea = self._capturar()
        self._actualizar_controles()

    def mostrar_error(self, mensaje):
        """Conserva los datos y el último cálculo cuando una entrada es inválida."""
        self.estado.set(mensaje)
        self.etiqueta_estado.configure(style="Error.TLabel")
        if self.resultado is not None:
            self.etiqueta_resultado.configure(text="Último cálculo · revisa los datos")

    def calcular(self, evento=None):
        """Lee los editores y llama al mismo núcleo que usa la consola."""
        self._invalidar_recorrido()
        try:
            a, b = self.editor_a.leer(), self.editor_b.leer()
            sumar = self.operacion.get() == "sumar"
            resultado = sumar_matrices(a, b) if sumar else restar_matrices(a, b)
        except ValueError as error:
            self.mostrar_error(str(error))
            return "break"
        self._recordar()
        self.resultado = resultado
        self.datos_calculo = (a, b, "+" if sumar else "-")
        self.vigente = True
        self._presentar_calculo()
        self.etiqueta_estado.configure(style="Estado.TLabel")
        self.estado.set("Cálculo completado · Dimensiones compatibles")
        self.instantanea = self._capturar()
        self._actualizar_controles()
        return "break"

    def reutilizar(self, destino):
        """Copia el último resultado al editor elegido como una acción deshacible."""
        if self.resultado is not None:
            with self._edicion():
                (self.editor_a if destino == "A" else self.editor_b).cargar(self.resultado)
                self.estado.set("Resultado copiado. Pulsa Calcular para actualizar.")

    def cargar_ejemplo(self):
        """Carga las matrices exactas de la maqueta aprobada sin calcular todavía."""
        with self._edicion():
            self.editor_a.cargar([["1/3", "1/10"], ["-2", "4"]])
            self.editor_b.cargar([["1/6", "1/5"], ["5", "-1"]])
            self.operacion.set("sumar")
            self.estado.set("Ejemplo cargado. Pulsa Calcular.")

    def limpiar(self):
        """Reinicia la sesión visible y permite deshacer esta acción."""
        with self._edicion():
            self.resultado = None
            self.datos_calculo = None
            self.editor_a.cargar([[0, 0], [0, 0]])
            self.editor_b.cargar([[0, 0], [0, 0]])
            self.operacion.set("sumar")
            self._presentar_calculo()
            self.estado.set("Completa las matrices y pulsa Calcular.")
            self.etiqueta_estado.configure(style="Estado.TLabel")

    def cerrar(self):
        """Cancela eventos pendientes antes de destruir la ventana."""
        self.reproductor.pausar()
        self.raiz.destroy()


def iniciar_ventana():
    """Abre la ventana local hasta que la persona cierre su sesión."""
    raiz = tk.Tk()
    CalculadoraVentana(raiz)
    raiz.mainloop()
