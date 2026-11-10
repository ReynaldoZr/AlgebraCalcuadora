pragma Singleton
import QtQuick

// Una sola paleta conserva azul y lavanda en todos los componentes.
QtObject {
    property bool oscuro: true
    readonly property color fondo: oscuro ? "#10243e" : "#eef2fa"
    readonly property color tarjeta: oscuro ? "#1a3350" : "#ffffff"
    readonly property color entrada: oscuro ? "#142b46" : "#f4f6fc"
    readonly property color texto: oscuro ? "#edf2fa" : "#10243e"
    readonly property color secundario: oscuro ? "#b3c2d6" : "#526580"
    readonly property color borde: oscuro ? "#405c79" : "#c5cede"
    readonly property color acento: oscuro ? "#a5a6ff" : "#6261b8"
    readonly property color sobreAcento: oscuro ? "#10243e" : "#ffffff"
    readonly property color error: oscuro ? "#ffabb5" : "#a8243c"
}
