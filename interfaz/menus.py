"""Coordina los menús y conecta datos, cálculos y resultados.

Tema: módulo de matrices y consulta de teoremas.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.cabeceras import mostrar_inicio, mostrar_matrices
from interfaz.entradas import elegir_matriz, leer_opcion
from interfaz.formato import mostrar_matriz, mostrar_procedimiento
from modulos.modulo_matrices import restar_matrices, sumar_matrices
from teoremas.resumen_teoremas import teoremas_matrices


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


def menu_matrices(ultimo_resultado):
    """Ejecuta las opciones de matrices y devuelve el último resultado de la sesión."""
    while True:
        mostrar_matrices()
        print("1. Sumar matrices\n2. Restar matrices\n3. Ver último resultado")
        print("0. Ver Teoremas Clave del Módulo\n9. Volver al menú principal")
        opcion = leer_opcion("Elige: ", ("0", "1", "2", "3", "9"))
        if opcion == "9":
            return ultimo_resultado
        if opcion == "0":
            print(teoremas_matrices())
        elif opcion == "3":
            if ultimo_resultado is None:
                print("Todavía no hay un resultado en esta sesión.")
            else:
                mostrar_matriz("Último resultado", ultimo_resultado)
        else:
            ultimo_resultado = ejecutar_operacion(opcion, ultimo_resultado)


def menu_principal(version):
    """Abre los temas disponibles y conserva el resultado mientras la app está abierta."""
    mostrar_inicio(version)
    ultimo_resultado = None
    while True:
        print("\nMENU PRINCIPAL\n1. Álgebra de matrices")
        print("0. Ver teoremas disponibles\n9. Salir")
        opcion = leer_opcion("Elige: ", ("0", "1", "9"))
        if opcion == "9":
            print("Hasta pronto.")
            return
        if opcion == "0":
            print(teoremas_matrices())
        else:
            ultimo_resultado = menu_matrices(ultimo_resultado)
