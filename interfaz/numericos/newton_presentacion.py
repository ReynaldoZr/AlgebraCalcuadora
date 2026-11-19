"""Presenta vista previa, todos los pasos y tabla completa de Newton (Issue #37).

Tema: consumo exclusivo del contrato Calculo/Paso de #33, sin cálculos ni parseo en QML.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.qt.presentacion import paso_visual
from modulos.numericos.funciones import formato
from modulos.procedimientos import Paso

COLUMNAS_TABLA_NEWTON = (
    'i',
    'xi',
    'f(xi)',
    'derivada',
    'x siguiente',
    'cambio absoluto',
    'error porcentual (%)',
    'residuo',
)


def _celda_newton(valor):
    """Formatea un valor numérico conservando precisión o indicando 'No definido'."""
    if valor is None:
        return 'No definido'
    if isinstance(valor, int) and not isinstance(valor, bool):
        return str(valor)
    return formato(valor)


def etapas_newton(calculo):
    """Devuelve pasos breves reutilizables por Qt y Tk, sin repetir el cálculo."""
    d = calculo.datos
    registros = d.get('registros', ())
    etapas = []
    for reg in registros:
        i = reg.get('i')
        xi = reg.get('xi')
        x_sig = reg.get('x_siguiente')
        err_abs = reg.get('error_absoluto')
        err_pct = reg.get('error_porcentual')
        criterio = d.get('criterio', 'absoluto')
        err_txt = (
            f'Error porcentual = {_celda_newton(err_pct)} %'
            if criterio == 'porcentual'
            else f'Cambio absoluto = {_celda_newton(err_abs)}'
        )
        etapas.append(Paso(
            f'Iteración {i}',
            f'Evaluamos la función y su derivada para avanzar con la tangente. {err_txt}; '
            f'residuo |f(x)| = {_celda_newton(reg.get("residuo"))}.',
            formulas=(
                (f'xᵢ = {_celda_newton(xi)}', '→', f'xᵢ₊₁ = {_celda_newton(x_sig)}'),
            ),
        ))
    if not etapas:
        etapas.append(Paso(
            'Resultado inicial',
            d.get('motivo', 'Sin iteraciones adicionales.'),
            formulas=((f'x = {_celda_newton(calculo.valor)}', f'|f(x)| = {_celda_newton(d.get("residuo"))}'),),
        ))
    return tuple(etapas)


def pasos_previa_newton(calculo):
    """Presenta las etapas breves mediante el contrato visual existente."""
    return tuple(paso_visual(p, completo=False) for p in etapas_newton(calculo))


def pasos_completos_newton(calculo):
    """Conserva todas las etapas originales de Calculo sin truncar ni ocultar iteraciones."""
    return [paso_visual(paso, completo=True) for paso in calculo.pasos]


def tabla_newton(calculo):
    """Prepara la tabla completa sin rellenar datos faltantes ni errores indefinidos con cero."""
    d = calculo.datos
    filas_origen = d.get('filas', ())
    if filas_origen:
        filas = [[_celda_newton(celda) for celda in fila] for fila in filas_origen]
    else:
        registros = d.get('registros', ())
        filas = [
            [
                _celda_newton(r.get('i')),
                _celda_newton(r.get('xi')),
                _celda_newton(r.get('fxi')),
                _celda_newton(r.get('derivada')),
                _celda_newton(r.get('x_siguiente')),
                _celda_newton(r.get('error_absoluto')),
                _celda_newton(r.get('error_porcentual')),
                _celda_newton(r.get('residuo')),
            ]
            for r in registros
        ]
    columnas = list(COLUMNAS_TABLA_NEWTON)
    return dict(columnas=columnas, filas=filas)
