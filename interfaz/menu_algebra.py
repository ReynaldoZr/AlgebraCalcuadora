"""Ofrece en consola los temas de álgebra del catálogo compartido.

Tema: navegación, entradas y procedimientos, sin duplicar algoritmos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.entradas import elegir_matriz, leer_numero, leer_opcion
from interfaz.formato import formatear_matriz
from interfaz.operaciones import OPERACIONES, calcular_operacion
from teoremas.resumen_teoremas import teoremas_tema


def formatear_pasos(pasos):
    """Expone todas las fórmulas y matrices del procedimiento como texto."""
    lineas = []
    for indice, paso in enumerate(pasos):
        lineas.append(f'\n{indice + 1}. {paso.titulo}')
        if paso.detalle:
            lineas.append(paso.detalle)
        for formula in paso.formulas:
            lineas.append(' '.join(f'({v[0]})/({v[1]})' if isinstance(v, tuple) else str(v) for v in formula))
        if paso.matriz is not None:
            if paso.separador is not None:
                lineas.append(f'Matriz aumentada: las primeras {paso.separador} columnas son coeficientes.')
            lineas.append(formatear_matriz(paso.matriz))
    return '\n'.join(lineas)


def ejecutar_metodo(clave, ultimo_resultado):
    """Lee solo los operandos requeridos y conserva el resultado previo ante un error."""
    operacion = OPERACIONES[clave]
    print(operacion.ayuda)
    entradas = {nombre: elegir_matriz(nombre, ultimo_resultado) for nombre in operacion.entradas}
    escalar = leer_numero('Escalar k: ') if operacion.escalar else 2
    try:
        presentacion = calcular_operacion(clave, entradas, escalar)
    except ValueError as error:
        print(f'No se pudo calcular: {error}')
        if getattr(error, 'pasos', ()):
            print(formatear_pasos(error.pasos))
        return ultimo_resultado
    print(presentacion.resumen)
    if presentacion.matriz is not None:
        print(formatear_matriz(presentacion.matriz))
    if leer_opcion('¿Ver todos los pasos? 1. Sí / 2. No: ', ('1', '2')) == '1':
        print(formatear_pasos(presentacion.calculo.pasos))
    return presentacion.matriz if presentacion.matriz is not None else ultimo_resultado


def menu_algebra(tema, ultimo_resultado=None):
    """Presenta una cabecera ASCII, opción 0 de teoremas y métodos reales del tema."""
    claves = [clave for clave, op in OPERACIONES.items() if op.tema == tema]
    iconos = {'Sistemas': '[ [1 2 | 3] ]  [ [0 1 | 5] ]', 'Vectores': 'v1 + v2  ->  A x = 0',
              'Determinantes': '| A |', 'Inversas': '[ A | I ] -> [ I | A^-1 ]',
              'LU': '[ L ] [ U ] = [ A ]', 'Propiedades': '[ Izquierda ] == [ Derecha ]'}
    while True:
        print('\n' + '=' * 58 + f'\n{iconos[tema]}\nMODULO: {tema.upper()}\n' + '=' * 58)
        for indice, clave in enumerate(claves, 1):
            print(f'{indice}. {OPERACIONES[clave].nombre}')
        print('0. Ver Teoremas Clave del Módulo\n99. Volver')
        opcion = leer_opcion('Elige: ', ('0', '99') + tuple(str(i) for i in range(1, len(claves) + 1)))
        if opcion == '99':
            return ultimo_resultado
        if opcion == '0':
            print(teoremas_tema(tema))
        else:
            ultimo_resultado = ejecutar_metodo(claves[int(opcion) - 1], ultimo_resultado)
