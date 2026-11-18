"""Construye gráficas de Newton-Raphson y comparación con bisección (Issue #38).

Tema: panel de función con tangente de iteración y panel de evolución con escala segura.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from math import isfinite

from matplotlib.figure import Figure


def datos_tangente(registro):
    """Devuelve pendiente e intercepto de la recta tangente y = m*x + b en (xi, f(xi))."""
    xi = registro.get('xi')
    fxi = registro.get('fxi')
    derivada = registro.get('derivada')
    if xi is None or fxi is None or derivada is None:
        return None
    if not (isfinite(xi) and isfinite(fxi) and isfinite(derivada)):
        return None
    return float(derivada), float(fxi) - float(derivada) * float(xi)


def _evaluar_seguro(funcion, x):
    """Interrumpe la curva ante evaluaciones inválidas; no detecta todas las asíntotas."""
    try:
        y = funcion(x)
        return float(y) if isfinite(y) else float('nan')
    except (ValueError, ZeroDivisionError, OverflowError, TypeError):
        return float('nan')


def _rango_funcion(calculo, registros):
    """Calcula límites horizontales legibles alrededor de x0, iteraciones y raíz."""
    puntos = [r[k] for r in registros for k in ('xi', 'x_siguiente')
              if r.get(k) is not None and isfinite(r.get(k))]
    if calculo.valor is not None and isfinite(calculo.valor):
        puntos.append(float(calculo.valor))
    if not puntos:
        return -2.0, 2.0
    minimo, maximo = min(puntos), max(puntos)
    amplitud = max(maximo - minimo, 1.0)
    margen = 0.3 * amplitud
    return minimo - margen, maximo + margen


def figura_newton(calculo, funcion=None, iteracion_seleccionada=None, comparacion_biseccion=None):
    """Construye la figura de Newton (función+tangente arriba, error+residuo abajo)."""
    d = calculo.datos
    registros = list(d.get('registros', ()))
    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')
    eje_f = figura.add_subplot(211)
    eje_e = figura.add_subplot(212)

    x_min, x_max = _rango_funcion(calculo, registros)
    if funcion is not None:
        xs = [x_min + (x_max - x_min) * idx / 400 for idx in range(401)]
        ys = [_evaluar_seguro(funcion, x) for x in xs]
        eje_f.plot(xs, ys, label='f(x)', color='#38bdf8')

    eje_f.axhline(0, color='gray', linewidth=0.8)

    if registros:
        x0 = registros[0].get('xi')
        y0 = registros[0].get('fxi')
        if x0 is not None and y0 is not None and isfinite(x0) and isfinite(y0):
            eje_f.scatter([x0], [y0], color='#f59e0b', zorder=4, label='x₀ inicial')

        aprox_x = [r['x_siguiente'] for r in registros
                   if r.get('x_siguiente') is not None and isfinite(r['x_siguiente'])]
        if aprox_x and funcion is not None:
            aprox_y = [_evaluar_seguro(funcion, x) for x in aprox_x]
            eje_f.scatter(aprox_x, aprox_y, color='#a5a6ff', s=28, zorder=3, label='Aproximaciones')

        idx_sel = len(registros) - 1 if iteracion_seleccionada is None else max(0, min(iteracion_seleccionada, len(registros) - 1))
        reg_sel = registros[idx_sel]
        tangente = datos_tangente(reg_sel)
        if tangente is not None:
            m, b = tangente
            tx = [x_min, x_max]
            ty = [m * tx[0] + b, m * tx[1] + b]
            eje_f.plot(tx, ty, linestyle='--', color='#f472b6', label=f'Tangente (i={reg_sel.get("i")})')

    if funcion is not None and calculo.valor is not None and isfinite(calculo.valor):
        y_raiz = _evaluar_seguro(funcion, calculo.valor)
        etiqueta_raiz = 'Raíz aproximada' if d.get('convergio') else 'Última aproximación (sin converger)'
        eje_f.scatter([calculo.valor], [y_raiz], color='#22c55e' if d.get('convergio') else '#ef4444',
                      zorder=5, label=etiqueta_raiz)

    eje_f.set(xlabel='x', ylabel='f(x)', title='Newton-Raphson · Función y recta tangente')
    eje_f.grid(alpha=0.3)
    eje_f.legend(loc='best', fontsize='small')

    criterio = d.get('criterio', 'absoluto')
    clave_err = 'error_porcentual' if criterio == 'porcentual' else 'error_absoluto'
    etiqueta_err = 'Error porcentual (%)' if criterio == 'porcentual' else 'Cambio absoluto |xᵢ₊₁ − xᵢ|'
    iters_err, vals_err = [], []
    iters_res, vals_res = [], []
    for r in registros:
        it = r.get('i')
        ev = r.get(clave_err)
        rv = r.get('residuo')
        if it is not None and ev is not None and isfinite(ev):
            iters_err.append(it)
            vals_err.append(float(ev))
        if it is not None and rv is not None and isfinite(rv):
            iters_res.append(it)
            vals_res.append(float(rv))

    if iters_err:
        eje_e.plot(iters_err, vals_err, marker='.', color='#a5a6ff', label=etiqueta_err)
    # Residuo y cambio no comparten necesariamente unidades ni tolerancia.
    eje_res = eje_e.twinx()
    eje_res.set_ylabel('Residuo |f(x)|', color='#087c9e')
    if iters_res:
        eje_res.plot(iters_res, vals_res, marker='x', linestyle=':', color='#087c9e', label='Residuo |f(x)|')
        if all(v > 0 for v in vals_res):
            eje_res.set_yscale('log')
        eje_res.legend(loc='upper right', fontsize='small')

    tol = d.get('tolerancia')
    if tol is not None and isfinite(tol) and tol > 0:
        eje_e.axhline(float(tol), color='#22c55e', linestyle='--', linewidth=1.0, label=f'Tolerancia ε={tol:g}')

    if comparacion_biseccion is not None:
        if criterio == 'porcentual':
            raise ValueError('Compara con bisección usando cambio absoluto; la cota no es porcentual.')
        filas_b = comparacion_biseccion.datos.get('filas', ())
        if filas_b:
            eje_e.plot(
                [f[0] for f in filas_b],
                [f[8] for f in filas_b],
                marker='s',
                markersize=3,
                color='#f59e0b',
                label='Bisección (cota de intervalo, criterio distinto)',
            )

    if vals_err and all(v > 0 for v in vals_err):
        eje_e.set_yscale('log')

    eje_e.set(xlabel='Iteración', ylabel=etiqueta_err, title='Evolución de error y residuo')
    eje_e.grid(alpha=0.3)
    if iters_err or iters_res or (tol is not None and tol > 0):
        eje_e.legend(loc='upper left', fontsize='small')

    return figura
