"""Calcula Newton-Raphson propio y conserva su historial y causa de parada.

Tema: preparación provisional del Programa 9, Sesión 22, issue 33.
Equipo responsable: Grupo 9.
"""

import math

from modulos.numericos.funciones import formato, numero_finito
from modulos.procedimientos import Calculo, Paso

COLUMNAS_NEWTON = (
    'i', 'xi', 'f(xi)', 'derivada', 'x_siguiente',
    'error_absoluto', 'error_porcentual', 'residuo',
)


def _validar(funcion, derivada, x0, tolerancia, maximo, criterio, tolerancia_f):
    """Valida el contrato de entrada, sin evaluar todavía la función del ejercicio."""
    if not callable(funcion) or not callable(derivada):
        raise ValueError('La función y su derivada deben ser evaluables.')
    x = numero_finito(x0, 'Valor inicial x₀')
    tol = numero_finito(tolerancia, 'Tolerancia del cambio')
    tol_f = numero_finito(tolerancia_f, 'Tolerancia del residuo')
    if tol <= 0 or tol_f <= 0:
        raise ValueError('Las dos tolerancias deben ser positivas.')
    if type(maximo) is not int or not 1 <= maximo <= 10000:
        raise ValueError('El máximo de iteraciones debe ser un entero entre 1 y 10000.')
    if criterio not in ('absoluto', 'porcentual'):
        raise ValueError('El criterio debe ser absoluto o porcentual.')
    return x, tol, tol_f


def _avance(funcion, derivada, x, fx):
    """Calcula un paso y comprueba las evaluaciones antes de aceptar el punto nuevo."""
    pendiente = numero_finito(derivada(x), 'Derivada')
    if pendiente == 0:
        raise ValueError('La derivada es cero: no se puede dividir para avanzar.')
    # Una derivada pequeña no se rechaza por un umbral arbitrario: importa el cociente.
    correccion = numero_finito(fx / pendiente, 'Cociente f(x)/derivada')
    nuevo = numero_finito(x - correccion, 'Siguiente aproximación')
    cambio = numero_finito(abs(nuevo - x), 'Cambio absoluto')
    fnuevo = numero_finito(funcion(nuevo), 'Función en la siguiente aproximación')
    porcentual = abs((nuevo - x) / nuevo) * 100 if nuevo != 0 else None
    if porcentual is not None and not math.isfinite(porcentual):
        porcentual = None
    return pendiente, nuevo, cambio, fnuevo, porcentual


def _paso_explicado(k, x, fx, pendiente, nuevo, cambio, porcentual, residuo):
    """Expone la sustitución numérica y las magnitudes sin redondear el cálculo."""
    return Paso(
        f'Iteración {k} de Newton',
        'Evaluamos función y derivada, avanzamos con la tangente y comprobamos el punto nuevo.',
        formulas=(
            (f'x{k - 1}={formato(x)}', f'f(x{k - 1})={formato(fx)}',
             f"f'(x{k - 1})={formato(pendiente)}"),
            (f'x{k}={formato(x)}−({formato(fx)})/({formato(pendiente)})'
             f'={formato(nuevo)}',),
            (f'Cambio absoluto={formato(cambio)}',
             f'Error porcentual (%)={formato(porcentual)}'),
            (f'|f(x{k})|={formato(residuo)}',),
        ),
    )


def _terminar(x, datos, pasos, motivo, convergio=False):
    """Cierra el resultado conservando solamente iteraciones completas y finitas."""
    datos.update(
        motivo=motivo, convergio=convergio, iteraciones=len(datos['filas']),
        filas=tuple(datos['filas']), registros=tuple(datos['registros']),
    )
    pasos.append(Paso(
        'Terminación de Newton', motivo,
        formulas=((f'Última aproximación={formato(x)}',),
                  (f'Residuo |f(x)|={formato(datos["residuo"])}',)),
    ))
    return Calculo(x, tuple(pasos), datos)


