"""Calcula bisección propia con tabla y contraste independiente de SciPy.

Tema: semana 12; intervalos, errores, residuo y motivos de terminación.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import math

from modulos.numericos.funciones import crear_funcion, formato, numero_finito
from modulos.procedimientos import Calculo, Paso



def biseccion(
    expresion, a, b, tolerancia=0.0001, max_iteraciones=200,
    criterio='intervalo', tolerancia_f=0.0001,
):
    """Devuelve raíz aproximada, todas las iteraciones y contraste SciPy.

    La tolerancia es absoluta en x para intervalo, o porcentual para criterio
    porcentual. También se exige el residuo independiente tolerancia_f.
    """
    # Validamos la función, el intervalo y las condiciones de parada todos los datos.
    funcion = crear_funcion(expresion)
    a, b = numero_finito(a, 'a'), numero_finito(b, 'b')
    tolerancia, tolerancia_f = (
        numero_finito(tolerancia, 'Tolerancia'),
        numero_finito(tolerancia_f, 'Tolerancia de residuo'),
    )

    if a >= b or not math.isfinite(b - a):
        raise ValueError(
            'El intervalo debe cumplir a < b y tener ancho finito.'
        )

    if tolerancia <= 0 or tolerancia_f <= 0:
        raise ValueError('Las tolerancias deben ser positivas.')

    if type(max_iteraciones) is not int or not 1 <= max_iteraciones <= 10000:
        raise ValueError('El máximo debe ser un entero entre 1 y 10000.')

    if criterio not in ('intervalo', 'porcentual'):
        raise ValueError('Criterio no reconocido.')

    # Revisamos los extremos antes de dividir el intervalo, 0 o negativo
    fa, fb = funcion(a), funcion(b)
    inicial_a, inicial_b = a, b
    predichas = (
        max(
            0,
            math.ceil((math.log(b - a) - math.log(tolerancia)) / math.log(2)),
        )
        if criterio == 'intervalo'
        else None
    )

    # Preparamos la tabla y el primer paso de la explicación.
    datos = dict(
        filas=[],
        columnas=(
            'i', 'xl', 'xu', 'xr', 'f(xl)', 'f(xu)', 'f(xr)',
            'Ea (%)', 'Cota en x',
        ),
        iteraciones_predichas=predichas, convergio=False,
        intervalo=(a, b), funcion=expresion, criterio=criterio,
        tolerancia=tolerancia, tolerancia_f=tolerancia_f,
    )
    pasos = [
        Paso(
            'Condiciones de bisección',
            f'f(x)={expresion}; intervalo [{a:g}, {b:g}]. '
            'La función debe ser continua en el intervalo.',
            formulas=((f'f(a)={formato(fa)}', f'f(b)={formato(fb)}'),),
        )
    ]

    if fa == 0 or fb == 0:
        raiz = a if fa == 0 else b
        datos.update(
            convergio=True, residuo=0.0,
            motivo='Raíz en un extremo',
            scipy=raiz, diferencia_scipy=0.0,
        )
        pasos.append(
            Paso(
                'Raíz en el extremo',
                formulas=((f'x={formato(raiz)}', 'f(x)=0'),),
            )
        )
        return Calculo(raiz, tuple(pasos), datos)

    if (fa > 0) == (fb > 0):
        raise ValueError(
            'No hay cambio de signo en los extremos; '
            'bisección no garantiza una raíz en este intervalo.'
        )

    anterior = None
    motivo = (
        'Se alcanzó el máximo de iteraciones sin cumplir ambas tolerancias.'
    )

    # Repetimos: evaluar funcion, error porcentual con el anterior.
    for i in range(1, max_iteraciones + 1):
        medio = a + (b - a) / 2
        fm = funcion(medio)
        error = (
            None if anterior is None or medio == 0
            else abs((medio - anterior) / medio) * 100
        )
        cota = (b - a) / 2
        datos['filas'].append((i, a, b, medio, fa, fb, fm, error, cota))


        # Elegimos la mitad que mantiene el cambio de signo.
        elige_izquierda = (fa > 0) != (fm > 0)
        decision = (
            'Conservamos [xl,xr].'
            if elige_izquierda
            else 'Conservamos [xr,xu].'
        )
        pasos.append(
            Paso(
                f'Iteración {i}', decision,
                formulas=(
                    (f'xr=({formato(a)}+{formato(b)})/2={formato(medio)}',),
                    (
                        f'f(xl)={formato(fa)}', f'f(xu)={formato(fb)}',
                        f'f(xr)={formato(fm)}',
                    ),
                    (
                        f'Ea={formato(error)} %', f'Cota={formato(cota)}',
                        f'|f(xr)|={formato(abs(fm))}',
                    ),
                ),
            )
        )

        # Pedimos precisión en x y un valor de la función cercano a cero
        cumple_x = (
            cota <= tolerancia
            if criterio == 'intervalo'
            else error is not None and error <= tolerancia
        )
        if fm == 0 or (cumple_x and abs(fm) <= tolerancia_f):
            datos['convergio'] = True
            motivo = (
                'Raíz exacta en punto medio.'
                if fm == 0
                else 'Se cumplen la tolerancia elegida y el residuo.'
            )
            break

        # Evitamos seguir si la precisión ya no permite reducir el intervalo.
        if medio == a or medio == b:
            motivo = (
                'La precisión de punto flotante impide reducir el intervalo; '
                'revisa tolerancias o continuidad.'
            )
            break

        # Actualizamos el intervalo y recordamos la aproximación anterior si hace falta
        if elige_izquierda:
            b, fb = medio, fm
        else:
            a, fa = medio, fm

        anterior = medio

    datos.update(motivo=motivo, residuo=abs(fm), cota=cota)

    # SciPy sirve de contraste; usa una tolerancia absoluta en x.
    from scipy.optimize import bisect

    try:
        referencia = float(
            bisect(
                funcion, inicial_a, inicial_b,
                xtol=max(5e-324, min(tolerancia, 1e-12)),
                maxiter=1100,
            )
        )
        diferencia = abs(medio - referencia)
    except (ValueError, RuntimeError) as error:
        referencia, diferencia = None, None
        datos['scipy_error'] = str(error)

    datos.update(scipy=referencia, diferencia_scipy=diferencia)

    # Entregamos resultado, pasos y tabla a la interfaz.
    pasos.append(
        Paso(
            'Terminación y contraste', motivo,
            formulas=(
                (f'Raíz={formato(medio)}', f'|f(x)|={formato(abs(fm))}'),
                (f'SciPy={formato(referencia)}',
                 f'Diferencia={formato(diferencia)}'),
            ),
        )
    )
    return Calculo(medio, tuple(pasos), datos)
