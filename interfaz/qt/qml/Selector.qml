import QtQuick
import QtQuick.Controls

ComboBox {
    id: control
    implicitHeight: 39
    font.pixelSize: 13
    leftPadding: 11
    rightPadding: 27
    contentItem: Text {
        text: control.displayText
        color: Paleta.texto
        font: control.font
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
    background: Rectangle {
        radius: 8
        color: Paleta.entrada
        border.color: control.visualFocus ? Paleta.acento : Paleta.borde
    }
    indicator: Text {
        x: control.width - width - 12
        anchors.verticalCenter: parent.verticalCenter
        text: "⌄"
        color: Paleta.secundario
        font.pixelSize: 18
    }
    delegate: ItemDelegate {
        required property int index
        width: control.width
        text: control.textRole ? control.model[index][control.textRole] : control.model[index]
        highlighted: control.highlightedIndex === index
        contentItem: Text { text: parent.text; color: Paleta.texto; font.pixelSize: 13; elide: Text.ElideRight }
        background: Rectangle { color: parent.highlighted ? Qt.lighter(Paleta.entrada, 1.3) : Paleta.entrada }
    }
    popup: Popup {
        y: control.height + 4
        width: control.width
        height: Math.min(360, contenido.implicitHeight + 8)
        padding: 4
        contentItem: ListView {
            id: contenido
            clip: true
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
            ScrollIndicator.vertical: ScrollIndicator { }
        }
        background: Rectangle { radius: 8; color: Paleta.entrada; border.color: Paleta.borde }
    }
}
