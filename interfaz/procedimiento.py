"""Presenta procedimientos generales completos con desplazamiento vertical.

Tema: matrices aumentadas y desarrollo de sistemas, determinantes e inversas.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from tkinter import ttk

from interfaz.desarrollo import Desarrollo, crear_notacion
from interfaz.lenguaje_pasos import explicar_paso


class VistaProcedimiento(Desarrollo):
    """Reutiliza el área desplazable para pasos matemáticos de diferentes temas."""

    def mostrar_procedimiento(self, pasos, aviso):
        """Dibuja todas las fórmulas y matrices, sin resumir ni limitar la cantidad."""
        self.pasos = tuple(pasos)
        self.aviso.configure(text=aviso)
        for hijo in self.cuerpo.winfo_children():
            hijo.destroy()
        for indice, paso in enumerate(self.pasos):
            tarjeta = ttk.Frame(self.cuerpo, style='Tarjeta.TFrame', padding=14)
            tarjeta.pack(fill='x', pady=(0, 10), padx=(0, 4))
            titulo = ttk.Label(tarjeta, text=f'{indice + 1}. {paso.titulo}', style='TarjetaTitulo.TLabel', wraplength=620)
            titulo.pack(anchor='w')
            explicacion = explicar_paso(paso, completo=True)
            nota = ttk.Label(tarjeta, text=explicacion, style='Tarjeta.TLabel', justify='left', wraplength=620)
            if explicacion:
                nota.pack(anchor='w', pady=(6, 4))
            for formula in paso.formulas:
                crear_notacion(tarjeta, self.tema, 62, 15).mostrar_formula(formula)
            if paso.matriz is not None:
                alto = min(340, len(paso.matriz) * 58 + 28)
                crear_notacion(tarjeta, self.tema, alto, 15).mostrar_matriz(paso.matriz, separador=paso.separador)
            tarjeta.bind('<Configure>', lambda evento, t=titulo, n=nota: self._ajustar_etiquetas(evento.width, t, n))
        self._vincular_rueda(self.cuerpo)
        self.lienzo.yview_moveto(0)
