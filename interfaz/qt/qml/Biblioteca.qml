import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: pagina
    property bool esHistorial: false
    property var elegido: ({})
    property bool puedeVolver: false
    signal abrirEdicion(var registro, bool historial)
    signal confirmarEliminacion(string identificador, bool historial)
    signal volverCalculadora()
    signal ejercicioCopiado(string identificador)
    spacing: 16
    RowLayout {
        Label { text: "Tu Biblioteca"; color: Paleta.texto; font.pixelSize: 24; font.bold: true; Layout.fillWidth: true }
        Boton {
            objectName: "volverDesdeBiblioteca"
            text: "‹ Volver a la calculadora"
            visible: pagina.puedeVolver
            onClicked: pagina.volverCalculadora()
        }
        Boton { text: "Guardados"; principal: !pagina.esHistorial; onClicked: { pagina.esHistorial = false; pagina.elegido = ({}) } }
        Boton { text: "Historial"; principal: pagina.esHistorial; onClicked: { pagina.esHistorial = true; pagina.elegido = ({}) } }
    }
    Entrada { id: buscar; objectName: "buscarBiblioteca"; Layout.fillWidth: true; placeholderText: "Buscar por nombre, símbolo, tema o notas…" }
    RowLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        spacing: 16
        Tarjeta {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 520
            ListView {
                id: elementos
                anchors.fill: parent
                clip: true
                spacing: 7
                model: (pagina.esHistorial ? cuaderno.historial : cuaderno.guardados).filter(r => (r.nombre + " " + r.simbolo + " " + r.tema + " " + r.notas).toLocaleLowerCase().includes(buscar.text.toLocaleLowerCase()))
                ScrollBar.vertical: ScrollBar { }
                Label { anchors.centerIn: parent; visible: elementos.count === 0; text: "No hay elementos para mostrar."; color: Paleta.secundario }
                delegate: ItemDelegate {
                    required property var modelData
                    objectName: "registro_" + modelData.id
                    width: elementos.width - 8
                    height: 79
                    onClicked: pagina.elegido = modelData
                    background: Rectangle { radius: 9; color: pagina.elegido.id === modelData.id ? Qt.rgba(Paleta.acento.r, Paleta.acento.g, Paleta.acento.b, 0.17) : Paleta.entrada; border.color: pagina.elegido.id === modelData.id ? Paleta.acento : Paleta.borde }
                    contentItem: RowLayout {
                        spacing: 14
                        Label { text: modelData.simbolo; color: Paleta.acento; font.pixelSize: 23; Layout.preferredWidth: 58; elide: Text.ElideRight }
                        ColumnLayout {
                            Layout.fillWidth: true
                            Label { text: modelData.nombre; color: Paleta.texto; font.bold: true; Layout.fillWidth: true; elide: Text.ElideRight }
                            Label { text: modelData.tema + " · " + modelData.tipo; color: Paleta.secundario; font.pixelSize: 12 }
                        }
                    }
                }
            }
        }
        Tarjeta {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 440
            ColumnLayout {
                anchors.fill: parent
                spacing: 12
                Label { text: pagina.elegido.nombre || "Selecciona un elemento"; color: Paleta.texto; font.pixelSize: 18; font.bold: true; Layout.fillWidth: true; wrapMode: Text.Wrap }
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    contentWidth: availableWidth
                    TextArea { text: (pagina.elegido.resumen || "Aquí podrás abrir ejercicios, guardar desde el historial o reutilizar una matriz.") + (pagina.elegido.notas ? "\n\n" + pagina.elegido.notas : "") + (pagina.elegido.resultado ? "\n\n" + pagina.elegido.resultado.map(f => "[ " + f.join("   ") + " ]").join("\n") : ""); color: Paleta.secundario; readOnly: true; wrapMode: TextEdit.Wrap; selectByMouse: true; background: null }
                }
                RowLayout {
                    Layout.fillWidth: true
                    Boton {
                        objectName: "abrirEjercicio"
                        text: "Abrir ejercicio"
                        principal: true
                        enabled: pagina.elegido.tipo === "ejercicio" && !cuaderno.estado.ocupado
                        Layout.fillWidth: true
                        onClicked: cuaderno.abrirGuardado(pagina.elegido.id, pagina.esHistorial)
                    }
                    Boton {
                        objectName: "copiarEjercicio"
                        text: "Copiar ejercicio"
                        visible: !pagina.esHistorial && pagina.elegido.tipo === "ejercicio"
                        enabled: !cuaderno.estado.ocupado
                        onClicked: {
                            const copia = cuaderno.copiarEjercicio(pagina.elegido.id)
                            if (copia.id) {
                                pagina.elegido = copia
                                elementos.positionViewAtBeginning()
                                pagina.ejercicioCopiado(copia.id)
                            }
                        }
                    }
                }
                RowLayout {
                    Layout.fillWidth: true
                    Selector {
                        id: destino
                        model: pagina.elegido.tipo === "resultado"
                               ? (pagina.elegido.valor ? cuaderno.estado.destinosValores : [])
                               : cuaderno.estado.destinos.map(nombre => ({clave: nombre, etiqueta: nombre}))
                        textRole: "etiqueta"
                        valueRole: "clave"
                        visible: pagina.elegido.tipo !== "resultado" || count > 0
                        Layout.fillWidth: true
                    }
                    Boton {
                        text: pagina.elegido.tipo === "resultado" && destino.count === 0
                              ? "Copiar resultado" : "Usar como " + destino.currentText
                        enabled: !cuaderno.estado.ocupado && (pagina.elegido.tipo === "resultado"
                                 ? destino.count === 0 || destino.currentIndex >= 0
                                 : !!pagina.elegido.resultado && destino.currentIndex >= 0)
                        onClicked: cuaderno.usarGuardado(pagina.elegido.id, pagina.esHistorial,
                                                        destino.count > 0 ? destino.currentValue : "")
                    }
                }
                Boton { text: pagina.esHistorial ? "Guardar permanentemente…" : "Editar nombre y notas…"; enabled: !!pagina.elegido.id; Layout.fillWidth: true; onClicked: pagina.abrirEdicion(pagina.elegido, pagina.esHistorial) }
                RowLayout {
                    Layout.fillWidth: true
                    Boton { text: "Exportar PDF"; enabled: !!pagina.elegido.id; Layout.fillWidth: true; onClicked: cuaderno.exportar(pagina.elegido.id, pagina.esHistorial) }
                    Boton { text: "Eliminar…"; enabled: !!pagina.elegido.id; onClicked: pagina.confirmarEliminacion(pagina.elegido.id, pagina.esHistorial) }
                }
            }
        }
    }
    Connections { target: cuaderno; function onBibliotecaCambiada() { pagina.elegido = ({}) } }
}
