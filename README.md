# Calculadora de Álgebra Lineal

## Nueva interfaz local: PySide6 + QML

El avance autorizado del 6 de noviembre incorpora una nueva interfaz de escritorio. Instala `python -m pip install -r requirements-interfaz.txt` y ejecuta `python gui.py` (o **Calculadora escritorio** en IntelliJ). Para los métodos de semana 12 instala también `requirements-numericos.txt`. `python main.py` conserva la consola y `python gui_tk.py` permite usar la interfaz anterior durante la transición. Esta propuesta sigue local, sin PR ni versión publicada.

Se mantienen los temas, entradas vacías, ejemplos explícitos, tres tarjetas, pasos completos, recorrido fijo de dos segundos, historial, guardados y PDF. Los datos de la Biblioteca son compatibles con la interfaz anterior. La guía de arquitectura y de prueba está en [docs/MIGRACION_QT.md](docs/MIGRACION_QT.md).

Calculadora educativa local para un equipo de dos estudiantes. **Versión v0.1.0:** suma y resta de matrices, con resultados exactos y procedimiento. Proyecto en desarrollo mediante issues y pull requests.

**Ampliación local sin publicar:** además de matrices, sistemas, vectores, determinantes, inversas, LU y verificadores, se incorpora **Numéricos · Semana 12**: bisección, errores, propagación, truncamiento/redondeo, bases, estabilidad, comparación Fraction/float/NumPy y gráficas. Se conserva el diseño de tres tarjetas y las vistas existentes. La nueva unidad necesita `requirements-numericos.txt`; el álgebra exacta sigue independiente. [Preparación y ejemplos de semana 12](docs/SEMANA_12.md).

**IntelliJ IDEA:** usar la configuración **Calculadora escritorio**, que ejecuta `gui.py` con `.venv/Scripts/python.exe`. También se puede ejecutar directamente `.venv\Scripts\python.exe gui.py`. El [mapa del código](docs/GUIA_CODIGO.md) explica qué hace cada archivo; se añadieron comentarios breves en decisiones y puntos de conexión.

## Antes de trabajar con una IA

**Guardados y estudio (local):** abre **Guardar / Estudio** para guardar una matriz, un ejercicio completo, cargar casos o consultar ayudas. La pestaña **Guardados** conserva elementos con símbolos como **Aᵀ** y nombres automáticos (**Transpuesta 1**, **Transpuesta 2**), nombres/símbolos propios y notas. Incluye búsqueda, historial de cien ejercicios, recuperación y PDF con todos los pasos. Cada editor permite copiar/pegar matrices. Los datos permanecen en tu equipo al cerrar. [Guía y ubicación de los datos](docs/GUARDADOS_Y_ESTUDIO.md).

La IA sigue **issue → rama → implementación → comprobaciones → PR → CI** y deja el pull request abierto para revisión humana. Reynaldo u otro humano autorizado decide si se corrige, se descarta o se integra. Las pruebas aprobadas no autorizan a la IA a hacer merge ni a publicar versiones. Leer [AGENTS.md](AGENTS.md) y el [flujo completo para la IA](docs/FLUJO_IA.md) antes de empezar.

## Ejecutar

Requiere Python 3.11 o posterior. El álgebra exacta y la consola no necesitan bibliotecas externas; la nueva ventana usa requirements-interfaz.txt y la semana 12 usa requirements-numericos.txt. En una terminal, dentro de la carpeta del repositorio:

```text
python main.py
```

En Windows también puedes usar `py -3 main.py` si ese es el lanzador instalado. En PyCharm o IntelliJ con soporte de Python, abre la carpeta, selecciona el intérprete y ejecuta main.py. Las fracciones y el texto en español se muestran en la consola.

## Referencia de la interfaz anterior (Tkinter)

