import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: ventana
    objectName: "cuadernoQt"
    width: 1440
    height: 900
    minimumWidth: 1100
    minimumHeight: 760
    visible: true
    title: "Cuaderno de Álgebra Lineal · Qt Quick · Local"
    color: Paleta.fondo
    font.family: "Segoe UI"
    font.pixelSize: 13
    palette.text: Paleta.texto
    palette.windowText: Paleta.texto
    palette.base: Paleta.entrada
    palette.window: Paleta.tarjeta
    palette.button: Paleta.entrada
    palette.buttonText: Paleta.texto
    palette.highlight: Paleta.acento
    property string pagina: "inicio"
    property string vista: "calculadora"
    property string guardarTipo: "ejercicio"
    property string registroEditar: ""
    property bool registroHistorial: false
    property bool bibliotecaDesdeCalculadora: false
    property string copiaParaCargar: ""

    function cambiarPagina(nombre) {
        cuaderno.pausar()
        if (nombre === "biblioteca" && pagina !== nombre)
            bibliotecaDesdeCalculadora = pagina === "calculadora"
        pagina = nombre
        transicion.restart()
    }
    function abrirGuardado(tipo) {
        guardarTipo = tipo
        registroEditar = ""
        nombreGuardar.text = ""
        simboloGuardar.text = ""
        notasGuardar.text = ""
        guardarDialogo.open()
    }
    function abrirDimensiones(nombre, filas, columnas) {
        dimensiones.nombre = nombre
        filasDimension.value = filas
        columnasDimension.value = columnas
        dimensiones.open()
    }

    Shortcut { sequence: "Ctrl+Return"; enabled: pagina === "calculadora" && !cuaderno.estado.ocupado; onActivated: cuaderno.calcular() }
    Shortcut { sequence: "Ctrl+Z"; enabled: pagina === "calculadora" && !cuaderno.estado.ocupado; onActivated: cuaderno.deshacer() }
    onClosing: cuaderno.pausar()
    NumberAnimation { id: transicion; target: paginas; property: "opacity"; from: 0.6; to: 1; duration: 180; easing.type: Easing.OutCubic }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 24
        spacing: 18
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 52
            Rectangle { width: 42; height: 42; radius: 11; color: Paleta.acento; Label { anchors.centerIn: parent; text: "π"; color: Paleta.sobreAcento; font.pixelSize: 28; font.family: "Cambria" } }
            Label { text: "Cuaderno de Álgebra"; color: Paleta.texto; font.pixelSize: 21; font.bold: true; Layout.leftMargin: 10 }
            Item { Layout.fillWidth: true }
            Boton { text: "☰  Temas"; onClicked: temas.open(); enabled: !cuaderno.estado.ocupado }
            Boton { text: "Inicio"; discreto: pagina !== "inicio"; onClicked: ventana.cambiarPagina("inicio") }
            Boton { text: "Biblioteca"; discreto: pagina !== "biblioteca"; onClicked: ventana.cambiarPagina("biblioteca") }
            Boton { text: "Estudio ⌄"; onClicked: estudio.open() }
            Menu {
                id: estudio
                MenuItem { text: "Teoremas del tema"; onTriggered: cuaderno.consultar("Teoremas") }
                MenuItem { text: "Ayudas de estudio"; onTriggered: cuaderno.consultar("Ayudas") }
                MenuItem { text: "Exportar ejercicio a PDF…"; enabled: cuaderno.estado.vigente; onTriggered: cuaderno.exportar("", false) }
            }
            Boton { text: Paleta.oscuro ? "☀" : "☾"; Accessible.name: "Cambiar tema claro u oscuro"; onClicked: Paleta.oscuro = !Paleta.oscuro }
        }
        Rectangle { Layout.fillWidth: true; height: 1; color: Paleta.borde }

        StackLayout {
            id: paginas
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: ventana.pagina === "inicio" ? 0 : ventana.pagina === "biblioteca" ? 2 : 1

            ScrollView {
                contentWidth: availableWidth
                ColumnLayout {
                    width: parent.width
                    spacing: 24
                    Label { text: "Elige un tema para comenzar"; font.pixelSize: 29; font.bold: true; color: Paleta.texto; Layout.topMargin: 16 }
                    Label { text: "Tus herramientas, organizadas por unidad. Cada ejercicio conserva su lugar."; color: Paleta.secundario }
                    GridLayout {
                        columns: 3
                        columnSpacing: 16
                        rowSpacing: 16
                        Layout.fillWidth: true
                        Repeater {
                            model: cuaderno.temas
                            Button {
                                required property var modelData
                                Layout.fillWidth: true
                                Layout.preferredWidth: 350
                                Layout.preferredHeight: 156
                                padding: 22
                                hoverEnabled: true
                                onClicked: cuaderno.abrirTema(modelData.nombre)
                                background: Rectangle { radius: 14; color: parent.hovered ? Qt.lighter(Paleta.tarjeta, 1.12) : Paleta.tarjeta; border.color: parent.hovered ? Paleta.acento : Paleta.borde; Behavior on color { ColorAnimation { duration: 130 } } }
                                contentItem: ColumnLayout {
                                    spacing: 10
                                    RowLayout {
                                        Label { visible: modelData.nombre !== "Matrices"; text: modelData.simbolo; color: Paleta.acento; font.pixelSize: 27; Layout.preferredWidth: 46 }
                                        Grid { visible: modelData.nombre === "Matrices"; columns: 3; spacing: 3; Layout.preferredWidth: 46; Repeater { model: 9; Rectangle { width: 7; height: 7; color: "transparent"; border.color: Paleta.acento } } }
                                        Label { text: modelData.nombre; color: Paleta.texto; font.pixelSize: 19; font.bold: true; Layout.fillWidth: true }
                                        Label { text: "›"; color: Paleta.secundario; font.pixelSize: 23 }
                                    }
                                    Label { text: modelData.detalle; color: Paleta.secundario; Layout.fillWidth: true; wrapMode: Text.Wrap; font.pixelSize: 13 }
                                }
                            }
                        }
                    }
                    Label { text: "Los ejemplos se cargan cuando tú lo decides. Tus guardados e historial están en Biblioteca."; color: Paleta.secundario; Layout.fillWidth: true; wrapMode: Text.Wrap }
                }
            }

            ColumnLayout {
                spacing: 14
                RowLayout {
                    Label { text: cuaderno.formulario.tema || ""; color: Paleta.texto; font.pixelSize: 23; font.bold: true }
                    Item { Layout.fillWidth: true }
                    Boton { text: "Calculadora"; principal: ventana.vista === "calculadora"; onClicked: { ventana.vista = "calculadora"; transicion.restart() } }
                    Boton { text: "Todos los pasos"; principal: ventana.vista === "pasos"; onClicked: { cuaderno.pausar(); ventana.vista = "pasos"; transicion.restart() } }
                }
                RowLayout {
                    Layout.fillWidth: true
                    enabled: !cuaderno.estado.ocupado
                    Selector {
                        id: metodo
                        objectName: "selectorMetodo"
                        Layout.preferredWidth: 370
                        model: cuaderno.formulario.metodos || []
                        textRole: "nombre"
                        currentIndex: model.findIndex(m => m.clave === cuaderno.formulario.clave)
                        onActivated: cuaderno.seleccionar(model[currentIndex].clave)
                    }
                    Boton { text: "Cargar ejemplo"; enabled: cuaderno.formulario.ejemplo; onClicked: cuaderno.cargarEjemplo("") }
                    Boton { text: "Otros casos…"; enabled: cuaderno.formulario.ejemplo; onClicked: casos.open() }
                    Item { Layout.fillWidth: true }
                    Boton { text: "Teoremas"; discreto: true; onClicked: cuaderno.consultar("Teoremas") }
                }
                StackLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    currentIndex: ventana.vista === "calculadora" ? 0 : 1
                    ColumnLayout {
                        spacing: 12
                        RowLayout {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            spacing: 14
                            Tarjeta {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                Layout.preferredWidth: 400
                                enabled: !cuaderno.estado.ocupado
                                ScrollView {
                                    anchors.fill: parent
                                    contentWidth: availableWidth
                                    ColumnLayout {
                                        width: parent.width
                                        spacing: 13
                                        Label { visible: (cuaderno.formulario.matricesA?.length || 0) === 0; text: "Datos del ejercicio"; color: Paleta.texto; font.pixelSize: 17; font.bold: true }
                                        Repeater {
                                            model: cuaderno.formulario.matricesA || []
                                            EditorMatriz { required property var modelData; datos: modelData; Layout.fillWidth: true; onGuardar: nombre => ventana.abrirGuardado(nombre); onDimensiones: (nombre, filas, columnas) => ventana.abrirDimensiones(nombre, filas, columnas) }
                                        }
                                        Repeater { model: cuaderno.formulario.camposA || []; Campo { required property var modelData; datos: modelData; Layout.fillWidth: true } }
                                        Label { visible: cuaderno.formulario.clave === "num_flotante"; text: "No necesitas escribir datos.\n\nPulsa Calcular para ver los experimentos de punto flotante."; color: Paleta.secundario; Layout.fillWidth: true; wrapMode: Text.Wrap }
                                    }
                                }
                            }
                            Tarjeta {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                Layout.preferredWidth: 340
                                enabled: !cuaderno.estado.ocupado
                                ScrollView {
                                    anchors.fill: parent
                                    contentWidth: availableWidth
                                    ColumnLayout {
                                        width: parent.width
                                        spacing: 13
                                        Label { visible: (cuaderno.formulario.matricesB?.length || 0) === 0; text: "Opciones y referencia"; color: Paleta.texto; font.pixelSize: 17; font.bold: true }
                                        Repeater {
                                            model: cuaderno.formulario.matricesB || []
                                            EditorMatriz { required property var modelData; datos: modelData; Layout.fillWidth: true; onGuardar: nombre => ventana.abrirGuardado(nombre); onDimensiones: (nombre, filas, columnas) => ventana.abrirDimensiones(nombre, filas, columnas) }
                                        }
                                        Repeater { model: cuaderno.formulario.camposB || []; Campo { required property var modelData; datos: modelData; Layout.fillWidth: true } }
                                        Label { text: cuaderno.formulario.ayuda || ""; color: Paleta.secundario; Layout.fillWidth: true; wrapMode: Text.Wrap; font.pixelSize: 12; lineHeight: 1.25 }
                                    }
                                }
                            }
                            Tarjeta {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                Layout.preferredWidth: 390
                                ColumnLayout {
                                    anchors.fill: parent
                                    spacing: 12
                                    Label { text: cuaderno.formulario.tema === "Numéricos" ? "Resultado aproximado" : "Resultado exacto"; color: Paleta.texto; font.pixelSize: 17; font.bold: true }
                                    Label { visible: !cuaderno.estado.vigente && (cuaderno.resultado.pasos?.length || 0) > 0; text: "Resultado anterior · Recalcula para actualizar"; color: Paleta.acento; Layout.fillWidth: true; wrapMode: Text.Wrap; font.pixelSize: 12 }
                                    ScrollView {
                                        Layout.fillWidth: true
                                        Layout.fillHeight: true
                                        contentWidth: availableWidth
                                        ColumnLayout {
                                            width: parent.width
                                            spacing: 14
                                            MatrizVista { visible: (cuaderno.resultado.matriz?.length || 0) > 0; matriz: cuaderno.resultado.matriz || []; Layout.fillWidth: true }
                                            TextArea { objectName: "resumenResultado"; text: cuaderno.resultado.resumen || "Todavía no hay resultado."; readOnly: true; selectByMouse: true; wrapMode: TextEdit.Wrap; color: Paleta.texto; font.pixelSize: 13; Layout.fillWidth: true; background: null }
                                        }
                                    }
                                    RowLayout {
                                        Layout.fillWidth: true
                                        Boton {
                                            text: "Guardar resultado…"
                                            objectName: "guardarResultado"
                                            enabled: cuaderno.estado.vigente
                                            Layout.fillWidth: true
                                            onClicked: ventana.abrirGuardado("resultado")
                                        }
                                        Boton {
                                            objectName: "cargarEjercicioGuardado"
                                            text: "Cargar guardado"
                                            enabled: !cuaderno.estado.ocupado
                                            Layout.fillWidth: true
                                            onClicked: ejerciciosGuardados.open()
                                        }
                                    }
                                    RowLayout {
                                        visible: cuaderno.estado.matriz
                                        Layout.fillWidth: true
                                        Boton { text: "Copiar o usar matriz ⌄"; Layout.fillWidth: true; onClicked: resultadoMenu.open() }
                                        Menu {
                                            id: resultadoMenu
                                            MenuItem { text: "Copiar resultado"; onTriggered: cuaderno.copiarMatriz("Resultado") }
                                            Repeater { model: cuaderno.estado.destinos; MenuItem { required property var modelData; text: "Usar como " + modelData; onTriggered: cuaderno.usarResultado(modelData) } }
                                        }
                                    }
                                }
                            }
                        }
                        RowLayout {
                            Layout.fillWidth: true
                            Boton { objectName: "calcular"; text: cuaderno.estado.ocupado ? "Calculando…" : "▶  Calcular"; principal: true; enabled: !cuaderno.estado.ocupado; onClicked: cuaderno.calcular() }
                            Boton { text: "Limpiar"; enabled: !cuaderno.estado.ocupado; onClicked: cuaderno.limpiar() }
                            Boton { text: "Deshacer"; enabled: cuaderno.estado.deshacer && !cuaderno.estado.ocupado; onClicked: cuaderno.deshacer() }
                            Item { Layout.fillWidth: true }
                            BusyIndicator { running: cuaderno.estado.ocupado; visible: running; implicitWidth: 30; implicitHeight: 30 }
                            Boton { text: "Ver gráfica"; enabled: cuaderno.estado.graficable; onClicked: cuaderno.verGrafica(Paleta.oscuro) }
                        }
                        Tarjeta {
                            Layout.fillWidth: true
                            Layout.preferredHeight: Math.max(165, resumenPaso.implicitHeight + 100)
                            ColumnLayout {
                                anchors.fill: parent
                                spacing: 9
                                RowLayout {
                                    Label { text: "Vista previa"; color: Paleta.texto; font.bold: true; font.pixelSize: 15 }
                                    Label { text: cuaderno.previa.total ? (cuaderno.previa.indice + 1) + " / " + cuaderno.previa.total : ""; color: Paleta.acento; font.pixelSize: 12 }
                                    Item { Layout.fillWidth: true }
                                    Boton { text: "Ver todos los pasos ↗"; discreto: true; implicitHeight: 26; onClicked: { cuaderno.pausar(); ventana.vista = "pasos"; transicion.restart() } }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 24
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        Layout.preferredWidth: 500
                                        Label { id: resumenPaso; text: cuaderno.previa.titulo || "Calcula para ver el procedimiento"; color: Paleta.acento; font.bold: true; font.pixelSize: 14; wrapMode: Text.Wrap; Layout.fillWidth: true }
                                        Repeater { model: cuaderno.previa.formulas || []; Formula { required property var modelData; tokens: modelData; tamano: 17; Layout.fillWidth: true } }
                                    }
                                    Label { text: (cuaderno.previa.origen ? cuaderno.previa.origen + "\n" : "") + (cuaderno.previa.detalle || "Las explicaciones esenciales aparecerán aquí. Todos los pasos conserva el desarrollo completo."); color: Paleta.secundario; wrapMode: Text.Wrap; Layout.fillWidth: true; Layout.preferredWidth: 450; font.pixelSize: 12 }
                                }
                                RowLayout {
                                    Layout.fillWidth: true
                                    enabled: cuaderno.estado.vigente
                                    Boton { text: "‹ Anterior"; implicitHeight: 31; onClicked: cuaderno.anterior() }
                                    Boton { text: cuaderno.estado.reproduciendo ? "Ⅱ Pausar" : "▶ Reproducir"; principal: true; implicitHeight: 31; onClicked: cuaderno.reproducir() }
                                    Boton { text: "Siguiente ›"; implicitHeight: 31; onClicked: { cuaderno.pausar(); cuaderno.siguiente() } }
                                    Boton { text: "Reiniciar"; discreto: true; implicitHeight: 31; onClicked: cuaderno.reiniciar() }
                                    Item { Layout.fillWidth: true }
                                    Label { text: "2 segundos por etapa"; color: Paleta.secundario; font.pixelSize: 11 }
                                }
                            }
                        }
                    }
                    Pasos { }
                }
            }
            Biblioteca {
                puedeVolver: ventana.bibliotecaDesdeCalculadora
                onVolverCalculadora: {
                    ventana.vista = "calculadora"
                    ventana.cambiarPagina("calculadora")
                }
                onEjercicioCopiado: identificador => {
                    ventana.copiaParaCargar = identificador
                    ventana.bibliotecaDesdeCalculadora = true
                }
                onAbrirEdicion: (registro, historial) => {
                    ventana.registroEditar = registro.id
                    ventana.registroHistorial = historial
                    nombreGuardar.text = historial ? "" : registro.nombre
                    simboloGuardar.text = registro.simbolo
                    notasGuardar.text = registro.notas
                    guardarDialogo.open()
                }
                onConfirmarEliminacion: (identificador, historial) => {
                    eliminar.identificador = identificador
                    eliminar.historial = historial
                    eliminar.open()
                }
            }
        }
        Label { objectName: "estado"; text: cuaderno.estado.mensaje; color: cuaderno.estado.error ? Paleta.error : Paleta.secundario; wrapMode: Text.Wrap; Layout.fillWidth: true; font.pixelSize: 12 }
    }

    EjerciciosGuardados {
        id: ejerciciosGuardados
        preferido: ventana.copiaParaCargar
        onCargar: (identificador, destino, ejercicio) => {
            ventana.copiaParaCargar = ""
            if (ejercicio)
                cuaderno.abrirGuardado(identificador, false)
            else
                cuaderno.usarGuardado(identificador, false, destino)
        }
    }

    Drawer {
        id: temas
        width: 310
        height: ventana.height
        background: Rectangle { color: Paleta.tarjeta; border.color: Paleta.borde }
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 10
            Label { text: "Temas"; color: Paleta.texto; font.pixelSize: 24; font.bold: true }
            Repeater { model: cuaderno.temas; Boton { required property var modelData; text: modelData.simbolo + "   " + modelData.nombre; Layout.fillWidth: true; onClicked: { temas.close(); cuaderno.abrirTema(modelData.nombre) } } }
            Item { Layout.fillHeight: true }
        }
    }
    Dialog {
        id: guardarDialogo
        objectName: "guardarDialogo"
        anchors.centerIn: parent
        width: 450
        modal: true
        title: ventana.registroEditar ? "Guardar nombre y notas" : "Guardar en Biblioteca"
        standardButtons: Dialog.Save | Dialog.Cancel
        background: Rectangle { radius: 14; color: Paleta.tarjeta; border.color: Paleta.borde }
        ColumnLayout {
            width: parent.width
            spacing: 12
            Label { text: "Deja el nombre vacío para usar uno automático."; color: Paleta.secundario; Layout.fillWidth: true; wrapMode: Text.Wrap }
            Entrada { id: nombreGuardar; Layout.fillWidth: true; placeholderText: "Nombre"; maximumLength: 120 }
            Entrada { id: simboloGuardar; Layout.fillWidth: true; placeholderText: "Símbolo opcional: Aᵀ, A₁…"; maximumLength: 24 }
            TextArea { id: notasGuardar; Layout.fillWidth: true; implicitHeight: 110; placeholderText: "Notas opcionales"; wrapMode: TextEdit.Wrap; color: Paleta.texto; background: Rectangle { radius: 8; color: Paleta.entrada; border.color: Paleta.borde } }
        }
        onAccepted: {
            if (ventana.registroEditar) cuaderno.editarGuardado(ventana.registroEditar, ventana.registroHistorial, nombreGuardar.text, simboloGuardar.text, notasGuardar.text)
            else cuaderno.guardar(ventana.guardarTipo, nombreGuardar.text, simboloGuardar.text, notasGuardar.text)
        }
    }
    Dialog {
        id: dimensiones
        property string nombre: "A"
        anchors.centerIn: parent
        width: 410
        modal: true
        title: "Tamaño de " + nombre
        standardButtons: Dialog.Apply | Dialog.Cancel
        background: Rectangle { radius: 14; color: Paleta.tarjeta; border.color: Paleta.borde }
        ColumnLayout {
            width: parent.width
            spacing: 14
            RowLayout {
                Label { text: "Filas"; color: Paleta.texto }
                SpinBox { id: filasDimension; from: 1; to: 10 }
                Label { text: "Columnas"; color: Paleta.texto }
                SpinBox { id: columnasDimension; from: 1; to: 10 }
            }
            Label { text: "Se conservan las celdas que coincidan. Al reducir, se quitarán las que queden fuera. Aplica solo si deseas continuar."; color: Paleta.secundario; wrapMode: Text.Wrap; Layout.fillWidth: true }
        }
        onApplied: { cuaderno.redimensionar(nombre, filasDimension.value, columnasDimension.value); close() }
    }
    Dialog {
        id: casos
        anchors.centerIn: parent
        width: 440
        modal: true
        title: "Ejemplos por caso"
        standardButtons: Dialog.Ok | Dialog.Cancel
        background: Rectangle { radius: 14; color: Paleta.tarjeta; border.color: Paleta.borde }
        Selector { id: caso; width: parent.width; model: cuaderno.formulario.casos || [] }
        onAccepted: cuaderno.cargarEjemplo(caso.currentText)
    }
    Dialog {
        id: consulta
        property string contenido: ""
        anchors.centerIn: parent
        width: Math.min(800, ventana.width - 80)
        height: Math.min(650, ventana.height - 100)
        modal: true
        standardButtons: Dialog.Close
        background: Rectangle { radius: 14; color: Paleta.tarjeta; border.color: Paleta.borde }
        ScrollView { anchors.fill: parent; contentWidth: availableWidth; TextArea { text: consulta.contenido; readOnly: true; selectByMouse: true; wrapMode: TextEdit.Wrap; color: Paleta.texto; background: null } }
    }
    Dialog {
        id: grafica
        anchors.centerIn: parent
        width: Math.min(1000, ventana.width - 60)
        height: Math.min(760, ventana.height - 70)
        modal: true
        title: "Gráfica del ejercicio"
        standardButtons: Dialog.Close
        background: Rectangle { radius: 14; color: Paleta.tarjeta; border.color: Paleta.borde }
        ColumnLayout {
            anchors.fill: parent
            Image { id: imagenGrafica; objectName: "imagenGrafica"; Layout.fillWidth: true; Layout.fillHeight: true; fillMode: Image.PreserveAspectFit; cache: false }
            Boton { text: "Guardar imagen…"; onClicked: cuaderno.guardarGrafica() }
        }
    }
    Dialog {
        id: eliminar
        property string identificador: ""
        property bool historial: false
        anchors.centerIn: parent
        width: 390
        title: "Eliminar elemento"
        modal: true
        standardButtons: Dialog.Yes | Dialog.No
        background: Rectangle { radius: 14; color: Paleta.tarjeta; border.color: Paleta.borde }
        Label { text: "¿Quieres eliminar este elemento de la Biblioteca?"; color: Paleta.texto; width: parent.width; wrapMode: Text.Wrap }
        onAccepted: cuaderno.eliminarGuardado(identificador, historial)
    }
    Connections {
        target: cuaderno
        function onNavegar(pagina) { ventana.vista = "calculadora"; ventana.cambiarPagina(pagina) }
        function onDialogoTexto(titulo, contenido) { consulta.title = titulo; consulta.contenido = contenido; consulta.open() }
        function onGraficaLista(fuente) { imagenGrafica.source = fuente; grafica.open() }
    }
}
