import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: raiz
    objectName: "resultadoIterativo"
    property var datos: ({})
    property bool mostrarDetalles: false
    spacing: 10
    onDatosChanged: mostrarDetalles = false

    Label {
        objectName: "estadoGeneralIterativo"
        text: raiz.datos.estado_general || ""
        visible: text.length > 0
        color: Paleta.texto
        font.pixelSize: 13
        font.bold: true
        wrapMode: Text.Wrap
        Layout.fillWidth: true
        Accessible.name: text
    }

    Label {
        objectName: "comparacionIteraciones"
        text: raiz.datos.comparacion_iteraciones || ""
        visible: text.length > 0
        color: Paleta.acento
        font.pixelSize: 12
        font.bold: true
        wrapMode: Text.Wrap
        Layout.fillWidth: true
    }

    Repeater {
        model: raiz.datos.advertencias || []
        Rectangle {
            required property var modelData
            Layout.fillWidth: true
            implicitHeight: avisoTxt.implicitHeight + 12
            radius: 8
            color: Paleta.entrada
            border.color: Paleta.error
            Label {
                id: avisoTxt
                anchors.fill: parent
                anchors.margins: 6
                text: modelData
                color: Paleta.error
                font.pixelSize: 12
                wrapMode: Text.Wrap
            }
        }
    }

    RowLayout {
        Layout.fillWidth: true
        spacing: 8
        visible: (raiz.datos.metodos?.length || 0) > 0
        Repeater {
            model: raiz.datos.metodos || []
            Rectangle {
                required property var modelData
                Layout.fillWidth: true
                implicitHeight: metodoCol.implicitHeight + 14
                radius: 8
                color: Paleta.entrada
                border.color: modelData.convergio ? Paleta.borde : Paleta.error
                ColumnLayout {
                    id: metodoCol
                    anchors.fill: parent
                    anchors.margins: 7
                    spacing: 2
                    Label { text: modelData.nombre; color: Paleta.texto; font.bold: true; font.pixelSize: 12; Layout.fillWidth: true; elide: Text.ElideRight }
                    Label { text: modelData.iteraciones + " iteraciones"; color: Paleta.acento; font.bold: true; font.pixelSize: 13; Layout.fillWidth: true }
                    Label { text: modelData.estado; color: modelData.convergio ? Paleta.secundario : Paleta.error; font.pixelSize: 11; wrapMode: Text.Wrap; Layout.fillWidth: true }
                }
            }
        }
    }

    Rectangle {
        Layout.fillWidth: true
        implicitHeight: Math.min(250, tablaContenedor.implicitHeight + 4)
        radius: 8
        color: Paleta.entrada
        border.color: Paleta.borde
        clip: true

        Flickable {
            id: tablaScroll
            objectName: "tablaResumenIterativo"
            anchors.fill: parent
            anchors.margins: 2
            readonly property int numCols: raiz.datos.columnas?.length || 1
            readonly property real colAncho: Math.max(76, (width - 4) / numCols)
            contentWidth: Math.max(width, numCols * colAncho)
            contentHeight: tablaContenedor.implicitHeight
            flickableDirection: Flickable.AutoFlickDirection
            boundsBehavior: Flickable.StopAtBounds
            clip: true
            ScrollBar.horizontal: ScrollBar { }
            ScrollBar.vertical: ScrollBar { }

            Column {
                id: tablaContenedor
                width: tablaScroll.contentWidth

                Rectangle {
                    width: parent.width
                    height: 30
                    color: Paleta.tarjeta
                    Row {
                        anchors.fill: parent
                        Repeater {
                            model: raiz.datos.columnas || []
                            Label {
                                required property var modelData
                                width: tablaScroll.colAncho
                                height: 30
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                                text: modelData
                                color: Paleta.acento
                                font.bold: true
                                font.pixelSize: 11
                                elide: Text.ElideRight
                                padding: 4
                                ToolTip.visible: hovCol.hovered
                                ToolTip.text: text
                                HoverHandler { id: hovCol }
                            }
                        }
                    }
                }

                Repeater {
                    model: raiz.datos.filas || []
                    Rectangle {
                        required property var modelData
                        required property int index
                        width: tablaContenedor.width
                        height: 28
                        color: index % 2 === 0 ? Paleta.entrada : Paleta.tarjeta
                        Row {
                            anchors.fill: parent
                            Repeater {
                                model: modelData
                                Label {
                                    required property var modelData
                                    required property int index
                                    width: tablaScroll.colAncho
                                    height: 28
                                    verticalAlignment: Text.AlignVCenter
                                    horizontalAlignment: Text.AlignHCenter
                                    text: modelData
                                    color: Paleta.texto
                                    font.bold: index === 0
                                    font.pixelSize: 12
                                    elide: Text.ElideRight
                                    padding: 4
                                    ToolTip.visible: hovCelda.hovered
                                    ToolTip.text: text
                                    HoverHandler { id: hovCelda }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Label {
        readonly property string textoNotas: [raiz.datos.nota_referencia || "", raiz.datos.nota_precision || ""].filter(t => t.length > 0).join("\n")
        text: textoNotas
        visible: textoNotas.length > 0
        color: Paleta.secundario
        font.pixelSize: 11
        wrapMode: Text.Wrap
        Layout.fillWidth: true
    }

    Rectangle {
        Layout.fillWidth: true
        visible: (raiz.datos.metodos?.length || 0) > 0 || (raiz.datos.explicacion_residuo || "").length > 0
        implicitHeight: residuoCol.implicitHeight + 16
        radius: 8
        color: Paleta.entrada
        border.color: Paleta.borde
        ColumnLayout {
            id: residuoCol
            anchors.fill: parent
            anchors.margins: 8
            spacing: 4
            Label { visible: (raiz.datos.metodos?.length || 0) > 0; text: raiz.datos.titulo_residuo || "Residuo (ajuste de las ecuaciones)"; color: Paleta.texto; font.bold: true; font.pixelSize: 12; Layout.fillWidth: true; wrapMode: Text.Wrap }
            Repeater {
                model: raiz.datos.metodos || []
                Label {
                    required property var modelData
                    text: modelData.nombre + ": " + modelData.residuo_corto + "  ·  " + (modelData.etiqueta_error || "Cambio entre iteraciones") + ": " + modelData.error_corto
                    color: Paleta.texto
                    font.pixelSize: 12
                    wrapMode: Text.Wrap
                    Layout.fillWidth: true
                }
            }
            Label {
                text: raiz.datos.explicacion_residuo || ""
                color: Paleta.secundario
                font.pixelSize: 11
                wrapMode: Text.Wrap
                Layout.fillWidth: true
            }
        }
    }

    Boton {
        objectName: "verDetallesTecnicos"
        discreto: true
        activeFocusOnTab: true
        Layout.fillWidth: true
        text: raiz.mostrarDetalles ? "Ocultar detalles técnicos ▴" : "Ver detalles técnicos ▾"
        Accessible.name: text
        onClicked: raiz.mostrarDetalles = !raiz.mostrarDetalles
    }

    Rectangle {
        objectName: "panelDetallesTecnicos"
        visible: raiz.mostrarDetalles
        Layout.fillWidth: true
        implicitHeight: detallesCol.implicitHeight + 16
        radius: 8
        color: Paleta.entrada
        border.color: Paleta.borde
        ColumnLayout {
            id: detallesCol
            anchors.fill: parent
            anchors.margins: 8
            spacing: 6
            Repeater {
                model: raiz.datos.detalles_tecnicos || []
                ColumnLayout {
                    required property var modelData
                    Layout.fillWidth: true
                    spacing: 1
                    Label { text: modelData.titulo; color: Paleta.acento; font.bold: true; font.pixelSize: 11; Layout.fillWidth: true; wrapMode: Text.Wrap }
                    TextEdit {
                        text: modelData.valor
                        readOnly: true
                        selectByMouse: true
                        wrapMode: TextEdit.Wrap
                        color: Paleta.texto
                        font.pixelSize: 12
                        Layout.fillWidth: true
                    }
                }
            }
        }
    }
}
