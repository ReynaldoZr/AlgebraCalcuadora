"""Comprueba pegado, casos de práctica y exportación PDF sin controlar la pantalla.

Tema: ayudas de estudio y evidencias completas de los cálculos exactos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from fractions import Fraction as F
from pathlib import Path
import tempfile
import unittest

from interfaz.biblioteca import crear_registro
from interfaz.datos import convertir_numero
from interfaz.ejemplos_casos import casos_disponibles, ejemplo_por_caso
from interfaz.exportar_pdf import crear_pdf, exportar_pdf, lineas_documento
from interfaz.operaciones import OPERACIONES, calcular_operacion
from interfaz.pegado import interpretar_matriz, texto_matriz
from modulos.procedimientos import Paso


class PruebasEstudio(unittest.TestCase):
    """Valida lectura exacta y documentos independientes de Tk y de bibliotecas externas."""

    def test_pegar_desde_tablas_listas_y_filas(self):
        """Los formatos admitidos conservan 0.1 como 1/10 y las fracciones exactas."""
        esperada = [[F(1, 3), F(1, 10)], [-2, 4]]
        for texto in ('1/3\t0.1\n-2\t4', '1/3,0.1; -2,4', '[[1/3,0.1],[-2,4]]', '[1/3, 0.1]\n[-2, 4]'):
            self.assertEqual(interpretar_matriz(texto), esperada)
        self.assertEqual(interpretar_matriz(texto_matriz(esperada)), esperada)

    def test_pegado_rechaza_errores_antes_de_cargar(self):
        """Filas irregulares, texto, división por cero y tamaños excesivos son errores recuperables."""
        for texto in ('', '1 2\n3', '1,,2', '1/0 2', '__import__("os")', 'nan', 'inf', '[[1,2]', ']1[', '1\n' * 11):
            with self.subTest(texto=texto), self.assertRaises(ValueError):
                interpretar_matriz(texto)

    def test_casos_de_sistemas_y_vectores_tienen_el_diagnostico_prometido(self):
        """Los ejemplos distinguen clasificación, pertenencia e independencia reales."""
        for clave in ('gauss', 'jordan'):
            for caso, esperado in (('Solución única', 'unica'), ('Infinitas soluciones', 'infinitas'), ('Sin solución', 'sin_solucion')):
                datos, k = ejemplo_por_caso(clave, caso)
                self.assertEqual(calcular_operacion(clave, datos).calculo.datos['clasificacion'], esperado)
        for caso, esperado in (('Sí es combinación', True), ('No es combinación', False)):
            datos, _ = ejemplo_por_caso('combinacion', caso)
            self.assertEqual(calcular_operacion('combinacion', datos).calculo.datos['pertenece'], esperado)
        for caso, esperado in (('Independientes', True), ('Dependientes', False), ('Incluye vector cero', False)):
            datos, _ = ejemplo_por_caso('independencia', caso)
            self.assertEqual(calcular_operacion('independencia', datos).calculo.valor, esperado)

    def test_todos_los_casos_son_ejecutables_o_fallan_por_su_condicion_anunciada(self):
        """Cada ejemplo del catálogo sirve al método y solo falla donde el caso lo exige."""
        for clave in OPERACIONES:
            for caso in casos_disponibles(clave):
                with self.subTest(clave=clave, caso=caso):
                    datos, escalar = ejemplo_por_caso(clave, caso)
                    entradas = {n: [[convertir_numero(str(v)) for v in f] for f in m] for n, m in datos.items()}
                    debe_fallar = (clave.startswith('inv_') and caso == 'Singular') or (
                        clave.startswith('lu_') and caso == 'Requiere PA=LU') or (clave == 'lu_resolver' and caso == 'Singular')
                    if debe_fallar:
                        with self.assertRaises(ValueError):
                            calcular_operacion(clave, entradas, convertir_numero(escalar))
                    else:
                        self.assertIsNotNone(calcular_operacion(clave, entradas, convertir_numero(escalar)))

    def test_pdf_incluye_todos_los_pasos_y_pagina_sin_recortes(self):
        """La exportación pagina una secuencia larga y conserva el último paso y sus fracciones."""
        pasos = tuple(Paso(f'Etapa {i}', 'Explicación breve', formulas=((F(1, 3), '+', F(1, 6), '=', F(1, 2)),)) for i in range(110))
        registro = crear_registro('Matrices', 'transponer', {'A': [[F(1, 3)]]}, resultado=[[F(1, 3)]], pasos=pasos)
        registro.update(nombre='Mi Aᵀ (fracciones)', notas='Inversa A⁻¹ y texto con acentos: álgebra.')
        lineas = lineas_documento(registro)
        self.assertIn('Etapa 109', '\n'.join(lineas))
        self.assertIn('1/3 + 1/6 = 1/2', '\n'.join(lineas))
        self.assertIn('A^(-1)', '\n'.join(lineas))
        pdf = crear_pdf(registro)
        self.assertTrue(pdf.startswith(b'%PDF-1.4'))
        self.assertGreater(pdf.count(b'/Type /Page '), 1)
        referencia = int(pdf.split(b'startxref\n')[-1].splitlines()[0])
        self.assertEqual(pdf[referencia:referencia + 4], b'xref')
        self.assertIn(b'Etapa 109', pdf)
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / 'ejercicio.pdf'
            exportar_pdf(registro, ruta)
            self.assertEqual(ruta.read_bytes(), pdf)
