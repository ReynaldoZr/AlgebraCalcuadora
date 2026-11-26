"""Muestra las cabeceras ASCII de la calculadora.

Tema: identidad de los módulos requerida desde el Programa 4.
Equipo responsable: Grupo 9.
"""


def mostrar_inicio(version):
    """Muestra el título de la calculadora y su versión."""
    print("\n======================================================")
    print("             CUADERNO DE ALGEBRA LINEAL")
    print(f"             Versión {version} | Python local")
    print("======================================================")
    print("Números: enteros, decimales con punto y fracciones como 1/3.")
    print("Puedes terminar en cualquier momento con Ctrl+C.")


def mostrar_matrices():
    """Muestra la cabecera del módulo y las operaciones disponibles hoy."""
    print("\n======================================================")
    print("  [ A ][ B ]   MODULO: ALGEBRA DE MATRICES")
    print("  [ C ][ D ]   Suma, resta, escalar, transpuesta y producto")
    print("======================================================")
