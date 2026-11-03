"""Presenta matrices alineadas y procedimientos de suma o resta.

Tema: notación matricial y operaciones elemento a elemento.
Elaboración: equipo del proyecto, con apoyo de IA.
"""


def mostrar_matriz(nombre, matriz):
    """Muestra una matriz rectangular con su nombre y dimensiones."""
    textos = [[str(numero) for numero in fila] for fila in matriz]
    anchos = [max(len(fila[j]) for fila in textos) for j in range(len(textos[0]))]
    print(f"\n{nombre} ({len(matriz)}x{len(matriz[0])})")
    for fila in textos:
        print("[ " + "  ".join(valor.rjust(ancho) for valor, ancho in zip(fila, anchos)) + " ]")


def mostrar_procedimiento(matriz_a, matriz_b, resultado, signo):
    """Muestra el cálculo de cada elemento usando las matrices ya calculadas."""
    print("\nProcedimiento: operamos los elementos en la misma posición.")
    for i in range(len(resultado)):
        for j in range(len(resultado[0])):
            print(
                f"R[{i + 1},{j + 1}] = ({matriz_a[i][j]}) "
                f"{signo} ({matriz_b[i][j]}) = {resultado[i][j]}"
            )