Roberto integró la interfaz del [PR #10](https://github.com/ReynaldoZr/AlgebraCalcuadora/pull/10) en main; la issue #8 está cerrada y el PR #9 permanece cerrado sin integrar. Las mejoras de la issue #2, escalar, transpuesta y producto matricial, se preparan localmente; [estado y límite de publicación](docs/ESTADO_UI_LOCAL.md). Todavía no hay una nueva release publicada.

Para abrir la ventana anterior durante la comparación con Qt:

```text
python gui_tk.py
```

Esta implementación anterior incluye casillas para A y B, suma/resta, resultado exacto, procedimiento, teoremas, ejemplo y reutilización del resultado. Usa Tkinter/ttk de la biblioteca estándar. La interfaz Qt se describe al inicio y en MIGRACION_QT.md; ambas reutilizan los cálculos y la consola sigue disponible.

**Mejora local de la issue #2:** selecciona **Escalar · kA**, introduce A y un escalar exacto (entero, decimal o fracción) y pulsa Calcular. La tarjeta de k ocupa el lugar de B, cuyos datos se conservan al cambiar de operación. Cargar ejemplo utiliza `k = -3/2` y produce `[[-1/2, -3/20], [3, -6]]`. La vista previa, Todos los pasos, reproducción, tema y Deshacer funcionan también con kA. En consola se añade **4. Multiplicar una matriz por un escalar**, conservando las opciones anteriores. Más ejemplos en [ejemplos/escalar.md](ejemplos/escalar.md).

**Transpuesta local:** selecciona **Transpuesta · Aᵀ → Cargar ejemplo → Calcular**. A de 2×3 produce Aᵀ de 3×2: `[[1/3, 0], [-2, 4], [5, 1/2]]`. Solo se pide A; el panel central explica cómo se intercambian las coordenadas. El recorrido muestra, por ejemplo, **A[1,2] → R[2,1]**, con tres etapas: Identificar, Ubicar y Guardar. Reutilizar el resultado como A permite comprobar la transpuesta doble. En consola es la opción 5. Véase [ejemplos/transpuesta.md](ejemplos/transpuesta.md).

**Producto matricial local:** selecciona **Producto · AB → Cargar ejemplo → Calcular**. A de 2×3 por B de 3×2 produce `[[5, 11], [14, 23]]`. Se valida que columnas de A = filas de B. El recorrido señala la fila y columna elegidas, cada par activo, sus productos y la suma final antes de guardar la celda. En consola es la opción 6. Se mantienen Deshacer, reutilización, errores recuperables y Todos los pasos. Véase [ejemplos/producto.md](ejemplos/producto.md). El conjunto de la issue #2 está en preparación local y aún requiere revisión humana.

Cada editor permite de 1 a 10 filas y columnas, con barras de desplazamiento. Al modificar dimensiones pulsa **Aplicar**; se mantienen las celdas coincidentes y se pide confirmación antes de recortar otras. El límite solo afecta a la cuadrícula gráfica, no al núcleo o la consola.

Pulsa **Cargar ejemplo → Calcular** para comenzar. Puedes editar cada casilla, usar Tab para pasar a la siguiente y Ctrl+Enter para calcular. Los errores identifican la matriz y la celda, conservando tus datos. Si cambias una entrada, el resultado anterior se identifica como tal hasta volver a calcular. **Limpiar** reinicia esta sesión.

El diseño local usa azul oscuro y lavanda, con el icono cuadrado de Matrices y un cambio de tema en la esquina superior derecha. Las fracciones aparecen apiladas; haz clic o usa Tab para editarlas como texto. **Deshacer** recupera estados anteriores, incluida una limpieza.

La calculadora muestra una vista previa con los puntos clave. **Abrir todos los pasos** lleva a otra pestaña interna, amplia y desplazable, con cada posición y sus equivalencias de fracciones; volver conserva tus entradas. El cambio revela la vista preparada con un desvanecimiento de unos 180 ms, sin mostrar cómo se acomodan sus tarjetas.

Para explorar el cálculo usa **Anterior**, **Reproducir/Pausar**, **Siguiente** y **Reiniciar**. Cada celda tiene etapas: identificar operandos, operar, simplificar si hace falta y guardar. Las etiquetas indican el origen (k, A[i,j], B[i,j]) y el destino R[i,j]; los bordes acompañan el color. La multiplicación muestra también el producto de numeradores y denominadores. El resultado de la celda aparece al guardarlo. El intervalo es fijo de **dos segundos por etapa**, sin selector, y el movimiento no empieza automáticamente. Editar datos cancela el recorrido anterior y exige calcular de nuevo; el desarrollo conservado avisa si está desactualizado. Todos los pasos muestra el desarrollo entero sin esperar esas etapas.

Tkinter debe estar incluido en tu instalación de Python; puedes comprobarlo con `python -m tkinter`. Si falta, consulta las instrucciones de tu distribución de Python. La consola funciona sin Tkinter. Más detalles y alcance en [docs/INTERFAZ_GRAFICA.md](docs/INTERFAZ_GRAFICA.md).

## Qué incluye

- Menú principal y módulo de matrices con cabecera ASCII.
- Suma y resta de matrices rectangulares del mismo tamaño.
- Entrada de enteros, fracciones como `1/3` y decimales con punto como `0.5`.
- Validación con reintentos ante datos incorrectos y mensaje para tamaños incompatibles.
- Resultado alineado y procedimiento opcional por posición.
- Último resultado reutilizable como A o B sin volver a escribirlo; se conserva al salir y volver al módulo, mientras la aplicación permanece abierta.
- Opción 0 de teoremas. En esta etapa muestra enunciados; todavía no verifica propiedades automáticamente.

Los cálculos usan listas y funciones propias. Los números ingresados se convierten directamente a `Fraction`: por eso 0.1 + 0.2 se muestra como 3/10. Si llamas a las funciones desde otro archivo, pasa enteros o Fraction; los float se rechazan para no perder exactitud silenciosamente.

## Probar un ejemplo

Entra a **1. Álgebra de matrices → 1. Sumar matrices**, ingresa A y B con 1 fila y 1 columna y usa 1/3 y 1/6 como valores. El resultado será 1/2. Elige ver el procedimiento. Más casos en [ejemplos/suma_y_resta.md](ejemplos/suma_y_resta.md).

Usa 9 para volver o salir, según el menú. Ctrl+C y el fin del flujo de entrada terminan la sesión sin traceback. Los resultados no se guardan al cerrar.

## Dónde encontrar cada cosa

| Lugar | Responsabilidad |
|---|---|
| [main.py](main.py) | Punto de entrada y versión |
| [gui.py](gui.py) | Punto de entrada de la ventana opcional |
| [modulos/](modulos/) | Cálculos y validaciones matemáticas, sin input ni print |
| [interfaz/](interfaz/) | Menús, lectura y presentación |
| [teoremas/](teoremas/) | Enunciados teóricos de los temas implementados |
| [ejemplos/](ejemplos/) | Casos revisados para practicar y exponer |
| [tests/](tests/) | Pruebas de resultados, errores y recorridos |
| [herramientas/](herramientas/) | Comprobaciones de reglas del proyecto |
| [docs/ESTRUCTURA.md](docs/ESTRUCTURA.md) | Mapa actual y destino de futuros temas |

## Comprobaciones

Desde la raíz del repositorio:

```text
python -m unittest discover -s tests -v
python herramientas/comprobar_reglas.py
```

GitHub Actions ejecuta ambas comprobaciones en Windows y Linux con Python 3.11 y 3.13. Las cuatro combinaciones pasaron en el PR inicial; cada cambio posterior vuelve a comprobarse. main exige un PR con las cuatro comprobaciones aprobadas antes de integrar.

Las pruebas de la ventana utilizan widgets reales. En Linux se ejecutan con `xvfb-run -a python -m unittest discover -s tests -v`. En CI, `CALCULADORA_EXIGIR_GUI=1` impide dar por aprobada la interfaz si se omitieron sus pruebas por falta de Tk o pantalla. Localmente, sin pantalla o Tk, se informa la omisión y siguen las pruebas de consola y cálculo.

El verificador analiza imports con AST, rechaza bibliotecas externas fuera del ámbito numérico autorizado, detecta entradas/salidas dentro del cálculo y comprueba docstrings. Es una ayuda de mantenimiento, no una prueba de corrección matemática ni una garantía contra cualquier incumplimiento.

## Cómo seguimos

- [Issues iniciales](docs/ISSUES.md) y [plan de versiones](docs/VERSIONES.md): tareas reales y orden de las etapas.
- [Guía para añadir operaciones](docs/COMO_AGREGAR.md): pasos y ejemplo concreto.
- [Trabajo entre dos](docs/TRABAJO_EN_EQUIPO.md): issues, ramas, revisión y PR.
- [AGENTS.md](AGENTS.md) y [guion de IA](docs/GUION_IA.md): reglas para mantener la estructura.
- [Requisitos de UAM](docs/REVISION_UAM.md) e [inventario de fuentes](docs/INVENTARIO_MATERIALES.md): indicaciones revisadas al 3 de noviembre de 2026.
- [Decisiones](docs/DECISIONES.md) e [historial](CHANGELOG.md): razones y cambios.

El permiso de NumPy/SciPy del plan semanal 12 se limita a Métodos Numéricos. Las tareas 1–6 conservarán sus algoritmos propios. Se mantiene la consola pedida desde la tarea 4.

Producto, transpuesta, sistemas, vectores, determinantes, inversas, verificadores y LU se añadirán por etapas; no están implementados en v0.1.0. La identidad de pantalla «Cuaderno de Álgebra Lineal» es provisional.

Una nueva función se propone con una issue y se presenta en un PR. Una corrección compatible puede corresponder a una mini versión, por ejemplo v0.1.1. Integrar requiere decisión humana; publicar una etiqueta o release requiere también autorización expresa. Los datos del segundo integrante y del nuevo grupo se registrarán cuando estén confirmados; las cabeceras actuales identifican el trabajo del equipo con apoyo de IA.


**Navegación local nueva:** al iniciar aparece el menú por unidades. Elige una tarjeta; «Temas» cambia de tema mediante un menú plegable e «Inicio» vuelve sin borrar la sesión. «Biblioteca» reúne Guardados/Historial. «Cambiar» despliega dimensiones y «⋯» contiene copiar/pegar o reutilizar resultados. [Guía de navegación](docs/INICIO_Y_NAVEGACION.md).
