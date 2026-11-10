"""Presenta el inicio por unidades y el menú de temas plegable.

Tema: navegación de escritorio; no calcula ni modifica ejercicios.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import tkinter as tk
from tkinter import ttk

from interfaz.notacion import crear_icono_matrices, crear_icono_tema

TEMAS = (
    ('Matrices', 'Suma, resta, producto y transpuesta'),
    ('Sistemas', 'Gauss y Gauss-Jordan'),
    ('Vectores', 'Operaciones, combinación e independencia'),
    ('Determinantes', 'Cofactores, Sarrus y reducción'),
    ('Inversas', 'Gauss-Jordan y adjunta'),
    ('LU', 'Factorización y solución de sistemas'),
    ('Propiedades', 'Comprobaciones y teoremas'),
    ('Numéricos', 'Bisección, errores y estabilidad'),
)


class Navegacion:
    """Dibuja los accesos; la ventana conserva las sesiones de cada tema."""

    def __init__(self, app):
        """Construye cabecera, inicio y menú reutilizando la paleta existente."""
        self.app, self.tema = app, app.tema
        self.botones, self.tarjetas = [], {}
        self.en_inicio = True
        self.cabecera = ttk.Frame(app.raiz, padding=(18, 10))
        self.cabecera.pack(fill='x')
        ttk.Button(self.cabecera, text='☰  Temas', command=self.alternar_menu).pack(side='left')
        ttk.Button(self.cabecera, text='Inicio', command=self.mostrar_inicio).pack(side='left', padx=8)
        self.ruta = ttk.Label(self.cabecera, text='Cuaderno de Álgebra', font=('Segoe UI', 12, 'bold'))
        self.ruta.pack(side='left', padx=12)
        app.cuerpo = ttk.Frame(app.raiz)
        app.cuerpo.pack(fill='both', expand=True)
        self.inicio = ttk.Frame(app.cuerpo, padding=(30, 24))
        self._crear_inicio()
        self.menu = ttk.Frame(app.cuerpo, style='Tarjeta.TFrame', padding=14, width=260)
        self._crear_menu()

    def _crear_inicio(self):
        """Agrupa las tarjetas por unidad sin ocultar los temas ya disponibles."""
        ttk.Label(self.inicio, text='Elige un tema para comenzar', style='Titulo.TLabel').pack(anchor='w')
        ttk.Label(self.inicio, text='Tus herramientas, organizadas por unidad',
                  style='Subtitulo.TLabel').pack(anchor='w', pady=(6, 28))
        grupos = ttk.Frame(self.inicio)
        grupos.pack(fill='both', expand=True)
        grupos.columnconfigure(0, weight=3)
        grupos.columnconfigure(1, weight=1)
        grupos.rowconfigure(0, weight=1)
        algebra = self._grupo(grupos, 'Álgebra lineal', 0)
        numericos = self._grupo(grupos, 'Métodos numéricos', 1)
        for columna in range(3):
            algebra.columnconfigure(columna, weight=1, uniform='inicio')
        for indice, (nombre, ayuda) in enumerate(TEMAS[:6]):
            self._tarjeta(algebra, nombre, ayuda, indice // 3 + 1, indice % 3)
        ttk.Button(algebra, text='Propiedades y teoremas →', command=lambda: self.elegir('Propiedades')).grid(
            row=3, column=0, columnspan=3, sticky='w', pady=(18, 4))
        numericos.columnconfigure(0, weight=1)
        self._tarjeta(numericos, *TEMAS[-1], 1, 0)
        ttk.Label(self.inicio, text='Tus matrices y ejercicios están en Biblioteca.',
                  style='Subtitulo.TLabel').pack(anchor='w', pady=(24, 4))

    def _grupo(self, padre, titulo, columna):
        """Crea una sección de tarjetas con su título de unidad."""
        grupo = ttk.Frame(padre, style='Tarjeta.TFrame', padding=18)
        grupo.grid(row=0, column=columna, sticky='nsew', padx=(0, 14) if columna == 0 else 0)
        ttk.Label(grupo, text=titulo, style='TarjetaTitulo.TLabel').grid(
            row=0, column=0, columnspan=3, sticky='w', pady=(0, 18))
        return grupo

    def _tarjeta(self, padre, nombre, ayuda, fila, columna):
        """Hace clicable toda la tarjeta y permite activarla también con el teclado."""
        tarjeta = tk.Frame(padre, padx=12, pady=18, borderwidth=0, highlightthickness=1)
        self.tema.vincular(tarjeta, bg='entrada', highlightbackground='borde')
        tarjeta.grid(row=fila, column=columna, sticky='nsew', padx=5, pady=6)
        icono = crear_icono_matrices(tarjeta, self.tema, False) if nombre == 'Matrices' else crear_icono_tema(tarjeta, self.tema, nombre)
        icono.pack(anchor='w', pady=(0, 12))
        boton = ttk.Button(tarjeta, text=nombre + '  ›', style='TarjetaTema.TButton', command=lambda: self.elegir(nombre))
        boton.pack(fill='x')
        etiqueta = tk.Label(tarjeta, text=ayuda, wraplength=175, justify='left', font=('Segoe UI', 10))
        self.tema.vincular(etiqueta, bg='entrada', fg='secundario')
        etiqueta.pack(anchor='w', pady=(10, 0))
        for widget in (tarjeta, icono, etiqueta):
            widget.bind('<Button-1>', lambda evento: self.elegir(nombre))
        self.tarjetas[nombre] = boton

    def _crear_menu(self):
        """Reutiliza los símbolos y deja el menú fuera del espacio de cálculo."""
        titulo = ttk.Frame(self.menu, style='Interior.TFrame')
        titulo.pack(fill='x', pady=(0, 12))
        ttk.Label(titulo, text='Temas', style='TarjetaTitulo.TLabel').pack(side='left')
        ttk.Button(titulo, text='×', width=3, command=self.cerrar_menu).pack(side='right')
        for nombre, _ in TEMAS:
            if nombre in ('Matrices', 'Numéricos'):
                ttk.Label(self.menu, text='Álgebra lineal' if nombre == 'Matrices' else 'Métodos numéricos',
                          style='Coordenada.TLabel').pack(anchor='w', pady=(10, 6))
            fila = ttk.Frame(self.menu, style='Interior.TFrame')
            fila.pack(fill='x', pady=3)
            icono = crear_icono_matrices(fila, self.tema) if nombre == 'Matrices' else crear_icono_tema(fila, self.tema, nombre)
            icono.pack(side='left', padx=(0, 6))
            boton = ttk.Button(fila, text=nombre, command=lambda n=nombre: self.elegir(n))
            boton.pack(side='left', fill='x', expand=True)
            boton.marco_tema, boton.icono_tema = fila, icono
            if nombre == 'Matrices':
                self.icono_matrices = icono
                self.boton_matrices = boton
            else:
                self.botones.append(boton)
            icono.bind('<Button-1>', lambda evento, n=nombre: self.elegir(n))
        ttk.Button(self.menu, text='⌂  Volver al inicio', command=self.mostrar_inicio).pack(fill='x', pady=(18, 0))

    def elegir(self, nombre):
        """Abre el tema pedido; no crea matrices ni calcula automáticamente."""
        if nombre == 'Matrices':
            return self.app.mostrar_matrices()
        return self.app.abrir_tema(nombre)

    def mostrar_trabajo(self):
        """Recupera el área de trabajo sin reconstruir sus formularios."""
        self.en_inicio = False
        self.cerrar_menu()
        # Ocultar conserva las sesiones; destruirlas haría perder entradas y resultados.
        self.inicio.pack_forget()
        self.app.zona.pack(fill='both', expand=True)

    def mostrar_inicio(self):
        """Pausa las explicaciones y conserva todos los datos al volver al inicio."""
        self.app.reproductor.pausar()
        for panel in self.app.paneles_algebra.values():
            panel.pausar()
        self.app.transicion.cancelar()
        self.cerrar_menu()
        self.en_inicio = True
        self.app.zona.pack_forget()
        self.inicio.pack(fill='both', expand=True)
        self.ruta.configure(text='Cuaderno de Álgebra')
        self.app.raiz.title('Cuaderno de Álgebra Lineal — Inicio · Local')

    def alternar_menu(self):
        """Superpone u oculta los temas sin comprimir las tres tarjetas."""
        if self.menu.winfo_manager():
            self.cerrar_menu()
        else:
            self.menu.place(x=12, y=4, width=260)
            self.menu.lift()

    def cerrar_menu(self):
        """Retira únicamente el menú, sin tocar la vista o el ejercicio."""
        self.menu.place_forget()

    def actualizar(self, nombre):
        """Sincroniza la ruta y el tema seleccionado con la vista actual."""
        unidad = 'Métodos numéricos' if nombre == 'Numéricos' else 'Álgebra lineal'
        if not self.en_inicio:
            self.ruta.configure(text=f'{unidad}  /  {nombre}')
            self.app.raiz.title(f'Cuaderno de Álgebra Lineal — {nombre} · Local')
        self.boton_matrices.configure(style='Principal.TButton' if nombre == 'Matrices' else 'TButton')
        self.icono_matrices.seleccionado = nombre == 'Matrices'
        self.icono_matrices.actualizar_tema()
        for boton in self.botones:
            seleccionado = boton.cget('text') == nombre
            boton.configure(style='Principal.TButton' if seleccionado else 'TButton')
            boton.icono_tema.seleccionado = seleccionado
            boton.icono_tema.actualizar_tema()
