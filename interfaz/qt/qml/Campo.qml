import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "Notacion.js" as Notacion

ColumnLayout {
    id: campo
    property var datos: ({clave: "", etiqueta: "", valor: "", opciones: []})
    spacing: 6

    Label { text: campo.datos.etiqueta; color: Paleta.secundario; font.pixelSize: 12 }
    Loader {
        id: cargador
        Layout.fillWidth: true
        sourceComponent: campo.datos.opciones.length > 0 ? seleccion : entrada
    }
    Label {
        objectName: campo.datos.clave === "funcion" ? "previaFuncion" : ""
        visible: campo.datos.clave === "funcion" && text.length > 0
        Layout.fillWidth: true
        text: campo.datos.clave === "funcion" && cargador.item
              ? Notacion.mostrarPotencias(cargador.item.text.trim()) : ""
        textFormat: Text.PlainText
        wrapMode: Text.Wrap
        color: Paleta.acento
        font.pixelSize: 16
        Accessible.name: "Vista previa de la función: " + text
    }
    Component {
        id: seleccion
        Selector {
            model: campo.datos.opciones
            currentIndex: Math.max(0, model.indexOf(campo.datos.valor))
            onActivated: cuaderno.editarCampo(campo.datos.clave, currentText)
        }
    }
    Component {
        id: entrada
        Entrada {
            id: texto
            objectName: "campo_" + campo.datos.clave
            text: campo.datos.valor
            placeholderText: campo.datos.clave === "funcion" ? "Escribe una función o carga un ejemplo" : campo.datos.clave === "h" ? "Automático" : ""
            Accessible.name: campo.datos.etiqueta
            onTextEdited: cuaderno.editarCampo(campo.datos.clave, text)
        }
    }
    // El teclado actúa sobre el cursor del campo; solo Python evalúa la función.
    GridLayout {
        visible: campo.datos.clave === "funcion"
        Layout.fillWidth: true
        columns: 5
        columnSpacing: 5
        rowSpacing: 5
        Repeater {
            model: campo.datos.clave === "funcion" ? ["x", "+", "−", "×", "÷", "(", ")", "x²", "xⁿ", "⌫"] : []
            Boton {
                required property string modelData
                objectName: "signo_" + modelData
                text: modelData
                Layout.fillWidth: true
                implicitWidth: 35
                implicitHeight: 31
                focusPolicy: Qt.NoFocus
                onClicked: {
                    let entrada = cargador.item
                    if (!entrada) return
                    let inicio = entrada.selectionStart >= 0 && entrada.selectedText.length ? entrada.selectionStart : entrada.cursorPosition
                    let fin = entrada.selectionEnd >= 0 && entrada.selectedText.length ? entrada.selectionEnd : entrada.cursorPosition
                    let traduccion = {"−": "-", "×": "*", "÷": "/", "x²": "x^2", "xⁿ": "x^"}
                    let insertar = traduccion[modelData] || modelData
                    if (modelData === "⌫") { insertar = ""; if (inicio === fin) inicio = Math.max(0, inicio - 1) }
                    entrada.text = entrada.text.slice(0, inicio) + insertar + entrada.text.slice(fin)
                    entrada.cursorPosition = inicio + insertar.length
                    entrada.forceActiveFocus()
                    cuaderno.editarCampo(campo.datos.clave, entrada.text)
                }
            }
        }
    }
}
