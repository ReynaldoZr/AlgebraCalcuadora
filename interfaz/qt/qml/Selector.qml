import QtQuick
import QtQuick.Controls

ComboBox {
    id: control
    implicitHeight: 39
    font.pixelSize: 13
    leftPadding: 11
    rightPadding: 27
    readonly property bool dosColumnas: control.count > 6

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
        border.color: control.visualFocus || control.popup.visible ? Paleta.acento : Paleta.borde
    }
    indicator: Text {
        x: control.width - width - 12
        anchors.verticalCenter: parent.verticalCenter
        text: "⌄"
        color: Paleta.secundario
        font.pixelSize: 18
    }
    delegate: ItemDelegate {
        id: itemDel
        required property int index
        width: control.dosColumnas ? Math.floor((contenido.width - 8) / 2) : contenido.width
        height: 36
        padding: 0
        hoverEnabled: true
        text: control.textRole ? control.model[index][control.textRole] : control.model[index]
        readonly property bool seleccionado: control.currentIndex === index
        highlighted: control.highlightedIndex === index

        contentItem: Row {
            anchors.fill: parent
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            spacing: 6
            Text {
                width: parent.width - (itemDel.seleccionado ? 18 : 0)
                anchors.verticalCenter: parent.verticalCenter
                text: itemDel.text
                color: itemDel.seleccionado ? Paleta.sobreAcento : Paleta.texto
                font.pixelSize: 13
                font.bold: itemDel.seleccionado
                elide: Text.ElideRight
            }
            Text {
                visible: itemDel.seleccionado
                anchors.verticalCenter: parent.verticalCenter
                text: "✓"
                color: Paleta.sobreAcento
                font.pixelSize: 12
                font.bold: true
            }
        }
        background: Rectangle {
            anchors.fill: parent
            anchors.margins: 2
            radius: 6
            color: itemDel.seleccionado
                   ? Paleta.acento
                   : (itemDel.hovered || itemDel.highlighted ? Paleta.tarjeta : "transparent")
            border.color: itemDel.hovered && !itemDel.seleccionado ? Paleta.borde : "transparent"
        }
    }
    popup: Popup {
        y: control.height + 4
        width: control.dosColumnas ? Math.max(control.width, 660) : control.width
        height: Math.min(380, contenido.contentHeight + 12)
        padding: 6
        contentItem: GridView {
            id: contenido
            clip: true
            cellWidth: control.dosColumnas ? Math.floor(width / 2) : width
            cellHeight: 36
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
            ScrollBar.vertical: ScrollBar { }
        }
        background: Rectangle {
            radius: 10
            color: Paleta.entrada
            border.color: Paleta.borde
        }
    }
}
