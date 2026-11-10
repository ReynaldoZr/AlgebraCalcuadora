import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: editor
    property var datos: ({nombre: "A", filas: 2, columnas: 2, celdas: []})
    signal guardar(string nombre)
    signal dimensiones(string nombre, int filas, int columnas)
    spacing: 12
    RowLayout {
        Layout.fillWidth: true
        Label { text: "Matriz " + editor.datos.nombre; color: Paleta.texto; font.pixelSize: 17; font.bold: true }
        Item { Layout.fillWidth: true }
        Boton { text: "···"; discreto: true; onClicked: herramientas.open() }
        Menu {
            id: herramientas
            MenuItem { text: "Copiar matriz"; onTriggered: cuaderno.copiarMatriz(editor.datos.nombre) }
            MenuItem { text: "Pegar matriz"; onTriggered: cuaderno.pegarMatriz(editor.datos.nombre) }
            MenuItem { text: "Guardar matriz…"; onTriggered: editor.guardar(editor.datos.nombre) }
        }
    }
    Boton { text: editor.datos.filas + " × " + editor.datos.columnas + " · Cambiar"; implicitHeight: 32; onClicked: editor.dimensiones(editor.datos.nombre, editor.datos.filas, editor.datos.columnas) }
    Flickable {
        Layout.fillWidth: true
        implicitHeight: Math.min(330, rejilla.implicitHeight + 24)
        contentWidth: Math.max(width, rejilla.implicitWidth + 28)
        contentHeight: rejilla.implicitHeight + 24
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        ScrollBar.horizontal: ScrollBar { }
        ScrollBar.vertical: ScrollBar { }
        Grid {
            id: rejilla
            x: Math.max(12, (parent.width - implicitWidth) / 2)
            y: 8
            columns: editor.datos.columnas
            spacing: 7
            Repeater {
                model: editor.datos.celdas
                Entrada {
                    required property var modelData
                    objectName: "celda_" + editor.datos.nombre + "_" + modelData.fila + "_" + modelData.columna
                    width: Math.max(65, ...text.split("/").map(p => p.length * 9 + 20))
                    height: 47
                    horizontalAlignment: Text.AlignHCenter
                    text: modelData.valor
                    color: activeFocus || text.trim().length === 0 ? Paleta.texto : "transparent"
                    placeholderText: "·"
                    Accessible.name: editor.datos.nombre + ", fila " + (modelData.fila + 1) + ", columna " + (modelData.columna + 1)
                    onTextEdited: cuaderno.editarCelda(editor.datos.nombre, modelData.fila, modelData.columna, text)
                    Fraccion {
                        anchors.centerIn: parent
                        visible: !parent.activeFocus && parent.text.trim().length > 0
                        valor: parent.text.split("/").length === 2 ? ({arriba: parent.text.split("/")[0], abajo: parent.text.split("/")[1]}) : ({arriba: parent.text, abajo: ""})
                        tamano: 17
                    }
                    background: Rectangle {
                        readonly property var p: cuaderno.previa
                        readonly property bool marcada: p.signo === "AB" ? (editor.datos.nombre === "A" && p.fila === modelData.fila) || (editor.datos.nombre === "B" && p.columna === modelData.columna) : p.fila === modelData.fila && p.columna === modelData.columna
                        readonly property bool parActivo: p.signo === "AB" && p.par >= 0 && ((editor.datos.nombre === "A" && p.fila === modelData.fila && p.par === modelData.columna) || (editor.datos.nombre === "B" && p.columna === modelData.columna && p.par === modelData.fila))
                        radius: 7
                        color: marcada ? Qt.rgba(Paleta.acento.r, Paleta.acento.g, Paleta.acento.b, parActivo ? 0.35 : 0.15) : Paleta.entrada
                        border.color: parent.activeFocus || marcada ? Paleta.acento : Paleta.borde
                        border.width: parent.activeFocus || parActivo ? 2 : 1
                    }
                }
            }
        }
    }
}
