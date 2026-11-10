"""Comprueba guardado persistente, nombres, historial y recuperación exacta.

Tema: archivos de la persona, conservación ante errores y JSON sin código ejecutable.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from interfaz.biblioteca import Biblioteca, crear_registro, leer_matriz_guardada, recuperar_pasos
from modulos.procedimientos import Paso


class PruebasBiblioteca(unittest.TestCase):
    """Usa archivos temporales; nunca lee ni modifica la biblioteca real del equipo."""

    def setUp(self):
        """Crea una biblioteca temporal con un ejercicio de transpuesta exacta."""
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.ruta = Path(self.temporal.name) / 'datos' / 'biblioteca.json'
        self.biblioteca = Biblioteca(self.ruta)
        self.registro = crear_registro('Matrices', 'transponer', {'A': [[F(1, 3), -2]]},
                                      resultado=[[F(1, 3)], [-2]], resumen='Transpuesta exacta',
                                      pasos=(Paso('Traslado', matriz=[[F(1, 3)], [-2]],
                                                  formulas=(('A[1,1]', '=', F(1, 3), '=', ('2', '6')),)),))

    def test_nombres_simbolos_propios_y_numeracion_sin_reutilizar(self):
        """Dos transpuestas se distinguen y borrar una no reinicia la numeración."""
        primero = self.biblioteca.guardar(self.registro)
        segundo = self.biblioteca.guardar(self.registro)
        self.assertEqual((primero['nombre'], segundo['nombre']), ('Transpuesta 1', 'Transpuesta 2'))
        self.assertEqual(primero['simbolo'], 'Aᵀ')
        self.assertNotEqual(primero['id'], segundo['id'])
        self.biblioteca.eliminar(primero['id'])
        tercero = self.biblioteca.guardar(self.registro)
        self.assertEqual(tercero['nombre'], 'Transpuesta 3')
        propio = self.biblioteca.guardar(self.registro, 'Mi Aᵀ de práctica', 'Revisar las columnas.', 'T₂')
        self.assertEqual(propio['notas'], 'Revisar las columnas.')
        self.assertEqual(propio['simbolo'], 'T₂')
        with self.assertRaisesRegex(ValueError, 'Ya existe'):
            self.biblioteca.guardar(self.registro, 'mi aᵀ de práctica')

    def test_reabrir_json_recupera_fracciones_formulas_y_copias(self):
        """Otra instancia recupera el ejercicio, incluidos resultados y fracciones sin simplificar."""
        original = deepcopy(self.registro)
        self.biblioteca.guardar(self.registro, 'Caso 1')
        self.biblioteca.registrar_historial(self.registro)
        nueva = Biblioteca(self.ruta)
        registro = nueva.listar()[0]
        self.assertEqual(leer_matriz_guardada(registro['resultado']), [[F(1, 3)], [-2]])
        pasos = recuperar_pasos(registro)
        self.assertEqual(pasos[0].formulas[0], ('A[1,1]', '=', F(1, 3), '=', ('2', '6')))
        self.assertEqual(self.registro, original)
        self.assertEqual(len(nueva.listar(True)), 1)
        registro['resultado'][0][0] = '99'
        self.assertEqual(nueva.listar()[0]['resultado'][0][0], '1/3')
        self.assertNotIn('Fraction(', self.ruta.read_text(encoding='utf-8'))

    def test_historial_acotado_y_guardados_permanentes_independientes(self):
        """El historial conserva cien cálculos; promover uno crea una copia permanente."""
        biblioteca = Biblioteca()
        for _ in range(103):
            biblioteca.registrar_historial(self.registro)
        historial = biblioteca.listar(True)
        self.assertEqual(len(historial), 100)
        self.assertEqual(historial[0]['nombre'], 'Transpuesta · 103')
        permanente = biblioteca.guardar(historial[-1], 'Primer ejercicio que conservé')
        biblioteca.eliminar(historial[-1]['id'], historial=True)
        self.assertEqual(biblioteca.listar()[0]['id'], permanente['id'])
        self.assertEqual(len(biblioteca.listar(True)), 99)

    def test_editar_nombre_notas_y_rechazar_duplicados(self):
        """Renombrar mantiene valores, fecha e identidad; un error no cambia el archivo."""
        uno = self.biblioteca.guardar(self.registro, 'Uno')
        self.biblioteca.guardar(self.registro, 'Dos')
        self.biblioteca.renombrar(uno['id'], 'Mi ejercicio', 'Una nota nueva')
        uno_editado = next(r for r in self.biblioteca.listar() if r['id'] == uno['id'])
        self.assertEqual(uno_editado['fecha'], uno['fecha'])
        self.assertEqual(uno_editado['resultado'], uno['resultado'])
        contenido = self.ruta.read_bytes()
        with self.assertRaises(ValueError):
            self.biblioteca.renombrar(uno['id'], 'DOS')
        self.assertEqual(self.ruta.read_bytes(), contenido)

    def test_archivo_corrupto_o_version_futura_no_se_sobrescribe(self):
        """Un archivo ilegible queda intacto y la app puede seguir calculando en su sesión."""
        self.ruta.parent.mkdir()
        for contenido in ('{rotura', '{"version": 3}', '{"version": true}'):
            self.ruta.write_text(contenido, encoding='utf-8')
            biblioteca = Biblioteca(self.ruta)
            self.assertTrue(biblioteca.error_lectura)
            with self.assertRaises(ValueError):
                biblioteca.guardar(self.registro)
            self.assertEqual(self.ruta.read_text(encoding='utf-8'), contenido)

    def test_fallo_de_escritura_conserva_archivo_y_estado_y_limpia_temporal(self):
        """Si reemplazar el archivo falla, se conserva el último guardado completo."""
        self.biblioteca.guardar(self.registro, 'Seguro')
        estado, contenido = deepcopy(self.biblioteca.datos), self.ruta.read_bytes()
        with patch('interfaz.biblioteca.os.replace', side_effect=OSError('Disco no disponible')):
            with self.assertRaises(OSError):
                self.biblioteca.guardar(self.registro, 'No escrito')
        self.assertEqual(self.biblioteca.datos, estado)
        self.assertEqual(self.ruta.read_bytes(), contenido)
        self.assertEqual(list(self.ruta.parent.glob('*.tmp')), [])

    def test_datos_invalidos_y_ids_duplicados_no_entran(self):
        """Los datos exactos se validan antes de usar el archivo y no se ejecuta su contenido."""
        with self.assertRaises(ValueError):
            crear_registro('Matrices', 'sumar', {'A': [[True]]})
        with self.assertRaises(ValueError):
            leer_matriz_guardada([['__import__("os")']])
        registro = self.biblioteca.guardar(self.registro)
        datos = deepcopy(self.biblioteca.datos)
        datos['guardados'].append(registro)
        self.ruta.write_text(json.dumps(datos), encoding='utf-8')
        self.assertTrue(Biblioteca(self.ruta).error_lectura)
