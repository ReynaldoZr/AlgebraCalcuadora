"""Muestra la biblioteca personal y el historial en una única pestaña.

Tema: búsqueda, nombres, notas, recuperación y exportación de ejercicios locales.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from datetime import datetime, timedelta, timezone
import tkinter as tk
from tkinter import messagebox, ttk

from interfaz.biblioteca import leer_matriz_guardada, recuperar_pasos
from interfaz.desarrollo import crear_notacion
from interfaz.procedimiento import VistaProcedimiento
from modulos.procedimientos import Paso


def fecha_visible(texto):
    """Presenta fechas de guardado en la zona horaria de Nicaragua (UTC−6)."""
    try:
        return datetime.fromisoformat(texto).astimezone(timezone(timedelta(hours=-6))).strftime('%d/%m/%Y %H:%M')
    except ValueError:
        return texto


class VistaGuardados(ttk.Frame):
    """Mantiene la biblioteca aparte de las tres tarjetas originales de cálculo."""

    def __init__(self, padre, tema, cuaderno):
        """Construye listado, búsqueda y vista previa sin diálogos automáticos."""
        super().__init__(padre, padding=(18, 8))
        self.tema = tema
        self.cuaderno = cuaderno
        self.registros = {}
        self.modo = tk.StringVar(self, 'Guardados')
        self.busqueda = tk.StringVar(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        cabecera = ttk.Frame(self)
        cabecera.grid(row=0, column=0, sticky='ew', pady=(0, 12))
        ttk.Label(cabecera, text='Mis matrices y ejercicios', style='Titulo.TLabel').pack(side='left')
        self.volver = ttk.Button(cabecera, text='‹ Volver a la lista', command=self.cerrar_desarrollo)
        self._crear_filtros()
        self.area = ttk.Frame(self)
        self.area.grid(row=2, column=0, sticky='nsew')
        self._crear_lista()
        self.detalle = VistaProcedimiento(self.area, tema)
        self._crear_acciones()
        self.aviso = ttk.Label(self, style='Estado.TLabel', wraplength=880)
        self.aviso.grid(row=4, column=0, sticky='ew', pady=(8, 0))
        self.modo.trace_add('write', self.actualizar)
        self.busqueda.trace_add('write', self.actualizar)
        self.actualizar()

    def _crear_filtros(self):
        """Permite cambiar entre guardados e historial y buscar nombres, operaciones o notas."""
        barra = ttk.Frame(self)
        barra.grid(row=1, column=0, sticky='ew', pady=(0, 12))
        for nombre in ('Guardados', 'Historial'):
            ttk.Radiobutton(barra, text=nombre, value=nombre, variable=self.modo).pack(side='left')
        ttk.Label(barra, text='Buscar:').pack(side='left', padx=(20, 6))
        ttk.Entry(barra, textvariable=self.busqueda, width=26).pack(side='left', fill='x', expand=True)

    def _crear_lista(self):
        """Organiza la lista y su vista previa con desplazamiento propio."""
        self.lista = ttk.Panedwindow(self.area, orient='horizontal')
        self.lista.pack(fill='both', expand=True)
        izquierda = ttk.Frame(self.lista)
        izquierda.columnconfigure(0, weight=1)
        izquierda.rowconfigure(0, weight=1)
        self.arbol = ttk.Treeview(izquierda, columns=('tipo', 'fecha'), selectmode='browse')
        self.arbol.heading('#0', text='Símbolo · Nombre')
        self.arbol.heading('tipo', text='Tipo')
        self.arbol.heading('fecha', text='Guardado')
        self.arbol.column('#0', width=220, minwidth=130)
        self.arbol.column('tipo', width=85, minwidth=70, stretch=False)
        self.arbol.column('fecha', width=125, minwidth=120, stretch=False)
        self.arbol.grid(row=0, column=0, sticky='nsew')
        for eje, orientacion, fila, columna in (('y', 'vertical', 0, 1), ('x', 'horizontal', 1, 0)):
            barra = ttk.Scrollbar(izquierda, orient=orientacion, command=self.arbol.yview if eje == 'y' else self.arbol.xview)
            barra.grid(row=fila, column=columna, sticky='ns' if eje == 'y' else 'ew')
            self.arbol.configure(**{eje + 'scrollcommand': barra.set})
        derecha = ttk.Frame(self.lista, style='Tarjeta.TFrame', padding=12)
        derecha.columnconfigure(0, weight=1)
        derecha.rowconfigure(3, weight=1, minsize=90)
        self.titulo = ttk.Label(derecha, text='Selecciona un guardado', style='TarjetaTitulo.TLabel', wraplength=330)
        self.titulo.grid(row=0, column=0, sticky='ew')
        self.metadatos = ttk.Label(derecha, style='Coordenada.TLabel', wraplength=330)
        self.metadatos.grid(row=1, column=0, sticky='ew', pady=8)
        texto = ttk.Frame(derecha, style='Interior.TFrame')
        texto.grid(row=2, column=0, sticky='ew')
        self.texto = tk.Text(texto, height=7, width=32, wrap='word', state='disabled', font=('Segoe UI', 10))
        self.tema.vincular(self.texto, bg='tarjeta', fg='texto')
        self.texto.pack(side='left', fill='both', expand=True)
        barra = ttk.Scrollbar(texto, command=self.texto.yview)
        barra.pack(side='right', fill='y')
        self.texto.configure(yscrollcommand=barra.set)
        matriz = ttk.Frame(derecha, style='Interior.TFrame')
        matriz.grid(row=3, column=0, sticky='nsew')
        self.matriz = crear_notacion(matriz, self.tema, 160, 16)
        derecha.bind('<Configure>', lambda evento: self._ajustar_ancho(evento.width))
        self.lista.add(izquierda, weight=3)
        self.lista.add(derecha, weight=2)
        self.arbol.bind('<<TreeviewSelect>>', self.seleccionar)

    def _ajustar_ancho(self, ancho):
        """Evita que un nombre largo ensanche la tarjeta de vista previa."""
        for etiqueta in (self.titulo, self.metadatos):
            etiqueta.configure(wraplength=max(140, ancho - 28))

    def _crear_acciones(self):
        """Separa recuperación de datos de la edición y eliminación de guardados."""
        acciones = ttk.Frame(self)
        acciones.grid(row=3, column=0, sticky='ew', pady=(12, 0))
        self.botones = {}
        for texto, comando in (('Abrir ejercicio', self.abrir), ('Usar matriz', self.dialogo_usar),
                               ('Ver desarrollo', self.ver_desarrollo)):
            boton = ttk.Button(acciones, text=texto, command=comando)
            boton.pack(side='left', padx=(0, 4))
            self.botones[texto] = boton
        secundaria = ttk.Frame(self)
        secundaria.grid(row=5, column=0, sticky='ew', pady=(4, 0))
        for texto, comando in (('Guardar del historial', self.guardar_historial), ('Nombre y notas', self.editar),
                               ('Exportar PDF', self.exportar), ('Eliminar', self.eliminar)):
            boton = ttk.Button(secundaria, text=texto, command=comando)
            boton.pack(side='left', padx=(0, 4))
            self.botones[texto] = boton

    def actualizar(self, *argumentos):
        """Filtra registros y conserva la selección cuando aún existe."""
        seleccion = self.arbol.selection()
        seleccion = seleccion[0] if seleccion else None
        historial = self.modo.get() == 'Historial'
        registros = self.cuaderno.biblioteca.listar(historial)
        consulta = self.busqueda.get().strip().casefold()
        registros = [r for r in registros if consulta in ' '.join(
            r[k] for k in ('nombre', 'notas', 'etiqueta', 'tema', 'simbolo')).casefold()]
        self.registros = {r['id']: r for r in registros}
        for identificador in self.arbol.get_children():
            self.arbol.delete(identificador)
        for registro in registros:
            self.arbol.insert('', 'end', iid=registro['id'], text=registro['simbolo'] + ' · ' + registro['nombre'],
                              values=(registro['tipo'].capitalize(), fecha_visible(registro['fecha'])))
        if seleccion in self.registros:
            self.arbol.selection_set(seleccion)
        self.aviso.configure(text=self.cuaderno.biblioteca.error_lectura or (
            f'{len(registros)} elementos · ' + ('Últimos 100 cálculos válidos' if historial else 'Guardados en este equipo')))
        self.cerrar_desarrollo()
        self.seleccionar()

    def registro(self):
        """Devuelve el registro seleccionado o comunica que hace falta elegir uno."""
        seleccion = self.arbol.selection()
        if not seleccion or seleccion[0] not in self.registros:
            raise ValueError('Selecciona una matriz o ejercicio de la lista.')
        return self.registros[seleccion[0]]

    def seleccionar(self, evento=None):
        """Dibuja una vista previa y habilita solo las acciones aplicables."""
        try:
            registro = self.registro()
        except ValueError:
            self.titulo.configure(text='Selecciona un guardado')
            self.metadatos.configure(text='')
            self._mostrar_texto('Guarda desde «Guardar / Estudio» o recupera un cálculo del historial.')
            self.matriz.mostrar_formula([])
            for boton in self.botones.values():
                boton.configure(state='disabled')
            return
        self.titulo.configure(text=registro['simbolo'] + ' · ' + registro['nombre'])
        self.metadatos.configure(text=registro['tema'] + ' · ' + registro['etiqueta'] + '\n' + fecha_visible(registro['fecha']))
        self._mostrar_texto((registro['notas'] + '\n\n' if registro['notas'] else '') + registro['resumen'])
        matriz = registro['resultado'] or next(iter(registro['entradas'].values()), None)
        if matriz is not None:
            self.matriz.mostrar_matriz(leer_matriz_guardada(matriz))
        else:
            self.matriz.mostrar_formula(['Ejercicio numérico', registro['simbolo']])
        for boton in self.botones.values():
            boton.configure(state='normal')
        historial = self.modo.get() == 'Historial'
        self.botones['Abrir ejercicio'].configure(state='normal' if registro['tipo'] == 'ejercicio' else 'disabled')
        self.botones['Guardar del historial'].configure(state='normal' if historial else 'disabled')
        self.botones['Nombre y notas'].configure(state='disabled' if historial else 'normal')
        self.botones['Usar matriz'].configure(state='normal' if matriz is not None and self.cuaderno.editores() else 'disabled')

    def _mostrar_texto(self, texto):
        """Actualiza un resumen de solo lectura con desplazamiento."""
        self.texto.configure(state='normal')
        self.texto.delete('1.0', 'end')
        self.texto.insert('1.0', texto)
        self.texto.configure(state='disabled')

    def abrir(self):
        """Recupera el ejercicio seleccionado sin pedir reescribir operandos."""
        try:
            self.cuaderno.abrir_ejercicio(self.registro())
        except (ValueError, KeyError) as error:
            self.aviso.configure(text=str(error))

    def ver_desarrollo(self):
        """Amplía la vista con el desarrollo guardado completo, sin pestañas anidadas."""
        try:
            registro = self.registro()
            pasos = recuperar_pasos(registro)
            if not pasos:
                pasos = (Paso('Matriz guardada', registro['resumen'], leer_matriz_guardada(registro['resultado'])),)
            pasos = (Paso(registro['nombre'], registro['resumen']),) + pasos
        except ValueError as error:
            self.aviso.configure(text=str(error))
            return
        self.detalle.mostrar_procedimiento(pasos, 'Desarrollo guardado · ' + registro['nombre'])
        self.lista.pack_forget()
        self.detalle.pack(fill='both', expand=True)
        self.volver.pack(side='right')

    def cerrar_desarrollo(self):
        """Vuelve a la lista sin perder el guardado seleccionado."""
        self.detalle.pack_forget()
        self.lista.pack(fill='both', expand=True)
        self.volver.pack_forget()

    def guardar_historial(self):
        """Permite convertir un elemento del historial en guardado permanente con nombre propio."""
        try:
            self.cuaderno.dialogo_nombre(self.registro())
        except ValueError as error:
            self.aviso.configure(text=str(error))

    def editar(self):
        """Abre la edición del nombre y las notas del elemento seleccionado."""
        try:
            self.cuaderno.dialogo_nombre(self.registro(), editar=True)
        except ValueError as error:
            self.aviso.configure(text=str(error))

    def exportar(self):
        """Exporta la instantánea guardada, aunque el cálculo actual sea diferente."""
        try:
            self.cuaderno.exportar(self.registro())
        except (ValueError, OSError) as error:
            self.aviso.configure(text=str(error))

    def eliminar(self):
        """Solicita confirmación local antes de quitar únicamente el elemento elegido."""
        try:
            registro = self.registro()
            if messagebox.askyesno('Eliminar guardado', f'¿Eliminar «{registro["nombre"]}»?', parent=self):
                self.cuaderno.biblioteca.eliminar(registro['id'], self.modo.get() == 'Historial')
                self.actualizar()
        except (ValueError, OSError) as error:
            self.aviso.configure(text=str(error))

    def dialogo_usar(self):
        """Permite elegir matriz de origen y casilla de destino antes de cargarla."""
        try:
            registro = self.registro()
            if not self.cuaderno.editores():
                raise ValueError('Elige primero un método que tenga entradas matriciales.')
        except ValueError as error:
            self.aviso.configure(text=str(error))
            return
        ventana = tk.Toplevel(self)
        ventana.title('Usar matriz guardada')
        marco = ttk.Frame(ventana, padding=18)
        marco.pack(fill='both', expand=True)
        ttk.Label(marco, text='Origen del guardado:').pack(anchor='w')
        opciones = (['Resultado'] if registro['resultado'] is not None else []) + list(registro['entradas'])
        origen = ttk.Combobox(marco, values=opciones, state='readonly', width=30)
        origen.current(0)
        origen.pack(fill='x', pady=(4, 12))
        ttk.Label(marco, text='Destino en ' + self.cuaderno.app.tema_seleccionado + ':').pack(anchor='w')
        destino = ttk.Combobox(marco, values=tuple(self.cuaderno.editores()), state='readonly', width=30)
        destino.current(0)
        destino.pack(fill='x', pady=(4, 12))
        aviso = ttk.Label(marco, style='Error.TLabel', wraplength=340)
        aviso.pack(fill='x')
        ttk.Button(marco, text='Cargar matriz', command=lambda: self._usar(registro, origen.get(), destino.get(), ventana, aviso)).pack(anchor='e')

    def _usar(self, registro, origen, destino, ventana, aviso):
        """Carga la copia elegida y conserva el diálogo si falla una validación."""
        try:
            self.cuaderno.usar_matriz(registro, origen, destino)
        except ValueError as error:
            aviso.configure(text=str(error))
        else:
            ventana.destroy()
