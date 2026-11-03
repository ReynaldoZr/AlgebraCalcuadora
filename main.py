"""Inicia la calculadora local de Álgebra Lineal.

Tema: operaciones matriciales y organización modular.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.menus import menu_principal

VERSION = "0.1.0"


def main():
    """Ejecuta el menú y permite terminar sin mostrar errores de consola."""
    try:
        menu_principal(VERSION)
    except (EOFError, KeyboardInterrupt):
        print("\nSesión terminada. Hasta pronto.")


if __name__ == "__main__":
    main()
