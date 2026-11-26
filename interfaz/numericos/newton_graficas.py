"""Construye gráficas de Newton-Raphson y comparación con bisección (Issue #38).

Tema: panel de función con tangente de iteración y panel de evolución con escala segura.
Equipo responsable: Grupo 9.
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
    intercepto = float(fxi) - float(derivada) * float(xi)
    return (float(derivada), intercepto) if isfinite(intercepto) else None


def _evaluar_seguro(funcion, x):
    """Interrumpe la curva ante evaluaciones inválidas; no detecta todas las asíntotas."""
    try:
        y = funcion(x)
        return float(y) if isfinite(y) and abs(y) < 1e100 else float('nan')
    except (ValueError, ZeroDivisionError, OverflowError, TypeError):
        return float('nan')


def _rango_funcion(calculo, registros):
    """Calcula límites horizontales legibles alrededor de x0, iteraciones y raíz."""
    puntos = [r[k] for r in registros for k in ('xi', 'x_siguiente')
              if r.get(k) is not None and isfinite(r.get(k))]
    if not puntos and isfinite(calculo.datos.get('x0', 0)):
        puntos.append(calculo.datos.get('x0', 0))
    if calculo.valor is not None and isfinite(calculo.valor):
        puntos.append(float(calculo.valor))
    if not puntos:
        return -2.0, 2.0
    minimo, maximo = min(puntos), max(puntos)
    amplitud = max(maximo - minimo, 1.0)
    margen = 0.3 * amplitud
    limites = minimo - margen, maximo + margen
    # Matplotlib tampoco representa de forma segura amplitudes cercanas a float máximo.
    if not all(isfinite(v) and abs(v) < 1e100 for v in limites):
        return None
    return limites


def figura_newton(calculo, funcion=None, iteracion_seleccionada=None,
                  comparacion_biseccion=None, oscuro=False):
    """Construye la figura de Newton (función+tangente arriba, error+residuo abajo)."""
    d = calculo.datos
    registros = list(d.get('registros', ()))
    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')
    eje_f = figura.add_subplot(211)
    eje_e = figura.add_subplot(212)

    limites = _rango_funcion(calculo, registros)
    if limites is None:
        eje_f.text(.5, .5, 'Trayectoria fuera del rango gráfico seguro.\n'
                   'Consulta los valores completos en la tabla.',
                   ha='center', va='center', transform=eje_f.transAxes)
        x_min, x_max = -2., 2.
        funcion = None
    else:
        x_min, x_max = limites
    azul = '#38bdf8' if oscuro else '#0369a1'
    violeta = '#c4b5fd' if oscuro else '#6d28d9'
    raiz = '#fbbf24' if oscuro else '#b91c1c'
    tangente_color = '#f9a8d4' if oscuro else '#be185d'
    residuo_color = '#22d3ee' if oscuro else '#0e7490'
    tolerancia_color = '#86efac' if oscuro else '#15803d'
    if funcion is not None:
        xs = [x_min * (1 - idx / 400) + x_max * (idx / 400) for idx in range(401)]
        ys = [_evaluar_seguro(funcion, x) for x in xs]
        # Un punto inválido corta la línea, sin unir lados de una singularidad conocida.
        for j in range(len(xs) - 1):
            medio = _evaluar_seguro(funcion, (xs[j] + xs[j + 1]) / 2)
            if not isfinite(medio) or (ys[j] * ys[j + 1] < 0
                                      and abs(medio) > max(abs(ys[j]), abs(ys[j + 1]))):
                ys[j] = float('nan')
        eje_f.plot(xs, ys, label='f(x)', color=azul)
        eje_f.set_xlim(x_min, x_max)
        if not any(isfinite(y) for y in ys):
            eje_f.text(.5, .8, 'Sin muestras representables: dominio o magnitud extrema.',
                       transform=eje_f.transAxes, ha='center')

    eje_f.axhline(0, color='gray', linewidth=0.8)

    if not registros and funcion is not None:
        x0 = d.get('x0')
        if x0 is not None and isfinite(x0):
            eje_f.scatter([x0], [_evaluar_seguro(funcion, x0)],
                          color=azul, label='x₀ inicial', zorder=4)
    if registros and limites is not None:
        x0 = registros[0].get('xi')
        y0 = registros[0].get('fxi')
        if x0 is not None and y0 is not None and isfinite(x0) and abs(y0) < 1e100:
            eje_f.scatter([x0], [y0], color='#fb923c' if oscuro else '#9a3412',
                          zorder=4, label='x₀ inicial')

        aprox_x = [r['x_siguiente'] for r in registros
                   if r.get('x_siguiente') is not None and isfinite(r['x_siguiente'])]
        if aprox_x and funcion is not None:
            aprox_y = [_evaluar_seguro(funcion, x) for x in aprox_x]
            eje_f.scatter(aprox_x, aprox_y, color=violeta, s=28, zorder=3, label='Aproximaciones')

        idx_sel = len(registros) - 1 if iteracion_seleccionada is None else max(0, min(iteracion_seleccionada, len(registros) - 1))
        reg_sel = registros[idx_sel]
        tangente = datos_tangente(reg_sel)
        if tangente is not None and abs(reg_sel['fxi']) < 1e100:
            m, b = tangente
            tx = [x_min, x_max]
            ty = [_evaluar_seguro(lambda x: m * x + b, x) for x in tx]
            eje_f.plot(tx, ty, linestyle='--', color=tangente_color,
                       label=f'Tangente (i={reg_sel.get("i")})')
            eje_f.scatter([reg_sel['xi']], [reg_sel['fxi']], marker='D',
                          color=tangente_color, label='Punto seleccionado', zorder=6)
            eje_f.scatter([reg_sel['x_siguiente']], [0], marker='x',
                          color=tangente_color, label='Siguiente x (corte de tangente)', zorder=6)

    if funcion is not None and calculo.valor is not None and isfinite(calculo.valor):
        y_raiz = _evaluar_seguro(funcion, calculo.valor)
        etiqueta_raiz = 'Raíz aproximada' if d.get('convergio') else 'Última aproximación (sin converger)'
        if isfinite(y_raiz):
            eje_f.scatter([calculo.valor], [y_raiz], color=raiz,
                          zorder=5, label=etiqueta_raiz)
            eje_f.annotate(f'x ≈ {calculo.valor:.8g}', (calculo.valor, y_raiz),
                           xytext=(6, 10), textcoords='offset points', color=raiz)

    eje_f.set(xlabel='x', ylabel='f(x)', title='Newton-Raphson · Función y recta tangente')
    eje_f.grid(alpha=0.3)
    if eje_f.get_legend_handles_labels()[0]:
        eje_f.legend(loc='upper right', fontsize=8, ncol=2)

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

    if any(abs(v) >= 1e100 for v in vals_err + vals_res):
        eje_e.text(.5, .5, 'Errores fuera del rango gráfico seguro. Consulta la tabla.',
                   transform=eje_e.transAxes, ha='center')
        iters_err, vals_err, iters_res, vals_res = [], [], [], []

    if iters_err:
        eje_e.plot(iters_err, vals_err, marker='.', color=violeta, label=etiqueta_err)
    # Residuo y cambio no comparten necesariamente unidades ni tolerancia.
    eje_res = eje_e.twinx()
    eje_res.set_ylabel('Residuo |f(x)|', color=residuo_color)
    if iters_res:
        eje_res.plot(iters_res, vals_res, marker='x', linestyle=':', color=residuo_color, label='Residuo |f(x)|')
        if all(v > 0 for v in vals_res):
            eje_res.set_yscale('log')
        eje_res.legend(loc='upper right', fontsize='small')

    tol_f = d.get('tolerancia_f')
    if iters_res and tol_f is not None and 0 < tol_f < 1e100:
        eje_res.axhline(tol_f, color=residuo_color, linestyle='--', alpha=.8,
                        label=f'Umbral residuo = {tol_f:g}')
        eje_res.legend(loc='upper right', fontsize='small')

    tol = d.get('tolerancia')
    if tol is not None and isfinite(tol) and 0 < tol < 1e100:
        eje_e.axhline(float(tol), color=tolerancia_color, linestyle='--', linewidth=1.0, label=f'Tolerancia ε={tol:g}')

    if comparacion_biseccion is not None:
        if criterio == 'porcentual':
            raise ValueError('Compara con bisección usando cambio absoluto; la cota no es porcentual.')
        if d.get('funcion') != comparacion_biseccion.datos.get('funcion'):
            raise ValueError('La comparación requiere la misma función en ambos métodos.')
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
    if registros:
        seleccionado = len(registros) - 1 if iteracion_seleccionada is None else max(
            0, min(iteracion_seleccionada, len(registros) - 1))
        eje_e.axvline(registros[seleccionado]['i'], color=tangente_color,
                      alpha=.6, linestyle=':', label='Iteración seleccionada')
    else:
        eje_e.text(.5, .5, 'Sin iteraciones: ' + d.get('motivo', ''),
                   transform=eje_e.transAxes, ha='center', va='center', wrap=True)
    eje_e.grid(alpha=0.3)
    if iters_err or iters_res or (tol is not None and tol > 0):
        eje_e.legend(loc='upper left', fontsize='small')

    return figura
