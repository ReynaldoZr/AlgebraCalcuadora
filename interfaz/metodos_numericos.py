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
}


def parametros_defecto(clave):
    """Devuelve una copia de valores iniciales pertinente a cada método."""
    datos = {k: v[1] for k, v in CAMPOS.items()}
    if clave == 'num_propagacion':
        datos['funcion'] = 'x^3'
    if clave == 'num_inestabilidad':
        datos['x'] = '1e16'
    return datos


def parametros_vacios(clave):
    """Mantiene ajustes de cálculo, pero deja sin llenar los datos del ejercicio."""
    datos = parametros_defecto(clave)
    # Tolerancias y límites son ajustes; función, extremos y cantidades son el ejercicio.
    for nombre in ('funcion', 'a', 'b', 'verdadero', 'aproximado', 'x', 'delta', 'capital', 'tasa', 'numero'):
        datos[nombre] = ''
    return datos


def entero(texto, nombre):
    """Convierte exclusivamente texto entero, con diagnóstico del campo afectado."""
    try:
        return int(texto)
    except (ValueError, TypeError):
        raise ValueError(f'{nombre} debe ser un entero.') from None


def ejecutar_numerico(clave, parametros, matrices=None):
    """Llama al núcleo de la semana 12; no requiere dependencias al iniciar otros temas."""
    from modulos.numericos.errores import calcular_errores, descomponer, inestabilidad, propagacion, punto_flotante, simulacion
    matrices = matrices or {}
    p = parametros
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


def resumen_numerico(clave, calculo):
    """Explica los resultados y límites de precisión con nombres de sus magnitudes."""
    from modulos.numericos.funciones import formato
    d = calculo.datos
    if clave == 'num_biseccion':
        return (f'Raíz aproximada: {formato(calculo.valor)}\n{d["motivo"]}\n'
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
            'num_inversa': ('Hilbert 5×5', 'Invertible 2×2', 'Singular'),
            'num_sistema': ('Hilbert 5×5', 'Solución conocida', 'Singular')}.get(clave, ('Ejemplo del profesor',))
