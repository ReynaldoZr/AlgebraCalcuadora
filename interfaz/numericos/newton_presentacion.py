"""Presenta vista previa, todos los pasos y tabla completa de Newton (Issue #37).

Tema: consumo exclusivo del contrato Calculo/Paso de #33, sin cálculos ni parseo en QML.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.metodos_numericos import formato_visual
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


def _fmt6(valor):
    """Formatea valores numéricos a 6 decimales únicamente para presentar pasos."""
    if valor is None:
        return 'No definido'
    if isinstance(valor, int) and not isinstance(valor, bool):
        return str(valor)
    return formato_visual(valor)


def _enriquecer_paso_newton(paso, reg, datos):
    """Presenta la iteración de Newton a 6 decimales con resta de error y ¿Detener?."""
    k = reg.get('i')
    xi = reg.get('xi')
    fxi = reg.get('fxi')
    derivada = reg.get('derivada')
    x_sig = reg.get('x_siguiente')
    err_abs = reg.get('error_absoluto')
    err_pct = reg.get('error_porcentual')
    residuo = reg.get('residuo')
    criterio = datos.get('criterio', 'absoluto')
    tol = datos.get('tolerancia')
    tol_f = datos.get('tolerancia_f')
    err_val = err_pct if criterio == 'porcentual' else err_abs

    formulas = [
        (f'x{k - 1}={_fmt6(xi)}', f'f(x{k - 1})={_fmt6(fxi)}', f"f'(x{k - 1})={_fmt6(derivada)}"),
        (f'x{k}={_fmt6(xi)}−({_fmt6(fxi)})/({_fmt6(derivada)})={_fmt6(x_sig)}',),
        (f'Cambio absoluto={_fmt6(err_abs)}', f'Error porcentual (%)={_fmt6(err_pct)}'),
        (f'|f(x{k})|={_fmt6(residuo)}',),
        (f'εa = |{_fmt6(x_sig)} − ({_fmt6(xi)})| = {_fmt6(err_abs)}',),
    ]
    if tol is not None and tol_f is not None:
        if err_val is None:
            err_cmp = 'Error no definido → seguir'
        elif err_val < tol:
            err_cmp = f'{_fmt6(err_val)} < {_fmt6(tol)} (cambio OK)'
        else:
            err_cmp = f'{_fmt6(err_val)} ≥ {_fmt6(tol)} → NO, seguir'

        if residuo == 0:
            res_cmp = 'f(x) = 0 (detener)'
        elif residuo is not None and residuo < tol_f:
            res_cmp = f'|f(x)| = {_fmt6(residuo)} < {_fmt6(tol_f)} (residuo OK)'
        else:
            res_cmp = f'|f(x)| = {_fmt6(residuo)} ≥ {_fmt6(tol_f)} → NO, seguir'

        detener = residuo == 0 or (
            err_val is not None and err_val < tol and residuo is not None and residuo < tol_f
        )
        decision = 'Detener (tolerancias cumplidas)' if detener else 'Seguir'
        formulas.append((f'¿Detener? {decision}', err_cmp, res_cmp))

    return Paso(
        paso.titulo,
        paso.detalle,
        formulas=tuple(formulas),
        matriz=paso.matriz,
        separador=paso.separador,
    )


def pasos_completos_newton(calculo):
    """Conserva todas las etapas originales de Calculo y agrega error explícito y ¿Detener?."""
    d = calculo.datos
    por_iter = {r.get('i'): r for r in d.get('registros', ()) if r.get('i') is not None}
    resultado = []
    for paso in calculo.pasos:
        reg = None
        if paso.titulo.startswith('Iteración '):
            trozo = paso.titulo[len('Iteración '):].split(' ', 1)[0]
            if trozo.isdigit():
                reg = por_iter.get(int(trozo))
        paso_final = _enriquecer_paso_newton(paso, reg, d) if reg is not None else paso
        resultado.append(paso_visual(paso_final, completo=True))
    return resultado


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
