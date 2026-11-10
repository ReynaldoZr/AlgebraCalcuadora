"""Describe etapas didácticas de operaciones ya calculadas, sin widgets.

Tema: origen, operación, simplificación y destino de cada elemento.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EtapaVisual:
    """Reúne el texto y la fórmula de una etapa de una celda del resultado."""

    paso: tuple
    posicion: int
    fase: str
    titulo: str
    operandos: str
    tokens: tuple
    mensaje: str
    par: int | None = None


def maximo_divisor(a, b):
    """Obtiene un divisor común para explicar simplificaciones, usando Euclides."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def operandos_de_paso(paso):
    """Etiqueta los valores con su escalar o coordenada de origen."""
    fila, columna, a, b, _, signo = paso
    coordenada = f"[{fila + 1},{columna + 1}]"
    if signo == "AB":
        return f"Fila {fila + 1} de A · {len(a)} elementos\nColumna {columna + 1} de B · {len(b)} elementos"
    if signo == "T":
        return f"Origen A[{columna + 1},{fila + 1}] = {a}\nDestino R{coordenada}"
    if signo == "×":
        return f"Escalar k = {a}\nElemento A{coordenada} = {b}"
    return f"Elemento A{coordenada} = {a}\nElemento B{coordenada} = {b}"


def operandos_agrupados(a, b, signo):
    """Agrupa el operando derecho negativo para distinguir claramente los signos."""
    return [a, signo] + (["(", b, ")"] if b < 0 else [b])


