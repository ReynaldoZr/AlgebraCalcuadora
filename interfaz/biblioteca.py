"""Conserva matrices, ejercicios e historial en un archivo local de la persona.

Tema: persistencia JSON exacta, independiente de los algoritmos matemáticos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
import json
import os
from pathlib import Path
import tempfile
from uuid import uuid4

from interfaz.datos import convertir_numero
from modulos.procedimientos import Paso
from modulos.validaciones import validar_matriz

ETIQUETAS = {
    'num_biseccion': ('Bisección', '≈x'), 'num_errores': ('Errores numéricos', 'Ea'),
    'num_propagacion': ('Propagación', 'Δy'), 'num_simulacion': ('Redondeo y truncamiento', '≈'),
    'num_flotante': ('Punto flotante', 'ε'), 'num_inestabilidad': ('Estabilidad', '≈'),
    'num_bases': ('Representación numérica', 'base'), 'num_inversa': ('Inversa exacta y aproximada', '≈A⁻¹'),
    'num_sistema': ('Sistema exacto y aproximado', '≈x'),
    'sumar': ('Suma', '+'), 'restar': ('Resta', '−'), 'escalar': ('Escalar', 'kA'),
    'transponer': ('Transpuesta', 'Aᵀ'), 'multiplicar': ('Producto', 'AB'),
    'gauss': ('Gauss', 'REF'), 'jordan': ('Gauss-Jordan', 'RREF'),
    'v_suma': ('Suma vectorial', 'u+v'), 'v_resta': ('Resta vectorial', 'u−v'),
    'v_escalar': ('Escalar vectorial', 'kv'), 'combinacion': ('Combinación lineal', 'Ac=b'),
    'independencia': ('Independencia', 'L.I./L.D.'), 'det_reduccion': ('Determinante por reducción', '|A|'),
    'det_cofactores': ('Determinante por cofactores', '|A|'), 'det_sarrus': ('Sarrus', '|A|'),
    'inv_jordan': ('Inversa por Gauss-Jordan', 'A⁻¹'), 'inv_adjunta': ('Inversa por adjunta', 'A⁻¹'),
    'lu_factorizar': ('Factorización LU', 'LU'), 'lu_resolver': ('Sistema por LU', 'LU·x=b'),
}


def ruta_biblioteca():
    """Ubica los datos fuera del repositorio, sin depender de la carpeta de arranque."""
    if os.name == 'nt':
        base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
    else:
        base = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
    return base / 'CuadernoAlgebra' / 'biblioteca.json'


def matriz_texto(matriz):
    """Valida y convierte una matriz exacta a cadenas sin redondear fracciones."""
    validar_matriz(matriz)
    return [[str(v) for v in fila] for fila in matriz]


def leer_matriz_guardada(matriz):
    """Recupera una matriz JSON como valores exactos; rechaza listas irregulares."""
    if not isinstance(matriz, list) or not matriz or any(not isinstance(f, list) for f in matriz):
        raise ValueError('La matriz guardada no es válida.')
    resultado = [[convertir_numero(v) if isinstance(v, str) else v for v in fila] for fila in matriz]
    validar_matriz(resultado)
    return resultado


def codificar_token(token):
    """Distingue números exactos, fracciones literales y etiquetas en las fórmulas JSON."""
    if isinstance(token, bool):
        raise ValueError('Una fórmula no admite booleanos como números.')
    if isinstance(token, (int, Fraction)):
        return {'numero': str(token)}
    if isinstance(token, tuple) and len(token) == 2:
        return {'fraccion': [str(v) for v in token]}
    if isinstance(token, str):
        return token
    raise ValueError('Token de fórmula no compatible con el guardado.')


def decodificar_token(token):
    """Recupera tokens sin ejecutar código ni importar clases desde el archivo."""
    if isinstance(token, str):
        return token
    if isinstance(token, dict) and set(token) == {'numero'} and isinstance(token['numero'], str):
        return convertir_numero(token['numero'])
    if isinstance(token, dict) and set(token) == {'fraccion'}:
        partes = token['fraccion']
        if isinstance(partes, list) and len(partes) == 2 and all(isinstance(p, str) for p in partes):
            return tuple(partes)
    raise ValueError('La fórmula guardada no es válida.')


def codificar_pasos(pasos):
    """Guarda cada fórmula y matriz del desarrollo completo, sin truncarlo."""
    return [dict(titulo=p.titulo, detalle=p.detalle,
                 matriz=matriz_texto(p.matriz) if p.matriz is not None else None,
                 formulas=[[codificar_token(t) for t in f] for f in p.formulas], separador=p.separador)
            for p in pasos]


def recuperar_pasos(registro):
    """Devuelve instantáneas del desarrollo conservado, sin volver a calcularlo."""
    return tuple(Paso(p['titulo'], p['detalle'], leer_matriz_guardada(p['matriz']) if p['matriz'] is not None else None,
                      tuple(tuple(decodificar_token(t) for t in f) for f in p['formulas']), p['separador'])
                 for p in registro['pasos'])


def crear_registro(tema, operacion, entradas, escalar='2', resultado=None, resumen='', pasos=(), tipo='ejercicio'):
    """Construye un ejercicio o matriz exportable, con datos separados de los widgets."""
    etiqueta, simbolo = ETIQUETAS.get(operacion, ('Propiedad', '='))
    return dict(id=uuid4().hex, tipo=tipo, tema=tema, operacion=operacion,
                etiqueta=etiqueta, simbolo=simbolo, nombre='', notas='',
                fecha=datetime.now(timezone.utc).isoformat(),
                entradas={k: matriz_texto(v) for k, v in entradas.items()}, escalar=str(escalar),
                resultado=matriz_texto(resultado) if resultado is not None else None,
                resumen=resumen, pasos=codificar_pasos(pasos))


def validar_registro(registro):
    """Comprueba el formato de datos antes de escribirlo o mostrar un archivo leído."""
    textos = ('id', 'tipo', 'tema', 'operacion', 'etiqueta', 'simbolo', 'nombre', 'notas', 'fecha', 'escalar', 'resumen')
    if not isinstance(registro, dict) or any(not isinstance(registro.get(k), str) for k in textos):
        raise ValueError('El registro guardado tiene un formato incompatible.')
    if registro['tipo'] not in ('matriz', 'ejercicio', 'resultado'):
        raise ValueError('Tipo de guardado desconocido.')
    numerico = registro['tema'] == 'Numéricos' and registro['tipo'] == 'ejercicio'
    if not isinstance(registro.get('entradas'), dict) or (
            not registro['entradas'] and not numerico and registro['tipo'] != 'resultado'):
        raise ValueError('Faltan las entradas del ejercicio.')
    if registro['tipo'] == 'resultado' and 'valor' in registro:
        if not isinstance(registro['valor'], str):
            raise ValueError('El valor guardado debe estar escrito como texto numérico.')
        convertir_numero(registro['valor'])
    if numerico:
        from interfaz.metodos_numericos import CAMPOS, METODOS_NUMERICOS
        parametros = registro.get('parametros')
        if registro['operacion'] not in METODOS_NUMERICOS or not isinstance(parametros, dict) or any(
                k not in CAMPOS or not isinstance(v, str) or len(v) > 300 for k, v in parametros.items()):
            raise ValueError('Los parámetros numéricos guardados no son válidos.')
        metodo = METODOS_NUMERICOS[registro['operacion']]
        if any(k not in parametros for k in metodo.campos_a + metodo.campos_b) or any(k not in registro['entradas'] for k in metodo.matrices):
            raise ValueError('El ejercicio numérico está incompleto.')
    for nombre, matriz in registro['entradas'].items():
        if nombre not in ('A', 'B', 'C', 'b'):
            raise ValueError('Nombre de matriz guardada desconocido.')
        leer_matriz_guardada(matriz)
    convertir_numero(registro['escalar'])
    if registro.get('resultado') is not None:
        leer_matriz_guardada(registro['resultado'])
    if not isinstance(registro.get('pasos'), list):
        raise ValueError('Falta el procedimiento del ejercicio.')
    for paso in registro['pasos']:
        if not isinstance(paso, dict) or not isinstance(paso.get('titulo'), str) or not isinstance(paso.get('detalle'), str):
            raise ValueError('Paso guardado no válido.')
        if not isinstance(paso.get('formulas'), list) or any(not isinstance(f, list) for f in paso['formulas']):
            raise ValueError('Fórmulas guardadas no válidas.')
        corte = paso.get('separador')
        if corte is not None and (isinstance(corte, bool) or not isinstance(corte, int)):
            raise ValueError('Separador de matriz no válido.')
    recuperar_pasos(registro)


class Biblioteca:
    """Mantiene guardados permanentes e historial de cien cálculos con escritura atómica."""

    def __init__(self, ruta=None):
        """Recibe una ruta JSON; None crea un almacén solo en memoria para pruebas."""
        self.ruta = Path(ruta) if ruta is not None else None
        self.error_lectura = ''
        self.datos = dict(version=2, guardados=[], historial=[], contadores={}, secuencia=0)
        if self.ruta is not None and self.ruta.exists():
            try:
                datos = json.loads(self.ruta.read_text(encoding='utf-8'))
                if not isinstance(datos, dict) or type(datos.get('version')) is not int or datos['version'] not in (1, 2):
                    raise ValueError('Versión de biblioteca no compatible.')
                for clave in ('guardados', 'historial'):
                    if not isinstance(datos.get(clave), list):
                        raise ValueError('Lista de guardados no válida.')
                    identificadores = set()
                    nombres = set()
                    for registro in datos[clave]:
                        validar_registro(registro)
                        if not registro['id'] or registro['id'] in identificadores:
                            raise ValueError('Identificador de guardado duplicado o vacío.')
                        self._validar_nombre(registro['nombre'], nombres if clave == 'guardados' else set())
                        identificadores.add(registro['id'])
                        nombres.add(registro['nombre'].casefold())
                if not isinstance(datos.get('contadores'), dict) or any(
                        not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in datos['contadores'].values()):
                    raise ValueError('Contadores no válidos.')
                if not isinstance(datos.get('secuencia'), int) or isinstance(datos['secuencia'], bool) or datos['secuencia'] < 0:
                    raise ValueError('Secuencia de historial no válida.')
                # La versión 2 añade parámetros aproximados; los registros exactos de v1 no cambian.
                self.datos = dict(datos, version=2)
            except (OSError, ValueError, TypeError, KeyError, ZeroDivisionError) as error:
                self.error_lectura = f'No se pudo leer la biblioteca: {error}. El archivo original se conserva; no se sobrescribirá.'

    def listar(self, historial=False):
        """Devuelve copias, con los elementos más recientes primero."""
        return deepcopy(list(reversed(self.datos['historial' if historial else 'guardados'])))

    def _confirmar(self, nuevos):
        """Escribe primero en un temporal y sustituye el JSON solo al terminar correctamente."""
        if self.error_lectura:
            raise ValueError(self.error_lectura)
        if self.ruta is not None:
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            temporal = None
            try:
                with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=self.ruta.parent,
                                                 prefix='.biblioteca-', suffix='.tmp', delete=False) as archivo:
                    temporal = Path(archivo.name)
                    json.dump(nuevos, archivo, ensure_ascii=False, indent=2)
                    archivo.flush()
                    os.fsync(archivo.fileno())
                os.replace(temporal, self.ruta)
            finally:
                if temporal is not None and temporal.exists():
                    temporal.unlink()
        # La memoria se actualiza después del disco: un fallo no aparenta haber guardado.
        self.datos = nuevos

    def guardar(self, registro, nombre='', notas='', simbolo=None):
        """Crea un guardado independiente; el nombre automático diferencia operaciones repetidas."""
        validar_registro(registro)
        nuevos, copia = deepcopy(self.datos), deepcopy(registro)
        copia['id'] = uuid4().hex
        existentes = {r['nombre'].casefold() for r in nuevos['guardados']}
        nombre = nombre.strip()
        if not nombre:
            prefijo = copia['etiqueta']
            numero = nuevos['contadores'].get(prefijo, 0)
            while True:
                numero += 1
                nombre = f'{prefijo} {numero}'
                if nombre.casefold() not in existentes:
                    break
            nuevos['contadores'][prefijo] = numero
        self._validar_nombre(nombre, existentes)
        if len(notas) > 2000:
            raise ValueError('Las notas admiten hasta 2000 caracteres.')
        copia.update(nombre=nombre, notas=notas)
        copia['simbolo'] = self._simbolo(simbolo, copia['simbolo'])
        nuevos['guardados'].append(copia)
        self._confirmar(nuevos)
        return deepcopy(copia)

    def registrar_historial(self, registro):
        """Recuerda un cálculo válido sin exigir guardarlo manualmente en la biblioteca."""
        validar_registro(registro)
        nuevos, copia = deepcopy(self.datos), deepcopy(registro)
        nuevos['secuencia'] += 1
        copia.update(id=uuid4().hex, nombre=f"{copia['etiqueta']} · {nuevos['secuencia']}")
        nuevos['historial'].append(copia)
        nuevos['historial'] = nuevos['historial'][-100:]
        self._confirmar(nuevos)

    @staticmethod
    def _validar_nombre(nombre, existentes):
        """Exige nombres legibles y únicos sin prohibir símbolos o acentos de la persona."""
        if not nombre or len(nombre) > 120 or any(ord(c) < 32 for c in nombre):
            raise ValueError('Escribe un nombre de 1 a 120 caracteres, en una sola línea.')
        if nombre.casefold() in existentes:
            raise ValueError('Ya existe un guardado con ese nombre; elige otro.')

    @staticmethod
    def _simbolo(simbolo, automatico):
        """Permite un símbolo personal corto; vacío conserva el sugerido por la operación."""
        simbolo = simbolo.strip() if simbolo is not None else ''
        simbolo = simbolo or automatico
        if len(simbolo) > 24 or any(ord(c) < 32 for c in simbolo):
            raise ValueError('El símbolo admite hasta 24 caracteres en una sola línea.')
        return simbolo

    def renombrar(self, identificador, nombre, notas='', simbolo=None):
        """Actualiza nombre y notas conservando identidad, fecha y cálculos."""
        nuevos = deepcopy(self.datos)
        registro = next((r for r in nuevos['guardados'] if r['id'] == identificador), None)
        if registro is None:
            raise ValueError('No se encontró el guardado.')
        nombre = nombre.strip()
        self._validar_nombre(nombre, {r['nombre'].casefold() for r in nuevos['guardados'] if r['id'] != identificador})
        if len(notas) > 2000:
            raise ValueError('Las notas admiten hasta 2000 caracteres.')
        registro.update(nombre=nombre, notas=notas)
        registro['simbolo'] = self._simbolo(simbolo, registro['simbolo'])
        self._confirmar(nuevos)

    def eliminar(self, identificador, historial=False):
        """Quita únicamente el registro indicado; la interfaz confirma la acción con la persona."""
        nuevos = deepcopy(self.datos)
        clave = 'historial' if historial else 'guardados'
        anteriores = nuevos[clave]
        nuevos[clave] = [r for r in anteriores if r['id'] != identificador]
        if len(nuevos[clave]) == len(anteriores):
            raise ValueError('No se encontró el registro.')
        self._confirmar(nuevos)
