import QtQuick
import "Notacion.js" as Notacion

Flow {
    id: formula
    property var tokens: []
    property int tamano: 19
    spacing: 7
    Repeater {
        model: formula.tokens
        Fraccion {
            required property var modelData
            valor: ({
                arriba: Notacion.mostrarPotencias(modelData.arriba || ""),
                abajo: Notacion.mostrarPotencias(modelData.abajo || "")
            })
            tamano: formula.tamano
            anchoMaximo: formula.width
        }
    }
}
