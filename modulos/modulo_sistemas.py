"""Resuelve Ax=b con Gauss o Gauss-Jordan y comprueba su solución general.

Tema: tareas 1 y 2; soluciones única, infinita e inconsistente.
Equipo responsable: Grupo 9.
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


def resolver_cramer(matriz, vector_b):
    """Resuelve un sistema cuadrado con determinantes y verifica Ax=b."""
    from fractions import Fraction
    from modulos.modulo_determinantes import calcular_determinante

    n, m = validar_matriz(matriz)
    validar_vector(vector_b, n)
    if n != m:
        raise ValueError("Cramer requiere una matriz cuadrada.")
    principal = calcular_determinante(matriz).valor
    pasos = [Paso("Determinante de A", f"det(A) = {principal}", matriz=matriz)]
    if principal == 0:
        raise ValueError("Cramer no aplica: det(A) = 0. Usa Gauss-Jordan para clasificar el sistema.")
    solucion, determinantes = [], []
    for j in range(n):
        reemplazo = [fila[:j] + [b] + fila[j + 1:] for fila, b in zip(matriz, vector_b)]
        det = calcular_determinante(reemplazo).valor
        valor = Fraction(det) / Fraction(principal)
        solucion.append(valor)
        determinantes.append(det)
        pasos.append(Paso(f"Sustituimos la columna {j + 1} por b", matriz=reemplazo))
        pasos.append(Paso(f"Calculamos x{j + 1}", formulas=((det, "÷", principal, "=", valor),)))
    producto = producto_matricial(matriz, [[v] for v in solucion])
    verificado = producto == [[v] for v in vector_b]
    pasos.append(Paso("Comprobación Ax = b", "Se cumple" if verificado else "No se cumple", producto))
    return Calculo(solucion, tuple(pasos), dict(verificado=verificado, det=principal, determinantes=determinantes))


def analizar_forma(matriz):
    '''Clasifica la entrada y calcula su forma reducida con aritmética exacta.'''
    validar_matriz(matriz)
    lideres = [next((j for j, v in enumerate(fila) if v != 0), None) for fila in matriz]
    posiciones = [(i, j) for i, j in enumerate(lideres) if j is not None]
    filas_nulas_abajo = all(i == k for k, (i, _) in enumerate(posiciones))
    orden = all(a[1] < b[1] for a, b in zip(posiciones, posiciones[1:]))
    escalonada = filas_nulas_abajo and orden
    unitaria = all(matriz[i][j] == 1 for i, j in posiciones)
    columnas_limpias = all(all(k == i or fila[j] == 0 for k, fila in enumerate(matriz))
                           for i, j in posiciones)
    reducida = escalonada and unitaria and columnas_limpias
    razones = []
    if not filas_nulas_abajo:
        razones.append('Hay una fila no nula después de una fila nula.')
    if not orden:
        razones.append('Los pivotes no avanzan hacia la derecha.')
    if escalonada and not unitaria:
        razones.append('Algún pivote no es 1.')
    if escalonada and not columnas_limpias:
        razones.append('Alguna columna pivote tiene otras entradas no nulas.')
    nombre = 'Escalonada reducida' if reducida else 'Solo escalonada' if escalonada else 'No escalonada'
    final = reducir(matriz, reducida=True)
    # Las columnas pivote se indican también sobre las posiciones correspondientes en A.
    pivotes = ', '.join(f'({i + 1}, {j + 1})' for i, j in enumerate(final.pivotes)) or 'ninguno'
    razones = ' '.join(razones) or 'La entrada cumple las condiciones de forma escalonada reducida.'
    pasos = (Paso(nombre, razones, matriz=matriz), *final.pasos,
             Paso('Forma escalonada reducida', f'Posiciones pivote: {pivotes}', matriz=final.matriz))
    return Calculo(final.matriz, pasos, dict(forma=nombre, razones=razones,
                   pivotes=final.pivotes, posiciones=pivotes))
