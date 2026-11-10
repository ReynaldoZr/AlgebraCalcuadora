"""Coordina los menús y conecta datos, cálculos y resultados.

Tema: módulo de matrices y consulta de teoremas.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.cabeceras import mostrar_inicio, mostrar_matrices
from interfaz.entradas import elegir_matriz, leer_numero, leer_opcion
from interfaz.formato import (formatear_procedimiento_escalar, formatear_procedimiento_transpuesta,
                              formatear_procedimiento_producto, mostrar_matriz, mostrar_procedimiento)
from modulos.modulo_matrices import (multiplicar_por_escalar, producto_matricial, restar_matrices,
                                     sumar_matrices, transponer_matriz)
from teoremas.resumen_teoremas import teoremas_matrices
from interfaz.menu_algebra import menu_algebra


def ejecutar_operacion(opcion, ultimo_resultado):
    """Lee operandos, muestra suma o resta y devuelve el nuevo resultado válido."""
    matriz_a = elegir_matriz("A", ultimo_resultado)
    matriz_b = elegir_matriz("B", ultimo_resultado)
    try:
        if opcion == "1":
            resultado = sumar_matrices(matriz_a, matriz_b)
            signo = "+"
        else:
            resultado = restar_matrices(matriz_a, matriz_b)
            signo = "-"
    except ValueError as error:
        print(f"\nNo se pudo realizar la operación: {error}")
        return ultimo_resultado
    mostrar_matriz("A", matriz_a)
    mostrar_matriz("B", matriz_b)
    mostrar_matriz(f"Resultado A {signo} B", resultado)
    ver = leer_opcion("¿Ver procedimiento? 1. Sí / 2. No: ", ("1", "2"))
    if ver == "1":
        mostrar_procedimiento(matriz_a, matriz_b, resultado, signo)
    return resultado


def ejecutar_escalar(ultimo_resultado):
    """Lee A y k, presenta kA y permite reutilizarlo como siguiente resultado."""
    matriz = elegir_matriz("A", ultimo_resultado)
    escalar = leer_numero("Escalar k: ")
    try:
        resultado = multiplicar_por_escalar(matriz, escalar)
    except ValueError as error:
        print(f"\nNo se pudo realizar la operación: {error}")
        return ultimo_resultado
    mostrar_matriz("A", matriz)
    print(f"Escalar k = {escalar}")
    mostrar_matriz("Resultado kA", resultado)
    if leer_opcion("¿Ver procedimiento? 1. Sí / 2. No: ", ("1", "2")) == "1":
        print("\n" + formatear_procedimiento_escalar(matriz, escalar, resultado))
    return resultado


def ejecutar_transpuesta(ultimo_resultado):
    """Pide solo A, muestra su transpuesta y permite reutilizarla después."""
    matriz = elegir_matriz("A", ultimo_resultado)
    try:
        resultado = transponer_matriz(matriz)
    except ValueError as error:
        print(f"\nNo se pudo realizar la operación: {error}")
        return ultimo_resultado
    mostrar_matriz("A", matriz)
    mostrar_matriz("Resultado Aᵀ", resultado)
    if leer_opcion("¿Ver procedimiento? 1. Sí / 2. No: ", ("1", "2")) == "1":
        print("\n" + formatear_procedimiento_transpuesta(matriz, resultado))
    return resultado


def ejecutar_producto(ultimo_resultado):
    """Lee A/B, explica el producto y conserva la respuesta previa ante un error."""
    matriz_a = elegir_matriz("A", ultimo_resultado)
    matriz_b = elegir_matriz("B", ultimo_resultado)
    try:
        resultado = producto_matricial(matriz_a, matriz_b)
    except ValueError as error:
        print(f"\nNo se pudo realizar la operación: {error}")
        return ultimo_resultado
    mostrar_matriz("A", matriz_a)
    mostrar_matriz("B", matriz_b)
    mostrar_matriz("Resultado AB", resultado)
    if leer_opcion("¿Ver procedimiento? 1. Sí / 2. No: ", ("1", "2")) == "1":
        print("\n" + formatear_procedimiento_producto(matriz_a, matriz_b, resultado))
    return resultado


def menu_matrices(ultimo_resultado):
    """Ejecuta las opciones de matrices y devuelve el último resultado de la sesión."""
    while True:
        mostrar_matrices()
        print("1. Sumar matrices\n2. Restar matrices\n3. Ver último resultado")
        print("4. Multiplicar una matriz por un escalar")
        print("5. Transponer una matriz")
        print("6. Multiplicar matrices (AB)")
        print("7. Determinantes\n8. Inversas\n10. Verificador de propiedades")
        print("0. Ver Teoremas Clave del Módulo\n9. Volver al menú principal")
        opcion = leer_opcion("Elige: ", ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"))
        if opcion == "9":
            return ultimo_resultado
        if opcion == "0":
            print(teoremas_matrices())
        elif opcion == "3":
            if ultimo_resultado is None:
                print("Todavía no hay un resultado en esta sesión.")
            else:
                mostrar_matriz("Último resultado", ultimo_resultado)
        elif opcion == "4":
            ultimo_resultado = ejecutar_escalar(ultimo_resultado)
        elif opcion == "5":
            ultimo_resultado = ejecutar_transpuesta(ultimo_resultado)
        elif opcion == "6":
            ultimo_resultado = ejecutar_producto(ultimo_resultado)
        elif opcion in ("7", "8", "10"):
            ultimo_resultado = menu_algebra({'7': 'Determinantes', '8': 'Inversas', '10': 'Propiedades'}[opcion], ultimo_resultado)
        else:
            ultimo_resultado = ejecutar_operacion(opcion, ultimo_resultado)


def menu_principal(version):
    """Abre los temas disponibles y conserva el resultado mientras la app está abierta."""
    mostrar_inicio(version)
    ultimo_resultado = None
    while True:
        print("\nMENU PRINCIPAL\n1. Álgebra de matrices")
        print("2. Sistemas (Gauss y Gauss-Jordan)\n3. Vectores e independencia lineal")
        print("4. Determinantes\n5. Inversas\n6. Factorización LU y solución Ax=b\n7. Propiedades")
        print('8. Métodos numéricos · Semana 12')
        print("0. Ver teoremas disponibles\n9. Salir")
        opcion = leer_opcion("Elige: ", ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))
        if opcion == "9":
            print("Hasta pronto.")
            return
        if opcion == "0":
            print(teoremas_matrices())
        elif opcion == "1":
            ultimo_resultado = menu_matrices(ultimo_resultado)
        elif opcion == '8':
            from interfaz.menu_numerico import menu_numerico
            ultimo_resultado = menu_numerico(ultimo_resultado)
        else:
            tema = {'2': 'Sistemas', '3': 'Vectores', '4': 'Determinantes', '5': 'Inversas', '6': 'LU', '7': 'Propiedades'}[opcion]
            ultimo_resultado = menu_algebra(tema, ultimo_resultado)
