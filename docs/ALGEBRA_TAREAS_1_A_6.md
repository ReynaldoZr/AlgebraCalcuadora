# Álgebra exacta: tareas 1 a 6

Esta ampliación está en la rama local `feat/3-algebra-tareas-1-a-6`, sin publicar. Conserva los cambios anteriores de matrices y añade los siete bloques acordados. Métodos Numéricos de la semana 12 no forma parte del cambio: no se crean módulos numéricos ni se instalan NumPy, SciPy o SymPy.

## Cobertura y ubicación

| Bloque | Cálculos | Archivo |
|---|---|---|
| Sistemas | Gauss/REF, Gauss-Jordan/RREF, clasificación, pivotes, libres, particular y solución general | modulos/modulo_sistemas.py |
| Reducción compartida | Intercambios, reemplazos, normalización, pivotes y registro componente por componente | modulos/eliminacion.py |
| Vectores | Suma, resta, escalar, pertenencia a una combinación, independencia y relación de dependencia | modulos/modulo_vectores.py |
| Determinantes | Cofactores recursivos, Sarrus 3×3 y triangularización con signo de intercambios | modulos/modulo_determinantes.py |
| Inversas | [A\|I], matriz de cofactores/adjunta y comprobación A·A⁻¹=I | modulos/modulo_matrices.py |
| LU | L m×m, U m×n, registro de multiplicadores, LU=A, Ly=b y Ux=y | modulos/modulo_lu.py |
| Propiedades | 21 comprobaciones de ambos miembros y sus condiciones | teoremas/verificadores.py |

Fuentes: [tarea 1](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=965262), [tarea 2](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=982676), [tarea 3](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=990114), [tarea 4](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=1001328), [tarea 5](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=1007311) y [tarea 6](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=1014338). Las copias privadas y credenciales quedan fuera del repositorio. Los informes académicos y capturas de entrega no se generan por implementar los cálculos.

## Contratos de datos

El cálculo admite matrices rectangulares no vacías con enteros/Fraction, nunca bool o float. No modifica entradas. Un vector es una lista; en la ventana b es una matriz columna m×1. Las operaciones vectoriales básicas usan una fila 1×n; combinación e independencia colocan los vectores como columnas de A. Los índices internos de pivotes y libres comienzan en cero; en pantalla se muestran desde uno.

`Paso(titulo, detalle, matriz, formulas, separador)` registra una operación matemática. Las matrices son instantáneas independientes y las fórmulas contienen tokens exactos; `separador` señala el corte de una aumentada. `Calculo(valor, pasos, datos)` devuelve valor y procedimiento. Un `ErrorCalculo` conserva los pasos realizados cuando la operación debe detenerse por una limitación matemática.

`reducir` devuelve `Reduccion`: matriz nueva, pivotes, pasos, cantidad de intercambios y multiplicadores `(destino, fila_pivote, factor)`. `columnas_pivote` impide buscar pivotes en b o en I al reducir matrices aumentadas. `registrar=False` omite únicamente la construcción de explicaciones, no el algoritmo.

`resolver_sistema(A,b,metodo)` acepta `gauss` o `jordan`. Devuelve la particular o None y datos: `clasificacion` (`unica`, `infinitas`, `sin_solucion`), matriz escalonada/reducida, pivotes, libres, base de direcciones y verificación. Para infinitas soluciones, `x=particular+Σ tk·base[k]`: se comprueba A·particular=b y A·base[k]=0. La clasificación no depende del determinante y admite sistemas rectangulares.

`calcular_determinante(A,metodo)` acepta `reduccion`, `cofactores` o `sarrus`. Devuelve un escalar exacto y pasos. Las funciones `determinante_*` devuelven solo el escalar. Los reemplazos conservan det y cada intercambio cambia el signo; la reducción no escala filas. Sarrus rechaza órdenes distintos de 3. El menor vacío usado por la adjunta 1×1 tiene determinante 1.

`calcular_inversa(A,metodo)` acepta `jordan` o `adjunta`. Devuelve una matriz y la comprobación exacta. Las funciones `inversa_gauss_jordan` e `inversa_adjunta` permiten reutilizar solo la matriz. Si A es singular, se detiene: el método de Jordan comunica cuántos pivotes encontró.

