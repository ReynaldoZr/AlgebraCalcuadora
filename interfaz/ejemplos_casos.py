"""Ofrece casos de práctica y ayudas breves sin cambiar los métodos del núcleo.

Tema: ejemplos de solución, singularidad, pertenencia y pivoteo.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy

from interfaz.operaciones import ejemplo_operacion

AYUDAS = {
    'Pivote': 'Primer elemento no nulo de una fila escalonada. Su columna identifica una variable básica; en RREF el pivote vale 1.',
    'Variable libre': 'Variable cuya columna no tiene pivote. En un sistema consistente puede tomar un parámetro y producir infinitas soluciones.',
    'Sistema inconsistente': 'Una fila aumentada [0 ... 0 | b] con b distinto de cero exige 0=b. Por eso el sistema no tiene solución.',
    'Solución general': 'Se escribe x=p+t1·v1+... . La particular cumple Ap=b y cada dirección cumple Avi=0.',
    'Combinación lineal': 'Un vector b es combinación de las columnas de A cuando existen coeficientes c tales que Ac=b.',
    'Independencia lineal': 'Las columnas son independientes si Ac=0 solo tiene c=0. Si hay una solución no trivial, son dependientes.',
    'Cofactor': 'Cij=(-1)^(i+j)det(Mij). El menor Mij se obtiene suprimiendo la fila i y la columna j.',
    'Matriz singular': 'Matriz cuadrada sin inversa. Tiene determinante cero y menos pivotes que columnas.',
    'Transpuesta': 'Aᵀ intercambia filas y columnas: el elemento A[i,j] pasa a Aᵀ[j,i] sin cambiar su valor.',
    'Adjunta': 'Es la transpuesta de la matriz de cofactores. Para det(A)≠0, A⁻¹=adj(A)/det(A).',
    'LU sin permutación': 'Registra multiplicadores en L y elimina en U usando reemplazos. Si hace falta intercambiar filas, se necesita PA=LU y este método se detiene.',
    'No aplicable': 'La propiedad no cumple sus condiciones de dimensión, invertibilidad u orden. No significa que la igualdad haya sido comprobada.',
}


def casos_disponibles(clave):
    """Enumera casos pertinentes para el método seleccionado, sin cambiarlo."""
    if clave in ('gauss', 'jordan'):
        return ('Solución única', 'Infinitas soluciones', 'Sin solución', 'Requiere intercambio')
    if clave == 'combinacion':
        return ('Sí es combinación', 'No es combinación', 'Coeficientes no únicos')
    if clave == 'independencia':
        return ('Independientes', 'Dependientes', 'Incluye vector cero')
    if clave.startswith('inv_'):
        return ('Invertible', 'Singular', 'Requiere intercambio')
    if clave.startswith('det_'):
        return ('Determinante no nulo', 'Determinante cero', 'Triangular')
    if clave.startswith('lu_'):
        return ('Sin permutación', 'Requiere PA=LU', 'Singular')
    if clave == 'transponer':
        return ('Rectangular', 'Con fracciones')
    return ('Ejemplo habitual', 'Con fracciones')


def ejemplo_por_caso(clave, caso):
    """Devuelve matrices nuevas y k para un caso válido del método actual."""
    if caso not in casos_disponibles(clave):
        raise ValueError('Ese caso no pertenece al método seleccionado.')
    if clave in ('sumar', 'restar', 'escalar', 'multiplicar', 'transponer'):
        datos = dict(A=[[1, 2], [3, 4]], B=[[2, 0], [1, 2]])
    else:
        datos, _ = ejemplo_operacion(clave)
    k = '3'
    if clave in ('gauss', 'jordan'):
        ejemplos = {
            'Solución única': ([[2, 1], [1, -1]], [[5], [1]]),
            'Infinitas soluciones': ([[1, 2], [2, 4]], [[3], [6]]),
            'Sin solución': ([[1, 1], [2, 2]], [[1], [3]]),
            'Requiere intercambio': ([[0, 2], [3, 1]], [[1], [2]]),
        }
        datos['A'], datos['b'] = ejemplos[caso]
    elif clave == 'combinacion':
        datos.update(A=[[1, 0], [0, 1], [1, 1]], b=[[2], [3], [5 if caso != 'No es combinación' else 6]])
        if caso == 'Coeficientes no únicos':
            datos.update(A=[[1, 2], [2, 4]], b=[[3], [6]])
    elif clave == 'independencia':
        datos['A'] = {'Independientes': [[1, 0], [0, 1]], 'Dependientes': [[1, 2], [2, 4]],
                      'Incluye vector cero': [[1, 0], [2, 0]]}[caso]
    elif clave.startswith('inv_'):
        datos['A'] = {'Invertible': [[1, 2], [3, 4]], 'Singular': [[1, 2], [2, 4]],
                      'Requiere intercambio': [[0, 1], [1, 2]]}[caso]
    elif clave.startswith('det_'):
        datos['A'] = {'Determinante no nulo': [[1, 2, 3], [0, 1, 4], [5, 6, 0]],
                      'Determinante cero': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                      'Triangular': [[2, 1, 0], [0, 3, 1], [0, 0, 4]]}[caso]
    elif clave.startswith('lu_'):
        if caso == 'Requiere PA=LU':
            datos.update(A=[[0, 1], [1, 0]], b=[[1], [2]])
        elif caso == 'Singular':
            datos.update(A=[[1, 2], [2, 4]], b=[[3], [6]])
    elif clave == 'transponer':
        datos['A'] = [[1, 2, 3], [4, 5, 6]] if caso == 'Rectangular' else [['1/3', '-2'], ['0', '1/2']]
    elif caso == 'Con fracciones':
        if clave in ('v_suma', 'v_resta', 'v_escalar'):
            datos.update(A=[['1/3', '-2', '1/2']], B=[['1/6', '3', '1/4']])
        else:
            datos.update(A=[['1/3', '-2'], ['0', '1/2']], B=[['1/6', '1'], ['2', '1/4']])
            if clave.startswith('prop_'):
                datos['C'] = [[1, 0], [0, 1]]
        k = '-3/2'
    return deepcopy(datos), k
