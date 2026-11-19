"""Evalúa polinomios y su derivada con Horner y comprueba deflación lineal.

Tema: Sesión 22, raíces de polinomios y preparación del Programa 9, issue 35.
Elaboración: equipo 9, con apoyo de IA.
"""

from modulos.numericos.funciones import formato, numero_finito
from modulos.procedimientos import Calculo, Paso


def _coeficientes(valores):
    """Copia coeficientes descendentes y normaliza solo los ceros iniciales."""
    if not isinstance(valores, (list, tuple)) or not valores:
        raise ValueError('Escribe una lista o tupla no vacía de coeficientes descendentes.')
    originales = tuple(numero_finito(v, 'Coeficiente') for v in valores)
    primero = 0
    while primero < len(originales) - 1 and originales[primero] == 0:
        primero += 1
    return originales, originales[primero:]


def _recorrer(coeficientes, x):
    """Obtiene p(x), p'(x) y acumulados con la recurrencia de Horner extendida."""
    valor, derivada = 0.0, 0.0
    filas = []
    for i, coeficiente in enumerate(coeficientes):
        # La derivada usa el acumulado anterior, antes de actualizar el valor.
        derivada = numero_finito(derivada * x + valor, 'Derivada por Horner')
        valor = numero_finito(valor * x + coeficiente, 'Valor por Horner')
        filas.append((i, coeficiente, valor, derivada))
    return valor, derivada, tuple(filas)


def evaluar_horner(coeficientes, x):
    """Devuelve Calculo con p(x), derivada, tabla y coeficientes sin mutar la entrada."""
    originales, normalizados = _coeficientes(coeficientes)
    punto = numero_finito(x, 'Punto x')
    valor, derivada, filas = _recorrer(normalizados, punto)
    pasos = [Paso(
        'Coeficientes de Horner',
        'Se escriben de mayor a menor grado, incluyendo cero para términos ausentes.',
        formulas=((f'Coeficientes={normalizados}', f'x={formato(punto)}'),),
    )]
    pasos.extend(Paso(
        f'Acumulado {i + 1}',
        'Multiplicamos el acumulado por x y sumamos el siguiente coeficiente.',
        formulas=((f'Coeficiente={formato(a)}', f'Acumulado={formato(b)}',
                   f'Acumulado de derivada={formato(c)}'),),
    ) for i, a, b, c in filas)
    pasos.append(Paso(
        'Resultado de Horner', 'Son valores numéricos aproximados, sin redondeo interno.',
        formulas=((f'p(x)={formato(valor)}', f"p'(x)={formato(derivada)}"),),
    ))
    return Calculo(valor, tuple(pasos), dict(
        coeficientes=normalizados, originales=originales, x=punto,
        grado=len(normalizados) - 1, derivada=derivada, filas=filas,
        columnas=('i', 'Coeficiente', 'Acumulado p', 'Acumulado derivada'),
        ceros_iniciales=len(originales) - len(normalizados),
    ))


def deflacionar_polinomio(coeficientes, raiz, tolerancia_resto=1e-8):
    """Devuelve cociente y resto de dividir por (x-raiz); no elimina restos grandes."""
    tolerancia = numero_finito(tolerancia_resto, 'Tolerancia del resto')
    if tolerancia <= 0:
        raise ValueError('La tolerancia del resto debe ser positiva.')
    calculo = evaluar_horner(coeficientes, raiz)
    d = calculo.datos
    if d['grado'] < 1:
        raise ValueError('Un polinomio constante no admite deflación lineal.')
    cociente = tuple(fila[2] for fila in d['filas'][:-1])
    resto = calculo.valor
    aceptada = abs(resto) < tolerancia
    aviso = (
        'El resto cumple la tolerancia; comprueba y refina la raíz con el polinomio original.'
        if aceptada else
        'El resto no cumple la tolerancia. No descartar este resto ni continuar como si fuera cero.'
    )
    paso = Paso(
        'Deflación por división sintética', aviso,
        formulas=((f'p(x)=(x−({formato(d["x"])}))·q(x)+({formato(resto)})',),
                  (f'Coeficientes de q={cociente}',
                   f'Tolerancia del resto={formato(tolerancia)}')),
    )
    return Calculo(cociente, calculo.pasos + (paso,), dict(
        coeficientes=d['coeficientes'], originales=d['originales'], raiz=d['x'],
        cociente=cociente, resto=resto, residuo=abs(resto), aceptada=aceptada,
        tolerancia_resto=tolerancia, motivo=aviso,
    ))


def crear_funciones_polinomio(coeficientes):
    """Crea p y su derivada como callables reales para Newton, con una copia estable."""
    _, copia = _coeficientes(coeficientes)

    def funcion(x):
        """Evalúa el polinomio mediante Horner sin generar pasos de presentación."""
        punto = numero_finito(x, 'Punto x')
        return _recorrer(copia, punto)[0]

    def derivada(x):
        """Evalúa la derivada extendida de Horner, sin diferencias finitas."""
        punto = numero_finito(x, 'Punto x')
        return _recorrer(copia, punto)[1]

    return funcion, derivada
