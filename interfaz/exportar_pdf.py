"""Exporta ejercicios completos a PDF de texto sin dependencias externas.

Tema: evidencias de estudio con datos exactos y todos los pasos conservados.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

import os
from pathlib import Path
import tempfile
import textwrap

from interfaz.biblioteca import recuperar_pasos, validar_registro
from interfaz.formato import formatear_matriz
from interfaz.menu_algebra import formatear_pasos

SIMBOLOS = str.maketrans({'ᵀ': '^T', '⁻': '-', '¹': '1', '²': '2', '³': '3', 'ⁿ': '^n',
                         '−': '-', '·': '*', '×': '*', '÷': '/', '→': '->', '←': '<-', '↔': '<->',
                         '≠': '!=', 'Σ': 'sum', '∑': 'sum', 'ℝ': 'R', '∞': 'infinito', '⁰': '0',
                         '∈': ' pertenece a ', '∉': ' no pertenece a ', '≤': '<=', '≥': '>=', '↗': '->'})


def lineas_documento(registro):
    """Incluye nombre, notas, entradas, resultado y cada paso sin recortes de cantidad."""
    validar_registro(registro)
    lineas = [registro['nombre'] or registro['etiqueta'], registro['simbolo'] + ' | ' + registro['tema'],
              'Fecha de guardado (UTC): ' + registro['fecha'], '']
    if registro['notas']:
        lineas += ['Notas:', registro['notas'], '']
    for nombre, matriz in registro['entradas'].items():
        lineas += ['Entrada ' + nombre, formatear_matriz(matriz), '']
    if registro.get('parametros'):
        lineas += ['Parámetros del ejercicio numérico']
        lineas += [f'{nombre}: {valor}' for nombre, valor in registro['parametros'].items()]
        lineas.append('')
    if registro['tipo'] != 'resultado':
        lineas += ['Escalar k: ' + registro['escalar'], '']
    lineas += [registro['resumen'], '']
    if registro['resultado'] is not None:
        lineas += ['Resultado guardado', formatear_matriz(registro['resultado']), '']
    if registro['tipo'] != 'resultado':
        lineas += ['Desarrollo completo', formatear_pasos(recuperar_pasos(registro))]
    resultado = []
    for linea in '\n'.join(lineas).splitlines():
        texto = linea.replace('⁻¹', '^(-1)').translate(SIMBOLOS).encode('cp1252', errors='backslashreplace').decode('cp1252')
        resultado.extend(textwrap.wrap(texto, width=92, replace_whitespace=False, drop_whitespace=False) or [''])
    return resultado


def escapar_pdf(texto):
    """Escapa delimitadores de cadenas PDF, sin interpretar el contenido de las notas."""
    return texto.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def crear_pdf(registro):
    """Construye páginas A4 numeradas con fuente monoespaciada y fracciones como a/b."""
    lineas = lineas_documento(registro)
    paginas = [lineas[i:i + 54] for i in range(0, len(lineas), 54)]
    objetos = [b'<< /Type /Catalog /Pages 2 0 R >>', b'',
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>']
    referencias = []
    for numero, pagina in enumerate(paginas, 1):
        indice = len(objetos) + 1
        referencias.append(f'{indice} 0 R')
        objetos.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {indice + 1} 0 R >>'.encode('ascii'))
        comandos = ['BT /F1 9 Tf 13 TL 45 792 Td']
        comandos += [f'({escapar_pdf(linea)}) Tj T*' for linea in pagina]
        comandos += ['ET', f'BT /F1 9 Tf 45 34 Td (Cuaderno de Algebra | Pagina {numero} de {len(paginas)}) Tj ET']
        contenido = '\n'.join(comandos).encode('cp1252')
        objetos.append(f'<< /Length {len(contenido)} >>\nstream\n'.encode('ascii') + contenido + b'\nendstream')
    objetos[1] = f"<< /Type /Pages /Kids [{' '.join(referencias)}] /Count {len(paginas)} >>".encode('ascii')
    salida = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
    posiciones = [0]
    for indice, objeto in enumerate(objetos, 1):
        posiciones.append(len(salida))
        salida.extend(f'{indice} 0 obj\n'.encode('ascii') + objeto + b'\nendobj\n')
    referencia = len(salida)
    salida.extend(f'xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n'.encode('ascii'))
    for posicion in posiciones[1:]:
        salida.extend(f'{posicion:010d} 00000 n \n'.encode('ascii'))
    salida.extend(f'trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{referencia}\n%%EOF\n'.encode('ascii'))
    return bytes(salida)


def exportar_pdf(registro, ruta):
    """Escribe el PDF completo de forma atómica en la ubicación elegida por la persona."""
    contenido = crear_pdf(registro)
    destino = Path(ruta)
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(dir=destino.parent, suffix='.pdf.tmp', delete=False) as archivo:
            temporal = Path(archivo.name)
            archivo.write(contenido)
        os.replace(temporal, destino)
    finally:
        if temporal is not None and temporal.exists():
            temporal.unlink()
