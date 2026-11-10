import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "Notacion.js" as Notacion

ColumnLayout {
    id: pagina
    readonly property bool hayTabla: (cuaderno.resultado.tabla?.filas?.length || 0) > 0
    property bool tablaAbierta: false
    spacing: 14
    onVisibleChanged: {
        if (!visible) tablaAbierta = false
    }
    Connections {
        target: cuaderno
        function onResultadoCambiado() { pagina.tablaAbierta = false }
    }
    RowLayout {
        spacing: 12
        Label { text: pagina.tablaAbierta ? "Tabla del cálculo" : "Todos los pasos"; color: Paleta.texto; font.pixelSize: 23; font.bold: true }
        Boton {
            objectName: "mostrarTabla"
            visible: pagina.hayTabla
            text: pagina.tablaAbierta ? "Volver a los pasos" : "Mostrar tabla"
            onClicked: pagina.tablaAbierta = !pagina.tablaAbierta
        }
    }
    Label { visible: !cuaderno.estado.vigente; text: cuaderno.resultado.pasos && cuaderno.resultado.pasos.length ? "Cálculo anterior · Recalcula para actualizarlo." : "Calcula un ejercicio para ver su desarrollo completo."; color: Paleta.acento }
    // Cada vista utiliza el área disponible y conserva su desplazamiento.
    Tarjeta {
        objectName: "tablaPasos"
        visible: pagina.hayTabla && pagina.tablaAbierta
        Layout.fillWidth: true
        Layout.fillHeight: true
        padding: 18
        Flickable {
            id: tabla
            readonly property int totalColumnas: cuaderno.resultado.tabla?.columnas?.length || 0
            readonly property real anchoColumna: Math.max(155, (width - 12) / Math.max(1, totalColumnas))
            anchors.fill: parent
            contentWidth: Math.max(width, totalColumnas * anchoColumna + 12)
            contentHeight: height
            clip: true
            ScrollBar.horizontal: ScrollBar { }
            ColumnLayout {
                width: parent.contentWidth
                height: parent.height - 12
                spacing: 6
                Row {
                    Repeater {
                        model: cuaderno.resultado.tabla?.columnas || []
                        Label { required property var modelData; text: modelData; color: Paleta.acento; font.bold: true; width: tabla.anchoColumna; padding: 8 }
                    }
                }
                ListView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    model: cuaderno.resultado.tabla?.filas || []
                    reuseItems: true
                    ScrollBar.vertical: ScrollBar { }
                    delegate: Row {
                        required property var modelData
                        height: 36
                        Repeater {
                            model: parent.modelData
                            Label { required property var modelData; text: modelData; width: tabla.anchoColumna; padding: 8; color: Paleta.texto; font.pixelSize: 13; elide: Text.ElideRight; ToolTip.visible: hover.hovered; ToolTip.text: text; HoverHandler { id: hover } }
                        }
                    }
                }
            }
        }
    }
    ListView {
        id: lista
        objectName: "listaPasos"
        visible: !pagina.tablaAbierta
        Layout.fillWidth: true
        Layout.fillHeight: true
        clip: true
        spacing: 16
        model: cuaderno.resultado.pasos || []
        reuseItems: true
        ScrollBar.vertical: ScrollBar { }
        delegate: Tarjeta {
            required property var modelData
            required property int index
            width: lista.width - 12
            padding: 22
            height: Math.max(120, contenido.implicitHeight + topPadding + bottomPadding)
            ColumnLayout {
                id: contenido
                width: parent.width
                spacing: 14
                Label { text: (index + 1) + ". " + Notacion.mostrarPotencias(modelData.titulo); textFormat: Text.PlainText; color: Paleta.texto; font.pixelSize: 16; font.bold: true; Layout.fillWidth: true; wrapMode: Text.Wrap }
                Label {
                    text: Notacion.mostrarPotencias(modelData.detalle)
                    visible: text.length > 0
                    textFormat: Text.PlainText
                    color: Paleta.secundario
                    Layout.fillWidth: true
                    wrapMode: Text.Wrap
                    font.pixelSize: 14
                    lineHeight: 1.2
                }
                Repeater {
                    model: modelData.formulas
                    Formula { required property var modelData; tokens: modelData; Layout.fillWidth: true }
                }
                MatrizVista { visible: modelData.matriz.length > 0; matriz: modelData.matriz; separador: modelData.separador; Layout.fillWidth: true }
            }
        }
        onModelChanged: positionViewAtBeginning()
    }
}
