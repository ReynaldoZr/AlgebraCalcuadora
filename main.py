"""Inicia la calculadora local de Álgebra Lineal.

Tema: operaciones matriciales y organización modular.
Equipo responsable: Grupo 9.
"""

from interfaz.menus import menu_principal

# Identificación del avance acordada por Reynaldo; no equivale a una release pública.
VERSION = "1.0.0"


def main():
    """Ejecuta el menú y permite terminar sin mostrar errores de consola."""
    try:
        menu_principal(VERSION)
    except (EOFError, KeyboardInterrupt):
        print("\nSesión terminada. Hasta pronto.")


if __name__ == "__main__":
    main()
