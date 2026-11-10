import QtQuick
import QtQuick.Controls

Button {
    id: control
    property bool principal: false
    property bool discreto: false
    implicitHeight: 40
    implicitWidth: Math.max(44, contenido.implicitWidth + 26)
    padding: 10
    hoverEnabled: true
    opacity: enabled ? 1 : 0.42
    font.pixelSize: 13
    contentItem: Text {
        id: contenido
        text: control.text
        font: control.font
        color: control.principal ? Paleta.sobreAcento : Paleta.texto
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
    background: Rectangle {
        radius: 9
        color: control.principal ? Paleta.acento : control.hovered ? Qt.lighter(Paleta.entrada, 1.18) : control.discreto ? "transparent" : Paleta.entrada
        border.width: control.visualFocus ? 2 : control.discreto ? 0 : 1
        border.color: control.visualFocus ? Paleta.acento : Paleta.borde
        Behavior on color { ColorAnimation { duration: 130 } }
    }
}
