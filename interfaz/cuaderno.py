"""Conecta la biblioteca y las herramientas de estudio con las sesiones existentes.

Tema: guardado y recuperación de ejercicios, sin cambiar algoritmos o distribución.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
from tkinter import filedialog, ttk

from interfaz.biblioteca import Biblioteca, ETIQUETAS, crear_registro, leer_matriz_guardada, ruta_biblioteca
from interfaz.ejemplos_casos import AYUDAS, casos_disponibles, ejemplo_por_caso
from interfaz.explicacion import etapas_completas
from interfaz.exportar_pdf import exportar_pdf
from interfaz.operaciones import OPERACIONES
from modulos.procedimientos import Paso


class Cuaderno:
    """Coordina herramientas compartidas; cada tema conserva su propia sesión."""

    def __init__(self, app, biblioteca=None):
        """Carga datos locales y conecta Biblioteca y Estudio a la cabecera."""
        from interfaz.guardados import VistaGuardados
        self.app = app
        self.biblioteca = biblioteca if biblioteca is not None else Biblioteca(ruta_biblioteca())
        self.vista = VistaGuardados(app.pestanas, app.tema, self)
        app.pestanas.add(self.vista, text='Biblioteca')
        app.pestanas.hide(self.vista)
        ttk.Button(app.navegacion.cabecera, text='Biblioteca', command=app.mostrar_biblioteca).pack(side='right', padx=8)
        self.boton = ttk.Menubutton(app.navegacion.cabecera, text='Estudio ▾')
        self.boton.pack(side='right', padx=4)
        self.menu = tk.Menu(self.boton, tearoff=False, postcommand=self._crear_menu)
        app.tema.vincular(self.menu, bg='tarjeta', fg='texto', activebackground='acento', activeforeground='sobre_acento')
        self.boton.configure(menu=self.menu)

    def fuente(self):
        """Obtiene el tema elegido incluso mientras la persona consulta Guardados."""
        tema = self.app.tema_seleccionado
        return self.app if tema == 'Matrices' else self.app.paneles_algebra[tema]

    def editores(self, fuente=None):
        """Devuelve solamente las entradas reales del método seleccionado."""
        fuente = fuente or self.fuente()
        if fuente is self.app:
            return {'A': fuente.editor_a} if fuente.operacion.get() in ('escalar', 'transponer') else {
                'A': fuente.editor_a, 'B': fuente.editor_b}
        if fuente.nombre == 'Numéricos':
            return fuente.entradas_matriciales()
        return {nombre: fuente.editores[nombre] for nombre in OPERACIONES[fuente.clave].entradas}

    def clave(self, fuente=None):
        """Devuelve el identificador del método actual sin consultar etiquetas dibujadas."""
        fuente = fuente or self.fuente()
        return fuente.operacion.get() if fuente is self.app else fuente.clave

    def _crear_menu(self):
        """Actualiza las acciones al abrir el menú según el método y su vigencia."""
        self.menu.delete(0, 'end')
        fuente = self.fuente()
        estado = 'normal' if fuente.vigente else 'disabled'
        self.menu.add_command(label='Guardar ejercicio completo…', state=estado, command=self.dialogo_guardar_ejercicio)
        for nombre in self.editores(fuente):
            self.menu.add_command(label=f'Guardar matriz {nombre}…', command=lambda n=nombre: self.dialogo_guardar_matriz(n))
        tiene_matriz = fuente.resultado is not None if fuente is self.app else (
            fuente.presentacion is not None and fuente.presentacion.matriz is not None)
        self.menu.add_command(label='Guardar matriz resultado…', state=estado if tiene_matriz else 'disabled', command=lambda: self.dialogo_guardar_matriz('Resultado'))
        self.menu.add_separator()
        self.menu.add_command(label='Exportar ejercicio a PDF…', state=estado, command=self.exportar_actual)
        self.menu.add_separator()
        self.menu.add_command(label='Ejemplos por caso…', command=self.dialogo_ejemplos)
        self.menu.add_command(label='Ayudas de estudio…', command=self.dialogo_ayudas)

    def ejercicio(self, fuente=None):
        """Captura entradas y el desarrollo completo del último cálculo vigente."""
        fuente = fuente or self.fuente()
        if not fuente.vigente:
            raise ValueError('Pulsa Calcular antes de guardar o exportar el ejercicio actualizado.')
        clave = self.clave(fuente)
        entradas = {nombre: editor.leer() for nombre, editor in self.editores(fuente).items()}
        if fuente is not self.app and fuente.nombre == 'Numéricos':
            from interfaz.metodos_numericos import METODOS_NUMERICOS
            metodo = METODOS_NUMERICOS[clave]
            registro = crear_registro('Numéricos', clave, entradas, resumen=fuente.presentacion.resumen,
                                     pasos=fuente.presentacion.calculo.pasos)
            registro['parametros'] = {k: fuente.parametros[k].get() for k in metodo.campos_a + metodo.campos_b}
            return registro
        if fuente is self.app:
            # Se captura el resultado completo, aunque la reproducción muestre solo una parte.
            pasos = [Paso('Matriz ' + nombre, matriz=matriz) for nombre, matriz in entradas.items()]
            for i, paso in enumerate(fuente._pasos_calculo()):
                for etapa in etapas_completas(paso, i):
                    pasos.append(Paso(f'R[{paso[0] + 1},{paso[1] + 1}] · {etapa.titulo}', etapa.mensaje,
                                      formulas=(etapa.tokens,)))
            pasos.append(Paso('Resultado final', matriz=fuente.resultado))
            resumen = ETIQUETAS[clave][0] + ' · Resultado exacto'
            resultado = fuente.resultado
            tema = 'Matrices'
        else:
            pasos = fuente.presentacion.calculo.pasos
            resumen, resultado, tema = fuente.presentacion.resumen, fuente.presentacion.matriz, fuente.nombre
        usa_escalar = clave == 'escalar' if fuente is self.app else OPERACIONES[clave].escalar
        escalar = fuente.escalar.get() if usa_escalar else '2'
        registro = crear_registro(tema, clave, entradas, escalar, resultado, resumen, pasos)
        if clave.startswith('prop_'):
            registro['etiqueta'] = OPERACIONES[clave].nombre
        return registro

    def matriz(self, nombre):
        """Captura una entrada o resultado; el símbolo corresponde a su procedencia."""
        fuente = self.fuente()
        if nombre == 'Resultado':
            ejercicio = self.ejercicio(fuente)
            if ejercicio['resultado'] is None:
                raise ValueError('Este ejercicio no produce una matriz reutilizable.')
            matriz = leer_matriz_guardada(ejercicio['resultado'])
            registro = crear_registro(ejercicio['tema'], ejercicio['operacion'], {'A': matriz},
                                     resultado=matriz, resumen='Matriz resultado guardada por separado.', tipo='matriz')
        else:
            matriz = self.editores(fuente)[nombre].leer()
            registro = crear_registro(self.app.tema_seleccionado, self.clave(), {'A': matriz},
                                     resultado=matriz, resumen=f'Matriz {nombre} guardada por separado.', tipo='matriz')
            registro.update(etiqueta=f'Matriz {nombre}', simbolo=f'[{nombre}]')
        return registro

    def registrar(self, fuente):
        """Añade cálculos válidos al historial sin impedir trabajar si falla el disco."""
        try:
            self.biblioteca.registrar_historial(self.ejercicio(fuente))
        except (OSError, ValueError) as error:
            fuente.estado.set(f'Cálculo válido · No se pudo guardar el historial: {error}')

    def dialogo_guardar_ejercicio(self, permanecer=False):
        """Prepara el guardado manual del ejercicio actual con nombre y notas opcionales."""
        try:
            self.dialogo_nombre(self.ejercicio(), permanecer=permanecer)
        except ValueError as error:
            self.fuente().mostrar_error(str(error))

    def dialogo_guardar_matriz(self, nombre, permanecer=False):
        """Prepara una matriz validada sin alterar sus entradas."""
        try:
            self.dialogo_nombre(self.matriz(nombre), permanecer=permanecer)
        except ValueError as error:
            self.fuente().mostrar_error(str(error))

    def guardar_resultado_directo(self):
        """Guarda la respuesta en la biblioteca sin salir de la calculadora actual."""
        self.dialogo_guardar_matriz('Resultado', permanecer=True)

    def dialogo_nombre(self, registro, editar=False, permanecer=False):
        """Permite nombre propio y notas en un solo diálogo; vacío genera nombre automático."""
        ventana = tk.Toplevel(self.app.raiz)
        ventana.title('Editar guardado' if editar else 'Guardar en mi biblioteca')
        ventana.transient(self.app.raiz)
        marco = ttk.Frame(ventana, padding=18)
        marco.pack(fill='both', expand=True)
        ttk.Label(marco, text=registro['simbolo'] + ' · ' + registro['etiqueta'], style='TarjetaTitulo.TLabel').pack(anchor='w')
        ttk.Label(marco, text='Nombre (vacío = automático)' if not editar else 'Nombre').pack(anchor='w', pady=(12, 4))
        nombre = ttk.Entry(marco, width=48)
        nombre.pack(fill='x')
        nombre.insert(0, registro['nombre'] if editar else '')
        ttk.Label(marco, text='Símbolo (puedes personalizarlo)').pack(anchor='w', pady=(12, 4))
        simbolo = ttk.Entry(marco, width=20)
        simbolo.insert(0, registro['simbolo'])
        simbolo.pack(anchor='w')
        ttk.Label(marco, text='Notas opcionales').pack(anchor='w', pady=(12, 4))
        notas = tk.Text(marco, height=5, width=48, wrap='word')
        self.app.tema.vincular(notas, bg='entrada', fg='texto', insertbackground='texto')
        notas.pack(fill='both', expand=True)
        notas.insert('1.0', registro['notas'])
        aviso = ttk.Label(marco, style='Error.TLabel', wraplength=430)
        aviso.pack(fill='x', pady=8)
        ttk.Button(marco, text='Guardar', style='Principal.TButton', command=lambda: self._confirmar_guardado(
            registro, nombre.get(), notas.get('1.0', 'end-1c'), editar, ventana, aviso, simbolo.get(), permanecer)).pack(anchor='e')
        nombre.focus_set()

    def _confirmar_guardado(self, registro, nombre, notas, editar, ventana, aviso, simbolo=None, permanecer=False):
        """Escribe solo al pulsar Guardar; los errores mantienen el diálogo y sus datos."""
        try:
            if editar:
                self.biblioteca.renombrar(registro['id'], nombre, notas, simbolo)
                identificador = registro['id']
            else:
                identificador = self.biblioteca.guardar(registro, nombre, notas, simbolo)['id']
        except (ValueError, OSError) as error:
            aviso.configure(text=str(error))
            return
        ventana.destroy()
        self.vista.modo.set('Guardados')
        self.vista.busqueda.set('')
        self.vista.actualizar()
        self.vista.arbol.selection_set(identificador)
        self.vista.arbol.see(identificador)
        self.vista.seleccionar()
        if permanecer:
            self.fuente().estado.set('Resultado guardado en tu biblioteca. Puedes continuar calculando.')
        else:
            self.app.mostrar_biblioteca()

    def abrir_ejercicio(self, registro):
        """Restaura entradas y método y recalcula sin duplicar el historial al abrirlo."""
        if registro['tipo'] != 'ejercicio':
            raise ValueError('Para una matriz utiliza «Usar matriz».')
        clave, tema = registro['operacion'], registro['tema']
        if tema == 'Numéricos':
            self._abrir_numerico(registro)
            return
        if tema == 'Matrices':
            if clave not in ETIQUETAS or clave not in ('sumar', 'restar', 'escalar', 'transponer', 'multiplicar'):
                raise ValueError('Este método guardado no está disponible en esta versión.')
            necesarios = ('A',) if clave in ('escalar', 'transponer') else ('A', 'B')
        else:
            if clave not in OPERACIONES or OPERACIONES[clave].tema != tema:
                raise ValueError('Este método guardado no está disponible en esta versión.')
            necesarios = OPERACIONES[clave].entradas
        matrices = {n: leer_matriz_guardada(registro['entradas'][n]) for n in necesarios}
        self._validar_tamanos(matrices.values())
        if tema == 'Matrices':
            self.app.mostrar_matrices()
            fuente = self.app
            fuente.operacion.set(clave)
        else:
            fuente = self.app.abrir_tema(tema)
            fuente.seleccionar(clave)
        with fuente._edicion():
            for nombre, matriz in matrices.items():
                self.editores(fuente)[nombre].cargar(matriz)
            fuente.escalar.set(registro['escalar'])
        fuente.calcular(registrar=False)

    def _abrir_numerico(self, registro):
        """Recupera parámetros aproximados sin convertirlos en una matriz exacta ficticia."""
        from interfaz.biblioteca import validar_registro
        validar_registro(registro)
        matrices = {n: leer_matriz_guardada(m) for n, m in registro['entradas'].items()}
        self._validar_tamanos(matrices.values())
        panel = self.app.abrir_tema('Numéricos')
        panel.seleccionar(registro['operacion'])
        with panel._edicion():
            for nombre, valor in registro['parametros'].items():
                panel.parametros[nombre].set(valor)
            for nombre, matriz in matrices.items():
                panel.editores[nombre].cargar(matriz)
        panel.calcular(registrar=False)

    @staticmethod
    def _validar_tamanos(matrices):
        """Evita cargar en las casillas una matriz que exceda los límites de escritorio."""
        if any(len(m) > 10 or len(m[0]) > 10 for m in matrices):
            raise ValueError('La cuadrícula admite como máximo 10×10; el guardado original se conserva.')

    def usar_matriz(self, registro, origen='Resultado', destino='A'):
        """Copia una matriz guardada al tema seleccionado, sin compartir memoria."""
        matriz = registro['resultado'] if origen == 'Resultado' else registro['entradas'].get(origen)
        if matriz is None:
            raise ValueError('Ese resultado no contiene una matriz; elige una entrada guardada.')
        matriz = leer_matriz_guardada(matriz)
        self._validar_tamanos((matriz,))
        fuente = self.fuente()
        if destino not in self.editores(fuente):
            raise ValueError('Esa entrada no forma parte del método seleccionado.')
        with fuente._edicion():
            self.editores(fuente)[destino].cargar(matriz)
        if fuente is self.app:
            self.app.mostrar_matrices()
        else:
            self.app.abrir_tema(fuente.nombre)

    def aplicar_caso(self, caso):
        """Carga un caso manteniendo método, historial de deshacer y datos de otros temas."""
        fuente = self.fuente()
        if fuente is not self.app and fuente.nombre == 'Numéricos':
            fuente.cargar_caso(caso)
            self.app.abrir_tema('Numéricos')
            return
        datos, escalar = ejemplo_por_caso(self.clave(), caso)
        with fuente._edicion():
            for nombre, editor in self.editores(fuente).items():
                editor.cargar(datos[nombre])
            fuente.escalar.set(escalar)
        if fuente is self.app:
            self.app.mostrar_matrices()
        else:
            self.app.abrir_tema(fuente.nombre)

    def dialogo_ejemplos(self):
        """Muestra una selección corta de casos válidos para la operación elegida."""
        ventana = tk.Toplevel(self.app.raiz)
        ventana.title('Ejemplos por caso')
        marco = ttk.Frame(ventana, padding=18)
        marco.pack(fill='both', expand=True)
        ttk.Label(marco, text='Elige un caso para el método actual.').pack(anchor='w', pady=(0, 8))
        fuente = self.fuente()
        casos = fuente.casos() if fuente is not self.app and fuente.nombre == 'Numéricos' else casos_disponibles(self.clave())
        selector = ttk.Combobox(marco, values=casos, state='readonly', width=38)
        selector.current(0)
        selector.pack(fill='x')
        ttk.Button(marco, text='Cargar caso', command=lambda: self._cargar_caso_dialogo(selector.get(), ventana)).pack(anchor='e', pady=(12, 0))

    def _cargar_caso_dialogo(self, caso, ventana):
        """Carga el caso y cierra el diálogo sin iniciar automáticamente el cálculo."""
        try:
            self.aplicar_caso(caso)
        except ValueError as error:
            self.fuente().mostrar_error(str(error))
        else:
            ventana.destroy()

    def dialogo_ayudas(self):
        """Explica términos bajo demanda, sin añadir párrafos al recorrido breve."""
        ventana = tk.Toplevel(self.app.raiz)
        ventana.title('Ayudas de estudio')
        marco = ttk.Frame(ventana, padding=20)
        marco.pack(fill='both', expand=True)
        selector = ttk.Combobox(marco, values=tuple(AYUDAS), state='readonly', width=40)
        selector.current(0)
        selector.pack(fill='x')
        texto = ttk.Label(marco, text=AYUDAS[selector.get()], wraplength=480, justify='left')
        texto.pack(fill='both', expand=True, pady=(16, 0))
        selector.bind('<<ComboboxSelected>>', lambda evento: texto.configure(text=AYUDAS[selector.get()]))

    def exportar_actual(self):
        """Exporta el ejercicio vigente sin necesitar guardarlo primero en la biblioteca."""
        try:
            self.exportar(self.ejercicio())
        except (ValueError, OSError) as error:
            self.fuente().mostrar_error(str(error))

    def exportar(self, registro):
        """Solicita una ubicación y escribe el desarrollo completo como PDF de texto."""
        ruta = filedialog.asksaveasfilename(parent=self.app.raiz, title='Exportar ejercicio completo',
                                          defaultextension='.pdf', filetypes=(('Documento PDF', '*.pdf'),),
                                          initialfile='ejercicio-algebra.pdf')
        if ruta:
            exportar_pdf(registro, ruta)
            self.vista.aviso.configure(text='PDF exportado con todos los pasos.')
