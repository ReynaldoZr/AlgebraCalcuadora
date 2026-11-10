"""Conecta eventos QML con sesiones y servicios existentes del proyecto.

Tema: señales, tareas de cálculo, biblioteca y temporizador de dos segundos.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from copy import deepcopy
from pathlib import Path

from PySide6.QtCore import QObject, Property, QRunnable, QThreadPool, QTimer, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFileDialog

from interfaz.biblioteca import Biblioteca, leer_matriz_guardada, ruta_biblioteca
from interfaz.datos import convertir_numero
from interfaz.ejemplos_casos import AYUDAS
from interfaz.exportar_pdf import exportar_pdf
from interfaz.metodos_numericos import CAMPOS, METODOS_NUMERICOS
from interfaz.pegado import interpretar_matriz, texto_matriz
from interfaz.qt.catalogo import (
    AYUDA_NUMERICA, CATALOGO, TEMAS, campos_de, ejecutar, matrices_de,
    metodos_tema, tema_de,
)
from interfaz.qt.presentacion import matriz_visual, paso_visual, previa_visual, tabla_visual
from interfaz.qt.sesion import Sesion
from interfaz.recorrido import INTERVALO_PASOS_MS
from teoremas.resumen_teoremas import teoremas_tema


class Respuesta(QObject):
    """Entrega la respuesta del trabajador al hilo de la interfaz."""

    lista = Signal(object, str)


class TrabajoCalculo(QRunnable):
    """Evita bloquear las animaciones mientras Python ejecuta el método."""

    def __init__(self, sesion):
        """Copia entradas para que la tarea no comparta datos editables con QML."""
        super().__init__()
        self.clave = sesion.clave
        self.parametros, self.entradas = deepcopy((sesion.parametros, sesion.entradas))
        self.respuesta = Respuesta()

    def run(self):
        """Devuelve errores comprensibles al hilo principal sin modificar widgets."""
        try:
            resultado = ejecutar(self.clave, self.parametros, self.entradas)
        except Exception as error:
            self.respuesta.lista.emit(None, str(error))
        else:
            self.respuesta.lista.emit(resultado, '')


class Controlador(QObject):
    """Presenta contratos simples a QML y mantiene la exactitud en Python."""

    formularioCambiado = Signal()
    resultadoCambiado = Signal()
    previaCambiada = Signal()
    estadoCambiado = Signal()
    bibliotecaCambiada = Signal()
    navegar = Signal(str)
    dialogoTexto = Signal(str, str)
    graficaLista = Signal(str)

    def __init__(self, biblioteca=None, padre=None):
        """Prepara sesiones vacías y servicios; no importa dependencias numéricas."""
        super().__init__(padre)
        self.biblioteca = biblioteca if biblioteca is not None else Biblioteca(ruta_biblioteca())
        self.sesiones, self.ultimos = {}, {}
        self.clave = 'sumar'
        self.sesiones[self.clave] = Sesion(self.clave)
        self._mensaje = self.biblioteca.error_lectura or 'Elige un tema para comenzar.'
        self._error, self._ocupado = bool(self.biblioteca.error_lectura), False
        self._salida, self._previa = {}, {}
        self._presentacion_publicada = None
        self._indice, self._revision_grafica = -1, 0
        self._tarea = None
        self._registrar = True
        self._fuente_grafica = None
        self.reloj = QTimer(self)
        self.reloj.setInterval(INTERVALO_PASOS_MS)
        self.reloj.timeout.connect(self.siguiente)

    @property
    def sesion(self):
        """Obtiene la sesión activa sin mezclar ejercicios de otros métodos."""
        return self.sesiones[self.clave]

    @Property('QVariantList', constant=True)
    def temas(self):
        """Lista las unidades implementadas con símbolos y descripciones."""
        return [dict(nombre=n, simbolo=s, detalle=d) for n, s, d in TEMAS]

    @Property('QVariantMap', notify=formularioCambiado)
    def formulario(self):
        """Entrega solo las entradas reales del método y las opciones permitidas."""
        s = self.sesion
        tema = tema_de(self.clave)
        matrices = []
        for nombre in matrices_de(self.clave):
            m = s.entradas[nombre]
            matrices.append(dict(nombre=nombre, filas=len(m), columnas=len(m[0]),
                                 celdas=[dict(fila=i, columna=j, valor=v) for i, f in enumerate(m) for j, v in enumerate(f)]))
        campos = []
        for columna in (0, 1):
            lista = []
            for nombre in campos_de(self.clave, columna):
                opciones = ['intervalo', 'porcentual'] if nombre == 'criterio' else ['2', '10'] if nombre == 'base' else []
                lista.append(dict(clave=nombre, etiqueta='Escalar k' if nombre == 'escalar' else CAMPOS[nombre][0],
                                  valor=s.parametros[nombre], opciones=opciones))
            campos.append(lista)
        ayuda = AYUDA_NUMERICA[self.clave] if tema == 'Numéricos' else CATALOGO[self.clave].ayuda
        return dict(clave=self.clave, tema=tema, metodos=metodos_tema(tema),
                    matricesA=matrices[:1], matricesB=matrices[1:], camposA=campos[0], camposB=campos[1],
                    ayuda=ayuda, casos=list(s.casos()), funcion='funcion' in campos_de(self.clave, 0),
                    ejemplo=self.clave != 'num_flotante')

    @Property('QVariantMap', notify=resultadoCambiado)
    def resultado(self):
        """Devuelve el resultado ya preparado; no recalcula al redibujar QML."""
        return self._salida

    @Property('QVariantMap', notify=previaCambiada)
    def previa(self):
        """Expone únicamente la etapa actual para que el temporizador sea ligero."""
        return self._previa

    @Property('QVariantMap', notify=estadoCambiado)
    def estado(self):
        """Habilita acciones según vigencia, datos y reproducción."""
        s = self.sesion
        return dict(mensaje=self._mensaje, error=self._error, ocupado=self._ocupado,
                    vigente=s.vigente, deshacer=bool(s.historial), reproduciendo=self.reloj.isActive(),
                    matriz=s.vigente and s.presentacion is not None and s.presentacion.matriz is not None,
                    destinos=list(s.entradas),
                    destinosValores=self._destinos_valores(),
                    graficable=s.vigente and self.clave in ('num_biseccion', 'num_propagacion', 'num_simulacion', 'num_inversa', 'num_sistema'))

    @Property('QVariantList', notify=bibliotecaCambiada)
    def guardados(self):
        """Presenta metadatos; los datos exactos permanecen en la biblioteca."""
        return self.biblioteca.listar()

    @Property('QVariantList', notify=bibliotecaCambiada)
    def historial(self):
        """Presenta los últimos cien ejercicios en orden de uso."""
        return self.biblioteca.listar(True)

    def avisar(self, mensaje, error=False):
        """Comunica un estado sin borrar entradas o resultados válidos."""
        self._mensaje, self._error = mensaje, error
        self.estadoCambiado.emit()

    def _seleccionar(self, clave):
        """Recupera una sesión por método sin cargar ejemplos automáticamente."""
        if clave not in CATALOGO and clave not in METODOS_NUMERICOS:
            raise ValueError('El método del ejercicio no está disponible en esta versión.')
        self.pausar()
        self.clave = clave
        self.ultimos[tema_de(clave)] = clave
        if clave not in self.sesiones:
            self.sesiones[clave] = Sesion(clave)
        self.formularioCambiado.emit()
        self._publicar()
        self.avisar('Completa los datos o carga un ejemplo. Las entradas se conservan al navegar.')

    @Slot(str)
    def abrirTema(self, tema):
        """Abre un tema real desde Inicio o el menú plegable."""
        if self._ocupado or not metodos_tema(tema):
            return
        self._seleccionar(self.ultimos.get(tema, metodos_tema(tema)[0]['clave']))
        self.navegar.emit('calculadora')

    @Slot(str)
    def seleccionar(self, clave):
        """Cambia de método conservando el ejercicio de cada sesión."""
        if not self._ocupado and (clave in CATALOGO or clave in METODOS_NUMERICOS):
            self._seleccionar(clave)

    def _editar(self):
        """Invalida la salida antes de modificar una entrada."""
        self.pausar()
        self.sesion.recordar()
        self._indice = -1

    def _terminar_edicion(self, formulario=False):
        """Actualiza la respuesta sin reconstruir los campos mientras se escribe."""
        if formulario:
            self.formularioCambiado.emit()
        self._publicar()
        self.avisar('Datos modificados · Pulsa Calcular para actualizar.')

    @Slot(str, str)
    def editarCampo(self, nombre, valor):
        """Conserva el texto original; la validación numérica ocurre al calcular."""
        if self._ocupado or nombre not in self.sesion.parametros or self.sesion.parametros[nombre] == valor:
            return
        self._editar()
        self.sesion.parametros[nombre] = valor
        self._terminar_edicion()

    @Slot(str, int, int, str)
    def editarCelda(self, nombre, fila, columna, valor):
        """Guarda una casilla como texto exacto sin pasarla por JavaScript Number."""
        if self._ocupado or nombre not in self.sesion.entradas:
            return
        matriz = self.sesion.entradas[nombre]
        if not 0 <= fila < len(matriz) or not 0 <= columna < len(matriz[0]) or matriz[fila][columna] == valor:
            return
        self._editar()
        matriz[fila][columna] = valor
        self._terminar_edicion()

    @Slot(str, int, int)
    def redimensionar(self, nombre, filas, columnas):
        """Aplica dimensiones tras la confirmación del diálogo, conservando coincidencias."""
        if self._ocupado or nombre not in self.sesion.entradas:
            return
        if not 1 <= filas <= 10 or not 1 <= columnas <= 10:
            self.avisar('El editor admite de 1 a 10 filas y columnas.', True)
            return
        anterior = self.sesion.entradas[nombre]
        self._editar()
        self.sesion.entradas[nombre] = [[anterior[i][j] if i < len(anterior) and j < len(anterior[0]) else ''
                                         for j in range(columnas)] for i in range(filas)]
        self._terminar_edicion(True)

    @Slot(str)
    def cargarEjemplo(self, caso=''):
        """Carga un caso pertinente únicamente por acción explícita."""
        if self._ocupado:
            return
        try:
            self.pausar()
            self.sesion.cargar_ejemplo(caso)
            self._terminar_edicion(True)
        except (ValueError, ImportError) as error:
            self.avisar(str(error), True)

    @Slot()
    def limpiar(self):
        """Vacía el ejercicio activo sin volver a suma u otro método."""
        if not self._ocupado:
            self.pausar()
            self.sesion.limpiar()
            self._terminar_edicion(True)

    @Slot()
    def deshacer(self):
        """Recupera la acción previa y deja el recorrido en pausa."""
        if not self._ocupado:
            self.pausar()
            self.sesion.deshacer()
            self.formularioCambiado.emit()
            self._publicar()
            self.avisar('Acción deshecha · Se conserva el método elegido.')

    @Slot()
    def calcular(self):
        """Inicia una tarea independiente y deshabilita las ediciones hasta recibirla."""
        self._iniciar_calculo(True)

    def _iniciar_calculo(self, registrar):
        """Conecta el trabajador; ninguna tarea escribe en la biblioteca por su cuenta."""
        if self._ocupado:
            return
        self.pausar()
        self.sesion.vigente = False
        self._publicar()
        self._ocupado, self._registrar = True, registrar
        self._tarea = TrabajoCalculo(self.sesion)
        self._tarea.respuesta.lista.connect(self._recibir)
        self.avisar('Calculando…')
        QThreadPool.globalInstance().start(self._tarea)

    @Slot(object, str)
    def _recibir(self, respuesta, error):
        """Publica el resultado en el hilo principal y registra historial sin duplicar cargas."""
        self._ocupado = False
        self._tarea = None
        if error:
            self._publicar()
            self.avisar('Faltan dependencias numéricas.' if 'No module named' in error else error, True)
            return
        self.sesion.aceptar(*respuesta)
        self._publicar()
        self.avisar('Cálculo completado · Consulta el recorrido o todos los pasos.')
        if self._registrar:
            try:
                self.biblioteca.registrar_historial(self.sesion.registro())
                self.bibliotecaCambiada.emit()
            except (OSError, ValueError) as fallo:
                self.avisar(f'El cálculo está listo, pero no se pudo guardar el historial: {fallo}', True)

    def _publicar(self):
        """Prepara todos los pasos una vez; el temporizador solo cambia la previa."""
        s = self.sesion
        self._indice = 0 if s.vigente and s.breves else -1
        if s.presentacion is not self._presentacion_publicada or not self._salida:
            self._salida = dict(resumen='Todavía no hay resultado para este método.', matriz=[], pasos=[], tabla=dict(columnas=[], filas=[]))
            if s.presentacion:
                p = s.presentacion
                self._salida.update(resumen=p.resumen, matriz=matriz_visual(p.matriz),
                                    pasos=[paso_visual(paso) for paso in p.calculo.pasos], tabla=tabla_visual(p.calculo))
            self._presentacion_publicada = s.presentacion
            self.resultadoCambiado.emit()
        self._actualizar_previa()
        self.estadoCambiado.emit()

    def _actualizar_previa(self):
        """Expone la etapa esencial y su posición sin modificar los pasos completos."""
        pasos = self.sesion.breves
        self._previa = previa_visual(pasos[self._indice]) if self.sesion.vigente and 0 <= self._indice < len(pasos) else {}
        self._previa.update(indice=self._indice, total=len(pasos) if self.sesion.vigente else 0)
        self.previaCambiada.emit()

    @Slot()
    def pausar(self):
        """Cancela el reloj al editar, navegar o cerrar la aplicación."""
        self.reloj.stop()
        self.estadoCambiado.emit()

    @Slot()
    def reproducir(self):
        """Alterna reproducción con ritmo fijo de dos segundos."""
        if self.reloj.isActive():
            self.pausar()
        elif self.sesion.vigente and self.sesion.breves:
            if self._indice >= len(self.sesion.breves) - 1:
                self._indice = 0
                self._actualizar_previa()
            self.reloj.start()
            self.estadoCambiado.emit()

    @Slot()
    def siguiente(self):
        """Avanza sin recortar etapas y se detiene al llegar al final."""
        if self.sesion.vigente and self._indice + 1 < len(self.sesion.breves):
            self._indice += 1
            self._actualizar_previa()
        if self._indice >= len(self.sesion.breves) - 1:
            self.pausar()

    @Slot()
    def anterior(self):
        """Retrocede en pausa conservando la misma secuencia."""
        self.pausar()
        self._indice = max(0, self._indice - 1)
        self._actualizar_previa()

    @Slot()
    def reiniciar(self):
        """Vuelve a la primera etapa sin iniciar reproducción automática."""
        self.pausar()
        self._indice = 0
        self._actualizar_previa()

    @Slot(str)
    def copiarMatriz(self, nombre):
        """Copia una matriz exacta al portapapeles por acción explícita."""
        try:
            registro = self.sesion.registro('resultado' if nombre == 'Resultado' else nombre)
            QGuiApplication.clipboard().setText(texto_matriz(leer_matriz_guardada(registro['resultado'])))
            self.avisar('Matriz copiada.')
        except (ValueError, ZeroDivisionError) as error:
            self.avisar(str(error), True)

    @Slot(str)
    def pegarMatriz(self, nombre):
        """Valida todo el portapapeles antes de reemplazar una matriz."""
        if self._ocupado or nombre not in self.sesion.entradas:
            return
        try:
            matriz = interpretar_matriz(QGuiApplication.clipboard().text())
            self._editar()
            self.sesion.entradas[nombre] = [[str(v) for v in f] for f in matriz]
            self._terminar_edicion(True)
        except (ValueError, ZeroDivisionError) as error:
            self.avisar(str(error), True)

    @Slot(str)
    def usarResultado(self, destino):
        """Reutiliza una matriz exacta en una entrada del método activo."""
        if self._ocupado:
            return
        try:
            registro = self.sesion.registro('resultado')
            self._usar_matriz(registro, destino)
        except ValueError as error:
            self.avisar(str(error), True)

    def _usar_matriz(self, registro, destino):
        """No convierte aproximaciones numéricas en matrices exactas ficticias."""
        matriz = registro.get('resultado')
        if destino not in self.sesion.entradas or matriz is None:
            raise ValueError('Elige una matriz y una entrada disponible del método.')
        leer_matriz_guardada(matriz)
        if len(matriz) > 10 or len(matriz[0]) > 10:
            raise ValueError('El editor admite matrices de hasta 10×10.')
        self._editar()
        self.sesion.entradas[destino] = deepcopy(matriz)
        self._terminar_edicion(True)
        self.navegar.emit('calculadora')

    def _destinos_valores(self):
        """Enumera los campos reales del método activo que reciben números."""
        excluidos = {'funcion', 'criterio', 'base', 'maximo', 'iteraciones', 'decimales', 'cifras'}
        return [dict(clave=nombre, etiqueta='Escalar k' if nombre == 'escalar' else CAMPOS[nombre][0])
                for columna in (0, 1) for nombre in campos_de(self.clave, columna)
                if nombre not in excluidos]

    def _usar_valor(self, registro, destino):
        """Coloca el valor en el campo elegido y registra la edición."""
        if destino not in {campo['clave'] for campo in self._destinos_valores()}:
            raise ValueError('Elige un campo numérico del ejercicio actual.')
        valor = registro['valor']
        if destino != 'escalar':
            from modulos.numericos.funciones import numero_finito
            numero = numero_finito(convertir_numero(valor) if '/' in valor else valor)
            if '/' in valor:
                valor = str(numero)
        self._editar()
        self.sesion.parametros[destino] = valor
        self._terminar_edicion(True)
        self.navegar.emit('calculadora')

    @Slot(str, str, str, str)
    def guardar(self, tipo, nombre, simbolo, notas):
        """Comparte nombres automáticos, símbolos y persistencia con la interfaz anterior."""
        try:
            self.biblioteca.guardar(self.sesion.registro(tipo), nombre, notas, simbolo)
            self.bibliotecaCambiada.emit()
            self.avisar('Guardado en la Biblioteca sin cambiar el ejercicio.')
        except (ValueError, OSError, ZeroDivisionError) as error:
            self.avisar(str(error), True)

    def _buscar(self, identificador, historial):
        """Localiza un registro validado sin aceptar rutas o código de la interfaz."""
        registro = next((r for r in self.biblioteca.listar(historial) if r['id'] == identificador), None)
        if registro is None:
            raise ValueError('No se encontró el ejercicio guardado.')
        return registro

    @Slot(str, result='QVariantMap')
    def copiarEjercicio(self, identificador):
        """Duplica un ejercicio guardado con un nombre disponible."""
        try:
            original = self._buscar(identificador, False)
            if original['tipo'] != 'ejercicio':
                raise ValueError('Selecciona un ejercicio guardado para copiarlo.')
            nombres = {registro['nombre'].casefold() for registro in self.biblioteca.listar()}
            numero = 1
            while True:
                sufijo = ' (copia)' if numero == 1 else f' (copia {numero})'
                nombre = original['nombre'][:120 - len(sufijo)].rstrip() + sufijo
                if nombre.casefold() not in nombres:
                    break
                numero += 1
            copia = self.biblioteca.guardar(original, nombre, original['notas'], original['simbolo'])
            self.bibliotecaCambiada.emit()
            self.avisar(f'Se guardó «{nombre}». Puedes cargar la copia desde la calculadora.')
            return copia
        except (ValueError, OSError) as error:
            self.avisar(str(error), True)
            return {}

    @Slot(str, bool)
    def abrirGuardado(self, identificador, historial):
        """Recupera entradas y recalcula sin registrar un historial duplicado."""
        if self._ocupado:
            return
        try:
            r = self._buscar(identificador, historial)
            if r['tipo'] != 'ejercicio':
                self.dialogoTexto.emit(r['nombre'], r['resumen'] or 'Elige «Usar como» para cargar esta matriz en el método actual.')
                return
            self._seleccionar(r['operacion'])
            self._editar()
            self.sesion.entradas = deepcopy(r['entradas'])
            self.sesion.parametros.update(r.get('parametros', {}), escalar=r['escalar'])
            self.formularioCambiado.emit()
            self.navegar.emit('calculadora')
            self._iniciar_calculo(False)
        except (KeyError, ValueError) as error:
            self.avisar(str(error), True)

    @Slot(str, bool, str)
    def usarGuardado(self, identificador, historial, destino):
        """Coloca una salida guardada en el destino elegido o la copia como texto."""
        if not self._ocupado:
            try:
                registro = self._buscar(identificador, historial)
                if registro['tipo'] != 'resultado':
                    self._usar_matriz(registro, destino)
                elif destino:
                    if 'valor' not in registro:
                        raise ValueError('El resultado no tiene un valor numérico único.')
                    self._usar_valor(registro, destino)
                else:
                    QGuiApplication.clipboard().setText(registro.get('valor', registro['resumen']))
                    self.avisar('Resultado copiado.')
            except ValueError as error:
                self.avisar(str(error), True)

    @Slot(str, bool, str, str, str)
    def editarGuardado(self, identificador, historial, nombre, simbolo, notas):
        """Renombra un guardado o convierte un cálculo del historial en permanente."""
        try:
            if historial:
                self.biblioteca.guardar(self._buscar(identificador, True), nombre, notas, simbolo)
            else:
                self.biblioteca.renombrar(identificador, nombre, notas, simbolo)
            self.bibliotecaCambiada.emit()
            self.avisar('Biblioteca actualizada.')
        except (ValueError, OSError) as error:
            self.avisar(str(error), True)

    @Slot(str, bool)
    def eliminarGuardado(self, identificador, historial):
        """Elimina un elemento después de la confirmación presentada en QML."""
        try:
            self.biblioteca.eliminar(identificador, historial)
            self.bibliotecaCambiada.emit()
            self.avisar('Elemento eliminado de la Biblioteca.')
        except (ValueError, OSError) as error:
            self.avisar(str(error), True)

    @Slot(str, bool)
    def exportar(self, identificador='', historial=False):
        """Pregunta el destino y escribe el PDF completo con el exportador existente."""
        try:
            registro = self._buscar(identificador, historial) if identificador else self.sesion.registro()
            ruta, _ = QFileDialog.getSaveFileName(None, 'Exportar ejercicio completo', 'ejercicio.pdf', 'PDF (*.pdf)')
            if ruta:
                exportar_pdf(registro, Path(ruta).with_suffix('.pdf'))
                self.avisar('PDF exportado con todos los pasos.')
        except (ValueError, OSError) as error:
            self.avisar(str(error), True)

    @Slot(str)
    def consultar(self, tipo):
        """Conserva teoremas y ayudas accesibles desde el encabezado."""
        texto = teoremas_tema(tema_de(self.clave)) if tipo == 'Teoremas' else '\n\n'.join(f'{k}\n{v}' for k, v in AYUDAS.items())
        self.dialogoTexto.emit(tipo, texto)

    @Slot(bool)
    def verGrafica(self, oscuro=True):
        """Genera la figura bajo demanda, fuera de los módulos de cálculo."""
        if not self.estado['graficable'] or self._fuente_grafica is None:
            return
        try:
            from interfaz.numericos.graficas_qt import imagen_grafica
            self._fuente_grafica.imagen = imagen_grafica(self.clave, self.sesion.presentacion.calculo, oscuro)
            self._revision_grafica += 1
            self.graficaLista.emit(f'image://graficas/{self._revision_grafica}')
        except (ImportError, ValueError) as error:
            self.avisar(f'No se pudo mostrar la gráfica: {error}', True)

    @Slot()
    def guardarGrafica(self):
        """Guarda la imagen únicamente cuando la persona selecciona un destino."""
        if self._fuente_grafica and not self._fuente_grafica.imagen.isNull():
            ruta, _ = QFileDialog.getSaveFileName(None, 'Guardar gráfica', 'grafica.png', 'PNG (*.png)')
            if ruta and not self._fuente_grafica.imagen.save(str(Path(ruta).with_suffix('.png'))):
                self.avisar('No se pudo guardar la imagen.', True)