def fraccion_intermedia(paso):
    """Devuelve numeradores equivalentes y denominador para explicar la operación."""
    _, _, a, b, _, signo = paso
    if signo == "×":
        return a.numerator, b.numerator, a.denominator * b.denominator
    comun = a.denominator * b.denominator // maximo_divisor(a.denominator, b.denominator)
    return a.numerator * (comun // a.denominator), b.numerator * (comun // b.denominator), comun


def operacion_de_paso(paso):
    """Expone equivalencias de fracciones sin sustituir la respuesta del núcleo."""
    _, _, a, b, resultado, signo = paso
    n1, n2, denominador = fraccion_intermedia(paso)
    if signo == "×":
        numerador = n1 * n2
        if a.denominator == b.denominator == 1:
            tokens = operandos_agrupados(a, b, signo) + ["=", resultado]
        else:
            texto_a = f"({n1})" if n1 < 0 else str(n1)
            texto_b = f"({n2})" if n2 < 0 else str(n2)
            tokens = [(f"{texto_a} × {texto_b}", f"{a.denominator} × {b.denominator}"),
                      "=", (numerador, denominador)]
        mensaje = "Multiplicamos numeradores y denominadores." if denominador != 1 else "Multiplicamos los enteros."
    else:
        numerador = n1 + n2 if signo == "+" else n1 - n2
        if denominador == 1:
            tokens = operandos_agrupados(a, b, signo) + ["=", resultado]
        else:
            derecha = ["(", (n2, denominador), ")"] if n2 < 0 else [(n2, denominador)]
            tokens = [(n1, denominador), signo] + derecha + ["=", (numerador, denominador)]
        verbo = "sumamos" if signo == "+" else "restamos"
        mensaje = f"Usamos denominador {denominador} y {verbo} los numeradores." if denominador != 1 else f"Operamos los enteros: {verbo}."
    return tokens, mensaje, numerador, denominador


def etapas_de_paso(paso, posicion):
    """Produce etapas legibles; el resultado solo se revela al guardarlo."""
    fila, columna, a, b, resultado, signo = paso
    if signo == "AB":
        return etapas_producto(paso, posicion)
    if signo == "T":
        return etapas_transpuesta(paso, posicion)
    destino = f"R[{fila + 1},{columna + 1}]"
    operandos = operandos_de_paso(paso)
    etapas = [EtapaVisual(paso, posicion, "identificar", "Identificamos los operandos", operandos,
                         tuple(operandos_agrupados(a, b, signo)), f"Tomamos estos valores para calcular {destino}.")]
    tokens, mensaje, numerador, denominador = operacion_de_paso(paso)
    etapas.append(EtapaVisual(paso, posicion, "operar", "Realizamos la operación", operandos,
                             tuple(tokens), mensaje))
    if (numerador, denominador) != (resultado.numerator, resultado.denominator):
        divisor = maximo_divisor(numerador, denominador)
        etapas.append(EtapaVisual(paso, posicion, "simplificar", "Simplificamos", operandos,
                                 ((numerador, denominador), "=", resultado),
                                 f"Dividimos numerador y denominador entre {divisor}."))
    etapas.append(EtapaVisual(paso, posicion, "guardar", "Guardamos el resultado", operandos,
                             (destino, "=", resultado), f"Guardamos {resultado} en {destino}."))
    return etapas


def etapas_transpuesta(paso, posicion):
    """Explica el traslado A[j,i] a R[i,j], sin operar sobre el valor."""
    fila, columna, valor, _, resultado, _ = paso
    origen = f"A[{columna + 1},{fila + 1}]"
    destino = f"R[{fila + 1},{columna + 1}]"
    operandos = operandos_de_paso(paso)
    return [
        EtapaVisual(paso, posicion, "identificar", "Identificamos el origen", operandos,
                    (origen, "=", valor), f"Tomamos el valor de {origen}."),
        EtapaVisual(paso, posicion, "ubicar", "Intercambiamos fila y columna", operandos,
                    (origen, "→", destino),
                    f"La fila {columna + 1} pasa a columna {columna + 1}; la columna {fila + 1} pasa a fila {fila + 1}."),
        EtapaVisual(paso, posicion, "guardar", "Guardamos el mismo valor", operandos,
                    (destino, "=", resultado), f"Colocamos {resultado} en {destino}, sin cambiarlo."),
    ]


def construir_etapas(pasos):
    """Aplana las etapas por celda para reproducirlas en orden de lectura."""
    return tuple(etapa for posicion, paso in enumerate(pasos) for etapa in etapas_de_paso(paso, posicion))


def terminos_producto(paso):
    """Forma la suma de pares de una fila y una columna, agrupando los signos."""
    fila, columna, valores_a, valores_b, resultado, _ = paso
    tokens = []
    for a, b in zip(valores_a, valores_b):
        if tokens:
            tokens.append("+")
        tokens += ["("] + operandos_agrupados(a, b, "×") + [")"]
    return tokens + ["=", resultado]


def etapas_completas(paso, posicion):
    """Amplía solo el desarrollo escrito con la suma exacta de productos fraccionarios."""
    etapas = etapas_de_paso(paso, posicion)
    if paso[-1] != "AB":
        return etapas
    productos = [a * b for a, b in zip(paso[2], paso[3])]
    comun = 1
    for producto in productos:
        comun = comun * producto.denominator // maximo_divisor(comun, producto.denominator)
    if comun == 1:
        return etapas
    numeradores = [p.numerator * (comun // p.denominator) for p in productos]
    equivalentes, suma = [], []
    for numerador in numeradores:
        if equivalentes:
            equivalentes.append("+")
        equivalentes += ["(", (numerador, comun), ")"] if numerador < 0 else [(numerador, comun)]
        suma.append(f"({numerador})" if numerador < 0 else str(numerador))
    numerador = sum(numeradores)
    base = etapas[-2]
    detalle = [EtapaVisual(paso, posicion, "denominador", "Usamos denominador común", base.operandos,
                          tuple(equivalentes + ["=", (" + ".join(suma), comun), "=", (numerador, comun)]),
                          f"Expresamos todos los productos con denominador {comun}.")]
    resultado = paso[4]
    if (numerador, comun) != (resultado.numerator, resultado.denominator):
        divisor = maximo_divisor(numerador, comun)
        detalle.append(EtapaVisual(paso, posicion, "simplificar", "Simplificamos la suma", base.operandos,
                                  ((numerador, comun), "=", resultado),
                                  f"Dividimos numerador y denominador entre {divisor}."))
    suma_inicial = EtapaVisual(paso, posicion, base.fase, base.titulo, base.operandos,
                              base.tokens[:-2], base.mensaje)
    return etapas[:-2] + [suma_inicial] + detalle + etapas[-1:]


def etapas_producto(paso, posicion):
    """Presenta cada par, la suma de productos y el guardado de R[i,j]."""
    fila, columna, valores_a, valores_b, resultado, _ = paso
    destino = f"R[{fila + 1},{columna + 1}]"
    origenes = operandos_de_paso(paso)
    etapas = [EtapaVisual(paso, posicion, "identificar", "Elegimos fila y columna", origenes,
                         (f"Fila {fila + 1} de A", "·", f"Columna {columna + 1} de B"),
                         f"Emparejamos {len(valores_a)} elementos para calcular {destino}.")]
    productos = []
    for k, (a, b) in enumerate(zip(valores_a, valores_b)):
        producto = a * b
        productos.append(producto)
        operandos = f"A[{fila + 1},{k + 1}] = {a}\nB[{k + 1},{columna + 1}] = {b}"
        tokens, mensaje, numerador, denominador = operacion_de_paso((fila, columna, a, b, producto, "×"))
        bruto = str(numerador) if denominador == 1 else f"{numerador}/{denominador}"
        etapas.append(EtapaVisual(paso, posicion, "multiplicar", f"Multiplicamos el par {k + 1} de {len(valores_a)}",
                                 operandos, tuple(tokens), f"A[{fila + 1},{k + 1}] × B[{k + 1},{columna + 1}] = {bruto}.", k))
        if (numerador, denominador) != (producto.numerator, producto.denominator):
            divisor = maximo_divisor(numerador, denominador)
            etapas.append(EtapaVisual(paso, posicion, "simplificar", "Simplificamos este producto", operandos,
                                     ((numerador, denominador), "=", producto), f"Dividimos ambos entre {divisor}.", k))
    suma = []
    for producto in productos:
        if suma:
            suma.append("+")
        suma += ["(", producto, ")"] if producto < 0 else [producto]
    etapas.append(EtapaVisual(paso, posicion, "sumar", "Sumamos los productos", origenes,
                             tuple(suma + ["=", resultado]), f"La suma de estos {len(productos)} productos forma {destino}."))
    etapas.append(EtapaVisual(paso, posicion, "guardar", "Guardamos el resultado", origenes,
                             (destino, "=", resultado), f"Guardamos {resultado} en {destino}."))
    return etapas
