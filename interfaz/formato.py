"""Presenta matrices alineadas y procedimientos de suma o resta.

Tema: notación matricial y operaciones elemento a elemento.
Elaboración: equipo del proyecto, con apoyo de IA.
"""


def formatear_matriz(matriz):
    """Devuelve una matriz rectangular como texto alineado para ambas interfaces."""
    textos = [[str(numero) for numero in fila] for fila in matriz]
    anchos = [max(len(fila[j]) for fila in textos) for j in range(len(textos[0]))]
    return "\n".join(
        "[ " + "  ".join(valor.rjust(ancho) for valor, ancho in zip(fila, anchos)) + " ]"
        for fila in textos
    )


def mostrar_matriz(nombre, matriz):
    """Muestra una matriz rectangular con su nombre y dimensiones."""
    print(f"\n{nombre} ({len(matriz)}x{len(matriz[0])})")
    print(formatear_matriz(matriz))


def formatear_procedimiento(matriz_a, matriz_b, resultado, signo):
    """Devuelve los pasos por posición usando resultados ya calculados."""
    pasos = ["Procedimiento: operamos los elementos en la misma posición."]
    for i in range(len(resultado)):
        for j in range(len(resultado[0])):
            pasos.append(
                f"R[{i + 1},{j + 1}] = ({matriz_a[i][j]}) "
                f"{signo} ({matriz_b[i][j]}) = {resultado[i][j]}"
            )
    return "\n".join(pasos)


def mostrar_procedimiento(matriz_a, matriz_b, resultado, signo):
    """Muestra los pasos compartidos por la consola y la ventana."""
    print("\n" + formatear_procedimiento(matriz_a, matriz_b, resultado, signo))
