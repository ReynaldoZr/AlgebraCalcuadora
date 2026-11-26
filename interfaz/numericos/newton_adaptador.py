"""Adapta el formulario y el resumen de Newton-Raphson al contrato de #33 (Issue #36).

Tema: entradas vacías, validación de derivada analítica/numérica y resumen sin datos falsos.
Elaboración: equipo del proyecto
"""

from dataclasses import dataclass

from modulos.numericos.funciones import crear_funcion, formato, numero_finito

CRITERIOS_NEWTON = ('absoluto', 'porcentual')
MODOS_DERIVADA = ('analitica', 'numerica')


@dataclass(frozen=True)
class CampoNewton:
    """Describe etiqueta y valor inicial de un campo del formulario de Newton."""

    clave: str
    etiqueta: str
    defecto: str


CAMPOS_NEWTON = {
    'funcion': CampoNewton('funcion', 'f(x)', ''),
    'x0': CampoNewton('x0', 'Valor inicial x₀', ''),
    'modo_derivada': CampoNewton('modo_derivada', 'Derivada', 'analitica'),
    'derivada': CampoNewton('derivada', "f'(x)", ''),
    'h': CampoNewton('h', 'Paso h (derivada numérica)', ''),
    'criterio': CampoNewton('criterio', 'Criterio de error', 'absoluto'),
    'tolerancia': CampoNewton('tolerancia', 'Tolerancia del cambio (en x o %)', '0.0001'),
    'tolerancia_f': CampoNewton('tolerancia_f', 'Tolerancia del residuo |f(x)|', '1e-8'),
    'maximo': CampoNewton('maximo', 'Máximo de iteraciones', '200'),
}


def parametros_defecto_newton():
    """Devuelve ajustes de cálculo por defecto para Newton-Raphson."""
    return {k: v.defecto for k, v in CAMPOS_NEWTON.items()}


def parametros_vacios_newton():
    """Mantiene ajustes de tolerancia y método, dejando vacíos los datos del ejercicio."""
    datos = parametros_defecto_newton()
    for campo in ('funcion', 'x0', 'derivada', 'h'):
        datos[campo] = ''
    return datos


def ejemplo_newton(caso='exp(-x)-x'):
    """Devuelve parámetros de ejemplo solo cuando la persona lo solicita."""
    casos = {
        'exp(-x)-x': dict(
            funcion='exp(-x)-x',
            x0='0',
            modo_derivada='analitica',
            derivada='-exp(-x)-1',
            h='',
            criterio='absoluto',
            tolerancia='0.0001',
            tolerancia_f='1e-8',
            maximo='50',
        ),
        'Ciclo cúbico': dict(
            funcion='x^3-2*x+2',
            x0='0',
            modo_derivada='analitica',
            derivada='3*x^2-2',
            h='',
            criterio='absoluto',
            tolerancia='1e-6',
            tolerancia_f='1e-8',
            maximo='20',
        ),
        'Salto x^10-1': dict(
            funcion='x^10-1',
            x0='0.5',
            modo_derivada='analitica',
            derivada='10*x^9',
            h='',
            criterio='absoluto',
            tolerancia='1e-6',
            tolerancia_f='1e-8',
            maximo='50',
        ),
    }
    if caso not in casos:
        raise ValueError('El ejemplo solicitado no pertenece a Newton-Raphson.')
    return dict(casos[caso])


