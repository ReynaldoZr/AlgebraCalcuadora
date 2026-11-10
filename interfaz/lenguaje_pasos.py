"""Explica acciones matemáticas en lenguaje cotidiano sin modificar sus datos.

Tema: texto breve para el recorrido y aclaraciones para el desarrollo completo.
Elaboración: equipo del proyecto, con apoyo de IA.
"""


def aclaracion_paso(paso):
    """Devuelve una frase sencilla según la acción registrada por el algoritmo."""
    titulo = paso.titulo.casefold()
    if paso.detalle.startswith('Conservamos [x'):
        return 'Tomamos el punto medio y conservamos la mitad donde cambia el signo.'
    if '↔' in titulo:
        return 'Cambiamos de lugar las dos filas para poder continuar.'
    if '←' in titulo:
        if ' / ' in titulo:
            return 'Dividimos toda la fila para que su primer valor importante sea 1.'
        return 'Restamos un múltiplo de otra fila para convertir este valor en cero.'
    acciones = (
        ('matriz inicial', 'Partimos de los datos que escribiste; todavía no los hemos cambiado.'),
        ('variables libres', 'Identificamos los valores que pueden elegirse y los representamos con letras.'),
        ('despejamos', 'Usamos los valores ya encontrados para obtener la siguiente incógnita.'),
        ('sin solución', 'Esta igualdad es imposible, por eso el sistema no tiene solución.'),
        ('comprobación', 'Sustituimos el resultado en la operación original para revisar si coincide.'),
        ('condiciones de bisección', 'Revisamos los extremos antes de buscar la raíz entre ellos.'),
        ('iteración', 'Repetimos la operación con los valores que se muestran en esta vuelta.'),
        ('error absoluto', 'Medimos cuánto se aleja la aproximación del valor verdadero.'),
        ('error relativo', 'Comparamos esa diferencia con el tamaño del valor verdadero.'),
        ('derivada', 'Estimamos cuánto cambia la función cerca del punto elegido.'),
        ('propagación', 'Estimamos cómo el error de entrada puede afectar el resultado.'),
        ('cambio evaluado', 'Evaluamos los dos valores de entrada y comparamos sus resultados.'),
        ('referencia racional', 'Hacemos la cuenta con fracciones para obtener una referencia exacta.'),
        ('referencia de alta precisión', 'Comparamos con una cuenta que conserva más cifras.'),
        ('racionalizada', 'Reescribimos la misma expresión para evitar perder cifras al restar.'),
        ('expresión directa', 'Calculamos la expresión original para compararla con otra forma equivalente.'),
        ('cifra entera', 'Calculamos lo que aporta esta cifra según su posición y su base.'),
        ('cifra fraccionaria', 'Calculamos lo que aporta esta cifra después del punto.'),
        ('reconstrucción', 'Sumamos los aportes y revisamos la parte que falta representar.'),
        ('cofactor', 'Tomamos la matriz menor y aplicamos el signo de esta posición.'),
        ('adjunta', 'Ordenamos los cofactores para construir la matriz que usaremos en la inversa.'),
        ('triangular inferior', 'Reunimos en L los factores usados para eliminar valores.'),
        ('forma escalonada', 'Mostramos la matriz obtenida después de eliminar los valores inferiores.'),
        ('resolvemos ly', 'Encontramos primero los valores intermedios y.'),
        ('resolvemos ux', 'Usamos esos valores intermedios para encontrar la solución x.'),
    )
    for patron, explicacion in acciones:
        if patron in titulo:
            return explicacion
    return ''


def explicar_paso(paso, completo=False):
    """Separa la frase esencial de la explicación completa sin recortar fórmulas."""
    aclaracion = aclaracion_paso(paso)
    detalle = paso.detalle.strip()
    if completo:
        # El detalle original puede contener condiciones o números: siempre se conserva.
        if aclaracion and aclaracion.casefold() not in detalle.casefold():
            return aclaracion + ('\n' + detalle if detalle else '')
        return detalle
    if aclaracion:
        return aclaracion
    primera = detalle.splitlines()[0] if detalle else 'Observa la cuenta mostrada antes de avanzar.'
    return primera if len(primera) <= 150 else primera[:147].rstrip() + '…'
