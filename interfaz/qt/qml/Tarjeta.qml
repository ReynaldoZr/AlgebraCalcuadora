import QtQuick
import QtQuick.Controls

Frame {
    padding: 18
    background: Rectangle {
        radius: 14
        color: Paleta.tarjeta
        border.color: Paleta.borde
        Behavior on color { ColorAnimation { duration: 160 } }
    }
}
