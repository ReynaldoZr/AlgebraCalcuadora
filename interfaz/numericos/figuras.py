"""Construye figuras interactivas de la semana 12 sin depender de Tk ni Qt.

Tema: reutilizar las mismas curvas en ambas interfaces con inspección y zoom.
Elaboracion: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction
import math

from matplotlib.colors import LogNorm
from matplotlib.figure import Figure

from interfaz.metodos_numericos import formato_visual, subindice
from modulos.numericos.funciones import crear_funcion, formato


def _evaluar_seguro(funcion, x):
    """Evalúa f(x) devolviendo NaN en discontinuidades para no unir segmentos inválidos."""
    try:
        y = funcion(x)
        return float(y) if math.isfinite(y) else float('nan')
    except (ValueError, ZeroDivisionError, OverflowError, TypeError):
        return float('nan')


def _aplicar_zoom(eje, zoom, indice_panel=0):
    """Aplica ventana de zoom/desplazamiento si se proporcionó para el panel."""
    if not zoom:
        return
    limites = zoom.get(indice_panel) if isinstance(zoom, dict) else (zoom if indice_panel == 0 else None)
    if limites and len(limites) == 4:
        xmin, xmax, ymin, ymax = limites
        if all(math.isfinite(v) for v in limites) and xmin != xmax:
            eje.set_xlim(xmin, xmax)
        if all(math.isfinite(v) for v in limites) and ymin != ymax:
            eje.set_ylim(ymin, ymax)


def _escala_log_segura(eje, valores):
    """Activa escala logarítmica solo cuando todos los valores son estrictamente positivos."""
    finitos = [v for v in valores if v is not None and math.isfinite(v)]
    if finitos and all(v > 0 for v in finitos):
        eje.set_yscale('log')


def _colores_tema(oscuro):
    """Devuelve colores contrastantes para curvas, raíces y avisos según tema claro/oscuro."""
    if oscuro:
        return dict(
            curva='#38bdf8',
            jacobi='#a5a6ff',
            gs='#38bdf8',
            raiz='#ffb454',
            seleccion='#f472b6',
            tolerancia='#22c55e',
            secundario='#f59e0b',
            texto='#e8ecf4',
        )
    return dict(
        curva='#1d4ed8',
        jacobi='#4f46e5',
        gs='#0284c7',
        raiz='#b52b27',
        seleccion='#be185d',
        tolerancia='#15803d',
        secundario='#b45309',
        texto='#344e41',
    )


def _figura_biseccion(calculo, oscuro, iteracion_seleccionada=None, zoom=None, panel_expandido=None):
    """Construye vista apilada de f(x) arriba y error abajo conectada a la fila elegida."""
    d = calculo.datos
    c = _colores_tema(oscuro)
    funcion = crear_funcion(d['funcion'])
    a, b = d['intervalo']
    filas = d.get('filas', ())
    con_iteraciones = bool(filas)
    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')

    mostrar_sup = panel_expandido in (None, 0)
    mostrar_inf = con_iteraciones and panel_expandido in (None, 1)

    if mostrar_sup:
        pos_sup = 211 if (mostrar_sup and mostrar_inf) else 111
        eje = figura.add_subplot(pos_sup)
        puntos = [a + (b - a) * i / 400 for i in range(401)]
        valores = [_evaluar_seguro(funcion, p) for p in puntos]
        eje.plot(puntos, valores, color=c['curva'], label='f(x)')
        eje.axhline(0, color='gray', linewidth=0.8)

        raices = d.get('raices_extremos') or ((calculo.valor,) if calculo.valor is not None else ())
        etiqueta = 'Raíces en los extremos' if d.get('raices_extremos') else 'Aproximación final'
        if raices:
            ys_raiz = [_evaluar_seguro(funcion, r) for r in raices]
            eje.scatter(raices, ys_raiz, label=etiqueta, color=c['raiz'], zorder=4)
            for raiz, y_r in zip(raices, ys_raiz):
                if math.isfinite(y_r):
                    eje.annotate(f'x={raiz:g}', (raiz, y_r), xytext=(0, 10),
                                 textcoords='offset points', ha='center', color=c['raiz'])

        if con_iteraciones and iteracion_seleccionada is not None:
            idx = max(0, min(iteracion_seleccionada, len(filas) - 1))
            fila = filas[idx]
            xl, xu, xr = fila[1], fila[2], fila[3]
            eje.axvspan(xl, xu, color=c['seleccion'], alpha=0.14, label=f'Intervalo [{formato_visual(xl)}, {formato_visual(xu)}]')
            yxr = _evaluar_seguro(funcion, xr)
            if math.isfinite(yxr):
                eje.scatter([xr], [yxr], color=c['seleccion'], s=55, zorder=5, label=f'xr (it. {fila[0]})')

        estado_txt = 'Convergió' if d.get('convergio') else 'Sin converger'
        titulo_sup = (
            f'Bisección · {estado_txt} · {d.get("motivo", "")}'
            if con_iteraciones
            else 'Raíces verificadas en los extremos · 0 iteraciones'
        )
        eje.set(xlabel='x', ylabel='f(x)', title=titulo_sup)
        eje.legend(loc='best', fontsize='small')
        eje.grid(alpha=0.3)
        _aplicar_zoom(eje, zoom, 0)

    if mostrar_inf:
        pos_inf = 212 if (mostrar_sup and mostrar_inf) else 111
        eje_err = figura.add_subplot(pos_inf)
        criterio = d.get('criterio', 'intervalo')
        if criterio == 'porcentual':
            pares = [(f[0], f[7]) for f in filas if f[7] is not None and math.isfinite(f[7])]
            ylabel = 'Error porcentual Ea (%)'
            titulo_inf = 'Evolución del error porcentual (%)'
            etiqueta_curva = 'Error porcentual (%)'
        else:
            pares = [(f[0], f[8]) for f in filas if f[8] is not None and math.isfinite(f[8])]
            ylabel = 'Cota absoluta en x'
            titulo_inf = 'Reducción del intervalo (cota en x)'
            etiqueta_curva = 'Cota absoluta en x'

        xs_err = [p[0] for p in pares]
        ys_err = [p[1] for p in pares]
        if xs_err:
            eje_err.plot(xs_err, ys_err, marker='.', color=c['jacobi'], label=etiqueta_curva)
        tol = d.get('tolerancia')
        if tol is not None and tol > 0:
            unidad_tol = '%' if criterio == 'porcentual' else 'x'
            eje_err.axhline(tol, color=c['tolerancia'], linestyle='--', linewidth=1.0,
                            label=f'Tolerancia ({formato_visual(tol)} {unidad_tol})')

        if iteracion_seleccionada is not None and filas:
            idx = max(0, min(iteracion_seleccionada, len(filas) - 1))
            fila = filas[idx]
            val_sel = fila[7] if criterio == 'porcentual' else fila[8]
            if val_sel is not None and math.isfinite(val_sel):
                eje_err.scatter([fila[0]], [val_sel], color=c['seleccion'], s=60, zorder=5,
                                label=f'It. {fila[0]}: {formato_visual(val_sel)}')

        _escala_log_segura(eje_err, ys_err + ([tol] if tol and tol > 0 else []))
        eje_err.set(xlabel='Iteración', ylabel=ylabel, title=titulo_inf)
        eje_err.legend(loc='best', fontsize='small')
        eje_err.grid(alpha=0.3)
        _aplicar_zoom(eje_err, zoom, 1)

    return figura


def _figura_iterativo(clave, calculo, oscuro, iteracion_seleccionada=None, zoom=None):
    """Construye gráfica individual de Jacobi o Gauss-Seidel con tolerancia y selección."""
    d = calculo.datos
    c = _colores_tema(oscuro)
    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')
    eje = figura.add_subplot(111)
    filas = d.get('filas', ())
    etiqueta = d.get('metodo', 'Jacobi' if clave == 'num_jacobi' else 'Gauss-Seidel')
    color_linea = c['jacobi'] if clave == 'num_jacobi' else c['gs']
    marcador = 'o' if clave == 'num_jacobi' else 's'

    xs = [f[0] for f in filas]
    ys = [f[-1] for f in filas]
    if xs:
        eje.plot(xs, ys, marker=marcador, markersize=5, color=color_linea, label=etiqueta)
        eje.scatter([xs[-1]], [ys[-1]], color=c['raiz'], zorder=4, s=55)
        eje.annotate(f'It. {xs[-1]}: {formato_visual(ys[-1])}', (xs[-1], ys[-1]),
                     xytext=(-8, 10), textcoords='offset points', ha='right', color=c['raiz'])
    else:
        eje.text(0.5, 0.5, 'Sin iteraciones registradas.\n' + d.get('motivo', ''),
                 transform=eje.transAxes, ha='center', va='center', color=c['texto'])

    tol = d.get('tolerancia')
    if tol is not None and tol > 0:
        eje.axhline(tol, color=c['tolerancia'], linestyle='--', linewidth=1.0,
                    label=f'Tolerancia ε = {formato_visual(tol)}')

    if iteracion_seleccionada is not None and filas:
        idx = max(0, min(iteracion_seleccionada, len(filas) - 1))
        eje.scatter([xs[idx]], [ys[idx]], color=c['seleccion'], s=75, zorder=5,
                    label=f'Seleccionada (it. {xs[idx]}): {formato_visual(ys[idx])}')

    _escala_log_segura(eje, ys + ([tol] if tol and tol > 0 else []))
    extra = ''
    if clave == 'num_gauss_seidel':
        lam = d.get('relajacion', 1)
        extra = f' · λ={formato_visual(lam)}'
    orden_txt = 'Reordenadas' if d.get('reordenado') else 'Original'
    estado_txt = 'Convergió' if d.get('convergio') else 'Sin converger'
    eje.set(
        xlabel='Iteración',
        ylabel='Diferencia máxima entre iteraciones',
        title=f'{etiqueta}{extra} ({orden_txt}) · {estado_txt}',
    )
    eje.grid(alpha=0.3)
    if xs or (tol and tol > 0):
        eje.legend(loc='best', fontsize='small')
    _aplicar_zoom(eje, zoom, 0)
    return figura


def _figura_comparar_iterativos(calculo, oscuro, iteracion_seleccionada=None, visibles=None, zoom=None):
    """Dibuja ambas curvas con sus longitudes reales y recorrido sincronizado."""
    d = calculo.datos
    c = _colores_tema(oscuro)
    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')
    eje = figura.add_subplot(111)
    filas_j = d['jacobi']['filas']
    filas_gs = d['gauss_seidel']['filas']
    visibles = visibles or {'jacobi': True, 'gauss_seidel': True}

    valores_log = []
    if visibles.get('jacobi', True) and filas_j:
        xj = [f[0] for f in filas_j]
        yj = [f[-1] for f in filas_j]
        valores_log.extend(yj)
        eje.plot(xj, yj, marker='o', markersize=4, color=c['jacobi'], label=f'Jacobi ({len(xj)} it.)')
        eje.annotate(f'J({xj[-1]}): {formato_visual(yj[-1])}', (xj[-1], yj[-1]),
                     xytext=(0, 8), textcoords='offset points', ha='center', color=c['jacobi'], fontsize=9)
        if iteracion_seleccionada is not None:
            idx_j = min(max(iteracion_seleccionada, 0), len(filas_j) - 1)
            eje.scatter([xj[idx_j]], [yj[idx_j]], color=c['seleccion'], s=65, zorder=5)

    if visibles.get('gauss_seidel', True) and filas_gs:
        xgs = [f[0] for f in filas_gs]
        ygs = [f[-1] for f in filas_gs]
        valores_log.extend(ygs)
        eje.plot(xgs, ygs, marker='s', markersize=4, color=c['gs'], label=f'Gauss-Seidel ({len(xgs)} it.)')
        eje.annotate(f'GS({xgs[-1]}): {formato_visual(ygs[-1])}', (xgs[-1], ygs[-1]),
                     xytext=(0, -14), textcoords='offset points', ha='center', color=c['gs'], fontsize=9)
        if iteracion_seleccionada is not None:
            idx_gs = min(max(iteracion_seleccionada, 0), len(filas_gs) - 1)
            eje.scatter([xgs[idx_gs]], [ygs[idx_gs]], color=c['seleccion'], marker='s', s=65, zorder=5)

    tol = d.get('tolerancia')
    if tol is not None and tol > 0:
        valores_log.append(tol)
        max_x = max([len(filas_j) if visibles.get('jacobi', True) else 0,
                     len(filas_gs) if visibles.get('gauss_seidel', True) else 0, 1])
        eje.hlines(tol, 1, max_x, colors=c['tolerancia'], linestyles='--', linewidth=1.0,
                   label=f'Tolerancia ε = {formato_visual(tol)}')

    _escala_log_segura(eje, valores_log)
    eje.set(
        xlabel='Iteración',
        ylabel='Diferencia máxima entre iteraciones',
        title=f'Comparador · {d.get("comparacion_iteraciones", "")}',
    )
    eje.grid(alpha=0.3)
    if valores_log:
        eje.legend(loc='best', fontsize='small')
    _aplicar_zoom(eje, zoom, 0)
    return figura


def _figura_propagacion(calculo, oscuro, zoom=None):
    """Enfoca alrededor de x y x+Δx mostrando Δx, Δy y aproximación lineal."""
    d = calculo.datos
    c = _colores_tema(oscuro)
    funcion = crear_funcion(d['funcion'])
    x = float(d['x'])
    delta = float(d['delta'])
    x2 = x + delta
    derivada = float(d['derivada'])
    fx = _evaluar_seguro(funcion, x)
    fx2 = _evaluar_seguro(funcion, x2)

    centro = 0.5 * (x + x2)
    radio = max(abs(delta) * 1.6, 0.25)
    xmin, xmax = centro - radio, centro + radio

    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')
    eje = figura.add_subplot(111)
    puntos = [xmin + (xmax - xmin) * i / 300 for i in range(301)]
    valores = [_evaluar_seguro(funcion, p) for p in puntos]
    eje.plot(puntos, valores, color=c['curva'], label='f(x)')

    if math.isfinite(fx):
        y_tan = [fx + derivada * (p - x) for p in puntos]
        eje.plot(puntos, y_tan, linestyle='--', color=c['secundario'], label='Aproximación lineal (tangente)')
        eje.scatter([x], [fx], color=c['raiz'], zorder=5, label=f'x = {formato_visual(x)}')
        if delta != 0 and math.isfinite(fx2):
            eje.scatter([x2], [fx2], color=c['seleccion'], zorder=5, label=f'x+Δx = {formato_visual(x2)}')
            eje.plot([x, x2], [fx, fx], linestyle=':', color=c['tolerancia'], label=f'Δx = {formato_visual(delta)}')
            eje.plot([x2, x2], [fx, fx2], linestyle=':', color=c['seleccion'],
                     label=f'Δy directo = {formato_visual(d["cambio"])} · lineal = {formato_visual(d["estimacion"])}')

    exacto_txt = f' · Ref. racional exacta: {d["cambio_exacto"]}' if d.get('cambio_exacto') is not None else ''
    eje.set(
        xlabel='x',
        ylabel='f(x)',
        title=f'Propagación del error · |error lineal| = {formato_visual(d["error"])}{exacto_txt}',
    )
    eje.grid(alpha=0.3)
    eje.legend(loc='best', fontsize='small')
    _aplicar_zoom(eje, zoom, 0)
    return figura


def _figura_simulacion(calculo, oscuro, visibles=None, zoom=None):
    """Compara error acumulado por redondeo frente a truncamiento con etiquetas finales."""
    d = calculo.datos
    c = _colores_tema(oscuro)
    filas = d.get('filas', ())
    visibles = visibles or {'redondeo': True, 'truncamiento': True}
    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')
    eje = figura.add_subplot(111)

    xs = [f[0] for f in filas]
    yr = [f[4] for f in filas]
    yt = [f[5] for f in filas]

    if xs and visibles.get('redondeo', True):
        eje.plot(xs, yr, marker='.', markersize=4, color=c['jacobi'], label='Error por redondeo (ROUND_HALF_EVEN)')
        eje.annotate(f'Redondeo: {formato_visual(yr[-1])}', (xs[-1], yr[-1]),
                     xytext=(-8, 8), textcoords='offset points', ha='right', color=c['jacobi'], fontsize=9)
    if xs and visibles.get('truncamiento', True):
        eje.plot(xs, yt, marker='s', markersize=3.5, color=c['secundario'], label='Error por truncamiento (ROUND_DOWN)')
        eje.annotate(f'Truncamiento: {formato_visual(yt[-1])}', (xs[-1], yt[-1]),
                     xytext=(-8, -14), textcoords='offset points', ha='right', color=c['secundario'], fontsize=9)

    eje.set(
        xlabel='Iteración',
        ylabel='Error absoluto frente a Decimal (100 cifras)',
        title='Acumulación de error: redondeo frente a truncamiento',
    )
    eje.grid(alpha=0.3)
    if xs:
        eje.legend(loc='best', fontsize='small')
    _aplicar_zoom(eje, zoom, 0)
    return figura


def _figura_sistema(calculo, oscuro, zoom=None):
    """Compara error por variable (x1..xn) entre Float propio y NumPy frente a Fraction."""
    d = calculo.datos
    c = _colores_tema(oscuro)
    filas = d.get('filas', ())
    exacto = d.get('exacto', ())
    n = len(filas)
    etiquetas = [f'x{subindice(i + 1)}' for i in range(n)]
    err_propio = [float(f[4]) for f in filas]
    err_numpy = [
        float(abs(Fraction.from_float(float(f[3])) - exacto[i][0]))
        for i, f in enumerate(filas)
    ]

    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')
    eje = figura.add_subplot(111)
    indices = list(range(n))
    ancho = 0.36
    eje.bar([i - ancho / 2 for i in indices], err_propio, width=ancho, color=c['jacobi'], label='Float propio')
    eje.bar([i + ancho / 2 for i in indices], err_numpy, width=ancho, color=c['gs'], label='NumPy')

    max_err = max(err_propio + err_numpy) if (err_propio or err_numpy) else 0.0
    if max_err > 0:
        idx_max = max(range(n), key=lambda i: max(err_propio[i], err_numpy[i]))
        etq_max = f'Mayor error en {etiquetas[idx_max]}: {formato_visual(max_err)}'
    else:
        etq_max = 'Errores nulos frente a Fraction'

    eje.set_xticks(indices)
    eje.set_xticklabels(etiquetas)
    eje.set(
        xlabel='Variable del sistema',
        ylabel='Error absoluto frente a Fraction',
        title=f'Sistema · {etq_max}\ncond(A)={formato_visual(d.get("condicion"))} · Residuo={formato_visual(d.get("residuo"))}',
    )
    eje.grid(axis='y', alpha=0.3)
    eje.legend(loc='best', fontsize='small')
    _aplicar_zoom(eje, zoom, 0)
    return figura


def _figura_inversa(calculo, oscuro, mostrar_log=False, zoom=None):
    """Construye mapa de calor n×n del error por fila y columna con mayor desviación."""
    d = calculo.datos
    c = _colores_tema(oscuro)
    exacto = d.get('exacto', ())
    filas = d.get('filas', ())
    n = len(exacto)
    matriz_err = [[0.0] * n for _ in range(n)]
    for idx, fila in enumerate(filas):
        i, j = divmod(idx, n)
        matriz_err[i][j] = float(fila[4])

    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')
    eje = figura.add_subplot(111)
    todos = [v for fila in matriz_err for v in fila]
    positivos = [v for v in todos if v > 0]
    norm = LogNorm(vmin=min(positivos), vmax=max(positivos)) if (mostrar_log and positivos and all(v > 0 for v in todos)) else None
    mapa = eje.imshow(matriz_err, cmap='viridis', norm=norm, aspect='equal')
    barra = figura.colorbar(mapa, ax=eje)
    barra.set_label('Error absoluto |Float propio − Exacto|')

    if n > 0:
        i_max, j_max = max(((i, j) for i in range(n) for j in range(n)), key=lambda pos: matriz_err[pos[0]][pos[1]])
        eje.scatter([j_max], [i_max], marker='s', s=220, facecolors='none', edgecolors=c['raiz'], linewidths=2,
                    label=f'Mayor desviación [{i_max + 1},{j_max + 1}]: {formato_visual(matriz_err[i_max][j_max])}')
        eje.legend(loc='upper right', fontsize='small')

    if n <= 6:
        for i in range(n):
            for j in range(n):
                rojo, verde, azul, _ = mapa.cmap(mapa.norm(matriz_err[i][j]))
                luminosidad = .2126 * rojo + .7152 * verde + .0722 * azul
                eje.text(j, i, formato_visual(matriz_err[i][j]), ha='center', va='center',
                         color='#111111' if luminosidad > .55 else 'white', fontsize=8)

    eje.set_xticks(range(n))
    eje.set_xticklabels([str(j + 1) for j in range(n)])
    eje.set_yticks(range(n))
    eje.set_yticklabels([str(i + 1) for i in range(n)])
    eje.set(
        xlabel='Columna',
        ylabel='Fila',
        title=f'Inversa ({n}×{n}) · Error absoluto por celda\ncond(A)={formato_visual(d.get("condicion"))} · Residuo={formato_visual(d.get("residuo"))}',
    )
    _aplicar_zoom(eje, zoom, 0)
    return figura


def figura_numerica(clave, calculo, oscuro=False, **opciones):
    """Construye una figura exportable sin abrir ventanas ni usar pyplot global."""
    if clave == 'num_newton':
        from interfaz.numericos.newton_graficas import figura_newton
        return figura_newton(calculo, crear_funcion(calculo.datos['funcion']),
                             oscuro=oscuro, **opciones)
    if clave == 'num_biseccion':
        return _figura_biseccion(
            calculo, oscuro,
            iteracion_seleccionada=opciones.get('iteracion_seleccionada'),
            zoom=opciones.get('zoom'),
            panel_expandido=opciones.get('panel_expandido'),
        )
    if clave in ('num_jacobi', 'num_gauss_seidel'):
        return _figura_iterativo(
            clave, calculo, oscuro,
            iteracion_seleccionada=opciones.get('iteracion_seleccionada'),
            zoom=opciones.get('zoom'),
        )
    if clave == 'num_comparar_iterativos':
        return _figura_comparar_iterativos(
            calculo, oscuro,
            iteracion_seleccionada=opciones.get('iteracion_seleccionada'),
            visibles=opciones.get('visibles'),
            zoom=opciones.get('zoom'),
        )
    if clave == 'num_propagacion':
        return _figura_propagacion(calculo, oscuro, zoom=opciones.get('zoom'))
    if clave == 'num_simulacion':
        return _figura_simulacion(
            calculo, oscuro,
            visibles=opciones.get('visibles'),
            zoom=opciones.get('zoom'),
        )
    if clave == 'num_sistema':
        return _figura_sistema(calculo, oscuro, zoom=opciones.get('zoom'))
    return _figura_inversa(calculo, oscuro, mostrar_log=bool(opciones.get('mostrar_log', False)),
                            zoom=opciones.get('zoom'))


def datos_grafica_interactiva(clave, calculo, iteracion_seleccionada=None, visibles=None, panel_expandido=None, mostrar_log=False):
    """Prepara estado de controles e inspección de fila/punto para Qt sin lógica en QML."""
    d = calculo.datos
    visibles = visibles or {}
    if clave == 'num_biseccion':
        filas = d.get('filas', ())
        total = len(filas)
        idx = min(max(iteracion_seleccionada or 0, 0), max(total - 1, 0))
        detalle = ''
        if total:
            f = filas[idx]
            err = f[7] if d.get('criterio') == 'porcentual' else f[8]
            detalle = f'It. {f[0]} · [xl, xu]=[{formato_visual(f[1])}, {formato_visual(f[2])}] · xr={formato_visual(f[3])} · Error={formato_visual(err)}'
        return dict(
            activo=True, total=total, indice=idx, detalle=detalle,
            reproducible=total > 0, conPaneles=total > 0, panelExpandido=-1 if panel_expandido is None else panel_expandido,
            series=[], conLog=False, mostrarLog=False,
        )
    if clave in ('num_jacobi', 'num_gauss_seidel'):
        filas = d.get('filas', ())
        total = len(filas)
        idx = min(max(iteracion_seleccionada or 0, 0), max(total - 1, 0))
        detalle = ''
        if total:
            f = filas[idx]
            vec = ', '.join(formato_visual(v) for v in f[1:-1])
            detalle = f'It. {f[0]} · X≈({vec}) · Dif.={formato_visual(f[-1])}'
        return dict(
            activo=True, total=total, indice=idx, detalle=detalle,
            reproducible=total > 0, conPaneles=False, panelExpandido=-1,
            series=[], conLog=False, mostrarLog=False,
        )
    if clave == 'num_comparar_iterativos':
        fj = d['jacobi']['filas']
        fgs = d['gauss_seidel']['filas']
        total = max(len(fj), len(fgs))
        idx = min(max(iteracion_seleccionada or 0, 0), max(total - 1, 0))
        partes = []
        if fj:
            rj = fj[min(idx, len(fj) - 1)]
            fin_j = ' (finalizada)' if idx >= len(fj) else ''
            partes.append(f'Jacobi it.{rj[0]}{fin_j}: dif={formato_visual(rj[-1])}')
        if fgs:
            rgs = fgs[min(idx, len(fgs) - 1)]
            fin_gs = ' (finalizada)' if idx >= len(fgs) else ''
            partes.append(f'GS it.{rgs[0]}{fin_gs}: dif={formato_visual(rgs[-1])}')
        return dict(
            activo=True, total=total, indice=idx, detalle='  |  '.join(partes),
            reproducible=total > 0, conPaneles=False, panelExpandido=-1,
            series=[
                dict(clave='jacobi', etiqueta='Jacobi', activa=visibles.get('jacobi', True)),
                dict(clave='gauss_seidel', etiqueta='Gauss-Seidel', activa=visibles.get('gauss_seidel', True)),
            ],
            conLog=False, mostrarLog=False,
        )
    if clave == 'num_simulacion':
        filas = d.get('filas', ())
        detalle = f'Iteraciones: {len(filas)} · Redondeo: {d.get("redondeado")} · Truncado: {d.get("truncado")}'
        return dict(
            activo=True, total=0, indice=0, detalle=detalle,
            reproducible=False, conPaneles=False, panelExpandido=-1,
            series=[
                dict(clave='redondeo', etiqueta='Redondeo', activa=visibles.get('redondeo', True)),
                dict(clave='truncamiento', etiqueta='Truncamiento', activa=visibles.get('truncamiento', True)),
            ],
            conLog=False, mostrarLog=False,
        )
    if clave == 'num_inversa':
        filas = d.get('filas', ())
        max_f = max(filas, key=lambda f: f[4]) if filas else None
        detalle = (
            f'Mayor desviación {max_f[0]}: Exacto={max_f[1]} · Float={formato(max_f[2])} · NumPy={formato(max_f[3])}'
            if max_f else ''
        )
        return dict(
            activo=True, total=0, indice=0, detalle=detalle,
            reproducible=False, conPaneles=False, panelExpandido=-1,
            series=[], conLog=True, mostrarLog=bool(mostrar_log),
        )
    return dict(
        activo=clave in ('num_propagacion', 'num_sistema'),
        total=0, indice=0, detalle='',
        reproducible=False, conPaneles=False, panelExpandido=-1,
        series=[], conLog=False, mostrarLog=False,
    )
