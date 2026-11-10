"""Traduce resultados exactos a datos de lectura para QML sin usar float.

Tema: fracciones apiladas, fórmulas completas y recorrido esencial.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from interfaz.lenguaje_pasos import explicar_paso
from modulos.procedimientos import Paso


def token_visual(valor):
    """Separa numerador y denominador; también admite fracciones explicativas."""
    if isinstance(valor, tuple) and len(valor) == 2:
        return dict(arriba=str(valor[0]), abajo=str(valor[1]))
    if hasattr(valor, 'denominator') and valor.denominator != 1:
        return dict(arriba=str(valor.numerator), abajo=str(valor.denominator))
    return dict(arriba=str(valor), abajo='')


def matriz_visual(matriz):
    """Conserva cada celda exacta y su posición, sin convertirla a número QML."""
    return [[token_visual(v) for v in fila] for fila in matriz] if matriz is not None else []


def paso_visual(paso, completo=True):
    """Expone fórmulas originales y explicaciones con las dos profundidades existentes."""
    return dict(titulo=paso.titulo, detalle=explicar_paso(paso, completo),
                formulas=[[token_visual(v) for v in f] for f in paso.formulas],
                matriz=matriz_visual(paso.matriz), separador=paso.separador or 0)


def previa_visual(paso):
    """Añade origen y destino al recorrido de matrices sin repetir sus operaciones."""
    if isinstance(paso, Paso):
        datos = paso_visual(paso, False)
        datos['formulas'] = datos['formulas'][:1]
        return datos
    fila, columna, _, _, _, signo = paso.paso
    origen = f'Fila {fila + 1} de A · Columna {columna + 1} de B' if signo == 'AB' else paso.operandos
    return dict(titulo=paso.titulo, detalle=paso.mensaje, origen=origen,
                formulas=[[token_visual(v) for v in paso.tokens]], matriz=[],
                fila=fila, columna=columna, par=-1 if paso.par is None else paso.par,
                signo=signo, fase=paso.fase)


def tabla_visual(calculo):
    """Entrega todas las filas; las cantidades no definidas se identifican en texto."""
    return dict(columnas=list(calculo.datos.get('columnas', ())),
                filas=[['No definido' if v is None else format(v, '.14g') if isinstance(v, float) else str(v)
                        for v in fila] for fila in calculo.datos.get('filas', ())])
