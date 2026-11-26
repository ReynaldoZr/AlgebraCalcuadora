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
        Layout.fillWidth: true
        spacing: 12
        Label { text: pagina.tablaAbierta ? "Tabla del cálculo" : "Todos los pasos"; color: Paleta.texto; font.pixelSize: 23; font.bold: true }
        Rectangle {
            visible: !pagina.tablaAbierta && (cuaderno.resultado.pasos?.length || 0) > 0
            radius: 10
            color: Paleta.entrada
            border.color: Paleta.borde
            implicitWidth: conteoPasos.implicitWidth + 16
            implicitHeight: conteoPasos.implicitHeight + 8
            Label {
                id: conteoPasos
                anchors.centerIn: parent
                text: (cuaderno.resultado.pasos?.length || 0) + " etapas"
                color: Paleta.secundario
                font.pixelSize: 12
                font.bold: true
            }
        }
        Boton {
            objectName: "mostrarTabla"
            visible: pagina.hayTabla
            text: pagina.tablaAbierta ? "Volver a los pasos" : "Mostrar tabla"
            onClicked: pagina.tablaAbierta = !pagina.tablaAbierta
        }
        Item { Layout.fillWidth: true }
        Boton {
            visible: !pagina.tablaAbierta && (cuaderno.resultado.pasos?.length || 0) > 2
            discreto: true
            text: "↑ Inicio"
            onClicked: lista.positionViewAtBeginning()
        }
        Boton {
            visible: !pagina.tablaAbierta && (cuaderno.resultado.pasos?.length || 0) > 2
            discreto: true
            text: "↓ Ir al final"
            onClicked: lista.positionViewAtEnd()
        }
    }
    Label { visible: !cuaderno.estado.vigente; text: cuaderno.resultado.pasos && cuaderno.resultado.pasos.length ? "Cálculo anterior · Recalcula para actualizarlo." : "Calcula un ejercicio para ver su desarrollo completo."; color: Paleta.acento }
    // Cada vista utiliza el área disponible y conserva su desplazamiento.
    StackLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        currentIndex: pagina.hayTabla && pagina.tablaAbierta ? 0 : 1

        Tarjeta {
            objectName: "tablaPasos"
            padding: 16
            Rectangle {
                anchors.fill: parent
                radius: 10
                color: Paleta.entrada
                border.color: Paleta.borde
                clip: true

                Flickable {
                    id: tabla
                    readonly property int totalColumnas: cuaderno.resultado.tabla?.columnas?.length || 0
                    readonly property real anchoColumna: Math.max(130, (width - 8) / Math.max(1, totalColumnas))
                    anchors.fill: parent
                    anchors.margins: 2
                    contentWidth: Math.max(width, totalColumnas * anchoColumna)
                    contentHeight: height
                    clip: true
                    ScrollBar.horizontal: ScrollBar { }
                    ColumnLayout {
                        width: tabla.contentWidth
                        height: tabla.height
                        spacing: 0

                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 40
                            implicitHeight: 40
                            color: Paleta.tarjeta
                            Row {
                                anchors.fill: parent
                                Repeater {
                                    model: cuaderno.resultado.tabla?.columnas || []
                                    Label {
                                        required property var modelData
                                        width: tabla.anchoColumna
                                        height: 40
                                        verticalAlignment: Text.AlignVCenter
                                        horizontalAlignment: Text.AlignLeft
                                        leftPadding: 12
                                        rightPadding: 8
                                        text: modelData
                                        color: Paleta.acento
                                        font.bold: true
                                        font.pixelSize: 13
                                        elide: Text.ElideRight
                                    }
                                }
                            }
                            Rectangle {
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.bottom: parent.bottom
                                height: 2
                                color: Paleta.acento
                            }
                        }

                        ListView {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.minimumHeight: 100
                            clip: true
                            model: cuaderno.resultado.tabla?.filas || []
                            ScrollBar.vertical: ScrollBar { }
                            delegate: Rectangle {
                                id: filaFondo
                                required property var modelData
                                required property int index
                                width: tabla.contentWidth
                                height: 38
                                implicitHeight: 38
                                color: filaHover.hovered ? Paleta.borde : (index % 2 === 0 ? Paleta.entrada : Paleta.tarjeta)
                                border.width: index + 1 === cuaderno.resultado.tabla.primeraTolerancia ? 2 : 0
                                border.color: Paleta.acento
                                HoverHandler { id: filaHover }
                                Row {
                                    anchors.fill: parent
                                    Repeater {
                                        model: filaFondo.modelData
                                        Label {
                                            required property var modelData
                                            required property int index
                                            width: tabla.anchoColumna
                                            height: 38
                                            verticalAlignment: Text.AlignVCenter
                                            horizontalAlignment: Text.AlignLeft
                                            leftPadding: 12
                                            rightPadding: 8
                                            text: modelData
                                            color: index === 0 ? Paleta.acento : Paleta.texto
                                            font.bold: index === 0
                                            font.pixelSize: 13
                                            elide: Text.ElideRight
                                            ToolTip.visible: hover.hovered
                                            ToolTip.text: text
                                            HoverHandler { id: hover }
                                        }
                                    }
                                }
                                Rectangle {
                                    anchors.left: parent.left
                                    anchors.right: parent.right
                                    anchors.bottom: parent.bottom
                                    height: 1
                                    color: Paleta.borde
                                    opacity: 0.35
                                }
                            }
                        }
                    }
                }
            }
        }
        ListView {
            id: lista
            objectName: "listaPasos"
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
                    spacing: 12
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 10
                        Rectangle {
                            width: Math.max(28, numPaso.implicitWidth + 12)
                            height: 26
                            radius: 13
                            color: Paleta.acento
                            Label {
                                id: numPaso
                                anchors.centerIn: parent
                                text: String(index + 1)
                                color: Paleta.sobreAcento
                                font.bold: true
                                font.pixelSize: 12
                            }
                        }
                        Label {
                            text: Notacion.mostrarPotencias(modelData.titulo)
                            textFormat: Text.PlainText
                            color: Paleta.texto
                            font.pixelSize: 16
                            font.bold: true
                            Layout.fillWidth: true
                            wrapMode: Text.Wrap
                        }
                    }
                    Rectangle { Layout.fillWidth: true; height: 1; color: Paleta.borde; opacity: 0.6 }
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
                        Rectangle {
                            required property var modelData
                            readonly property bool esDecision: modelData.some(t => String(t?.arriba || t || "").indexOf("¿Detener?") !== -1)
                            Layout.fillWidth: true
                            implicitHeight: formulaItem.implicitHeight + 16
                            radius: 8
                            color: Paleta.entrada
                            border.color: esDecision ? Paleta.acento : Paleta.borde
                            Formula {
                                id: formulaItem
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.margins: 10
                                tokens: modelData
                            }
                        }
                    }
                    MatrizVista { visible: modelData.matriz.length > 0; matriz: modelData.matriz; separador: modelData.separador; Layout.fillWidth: true }
                }
            }
            onModelChanged: positionViewAtBeginning()
        }
    }
}
