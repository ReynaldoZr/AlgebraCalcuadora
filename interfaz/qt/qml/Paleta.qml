pragma Singleton
import QtQuick

// Paleta principal: carbón e índigo en modo oscuro y verde salvia en modo claro.
QtObject {
    property bool oscuro: true
    readonly property color fondo: oscuro ? "#14151a" : "#dad7cd"
    readonly property color tarjeta: oscuro ? "#1c1e26" : "#eae8e1"
    readonly property color entrada: oscuro ? "#252833" : "#f5f4f0"
    readonly property color texto: oscuro ? "#f1f5f9" : "#344e41"
    readonly property color secundario: oscuro ? "#9ca3af" : "#3a5a40"
    readonly property color borde: oscuro ? "#323646" : "#a3b18a"
    readonly property color acento: oscuro ? "#6366f1" : "#588157"
    readonly property color sobreAcento: oscuro ? "#ffffff" : "#f5f4f0"
    readonly property color error: oscuro ? "#ffabb5" : "#a8243c"
}
