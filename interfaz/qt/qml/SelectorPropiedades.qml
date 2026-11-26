import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: panel
    objectName: "selectorPropiedades"
    property bool numericos: false
    required property var metodos
    required property string actual
    signal elegir(string clave)
    signal volver()
    spacing: 10
    readonly property real escalaTarjetas: Math.max(1, Math.min(1.2, lista.height / 475, lista.width / 1240))

    function nombre(clave) {
        for (const columna of columnas)
            for (const grupo of columna)
                for (const item of grupo.items)
                    if (item.clave === clave)
                        return item.nombre
        return "Comprobar todas las propiedades"
    }

    function reiniciar() {
        buscar.clear()
        lista.contentItem.contentY = 0
        buscar.forceActiveFocus()
    }

    function normalizar(texto) {
        return texto.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s/g, "")
    }

    // Las fórmulas vienen del catálogo para coincidir con la comprobación.
    readonly property var columnas: numericos ? [
        [{ titulo: "Raíces", items: [
            { clave: "num_biseccion", nombre: "Bisección", detalle: "Busca una raíz reduciendo un intervalo." },
            { clave: "num_newton", nombre: "Newton-Raphson", detalle: "Busca una raíz usando tangentes." },
        ] }],
        [{ titulo: "Sistemas y matrices", items: [
            { clave: "num_jacobi", nombre: "Jacobi", detalle: "Usa los valores de la iteración anterior." },
            { clave: "num_gauss_seidel", nombre: "Gauss-Seidel", detalle: "Usa los valores nuevos al calcularlos." },
            { clave: "num_comparar_iterativos", nombre: "Comparar métodos iterativos", detalle: "Contrasta Jacobi y Gauss-Seidel." },
            { clave: "num_sistema", nombre: "Comparar soluciones de un sistema", detalle: "Compara Fraction, float propio y NumPy." },
            { clave: "num_inversa", nombre: "Comparar métodos de inversa", detalle: "Compara Fraction, float propio y NumPy." },
        ] }],
        [{ titulo: "Error y precisión", items: [
            { clave: "num_errores", nombre: "Errores numéricos", detalle: "Calcula errores absoluto, relativo y porcentual." },
            { clave: "num_propagacion", nombre: "Propagación del error", detalle: "Estima el efecto de la incertidumbre." },
            { clave: "num_maclaurin", nombre: "Serie de Maclaurin", detalle: "Aproxima exp(x) término a término." },
            { clave: "num_simulacion", nombre: "Simulación", detalle: "Compara truncamiento y redondeo." },
            { clave: "num_flotante", nombre: "Punto flotante", detalle: "Explora épsilon, overflow y underflow." },
            { clave: "num_inestabilidad", nombre: "Inestabilidad numérica", detalle: "Compara expresiones equivalentes." },
        ] }],
        [{ titulo: "Representación", items: [
            { clave: "num_bases", nombre: "Bases 2 y 10", detalle: "Representa números en binario o decimal." },
        ] }],
    ] : [
        [
            { titulo: "Transpuestas", items: [
                {"clave": "prop_transpuesta_doble", "nombre": "Transpuesta de la transpuesta"},
                {"clave": "prop_transpuesta_suma", "nombre": "Transpuesta de una suma"},
                {"clave": "prop_transpuesta_escalar", "nombre": "Transpuesta por escalar"},
                {"clave": "prop_transpuesta_producto", "nombre": "Transpuesta de un producto"},
            ] },
            { titulo: "Productos", items: [
                {"clave": "prop_distributividad", "nombre": "Propiedad distributiva"},
                {"clave": "prop_asociatividad", "nombre": "Propiedad asociativa"},
            ] },
        ],
        [
            { titulo: "Inversas", items: [
                {"clave": "prop_inversa_doble", "nombre": "Inversa de la inversa"},
                {"clave": "prop_inversa_producto", "nombre": "Inversa de un producto"},
                {"clave": "prop_inversa_transpuesta", "nombre": "Inversa de la transpuesta"},
                {"clave": "prop_inversa_identidad", "nombre": "Producto por su inversa"},
            ] },
            { titulo: "Comparación de métodos", items: [
                {"clave": "prop_metodos_inversa", "nombre": "Métodos de inversa"},
            ] },
        ],
        [
            { titulo: "Determinantes", items: [
                {"clave": "prop_det_transpuesta", "nombre": "Determinante de la transpuesta"},
                {"clave": "prop_det_producto", "nombre": "Determinante de un producto"},
                {"clave": "prop_det_inversa", "nombre": "Determinante de la inversa"},
                {"clave": "prop_det_escalar", "nombre": "Determinante por escalar"},
                {"clave": "prop_det_triangular", "nombre": "Matriz triangular"},
            ] },
        ],
        [
            { titulo: "Operaciones por filas", items: [
                {"clave": "prop_fila_intercambio", "nombre": "Intercambiar dos filas"},
                {"clave": "prop_fila_reemplazo", "nombre": "Sumar un múltiplo de otra fila"},
                {"clave": "prop_fila_escalar", "nombre": "Multiplicar una fila por k"},
            ] },
            { titulo: "Comparación de métodos", items: [
                {"clave": "prop_metodos_determinante", "nombre": "Métodos de determinante"},
                {"clave": "prop_metodo_sarrus", "nombre": "Regla de Sarrus (3 × 3)"},
            ] },
        ],
    ]
    readonly property var formulas: {
        const resultado = {}
        for (const metodo of metodos)
            resultado[metodo.clave] = metodo.nombre
        return resultado
    }
    readonly property var visibles: {
        const consulta = normalizar(buscar.text)
        return columnas.map(columna => columna.map(grupo => ({
            titulo: grupo.titulo,
            items: grupo.items.filter(item => normalizar(item.nombre).includes(consulta)
                || normalizar(formulas[item.clave] || "").includes(consulta)
                || normalizar(item.detalle || "").includes(consulta))
        })).filter(grupo => grupo.items.length))
    }

    Boton { text: "← Volver a la calculadora"; onClicked: panel.volver() }
    RowLayout {
        Layout.fillWidth: true
        Label {
            text: panel.numericos ? "Selecciona un método numérico" : "Selecciona una propiedad"
            color: Paleta.texto
            font.pixelSize: 27
            font.bold: true
            Layout.fillWidth: true
        }
        Boton { visible: !panel.numericos; text: "Comprobar todas"; onClicked: panel.elegir("prop_todas") }
    }
    TextField {
        id: buscar
        objectName: "buscarPropiedad"
        Layout.fillWidth: true
        placeholderText: panel.numericos ? "Buscar método…" : "Buscar por nombre o fórmula…"
        Accessible.name: placeholderText
    }
    Label {
        visible: panel.visibles.every(columna => !columna.length)
        text: panel.numericos ? "No se encontraron métodos." : "No se encontraron propiedades."
        color: Paleta.secundario
    }

    ScrollView {
        id: lista
        Layout.fillWidth: true
        Layout.fillHeight: true
        contentWidth: availableWidth
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

        RowLayout {
            width: lista.availableWidth
            spacing: 10
            Repeater {
                model: panel.visibles.filter(columna => columna.length)
                ColumnLayout {
                    required property var modelData
                    Layout.fillWidth: true
                    Layout.preferredWidth: 1
                    Layout.alignment: Qt.AlignTop
                    spacing: 5
                    Repeater {
                        model: modelData
                        ColumnLayout {
                            required property var modelData
                            Layout.fillWidth: true
                            spacing: 5
                            Label {
                                text: modelData.titulo
                                color: Paleta.acento
                                font.bold: true
                                font.pixelSize: Math.round(15 * panel.escalaTarjetas)
                                Layout.topMargin: 6
                            }
                            Repeater {
                                model: modelData.items
                                Boton {
                                    id: opcion
                                    required property var modelData
                                    readonly property string formula: modelData.detalle || panel.formulas[modelData.clave] || ""
                                    Layout.fillWidth: true
                                    text: modelData.nombre
                                    Accessible.name: text + ". " + formula
                                    principal: panel.actual === modelData.clave
                                    padding: Math.round(9 * panel.escalaTarjetas)
                                    implicitHeight: Math.max(58 * panel.escalaTarjetas, etiquetas.implicitHeight + 2 * padding)
                                    contentItem: ColumnLayout {
                                        id: etiquetas
                                        spacing: 2
                                        Label {
                                            text: opcion.text
                                            color: opcion.principal ? Paleta.sobreAcento : Paleta.texto
                                            font.pixelSize: Math.round(15 * panel.escalaTarjetas)
                                            font.bold: true
                                            Layout.fillWidth: true
                                            wrapMode: Text.Wrap
                                        }
                                        Label {
                                            text: opcion.formula
                                            color: opcion.principal ? Paleta.sobreAcento : Paleta.secundario
                                            font.pixelSize: Math.round(13 * panel.escalaTarjetas)
                                            Layout.fillWidth: true
                                            wrapMode: Text.Wrap
                                        }
                                    }
                                    onClicked: panel.elegir(modelData.clave)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
