"""Interpreta funciones matemáticas mediante una lista explícita de operaciones.

Tema: entrada segura de f(x), sin eval, atributos, imports o instrucciones Python.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import ast
import math
import operator
from fractions import Fraction

FUNCIONES = {nombre: getattr(math, nombre) for nombre in ('sin', 'cos', 'tan', 'exp', 'log', 'log10', 'sqrt')}
FUNCIONES.update(sen=math.sin, ln=math.log, abs=abs)
OPERADORES = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
              ast.Div: operator.truediv, ast.Pow: operator.pow}


def numero_finito(valor, nombre='Valor'):
    """Convierte un número real finito; rechaza booleanos, complejos, NaN e infinito."""
    if isinstance(valor, bool):
        raise ValueError(f'{nombre} debe ser un número real finito.')
    try:
        numero = float(valor)
    except (ValueError, TypeError, OverflowError):
        raise ValueError(f'{nombre} debe ser un número real finito.') from None
    if not math.isfinite(numero):
        raise ValueError(f'{nombre} debe ser finito.')
    return numero


def validar_nodo(nodo, profundidad=0):
    """Admite solo aritmética, x, pi/e y llamadas de un argumento conocidas."""
    if profundidad > 24:
        raise ValueError('La expresión tiene demasiados niveles.')
    if isinstance(nodo, ast.Constant) and type(nodo.value) in (int, float):
        numero_finito(nodo.value)
    elif isinstance(nodo, ast.Name) and nodo.id in ('x', 'pi', 'e'):
        return
    elif isinstance(nodo, ast.BinOp) and type(nodo.op) in OPERADORES:
        validar_nodo(nodo.left, profundidad + 1)
        validar_nodo(nodo.right, profundidad + 1)
    elif isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, (ast.UAdd, ast.USub)):
        validar_nodo(nodo.operand, profundidad + 1)
    elif isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name) and nodo.func.id in FUNCIONES and len(nodo.args) == 1 and not nodo.keywords:
        validar_nodo(nodo.args[0], profundidad + 1)
    else:
        raise ValueError('Usa x, números, + − * / ^ y sin, cos, tan, exp, log, log10, sqrt o abs.')


def calcular_nodo(nodo, x):
    """Recorre el árbol validado; limita potencias y comprueba cada resultado intermedio."""
    if isinstance(nodo, ast.Constant):
        return float(nodo.value)
    if isinstance(nodo, ast.Name):
        return {'x': x, 'pi': math.pi, 'e': math.e}[nodo.id]
    if isinstance(nodo, ast.UnaryOp):
        valor = calcular_nodo(nodo.operand, x)
        return -valor if isinstance(nodo.op, ast.USub) else valor
    if isinstance(nodo, ast.Call):
        return numero_finito(FUNCIONES[nodo.func.id](calcular_nodo(nodo.args[0], x)), 'f(x)')
    izquierda, derecha = calcular_nodo(nodo.left, x), calcular_nodo(nodo.right, x)
    # La cota evita expresiones desproporcionadas; no ejecutamos código del texto.
    if isinstance(nodo.op, ast.Pow) and abs(derecha) > 100:
        raise ValueError('El exponente permitido está entre −100 y 100.')
    return numero_finito(OPERADORES[type(nodo.op)](izquierda, derecha), 'f(x)')


def crear_funcion(texto):
    """Devuelve f(x) a partir de una expresión breve validada, admitiendo ^ como potencia."""
    if not isinstance(texto, str) or not texto.strip() or len(texto) > 300:
        raise ValueError('Escribe una función de hasta 300 caracteres.')
    try:
        arbol = ast.parse(texto.replace('^', '**'), mode='eval')
    except (SyntaxError, RecursionError):
        raise ValueError('La expresión no tiene una sintaxis matemática válida.') from None
    if len(list(ast.walk(arbol))) > 160:
        raise ValueError('La expresión es demasiado extensa.')
    validar_nodo(arbol.body)

    def funcion(x):
        """Evalúa en un punto real y comunica errores de dominio sin ocultarlos."""
        x = numero_finito(x, 'x')
        try:
            return calcular_nodo(arbol.body, x)
        except (ValueError, OverflowError, ZeroDivisionError, TypeError) as error:
            raise ValueError(f'No se puede evaluar f({x:g}): {error}') from None

    return funcion


def formato(valor):
    """Prepara números aproximados para pantalla sin convertirlos en fracciones exactas."""
    return 'No definido' if valor is None else f'{valor:.16g}'


def valor_exacto(expresion, x):
    """Obtiene una referencia racional para aritmética/polinomios; otras funciones devuelven None."""
    fuente = expresion.replace('^', '**')
    arbol = ast.parse(fuente, mode='eval')
    validar_nodo(arbol.body)

    def recorrer(nodo):
        """Conserva el decimal escrito y evita llamar exacto a un resultado trascendente."""
        if isinstance(nodo, ast.Constant):
            valor = Fraction(ast.get_source_segment(fuente, nodo))
        elif isinstance(nodo, ast.Name) and nodo.id == 'x':
            valor = Fraction(str(x))
        elif isinstance(nodo, ast.UnaryOp):
            valor = recorrer(nodo.operand)
            valor = -valor if isinstance(nodo.op, ast.USub) else valor
        elif isinstance(nodo, ast.Call) and nodo.func.id == 'abs':
            valor = abs(recorrer(nodo.args[0]))
        elif isinstance(nodo, ast.BinOp):
            a, b = recorrer(nodo.left), recorrer(nodo.right)
            if isinstance(nodo.op, ast.Pow) and (b.denominator != 1 or abs(b) > 100):
                raise ValueError('La potencia no tiene referencia racional admitida.')
            valor = OPERADORES[type(nodo.op)](a, b)
        else:
            raise ValueError('No hay una referencia racional para esta función.')
        if valor.numerator.bit_length() > 8192 or valor.denominator.bit_length() > 8192:
            raise ValueError('La referencia exacta es demasiado extensa.')
        return valor

    try:
        return recorrer(arbol.body)
    except (ValueError, TypeError, ArithmeticError):
        return None
