"""Detecta incumplimientos básicos de estructura y documentación.

Tema: separación de cálculo, interfaz y bibliotecas por unidad.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import ast
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
EXTERNAS = {'numpy', 'scipy', 'sympy', 'matplotlib', 'pandas'}
NUMERICAS = {'numpy', 'scipy', 'matplotlib'}


def revisar_import(nodo, calculo, numerico):
    """Devuelve motivos de rechazo para un import según el ámbito de su archivo."""
    nombres = [alias.name for alias in nodo.names] if isinstance(nodo, ast.Import) else [nodo.module or '']
    errores = []
    for nombre in nombres:
        raiz = nombre.split('.')[0]
        if raiz in EXTERNAS and (not numerico or raiz not in NUMERICAS):
            errores.append(f'Biblioteca {raiz} fuera del ámbito numérico permitido.')
        if calculo and raiz == 'interfaz':
            errores.append('El cálculo no debe importar la interfaz.')
        if calculo and raiz not in sys.stdlib_module_names | {'modulos', 'teoremas'}:
            if not (numerico and raiz in NUMERICAS):
                errores.append(f'Import no permitido en cálculo: {nombre}.')
        if calculo and raiz in {'builtins', 'importlib'}:
            errores.append('No ocultar entrada/salida ni imports mediante aliases dinámicos.')
        if calculo and isinstance(nodo, ast.ImportFrom) and nodo.level:
            errores.append('Usar imports absolutos para comprobar las dependencias del cálculo.')
        if calculo and raiz == 'math' and not numerico:
            errores.append('No usar math en el cálculo algebraico de las tareas 1–6.')
        if calculo and raiz == 'modulos' and '.numericos' in nombre and not numerico:
            errores.append('El álgebra anterior no debe depender de Métodos Numéricos.')
        if calculo and isinstance(nodo, ast.ImportFrom) and nombre == 'modulos':
            if any(alias.name == 'numericos' for alias in nodo.names) and not numerico:
                errores.append('El álgebra anterior no debe importar el paquete numérico.')
    return errores


def revisar_archivo(ruta):
    """Analiza un archivo Python y devuelve infracciones con su posición."""
    arbol = ast.parse(ruta.read_text(encoding='utf-8'), filename=str(ruta))
    relativa = ruta.relative_to(RAIZ)
    calculo = relativa.parts[0] == 'modulos' or relativa.as_posix() == 'teoremas/verificadores.py'
    numerico = relativa.parts[:2] in (('modulos', 'numericos'), ('tests', 'numericos'), ('interfaz', 'numericos'))
    errores = []
    if not ast.get_docstring(arbol):
        errores.append((1, 'Falta docstring de módulo.'))
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) and not ast.get_docstring(nodo):
            errores.append((nodo.lineno, 'Falta docstring de función.'))
        if isinstance(nodo, (ast.Import, ast.ImportFrom)):
            errores.extend((nodo.lineno, motivo) for motivo in revisar_import(nodo, calculo, numerico))
        if isinstance(nodo, ast.Name) and calculo and nodo.id in {'input', 'print', '__import__', 'eval', 'exec', 'importlib', 'builtins'}:
            errores.append((nodo.lineno, f'{nodo.id} no está permitido dentro del cálculo.'))
    return [(relativa.as_posix(), linea, motivo) for linea, motivo in errores]


def main():
    """Revisa las carpetas de código y devuelve 0 si no detecta infracciones."""
    archivos = list(RAIZ.glob('*.py'))
    for carpeta in ('modulos', 'interfaz', 'teoremas', 'tests', 'herramientas'):
        archivos.extend((RAIZ / carpeta).rglob('*.py'))
    errores = [error for ruta in archivos for error in revisar_archivo(ruta)]
    for archivo, linea, motivo in errores:
        print(f'{archivo}:{linea}: {motivo}')
    if errores:
        return 1
    print(f'Reglas verificadas en {len(archivos)} archivos Python.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
