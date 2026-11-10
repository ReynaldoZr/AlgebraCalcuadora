.pragma library

// Presenta exponentes enteros completos como superíndices.
function mostrarPotencias(expresion) {
    const normales = "0123456789+-"
    const elevados = "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻"
    return expresion.replace(/(?:\^|\*\*)\s*([+-]?\d+)(?![\w.^]|\s*(?:\^|\*\*))/g,
        (potencia, exponente) => exponente.split("").map(digito => elevados[normales.indexOf(digito)]).join(""))
}
