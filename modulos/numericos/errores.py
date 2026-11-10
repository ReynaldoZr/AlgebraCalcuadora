"""Calcula errores y experimentos de precisión de la semana 12.

Tema: propagación, redondeo, truncamiento, representación e inestabilidad.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from decimal import Decimal, InvalidOperation, ROUND_DOWN, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
import math

from modulos.numericos.funciones import crear_funcion, formato, numero_finito, valor_exacto
from modulos.procedimientos import Calculo, Paso


def calcular_errores(verdadero, aproximado):
    """Devuelve errores absoluto, relativo y porcentual; relativo no definido si verdadero=0."""
    verdadero, aproximado = numero_finito(verdadero), numero_finito(aproximado)
    absoluto = numero_finito(abs(verdadero - aproximado), 'Error absoluto')
    relativo = absoluto / abs(verdadero) if verdadero != 0 else None
    datos = dict(absoluto=absoluto, relativo=relativo, porcentual=relativo * 100 if relativo is not None else None)
    pasos = (Paso('Error absoluto', formulas=((f'|{formato(verdadero)} − {formato(aproximado)}| = {formato(absoluto)}',),)),
             Paso('Error relativo y porcentual', 'No definidos porque el valor verdadero es cero.' if relativo is None else '',
                  formulas=((f'Er=Ea/|verdadero|={formato(relativo)}', f'Er(%)={formato(datos["porcentual"])}'),)))
    return Calculo(datos, pasos, datos)


def propagacion(expresion, x, delta, paso_derivada=None):
    """Estima Δy por derivada central y lo compara con f(x+Δx)−f(x)."""
    funcion = crear_funcion(expresion)
    original_x, original_delta = str(x), str(delta)
    x, delta = numero_finito(x, 'x'), numero_finito(delta, 'Δx')
    if delta < 0:
        raise ValueError('La incertidumbre Δx no puede ser negativa.')
    h = math.ulp(1.0) ** (1 / 3) * max(1, abs(x)) if paso_derivada is None else numero_finito(paso_derivada, 'h')
    if h <= 0 or x + h == x or x - h == x:
        raise ValueError('El paso h debe ser positivo y distinguible de x en punto flotante.')
    superior, inferior = funcion(x + h), funcion(x - h)
    derivada = numero_finito((superior - inferior) / (2 * h), 'Derivada')
    estimacion = numero_finito(derivada * delta, 'Δy estimado')
    cambio = numero_finito(funcion(x + delta) - funcion(x), 'Cambio evaluado')
    exacto_inicial = valor_exacto(expresion, original_x)
    exacto_final = valor_exacto(expresion, Fraction(original_x) + Fraction(original_delta))
    cambio_exacto = exacto_final - exacto_inicial if exacto_inicial is not None and exacto_final is not None else None
    datos = dict(derivada=derivada, h=h, estimacion=estimacion, cambio=cambio, error=abs(estimacion - cambio),
                 funcion=expresion, x=x, delta=delta, cambio_exacto=str(cambio_exacto) if cambio_exacto is not None else None)
    pasos = (Paso('Derivada numérica central', formulas=((f"f'(x)≈[f(x+h)−f(x−h)]/(2h)={formato(derivada)}", f'h={formato(h)}'),)),
             Paso('Propagación lineal', formulas=((f'Δy≈f\'(x)·Δx={formato(estimacion)}',),)),
             Paso('Cambio evaluado directamente', 'El cambio de referencia también se evalúa en punto flotante; no es una igualdad simbólica.',
                  formulas=((f'f(x+Δx)−f(x)={formato(cambio)}', f'Diferencia={formato(datos["error"])}'),)))
    if cambio_exacto is not None:
        datos['error_exacto'] = float(abs(Fraction.from_float(estimacion) - cambio_exacto))
        pasos += (Paso('Referencia racional exacta', 'En este polinomio usamos las entradas decimales originales como fracciones.',
                       formulas=((f'Δy exacto={cambio_exacto}', f'Error de la estimación={formato(datos["error_exacto"])}'),)),)
    return Calculo(estimacion, pasos, datos)


def simulacion(capital=1000, tasa=0.005, iteraciones=50, decimales=2):
    """Compara interés compuesto con redondeo/truncamiento en cada iteración."""
    capital, tasa = numero_finito(capital), numero_finito(tasa)
    if type(iteraciones) is not int or not 1 <= iteraciones <= 500 or type(decimales) is not int or not 0 <= decimales <= 12:
        raise ValueError('Usa de 1 a 500 iteraciones y de 0 a 12 decimales.')
    if abs(capital) > 1e20 or abs(tasa) > 1 or tasa <= -1:
        raise ValueError('Usa |capital|≤10^20 y una tasa mayor que −1 y como máximo 1 en valor absoluto.')
    filas, pasos = [], []
    with localcontext() as contexto:
        contexto.prec = 100
        referencia = redondeado = truncado = Decimal(str(capital))
        factor, unidad = 1 + Decimal(str(tasa)), Decimal(1).scaleb(-decimales)
        try:
            for i in range(1, iteraciones + 1):
                referencia *= factor
                redondeado = (redondeado * factor).quantize(unidad, rounding=ROUND_HALF_EVEN)
                truncado = (truncado * factor).quantize(unidad, rounding=ROUND_DOWN)
                fila = (i, float(referencia), float(redondeado), float(truncado), float(abs(redondeado - referencia)), float(abs(truncado - referencia)))
                if not all(math.isfinite(v) for v in fila):
                    raise ValueError('La simulación supera el rango de representación; reduce tasa o iteraciones.')
                filas.append(fila)
                pasos.append(Paso(f'Iteración {i}', 'Redondeo: mitad al par. Truncamiento: hacia cero.', formulas=(
                    (f'Referencia={referencia}',), (f'Redondeado={redondeado}', f'Truncado={truncado}'),
                    (f'Error redondeo={formato(fila[4])}', f'Error truncamiento={formato(fila[5])}'))))
        except InvalidOperation:
            raise ValueError('Se agotó la precisión de la simulación; reduce los parámetros.') from None
    return Calculo(filas[-1][1], tuple(pasos), dict(filas=filas, columnas=('i', 'Referencia', 'Redondeado', 'Truncado', 'Error redondeo', 'Error truncamiento'),
                   referencia=str(referencia), redondeado=str(redondeado), truncado=str(truncado)))


def punto_flotante():
    """Demuestra épsilon, overflow, underflow y suma decimal usando NumPy solo en esta unidad."""
    import numpy as np
    with np.errstate(over='ignore', under='ignore'):
        desbordamiento = np.float32(np.finfo(np.float32).max) * np.float32(2)
        subdesbordamiento = np.float32(np.finfo(np.float32).tiny) * np.float32(1e-20)
    filas = [('0.1 + 0.2 (float)', repr(0.1 + 0.2)), ('1/10 + 1/5 (Fraction)', str(Fraction(1, 10) + Fraction(1, 5))),
             ('Épsilon float64', str(np.finfo(np.float64).eps)), ('Épsilon float32', str(np.finfo(np.float32).eps)),
             ('Overflow float32', str(desbordamiento)), ('Underflow float32', str(subdesbordamiento))]
    pasos = tuple(Paso(nombre, 'Overflow/underflow se provocan deliberadamente como demostración.', formulas=((valor,),)) for nombre, valor in filas)
    return Calculo(None, pasos, dict(filas=filas, columnas=('Experimento', 'Valor')))


def inestabilidad(x=1e16):
    """Compara sqrt(x+1)−sqrt(x) con su forma racionalizada y referencia Decimal."""
    x = numero_finito(x, 'x')
    if x < 0:
        raise ValueError('Para este ejemplo x debe ser no negativo.')
    directo = math.sqrt(x + 1) - math.sqrt(x)
    estable = 1 / (math.sqrt(x + 1) + math.sqrt(x))
    with localcontext() as contexto:
        contexto.prec = 100
        decimal = Decimal(str(x))
        referencia = 1 / ((decimal + 1).sqrt() + decimal.sqrt())
        error_directo = float(abs(Decimal.from_float(directo) - referencia))
        error_estable = float(abs(Decimal.from_float(estable) - referencia))
    pasos = (Paso('Expresión directa', 'Restar cantidades casi iguales puede perder cifras significativas.', formulas=((f'sqrt(x+1)−sqrt(x)={formato(directo)}',),)),
             Paso('Expresión racionalizada', formulas=((f'1/(sqrt(x+1)+sqrt(x))={formato(estable)}',),)),
             Paso('Referencia de alta precisión', formulas=((str(referencia),), (f'Error directo={formato(error_directo)}', f'Error reformulado={formato(error_estable)}'))))
    return Calculo(estable, pasos, dict(directo=directo, estable=estable, referencia=str(referencia), error_directo=error_directo, error_estable=error_estable))


def descomponer(texto='0.1', base=2, cifras=16):
    """Descompone un decimal exacto en base 2 o 10 y conserva el resto no representado."""
    numero_finito(texto)
    if type(base) is not int or base not in (2, 10) or type(cifras) is not int or not 1 <= cifras <= 40:
        raise ValueError('Elige base 2 o 10 y de 1 a 40 cifras fraccionarias.')
    valor = Fraction(str(texto))
    signo, valor_abs = '-' if valor < 0 else '', abs(valor)
    entero = valor_abs.numerator // valor_abs.denominator
    resto = valor_abs - entero
    digitos = []
    while entero:
        digitos.insert(0, entero % base)
        entero //= base
    digitos = digitos or [0]
    pasos = []
    for i, digito in enumerate(digitos):
        potencia = len(digitos) - i - 1
        pasos.append(Paso(f'Cifra entera {i + 1}', formulas=((f'{digito} × {base}^{potencia} = {digito * base ** potencia}',),)))
    fraccionarios = []
    for i in range(1, cifras + 1):
        if resto == 0:
            break
        resto *= base
        digito = resto.numerator // resto.denominator
        resto -= digito
        fraccionarios.append(digito)
        pasos.append(Paso(f'Cifra fraccionaria {i}', formulas=((f'{digito} × {base}^(-{i}) = {Fraction(digito, base ** i)}',),)))
    representacion = signo + ''.join(str(d) for d in digitos) + ('.' + ''.join(str(d) for d in fraccionarios) if fraccionarios else '')
    error = resto / base ** len(fraccionarios)
    pasos.append(Paso('Reconstrucción y resto', 'El resto no nulo indica que la expansión mostrada se truncó.', formulas=((f'Base {base}: {representacion}', f'Error absoluto exacto={error}'),)))
    return Calculo(representacion, tuple(pasos), dict(base=base, resto=str(error), original=str(valor)))
