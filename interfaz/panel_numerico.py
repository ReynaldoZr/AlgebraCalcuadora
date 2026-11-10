"""Integra la semana 12 conservando tres tarjetas y las vistas generales.

Tema: formularios aproximados, tabla completa, pasos, historial y gráficas.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from contextlib import contextmanager
from copy import deepcopy
import tkinter as tk
from tkinter import ttk

from interfaz.cuadricula import EditorMatriz
from interfaz.desarrollo import crear_notacion
from interfaz.metodos_numericos import CAMPOS, METODOS_NUMERICOS, casos_numericos, ejecutar_numerico, parametros_defecto, parametros_vacios, resumen_numerico
from interfaz.operaciones import Presentacion
from interfaz.procedimiento import VistaProcedimiento
from interfaz.recorrido import INTERVALO_PASOS_MS, ReproductorPasos
from interfaz.lenguaje_pasos import explicar_paso
from interfaz.numericos.teclado import TecladoFuncion


class PanelNumerico(ttk.Frame):
    """Mantiene una sesión numérica separada de los resultados exactos de álgebra."""

    def __init__(self, padre, tema, al_calcular=None, al_guardar=None):
        """Prepara formularios y temporizador sin importar SciPy, NumPy o Matplotlib."""
        super().__init__(padre, padding=(18, 8))
        self.nombre, self.tema, self.vistas = 'Numéricos', tema, padre
        self.al_calcular, self.al_guardar = al_calcular, al_guardar
        self.clave = 'num_biseccion'
        self.vigente, self.presentacion, self.reproductor = False, None, None
        self._cargando, self._desarrollo_pendiente = True, True
        self.historial, self.instantanea = [], None
        self.estado = tk.StringVar(self, 'Completa los datos; los resultados de esta unidad son aproximados.')
        self.escalar = tk.StringVar(self, '2')
        self.parametros = {k: tk.StringVar(self, v) for k, v in parametros_vacios(self.clave).items()}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self._crear_cabecera()
        self._crear_tarjetas()
        self._crear_previa()
        self._crear_desarrollo()
        self.reproductor = ReproductorPasos(self.after, self.after_cancel, self._mostrar_paso, lambda: INTERVALO_PASOS_MS, self._actualizar_controles)
        for variable in self.parametros.values():
            variable.trace_add('write', self.marcar_cambio)
        self._configurar()
        self._cargando = False
        self._presentar()
        self.instantanea = self._capturar()
        self._actualizar_controles()

    def _crear_cabecera(self):
        """Presenta el catálogo numérico y ejemplos sin añadir pestañas internas."""
        cabecera = ttk.Frame(self)
        cabecera.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        # La cabecera global ya identifica la unidad; reservar altura para sus campos.
        barra = ttk.Frame(cabecera)
        barra.pack(fill='x')
        self.selector = ttk.Combobox(barra, values=[m.nombre for m in METODOS_NUMERICOS.values()], state='readonly', width=44)
        self.selector.current(0)
        self.selector.pack(side='left')
        self.selector.bind('<<ComboboxSelected>>', self._cambiar_metodo)
        self.ejemplo_boton = ttk.Button(barra, text='Cargar ejemplo', command=self.cargar_ejemplo)
        self.ejemplo_boton.pack(side='left', padx=10)
        ttk.Button(barra, text='Teoremas', command=self.ver_teoremas).pack(side='right')

    def _crear_tarjetas(self):
        """Reserva datos, opciones y resultado en la distribución aprobada."""
        self.tarjetas = ttk.Frame(self)
        self.tarjetas.grid(row=1, column=0, sticky='nsew')
        self.tarjetas.rowconfigure(0, weight=1)
        self.grupos, self.campos, self.entradas = [], {}, {}
        for columna, titulo in enumerate(('Datos del ejercicio', 'Opciones y referencia')):
            self.tarjetas.columnconfigure(columna, weight=1, uniform='numericos')
            grupo = ttk.Frame(self.tarjetas, style='Tarjeta.TFrame', padding=12)
            grupo.grid(row=0, column=columna, sticky='nsew', padx=(0, 6))
            ttk.Label(grupo, text=titulo, style='TarjetaTitulo.TLabel').pack(anchor='w')
            self.grupos.append(grupo)
        for nombre, (etiqueta, _) in CAMPOS.items():
            columna = 0 if nombre in ('funcion', 'a', 'b', 'verdadero', 'aproximado', 'x', 'delta', 'capital', 'tasa', 'numero') else 1
            marco = ttk.Frame(self.grupos[columna], style='Interior.TFrame')
            ttk.Label(marco, text=etiqueta, style='Tarjeta.TLabel').pack(anchor='w')
            if nombre in ('criterio', 'base'):
                valores = ('intervalo', 'porcentual') if nombre == 'criterio' else ('2', '10')
                ttk.Combobox(marco, textvariable=self.parametros[nombre], values=valores, state='readonly', width=16).pack(fill='x', pady=(2, 0))
            else:
                entrada = ttk.Entry(marco, textvariable=self.parametros[nombre], width=18)
                entrada.pack(fill='x', pady=(2, 0))
                self.entradas[nombre] = entrada
            self.campos[nombre] = marco
        self.teclado = TecladoFuncion(self.grupos[0], self.entradas['funcion'], self._edicion)
        self.ayuda_entrada = ttk.Label(self.grupos[0], style='Tarjeta.TLabel', wraplength=240, justify='left')
        self.nota = ttk.Label(self.grupos[1], style='Tarjeta.TLabel', wraplength=240, justify='left')
        for grupo, etiqueta in ((self.grupos[0], self.ayuda_entrada), (self.grupos[1], self.nota)):
            grupo.bind('<Configure>', lambda e, n=etiqueta: n.configure(wraplength=max(120, e.width - 28)))
        self.editores = {n: EditorMatriz(self.tarjetas, n, self.marcar_cambio, self.mostrar_error, self.tema) for n in ('A', 'b')}
        self.editores['b'].cargar([[''], ['']])
        self.tarjetas.columnconfigure(2, weight=1, uniform='numericos')
        resultado = ttk.Frame(self.tarjetas, style='Tarjeta.TFrame', padding=12)
        resultado.grid(row=0, column=2, sticky='nsew', padx=(6, 0))
        ttk.Label(resultado, text='Resultado aproximado', style='TarjetaTitulo.TLabel').pack(anchor='w')
        self.guardar = ttk.Button(resultado, text='Guardar ejercicio…', command=self.al_guardar)
        self.guardar.pack(side='bottom', fill='x', pady=(8, 0))
        self.resultado_texto = tk.Text(resultado, wrap='word', width=22, height=8, state='disabled', font=('Segoe UI', 10))
        self.tema.vincular(self.resultado_texto, bg='tarjeta', fg='texto')
        barra = ttk.Scrollbar(resultado, command=self.resultado_texto.yview)
        barra.pack(side='right', fill='y')
        self.resultado_texto.configure(yscrollcommand=barra.set)
        self.resultado_texto.pack(fill='both', expand=True)

    def _crear_previa(self):
        """Comparte el recorrido breve, ritmo fijo y acciones habituales del proyecto."""
        acciones = ttk.Frame(self)
        acciones.grid(row=2, column=0, sticky='ew', pady=10)
        ttk.Button(acciones, text='Calcular', style='Principal.TButton', command=self.calcular).pack(side='left')
        ttk.Button(acciones, text='Limpiar', command=self.limpiar).pack(side='left', padx=4)
        self.deshacer_boton = ttk.Button(acciones, text='Deshacer', command=self.deshacer)
        self.deshacer_boton.pack(side='left')
        self.grafica = ttk.Button(acciones, text='Ver gráfica', command=self.ver_grafica)
        self.grafica.pack(side='right')
        breve = ttk.Frame(self, style='Tarjeta.TFrame', padding=12)
        breve.grid(row=3, column=0, sticky='ew')
        self.titulo_paso = ttk.Label(breve, text='Vista previa del procedimiento', style='TarjetaTitulo.TLabel', wraplength=800)
        self.titulo_paso.pack(anchor='w')
        self.formula = crear_notacion(breve, self.tema, 60, 14)
        controles = ttk.Frame(breve, style='Interior.TFrame')
        controles.pack(fill='x', pady=(6, 0))
        self.anterior = ttk.Button(controles, text='‹ Anterior', command=lambda: self.reproductor.anterior())
        self.anterior.pack(side='left')
        self.reproducir = ttk.Button(controles, text='▶ Reproducir', command=self.alternar_recorrido)
        self.reproducir.pack(side='left', padx=4)
        self.siguiente = ttk.Button(controles, text='Siguiente ›', command=lambda: self.reproductor.siguiente())
        self.siguiente.pack(side='left')
        ttk.Button(controles, text='Todos los pasos y tabla ↗', command=lambda: self.vistas.select(self.pagina_pasos)).pack(side='right')
        ttk.Label(self, textvariable=self.estado, style='Estado.TLabel', wraplength=860).grid(row=4, column=0, sticky='ew', pady=(6, 0))

    def _crear_desarrollo(self):
        """Construye una tabla desplazable y el procedimiento completo en la vista general."""
        self.pagina_pasos = ttk.Frame(self.vistas, padding=(18, 8))
        ttk.Label(self.pagina_pasos, text='Todos los pasos · Numéricos', style='Titulo.TLabel').pack(anchor='w')
        ttk.Button(self.pagina_pasos, text='‹ Volver a calculadora', command=lambda: self.vistas.select(self)).pack(side='bottom', anchor='w')
        self.marco_tabla = ttk.Frame(self.pagina_pasos)
        self.tabla = ttk.Treeview(self.marco_tabla, show='headings', height=6)
        self.tabla.grid(row=0, column=0, sticky='nsew')
        self.marco_tabla.columnconfigure(0, weight=1)
        for orientacion, fila, columna in (('horizontal', 1, 0), ('vertical', 0, 1)):
            barra = ttk.Scrollbar(self.marco_tabla, orient=orientacion, command=self.tabla.xview if fila == 1 else self.tabla.yview)
            barra.grid(row=fila, column=columna, sticky='ew' if fila == 1 else 'ns')
            self.tabla.configure(**{'xscrollcommand' if fila == 1 else 'yscrollcommand': barra.set})
        self.desarrollo = VistaProcedimiento(self.pagina_pasos, self.tema)
        self.desarrollo.pack(fill='both', expand=True, pady=8)

    def _configurar(self):
        """Oculta campos ajenos al método conservando sus valores para volver después."""
        metodo = METODOS_NUMERICOS[self.clave]
        self.teclado.pack_forget()
        self.nota.pack_forget()
        self.ayuda_entrada.pack_forget()
        for marco in self.campos.values():
            marco.pack_forget()
        for grupo in self.grupos:
            grupo.grid()
        for editor in self.editores.values():
            editor.grid_remove()
        for nombre in metodo.campos_a + metodo.campos_b:
            self.campos[nombre].pack(fill='x', pady=(4, 0))
            if nombre == 'funcion':
                self.teclado.pack(fill='x', pady=(6, 2))
        ayudas = {
            'num_biseccion': 'Intervalo: tolerancia en x.\nPorcentual: error relativo (%).\nResiduo: tolerancia independiente.',
            'num_errores': 'Comparamos el valor aproximado con el verdadero. Si el verdadero es cero, el error relativo y porcentual no están definidos.',
            'num_propagacion': 'Deja el paso vacío para elegirlo automáticamente. La estimación usa la derivada cerca del punto x.',
            'num_simulacion': 'La tasa se escribe en decimal: 0.005 equivale a 0.5 %. Comparamos truncamiento y redondeo en cada iteración.',
            'num_flotante': 'Se comparan float32 y float64: épsilon, números demasiado grandes (overflow) y demasiado pequeños (underflow). Consulta los ejemplos en Todos los pasos.',
            'num_inestabilidad': 'Directa: √(x + 1) − √x\nReformulada: 1 / (√(x + 1) + √x)\n\nRepresentan lo mismo, pero pueden dar distinta precisión. Usa x ≥ 0. Por ejemplo, 1e16 significa 10^16.',
            'num_bases': 'Elige base 2 o 10 y cuántas cifras mostrar. Si queda un resto, la representación se ha truncado.',
            'num_inversa': 'Introduce una matriz A cuadrada e invertible. Comparamos la inversa exacta con float propio y NumPy.',
        }
        if self.clave in ayudas:
            self.nota.configure(text=ayudas[self.clave])
            self.nota.pack(fill='x', pady=(10, 0))
        if self.clave == 'num_flotante':
            self.ayuda_entrada.configure(text='Esta demostración no necesita datos de entrada.\n\nPulsa Calcular para ver los experimentos de punto flotante.')
            self.ayuda_entrada.pack(fill='x', pady=(10, 0))
        self.ejemplo_boton.configure(state='disabled' if self.clave == 'num_flotante' else 'normal')
        for columna, nombre in enumerate(metodo.matrices):
            self.grupos[columna].grid_remove()
            self.editores[nombre].grid(row=0, column=columna, sticky='nsew', padx=(0, 6))

    def seleccionar(self, clave):
        """Elige un método numérico disponible sin cambiar los demás temas."""
        self.selector.current(list(METODOS_NUMERICOS).index(clave))
        self._cambiar_metodo()

    def _cambiar_metodo(self, evento=None):
        """Conserva entradas y exige recalcular al cambiar el método."""
        clave = list(METODOS_NUMERICOS)[self.selector.current()]
        if clave == self.clave:
            return
        self._recordar()
        self.clave = clave
        # Una respuesta de otro método no debe aparecer bajo la selección nueva.
        self.presentacion = None
        self._configurar()
        self._invalidar()
        self.instantanea = self._capturar()

    def entradas_matriciales(self):
        """Devuelve únicamente A/b cuando el método numérico los requiere."""
        return {n: self.editores[n] for n in METODOS_NUMERICOS[self.clave].matrices}

    def _capturar(self):
        """Copia parámetros, matrices y último cálculo para deshacer sin alterar el método."""
        return deepcopy(dict(clave=self.clave, parametros={k: v.get() for k, v in self.parametros.items()},
                             matrices={n: [[c.get() for c in f] for f in e.celdas] for n, e in self.editores.items()},
                             presentacion=self.presentacion, vigente=self.vigente))

    def _recordar(self):
        """Conserva hasta cincuenta acciones locales."""
        if self.instantanea is not None:
            self.historial = (self.historial + [self.instantanea])[-50:]

    def _invalidar(self):
        """Marca la respuesta anterior y detiene toda reproducción pendiente."""
        self.vigente = False
        self._desarrollo_pendiente = True
        if self.reproductor is not None:
            self.reproductor.preparar(())
        self.formula.mostrar_formula([])
        self.titulo_paso.configure(text='Vista previa del procedimiento · Pulsa Calcular')
        self._escribir_resultado()
        self.estado.set('Datos modificados · Pulsa Calcular para actualizar la aproximación.')
        self._actualizar_controles()
        self._cambiar_vista()

    def marcar_cambio(self, *argumentos):
        """Registra cambios solo después de terminar la construcción de los editores."""
        if self._cargando or any(e.cargando for e in self.editores.values()):
            return
        self._recordar()
        self._invalidar()
        self.instantanea = self._capturar()

    @contextmanager
    def _edicion(self):
        """Agrupa cargas completas como una acción de historial."""
        self._recordar()
        self._cargando = True
        try:
            yield
        finally:
            self._cargando = False
            self._invalidar()
            self.instantanea = self._capturar()

    def casos(self):
        """Ofrece ejemplos pertinentes al método numérico elegido."""
        return casos_numericos(self.clave)

    def cargar_ejemplo(self):
        """Carga el ejemplo inicial del método sin calcular automáticamente."""
        self.cargar_caso(self.casos()[0])

    def cargar_caso(self, caso):
        """Carga casos de bisección o matrices de Hilbert, preservando las fracciones de entrada."""
        if caso not in self.casos():
            raise ValueError('El caso no corresponde al método seleccionado.')
        datos = parametros_defecto(self.clave)
        with self._edicion():
            if self.clave == 'num_biseccion':
                if caso == 'cos(x)-x':
                    datos.update(funcion='cos(x)-x', a='0', b='1')
                elif caso == 'Sin cambio de signo':
                    datos.update(funcion='x^2+1', a='-1', b='1')
                elif caso == 'Raíz en extremo':
                    datos.update(funcion='x-1', a='1', b='3')
            if self.clave in ('num_inversa', 'num_sistema'):
                if caso == 'Hilbert 5×5':
                    from modulos.numericos.comparadores import hilbert
                    matriz = hilbert(5)
                    b = [[sum(fila)] for fila in matriz]
                else:
                    matriz = [[1, 2], [2, 4]] if caso == 'Singular' else [[2, 1], [1, -1]]
                    b = [[5], [1]]
                self.editores['A'].cargar(matriz)
                self.editores['b'].cargar(b)
            for nombre, valor in datos.items():
                self.parametros[nombre].set(valor)

    def calcular(self, registrar=True):
        """Valida datos y ejecuta el método; conserva el último resultado si hay un error."""
        self._invalidar()
        try:
            parametros = {k: v.get().strip() for k, v in self.parametros.items()}
            matrices = {n: e.leer() for n, e in self.entradas_matriciales().items()}
            calculo = ejecutar_numerico(self.clave, parametros, matrices)
        except ImportError:
            self.mostrar_error('Instala las dependencias con: python -m pip install -r requirements-numericos.txt')
            return
        except (ValueError, OverflowError, ZeroDivisionError) as error:
            self.mostrar_error(str(error))
            return
        self._recordar()
        self.presentacion = Presentacion(calculo, resumen_numerico(self.clave, calculo), None)
        self.vigente = True
        self._presentar()
        self.instantanea = self._capturar()
        if registrar and self.al_calcular is not None:
            self.al_calcular(self)

    def _presentar(self):
        """Muestra aproximaciones como texto, sin convertirlas a resultados matriciales exactos."""
        self._escribir_resultado()
        self.formula.mostrar_formula([])
        self.titulo_paso.configure(text='Vista previa del procedimiento · Pulsa Calcular')
        self.reproductor.preparar(self.presentacion.calculo.pasos if self.vigente and self.presentacion else ())
        if self.vigente:
            self.reproductor.reiniciar()
        self.estado.set('Cálculo numérico completado · Consulta tabla y todos los pasos.' if self.vigente else 'Último cálculo · datos modificados' if self.presentacion else 'Completa los datos o carga un ejemplo y pulsa Calcular.')
        self._desarrollo_pendiente = True
        self._cambiar_vista()
        self._actualizar_controles()

    def _escribir_resultado(self):
        """Distingue un cálculo anterior de una respuesta vigente."""
        texto = 'Todavía no hay resultado para este método.'
        if self.presentacion:
            prefijo = '' if self.vigente else 'Resultado anterior · Vuelve a calcular con los datos actuales.\n\n'
            texto = prefijo + self.presentacion.resumen
        self.resultado_texto.configure(state='normal')
        self.resultado_texto.delete('1.0', 'end')
        self.resultado_texto.insert('1.0', texto)
        self.resultado_texto.configure(state='disabled')

    def limpiar(self):
        """Vacía el resultado y reinicia parámetros sin cambiar el método."""
        with self._edicion():
            for nombre, valor in parametros_vacios(self.clave).items():
                self.parametros[nombre].set(valor)
            for editor in self.editores.values():
                editor.vaciar()
            self.presentacion = None
            self._presentar()

    def deshacer(self):
        """Restaura la acción anterior manteniendo el método actualmente elegido."""
        if not self.historial:
            return
        anterior = self.historial.pop()
        self._cargando = True
        self._invalidar()
        for k, v in anterior['parametros'].items():
            self.parametros[k].set(v)
        for n, matriz in anterior['matrices'].items():
            self.editores[n].cargar(matriz)
        self.presentacion = anterior['presentacion'] if anterior['clave'] == self.clave else None
        self.vigente = anterior['vigente'] and anterior['clave'] == self.clave
        self._cargando = False
        self._presentar()
        self.instantanea = self._capturar()

    def _mostrar_paso(self, paso, indice, total):
        """Muestra solo la fórmula esencial; el resto permanece en la vista completa."""
        self.titulo_paso.configure(text=f'{indice + 1}/{total} · {paso.titulo}\n{explicar_paso(paso)}')
        self.formula.mostrar_formula(paso.formulas[0] if paso.formulas else [paso.detalle])

    def _actualizar_controles(self):
        """Habilita acciones según vigencia y disponibilidad de la gráfica."""
        if self.reproductor is None:
            return
        for boton in (self.anterior, self.reproducir, self.siguiente, self.guardar):
            boton.configure(state='normal' if self.vigente else 'disabled')
        self.reproducir.configure(text='Ⅱ Pausar' if self.reproductor.activo else '▶ Reproducir')
        self.deshacer_boton.configure(state='normal' if self.historial else 'disabled')
        graficable = self.clave in ('num_biseccion', 'num_propagacion', 'num_simulacion', 'num_inversa', 'num_sistema')
        self.grafica.configure(state='normal' if self.vigente and graficable else 'disabled')

    def alternar_recorrido(self):
        """Alterna reproducción sin permitir ajustar los dos segundos por etapa."""
        self.reproductor.pausar() if self.reproductor.activo else self.reproductor.reproducir()

    def pausar(self):
        """Cancela el temporizador al navegar o cerrar."""
        self.reproductor.pausar()

    def _cambiar_vista(self):
        """Construye tabla y todos los pasos bajo demanda, sin truncar las filas."""
        if self.vistas.select() != str(self.pagina_pasos) or not self._desarrollo_pendiente:
            return
        self.pausar()
        calculo = self.presentacion.calculo if self.presentacion else None
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.marco_tabla.pack_forget()
        if calculo is not None and calculo.datos.get('filas'):
            columnas = calculo.datos['columnas']
            self.tabla.configure(columns=tuple(str(i) for i in range(len(columnas))))
            for i, nombre in enumerate(columnas):
                self.tabla.heading(str(i), text=nombre)
                self.tabla.column(str(i), width=120, stretch=False)
            for fila in calculo.datos['filas']:
                self.tabla.insert('', 'end', values=tuple('No definido' if v is None else f'{v:.14g}' if isinstance(v, float) else str(v) for v in fila))
            self.marco_tabla.pack(fill='x', before=self.desarrollo)
        self.desarrollo.mostrar_procedimiento(calculo.pasos if calculo else (),
                                             'Desarrollo numérico completo' if self.vigente else 'Último cálculo · datos modificados')
        self._desarrollo_pendiente = False

    def mostrar_error(self, mensaje):
        """Comunica un error conservando parámetros y último cálculo válido."""
        self.estado.set(mensaje)

    def ver_grafica(self):
        """Abre únicamente por acción del usuario la gráfica correspondiente al cálculo."""
        if not self.vigente:
            return
        try:
            from interfaz.numericos.graficas import abrir_grafica
            abrir_grafica(self, self.clave, self.presentacion.calculo, self.tema)
        except ImportError:
            self.mostrar_error('Falta Matplotlib: instala requirements-numericos.txt.')

    def ver_teoremas(self):
        """Muestra supuestos y criterios de la unidad numérica."""
        from teoremas.resumen_teoremas import teoremas_tema
        ventana = tk.Toplevel(self)
        ventana.title('Teoremas · Semana 12')
        ttk.Label(ventana, text=teoremas_tema('Numéricos'), padding=20, wraplength=650, justify='left').pack()
