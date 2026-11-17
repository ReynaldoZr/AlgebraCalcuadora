"""Describe formularios y adapta la unidad numérica a consola y escritorio.

Tema: semana 12, con imports de algoritmos bajo demanda y ejemplos conocidos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MetodoNumerico:
    """Define nombre, campos de las dos tarjetas y matrices originales necesarias."""

    nombre: str
    campos_a: tuple
    campos_b: tuple
    matrices: tuple = ()


CAMPOS = {
    'funcion': ('f(x)', 'x^4-5*x^3+0.5*x^2-11*x+10'), 'a': ('Extremo a', '0.55'), 'b': ('Extremo b', '1.1'),
    'tolerancia': ('Tolerancia en x o %', '0.0001'), 'tolerancia_f': ('Tolerancia |f(xr)|', '0.0001'),
    'maximo': ('Máximo de iteraciones', '200'), 'criterio': ('Criterio de error', 'intervalo'),
    'verdadero': ('Valor verdadero', '250'), 'aproximado': ('Valor aproximado', '248.5'),
    'x': ('Punto x', '2.5'), 'delta': ('Incertidumbre Δx', '0.01'), 'h': ('Paso derivada (vacío=auto)', ''),
    'capital': ('Capital inicial', '1000'), 'tasa': ('Tasa por iteración', '0.005'),
    'iteraciones': ('Iteraciones', '50'), 'decimales': ('Decimales conservados', '2'),
    'numero': ('Número decimal', '0.1'), 'base': ('Base (2 o 10)', '2'), 'cifras': ('Cifras fraccionarias', '16'),
    'vector_b': ('Vector b · valores separados por comas', '7, -21, 15'),
    'inicial': ('Vector inicial X₀ · separado por comas', '0, 0, 0'),
    'epsilon': ('Tolerancia ε · decimal', '0.0001'),
    'relajacion': ('Relajación λ (0 < λ < 2)', '1'),
    'reordenar': ('Reordenar ecuaciones', 'si'),
}
METODOS_NUMERICOS = {
    'num_biseccion': MetodoNumerico('Bisección y contraste con SciPy', ('funcion', 'a', 'b'), ('criterio', 'tolerancia', 'tolerancia_f', 'maximo')),
    'num_errores': MetodoNumerico('Error absoluto, relativo y porcentual', ('verdadero', 'aproximado'), ()),
    'num_propagacion': MetodoNumerico('Propagación del error', ('funcion', 'x', 'delta'), ('h',)),
    'num_simulacion': MetodoNumerico('Truncamiento frente a redondeo', ('capital', 'tasa'), ('iteraciones', 'decimales')),
    'num_flotante': MetodoNumerico('Punto flotante: épsilon, overflow y underflow', (), ()),
    'num_inestabilidad': MetodoNumerico('Estabilidad: expresión directa y reformulada', ('x',), ()),
    'num_bases': MetodoNumerico('Representación en base 2 y base 10', ('numero',), ('base', 'cifras')),
    'num_inversa': MetodoNumerico('Inversa: Fraction, float propio y NumPy', (), (), ('A',)),
    'num_sistema': MetodoNumerico('Sistema: Fraction, float propio y NumPy', (), (), ('A', 'b')),
    'num_jacobi': MetodoNumerico('Jacobi · sistemas iterativos', (), ('vector_b', 'inicial', 'epsilon', 'maximo', 'reordenar'), ('A',)),
    'num_gauss_seidel': MetodoNumerico('Gauss-Seidel · sistemas iterativos', (), ('vector_b', 'inicial', 'epsilon', 'maximo', 'relajacion', 'reordenar'), ('A',)),
    'num_comparar_iterativos': MetodoNumerico('Comparar Jacobi y Gauss-Seidel', (), ('vector_b', 'inicial', 'epsilon', 'maximo', 'reordenar'), ('A',)),
}


def parametros_defecto(clave):
    """Devuelve una copia de valores iniciales pertinente a cada método."""
    datos = {k: v[1] for k, v in CAMPOS.items()}
    if clave == 'num_jacobi':
        datos['reordenar'] = 'no'
    if clave == 'num_propagacion':
        datos['funcion'] = 'x^3'
    if clave == 'num_inestabilidad':
        datos['x'] = '1e16'
    return datos


def parametros_vacios(clave):
    """Mantiene ajustes de cálculo, pero deja sin llenar los datos del ejercicio."""
    datos = parametros_defecto(clave)
    # Tolerancias y límites son ajustes; función, extremos y cantidades son el ejercicio.
    for nombre in ('funcion', 'a', 'b', 'verdadero', 'aproximado', 'x', 'delta', 'capital', 'tasa', 'numero', 'vector_b', 'inicial'):
        datos[nombre] = ''
    return datos


def entero(texto, nombre):
    """Convierte exclusivamente texto entero, con diagnóstico del campo afectado."""
    try:
        return int(texto)
    except (ValueError, TypeError):
        raise ValueError(f'{nombre} debe ser un entero.') from None


def leer_vector_numerico(texto, nombre):
    """Convierte un vector escrito con comas y conserva las fracciones de entrada."""
    from interfaz.datos import convertir_numero
    try:
        return [convertir_numero(v.strip()) for v in texto.split(',')]
    except (ValueError, ZeroDivisionError):
        raise ValueError(f'{nombre}: separa los números con comas. Ejemplo: 0, 0, 0.') from None


def ejemplo_jacobi(caso):
    """Devuelve A y parámetros del caso de práctica solicitado explícitamente."""
    if caso == 'Reordenar 2×2':
        return [[1, 5], [7, 1]], dict(vector_b='11, 15', inicial='0, 0', maximo='200', reordenar='si')
    if caso == 'Sin convergencia':
        return [[1, 5], [7, 1]], dict(vector_b='11, 15', inicial='0, 0', maximo='20', reordenar='no')
    if caso == 'Diagonal con cero':
        return [[0, 2], [3, 1]], dict(vector_b='4, 5', inicial='0, 0', maximo='200', reordenar='si')
    return [[4, -1, 1], [4, -8, 1], [-2, 1, 5]], dict(vector_b='7, -21, 15', inicial='0, 0, 0', maximo='200', reordenar='si')


def _opcion_reordenar(valor):
    """Interpreta la opción textual de reordenamiento para consola y formularios."""
    texto = str(valor).strip().lower()
    if texto in ('si', 'sí', 'true', '1'):
        return True
    if texto in ('no', 'false', '0'):
        return False
    raise ValueError('Reordenar ecuaciones debe ser "si" o "no".')


def ejecutar_numerico(clave, parametros, matrices=None):
    """Llama al núcleo de la semana 12; no requiere dependencias al iniciar otros temas."""
    from modulos.numericos.errores import calcular_errores, descomponer, inestabilidad, propagacion, punto_flotante, simulacion
    matrices = matrices or {}
    p = parametros
    if clave in ('num_jacobi', 'num_gauss_seidel', 'num_comparar_iterativos'):
        from modulos.numericos.iterativos import comparar_iterativos, gauss_seidel, jacobi
        from modulos.numericos.comparadores import verificar_iterativo
        b_vec = leer_vector_numerico(p['vector_b'], 'b')
        x0_vec = leer_vector_numerico(p['inicial'], 'X₀')
        maximo = entero(p['maximo'], 'Máximo')
        reordenar = _opcion_reordenar(p.get('reordenar', 'si'))
        if clave == 'num_jacobi':
            calculo = jacobi(matrices['A'], b_vec, x0_vec, p['epsilon'], maximo,
                             reordenar=reordenar)
        elif clave == 'num_gauss_seidel':
            calculo = gauss_seidel(
                matrices['A'], b_vec, x0_vec, p['epsilon'], maximo,
                reordenar=reordenar, relajacion=p.get('relajacion', '1') or '1',
            )
        else:
            calculo = comparar_iterativos(
                matrices['A'], b_vec, x0_vec, p['epsilon'], maximo, reordenar=reordenar,
            )
        return verificar_iterativo(calculo)
    if clave == 'num_biseccion':
        from modulos.numericos.biseccion import biseccion
        return biseccion(p['funcion'], p['a'], p['b'], p['tolerancia'], entero(p['maximo'], 'Máximo'), p['criterio'], p['tolerancia_f'])
    if clave == 'num_errores':
        return calcular_errores(p['verdadero'], p['aproximado'])
    if clave == 'num_propagacion':
        return propagacion(p['funcion'], p['x'], p['delta'], p['h'] or None)
    if clave == 'num_simulacion':
        return simulacion(p['capital'], p['tasa'], entero(p['iteraciones'], 'Iteraciones'), entero(p['decimales'], 'Decimales'))
    if clave == 'num_flotante':
        return punto_flotante()
    if clave == 'num_inestabilidad':
        return inestabilidad(p['x'])
    if clave == 'num_bases':
        return descomponer(p['numero'], entero(p['base'], 'Base'), entero(p['cifras'], 'Cifras'))
    if clave in ('num_inversa', 'num_sistema'):
        from modulos.numericos.comparadores import comparar
        b = None
        if clave == 'num_sistema':
            if len(matrices['b'][0]) != 1:
                raise ValueError('b debe ser una columna m×1.')
            b = [f[0] for f in matrices['b']]
        return comparar(matrices['A'], b)
    raise ValueError('Método numérico no disponible.')


def subindice(numero):
    """Convierte un entero positivo en subíndice Unicode para etiquetar variables."""
    tabla = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
    return str(numero).translate(tabla)


def formato_visual(valor):
    """Redondea solo para mostrar; usa notación científica en magnitudes pequeñas o grandes."""
    if valor is None:
        return 'No definido'
    numero = float(valor)
    if numero == 0:
        return '0'
    magnitud = abs(numero)
    if magnitud < 1e-4 or magnitud >= 1e6:
        return f'{numero:.4e}'
    return f'{numero:.4f}'


def _resumen_metodo_iterativo(nombre, datos, diferencia_ref=None):
    """Prepara métricas breves y completas de un método iterativo sin recalcular."""
    from modulos.numericos.funciones import formato
    convergio = bool(datos['convergio'])
    return dict(
        nombre=nombre,
        convergio=convergio,
        iteraciones=len(datos['filas']),
        estado='Alcanzó la tolerancia' if convergio else 'No alcanzó la tolerancia',
        residuo_corto=formato_visual(datos['residuo']),
        residuo_completo=formato(datos['residuo']),
        error_corto=formato_visual(datos['error']),
        error_completo=formato(datos['error']),
        motivo=datos['motivo'],
        diferencia_ref_completa=formato(diferencia_ref) if diferencia_ref is not None else None,
        advertencias=list(datos.get('advertencias', ())),
    )


def resumen_iterativo_estructurado(clave, calculo):
    """Estructura aproximaciones, referencia y detalles técnicos para la tarjeta de resultados."""
    from modulos.numericos.funciones import formato
    if clave not in ('num_comparar_iterativos', 'num_jacobi', 'num_gauss_seidel'):
        return dict(activo=False)
    d = calculo.datos
    es_comparacion = clave == 'num_comparar_iterativos'
    ref = d.get('referencia')
    ref_disponible = ref is not None
    advertencias = []
    if es_comparacion:
        dj, dgs = d['jacobi'], d['gauss_seidel']
        vj_vec, vgs_vec = d['valor_jacobi'], d['valor_gauss_seidel']
        metodos = [
            _resumen_metodo_iterativo('Jacobi', dj, d.get('diferencia_referencia_jacobi')),
            _resumen_metodo_iterativo('Gauss-Seidel', dgs, d.get('diferencia_referencia_gauss_seidel')),
        ]
        if dj['convergio'] and dgs['convergio']:
            estado_general = 'Ambos métodos alcanzaron la tolerancia.'
            comparacion = d['comparacion_iteraciones']
        elif dj['convergio'] or dgs['convergio']:
            estado_general = d['comparacion_iteraciones']
            comparacion = ''
        else:
            estado_general = 'Ninguno de los dos métodos alcanzó la tolerancia.'
            comparacion = ''
            advertencias.append('Ninguno alcanzó la tolerancia solicitada; revisa el motivo de parada.')
        columnas = ['Variable', 'Jacobi ≈', 'Gauss-Seidel ≈', 'Referencia para comparar']
        filas = [
            [
                f'x{subindice(i + 1)}',
                formato_visual(vj_vec[i]),
                formato_visual(vgs_vec[i]),
                formato_visual(ref[i]) if ref_disponible else 'No disponible',
            ]
            for i in range(len(vj_vec))
        ]
        advertencias.extend(dj.get('advertencias', ()))
        advertencias.extend(dgs.get('advertencias', ()))
    else:
        nombre = d.get('metodo', 'Jacobi' if clave == 'num_jacobi' else 'Gauss-Seidel')
        vec = calculo.valor
        metodos = [_resumen_metodo_iterativo(nombre, d, d.get('diferencia_referencia'))]
        estado_general = (
            f'{nombre} alcanzó la tolerancia.'
            if d['convergio']
            else f'{nombre} no alcanzó la tolerancia.'
        )
        comparacion = ''
        if not d['convergio']:
            advertencias.append(f'{nombre} no alcanzó la tolerancia: {d["motivo"]}')
        columnas = ['Variable', f'{nombre} ≈', 'Referencia para comparar']
        filas = [
            [
                f'x{subindice(i + 1)}',
                formato_visual(vec[i]),
                formato_visual(ref[i]) if ref_disponible else 'No disponible',
            ]
            for i in range(len(vec))
        ]
        advertencias.extend(d.get('advertencias', ()))

    if not ref_disponible:
        advertencias.append(f'Referencia para comparar no disponible: {d.get("error_referencia", "error numérico")}')

    orden_txt = f'Reordenadas ({list(d["orden_ecuaciones"])})' if d.get('reordenado') else 'Original'
    dominancia_txt = 'Sí' if all(d['dominantes']) else 'Sin garantía'
    detalles = [
        dict(titulo='Tolerancia ε', valor=formato(d['tolerancia'])),
        dict(titulo='Orden de ecuaciones', valor=orden_txt),
        dict(titulo='Diagonal dominante', valor=dominancia_txt),
    ]
    if clave == 'num_gauss_seidel':
        detalles.append(dict(titulo='Relajación λ', valor=formato(d['relajacion'])))
    for m in metodos:
        detalles.append(dict(titulo=f'Cambio final ({m["nombre"]})', valor=m['error_completo']))
        detalles.append(dict(titulo=f'Residuo ‖Ax − b‖∞ ({m["nombre"]})', valor=m['residuo_completo']))
        detalles.append(dict(titulo=f'Parada ({m["nombre"]})', valor=m['motivo']))
        if m['diferencia_ref_completa'] is not None:
            detalles.append(dict(titulo=f'Diferencia máx. con referencia ({m["nombre"]})', valor=m['diferencia_ref_completa']))
    if es_comparacion:
        detalles.append(dict(titulo='Diferencia máx. entre métodos', valor=formato(d['diferencia_metodos'])))
        detalles.append(dict(titulo='Vector completo Jacobi', valor='(' + ', '.join(formato(v) for v in d['valor_jacobi']) + ')'))
        detalles.append(dict(titulo='Vector completo Gauss-Seidel', valor='(' + ', '.join(formato(v) for v in d['valor_gauss_seidel']) + ')'))
    else:
        detalles.append(dict(titulo='Vector completo', valor='(' + ', '.join(formato(v) for v in calculo.valor) + ')'))
    detalles.append(dict(
        titulo='Referencia para comparar (NumPy)',
        valor='(' + ', '.join(formato(v) for v in ref) + ')' if ref_disponible else d.get('error_referencia', 'No disponible'),
    ))

    return dict(
        activo=True,
        es_comparacion=es_comparacion,
        estado_general=estado_general,
        comparacion_iteraciones=comparacion,
        metodos=metodos,
        columnas=columnas,
        filas=filas,
        referencia_disponible=ref_disponible,
        nota_referencia=(
            'Referencia para comparar (NumPy): aproximación independiente para contraste; no es una solución exacta.'
            if ref_disponible
            else f'Referencia para comparar no disponible: {d.get("error_referencia", "")}'
        ),
        nota_precision='Valores redondeados solo para mostrar; cálculos, tablas y guardados conservan la precisión completa.',
        explicacion_residuo='El residuo ‖Ax − b‖∞ comprueba cuánto falta para satisfacer las ecuaciones. Es distinto al cambio entre iteraciones y a la diferencia con la referencia.',
        advertencias=list(dict.fromkeys(advertencias)),
        detalles_tecnicos=detalles,
    )


def resumen_numerico(clave, calculo):
    """Explica los resultados y límites de precisión con nombres de sus magnitudes."""
    from modulos.numericos.funciones import formato
    d = calculo.datos
    if clave in ('num_jacobi', 'num_gauss_seidel'):
        vector = ', '.join(formato(v) for v in calculo.valor)
        referencia = ', '.join(formato(v) for v in d['referencia']) if d['referencia'] is not None else d['error_referencia']
        orden_txt = f'Reordenadas ({list(d["orden_ecuaciones"])})' if d.get('reordenado') else 'Original'
        relajacion_txt = ''
        if clave == 'num_gauss_seidel':
            relajacion_txt = f'Relajación λ: {formato(d["relajacion"])}'
            relajacion_txt += (' · Gauss-Seidel sin relajación.\n' if d['relajacion'] == 1 else
                              ' · No garantiza convergencia para cualquier λ; revisar el residuo.\n')
        return (f'{d["metodo"]} · X ≈ ({vector})\n{d["motivo"]}\n'
                f'{relajacion_txt}'
                f'Iteraciones: {len(d["filas"])} · Cambio entre iteraciones: {formato(d["error"])}\n'
                f'Residuo ‖Ax − b‖∞: {formato(d["residuo"])}\n'
                f'Orden de ecuaciones: {orden_txt} · Diagonal dominante: {"Sí" if all(d["dominantes"]) else "Sin garantía"}\n'
                f'Referencia para comparar (Referencia NumPy): {referencia}\nDiferencia frente a la referencia: {formato(d["diferencia_referencia"])}\n'
                + '\n'.join(d['advertencias']))
    if clave == 'num_comparar_iterativos':
        dj, dgs = d['jacobi'], d['gauss_seidel']
        vec_j = ', '.join(formato(v) for v in d['valor_jacobi'])
        vec_gs = ', '.join(formato(v) for v in d['valor_gauss_seidel'])
        referencia = ', '.join(formato(v) for v in d['referencia']) if d['referencia'] is not None else d['error_referencia']
        orden_txt = f'Reordenadas ({list(d["orden_ecuaciones"])})' if d.get('reordenado') else 'Original'
        avisos = dj['advertencias'] + dgs['advertencias']
        return (f'{d["comparacion_iteraciones"]}\n'
                f'Orden de ecuaciones: {orden_txt} · Diagonal dominante: {"Sí" if all(d["dominantes"]) else "Sin garantía"}\n'
                f'Jacobi ({len(dj["filas"])} it., {"convergió" if dj["convergio"] else "sin converger"}): X ≈ ({vec_j}) · Cambio: {formato(dj["error"])} · Residuo: {formato(dj["residuo"])}\n'
                f'Parada Jacobi: {dj["motivo"]}\n'
                f'Gauss-Seidel ({len(dgs["filas"])} it., {"convergió" if dgs["convergio"] else "sin converger"}): X ≈ ({vec_gs}) · Cambio: {formato(dgs["error"])} · Residuo: {formato(dgs["residuo"])}\n'
                f'Parada Gauss-Seidel: {dgs["motivo"]}\n'
                f'Diferencia entre métodos: {formato(d["diferencia_metodos"])}\n'
                f'Referencia para comparar (Referencia NumPy): {referencia} · Dif. Jacobi: {formato(d["diferencia_referencia_jacobi"])} · Dif. Gauss-Seidel: {formato(d["diferencia_referencia_gauss_seidel"])}\n'
                + '\n'.join(dict.fromkeys(avisos)))
    if clave == 'num_biseccion':
        raices = d.get('raices_extremos', ())
        titulo = (f'Raíces en los extremos: {", ".join(formato(x) for x in raices)}\n'
                  f'Valor principal para guardar: {formato(calculo.valor)}'
                  if len(raices) > 1 else f'Raíz aproximada: {formato(calculo.valor)}')
        return (f'{titulo}\n{d["motivo"]}\n'
                f'Iteraciones realizadas: {len(d["filas"])} · Predicción por ancho: {d["iteraciones_predichas"]}\n'
                f'Residuo |f(xr)|: {formato(d["residuo"])}\nSciPy: {formato(d.get("scipy"))}\nDiferencia con SciPy: {formato(d.get("diferencia_scipy"))}')
    if clave == 'num_errores':
        return f'Error absoluto: {formato(d["absoluto"])}\nError relativo: {formato(d["relativo"])}\nError porcentual: {formato(d["porcentual"])} %\nCon valor verdadero cero, el relativo y porcentual no están definidos.'
    if clave == 'num_propagacion':
        referencia = f'Referencia racional exacta: {d["cambio_exacto"]}' if d['cambio_exacto'] is not None else 'Esta función no tiene una referencia racional disponible; el cambio directo es flotante.'
        return f'Derivada aproximada: {formato(d["derivada"])}\nΔy lineal: {formato(d["estimacion"])}\nCambio directo: {formato(d["cambio"])}\nDiferencia: {formato(d["error"])}\n{referencia}'
    if clave == 'num_simulacion':
        return f'Referencia Decimal (100 cifras): {d["referencia"]}\nRedondeado: {d["redondeado"]}\nTruncado: {d["truncado"]}\nConsulta todos los errores por iteración en la tabla.'
    if clave == 'num_flotante':
        return '\n'.join(f'{fila[0]}: {fila[1]}' for fila in d['filas'])
    if clave == 'num_inestabilidad':
        return f'Forma directa: {formato(d["directo"])}\nReformulada: {formato(d["estable"])}\nError directo: {formato(d["error_directo"])}\nError reformulado: {formato(d["error_estable"])}'
    if clave == 'num_bases':
        return f'Representación en base {d["base"]}:\n{calculo.valor}\nResto exacto no mostrado: {d["resto"]}'
    return f'Comparación con Fraction, float propio y NumPy\ncond(A): {formato(d["condicion"])}\nResiduo propio: {formato(d["residuo"])}\nResiduo NumPy: {formato(d["residuo_numpy"])}\nLa tabla conserva cada error absoluto y relativo.'


def casos_numericos(clave):
    """Devuelve casos pequeños para practicar criterios y fallos de precondiciones."""
    return {'num_biseccion': ('Ejemplo del profesor', 'cos(x)-x', 'Sin cambio de signo', 'Raíz en extremo'),
            'num_jacobi': ('Diagonal dominante', 'Reordenar 2×2', 'Sin convergencia', 'Diagonal con cero'),
            'num_gauss_seidel': ('Diagonal dominante', 'Reordenar 2×2', 'Diagonal con cero', 'Sin convergencia'),
            'num_comparar_iterativos': ('Diagonal dominante', 'Reordenar 2×2', 'Diagonal con cero', 'Sin convergencia'),
            'num_inversa': ('Hilbert 5×5', 'Invertible 2×2', 'Singular'),
            'num_sistema': ('Hilbert 5×5', 'Solución conocida', 'Singular')}.get(clave, ('Ejemplo del profesor',))
