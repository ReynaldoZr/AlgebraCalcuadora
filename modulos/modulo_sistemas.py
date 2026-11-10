"""Resuelve Ax=b con Gauss o Gauss-Jordan y comprueba su solución general.

Tema: tareas 1 y 2; soluciones única, infinita e inconsistente.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction

from modulos.eliminacion import reducir
from modulos.modulo_matrices import producto_matricial
from modulos.procedimientos import Calculo, Paso
from modulos.validaciones import validar_matriz, validar_vector


def sustitucion(matriz, pivotes, variables, libre=None, homogeneo=False):
    """Resuelve desde abajo con libres cero o una libre unitaria; devuelve vector y pasos."""
    vector = [Fraction(0) for _ in range(variables)]
    if libre is not None:
        vector[libre] = Fraction(1)
    pasos = []
    for fila in range(len(pivotes) - 1, -1, -1):
        columna = pivotes[fila]
        termino = Fraction(0) if homogeneo else matriz[fila][-1]
        suma = sum(matriz[fila][j] * vector[j] for j in range(columna + 1, variables))
        valor = (termino - suma) / matriz[fila][columna]
        tokens = [f"x{columna + 1}", "=", "(", termino]
        for j in range(columna + 1, variables):
            if matriz[fila][j] != 0:
                tokens += ["−", "(", matriz[fila][j], "×", "(", vector[j], ")", ")"]
        tokens += [")", "÷", "(", matriz[fila][columna], ")", "=", valor]
        vector[columna] = valor
        pasos.append(Paso(f"Despejamos x{columna + 1}", "Sustituimos los valores ya conocidos.", formulas=(tuple(tokens),)))
    return vector, pasos


def resolver_sistema(matriz_a, vector_b, metodo="gauss"):
    """Devuelve Calculo(particular o None, pasos, clasificación/pivotes/libres/base/verificación).

    Las columnas pivote/libres son de base cero. Para infinitas soluciones:
    x = particular + t1*base[0] + ...; se comprueban A*particular=b y A*base[i]=0.
    """
    filas, variables = validar_matriz(matriz_a)
    validar_vector(vector_b, filas)
    if metodo not in ("gauss", "jordan"):
        raise ValueError("El método debe ser gauss o jordan.")
    aumentada = [fila[:] + [b] for fila, b in zip(matriz_a, vector_b)]
    reduccion = reducir(aumentada, reducida=metodo == "jordan", columnas_pivote=variables)
    escalonada = reduccion.matriz
    pasos = list(reduccion.pasos)
    libres = tuple(j for j in range(variables) if j not in reduccion.pivotes)
    datos = dict(matriz=escalonada, pivotes=reduccion.pivotes, libres=libres, base=[], verificado=None)
    for i, fila in enumerate(escalonada):
        if all(valor == 0 for valor in fila[:variables]) and fila[-1] != 0:
            pasos.append(Paso("Sistema inconsistente · Sin solución", f"La fila {i + 1} exige 0 = {fila[-1]}, una contradicción.", formulas=((0, "≠", fila[-1]),)))
            datos["clasificacion"] = "sin_solucion"
            return Calculo(None, tuple(pasos), datos)
    particular, desarrollo = sustitucion(escalonada, reduccion.pivotes, variables)
    pasos.append(Paso("Variables libres", ", ".join(f"x{j + 1} = t{k + 1}" for k, j in enumerate(libres)) if libres else "No hay variables libres."))
    pasos.extend(desarrollo)
    for k, libre in enumerate(libres):
        # Cada libre unitaria genera una dirección de la solución general de Ax=0.
        vector, desarrollo = sustitucion(escalonada, reduccion.pivotes, variables, libre, True)
        pasos.append(Paso(f"Dirección del parámetro t{k + 1}", f"Fijamos x{libre + 1}=1 y las otras libres en 0 para resolver Ax=0."))
        pasos.extend(desarrollo)
        datos["base"].append(vector)
    comprobacion = producto_matricial(matriz_a, [[v] for v in particular])
    datos["verificado"] = comprobacion == [[v] for v in vector_b] and all(
        producto_matricial(matriz_a, [[v] for v in direccion]) == [[0] for _ in range(filas)] for direccion in datos["base"])
    datos["clasificacion"] = "infinitas" if libres else "unica"
    pasos.append(Paso("Comprobación en el sistema original", "A·particular=b y cada dirección satisface A·v=0." if libres else "A·x=b, comprobado con las entradas originales.", comprobacion))
    return Calculo(particular, tuple(pasos), datos)