def validar_entrada_newton(parametros, proveedor_derivada=None):
    """Valida campos del formulario antes de invocar el núcleo de Newton."""
    p = parametros
    funcion_txt = str(p.get('funcion', '')).strip()
    if not funcion_txt:
        raise ValueError('Escribe la función f(x).')
    funcion = crear_funcion(funcion_txt)

    x0_txt = str(p.get('x0', '')).strip()
    if not x0_txt:
        raise ValueError('Escribe el valor inicial x₀.')
    x0 = numero_finito(x0_txt, 'Valor inicial x₀')

    modo = str(p.get('modo_derivada', 'analitica')).strip().lower()
    if modo not in MODOS_DERIVADA:
        raise ValueError('El modo de derivada debe ser "analitica" o "numerica".')

    if modo == 'analitica':
        deriv_txt = str(p.get('derivada', '')).strip()
        if not deriv_txt:
            raise ValueError("Escribe la derivada analítica f'(x) o elige derivada numérica.")
        derivada = crear_funcion(deriv_txt)
    else:
        h = numero_finito(p.get('h', ''), 'Paso h')
        if h <= 0:
            raise ValueError('El paso h debe ser mayor que cero.')
        if x0 + h == x0 or x0 - h == x0:
            raise ValueError('El paso h debe ser distinguible de x₀ en punto flotante.')
        # El cálculo se delega al módulo numérico; la interfaz no deriva la función.
        if proveedor_derivada is None:
            from modulos.numericos.derivadas import crear_derivada
            proveedor_derivada = crear_derivada
        derivada = proveedor_derivada(funcion, h)
        if not callable(derivada):
            raise ValueError('El proveedor debe devolver una función de derivada.')

    criterio = str(p.get('criterio', 'absoluto')).strip().lower()
    if criterio not in CRITERIOS_NEWTON:
        raise ValueError('El criterio debe ser "absoluto" o "porcentual".')

    tolerancia = numero_finito(p.get('tolerancia', ''), 'Tolerancia ε')
    if tolerancia <= 0:
        raise ValueError('La tolerancia ε debe ser mayor que cero.')
    tolerancia_f = numero_finito(p.get('tolerancia_f', '1e-8'), 'Tolerancia del residuo')
    if tolerancia_f <= 0:
        raise ValueError('La tolerancia del residuo debe ser mayor que cero.')

    try:
        maximo = int(str(p.get('maximo', '')).strip())
    except ValueError:
        raise ValueError('El máximo de iteraciones debe ser un entero positivo.') from None
    if not 1 <= maximo <= 10000:
        raise ValueError('El máximo de iteraciones debe estar entre 1 y 10000.')

    return dict(
        funcion=funcion,
        derivada=derivada,
        x0=x0,
        tolerancia=tolerancia,
        max_iteraciones=maximo,
        criterio=criterio,
        tolerancia_f=tolerancia_f,
    )


def resumen_newton(calculo):
    """Genera un resumen breve y claro sin llamar valor real a referencias aproximadas."""
    d = calculo.datos
    convergio = bool(d.get('convergio'))
    unidad = '%' if d.get('criterio') == 'porcentual' else '(cambio absoluto)'
    raiz_txt = formato(calculo.valor) if calculo.valor is not None else 'No disponible'
    etiqueta = 'Raíz aproximada' if convergio else 'Última aproximación'
    residuo_txt = formato(d.get('residuo'))
    estado = 'Convergió' if convergio else 'No convergió'
    return (
        f'{etiqueta}: {raiz_txt}\n'
        f'Estado: {estado} · Iteraciones: {d.get("iteraciones", len(d.get("filas", ())))}\n'
        f'Motivo: {d.get("motivo", "")}\n'
        f'Criterio: {d.get("criterio", "absoluto")} {unidad} · Tolerancia: {formato(d.get("tolerancia"))}\n'
        f'Comprobación |f(x)| (residuo): {residuo_txt}\n'
        f'Tolerancia del residuo: {formato(d.get("tolerancia_f"))}'
    )


def ejecutar_newton_adaptador(parametros, solver=None, proveedor_derivada=None):
    """Valida entradas y ejecuta Newton usando un solver inyectado o el núcleo de #33."""
    args = validar_entrada_newton(parametros, proveedor_derivada)
    if solver is None:
        from modulos.numericos.newton import resolver_newton
        solver = resolver_newton
    return solver(
        args['funcion'],
        args['derivada'],
        args['x0'],
        args['tolerancia'],
        args['max_iteraciones'],
        criterio=args['criterio'],
        tolerancia_f=args['tolerancia_f'],
        **({'solo_error': True} if parametros.get('parada') == 'Solo tolerancia del error' else {}),
        **({'iteraciones_fijas': True} if parametros.get('parada') == 'Iteraciones fijas' else {}),
    )
