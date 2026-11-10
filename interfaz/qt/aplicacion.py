"""Arranca Qt Quick y mantiene la consola libre de dependencias gráficas.

Tema: aplicación de escritorio local y proveedor de imágenes numéricas.
Elaboración: equipo del proyecto, con apoyo de IA.
"""

from pathlib import Path
import os
import sys

from PySide6.QtCore import QEventLoop, QTimer, QUrl
from PySide6.QtGui import QFontDatabase, QImage
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtWidgets import QApplication

from interfaz.qt.controlador import Controlador


class ImagenesGraficas(QQuickImageProvider):
    """Entrega a QML la última figura calculada únicamente a petición del usuario."""

    def __init__(self):
        """Prepara una imagen vacía sin importar Matplotlib al iniciar."""
        super().__init__(QQuickImageProvider.ImageType.Image)
        self.imagen = QImage()

    def requestImage(self, identificador, tamano, solicitado):
        """Devuelve una copia de la figura, preservando su proporción."""
        if tamano is not None:
            tamano.setWidth(self.imagen.width())
            tamano.setHeight(self.imagen.height())
        return self.imagen.copy()


def crear_motor(app, biblioteca=None):
    """Carga los componentes locales; inyecta una biblioteca en memoria en pruebas."""
    # El modo de pruebas sin pantalla de Windows necesita registrar fuentes locales.
    if sys.platform == 'win32':
        fuentes = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
        for archivo in ('segoeui.ttf', 'segoeuib.ttf', 'cambria.ttc'):
            if (fuentes / archivo).exists():
                QFontDatabase.addApplicationFont(str(fuentes / archivo))
    motor = QQmlApplicationEngine()
    controlador = Controlador(biblioteca, motor)
    imagenes = ImagenesGraficas()
    controlador._fuente_grafica = imagenes
    motor.addImageProvider('graficas', imagenes)
    motor.rootContext().setContextProperty('cuaderno', controlador)
    espera = QEventLoop()
    motor.objectCreated.connect(espera.quit)
    motor.objectCreationFailed.connect(espera.quit)
    limite = QTimer()
    limite.setSingleShot(True)
    limite.timeout.connect(espera.quit)
    limite.start(15000)
    motor.load(QUrl.fromLocalFile(str(Path(__file__).parent / 'qml' / 'Principal.qml')))
    if not motor.rootObjects():
        espera.exec()
    limite.stop()
    app.aboutToQuit.connect(controlador.pausar)
    return motor, controlador


def iniciar():
    """Ejecuta la ventana y comunica un fallo de carga en vez de ocultarlo."""
    QQuickStyle.setStyle('Basic')
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName('Cuaderno de Álgebra')
    app.setOrganizationName('CuadernoAlgebra')
    motor, controlador = crear_motor(app)
    if not motor.rootObjects():
        return 1
    # Ajustamos la ventana al escritorio disponible sin ampliar el mínimo a la fuerza.
    pantalla = app.primaryScreen()
    if pantalla is not None:
        area = pantalla.availableGeometry()
        ventana = motor.rootObjects()[0]
        ventana.setMinimumWidth(min(1100, area.width() - 40))
        ventana.setMinimumHeight(min(760, area.height() - 50))
        ventana.resize(min(1440, area.width() - 40), min(900, area.height() - 50))
    salida = app.exec()
    controlador.pausar()
    return salida
