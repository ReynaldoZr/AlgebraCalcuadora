"""Adapta los catálogos existentes a formularios de Qt Quick.

Tema: metadatos de pantallas y reutilización de cálculos, sin widgets Tk.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.datos import convertir_numero
from interfaz.explicacion import construir_etapas, etapas_completas
from interfaz.metodos_numericos import (
    CAMPOS, METODOS_NUMERICOS, ejecutar_numerico, resumen_numerico,
)
from interfaz.operaciones import Operacion, OPERACIONES, Presentacion, calcular_operacion
from modulos.modulo_matrices import (
    multiplicar_por_escalar, producto_matricial, restar_matrices,
    sumar_matrices, transponer_matriz,
)
from modulos.procedimientos import Calculo, Paso


MATRICES = {
    'sumar': Operacion('Matrices', 'Suma · A + B', ('A', 'B'), 'A y B deben tener el mismo tamaño.'),
    'restar': Operacion('Matrices', 'Resta · A − B', ('A', 'B'), 'Restamos elementos de la misma posición.'),
    'escalar': Operacion('Matrices', 'Escalar · kA', ('A',), 'Multiplicamos cada elemento por el escalar k.', True),
    'multiplicar': Operacion('Matrices', 'Producto · AB', ('A', 'B'), 'Columnas de A = filas de B.'),
    'transponer': Operacion('Matrices', 'Transpuesta · Aᵀ', ('A',), 'Las filas pasan a columnas; se conservan los valores.'),
}
CATALOGO = {**MATRICES, **OPERACIONES}
TEMAS = (
    ('Matrices', '▦', 'Suma, resta, producto y transpuesta'),
    ('Sistemas', 'A│b', 'Gauss, Gauss-Jordan y solución general'),
    ('Vectores', '↗', 'Operaciones, combinación e independencia'),
    ('Determinantes', '|A|', 'Reducción, cofactores y Sarrus'),
    ('Inversas', 'A⁻¹', 'Gauss-Jordan y adjunta'),
    ('LU', 'L·U', 'Factorización y solución de sistemas'),
    ('Propiedades', '✓=', 'Comprobaciones con ambos miembros'),
    ('Numéricos', '≈ƒ', 'Bisección, errores y estabilidad'),
)
AYUDA_NUMERICA = {
    'num_biseccion': 'Intervalo: tolerancia en x. Porcentual: error relativo (%). El residuo controla |f(x)|. La función debe ser continua.',
    'num_errores': 'Se compara el valor aproximado con el verdadero. Con referencia cero, el relativo y el porcentual no están definidos.',
    'num_propagacion': 'Δx es la incertidumbre de entrada. Deja el paso vacío para elegirlo automáticamente.',
    'num_simulacion': 'La tasa se escribe en decimal: 0.005 equivale a 0.5 %. Consulta los errores de cada iteración.',
    'num_flotante': 'Esta demostración no necesita entradas. Pulsa Calcular para comparar precisión, overflow y underflow.',
    'num_inestabilidad': 'Comparamos √(x + 1) − √x con 1 / (√(x + 1) + √x). Usa x ≥ 0. Por ejemplo: 1e16 significa 10^16.',
    'num_bases': 'Elige base 2 o 10 y el número de cifras fraccionarias. Se conserva el resto exacto.',
    'num_inversa': 'A debe ser cuadrada e invertible. Comparamos Fraction, float propio y NumPy.',
    'num_sistema': 'A debe ser cuadrada e invertible; b debe tener una columna y tantas filas como A.',
}


def metodos_tema(tema):
    """Devuelve identificadores y etiquetas de métodos implementados."""
    if tema == 'Numéricos':
        return [{'clave': k, 'nombre': v.nombre} for k, v in METODOS_NUMERICOS.items()]
    return [{'clave': k, 'nombre': v.nombre} for k, v in CATALOGO.items() if v.tema == tema]


def tema_de(clave):
    """Resuelve el tema sin depender del texto visible del selector."""
    return 'Numéricos' if clave in METODOS_NUMERICOS else CATALOGO[clave].tema


def matrices_de(clave):
    """Identifica únicamente las matrices reales que pide el método."""
    return METODOS_NUMERICOS[clave].matrices if clave in METODOS_NUMERICOS else CATALOGO[clave].entradas


def campos_de(clave, columna):
    """Expone parámetros pertinentes; k es una entrada exacta, no flotante."""
    if clave in METODOS_NUMERICOS:
        metodo = METODOS_NUMERICOS[clave]
        return metodo.campos_a if columna == 0 else metodo.campos_b
    return ('escalar',) if columna == 1 and CATALOGO[clave].escalar else ()


def leer_matrices(entradas, nombres):
    """Convierte texto directamente a Fraction e identifica cualquier celda inválida."""
    matrices = {}
    for nombre in nombres:
        matriz = []
        for i, fila in enumerate(entradas[nombre]):
            valores = []
            for j, texto in enumerate(fila):
                try:
                    valores.append(convertir_numero(texto))
                except (ValueError, ZeroDivisionError):
                    raise ValueError(f'Revisa {nombre}[{i + 1},{j + 1}]: escribe un entero, decimal o fracción.') from None
            matriz.append(valores)
        matrices[nombre] = matriz
    return matrices


def calcular_matrices(clave, entradas, escalar):
    """Reutiliza los algoritmos y las etapas ya disponibles para matrices básicas."""
    a, b = entradas['A'], entradas.get('B')
    if clave == 'escalar':
        resultado, signo = multiplicar_por_escalar(a, escalar), '×'
    elif clave == 'transponer':
        resultado, signo = transponer_matriz(a), 'T'
    elif clave == 'multiplicar':
        resultado, signo = producto_matricial(a, b), 'AB'
    else:
        resultado = sumar_matrices(a, b) if clave == 'sumar' else restar_matrices(a, b)
        signo = '+' if clave == 'sumar' else '-'

    posiciones = []
    for i, fila in enumerate(resultado):
        for j, valor in enumerate(fila):
            if signo == 'AB':
                operandos = tuple(a[i]), tuple(f[j] for f in b)
            elif signo == 'T':
                operandos = a[j][i], None
            elif signo == '×':
                operandos = escalar, a[i][j]
            else:
                operandos = a[i][j], b[i][j]
            posiciones.append((i, j, *operandos, valor, signo))
    pasos = [Paso('Matriz ' + n, matriz=m) for n, m in entradas.items()]
    for posicion, paso in enumerate(posiciones):
        for etapa in etapas_completas(paso, posicion):
            pasos.append(Paso(f'R[{paso[0] + 1},{paso[1] + 1}] · {etapa.titulo}',
                              etapa.mensaje, formulas=(etapa.tokens,)))
    pasos.append(Paso('Resultado final', matriz=resultado))
    presentacion = Presentacion(Calculo(resultado, tuple(pasos)), 'Resultado exacto · ' + MATRICES[clave].nombre, resultado)
    return presentacion, tuple(construir_etapas(posiciones))


def ejecutar(clave, parametros, entradas):
    """Llama al mismo núcleo de consola y Tk, sin resolver matemáticas en QML."""
    matrices = leer_matrices(entradas, matrices_de(clave))
    if clave in METODOS_NUMERICOS:
        calculo = ejecutar_numerico(clave, parametros, matrices)
        presentacion = Presentacion(calculo, resumen_numerico(clave, calculo), None)
        return presentacion, calculo.pasos
    escalar = convertir_numero(parametros['escalar']) if CATALOGO[clave].escalar else 2
    if clave in MATRICES:
        return calcular_matrices(clave, matrices, escalar)
    presentacion = calcular_operacion(clave, matrices, escalar)
    return presentacion, presentacion.calculo.pasos
