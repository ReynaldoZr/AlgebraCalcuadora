"""Conecta los temas nuevos al mismo catálogo de consola y escritorio.

Tema: presentación de cálculos exactos; no contiene algoritmos de resolución.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from dataclasses import dataclass

from interfaz.explicacion import etapas_completas
from modulos.modulo_determinantes import calcular_determinante
from modulos.modulo_lu import factorizar_lu, resolver_lu
from modulos.modulo_matrices import calcular_inversa, transponer_matriz
from modulos.modulo_sistemas import resolver_sistema
from modulos.modulo_vectores import combinacion_lineal, escalar_vector, independencia_lineal, restar_vectores, sumar_vectores
from modulos.procedimientos import Calculo, Paso
from teoremas.verificadores import PROPIEDADES, verificar_propiedad, verificar_todas

TEMAS = ('Sistemas', 'Vectores', 'Determinantes', 'Inversas', 'LU', 'Propiedades')


@dataclass(frozen=True)
class Operacion:
    """Describe un método, sus entradas reales y la orientación de sus datos."""

    tema: str
    nombre: str
    entradas: tuple
    ayuda: str
    escalar: bool = False


OPERACIONES = {
    'gauss': Operacion('Sistemas', 'Eliminación de Gauss', ('A', 'b'), 'A: coeficientes m×n. b: columna m×1.'),
    'jordan': Operacion('Sistemas', 'Gauss-Jordan', ('A', 'b'), 'A: coeficientes m×n. b: columna m×1.'),
    'v_suma': Operacion('Vectores', 'Suma de vectores', ('A', 'B'), 'Cada vector se escribe como una fila 1×n.'),
    'v_resta': Operacion('Vectores', 'Resta de vectores', ('A', 'B'), 'Cada vector se escribe como una fila 1×n.'),
    'v_escalar': Operacion('Vectores', 'Escalar por vector', ('A',), 'A: vector fila 1×n. k: escalar exacto.', True),
    'combinacion': Operacion('Vectores', 'Combinación lineal', ('A', 'b'), 'Cada columna de A es un vector. b: objetivo en una columna m×1.'),
    'independencia': Operacion('Vectores', 'Independencia lineal', ('A',), 'Cada columna de A es un vector. Resolvemos Ac=0.'),
    'det_reduccion': Operacion('Determinantes', 'Determinante por reducción', ('A',), 'A debe ser cuadrada. Se registran reemplazos e intercambios.'),
    'det_cofactores': Operacion('Determinantes', 'Determinante por cofactores', ('A',), 'A debe ser cuadrada. La expansión crece rápidamente; practica con órdenes pequeños.'),
    'det_sarrus': Operacion('Determinantes', 'Determinante por Sarrus', ('A',), 'Sarrus es exclusivamente para matrices 3×3.'),
    'inv_jordan': Operacion('Inversas', 'Inversa por Gauss-Jordan', ('A',), 'A cuadrada: [A|I] → [I|A⁻¹], con comprobación A·A⁻¹=I.'),
    'inv_adjunta': Operacion('Inversas', 'Inversa por adjunta', ('A',), 'A cuadrada y det(A)≠0. Se muestran menores, cofactores y adjunta.'),
    'lu_factorizar': Operacion('LU', 'Factorización A=LU', ('A',), 'Admite A rectangular: L m×m y U m×n. Sin permutación.'),
    'lu_resolver': Operacion('LU', 'Resolver Ax=b por LU', ('A', 'b'), 'A cuadrada, b columna m×1. Encadena Ly=b y Ux=y.'),
    'prop_todas': Operacion('Propiedades', 'Comprobar todas las propiedades', ('A', 'B', 'C'), 'Se calculan ambos miembros; las condiciones fallidas se indican como «No aplicable».', True),
}
for _clave, _nombre in PROPIEDADES.items():
    _entradas = ('A', 'B', 'C') if _clave in ('distributividad', 'asociatividad') else (
        ('A', 'B') if _clave in ('transpuesta_suma', 'transpuesta_producto', 'inversa_producto', 'det_producto') else ('A',))
    OPERACIONES['prop_' + _clave] = Operacion('Propiedades', _nombre, _entradas,
        'La comprobación reutiliza los cálculos internos y muestra ambos miembros.',
        _clave in ('transpuesta_escalar', 'det_escalar', 'fila_intercambio', 'fila_reemplazo', 'fila_escalar'))


@dataclass(frozen=True)
class Presentacion:
    """Reúne el cálculo completo, texto de resultado y matriz que se puede reutilizar."""

    calculo: Calculo
    resumen: str
    matriz: list | None


def extraer_columna(matriz):
    """Lee b exclusivamente como matriz columna, sin aplanar datos incompatibles."""
    if len(matriz[0]) != 1:
        raise ValueError('b debe ser una matriz columna m×1.')
    return [fila[0] for fila in matriz]


def describir_sistema(calculo, coeficientes=False):
    """Expresa clasificación, pivotes, libres y solución general por componentes."""
    datos = calculo.datos
    clasificaciones = dict(unica='Solución única · Consistente determinado',
                           infinitas='Infinitas soluciones · Consistente indeterminado',
                           sin_solucion='Sin solución · Sistema inconsistente')
    texto = [clasificaciones[datos['clasificacion']],
             'Columnas pivote: ' + (', '.join(str(j + 1) for j in datos['pivotes']) or 'ninguna'),
             'Variables libres: ' + (', '.join(f'x{j + 1}' for j in datos['libres']) or 'ninguna')]
    if calculo.valor is not None:
        for j, valor in enumerate(calculo.valor):
            expresion = str(valor)
            for k, base in enumerate(datos['base']):
                if base[j] != 0:
                    expresion += f' + ({base[j]})t{k + 1}'
            texto.append(f"{'c' if coeficientes else 'x'}{j + 1} = {expresion}")
        texto.append('Comprobación exacta: ' + ('se cumple' if datos['verificado'] else 'no se cumple'))
    return '\n'.join(texto)


def presentar_verificaciones(verificaciones):
    """Convierte ambos miembros de cada verificación en pasos visibles completos."""
    pasos, texto = [], []
    for verificacion in verificaciones:
        estado = 'No aplicable' if verificacion.cumple is None else 'Se cumple' if verificacion.cumple else 'No se cumple'
        titulo = verificacion.propiedad + ' · ' + estado
        texto.append(titulo + (': ' + verificacion.motivo if verificacion.motivo else ''))
        if verificacion.cumple is None:
            pasos.append(Paso(titulo, verificacion.motivo))
            continue
        for nombre, valor in (('Miembro izquierdo', verificacion.izquierda), ('Miembro derecho', verificacion.derecha)):
            pasos.append(Paso(titulo + ' · ' + nombre, matriz=valor) if isinstance(valor, list)
                         else Paso(titulo + ' · ' + nombre, formulas=((nombre, '=', valor),)))
    return Presentacion(Calculo(verificaciones, tuple(pasos)), '\n'.join(texto), None)


def calcular_operacion(clave, entradas, escalar=2):
    """Despacha un método del catálogo y adapta su salida a las dos interfaces."""
    operacion = OPERACIONES[clave]
    a = entradas['A']
    if clave in ('gauss', 'jordan'):
        calculo = resolver_sistema(a, extraer_columna(entradas['b']), clave)
        resumen = describir_sistema(calculo)
        pasos = calculo.pasos + (Paso('Solución y clasificación', resumen),)
        return Presentacion(Calculo(calculo.valor, pasos, calculo.datos), resumen,
                            [[v] for v in calculo.valor] if calculo.valor is not None else None)
    if clave.startswith('det_'):
        calculo = calcular_determinante(a, clave[4:])
        return Presentacion(calculo, f'det(A) = {calculo.valor}', [[calculo.valor]])
    if clave.startswith('inv_'):
        calculo = calcular_inversa(a, clave[4:])
        return Presentacion(calculo, 'Inversa calculada.\nComprobación exacta A·A⁻¹ = I: se cumple.', calculo.valor)
    if clave.startswith('lu_'):
        calculo = factorizar_lu(a) if clave == 'lu_factorizar' else resolver_lu(a, extraer_columna(entradas['b']))
        if clave == 'lu_factorizar':
            return Presentacion(calculo, 'Factorización sin permutación.\nComprobación exacta L·U = A: se cumple.\nLas matrices L y U aparecen en Todos los pasos.', calculo.valor[1])
        resumen = 'Solución: ' + ', '.join(f'x{i + 1}={v}' for i, v in enumerate(calculo.valor))
        resumen += '\ny = (' + ', '.join(str(v) for v in calculo.datos['y']) + ')\nComprobación A·x=b: se cumple.'
        return Presentacion(calculo, resumen, [[v] for v in calculo.valor])
    if clave in ('combinacion', 'independencia'):
        vectores = transponer_matriz(a)
        calculo = combinacion_lineal(vectores, extraer_columna(entradas['b'])) if clave == 'combinacion' else independencia_lineal(vectores)
        if clave == 'combinacion':
            resumen = ('Sí es combinación lineal.\n' if calculo.datos['pertenece'] else 'No es combinación lineal.\n') + describir_sistema(calculo, True)
            matriz = [[v] for v in calculo.valor] if calculo.valor is not None else None
        else:
            resumen = ('Linealmente independiente (L.I.)' if calculo.valor else 'Linealmente dependiente (L.D.)')
            resumen += f"\nPivotes: {len(calculo.datos['pivotes'])} · Variables libres: {len(calculo.datos['libres'])}"
            if calculo.datos['relacion'] is not None:
                resumen += '\nRelación no trivial Ac=0: c = (' + ', '.join(str(v) for v in calculo.datos['relacion']) + ')'
            matriz = calculo.datos['matriz']
        return Presentacion(Calculo(calculo.valor, calculo.pasos + (Paso('Conclusión', resumen),), calculo.datos), resumen, matriz)
    if clave.startswith('prop_'):
        b, c = entradas.get('B'), entradas.get('C')
        verificaciones = verificar_todas(a, b, c, escalar) if clave == 'prop_todas' else [verificar_propiedad(clave[5:], a, b, c, escalar)]
        return presentar_verificaciones(verificaciones)
    if clave.startswith('v_'):
        if len(a) != 1 or ('B' in operacion.entradas and len(entradas['B']) != 1):
            raise ValueError('Cada vector debe tener una sola fila (1×n).')
        u = a[0]
        v = entradas['B'][0] if 'B' in entradas else None
        resultado = escalar_vector(u, escalar) if clave == 'v_escalar' else (
            sumar_vectores(u, v) if clave == 'v_suma' else restar_vectores(u, v))
        pasos = []
        for j, valor in enumerate(resultado):
            paso = (0, j, escalar, u[j], valor, '×') if clave == 'v_escalar' else (0, j, u[j], v[j], valor, '+' if clave == 'v_suma' else '-')
            for etapa in etapas_completas(paso, j):
                pasos.append(Paso(f'Componente {j + 1} · {etapa.titulo}', etapa.mensaje, formulas=(etapa.tokens,)))
        return Presentacion(Calculo(resultado, tuple(pasos)), 'Vector resultado: (' + ', '.join(str(v) for v in resultado) + ')', [resultado])
    raise ValueError('Operación no disponible.')


def ejemplo_operacion(clave):
    """Devuelve entradas nuevas de ejemplos pequeños con respuestas conocidas."""
    tema = OPERACIONES[clave].tema
    datos = dict(A=[[1, 2], [3, 4]], B=[[0, 1], [1, 1]], C=[[1, 0], [0, 1]], b=[[5], [1]])
    if tema == 'Sistemas':
        datos['A'] = [[2, 1], [1, -1]]
    elif clave in ('v_suma', 'v_resta', 'v_escalar'):
        datos.update(A=[[1, 2, 3]], B=[[3, -1, 2]])
    elif clave == 'combinacion':
        datos.update(A=[[1, 0], [0, 1], [1, 1]], b=[[2], [3], [5]])
    elif clave == 'independencia':
        datos['A'] = [[1, 2], [2, 4]]
    elif tema == 'Determinantes' or clave == 'prop_metodo_sarrus':
        datos['A'] = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    elif tema == 'LU':
        datos.update(A=[[2, 1, 1], [4, -6, 0], [-2, 7, 2]], b=[[5], [-2], [9]])
    elif clave == 'prop_det_triangular':
        datos['A'] = [[2, 1], [0, 3]]
    return datos, '3'
