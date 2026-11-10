import QtQuick
import QtQuick.Controls

Flickable {
    id: vista
    property var matriz: []
    property int separador: 0
    readonly property var anchos: matriz.length ? matriz[0].map((v, j) => Math.max(64, ...matriz.map(f => Math.max(f[j].arriba.length, f[j].abajo.length) * 10 + 18))) : []
    implicitHeight: Math.min(300, cuerpo.implicitHeight + 22)
    contentWidth: Math.max(width, cuerpo.implicitWidth + 30)
    contentHeight: cuerpo.implicitHeight + 20
    clip: true
    boundsBehavior: Flickable.StopAtBounds
    ScrollBar.horizontal: ScrollBar { }
    ScrollBar.vertical: ScrollBar { }
    Row {
        id: cuerpo
        x: Math.max(8, (vista.width - implicitWidth) / 2)
        y: 8
        spacing: 6
        Text { text: "["; font.family: "Cambria"; font.pixelSize: Math.min(180, filas.implicitHeight); color: Paleta.secundario }
        Column {
            id: filas
            spacing: 10
            Repeater {
                model: vista.matriz
                Row {
                    required property var modelData
                    spacing: 5
                    Repeater {
                        model: parent.modelData
                        Item {
                            required property var modelData
                            required property int index
                            width: vista.anchos[index] || 64
                            height: Math.max(46, fraccion.height + 6)
                            Rectangle { visible: vista.separador > 0 && index === vista.separador; width: 1; height: parent.height; color: Paleta.acento }
                            Fraccion { id: fraccion; anchors.centerIn: parent; valor: parent.modelData; tamano: 17 }
                        }
                    }
                }
            }
        }
        Text { text: "]"; font.family: "Cambria"; font.pixelSize: Math.min(180, filas.implicitHeight); color: Paleta.secundario }
    }
}
