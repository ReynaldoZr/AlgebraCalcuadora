"""Conserva entradas, cálculos y Deshacer separados de los controles gráficos.

Tema: sesiones por método y ejemplos explícitos, sin dependencia de Qt o Tk.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from math import isfinite

from interfaz.biblioteca import crear_registro
from interfaz.ejemplos_casos import casos_disponibles, ejemplo_por_caso
from interfaz.metodos_numericos import METODOS_NUMERICOS, casos_numericos, parametros_defecto, parametros_vacios
from interfaz.qt.catalogo import CATALOGO, campos_de, ejecutar, leer_matrices, matrices_de, tema_de


class Sesion:
    """Mantiene un ejercicio y hasta cincuenta estados recuperables por método."""

    def __init__(self, clave):
        """Inicializa datos vacíos; los ajustes numéricos mantienen sus valores útiles."""
        self.clave = clave
        self.parametros = {**parametros_vacios(clave), 'escalar': ''}
        self.entradas = {}
        for nombre in matrices_de(clave):
            filas = 1 if clave in ('v_suma', 'v_resta', 'v_escalar') else 2
            columnas = 1 if nombre == 'b' else 3 if filas == 1 else 2
            self.entradas[nombre] = [[''] * columnas for _ in range(filas)]
        self.presentacion, self.breves, self.vigente = None, (), False
        self.historial = []
        self.revision = 0

    def capturar(self):
        """Copia datos mutables para no compartir las filas al deshacer."""
        return deepcopy((self.parametros, self.entradas, self.presentacion, self.breves, self.vigente))

    def recordar(self):
        """Registra una acción antes de editar y marca el resultado como anterior."""
        self.historial = (self.historial + [self.capturar()])[-50:]
        self.vigente = False
        self.revision += 1

    def deshacer(self):
        """Restaura el ejercicio sin cambiar el método elegido."""
        if self.historial:
            self.parametros, self.entradas, self.presentacion, self.breves, self.vigente = self.historial.pop()
            self.revision += 1

    def limpiar(self):
        """Vacía datos y resultado conservando método y dimensiones."""
        self.recordar()
        self.parametros = {**parametros_vacios(self.clave), 'escalar': ''}
        self.entradas = {n: [[''] * len(m[0]) for _ in m] for n, m in self.entradas.items()}
        self.presentacion, self.breves = None, ()

    def casos(self):
        """Devuelve los mismos casos de práctica que las interfaces anteriores."""
        return casos_numericos(self.clave) if self.clave in METODOS_NUMERICOS else casos_disponibles(self.clave)

    def cargar_ejemplo(self, caso=''):
        """Carga un ejemplo solo cuando la persona lo solicita."""
        caso = caso or self.casos()[0]
        if caso not in self.casos():
            raise ValueError('El caso no pertenece al método elegido.')
        self.recordar()
        if self.clave not in METODOS_NUMERICOS:
            entradas, escalar = ejemplo_por_caso(self.clave, caso)
            self.entradas = {n: [[str(v) for v in f] for f in entradas[n]] for n in matrices_de(self.clave)}
            self.parametros['escalar'] = escalar
            return
        self.parametros.update(parametros_defecto(self.clave))
        if self.clave == 'num_biseccion':
            variantes = {'cos(x)-x': ('cos(x)-x', '0', '1'),
                         'Sin cambio de signo': ('x^2+1', '-1', '1'),
                         'Raíz en extremo': ('x-1', '1', '3')}
            if caso in variantes:
                self.parametros.update(zip(('funcion', 'a', 'b'), variantes[caso]))
        if self.clave in ('num_inversa', 'num_sistema'):
            if caso == 'Hilbert 5×5':
                from modulos.numericos.comparadores import hilbert
                a = hilbert(5)
                b = [[sum(f)] for f in a]
            else:
                a = [[1, 2], [2, 4]] if caso == 'Singular' else [[2, 1], [1, -1]]
                b = [[5], [1]]
            datos = dict(A=a, b=b)
            self.entradas = {n: [[str(v) for v in f] for f in datos[n]] for n in matrices_de(self.clave)}

    def calcular(self):
        """Ejecuta y acepta una respuesta válida; un error conserva el cálculo anterior."""
        self.vigente = False
        presentacion, breves = ejecutar(self.clave, self.parametros, self.entradas)
        self.aceptar(presentacion, breves)

    def aceptar(self, presentacion, breves):
        """Conserva la salida del núcleo y una secuencia breve separada de todos los pasos."""
        self.recordar()
        self.presentacion, self.breves, self.vigente = presentacion, breves, True

    def registro(self, tipo='ejercicio'):
        """Construye el mismo formato JSON, respetando aproximaciones y fracciones."""
        if tipo == 'ejercicio' and not self.vigente:
            raise ValueError('Calcula primero el ejercicio actualizado.')
        if tipo == 'resultado':
            return self._registro_resultado()
        if tipo in self.entradas:
            entradas = leer_matrices(self.entradas, (tipo,))
            return crear_registro(tema_de(self.clave), self.clave, entradas,
                                  resultado=entradas[tipo], tipo='matriz')
        if tipo != 'ejercicio':
            raise ValueError('Elige una entrada, el resultado o el ejercicio completo.')
        entradas = leer_matrices(self.entradas, matrices_de(self.clave))
        p = self.presentacion
        registro = crear_registro(tema_de(self.clave), self.clave, entradas,
                                  escalar=self.parametros['escalar'] or '2',
                                  resultado=p.matriz, resumen=p.resumen, pasos=p.calculo.pasos)
        if self.clave in METODOS_NUMERICOS:
            registro['parametros'] = {k: self.parametros[k] for k in campos_de(self.clave, 0) + campos_de(self.clave, 1)}
        return registro

    def _registro_resultado(self):
        """Guarda la salida vigente como matriz, valor numérico o resumen."""
        if not self.vigente:
            raise ValueError('Calcula primero el resultado actualizado.')
        tema, p = tema_de(self.clave), self.presentacion
        if p.matriz is not None:
            return crear_registro(tema, self.clave, {'A': p.matriz},
                                  resultado=p.matriz, tipo='matriz')
        registro = crear_registro(tema, self.clave, {}, resumen=p.resumen, tipo='resultado')
        valor = p.calculo.valor
        if (type(valor) is int or isinstance(valor, Fraction)
                or isinstance(valor, float) and isfinite(valor)
                or isinstance(valor, Decimal) and valor.is_finite()):
            registro['valor'] = str(valor)
        return registro
