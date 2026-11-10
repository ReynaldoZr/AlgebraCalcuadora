"""Abre la nueva interfaz Qt Quick sin sustituir la consola ni la interfaz Tk.

Tema: lanzador de la migración visual de escritorio.
Elaboración: equipo del proyecto, con apoyo de IA.
"""


def main():
    """Carga Qt solo al ejecutarlo; explica cómo instalar la dependencia opcional."""
    try:
        from interfaz.qt.aplicacion import iniciar
    except ModuleNotFoundError as error:
        if not error.name.startswith(('PySide6', 'shiboken6')):
            raise
        print('Instala la interfaz con: python -m pip install -r requirements-interfaz.txt')
        print('La consola sigue disponible con: python main.py')
        return 1
    return iniciar()


if __name__ == '__main__':
    raise SystemExit(main())
