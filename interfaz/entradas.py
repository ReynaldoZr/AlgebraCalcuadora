"""Lee datos y repite preguntas cuando la entrada es incorrecta.

Tema: dimensiones y componentes de matrices.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction


def leer_opcion(mensaje, opciones):
    """Lee una opción de texto y devuelve una de las opciones permitidas."""
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones:
            return opcion
        print("Opción inválida. Elige una de las opciones del menú.")


def leer_entero_positivo(mensaje):
    """Lee y devuelve un entero mayor que cero; reintenta ante datos inválidos."""
    while True:
        try:
            numero = int(input(mensaje).strip())
            if numero > 0:
                return numero
        except ValueError:
            pass
        print("Escribe un número entero mayor que cero.")


def leer_numero(mensaje):
    """Lee un entero, decimal con punto o fracción y devuelve un Fraction exacto."""
    while True:
        try:
            # Convertir el texto directamente evita introducir redondeo de float.
            return Fraction(input(mensaje).strip())
        except (ValueError, ZeroDivisionError):
            print("Número inválido. Usa 2, -3, 0.5 o 1/3; el denominador no puede ser 0.")


def leer_matriz(nombre):
    """Pide dimensiones y elementos de una matriz; devuelve una lista de filas."""
    print(f"\nMatriz {nombre}")
    filas = leer_entero_positivo("Número de filas: ")
    columnas = leer_entero_positivo("Número de columnas: ")
    matriz = []
    for i in range(filas):
        print(f"Fila {i + 1}:")
        fila = []
        for j in range(columnas):
            fila.append(leer_numero(f"  {nombre}[{i + 1},{j + 1}]: "))
        matriz.append(fila)
    return matriz


def elegir_matriz(nombre, ultimo_resultado):
    """Lee una matriz nueva o devuelve una copia del resultado anterior."""
    if ultimo_resultado is not None:
        print(f"\nMatriz {nombre}: 1. Ingresar nueva / 2. Usar último resultado")
        opcion = leer_opcion("Elige: ", ("1", "2"))
        if opcion == "2":
            return [fila[:] for fila in ultimo_resultado]
    return leer_matriz(nombre)
