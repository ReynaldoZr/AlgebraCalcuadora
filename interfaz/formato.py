"""Presenta matrices alineadas y procedimientos de operaciones implementadas.

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


def formatear_procedimiento_escalar(matriz, escalar, resultado):
    """Explica kA por posición utilizando el resultado que devuelve el núcleo."""
    pasos = [f"Procedimiento: multiplicamos cada elemento de A por k = {escalar}."]
    for i, fila in enumerate(resultado):
        for j, valor in enumerate(fila):
            pasos.append(f"R[{i + 1},{j + 1}] = ({escalar}) × ({matriz[i][j]}) = {valor}")
    return "\n".join(pasos)


def formatear_procedimiento_transpuesta(matriz, resultado):
    """Relaciona cada posición de A con su destino en la transpuesta calculada."""
    pasos = [f"Procedimiento: A es {len(matriz)}x{len(matriz[0])}; Aᵀ es {len(resultado)}x{len(resultado[0])}."]
    for i, fila in enumerate(resultado):
        for j, valor in enumerate(fila):
            pasos.append(f"A[{j + 1},{i + 1}] = {matriz[j][i]} → R[{i + 1},{j + 1}] = {valor}")
    return "\n".join(pasos)


def formatear_procedimiento_producto(matriz_a, matriz_b, resultado):
    """Expone los pares de cada fila/columna usando el resultado calculado."""
    pasos = ["Procedimiento: cada entrada de AB es la suma de los productos de una fila de A por una columna de B."]
    for i, fila in enumerate(resultado):
        for j, valor in enumerate(fila):
            terminos = [f"({matriz_a[i][k]}) × ({matriz_b[k][j]})" for k in range(len(matriz_b))]
            pasos.append(f"R[{i + 1},{j + 1}] = " + " + ".join(terminos) + f" = {valor}")
    return "\n".join(pasos)
