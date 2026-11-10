"""Define resultados y pasos reutilizables sin depender de la interfaz.

Tema: procedimientos exactos de las tareas 1 a 6.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Paso:
    """Conserva una explicación breve, fórmulas y una matriz independiente."""

    titulo: str
    detalle: str = ""
    matriz: list | None = None
    formulas: tuple = ()
    separador: int | None = None


@dataclass(frozen=True)
class Calculo:
    """Devuelve el valor, su procedimiento y datos auxiliares documentados."""

    valor: object
    pasos: tuple = ()
    datos: dict = field(default_factory=dict)


class ErrorCalculo(ValueError):
    """Comunica una limitación matemática conservando el procedimiento realizado."""

    def __init__(self, mensaje, pasos=()):
        """Recibe el diagnóstico y una secuencia independiente de pasos."""
        super().__init__(mensaje)
        self.pasos = tuple(pasos)
