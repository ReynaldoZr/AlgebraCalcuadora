import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: dialogo
    property string preferido: ""
    readonly property var guardados: cuaderno.guardados
    readonly property var elegido: guardados[lista.currentIndex] || ({})
    readonly property var destinos: elegido.tipo === "matriz"
                                     ? cuaderno.estado.destinos.map(nombre => ({clave: nombre, etiqueta: "Matriz " + nombre}))
                                     : elegido.tipo === "resultado" && elegido.valor ? cuaderno.estado.destinosValores : []
    signal cargar(string identificador, string destino, bool ejercicio)

    objectName: "listaEjerciciosGuardados"
    anchors.centerIn: parent
    width: 480
    height: 370
    modal: true
    title: "Guardados"
    background: Rectangle {
        radius: 14
        color: Paleta.tarjeta
        border.color: Paleta.borde
    }
    onAboutToShow: {
        const indice = guardados.findIndex(registro => registro.id === preferido)
        lista.currentIndex = indice >= 0 ? indice : guardados.length ? 0 : -1
    }
    onOpened: {
        if (lista.currentIndex >= 0)
            lista.positionViewAtIndex(lista.currentIndex, ListView.Contain)
        lista.forceActiveFocus()
    }

    contentItem: ColumnLayout {
        spacing: 10
        ListView {
            id: lista
            objectName: "ejerciciosParaCargar"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            spacing: 6
            model: dialogo.guardados
            ScrollBar.vertical: ScrollBar {}
            Keys.onReturnPressed: {
                if (confirmar.enabled)
                    dialogo.accept()
            }
            Label {
                anchors.centerIn: parent
                visible: lista.count === 0
                text: "Todavía no hay elementos guardados."
                color: Paleta.secundario
            }
            delegate: ItemDelegate {
                id: fila
                required property var modelData
                required property int index
                width: lista.width - 12
                text: modelData.nombre + " · " + modelData.tipo
                highlighted: ListView.isCurrentItem
                onClicked: lista.currentIndex = index
                contentItem: Label {
                    text: fila.text
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    color: Paleta.texto
                }
                background: Rectangle {
                    radius: 8
                    color: Paleta.entrada
                    border.color: fila.highlighted ? Paleta.acento : Paleta.borde
                }
            }
        }
        Selector {
            id: destino
            objectName: "destinoResultadoGuardado"
            visible: dialogo.destinos.length > 0
            Layout.fillWidth: true
            model: dialogo.destinos
            textRole: "etiqueta"
            valueRole: "clave"
        }
        Label {
            visible: dialogo.elegido.tipo === "matriz" && dialogo.destinos.length === 0
            text: "Selecciona un método que reciba matrices para usar este resultado."
            color: Paleta.secundario
            Layout.fillWidth: true
            wrapMode: Text.Wrap
        }
    }
    footer: DialogButtonBox {
        Boton {
            text: "Cancelar"
            DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
        }
        Boton {
            id: confirmar
            objectName: "confirmarCargaEjercicio"
            text: dialogo.elegido.tipo === "ejercicio" ? "Cargar ejercicio"
                  : dialogo.elegido.tipo === "resultado" && dialogo.destinos.length === 0 ? "Copiar resultado" : "Usar resultado"
            principal: true
            enabled: !!dialogo.elegido.id
                     && (dialogo.destinos.length > 0 ? destino.currentIndex >= 0 : dialogo.elegido.tipo !== "matriz")
                     && !cuaderno.estado.ocupado
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
        }
    }
    onAccepted: {
        if (confirmar.enabled)
            cargar(elegido.id, destinos.length > 0 ? destino.currentValue : "", elegido.tipo === "ejercicio")
    }
}
