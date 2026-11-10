"""Abre la interfaz gráfica opcional de la calculadora.

Tema: edición de matrices en una ventana de escritorio.
Elaboración: equipo del proyecto, con apoyo de IA.
"""


def main():
    """Inicia la ventana sin cambiar el punto de entrada de consola."""
    try:
        # Tk es opcional para la consola; por eso la ventana se importa al ejecutarla.
        from interfaz.ventana import iniciar_ventana
    except ModuleNotFoundError as error:
        if error.name not in {"tkinter", "_tkinter"}:
            raise
        print("Esta instalación de Python no incluye Tkinter.")
        print("Puedes seguir usando la consola con: python main.py")
        return 1
    iniciar_ventana()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
