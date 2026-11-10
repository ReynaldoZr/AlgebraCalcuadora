"""Facilita escribir expresiones con los signos admitidos por la calculadora.

Tema: entrada de funciones, sin modificar los algoritmos numéricos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from tkinter import ttk


class TecladoFuncion(ttk.Frame):
    """Inserta signos en el cursor de una entrada de función existente."""

    def __init__(self, padre, entrada, editar):
        """Recibe la entrada y el contexto que agrupa cada pulsación al deshacer."""
        super().__init__(padre, style='Interior.TFrame')
        self.entrada, self.editar = entrada, editar
        self.botones = {}
        signos = (
            ('x', 'x'), ('+', '+'), ('−', '-'), ('×', '*'), ('÷', '/'),
            ('(', '('), (')', ')'), ('x²', 'x^2'), ('xⁿ', 'x^'), ('⌫', None),
        )
        for i, (etiqueta, texto) in enumerate(signos):
            boton = ttk.Button(
                self, text=etiqueta, width=4, padding=(3, 3), takefocus=False,
                command=lambda t=texto: self.insertar(t),
            )
            boton.grid(row=i // 5, column=i % 5, sticky='ew', padx=2, pady=2)
            self.columnconfigure(i % 5, weight=1)
            self.botones[etiqueta] = boton

    def insertar(self, texto):
        """Respeta cursor y selección; borrar elimina solo un carácter o selección."""
        entrada = self.entrada
        inicio = fin = entrada.index('insert')
        if entrada.selection_present():
            inicio, fin = entrada.index('sel.first'), entrada.index('sel.last')
        elif texto is None:
            inicio = max(0, inicio - 1)

        if texto is None and inicio == fin:
            entrada.focus_set()
            return

        # Una pulsación completa equivale a una sola acción de Deshacer.
        with self.editar():
            entrada.delete(inicio, fin)
            entrada.insert(inicio, texto or '')
        entrada.selection_clear()
        entrada.icursor(inicio + len(texto or ''))
        entrada.focus_set()
