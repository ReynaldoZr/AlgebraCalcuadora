"""Contiene el resumen teórico de las operaciones implementadas.

Tema: suma/resta de igual dimensión, escalar y transpuesta.
Elaboración: equipo del proyecto, con apoyo de IA.
"""


def teoremas_matrices():
    """Devuelve condiciones y propiedades de suma, resta y escalar."""
    return (
        "\nTEOREMAS CLAVE: SUMA, RESTA, ESCALAR Y TRANSPUESTA\n"
        "Para sumar/restar: A y B deben tener las mismas filas y columnas.\n"
        "Suma: (A + B)[i,j] = A[i,j] + B[i,j].\n"
        "Resta: (A - B)[i,j] = A[i,j] - B[i,j].\n"
        "Conmutatividad de la suma: A + B = B + A.\n"
        "Asociatividad de la suma: (A + B) + C = A + (B + C).\n"
        "Neutro: A + 0 = A, con matriz cero del mismo tamaño.\n"
        "Inverso aditivo: A + (-A) = 0.\n"
        "La resta no es conmutativa en general: A - B puede diferir de B - A.\n"
        "Escalar: (kA)[i,j] = k · A[i,j]; se conservan las dimensiones de A.\n"
        "Identidad y cero: 1A = A; 0A es la matriz cero del mismo tamaño.\n"
        "Para A y B del mismo tamaño: k(A + B) = kA + kB.\n"
        "Transpuesta: si A es m×n, Aᵀ es n×m y (Aᵀ)[j,i] = A[i,j].\n"
        "Transpuesta doble: (Aᵀ)ᵀ = A. Los valores se conservan.\n"
        "Producto: si A es m×n y B es n×p, AB es m×p.\n"
        "(AB)[i,j] = A[i,1]B[1,j] + ... + A[i,n]B[n,j].\n"
        "El producto de matrices no es conmutativo en general: AB puede diferir de BA.\n"
        "Con tamaños compatibles: A(BC) = (AB)C y A(B + C) = AB + AC.\n"
        "El tema Propiedades calcula ambos miembros y comprueba las condiciones de aplicación."
    )


def teoremas_tema(tema):
    """Devuelve condiciones y enunciados de los temas implementados, sin calcularlos."""
    resumenes = {
        'Numéricos': 'Bisección requiere continuidad y cambio de signo, salvo raíz en un extremo.\n'
                     'Cota del punto medio: (xu-xl)/2. Predicción de reducciones: n≥log2((b-a)/E).\n'
                     'Ea(%)=100·|xr_actual−xr_anterior|/|xr_actual|, no definido si xr=0.\n'
                     'Tolerancia en x, porcentaje y residuo son magnitudes distintas.\n'
                     'Error absoluto=|verdadero−aproximado|; relativo=absoluto/|verdadero|.\n'
                     'La propagación lineal usa Δy≈f\'(x)Δx; la derivada se aproxima numéricamente.\n'
                     'Un residuo pequeño no garantiza precisión si la matriz está mal condicionada.\n'
                     'Los algoritmos exactos anteriores conservan su implementación con Fraction.',
        'Sistemas': 'Gauss produce forma escalonada; Gauss-Jordan, forma reducida.\n'
                    'Una fila 0=b con b≠0 implica inconsistencia.\n'
                    'Un pivote por variable implica solución única; variables libres implican infinitas soluciones si el sistema es consistente.\n'
                    'La solución general es x=p+t1·v1+...; Ap=b y Avi=0.',
        'Vectores': 'Las operaciones requieren igual dimensión.\n'
                    'b pertenece al espacio generado por v1,...,vk si Ac=b es consistente, colocando los vectores como columnas.\n'
                    'Son L.I. si Ac=0 tiene solo la solución trivial: un pivote por columna, sin variables libres.\n'
                    'Son L.D. si existe una relación no trivial Ac=0.',
        'Determinantes': 'El determinante se define para matrices cuadradas.\n'
                         'Cij=(-1)^(i+j)det(Mij); det(A)=Σ a1j C1j.\n'
                         'Sarrus solo se aplica a orden 3.\n'
                         'Intercambiar filas cambia el signo; reemplazar una fila conserva det; escalar una fila por k multiplica det por k.\n'
                         'El determinante de una triangular es el producto de su diagonal.',
        'Inversas': 'A tiene inversa si es cuadrada y det(A)≠0.\n'
                    '[A|I] → [I|A⁻¹] por Gauss-Jordan.\n'
                    'A⁻¹=adj(A)/det(A); adj(A) es la transpuesta de la matriz de cofactores.\n'
                    'La comprobación exacta es A·A⁻¹=I.',
        'LU': 'A=LU, con L triangular inferior m×m de diagonal 1 y U escalonada m×n.\n'
              'Los multiplicadores de los reemplazos se registran en L.\n'
              'Si hace falta intercambiar filas, se necesita PA=LU y este método se detiene.\n'
              'Para resolver un sistema cuadrado no singular: Ly=b, después Ux=y. Se comprueban LU=A y Ax=b.',
        'Propiedades': 'Se calculan ambos miembros de cada igualdad con los algoritmos del proyecto.\n'
                       'Un resultado «No aplicable» significa que falla una precondición; no significa «Se cumple».\n'
                       'Las igualdades son exactas con enteros y fracciones. No se reingresan resultados intermedios.\n'
                       'Incluye transposición, distributividad, asociatividad, inversas, determinantes, operaciones de fila y coincidencia de métodos.',
    }
    return resumenes.get(tema, teoremas_matrices())
