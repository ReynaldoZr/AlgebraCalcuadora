"""Resuelve sistemas por Jacobi y Gauss-Seidel con reordenamiento y comparación.

Tema: Programa 8, aproximaciones sucesivas, dominancia diagonal y relajación.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import math

from modulos.numericos.funciones import formato, numero_finito
from modulos.procedimientos import Calculo, Paso


def vector_numerico(vector, dimension, nombre):
    """Convierte un vector de la dimensión indicada a una lista independiente de float."""
    if not isinstance(vector, (list, tuple)) or len(vector) != dimension:
        raise ValueError(f'{nombre} debe tener {dimension} componentes.')
    return [numero_finito(v, f'{nombre}[{i + 1}]') for i, v in enumerate(vector)]


def validar_datos_iterativos(matriz, vector_b, inicial, tolerancia, max_iteraciones,
                             permitir_diagonal_cero=False):
    """Devuelve copias numéricas de A, B, X₀ y tolerancia tras validar sus condiciones."""
    if not isinstance(matriz, (list, tuple)) or not matriz:
        raise ValueError('A debe ser una matriz cuadrada no vacía.')
    orden = len(matriz)
    a = [vector_numerico(fila, orden, f'Fila {i + 1} de A')
         for i, fila in enumerate(matriz)]
    b = vector_numerico(vector_b, orden, 'B')
    x = vector_numerico(inicial, orden, 'X₀')
    tolerancia = numero_finito(tolerancia, 'Tolerancia')
    if tolerancia <= 0:
        raise ValueError('La tolerancia debe ser positiva.')
    if type(max_iteraciones) is not int or not 1 <= max_iteraciones <= 10000:
        raise ValueError('El máximo debe ser un entero entre 1 y 10000.')
    if not permitir_diagonal_cero and any(fila[i] == 0 for i, fila in enumerate(a)):
        raise ValueError('La diagonal contiene un cero. Reordena las ecuaciones antes de iterar.')
    return a, b, x, tolerancia


def validar_relajacion(relajacion):
    """Valida el factor de relajación λ en el intervalo abierto (0, 2)."""
    valor = numero_finito(relajacion, 'Relajación λ')
    if not 0 < valor < 2:
        raise ValueError('El factor de relajación λ debe cumplir 0 < λ < 2.')
    return valor


def _margen_dominancia_fila(fila, columna):
    """Devuelve si la fila domina estrictamente en la columna y su margen relativo."""
    escala = max(abs(v) for v in fila)
    if not escala or fila[columna] == 0:
        return False, 0.0
    diag = abs(fila[columna]) / escala
    suma = math.fsum(abs(v) / escala for j, v in enumerate(fila) if j != columna)
    return diag > suma, diag - suma


def dominancia_diagonal(matriz):
    """Indica por fila si la diagonal domina estrictamente a los demás coeficientes."""
    # Escalar cada fila evita desbordar la suma de magnitudes grandes.
    return tuple(_margen_dominancia_fila(fila, i)[0] for i, fila in enumerate(matriz))


def _buscar_permutacion_optima(a):
    """Busca la mejor permutación sin ceros en la diagonal, priorizando dominancia."""
    orden = len(a)
    candidatos = [
        [r for r in range(orden) if a[r][col] != 0]
        for col in range(orden)
    ]
    if any(not c for c in candidatos):
        return None
    if orden <= 9:
        mejor = None
        usadas = [False] * orden
        actual = [0] * orden
        columnas = sorted(range(orden), key=lambda c: len(candidatos[c]))

        def explorar(pos, doms, cambios, margen):
            """Explora permutaciones válidas con poda por dominancia máxima posible."""
            nonlocal mejor
            if mejor is not None and doms + (orden - pos) < mejor[0]:
                return
            if pos == orden:
                puntaje = (doms, -cambios, margen)
                if mejor is None or puntaje > mejor[:3]:
                    mejor = (*puntaje, tuple(actual))
                return
            col = columnas[pos]
            for fila in sorted(candidatos[col],
                               key=lambda r: _margen_dominancia_fila(a[r], col),
                               reverse=True):
                if usadas[fila]:
                    continue
                usadas[fila] = True
                actual[col] = fila
                es_dom, dif = _margen_dominancia_fila(a[fila], col)
                explorar(pos + 1, doms + int(es_dom), cambios + int(fila != col), margen + dif)
                usadas[fila] = False

        explorar(0, 0, 0, 0.0)
        return mejor[3] if mejor is not None else None

    # Respaldo voraz con búsqueda de camino aumentante para sistemas grandes.
    asignacion = [-1] * orden

    def emparejar(col, visitado):
        """Asigna una fila con coeficiente no nulo a la columna mediante camino aumentante."""
        for fila in sorted(candidatos[col], key=lambda r: _margen_dominancia_fila(a[r], col), reverse=True):
            if visitado[fila]:
                continue
            visitado[fila] = True
            if asignacion[fila] == -1 or emparejar(asignacion[fila], visitado):
                asignacion[fila] = col
                return True
        return False

    for col in sorted(range(orden), key=lambda c: len(candidatos[c])):
        if not emparejar(col, [False] * orden):
            return None
    perm = [0] * orden
    for fila, col in enumerate(asignacion):
        perm[col] = fila
    return tuple(perm)


def reordenar_ecuaciones(matriz, vector_b):
    """Reordena filas de A y B juntos buscando dominancia estricta y diagonal no nula."""
    if not isinstance(matriz, (list, tuple)) or not matriz:
        raise ValueError('A debe ser una matriz cuadrada no vacía.')
    orden = len(matriz)
    a = [vector_numerico(fila, orden, f'Fila {i + 1} de A') for i, fila in enumerate(matriz)]
    b = vector_numerico(vector_b, orden, 'B')
    identidad_perm = tuple(range(orden))
    if all(dominancia_diagonal(a)):
        return a, b, identidad_perm, False
    perm = _buscar_permutacion_optima(a)
    if perm is None:
        raise ValueError(
            'No es posible eliminar los ceros de la diagonal intercambiando ecuaciones.'
        )
    a_reord = [a[idx][:] for idx in perm]
    b_reord = [b[idx] for idx in perm]
    return a_reord, b_reord, perm, perm != identidad_perm


def residuo_sistema(matriz, vector_b, vector_x):
    """Devuelve la norma máxima de Ax−b, o None si su evaluación desborda."""
    try:
        diferencias = [abs(math.fsum([v * vector_x[j] for j, v in enumerate(fila)] + [-b]))
                       for fila, b in zip(matriz, vector_b)]
        residuo = max(diferencias)
        return residuo if math.isfinite(residuo) else None
    except (OverflowError, ValueError):
        return None


def _preparar_sistema(matriz, vector_b, inicial, tolerancia, max_iteraciones, reordenar):
    """Valida entradas y aplica reordenamiento opcional conservando A y B originales."""
    a_orig, b_orig, x_ini, tol = validar_datos_iterativos(
        matriz, vector_b, inicial, tolerancia, max_iteraciones,
        permitir_diagonal_cero=reordenar,
    )
    if reordenar:
        a_trab, b_trab, perm, reordenado = reordenar_ecuaciones(a_orig, b_orig)
    else:
        a_trab, b_trab = [f[:] for f in a_orig], b_orig[:]
        perm, reordenado = tuple(range(len(a_orig))), False
    return a_orig, b_orig, a_trab, b_trab, x_ini, tol, perm, reordenado


def _ejecutar_iterativo(metodo, a_orig, b_orig, a_trab, b_trab, x_ini, tolerancia,
                        max_iteraciones, perm, reordenado, relajacion=1.0):
    """Ejecuta el ciclo común de Jacobi o Gauss-Seidel sobre el sistema preparado."""
    x = x_ini[:]
    dominantes = dominancia_diagonal(a_trab)
    orden_ecuaciones = tuple(i + 1 for i in perm)
    aviso = ('La diagonal es estrictamente dominante y garantiza convergencia.'
             if all(dominantes) else
             'Falta dominancia diagonal estricta. La convergencia no está garantizada.')
    if reordenado:
        aviso = f'Ecuaciones reordenadas (orden aplicado: {list(orden_ecuaciones)}). ' + aviso
    datos = dict(
        metodo=metodo, matriz=a_orig, vector_b=b_orig, inicial=x_ini[:],
        tolerancia=tolerancia, max_iteraciones=max_iteraciones,
        dominantes=dominantes, reordenado=reordenado,
        orden_ecuaciones=orden_ecuaciones, relajacion=relajacion,
        convergio=False, filas=[], error=None, advertencias=[],
        columnas=('k',) + tuple(f'x{i + 1}' for i in range(len(x))) + ('Error máximo',),
        motivo='Se alcanzó el máximo de iteraciones sin cumplir la tolerancia.',
    )
    filas_datos = tuple(
        (f'Fila {i + 1}: [{", ".join(formato(v) for v in fila)}] | b={formato(b_trab[i])}',)
        for i, fila in enumerate(a_trab)
    )
    extras = (f'X₀={x}', f'Tolerancia={formato(tolerancia)}')
    if metodo == 'Gauss-Seidel' and relajacion != 1.0:
        extras += (f'λ={formato(relajacion)}',)
    pasos = [Paso(f'Datos de {metodo}', aviso, formulas=filas_datos + (extras,))]
    es_gs = metodo == 'Gauss-Seidel'
    detalle_iter = ('Calculamos cada componente usando de inmediato los valores recién obtenidos.'
                    if es_gs else 'Calculamos cada componente con el vector anterior.')

    for k in range(1, max_iteraciones + 1):
        try:
            if es_gs:
                nuevo = x[:]
                for i, fila in enumerate(a_trab):
                    gs = (b_trab[i] - math.fsum(v * nuevo[j] for j, v in enumerate(fila) if j != i)) / fila[i]
                    nuevo[i] = gs if relajacion == 1.0 else relajacion * gs + (1.0 - relajacion) * x[i]
            else:
                nuevo = [(b_trab[i] - math.fsum(v * x[j] for j, v in enumerate(fila) if j != i)) / fila[i]
                         for i, fila in enumerate(a_trab)]
            error = max(abs(v - anterior) for v, anterior in zip(nuevo, x))
            if not all(math.isfinite(v) for v in nuevo) or not math.isfinite(error):
                raise OverflowError
        except (OverflowError, ValueError):
            datos['motivo'] = 'La iteración produjo valores no finitos. Se conserva el último vector finito.'
            break
        crece = datos['error'] is not None and error > datos['error']
        if crece and not datos['advertencias']:
            datos['advertencias'].append(
                f'El error creció en la iteración {k}. Hay posible falta de convergencia.'
            )
        datos['filas'].append((k, *nuevo, error))
        datos['error'] = error
        pasos.append(Paso(
            f'Iteración {k} de {metodo}',
            'El error creció respecto a la iteración anterior.' if crece else detalle_iter,
            formulas=tuple((f'x{i + 1}={formato(v)}',) for i, v in enumerate(nuevo))
            + ((f'Error máximo={formato(error)}',),),
        ))
        x = nuevo
        if error <= tolerancia:
            datos.update(convergio=True, motivo='La diferencia máxima es menor o igual que la tolerancia.')
            break

    datos['residuo'] = residuo_sistema(a_orig, b_orig, x)
    if datos['residuo'] is None:
        datos['advertencias'].append('No se pudo evaluar el residuo con valores finitos.')
    pasos.append(Paso(
        f'Terminación de {metodo}', ' '.join([datos['motivo']] + datos['advertencias']),
        formulas=((f'X={x}',), (f'Residuo ||Ax−b||∞={formato(datos["residuo"])}',)),
    ))
    return Calculo(x[:], tuple(pasos), datos)


def jacobi(matriz, vector_b, inicial, tolerancia=0.0001, max_iteraciones=200, reordenar=False):
    """Devuelve Calculo con el último vector, pasos y tabla usando actualización simultánea."""
    a_orig, b_orig, a_trab, b_trab, x_ini, tol, perm, reordenado = _preparar_sistema(
        matriz, vector_b, inicial, tolerancia, max_iteraciones, reordenar,
    )
    return _ejecutar_iterativo(
        'Jacobi', a_orig, b_orig, a_trab, b_trab, x_ini, tol, max_iteraciones, perm, reordenado,
    )


def gauss_seidel(matriz, vector_b, inicial, tolerancia=0.0001, max_iteraciones=200,
                 reordenar=False, relajacion=1.0):
    """Devuelve Calculo con el último vector, pasos y tabla usando actualización inmediata."""
    lam = validar_relajacion(relajacion)
    a_orig, b_orig, a_trab, b_trab, x_ini, tol, perm, reordenado = _preparar_sistema(
        matriz, vector_b, inicial, tolerancia, max_iteraciones, reordenar,
    )
    return _ejecutar_iterativo(
        'Gauss-Seidel', a_orig, b_orig, a_trab, b_trab, x_ini, tol, max_iteraciones,
        perm, reordenado, relajacion=lam,
    )


def comparar_iterativos(matriz, vector_b, inicial, tolerancia=0.0001, max_iteraciones=200,
                        reordenar=True, relajacion=1.0):
    """Ejecuta Jacobi y Gauss-Seidel con los mismos datos y conserva ambas tablas completas."""
    res_j = jacobi(matriz, vector_b, inicial, tolerancia, max_iteraciones, reordenar=reordenar)
    res_gs = gauss_seidel(
        matriz, vector_b, inicial, tolerancia, max_iteraciones,
        reordenar=reordenar, relajacion=relajacion,
    )
    dj, dgs = res_j.datos, res_gs.datos
    diferencia_metodos = max(abs(vj - vg) for vj, vg in zip(res_j.valor, res_gs.valor))
    it_j, it_gs = len(dj['filas']), len(dgs['filas'])
    if dj['convergio'] and dgs['convergio']:
        if it_gs < it_j:
            comparacion = f'Gauss-Seidel necesitó menos iteraciones ({it_gs} frente a {it_j} de Jacobi).'
        elif it_j < it_gs:
            comparacion = f'Jacobi necesitó menos iteraciones ({it_j} frente a {it_gs} de Gauss-Seidel).'
        else:
            comparacion = f'Ambos métodos convergieron en {it_j} iteraciones.'
    elif dgs['convergio']:
        comparacion = f'Gauss-Seidel convergió en {it_gs} iteraciones; Jacobi no cumplió la tolerancia.'
    elif dj['convergio']:
        comparacion = f'Jacobi convergió en {it_j} iteraciones; Gauss-Seidel no cumplió la tolerancia.'
    else:
        comparacion = 'Ninguno de los dos métodos alcanzó la tolerancia dentro del máximo indicado.'

    columnas = ('Método',) + dj['columnas']
    filas = [('Jacobi', *fila) for fila in dj['filas']] + [
        ('Gauss-Seidel', *fila) for fila in dgs['filas']
    ]
    datos = dict(
        metodo='Comparación Jacobi vs Gauss-Seidel',
        matriz=dj['matriz'], vector_b=dj['vector_b'], inicial=dj['inicial'],
        tolerancia=dj['tolerancia'], max_iteraciones=max_iteraciones,
        dominantes=dj['dominantes'], reordenado=dj['reordenado'],
        orden_ecuaciones=dj['orden_ecuaciones'],
        jacobi=dj, gauss_seidel=dgs,
        valor_jacobi=res_j.valor[:], valor_gauss_seidel=res_gs.valor[:],
        diferencia_metodos=diferencia_metodos,
        comparacion_iteraciones=comparacion,
        convergio=dj['convergio'] or dgs['convergio'],
        residuo=dgs['residuo'],
        columnas=columnas, filas=filas,
    )
    paso_comp = Paso(
        'Comparación Jacobi vs Gauss-Seidel', comparacion,
        formulas=(
            (f'Jacobi ({it_j} it.): X={res_j.valor}', f'Residuo={formato(dj["residuo"])}'),
            (f'Gauss-Seidel ({it_gs} it.): X={res_gs.valor}', f'Residuo={formato(dgs["residuo"])}'),
            (f'Diferencia máxima entre métodos={formato(diferencia_metodos)}',),
        ),
    )
    pasos = res_j.pasos + res_gs.pasos + (paso_comp,)
    return Calculo(res_gs.valor[:], pasos, datos)
