"""Selecciona la tarjeta estructurada de resultados de la issue 32.

Tema: Jacobi/Gauss-Seidel; los demás métodos conservan su resumen original.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.metodos_numericos import resumen_iterativo_estructurado


def resumen_estructurado(clave, presentacion):
    """Activa la tabla solo para los métodos iterativos incluidos en la issue."""
    return resumen_iterativo_estructurado(clave, presentacion.calculo)
