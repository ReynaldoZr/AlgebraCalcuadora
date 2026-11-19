"""Aproxima derivadas por diferencias hacia adelante y centrales.

Tema: Sesión 22 y preparación provisional del Programa 9, issue 34.
Elaboración: equipo 9, con apoyo de IA.
"""

from modulos.numericos.funciones import formato, numero_finito
from modulos.procedimientos import Calculo, Paso


def _validar_configuracion(funcion, h, metodo):
    """Comprueba el proveedor, el paso nominal positivo y el esquema solicitado."""
    if not callable(funcion):
        raise ValueError('La función debe ser evaluable.')
    paso = numero_finito(h, 'Paso h')
    if paso <= 0:
        raise ValueError('El paso h debe ser positivo.')
    if metodo not in ('adelante', 'central'):
        raise ValueError('El método debe ser adelante o central.')
    return paso


def _muestras(funcion, x, h, metodo):
    """Evalúa solo puntos finitos y distinguibles de x, con diagnóstico de dominio."""
    izquierda = numero_finito(x - h, 'x−h') if metodo == 'central' else x
    derecha = numero_finito(x + h, 'x+h')
    if derecha == x or (metodo == 'central' and izquierda == x):
        raise ValueError('El paso h no es distinguible de x en punto flotante.')
    denominador = numero_finito(2 * h if metodo == 'central' else h, 'Denominador')
    try:
        fi = numero_finito(funcion(izquierda), 'f en el primer punto')
        fd = numero_finito(funcion(derecha), 'f en el segundo punto')
    except (ArithmeticError, ValueError, TypeError) as error:
        raise ValueError(f'No se puede evaluar la derivada en sus puntos: {error}') from None
    return izquierda, derecha, fi, fd, denominador


def calcular_derivada(funcion, x, h=1e-5, metodo='central'):
    """Devuelve Calculo con derivada aproximada, muestras, pasos y avisos de cancelación.

    No selecciona un h óptimo ni deriva simbólicamente. Dominio, h indistinguible
    o resultados no finitos producen ValueError, conservando a la función original.
    """
    paso = _validar_configuracion(funcion, h, metodo)
    punto = numero_finito(x, 'Punto x')
    izq, der, fi, fd, denominador = _muestras(funcion, punto, paso, metodo)
    diferencia = numero_finito(fd - fi, 'Diferencia de evaluaciones')
    valor = numero_finito(diferencia / denominador, 'Derivada aproximada')
    avisos = ()
    if fd == fi:
        # Igualdad de muestras no distingue derivada cero de pérdida de precisión.
        avisos = ('Las evaluaciones coinciden: puede ser derivada local cero o '
                  'cancelación por redondeo. Revisa la función y el paso h.',)
    elif valor == 0:
        avisos = ('El cociente se redondeó a cero por subdesbordamiento; '
                  'no debe interpretarse como una derivada exacta.',)
    esquema = '[f(x+h)−f(x−h)]/(2h)' if metodo == 'central' else '[f(x+h)−f(x)]/h'
    pasos = (
        Paso('Puntos de la derivada',
             'El paso debe cambiar los puntos y permitir evaluar la función.',
             formulas=((f'x={formato(punto)}', f'h={formato(paso)}'),
                       (f'f({formato(izq)})={formato(fi)}',
                        f'f({formato(der)})={formato(fd)}'))),
        Paso(f'Diferencia {metodo}', ' '.join(avisos),
             formulas=((f"f'(x)≈{esquema}={formato(valor)}",),)),
    )
    return Calculo(valor, pasos, dict(
        metodo=metodo, x=punto, h=paso, puntos=(izq, der), valores=(fi, fd),
        denominador=denominador, advertencias=avisos,
        orden_truncamiento=2 if metodo == 'central' else 1,
    ))


def crear_derivada(funcion, h=1e-5, metodo='central'):
    """Devuelve un callable de derivada compatible con Newton y con el adaptador #36."""
    paso = _validar_configuracion(funcion, h, metodo)

    def derivada(x):
        """Valida h y dominio en cada punto nuevo; no ejecuta otro bucle de Newton."""
        return calcular_derivada(funcion, x, paso, metodo).valor

    return derivada
