pragma Singleton
import QtQuick

// Paleta principal: obsidiana y amatista en modo oscuro y verde salvia en modo claro.
QtObject {
    property bool oscuro: true
    readonly property color fondo: oscuro ? "#15131b" : "#dad7cd"
    readonly property color tarjeta: oscuro ? "#1f1c28" : "#eae8e1"
    readonly property color entrada: oscuro ? "#292536" : "#f5f4f0"
    readonly property color texto: oscuro ? "#f3effa" : "#344e41"
    readonly property color secundario: oscuro ? "#a69db8" : "#3a5a40"
    readonly property color borde: oscuro ? "#3a344d" : "#a3b18a"
    readonly property color acento: oscuro ? "#a855f7" : "#588157"
    readonly property color sobreAcento: oscuro ? "#ffffff" : "#f5f4f0"
    readonly property color error: oscuro ? "#ffabb5" : "#a8243c"
}
