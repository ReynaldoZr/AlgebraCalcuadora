"""Adapta la vista de resultados en tabla a todos los métodos de la calculadora.

Tema: presentación uniforme con tabla, métricas y detalles técnicos sin cálculos en QML.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.metodos_numericos import (
    METODOS_NUMERICOS, formato_visual, resumen_iterativo_estructurado,
)
from modulos.numericos.funciones import formato


def _tabla_desde_resumen(resumen):
    """Convierte líneas de resumen exacto en filas de dos columnas para mostrar en tabla."""
    filas = []
    for linea in (resumen or '').splitlines():
        texto = linea.strip()
        if not texto:
            continue
        if ':' in texto:
            clave, valor = texto.split(':', 1)
            filas.append([clave.strip(), valor.strip() or '—'])
        else:
            filas.append(['Resultado', texto])
    return filas or [['Resultado', 'Cálculo completado']]


def _construir_newton(calculo):
    """Genera tabla, estado y detalles técnicos con precisión completa para Newton-Raphson."""
    d = calculo.datos
    convergio = bool(d.get('convergio'))
    raiz_txt = formato_visual(calculo.valor) if calculo.valor is not None else 'No disponible'
    filas = [
        ['Raíz aproximada' if convergio else 'Última aproximación', raiz_txt],
        ['Iteraciones realizadas', str(d.get('iteraciones', len(d.get('filas', ()))))],
        ['Criterio de error', str(d.get('criterio', 'absoluto'))],
        ['Tolerancia del cambio', formato_visual(d.get('tolerancia'))],
        ['Tolerancia del residuo', formato_visual(d.get('tolerancia_f'))],
        ['Comprobación |f(x)|', formato_visual(d.get('residuo'))],
    ]
    if d.get('scipy') is not None:
        filas.append(['Referencia SciPy', formato_visual(d.get('scipy'))])
    if d.get('diferencia_scipy') is not None:
        filas.append(['Diferencia con SciPy', formato_visual(d.get('diferencia_scipy'))])

    detalles = [
        dict(titulo='Motivo de parada', valor=str(d.get('motivo', ''))),
        dict(titulo='Aproximación (precisión completa)', valor=formato(calculo.valor) if calculo.valor is not None else 'No disponible'),
        dict(titulo='Residuo |f(x)| completo', valor=formato(d.get('residuo'))),
        dict(titulo='Tolerancia del cambio completa', valor=formato(d.get('tolerancia'))),
        dict(titulo='Tolerancia del residuo completa', valor=formato(d.get('tolerancia_f'))),
    ]
    if d.get('scipy') is not None:
        detalles.append(dict(titulo='Referencia SciPy completa', valor=formato(d.get('scipy'))))
        detalles.append(dict(titulo='Diferencia con SciPy completa', valor=formato(d.get('diferencia_scipy'))))

    advertencias = [] if convergio else [f'No convergió: {d.get("motivo", "")}']
    return dict(
        activo=True,
        estado_general='Newton-Raphson convergió.' if convergio else 'Newton-Raphson no convergió.',
        comparacion_iteraciones='',
        metodos=[
            dict(
                nombre='Newton-Raphson',
                iteraciones=d.get('iteraciones', len(d.get('filas', ()))),
                estado='Convergió' if convergio else 'Sin converger',
                convergio=convergio,
                residuo_corto=formato_visual(d.get('residuo')),
                error_corto=formato_visual(d.get('registros', ())[-1].get(
                    'error_porcentual' if d.get('criterio') == 'porcentual' else 'error_absoluto'
                )) if d.get('registros') else 'No definido',
                etiqueta_error='Cambio (%)' if d.get('criterio') == 'porcentual' else 'Cambio absoluto',
            ),
        ],
        columnas=['Concepto', 'Valor'],
        filas=filas,
        nota_referencia='Referencia SciPy: contraste independiente cuando aplica; no es un valor exacto.',
        nota_precision='Valores redondeados solo para mostrar; tabla, pasos y detalles conservan precisión completa.',
        titulo_residuo='Residuo en la función',
        explicacion_residuo='El residuo |f(x)| comprueba qué tan cerca de cero queda f(x) en la aproximación final.',
        advertencias=advertencias,
        detalles_tecnicos=detalles,
    )


def _construir_numerico(clave, calculo, resumen):
    """Genera tabla, tarjetas clave y detalles técnicos para métodos numéricos."""
    if clave == 'num_newton':
        return _construir_newton(calculo)
    d = calculo.datos
    if clave == 'num_biseccion':
        raices = d.get('raices_extremos', ())
        filas = [
            ['Valor principal para guardar' if len(raices) > 1 else
             'Raíz aproximada' if d.get('convergio') else 'Última aproximación', formato_visual(calculo.valor)],
            ['Iteraciones realizadas', str(len(d.get('filas', ())))],
            ['Predicción por ancho', str(d.get('iteraciones_predichas', '—'))],
            ['Residuo |f(xr)|', formato_visual(d.get('residuo'))],
            ['Referencia SciPy', formato_visual(d.get('scipy'))],
            ['Diferencia con SciPy', formato_visual(d.get('diferencia_scipy'))],
        ]
        if len(raices) > 1:
            filas.insert(0, ['Raíces en extremos', ', '.join(formato_visual(r) for r in raices)])
        detalles = [
            dict(titulo='Motivo de parada', valor=str(d.get('motivo', ''))),
            dict(titulo='Raíz (precisión completa)', valor=formato(calculo.valor)),
            dict(titulo='Residuo |f(xr)| completo', valor=formato(d.get('residuo'))),
            dict(titulo='Referencia SciPy completa', valor=formato(d.get('scipy'))),
            dict(titulo='Diferencia con SciPy completa', valor=formato(d.get('diferencia_scipy'))),
        ]
        return dict(
            activo=True,
            estado_general=d.get('motivo', 'Bisección completada.'),
            comparacion_iteraciones='',
            metodos=[
                dict(nombre='Iteraciones', iteraciones=len(d.get('filas', ())), estado='Convergió' if d.get('convergio') else 'Sin converger',
                     convergio=bool(d.get('convergio')), residuo_corto=formato_visual(d.get('residuo')),
                     error_corto=formato_visual(d.get('diferencia_scipy')),
                     etiqueta_error='Diferencia con SciPy'),
            ],
            columnas=['Concepto', 'Valor'],
            filas=filas,
            nota_referencia='Referencia SciPy: valor de contraste; no es una solución exacta.',
            nota_precision='Valores redondeados solo para mostrar; detalles y tabla conservan precisión completa.',
            explicacion_residuo='El residuo |f(xr)| mide qué tan cerca de cero queda la función evaluada.',
            advertencias=[] if d.get('convergio') else [d.get('motivo', 'No convergió')],
            titulo_residuo='Residuo en la función',
            detalles_tecnicos=detalles,
        )

    if clave == 'num_errores':
        filas = [
            ['Error absoluto', formato_visual(d.get('absoluto'))],
            ['Error relativo', formato_visual(d.get('relativo'))],
            ['Error porcentual (%)', formato_visual(d.get('porcentual'))],
        ]
        detalles = [
            dict(titulo='Error absoluto completo', valor=formato(d.get('absoluto'))),
            dict(titulo='Error relativo completo', valor=formato(d.get('relativo'))),
            dict(titulo='Error porcentual completo', valor=formato(d.get('porcentual')) + ' %'),
        ]
        return dict(
            activo=True, estado_general='Cálculo de errores completado.', comparacion_iteraciones='',
            metodos=[], columnas=['Tipo de error', 'Valor'], filas=filas,
            nota_referencia='', nota_precision='Con valor verdadero cero, el relativo y porcentual no están definidos.',
            explicacion_residuo='', advertencias=[], detalles_tecnicos=detalles,
        )

    if clave == 'num_propagacion':
        ref_exacta = str(d['cambio_exacto']) if d.get('cambio_exacto') is not None else 'No disponible'
        filas = [
            ['Derivada aproximada', formato_visual(d.get('derivada'))],
            ['Δy lineal', formato_visual(d.get('estimacion'))],
            ['Cambio directo', formato_visual(d.get('cambio'))],
            ['Diferencia', formato_visual(d.get('error'))],
            ['Referencia racional exacta', ref_exacta],
        ]
        detalles = [
            dict(titulo='Derivada completa', valor=formato(d.get('derivada'))),
            dict(titulo='Δy lineal completo', valor=formato(d.get('estimacion'))),
            dict(titulo='Cambio directo completo', valor=formato(d.get('cambio'))),
            dict(titulo='Diferencia completa', valor=formato(d.get('error'))),
        ]
        return dict(
            activo=True, estado_general='Propagación del error calculada.', comparacion_iteraciones='',
            metodos=[], columnas=['Magnitud', 'Valor'], filas=filas,
            nota_referencia='', nota_precision='Valores redondeados solo para mostrar.',
            explicacion_residuo='', advertencias=[], detalles_tecnicos=detalles,
        )

    if clave == 'num_simulacion':
        filas = [
            ['Referencia Decimal (100 cifras)', str(d.get('referencia', ''))],
            ['Redondeado', str(d.get('redondeado', ''))],
            ['Truncado', str(d.get('truncado', ''))],
        ]
        return dict(
            activo=True, estado_general='Simulación de redondeo y truncamiento.', comparacion_iteraciones='',
            metodos=[], columnas=['Método', 'Valor final'], filas=filas,
            nota_referencia='Referencia Decimal: calculada con 100 cifras.',
            nota_precision='Consulta todas las iteraciones en «Todos los pasos» → «Mostrar tabla».',
            explicacion_residuo='', advertencias=[],
            detalles_tecnicos=[dict(titulo='Resumen completo', valor=resumen)],
        )

    if clave == 'num_flotante':
        filas = [[str(f[0]), str(f[1])] for f in d.get('filas', ())]
        return dict(
            activo=True, estado_general='Experimentos de punto flotante.', comparacion_iteraciones='',
            metodos=[], columnas=['Experimento', 'Resultado'], filas=filas,
            nota_referencia='', nota_precision='', explicacion_residuo='', advertencias=[],
            detalles_tecnicos=[dict(titulo='Detalle completo', valor=resumen)],
        )

    if clave == 'num_inestabilidad':
        filas = [
            ['Forma directa', formato_visual(d.get('directo')), formato_visual(d.get('error_directo'))],
            ['Reformulada', formato_visual(d.get('estable')), formato_visual(d.get('error_estable'))],
        ]
        detalles = [
            dict(titulo='Directa completa', valor=formato(d.get('directo'))),
            dict(titulo='Error directo completo', valor=formato(d.get('error_directo'))),
            dict(titulo='Reformulada completa', valor=formato(d.get('estable'))),
            dict(titulo='Error reformulado completo', valor=formato(d.get('error_estable'))),
        ]
        return dict(
            activo=True, estado_general='Comparación de estabilidad numérica.', comparacion_iteraciones='',
            metodos=[], columnas=['Expresión', 'Valor', 'Error'], filas=filas,
            nota_referencia='', nota_precision='Valores redondeados solo para mostrar.',
            explicacion_residuo='', advertencias=[], detalles_tecnicos=detalles,
        )

    if clave == 'num_bases':
        filas = [
            [f'Base {d.get("base", "")}', str(calculo.valor)],
            ['Resto exacto no mostrado', str(d.get('resto', ''))],
        ]
        return dict(
            activo=True, estado_general=f'Conversión a base {d.get("base", "")}.', comparacion_iteraciones='',
            metodos=[], columnas=['Concepto', 'Valor'], filas=filas,
            nota_referencia='', nota_precision='', explicacion_residuo='', advertencias=[],
            detalles_tecnicos=[dict(titulo='Resumen completo', valor=resumen)],
        )

    filas = [
        [str(f[0]), str(f[1]), formato_visual(f[2]), formato_visual(f[3]), formato_visual(f[4])]
        for f in d.get('filas', ())
    ]
    detalles = [
        dict(titulo='Número de condición cond(A)', valor=formato(d.get('condicion'))),
        dict(titulo='Residuo propio', valor=formato(d.get('residuo'))),
        dict(titulo='Residuo NumPy', valor=formato(d.get('residuo_numpy'))),
        dict(titulo='Resumen completo', valor=resumen),
    ]
    return dict(
        activo=True,
        estado_general=f'Comparación exacta frente a flotante · cond(A) = {formato_visual(d.get("condicion"))}',
        comparacion_iteraciones='',
        metodos=[],
        columnas=['Posición', 'Exacto', 'Float propio', 'Ref. NumPy', 'Error abs.'],
        filas=filas,
        nota_referencia='Ref. NumPy: referencia flotante independiente para comparar.',
        nota_precision='Valores redondeados solo para mostrar; detalles conservan precisión completa.',
        explicacion_residuo=f'Residuo propio: {formato_visual(d.get("residuo"))} · Residuo NumPy: {formato_visual(d.get("residuo_numpy"))}',
        advertencias=[],
        detalles_tecnicos=detalles,
    )


def resumen_estructurado(clave, presentacion):
    """Construye una vista de tabla estructurada para cualquier método de la calculadora."""
    if clave in ('num_comparar_iterativos', 'num_jacobi', 'num_gauss_seidel'):
        return resumen_iterativo_estructurado(clave, presentacion.calculo)
    if clave in METODOS_NUMERICOS:
        return _construir_numerico(clave, presentacion.calculo, presentacion.resumen)

    filas = []
    if presentacion.matriz is not None and len(presentacion.matriz) > 0:
        filas.append(['Tamaño de matriz', f'{len(presentacion.matriz)}×{len(presentacion.matriz[0])}'])
    filas.extend(_tabla_desde_resumen(presentacion.resumen))
    return dict(
        activo=True,
        estado_general='Resultado exacto con fracciones.',
        comparacion_iteraciones='',
        metodos=[],
        columnas=['Concepto', 'Resultado'],
        filas=filas,
        nota_referencia='',
        nota_precision='',
        explicacion_residuo='',
        advertencias=[],
        detalles_tecnicos=[
            dict(titulo='Pasos generados', valor=str(len(presentacion.calculo.pasos))),
            dict(titulo='Resumen completo', valor=presentacion.resumen or ''),
        ],
    )
