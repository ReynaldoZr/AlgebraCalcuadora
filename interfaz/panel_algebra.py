"""Compone entradas y procedimientos de los temas de álgebra pendientes.

Tema: escritorio local con navegación y pasos, sin bibliotecas numéricas.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from contextlib import contextmanager
from copy import deepcopy
import tkinter as tk
from tkinter import ttk

from interfaz.cuadricula import EditorMatriz
from interfaz.datos import convertir_numero
from interfaz.desarrollo import crear_notacion
from interfaz.operaciones import OPERACIONES, calcular_operacion, ejemplo_operacion
from interfaz.procedimiento import VistaProcedimiento
from interfaz.recorrido import INTERVALO_PASOS_MS, ReproductorPasos
from interfaz.lenguaje_pasos import explicar_paso
from teoremas.resumen_teoremas import teoremas_tema


class PanelAlgebra(ttk.Frame):
    """Conserva una sesión independiente por tema y construye solo lo necesario."""

    def __init__(self, padre, tema_visual, nombre, al_calcular=None, al_guardar_resultado=None):
        """Construye el formulario y el recorrido sin calcular ni cargar ejemplos."""
        super().__init__(padre, padding=(18, 8))
        self.vistas = padre
        self.tema = tema_visual
        self.nombre = nombre
        self.al_calcular = al_calcular
        self.al_guardar_resultado = al_guardar_resultado
        self.claves = [clave for clave, op in OPERACIONES.items() if op.tema == nombre]
        self.clave = self.claves[0]
        self.editores = {}
        self.presentacion = None
        self.vigente = False
        self.historial = []
        self.instantanea = None
        self._cargando = True
        self._desarrollo_pendiente = True
        self.pasos_fallo = ()
        self.reproductor = None
        self.escalar = tk.StringVar(self, '')
        self.metodo = tk.StringVar(self, self.clave)
        self.secundaria = tk.StringVar(self, 'B')
        self.estado = tk.StringVar(self, 'Completa las entradas y pulsa Calcular.')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)
        self._crear_cabecera()
        self._crear_entradas()
        self._crear_resultados()
        self.reproductor = ReproductorPasos(self.after, self.after_cancel, self._mostrar_paso,
                                          lambda: INTERVALO_PASOS_MS, self._actualizar_controles)
        self._configurar_entradas()
        self.escalar.trace_add('write', self.marcar_cambio)
        self.metodo.trace_add('write', self._cambiar_metodo)
        self._cargando = False
        self.instantanea = self._capturar()
        self._actualizar_controles()

    def _crear_cabecera(self):
        """Añade método, ayuda y acciones sin alterar la navegación de matrices."""
        cabecera = ttk.Frame(self)
        cabecera.grid(row=0, column=0, sticky='ew', pady=(0, 12))
        ttk.Label(cabecera, text=self.nombre, style='Titulo.TLabel').pack(anchor='w', pady=(6, 12))
        barra = ttk.Frame(cabecera)
        barra.pack(fill='x')
        self.selector = ttk.Combobox(barra, state='readonly', width=42,
                                    values=[OPERACIONES[c].nombre for c in self.claves])
        self.selector.current(0)
        self.selector.pack(side='left')
        self.selector.bind('<<ComboboxSelected>>', self._elegir_selector)
        ttk.Button(barra, text='Cargar ejemplo', command=self.cargar_ejemplo).pack(side='left', padx=18)
        ttk.Button(barra, text='Teoremas', command=self.ver_teoremas).pack(side='right')
        self.ayuda = ttk.Label(cabecera, style='Subtitulo.TLabel', wraplength=840, justify='left')
        self.ayuda.pack(anchor='w', pady=(6, 0))

    def _crear_entradas(self):
        """Reserva las casillas para las entradas reales de cada método."""
        self.tarjetas = ttk.Frame(self)
        self.tarjetas.grid(row=1, column=0, sticky='nsew')
        self.tarjetas.rowconfigure(0, weight=1)
        for columna in range(3):
            self.tarjetas.columnconfigure(columna, weight=1, uniform='matrices')
        self.regla = ttk.Frame(self.tarjetas, style='Tarjeta.TFrame', padding=14)
        ttk.Label(self.regla, text='Regla del método', style='TarjetaTitulo.TLabel').pack(anchor='w')
        self.texto_regla = ttk.Label(self.regla, style='Tarjeta.TLabel', wraplength=260, justify='left')
        self.texto_regla.pack(fill='x', pady=16)
        self.escalar_central = ttk.Entry(self.regla, textvariable=self.escalar, width=16)
        acciones = ttk.Frame(self)
        acciones.grid(row=2, column=0, sticky='ew', pady=12)
        self.marco_escalar = ttk.Frame(acciones)
        ttk.Label(self.marco_escalar, text='Escalar k:').pack(side='left')
        ttk.Entry(self.marco_escalar, textvariable=self.escalar, width=16).pack(side='left', padx=8)
        ttk.Button(acciones, text='Calcular', command=self.calcular, style='Principal.TButton').pack(side='left')
        ttk.Button(acciones, text='Limpiar', command=self.limpiar).pack(side='left', padx=4)
        self.boton_deshacer = ttk.Button(acciones, text='Deshacer', command=self.deshacer)
        self.boton_deshacer.pack(side='left')
        self.alternar_secundaria = ttk.Frame(acciones)
        for nombre in ('B', 'C'):
            ttk.Radiobutton(self.alternar_secundaria, text='Editar ' + nombre, variable=self.secundaria,
                            value=nombre, command=self._mostrar_secundaria).pack(side='left')
        ttk.Label(self, textvariable=self.estado, style='Estado.TLabel', wraplength=880).grid(row=4, column=0, sticky='ew', pady=(6, 0))

    def _crear_resultados(self):
        """Separa vista breve y procedimiento completo, con controles de dos segundos."""
        resultado = ttk.Frame(self.tarjetas, style='Tarjeta.TFrame', padding=14)
        resultado.grid(row=0, column=2, sticky='nsew', padx=(6, 0))
        ttk.Label(resultado, text='Resultado', style='TarjetaTitulo.TLabel').pack(anchor='w')
        self.reutilizar_boton = ttk.Button(resultado, text='Usar resultado como A', command=self.reutilizar)
        from interfaz.herramientas import menu_botones
        self.menu_resultado = menu_botones(resultado, self.tema, (self.reutilizar_boton,))
        self.menu_resultado.pack(side='bottom', anchor='e', pady=(6, 0))
        self.guardar_resultado = ttk.Button(resultado, text='Guardar resultado…', command=self.al_guardar_resultado)
        self.guardar_resultado.pack(side='bottom', fill='x', pady=(8, 0))
        self.vista_matriz = crear_notacion(resultado, self.tema, 180, 17)
        breve = ttk.Frame(self, style='Tarjeta.TFrame', padding=14)
        breve.grid(row=3, column=0, sticky='nsew')
        breve.columnconfigure(0, weight=1)
        breve.columnconfigure(1, weight=2)
        breve.rowconfigure(2, weight=1)
        ttk.Label(breve, text='Vista previa del procedimiento', style='TarjetaTitulo.TLabel').grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 12))
        self.resumen = ttk.Label(breve, text='Aquí aparecerá el resultado.', style='Tarjeta.TLabel', wraplength=380, justify='left')
        self.resumen.grid(row=1, column=0, rowspan=2, sticky='nw', padx=(0, 20))
        self.titulo_paso = ttk.Label(breve, text='Calcula para iniciar el recorrido.', style='Coordenada.TLabel', wraplength=520)
        self.titulo_paso.grid(row=1, column=1, sticky='ew')
        formula = ttk.Frame(breve, style='Interior.TFrame')
        formula.grid(row=2, column=1, sticky='nsew')
        self.formula = crear_notacion(formula, self.tema, 62, 16)
        controles = ttk.Frame(breve, style='Interior.TFrame')
        controles.grid(row=3, column=0, columnspan=2, sticky='ew', pady=8)
        self.anterior = ttk.Button(controles, text='‹ Anterior', command=lambda: self.reproductor.anterior())
        self.anterior.pack(side='left')
        self.reproducir = ttk.Button(controles, text='Reproducir', command=self.alternar_recorrido)
        self.reproducir.pack(side='left', padx=4)
        self.siguiente = ttk.Button(controles, text='Siguiente ›', command=lambda: self.reproductor.siguiente())
        self.siguiente.pack(side='left')
        self.reiniciar = ttk.Button(controles, text='↺ Reiniciar', command=lambda: self.reproductor.reiniciar())
        self.reiniciar.pack(side='left', padx=4)
        ttk.Button(controles, text='Abrir todos los pasos ↗', command=lambda: self.vistas.select(self.pagina_pasos)).pack(side='right')
        self.progreso = ttk.Label(breve, text='2 segundos por etapa', style='Coordenada.TLabel')
        self.progreso.grid(row=4, column=0, columnspan=2, sticky='w')
        self.pagina_pasos = ttk.Frame(self.vistas, padding=(18, 8))
        ttk.Label(self.pagina_pasos, text='Todos los pasos', style='Titulo.TLabel').pack(anchor='w')
        ttk.Label(self.pagina_pasos, text=self.nombre, style='Subtitulo.TLabel').pack(anchor='w', pady=(0, 12))
        ttk.Button(self.pagina_pasos, text='‹  Volver a calculadora', command=lambda: self.vistas.select(self)).pack(side='bottom', anchor='w', pady=(12, 0))
        self.completa = VistaProcedimiento(self.pagina_pasos, self.tema)
        self.completa.pack(fill='both', expand=True)
        breve.bind('<Configure>', lambda evento: self._ajustar_texto(evento.width))

    def _ajustar_texto(self, ancho):
        """Ajusta las etiquetas al espacio visible sin ampliar la letra."""
        self.resumen.configure(wraplength=max(160, ancho // 3 - 28))
        self.titulo_paso.configure(wraplength=max(240, ancho * 2 // 3 - 28))

    def _configurar_entradas(self):
        """Conserva los datos ocultos y muestra solo las matrices necesarias."""
        operacion = OPERACIONES[self.clave]
        for editor in self.editores.values():
            editor.grid_remove()
        for nombre in operacion.entradas:
            if nombre not in self.editores:
                editor = EditorMatriz(self.tarjetas, nombre, self.marcar_cambio, self.mostrar_error, self.tema)
                self.editores[nombre] = editor
                if nombre == 'b':
                    editor.cargar([[''], ['']])
        self.editores['A'].grid(row=0, column=0, sticky='nsew', padx=(0, 6))
        self.regla.grid(row=0, column=1, sticky='nsew', padx=6)
        self.texto_regla.configure(text=operacion.ayuda)
        self.escalar_central.pack_forget()
        if operacion.escalar and len(operacion.entradas) == 1:
            self.escalar_central.pack(pady=12)
        self.alternar_secundaria.pack_forget()
        if 'C' in operacion.entradas:
            self.alternar_secundaria.pack(side='left', padx=10)
        self._mostrar_secundaria()
        self.marco_escalar.pack_forget()
        if operacion.escalar and len(operacion.entradas) > 1:
            self.marco_escalar.pack(side='left', padx=10)
        self.ayuda.configure(text=operacion.ayuda)

    def _mostrar_secundaria(self):
        """Muestra b o B en la tarjeta central; C comparte ese lugar solo cuando hace falta."""
        nombres = OPERACIONES[self.clave].entradas[1:]
        for nombre, editor in self.editores.items():
            if nombre != 'A':
                editor.grid_remove()
        if nombres:
            nombre = self.secundaria.get() if self.secundaria.get() in nombres else nombres[0]
            self.regla.grid_remove()
            self.editores[nombre].grid(row=0, column=1, sticky='nsew', padx=6)

    def _elegir_selector(self, evento=None):
        """Traduce el selector de propiedades a la misma selección usada por los botones."""
        self.metodo.set(self.claves[self.selector.current()])

    def seleccionar(self, clave):
        """Selecciona un método disponible y conserva las entradas del tema."""
        self.metodo.set(clave)

    def _cambiar_metodo(self, *argumentos):
        """Cambia el formulario y marca el resultado anterior como desactualizado."""
        self._recordar()
        self._cargando = True
        self.clave = self.metodo.get()
        self.selector.current(self.claves.index(self.clave))
        self._configurar_entradas()
        self._cargando = False
        self._invalidar()
        self.instantanea = self._capturar()

    def _capturar(self):
        """Copia entradas, dimensiones y cálculo para un historial local de cincuenta estados."""
        entradas = {nombre: ([[c.get() for c in fila] for fila in e.celdas], e.filas.get(), e.columnas.get())
                    for nombre, e in self.editores.items()}
        return deepcopy(dict(entradas=entradas, clave=self.clave, escalar=self.escalar.get(),
                             presentacion=self.presentacion, vigente=self.vigente))

    def _recordar(self):
        """Guarda el estado previo sin duplicar la lectura de widgets en reconstrucción."""
        if self.instantanea is not None:
            self.historial.append(self.instantanea)
            self.historial = self.historial[-50:]

    def _invalidar(self):
        """Cancela pasos anteriores y conserva el último cálculo identificado como anterior."""
        self.vigente = False
        self.pasos_fallo = ()
        self._desarrollo_pendiente = True
        if self.reproductor is not None:
            self.reproductor.preparar(())
        self.estado.set('Datos modificados. Pulsa Calcular para actualizar.')
        self.titulo_paso.configure(text='Último cálculo · datos modificados' if self.presentacion else 'Calcula para iniciar el recorrido.')
        self.completa.aviso.configure(text='Último cálculo · datos modificados; vuelve a calcular.')
        self._actualizar_controles()

    def marcar_cambio(self, *argumentos):
        """Registra una edición manual sin acceder a celdas en reconstrucción."""
        if self._cargando or any(e.cargando for e in self.editores.values()):
            return
        self._recordar()
        self._invalidar()
        self.instantanea = self._capturar()

    @contextmanager
    def _edicion(self):
        """Agrupa ejemplo, limpieza o reutilización como una sola acción deshacible."""
        self._recordar()
        self._cargando = True
        try:
            yield
        finally:
            self._cargando = False
            self._invalidar()
            self.instantanea = self._capturar()
            self._cargar_desarrollo_si_visible()

    def cargar_ejemplo(self):
        """Carga entradas conocidas del método seleccionado sin cambiarlo."""
        datos, escalar = ejemplo_operacion(self.clave)
        with self._edicion():
            for nombre in OPERACIONES[self.clave].entradas:
                self.editores[nombre].cargar(datos[nombre])
            self.escalar.set(escalar)

    def limpiar(self):
        """Vacía los datos del método conservando su selección y tamaños aplicados."""
        with self._edicion():
            for nombre in OPERACIONES[self.clave].entradas:
                editor = self.editores[nombre]
                editor.vaciar()
            self.escalar.set('')
            self.presentacion = None
            self.vista_matriz.mostrar_formula([])
            self.formula.mostrar_formula([])
            self.resumen.configure(text='Aquí aparecerá el resultado.')

    def deshacer(self):
        """Restaura datos sin cambiar el método; un cálculo ajeno queda como anterior."""
        if not self.historial:
            return
        anterior = self.historial.pop()
        self._cargando = True
        self._invalidar()
        for nombre, (matriz, filas, columnas) in anterior['entradas'].items():
            editor = self.editores[nombre]
            editor.cargar(matriz)
            editor.filas.set(filas)
            editor.columnas.set(columnas)
        self.escalar.set(anterior['escalar'])
        self.presentacion = anterior['presentacion']
        self.vigente = anterior['vigente'] and anterior['clave'] == self.clave
        self._cargando = False
        self._presentar()
        self.instantanea = self._capturar()

    def calcular(self, registrar=True):
        """Lee entradas exactas y llama al catálogo; los errores no borran el último resultado."""
        self._invalidar()
        try:
            operacion = OPERACIONES[self.clave]
            entradas = {nombre: self.editores[nombre].leer() for nombre in operacion.entradas}
            escalar = convertir_numero(self.escalar.get()) if operacion.escalar else 2
            presentacion = calcular_operacion(self.clave, entradas, escalar)
        except (ValueError, ZeroDivisionError) as error:
            self.pasos_fallo = getattr(error, 'pasos', ())
            self.mostrar_error(str(error))
            self._cargar_desarrollo_si_visible()
            return
        self._recordar()
        self.presentacion = presentacion
        self.vigente = True
        self._presentar()
        self.instantanea = self._capturar()
        if registrar and self.al_calcular is not None:
            self.al_calcular(self)

    def _presentar(self):
        """Actualiza el resultado y prepara el recorrido; el desarrollo se dibuja al abrirlo."""
        self._desarrollo_pendiente = True
        self.formula.mostrar_formula([])
        if self.presentacion is None:
            self.resumen.configure(text='Aquí aparecerá el resultado.')
            self.vista_matriz.mostrar_formula([])
        else:
            lineas = self.presentacion.resumen.splitlines()
            texto = '\n'.join(lineas[:6])
            if len(lineas) > 6:
                texto += '\nConsulta el resultado completo en Todos los pasos.'
            self.resumen.configure(text=texto)
            if self.presentacion.matriz is not None:
                self.vista_matriz.mostrar_matriz(self.presentacion.matriz)
            else:
                self.vista_matriz.mostrar_formula([])
        pasos = self.presentacion.calculo.pasos if self.presentacion and self.vigente else ()
        self.reproductor.preparar(pasos)
        self.estado.set('Cálculo completado.' if self.vigente else 'Datos restaurados. Pulsa Calcular para actualizar.')
        self.titulo_paso.configure(text='Resultado · Avanza para ver lo esencial.' if self.vigente else 'Último cálculo · datos modificados')
        self._cargar_desarrollo_si_visible()
        self._actualizar_controles()

    def mostrar_error(self, mensaje):
        """Expone un error recuperable y conserva entradas y cálculo válido anterior."""
        self.estado.set(mensaje)

    def reutilizar(self):
        """Copia la matriz de resultado a A sin reescribir valores intermedios."""
        if self.presentacion is not None and self.presentacion.matriz is not None:
            with self._edicion():
                self.editores['A'].cargar(self.presentacion.matriz)

    def _mostrar_paso(self, paso, indice, total):
        """Expone una fórmula esencial y la matriz vigente de esa etapa, también al retroceder."""
        detalle = explicar_paso(paso)
        self.titulo_paso.configure(text=f'{indice + 1}/{total} · {paso.titulo}\n{detalle}')
        self.formula.mostrar_formula(paso.formulas[0] if paso.formulas else [])
        matriz = next((p for p in reversed(self.reproductor.secuencia[:indice + 1]) if p.matriz is not None), None)
        if matriz is not None:
            self.vista_matriz.mostrar_matriz(matriz.matriz, separador=matriz.separador)
        elif self.presentacion.matriz is not None:
            self.vista_matriz.mostrar_matriz(self.presentacion.matriz)

    def alternar_recorrido(self):
        """Reproduce o pausa a dos segundos por etapa sin selector de velocidad."""
        if self.reproductor.activo:
            self.reproductor.pausar()
        else:
            self.reproductor.reproducir()

    def _actualizar_controles(self):
        """Sincroniza botones de reproducción, historial y reutilización."""
        if self.reproductor is None:
            return
        habilitado = self.vigente and bool(self.reproductor.pasos)
        for boton in (self.anterior, self.reproducir, self.siguiente, self.reiniciar):
            boton.configure(state='normal' if habilitado else 'disabled')
        self.reproducir.configure(text='Ⅱ Pausar' if self.reproductor.activo else '▶ Reproducir')
        self.progreso.configure(text=f'Paso {max(0, self.reproductor.indice + 1)} de {len(self.reproductor.secuencia)} · 2 segundos por etapa')
        self.boton_deshacer.configure(state='normal' if self.historial else 'disabled')
        self.reutilizar_boton.configure(state='normal' if self.presentacion and self.presentacion.matriz is not None else 'disabled')
        self.guardar_resultado.configure(state='normal' if self.vigente and self.presentacion
                                        and self.presentacion.matriz is not None and self.al_guardar_resultado is not None else 'disabled')

    def _cambiar_vista(self, evento=None):
        """Pausa al navegar y construye el desarrollo completo solo cuando se necesita."""
        if self.reproductor is not None:
            self.reproductor.pausar()
        self._cargar_desarrollo_si_visible()

    def _cargar_desarrollo_si_visible(self):
        """Muestra todos los pasos o el diagnóstico detenido sin truncar el contenido."""
        if self.vistas.select() != str(self.pagina_pasos) or not self._desarrollo_pendiente:
            return
        pasos = self.pasos_fallo or (self.presentacion.calculo.pasos if self.presentacion else ())
        aviso = 'Procedimiento detenido · ' + self.estado.get() if self.pasos_fallo else (
            'Desarrollo completo' if self.vigente else 'Último cálculo · datos modificados')
        self.completa.mostrar_procedimiento(pasos, aviso)
        self._desarrollo_pendiente = False

    def ver_teoremas(self):
        """Abre una consulta breve del tema en una ventana del mismo diseño."""
        ventana = tk.Toplevel(self)
        ventana.title('Teoremas · ' + self.nombre)
        ttk.Label(ventana, text=teoremas_tema(self.nombre), padding=22, wraplength=640, justify='left').pack(fill='both', expand=True)

    def pausar(self):
        """Cancela el evento pendiente al cambiar de tema o cerrar la aplicación."""
        self.reproductor.pausar()
