"""Construye figuras de la semana 12 sin depender de Tk ni Qt.

Tema: reutilizar las mismas curvas en ambas interfaces.
Elaboracion: equipo del proyecto, con apoyo de IA.
"""

from matplotlib.figure import Figure

from modulos.numericos.funciones import crear_funcion


def figura_numerica(clave, calculo):
    """Construye una figura exportable sin abrir ventanas ni usar pyplot global."""
    figura = Figure(figsize=(9, 6), dpi=100, layout='constrained')
    d = calculo.datos
    if clave in ('num_biseccion', 'num_propagacion'):
        funcion = crear_funcion(d['funcion'])
        a, b = d['intervalo'] if clave == 'num_biseccion' else (d['x'] - max(d['delta'] * 2, 0.1), d['x'] + max(d['delta'] * 2, 0.1))
        eje = figura.add_subplot(211 if clave == 'num_biseccion' else 111)
        puntos = [a + (b - a) * i / 400 for i in range(401)]
        valores = []
        for punto in puntos:
            try:
                valores.append(funcion(punto))
            except ValueError:
                valores.append(float('nan'))
        eje.plot(puntos, valores, label='f(x)')
        eje.axhline(0, color='gray', linewidth=0.8)
        eje.set(xlabel='x', ylabel='f(x)', title='Función del ejercicio')
        if clave == 'num_biseccion':
            eje.scatter([calculo.valor], [funcion(calculo.valor)], label='Aproximación', color='#a5a6ff')
            error = figura.add_subplot(212)
            filas = d['filas']
            error.plot([f[0] for f in filas], [f[8] for f in filas], marker='.', label='Cota absoluta en x')
            error.set(xlabel='Iteración', ylabel='Cota de error', yscale='log', title='Reducción del intervalo')
            error.grid(alpha=0.3)
        else:
            eje.scatter([d['x'], d['x'] + d['delta']], [funcion(d['x']), funcion(d['x'] + d['delta'])], label='Puntos comparados')
        eje.legend()
        eje.grid(alpha=0.3)
    elif clave == 'num_simulacion':
        eje = figura.add_subplot(111)
        filas = d['filas']
        eje.plot([f[0] for f in filas], [f[4] for f in filas], label='Error por redondeo')
        eje.plot([f[0] for f in filas], [f[5] for f in filas], label='Error por truncamiento')
        eje.set(xlabel='Iteración', ylabel='Error absoluto', title='Acumulación del error')
        eje.legend()
        eje.grid(alpha=0.3)
    else:
        eje = figura.add_subplot(111)
        filas = d['filas']
        eje.bar(range(len(filas)), [f[4] for f in filas])
        eje.set(xlabel='Elemento comparado', ylabel='Error absoluto', title='Float propio frente al resultado exacto')
    return figura
