"""Expone los cálculos de semana 12 en consola conservando los menús anteriores.

Tema: funciones, tablas completas, contraste de bibliotecas y errores recuperables.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.entradas import elegir_matriz, leer_opcion
from interfaz.menu_algebra import formatear_pasos
from interfaz.metodos_numericos import CAMPOS, METODOS_NUMERICOS, ejecutar_numerico, parametros_defecto, resumen_numerico
from teoremas.resumen_teoremas import teoremas_tema


def menu_numerico(ultimo_resultado=None):
    """Pide datos originales y muestra tabla/pasos; nunca convierte aproximaciones en matrices exactas."""
    claves = list(METODOS_NUMERICOS)
    while True:
        print('\n' + '=' * 58 + '\n [ f(x) ~ 0 ]  METODOS NUMERICOS · SEMANA 12\n' + '=' * 58)
        for i, clave in enumerate(claves, 1):
            print(f'{i}. {METODOS_NUMERICOS[clave].nombre}')
        print('0. Ver Teoremas Clave del Módulo\n99. Volver')
        opcion = leer_opcion('Elige: ', ('0', '99') + tuple(str(i) for i in range(1, len(claves) + 1)))
        if opcion == '99':
            return ultimo_resultado
        if opcion == '0':
            print(teoremas_tema('Numéricos'))
            continue
        clave = claves[int(opcion) - 1]
        metodo, parametros = METODOS_NUMERICOS[clave], parametros_defecto(clave)
        for nombre in metodo.campos_a + metodo.campos_b:
            valor = input(f'{CAMPOS[nombre][0]} [{parametros[nombre]}]: ').strip()
            if valor:
                parametros[nombre] = valor
        matrices = {nombre: elegir_matriz(nombre, ultimo_resultado) for nombre in metodo.matrices}
        try:
            calculo = ejecutar_numerico(clave, parametros, matrices)
        except ImportError:
            print('Instala: python -m pip install -r requirements-numericos.txt')
            continue
        except (ValueError, OverflowError) as error:
            print(f'No se pudo calcular: {error}')
            continue
        print(resumen_numerico(clave, calculo))
        if calculo.datos.get('filas'):
            print(' | '.join(calculo.datos['columnas']))
            for fila in calculo.datos['filas']:
                print(' | '.join('No definido' if v is None else f'{v:.14g}' if isinstance(v, float) else str(v) for v in fila))
        if leer_opcion('¿Ver todos los pasos? 1. Sí / 2. No: ', ('1', '2')) == '1':
            print(formatear_pasos(calculo.pasos))
