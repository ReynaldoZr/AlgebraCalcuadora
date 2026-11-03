"""Contiene el resumen teórico de las operaciones implementadas.

Tema: suma y resta de matrices de igual dimensión.
Elaboración: equipo del proyecto, con apoyo de IA.
"""


def teoremas_matrices():
    """Devuelve texto con condiciones y propiedades de la suma y resta."""
    return (
        "\nTEOREMAS CLAVE: SUMA Y RESTA\n"
        "Condición: A y B deben tener las mismas filas y columnas.\n"
        "Suma: (A + B)[i,j] = A[i,j] + B[i,j].\n"
        "Resta: (A - B)[i,j] = A[i,j] - B[i,j].\n"
        "Conmutatividad de la suma: A + B = B + A.\n"
        "Asociatividad de la suma: (A + B) + C = A + (B + C).\n"
        "Neutro: A + 0 = A, con matriz cero del mismo tamaño.\n"
        "Inverso aditivo: A + (-A) = 0.\n"
        "La resta no es conmutativa en general: A - B puede diferir de B - A.\n"
        "Esta versión muestra las propiedades; su verificador se añadirá después."
    )