def resolver_newton(funcion, derivada, x0, tolerancia=0.0001, max_iteraciones=200,
                    criterio='absoluto', *, tolerancia_f=1e-8, iteraciones_fijas=False, solo_error=False):
    """Devuelve Calculo con Newton propio, tabla y registros compatibles con #36–#38.

    El cambio elegido y el residuo deben ser menores que sus tolerancias; f(x)=0
    en la aritmética utilizada permite terminar antes. No busca todas las raíces.
    Entrada mal formada lanza ValueError; un fallo numérico conserva el historial.
    """
    x, tol, tol_f = _validar(
        funcion, derivada, x0, tolerancia, max_iteraciones, criterio, tolerancia_f,
    )
    datos = dict(
        metodo='newton', x0=x, tolerancia=tol, tolerancia_f=tol_f,
        max_iteraciones=max_iteraciones, criterio=criterio, columnas=COLUMNAS_NEWTON,
        filas=[], registros=[], residuo=None, advertencias=[],
    )
    pasos = [Paso(
        'Datos de Newton',
        'Newton parte de un punto inicial; no garantiza convergencia ni todas las raíces.',
        formulas=((f'x₀={formato(x)}', f'Tolerancia del cambio={formato(tol)}'),
                  (f'Tolerancia del residuo={formato(tol_f)}',)),
    )]
    try:
        fx = numero_finito(funcion(x), 'Función en x₀')
    except (ArithmeticError, ValueError, TypeError) as error:
        return _terminar(None, datos, pasos, f'No se pudo evaluar la función inicial: {error}')
    datos['residuo'] = abs(fx)
    if fx == 0:
        return _terminar(x, datos, pasos, 'La función evaluada da cero en x₀.', True)

    penultimo = None
    for k in range(1, max_iteraciones + 1):
        try:
            pendiente, nuevo, cambio, fnuevo, porcentual = _avance(funcion, derivada, x, fx)
        except (ArithmeticError, ValueError, TypeError) as error:
            return _terminar(
                x, datos, pasos,
                f'Interrupción al intentar la iteración {k}: {error}. '
                'Se conserva el último punto evaluado y su historial.',
            )
        residuo = abs(fnuevo)
        datos['residuo'] = residuo
        datos['filas'].append((k, x, fx, pendiente, nuevo, cambio, porcentual, residuo))
        datos['registros'].append(dict(
            i=k, xi=x, fxi=fx, derivada=pendiente, x_siguiente=nuevo,
            error_absoluto=cambio, error_porcentual=porcentual, residuo=residuo,
        ))
        pasos.append(_paso_explicado(k, x, fx, pendiente, nuevo, cambio, porcentual, residuo))
        error_elegido = porcentual if criterio == 'porcentual' else cambio
        if fnuevo == 0:
            return _terminar(nuevo, datos, pasos, 'La función evaluada da cero en el punto nuevo.', True)
        if nuevo == x:
            return _terminar(
                nuevo, datos, pasos,
                'Estancamiento en punto flotante con función no nula; revisar escala y residuo.',
            )
        cumple_error = error_elegido is not None and error_elegido < tol
        if cumple_error:
            datos.setdefault('primera_tolerancia', k)
        if cumple_error and iteraciones_fijas and k == max_iteraciones:
            return _terminar(nuevo, datos, pasos, 'Iteraciones completadas y tolerancia alcanzada.', True)
        if not iteraciones_fijas and cumple_error and (solo_error or residuo < tol_f):
            return _terminar(
                nuevo, datos, pasos, 'Se cumplen la tolerancia del cambio y la del residuo.', True,
            )
        if nuevo == penultimo:
            return _terminar(
                nuevo, datos, pasos, 'Se repite un ciclo de dos puntos sin alcanzar una raíz.',
            )
        penultimo, x, fx = x, nuevo, fnuevo
    if iteraciones_fijas:
        return _terminar(x, datos, pasos, 'Iteraciones solicitadas completadas sin cumplir la tolerancia final.')
    return _terminar(
        x, datos, pasos, 'Máximo de iteraciones alcanzado sin cumplir ambas tolerancias.',
    )


def contrastar_newton(calculo, funcion, derivada):
    """Añade una referencia opcional de SciPy sin reemplazar ni modificar el cálculo propio."""
    if calculo.datos.get('metodo') != 'newton':
        raise ValueError('El contraste requiere un resultado de Newton.')
    datos = dict(calculo.datos)
    datos.update(scipy=None, scipy_convergio=False, residuo_scipy=None, diferencia_scipy=None)
    try:
        import warnings
        from scipy.optimize import newton
        with warnings.catch_warnings(record=True) as avisos:
            warnings.simplefilter('always', RuntimeWarning)
            referencia, estado = newton(
                funcion, calculo.datos['x0'], fprime=derivada,
                tol=1e-12, maxiter=calculo.datos['max_iteraciones'],
                full_output=True, disp=False,
            )
        referencia = numero_finito(referencia, 'Referencia SciPy')
        residuo = abs(numero_finito(funcion(referencia), 'Residuo SciPy'))
        diferencia = numero_finito(abs(calculo.valor - referencia), 'Diferencia SciPy')
        datos.update(
            scipy=referencia, scipy_convergio=bool(estado.converged),
            residuo_scipy=residuo, diferencia_scipy=diferencia,
            aviso_scipy='; '.join(str(aviso.message) for aviso in avisos),
        )
    except (ImportError, ArithmeticError, ValueError, TypeError, RuntimeError) as error:
        datos['aviso_scipy'] = f'Referencia no disponible: {error}'
    return Calculo(calculo.valor, calculo.pasos, datos)
