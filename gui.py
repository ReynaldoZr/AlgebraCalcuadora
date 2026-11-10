"""Abre la interfaz Qt Quick conservando main.py para la consola.

Tema: punto de entrada de escritorio configurado en IntelliJ.
Elaboración: equipo del proyecto, con apoyo de IA.
"""


def main():
    """Importa la nueva ventana bajo demanda; gui_tk.py conserva la anterior."""
    from gui_qt import main as iniciar_qt
    return iniciar_qt()


if __name__ == "__main__":
    raise SystemExit(main())
