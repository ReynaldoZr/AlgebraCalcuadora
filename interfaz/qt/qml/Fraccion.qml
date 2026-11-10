import QtQuick

Column {
    id: celda
    property var valor: ({arriba: "", abajo: ""})
    property int tamano: 19
    property real anchoMaximo: 0
    property color tinta: Paleta.texto
    spacing: 2
    readonly property real anchoNatural: Math.max(arriba.implicitWidth, abajo.visible ? abajo.implicitWidth : 0) + 8
    width: anchoMaximo > 8 ? Math.min(anchoNatural, anchoMaximo) : anchoNatural
    Text {
        id: arriba
        anchors.horizontalCenter: parent.horizontalCenter
        text: celda.valor.arriba || ""
        width: celda.width - 8
        textFormat: Text.PlainText
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.Wrap
        font.family: "Cambria"
        font.pixelSize: celda.tamano
        color: celda.tinta
    }
    Rectangle { visible: abajo.visible; width: parent.width; height: 1; color: celda.tinta }
    Text {
        id: abajo
        visible: text.length > 0
        anchors.horizontalCenter: parent.horizontalCenter
        text: celda.valor.abajo || ""
        width: celda.width - 8
        textFormat: Text.PlainText
        horizontalAlignment: Text.AlignHCenter
        wrapMode: Text.Wrap
        font.family: "Cambria"
        font.pixelSize: celda.tamano
        color: celda.tinta
    }
}