`factorizar_lu(A)` devuelve `(L,U)` y `verificado`. Admite matrices rectangulares y columnas sin pivote, conserva diagonal unitaria de L y no normaliza filas de U. Si necesita intercambio, se detiene con el aviso de PA=LU. `resolver_lu(A,b)` requiere matriz cuadrada con solución única y devuelve x, L, U, y y la comprobación Ax=b. Un caso singular se remite a Gauss-Jordan para su solución general.

`verificar_propiedad` devuelve `Verificacion(propiedad, izquierda, derecha, cumple, motivo)`. `cumple=None` significa «No aplicable», con un motivo concreto; no se interpreta como éxito. El catálogo incluye transpuestas, distributividad, asociatividad, inversas, determinantes, efectos de filas, producto diagonal triangular y coincidencia de métodos. LU=A y Ax=b se comprueban también al ejecutar esos cálculos.

## Interfaz y ampliación

`interfaz/operaciones.py` es el catálogo compartido de métodos, entradas, ayudas y ejemplos. Despacha al núcleo y prepara texto: no implementa eliminación, inversas o determinantes. Al añadir un método, hacerlo primero en su módulo y pruebas; después añadir su entrada al catálogo y un ejemplo conocido.

`panel_algebra.py` adapta los temas a las tres tarjetas originales. No añade pestañas internas: cada tema conserva las dos vistas generales Calculadora/Todos los pasos. En propiedades que necesitan C, B y C comparten la tarjeta central mediante «Editar B/C»; ambos datos se conservan. Los métodos que usan solo A muestran la regla en el centro. La sesión de Matrices sigue independiente y se recupera desde la barra lateral.

El recorrido breve muestra una fórmula esencial por operación y reproduce cada etapa a dos segundos, sin selector de velocidad. `procedimiento.py` dibuja todas las fórmulas y matrices al abrir la vista completa; no trunca la cantidad de pasos. Editar cancela el recorrido; el último resultado se conserva marcado como anterior. Limpiar y Deshacer mantienen el método seleccionado. El historial local guarda hasta cincuenta estados y se pierde al cerrar.

`menu_algebra.py` ofrece los mismos métodos en consola, con cabecera ASCII y opción 0 de teoremas. Los submenús nuevos usan 99 para volver: evita colisión con el catálogo de más de nueve propiedades. Se conservan las opciones anteriores del menú de matrices; determinantes, inversas y verificadores también son accesibles desde allí.

## Ejemplos para revisión humana

- Sistemas: A=`[[2,1],[1,-1]]`, b=`[5,1]` → x=`[2,1]`.
- Infinitas: A=`[[1,2],[2,4]]`, b=`[3,6]` → x=`[3,0]+t·[-2,1]`.
- Inconsistente: A=`[[1,1],[2,2]]`, b=`[1,3]` → sin solución.
- Combinación: columnas de A=`[[1,0],[0,1],[1,1]]`, b=`[2,3,5]` → coeficientes `[2,3]`.
- Determinante: A=`[[1,2,3],[0,1,4],[5,6,0]]` → 1 por los tres métodos.
- Inversa: A=`[[1,2],[3,4]]` → `[[-2,1],[3/2,-1/2]]` por ambos métodos.
- LU: A=`[[2,1,1],[4,-6,0],[-2,7,2]]`, b=`[5,-2,9]` → y=`[5,-12,2]`, x=`[1,1,2]`.
- Pivoteo LU: A=`[[0,1],[1,0]]` → detener, requiere PA=LU; no anunciar A=LU.
- Propiedades: cargar el ejemplo y comprobar ambos miembros. Sarrus no se aplica a la A 2×2 del ejemplo general; triangular requiere una A triangular.

## Comprobación y límites

Ejecutar `python -m unittest discover -s tests -v`, `python herramientas/comprobar_reglas.py` y `git diff --check`. Las pruebas de álgebra cubren valores conocidos, fracciones, singularidad, dimensiones, conservación, parámetros y coincidencia de métodos; las de interfaz comprueban sesiones, formularios y procedimientos completos. En Linux las pruebas Tk requieren Xvfb, como indica la CI existente.

Cofactores y adjunta tienen crecimiento factorial: para órdenes grandes usar reducción o Gauss-Jordan. La cuadrícula sigue limitada a 10×10; los algoritmos no introducen ese límite de interfaz. El desarrollo completo puede ser extenso porque conserva todas las operaciones. No se afirma que una comprobación local equivalga a CI o revisión humana. No se cambia la versión publicada, se cierra una issue ni se publica la rama automáticamente.
