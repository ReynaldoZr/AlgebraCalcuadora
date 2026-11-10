"""Compone la calculadora y su desarrollo completo en pestañas internas.

Tema: sesión gráfica de suma, resta y escalar, sin duplicar el núcleo.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from contextlib import contextmanager
from copy import deepcopy
import tkinter as tk
from tkinter import ttk

from interfaz.cuadricula import EditorMatriz
from interfaz.desarrollo import Desarrollo, crear_notacion
from interfaz.datos import convertir_numero
from interfaz.explicacion import construir_etapas
from interfaz.recorrido import INTERVALO_PASOS_MS, ReproductorPasos
from interfaz.tema import Tema
from interfaz.transicion import TransicionVistas
from modulos.modulo_matrices import (multiplicar_por_escalar, producto_matricial, restar_matrices,
                                     sumar_matrices, transponer_matriz)
from teoremas.resumen_teoremas import teoremas_matrices


class CalculadoraVentana:
    """Coordina las entradas y la revisión visual de resultados exactos."""

    def __init__(self, raiz, biblioteca=None):
        """Construye la sesión sin reproducir ni calcular automáticamente."""
        self.raiz = raiz
        self.resultado = None
        self.datos_calculo = None
        self.vigente = False
        self.reproductor = None
        self._cargando = True
        self.historial = []
        self.instantanea = None
        self.paneles_algebra = {}
        self.botones_temas = []
        self.tema_seleccionado = 'Matrices'
        self.operacion = tk.StringVar(raiz, "sumar")
        self.escalar = tk.StringVar(raiz, "")
        self.estado = tk.StringVar(raiz, "Completa las matrices y pulsa Calcular.")
        raiz.title("Cuaderno de Álgebra Lineal — Matrices · Local")
        ancho = min(1440, raiz.winfo_screenwidth() - 80)
        alto = min(900, raiz.winfo_screenheight() - 90)
        raiz.geometry(f"{ancho}x{alto}")
        raiz.minsize(1120, 760)
        self.tema = Tema(raiz)
        self.transicion = TransicionVistas(raiz, self.tema)
        # Composición de la pantalla: navegación, entradas, acciones y dos formas de ver pasos.
        self._crear_navegacion()
        self._crear_pestanas()
        self._crear_encabezado()
        self._crear_editores()
        self._crear_acciones()
        self._crear_previa()
        self._crear_desarrollo()
        from interfaz.cuaderno import Cuaderno
        self.cuaderno = Cuaderno(self, biblioteca)
        self.reproductor = ReproductorPasos(
            raiz.after, raiz.after_cancel, self._mostrar_etapa,
            lambda: INTERVALO_PASOS_MS, self._actualizar_controles,
        )
        # Las trazas invalidan pasos antiguos en cuanto cambian las entradas.
        self.operacion.trace_add("write", self._cambiar_operacion)
        self.escalar.trace_add("write", self._cambiar_escalar)
        raiz.protocol("WM_DELETE_WINDOW", self.cerrar)
        raiz.bind("<Control-Return>", self._calcular_visible)
        self._cargando = False
        self.instantanea = self._capturar()
        self._actualizar_controles()
        self.navegacion.mostrar_inicio()

    def _crear_navegacion(self):
        """Delega el inicio y el menú plegable, sin acoplarlos a los cálculos."""
        from interfaz.inicio import Navegacion
        self.navegacion = Navegacion(self)
        self.lateral = self.navegacion.menu
        self.botones_temas = self.navegacion.botones
        self.icono_matrices = self.navegacion.icono_matrices

    def _crear_pestanas(self):
        """Crea dos vistas internas que comparten la misma sesión."""
        self.zona = ttk.Frame(self.cuerpo, padding=(16, 8, 16, 12))
        self.zona.pack(side="left", fill="both", expand=True)
        self.pestanas = ttk.Notebook(self.zona)
        self.pestanas.pack(fill="both", expand=True)
        self.contenido = ttk.Frame(self.pestanas, padding=(18, 8))
        self.pagina_pasos = ttk.Frame(self.pestanas, padding=(18, 8))
        self.pestanas.add(self.contenido, text="▦  Calculadora")
        self.pestanas.add(self.pagina_pasos, text="☷  Todos los pasos")
        self.pestanas.bind("<<NotebookTabChanged>>", self._cambiar_pestana)
        self.boton_tema = ttk.Button(self.navegacion.cabecera, text="☀  Modo claro", command=self.alternar_tema)
        self.boton_tema.pack(side="right", padx=(8, 0))
        self._pestana_anterior = self.pestanas.select()
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(1, weight=1)
        self.contenido.rowconfigure(3, weight=1)

    def _crear_encabezado(self):
        """Presenta suma y resta con las acciones de ejemplo y consulta existentes."""
        marco = ttk.Frame(self.contenido)
        marco.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ttk.Label(marco, text="Operaciones con matrices", style="Titulo.TLabel").pack(anchor="w", pady=(6, 12))
        barra = ttk.Frame(marco)
        barra.pack(fill="x")
        self.nombres_operaciones = {'Suma': 'sumar', 'Resta': 'restar', 'Escalar · kA': 'escalar',
                                   'Transpuesta · Aᵀ': 'transponer', 'Producto · AB': 'multiplicar'}
        self.selector_operacion = ttk.Combobox(barra, state='readonly', width=25,
                                                values=list(self.nombres_operaciones))
        self.selector_operacion.current(0)
        self.selector_operacion.pack(side='left')
        self.selector_operacion.bind('<<ComboboxSelected>>', self._elegir_operacion)
        ttk.Button(barra, text="Cargar ejemplo", command=self.cargar_ejemplo).pack(side="left", padx=18)
        ttk.Button(barra, text="Teoremas", command=self.ver_teoremas).pack(side="right")

    def _elegir_operacion(self, evento=None):
        """Traduce el nombre del selector al identificador que ya usa el cálculo."""
        self.operacion.set(self.nombres_operaciones[self.selector_operacion.get()])

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
        self._crear_escalar(tarjetas)
        self._crear_regla_transpuesta(tarjetas)
        tarjeta = ttk.Frame(tarjetas, style="Tarjeta.TFrame", padding=14)
        tarjeta.grid(row=0, column=2, sticky="nsew", padx=(6, 0))
        self.titulo_resultado = ttk.Label(tarjeta, text="Resultado", style="TarjetaTitulo.TLabel")
        self.titulo_resultado.pack(anchor="w")
        self.etiqueta_resultado = ttk.Label(tarjeta, text="Solo lectura · Aún no hay un cálculo", style="Coordenada.TLabel")
        self.etiqueta_resultado.pack(anchor="w", pady=(4, 8))
        botones = ttk.Frame(tarjeta, style="Interior.TFrame")
        botones.pack(side="bottom", fill="x", pady=(12, 0))
        self.guardar_resultado = ttk.Button(botones, text='Guardar resultado…', state='disabled',
                                           command=lambda: self.cuaderno.guardar_resultado_directo())
        self.guardar_resultado.pack(side='left')
        self.usar_a = ttk.Button(botones, text="Usar como A", command=lambda: self.reutilizar("A"), state="disabled")
        self.usar_b = ttk.Button(botones, text="Usar como B", command=lambda: self.reutilizar("B"), state="disabled")
        from interfaz.herramientas import menu_botones
        self.menu_resultado = menu_botones(botones, self.tema, (self.usar_a, self.usar_b))
        self.menu_resultado.pack(side='right')
        self.vista_resultado = crear_notacion(tarjeta, self.tema, 138, 16)
        self.vista_resultado.mostrar_formula(["Sin resultado"])

    def _crear_escalar(self, padre):
        """Prepara una tarjeta de k en el lugar de B para la operación unaria."""
        self.tarjeta_escalar = ttk.Frame(padre, style="Tarjeta.TFrame", padding=14)
        self.tarjeta_escalar.grid(row=0, column=1, sticky="nsew", padx=6)
        ttk.Label(self.tarjeta_escalar, text="Escalar k", style="TarjetaTitulo.TLabel").pack(anchor="w")
        ttk.Label(self.tarjeta_escalar, text="Multiplica cada elemento de A.",
                  style="Tarjeta.TLabel").pack(anchor="w", pady=(8, 14))
        ttk.Label(self.tarjeta_escalar, text="Valor de k", style="Coordenada.TLabel").pack(anchor="w")
        self.entrada_escalar = ttk.Entry(self.tarjeta_escalar, textvariable=self.escalar,
                                         width=14, font=("Segoe UI", 13), justify="center")
        self.entrada_escalar.pack(fill="x", pady=(6, 8))
        ttk.Label(self.tarjeta_escalar, text="Ejemplos: −2, 0.5, 1/3", style="Coordenada.TLabel").pack(anchor="w")
        self.vista_escalar = crear_notacion(self.tarjeta_escalar, self.tema, 70, 18)
        self.tarjeta_escalar.grid_remove()
        self._cambiar_escalar()

    def _crear_regla_transpuesta(self, padre):
        """Presenta la regla de una operación que utiliza únicamente la matriz A."""
        self.tarjeta_transpuesta = ttk.Frame(padre, style="Tarjeta.TFrame", padding=14)
        self.tarjeta_transpuesta.grid(row=0, column=1, sticky="nsew", padx=6)
        ttk.Label(self.tarjeta_transpuesta, text="Filas → Columnas", style="TarjetaTitulo.TLabel").pack(anchor="w")
        ttk.Label(self.tarjeta_transpuesta, text="Intercambiamos las posiciones.\nCada número conserva su valor.",
                  style="Tarjeta.TLabel", wraplength=220, justify="left").pack(anchor="w", pady=(12, 8))
        self.dimensiones_transpuesta = ttk.Label(self.tarjeta_transpuesta, text="", style="Coordenada.TLabel")
        self.dimensiones_transpuesta.pack(anchor="w")
        crear_notacion(self.tarjeta_transpuesta, self.tema, 80, 15).mostrar_formula(["A[i,j]", "→", "R[j,i]"])
        self.tarjeta_transpuesta.grid_remove()

    def _sincronizar_operacion(self):
        """Alterna B y k sin reconstruir los editores ni perder sus valores."""
        operacion = self.operacion.get()
        self.tarjeta_escalar.grid_remove()
        self.tarjeta_transpuesta.grid_remove()
        if operacion in ("escalar", "transponer"):
            self.editor_b.grid_remove()
            if operacion == "escalar":
                self.tarjeta_escalar.grid()
            else:
                self.tarjeta_transpuesta.grid()
                self._actualizar_dimensiones_transpuesta()
            self.usar_b.configure(state="disabled")
        else:
            self.editor_b.grid()
            self.usar_b.configure(state="normal" if self.resultado is not None else "disabled")

    def _actualizar_dimensiones_transpuesta(self):
        """Describe el tamaño aplicado de A y el tamaño que tendrá su transpuesta."""
        filas = len(self.editor_a.celdas)
        if filas:
            columnas = len(self.editor_a.celdas[0])
            self.dimensiones_transpuesta.configure(text=f"A: {filas} × {columnas}  →  Aᵀ: {columnas} × {filas}")

    def _cambiar_operacion(self, *argumentos):
        """Actualiza las entradas visibles e invalida los pasos de la operación anterior."""
        self._sincronizar_operacion()
        nombre = next(n for n, clave in self.nombres_operaciones.items() if clave == self.operacion.get())
        self.selector_operacion.set(nombre)
        self.marcar_cambio()

    def _cambiar_escalar(self, *argumentos):
        """Representa k como fracción mientras la entrada conserva su texto editable."""
        try:
            valor = convertir_numero(self.escalar.get())
        except (ValueError, ZeroDivisionError):
            valor = "…"
        self.vista_escalar.mostrar_formula(["k", "=", valor])
        self.marcar_cambio()

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
        actual = self.pestanas.select()
        nombre_actual = next((nombre for nombre, panel in self.paneles_algebra.items()
                              if actual in (str(panel), str(panel.pagina_pasos))),
                             self.tema_seleccionado if hasattr(self, 'cuaderno') and actual == str(self.cuaderno.vista) else 'Matrices')
        if hasattr(self, 'cuaderno') and actual == str(self.cuaderno.vista):
            self.cuaderno.vista.actualizar()
        self.navegacion.actualizar(nombre_actual)
        if hasattr(self, 'cuaderno') and actual == str(self.cuaderno.vista) and not self.navegacion.en_inicio:
            self.navegacion.ruta.configure(text='Biblioteca · Guardados e historial')
        if actual != self._pestana_anterior:
            self.transicion.iniciar()
        self._pestana_anterior = actual
        if self.reproductor is not None:
            self.reproductor.pausar()
        for panel in self.paneles_algebra.values():
            if str(panel) != actual:
                panel.pausar()
            if actual == str(panel.pagina_pasos):
                panel._cambiar_vista()

    def abrir_tema(self, nombre):
        """Abre un tema bajo demanda sin perder la sesión de matrices ni las demás."""
        if nombre == 'Matrices':
            return self.mostrar_matrices()
        from interfaz.inicio import TEMAS
        if nombre not in dict(TEMAS):
            raise ValueError('Tema no disponible.')
        self.navegacion.mostrar_trabajo()
        from interfaz.panel_algebra import PanelAlgebra
        if nombre not in self.paneles_algebra:
            if nombre == 'Numéricos':
                # La unidad nueva se carga al abrirla, sin exigir sus bibliotecas al álgebra exacta.
                from interfaz.panel_numerico import PanelNumerico
                self.paneles_algebra[nombre] = PanelNumerico(self.pestanas, self.tema, self.cuaderno.registrar,
                    lambda: self.cuaderno.dialogo_guardar_ejercicio(permanecer=True))
            else:
                self.paneles_algebra[nombre] = PanelAlgebra(self.pestanas, self.tema, nombre,
                                                           self.cuaderno.registrar, self.cuaderno.guardar_resultado_directo)
        self.tema_seleccionado = nombre
        self._ocultar_vistas()
        panel = self.paneles_algebra[nombre]
        self.pestanas.insert(0, panel, text='▦  Calculadora')
        self.pestanas.insert(1, panel.pagina_pasos, text='☷  Todos los pasos')
        self.pestanas.select(panel)
        return panel

    def _ocultar_vistas(self):
        """Mantiene dos pestañas visibles; conserva las sesiones de otros temas ocultas."""
        for pagina in self.pestanas.tabs():
            self.pestanas.hide(pagina)

    def mostrar_matrices(self):
        """Recupera las dos vistas originales de Matrices y sus datos intactos."""
        self.navegacion.mostrar_trabajo()
        self._ocultar_vistas()
        self.tema_seleccionado = 'Matrices'
        self.pestanas.insert(0, self.contenido, text='▦  Calculadora')
        self.pestanas.insert(1, self.pagina_pasos, text='☷  Todos los pasos')
        self.pestanas.select(self.contenido)

    def mostrar_biblioteca(self):
        """Abre guardados e historial desde el inicio o cualquier tema."""
        self.navegacion.mostrar_trabajo()
        self._ocultar_vistas()
        self.pestanas.add(self.cuaderno.vista, text='Biblioteca · Guardados e historial')
        self.pestanas.select(self.cuaderno.vista)
        self.cuaderno.vista.actualizar()
        self.navegacion.ruta.configure(text='Biblioteca · Guardados e historial')

    def _calcular_visible(self, evento=None):
        """Dirige el atajo al tema visible sin calcular sobre otro formulario."""
        if self.navegacion.en_inicio or (hasattr(self, 'cuaderno') and self.pestanas.select() == str(self.cuaderno.vista)):
            return 'break'
        for panel in self.paneles_algebra.values():
            if self.pestanas.select() in (str(panel), str(panel.pagina_pasos)):
                panel.calcular()
                return 'break'
        return self.calcular(evento)

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
        self.guardar_resultado.configure(state='normal' if self.vigente and self.resultado is not None else 'disabled')
        disponibles = reproductor is not None and bool(reproductor.pasos)
        for boton in (self.boton_anterior, self.boton_reproducir, self.boton_siguiente,
                      self.boton_reiniciar, self.boton_todo):
            boton.configure(state="normal" if disponibles else "disabled")
        self.boton_reproducir.configure(text="Ⅱ Pausar" if disponibles and reproductor.activo else "▶ Reproducir")
        if disponibles:
            self.boton_anterior.configure(state="normal" if reproductor.indice > 0 else "disabled")
            total = len(reproductor.secuencia)
            self.boton_siguiente.configure(state="normal" if reproductor.indice < total - 1 else "disabled")
            posicion = reproductor.secuencia[reproductor.indice].posicion + 1 if reproductor.indice >= 0 else 0
            self.progreso.configure(text=f"Paso {posicion} de {len(reproductor.pasos)} · Etapa {max(0, reproductor.indice + 1)} de {total} · 2 segundos por etapa")
        else:
            self.progreso.configure(text="Ctrl + Enter para calcular · El recorrido comienza cuando lo solicitas")
        self.boton_deshacer.configure(state="normal" if self.historial else "disabled")

    def _pasos_calculo(self):
        """Devuelve posiciones y valores del último resultado, sin recalcularlo."""
        if self.datos_calculo is None:
            return []
        a, b, signo = self.datos_calculo
        if signo == "AB":
            return [(i, j, tuple(a[i]), tuple(fila_b[j] for fila_b in b), valor, signo)
                    for i, fila in enumerate(self.resultado) for j, valor in enumerate(fila)]
        if signo == "T":
            return [(i, j, a[j][i], None, valor, signo)
                    for i, fila in enumerate(self.resultado) for j, valor in enumerate(fila)]
        if signo == "×":
            return [(i, j, b, a[i][j], valor, signo)
                    for i, fila in enumerate(self.resultado) for j, valor in enumerate(fila)]
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
            filas, columnas = len(self.resultado), len(self.resultado[0])
            condicion = self._describir_calculo(filas, columnas)
            self.desarrollo.mostrar(pasos, self.resultado, condicion)
            self._mostrar_formula(pasos[min(1, len(pasos) - 1)])
            signo = self.datos_calculo[2]
            nombre = "AB" if signo == "AB" else "Aᵀ" if signo == "T" else "kA" if signo == "×" else f"A {signo} B"
            self.etiqueta_resultado.configure(text=f"{nombre} · {filas} × {columnas} · Solo lectura" if self.vigente else "Último cálculo · datos modificados")
            if not self.vigente:
                self.desarrollo.aviso.configure(text="Último cálculo · Las entradas cambiaron. Vuelve a calcular para actualizar.")
        pasos = self._pasos_calculo() if self.vigente else ()
        self.reproductor.preparar(pasos, construir_etapas(pasos))
        for boton in (self.usar_a, self.usar_b):
            permite_b = boton is not self.usar_b or self.operacion.get() not in ('escalar', 'transponer')
            boton.configure(state='normal' if self.resultado is not None and permite_b else 'disabled')

    def _describir_calculo(self, filas, columnas):
        """Elige los textos de cada operación a partir del cálculo guardado."""
        a, operando, signo = self.datos_calculo
        if signo == "AB":
            comunes = len(a[0])
            self.resumen.configure(text=f"① {comunes} columnas de A = {len(operando)} filas de B.\n\n② Multiplicamos cada fila por cada columna.\n\n③ Sumamos los productos; AB tiene tamaño {filas} × {columnas}.")
            self.subtitulo_pasos.configure(text="Producto de matrices · AB")
            return f"A: {filas} × {comunes} · B: {len(operando)} × {columnas} → AB: {filas} × {columnas}."
        if signo == "T":
            self.resumen.configure(text=f"① A tiene tamaño {len(a)} × {len(a[0])}.\n\n② Las filas pasan a columnas.\n\n③ Aᵀ tiene tamaño {filas} × {columnas}; los valores se conservan.")
            self.subtitulo_pasos.configure(text="Transpuesta de una matriz · Aᵀ")
            return f"A: {len(a)} × {len(a[0])} → Aᵀ: {filas} × {columnas}. Intercambiamos filas y columnas."
        if signo == "×":
            self.resumen.configure(text=f"① Usamos el escalar k = {operando}.\n\n② Multiplicamos cada elemento de A por k.\n\n③ Conservamos el tamaño {filas} × {columnas} y las fracciones exactas.")
            self.subtitulo_pasos.configure(text="Multiplicación por escalar · kA")
            return f"k = {operando} · A y kA tienen dimensiones {filas} × {columnas}."
        self.resumen.configure(text=f"① A y B tienen dimensiones {filas} × {columnas}.\n\n② Operamos los elementos de la misma posición.\n\n③ Conservamos las fracciones exactas.")
        self.subtitulo_pasos.configure(text=f"{'Suma' if signo == '+' else 'Resta'} de matrices · A {signo} B")
        return f"A y B tienen las mismas dimensiones: {filas} × {columnas}."

    def _mostrar_formula(self, paso):
        """Muestra solo una igualdad importante en la vista previa."""
        fila, columna, a, b, resultado, signo = paso
        if signo == "AB":
            tokens = [f"Fila {fila + 1} de A", "·", f"Columna {columna + 1} de B", "=", resultado]
        elif signo == "T":
            tokens = [f"A[{columna + 1},{fila + 1}]", "=", a, "→", f"R[{fila + 1},{columna + 1}]", "=", resultado]
        else:
            tokens = [a, signo] + (["(", b, ")"] if b < 0 else [b]) + ["=", resultado]
        self.formula_previa.mostrar_formula(tokens)
        self.coordenada_previa.configure(text=f"Fila {fila + 1} · Columna {columna + 1}")

    def _mostrar_etapa(self, etapa, indice, total):
        """Relaciona origen, cuenta y destino; revela la celda solo al guardarla."""
        paso = etapa.paso
        fila, columna = paso[:2]
        if paso[-1] == "AB":
            self.editor_a.resaltar_fila(fila, etapa.par)
            self.editor_b.resaltar_columna(columna, etapa.par)
        else:
            origen_fila, origen_columna = (columna, fila) if paso[-1] == "T" else (fila, columna)
            self.editor_a.resaltar(origen_fila, origen_columna)
            if paso[-1] in ("+", "-"):
                self.editor_b.resaltar(fila, columna)
            elif paso[-1] == "×":
                self.entrada_escalar.configure(style="Activa.TEntry")
        columnas = len(self.resultado[0])
        limite = etapa.posicion if etapa.fase == "guardar" else etapa.posicion - 1
        parcial = [[valor if i * columnas + j <= limite else "·" for j, valor in enumerate(valores)]
                   for i, valores in enumerate(self.resultado)]
        self.vista_resultado.mostrar_matriz(parcial, (fila, columna))
        self.titulo_resultado.configure(text=f"Resultado · R[{fila + 1},{columna + 1}]")
        self.formula_previa.mostrar_formula(etapa.tokens)
        self.coordenada_previa.configure(text=f"Fila {fila + 1} · Columna {columna + 1} · {etapa.fase.capitalize()}")
        origenes = etapa.operandos.replace("\n", " · ")
        self.resumen.configure(text=f"{origenes}\n{etapa.mensaje}")

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
        self._quitar_orientacion()
        self.pestanas.select(self.pagina_pasos)

    def _quitar_orientacion(self):
        """Retira indicadores de origen y destino al salir del recorrido."""
        self.titulo_resultado.configure(text="Resultado")
        self.entrada_escalar.configure(style="TEntry")
        self.vista_escalar.resaltada = False
        self.vista_escalar.actualizar_tema()

    def _invalidar_recorrido(self):
        """Cancela temporizadores y marca como anterior el cálculo visible."""
        self.vigente = False
        self.transicion.cancelar()
        if self.reproductor is not None:
            self.reproductor.preparar(())
            self.editor_a.quitar_resaltado()
            self.editor_b.quitar_resaltado()
            self._quitar_orientacion()
            if self.resultado is not None:
                self.vista_resultado.mostrar_matriz(self.resultado)
                self.resumen.configure(text="Último cálculo · entradas modificadas.\n\nVuelve a calcular para recorrer las etapas actualizadas.")
                self.etiqueta_resultado.configure(text="Último cálculo · datos modificados")
                self.desarrollo.aviso.configure(text="Último cálculo · Las entradas cambiaron. Vuelve a calcular para actualizar.")

    def _capturar(self):
        """Copia entradas, dimensiones pendientes y último cálculo para deshacer."""
        entradas = []
        for editor in (self.editor_a, self.editor_b):
            entradas.append(([[celda.get() for celda in fila] for fila in editor.celdas],
                             editor.filas.get(), editor.columnas.get()))
        return deepcopy(dict(entradas=entradas, operacion=self.operacion.get(), escalar=self.escalar.get(), resultado=self.resultado,
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
            self._actualizar_dimensiones_transpuesta()
            self.instantanea = self._capturar()
            self._actualizar_controles()

    def marcar_cambio(self, *argumentos):
        """Invalida pasos viejos y registra modificaciones sin leer widgets destruidos."""
        if self._cargando or any(getattr(self, nombre, None) is not None and
                                getattr(self, nombre).cargando for nombre in ("editor_a", "editor_b")):
            return
        self._actualizar_dimensiones_transpuesta()
        nueva = self._capturar()
        if self.instantanea and all(nueva[clave] == self.instantanea[clave]
                                   for clave in ("entradas", "operacion", "escalar")):
            return
        self._recordar()
        self._invalidar_recorrido()
        self.estado.set("Datos modificados. Pulsa Calcular para actualizar.")
        self.etiqueta_estado.configure(style="Estado.TLabel")
        self.instantanea = self._capturar()
        self._actualizar_controles()

    def deshacer(self):
        """Restaura entradas y cálculo sin cambiar la operación seleccionada."""
        if not self.historial:
            return
        anterior = self.historial.pop()
        self._cargando = True
        self._invalidar_recorrido()
        for editor, (matriz, filas, columnas) in zip((self.editor_a, self.editor_b), anterior["entradas"]):
            editor.cargar(matriz)
            editor.filas.set(filas)
            editor.columnas.set(columnas)
        self.escalar.set(anterior["escalar"])
        self.resultado, self.datos_calculo = anterior["resultado"], anterior["datos"]
        misma_operacion = self.operacion.get() == anterior["operacion"]
        self.vigente = anterior["vigente"] and misma_operacion
        self.estado.set(anterior["estado"] if misma_operacion else
                        "Datos restaurados. Pulsa Calcular para la operación seleccionada.")
        self.etiqueta_estado.configure(style="Estado.TLabel")
        self._sincronizar_operacion()
        self._actualizar_dimensiones_transpuesta()
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

    def calcular(self, evento=None, registrar=True):
        """Lee los editores y llama al mismo núcleo que usa la consola."""
        self._invalidar_recorrido()
        try:
            a = self.editor_a.leer()
            if self.operacion.get() == "transponer":
                b = None
                resultado = transponer_matriz(a)
                signo = "T"
            elif self.operacion.get() == "escalar":
                b = self._leer_escalar()
                resultado = multiplicar_por_escalar(a, b)
                signo = "×"
            else:
                b = self.editor_b.leer()
                if self.operacion.get() == "multiplicar":
                    resultado = producto_matricial(a, b)
                    signo = "AB"
                else:
                    sumar = self.operacion.get() == "sumar"
                    resultado = sumar_matrices(a, b) if sumar else restar_matrices(a, b)
                    signo = "+" if sumar else "-"
        except ValueError as error:
            self.mostrar_error(str(error))
            return "break"
        self._recordar()
        self.resultado = resultado
        self.datos_calculo = (a, b, signo)
        self.vigente = True
        self._presentar_calculo()
        self.etiqueta_estado.configure(style="Estado.TLabel")
        self.estado.set("Cálculo completado · Filas y columnas intercambiadas" if signo == "T" else
                        "Cálculo completado · Se conserva el tamaño de A" if signo == "×"
                        else "Cálculo completado · Dimensiones compatibles")
        self.instantanea = self._capturar()
        self._actualizar_controles()
        if registrar:
            self.cuaderno.registrar(self)
        return "break"

    def _leer_escalar(self):
        """Convierte k exactamente y enfoca su entrada ante un error recuperable."""
        try:
            return convertir_numero(self.escalar.get())
        except (ValueError, ZeroDivisionError):
            self.entrada_escalar.focus_set()
            self.entrada_escalar.selection_range(0, "end")
            raise ValueError("Revisa el escalar k: usa un número como −2, 0.5 o 1/3.") from None

    def reutilizar(self, destino):
        """Copia el último resultado al editor elegido como una acción deshacible."""
        if self.resultado is not None:
            with self._edicion():
                (self.editor_a if destino == "A" else self.editor_b).cargar(self.resultado)
                self.estado.set("Resultado copiado. Pulsa Calcular para actualizar.")

    def cargar_ejemplo(self):
        """Carga un ejemplo de la operación seleccionada sin calcular todavía."""
        with self._edicion():
            self.editor_a.cargar([["1/3", "1/10"], ["-2", "4"]])
            if self.operacion.get() == "multiplicar":
                self.editor_a.cargar([[1, 2, 3], [4, 5, 6]])
                self.editor_b.cargar([[1, 0], [2, 1], [0, 3]])
            elif self.operacion.get() == "transponer":
                self.editor_a.cargar([["1/3", "-2", "5"], ["0", "4", "1/2"]])
                self._sincronizar_operacion()
            elif self.operacion.get() == "escalar":
                self.escalar.set("-3/2")
                self._sincronizar_operacion()
            else:
                self.editor_b.cargar([["1/6", "1/5"], ["5", "-1"]])
                self.operacion.set("sumar")
            self.estado.set("Ejemplo cargado. Pulsa Calcular.")

    def limpiar(self):
        """Reinicia la sesión visible y permite deshacer esta acción."""
        with self._edicion():
            self.resultado = None
            self.datos_calculo = None
            self.editor_a.vaciar()
            self.editor_b.vaciar()
            self.escalar.set("")
            self._presentar_calculo()
            self.estado.set("Completa las matrices y pulsa Calcular.")
            self.etiqueta_estado.configure(style="Estado.TLabel")

    def cerrar(self):
        """Cancela eventos pendientes antes de destruir la ventana."""
        self.reproductor.pausar()
        for panel in self.paneles_algebra.values():
            panel.pausar()
        self.transicion.cancelar()
        self.raiz.destroy()


def iniciar_ventana():
    """Abre la ventana local hasta que la persona cierre su sesión."""
    raiz = tk.Tk()
    CalculadoraVentana(raiz)
    raiz.mainloop()
