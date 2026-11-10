import QtQuick
import QtQuick.Controls

TextField {
    id: control
    implicitHeight: 39
    color: Paleta.texto
    placeholderTextColor: Paleta.secundario
    selectionColor: Paleta.acento
    selectedTextColor: Paleta.sobreAcento
    font.pixelSize: 14
    leftPadding: 11
    rightPadding: 11
    selectByMouse: true
    background: Rectangle {
        radius: 8
        color: Paleta.entrada
        border.color: control.activeFocus ? Paleta.acento : Paleta.borde
        border.width: control.activeFocus ? 2 : 1
        Behavior on border.color { ColorAnimation { duration: 130 } }
    }
}
