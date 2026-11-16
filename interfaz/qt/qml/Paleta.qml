pragma Singleton
import QtQuick

// Paleta principal: azul profundo en modo oscuro y verde salvia en modo claro.
QtObject {
    property bool oscuro: true
    readonly property color fondo: oscuro ? "#001233" : "#dad7cd"
    readonly property color tarjeta: oscuro ? "#001845" : "#eae8e1"
    readonly property color entrada: oscuro ? "#002855" : "#f5f4f0"
    readonly property color texto: oscuro ? "#e8ecf4" : "#344e41"
    readonly property color secundario: oscuro ? "#979dac" : "#3a5a40"
    readonly property color borde: oscuro ? "#33415c" : "#a3b18a"
    readonly property color acento: oscuro ? "#0466c8" : "#588157"
    readonly property color sobreAcento: oscuro ? "#ffffff" : "#f5f4f0"
    readonly property color error: oscuro ? "#ffabb5" : "#a8243c"
}
