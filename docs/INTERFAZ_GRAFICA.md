# Interfaz gráfica de escritorio

**Actualización del 6 de noviembre:** `gui.py` abre la interfaz PySide6 + QML descrita en [MIGRACION_QT.md](MIGRACION_QT.md). Este documento conserva la referencia de la implementación Tkinter, disponible mediante `gui_tk.py` durante la revisión de la migración.

La instrucción posterior del usuario autoriza una tercera pestaña **Guardados** y un menú pequeño **Guardar / Estudio**. Incluye biblioteca/historial persistentes, nombres y símbolos personalizables, recuperación, ejemplos, ayudas, PDF y copiar/pegar en cada editor. No cambia la distribución de las tres tarjetas ni introduce pestañas anidadas. Véase [GUARDADOS_Y_ESTUDIO.md](GUARDADOS_Y_ESTUDIO.md). La descripción de «dos vistas» de los cálculos que sigue corresponde a Calculadora/Todos los pasos y no excluye esta nueva pestaña autorizada.

La ampliación local de tareas 1 a 6 incorpora Sistemas, Vectores, Determinantes, Inversas, LU y Propiedades en la barra lateral. Cada tema usa la distribución original de tres tarjetas y las dos vistas generales Calculadora/Todos los pasos, sin pestañas anidadas. Las sesiones se conservan al navegar; «Matrices» recupera su calculadora original. Los métodos de entrada única muestran la regla en la tarjeta central y los de sistemas muestran b como columna. Detalles y contratos en [ALGEBRA_TAREAS_1_A_6.md](ALGEBRA_TAREAS_1_A_6.md). Semana 12 queda pendiente.

La ventana de la [issue #8](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/8) se integró mediante el PR #10 por decisión de Roberto. Usa Tkinter/ttk de la biblioteca estándar y conserva la consola requerida por el profesor. El PR #9 está cerrado sin integrar. La continuación local añade escalar y transpuesta como parte de la issue #2; [ESTADO_UI_LOCAL.md](ESTADO_UI_LOCAL.md) distingue lo integrado de lo nuevo.

## Probar

1. Ejecutar `python gui_tk.py` desde la raíz para probar esta interfaz anterior.
2. Pulsar Cargar ejemplo y Calcular. Esperado: `[[1/2, 3/10], [3, 3]]`.
3. Elegir Resta y calcular: `[[1/6, -1/10], [-7, 5]]`.
4. Hacer clic en una fracción para editarla como texto (`1/3`, `0.5`, `-2`). Tab recorre entradas; al salir de ellas vuelve la notación apilada. Ctrl+Enter calcula.
5. Usar Anterior, Reproducir/Pausar, Siguiente y Reiniciar. El intervalo es fijo de dos segundos por etapa; Reiniciar deja Identificar de la primera celda en pausa. Cada celda avanza por Identificar → Operar → Simplificar (si procede) → Guardar. Los operandos están etiquetados y la cuenta se desarrolla antes de revelar la celda de R; retroceder vuelve a ocultarla cuando corresponda.
6. Abrir Todos los pasos: muestra todas las posiciones con equivalencias de fracciones y resultado, con desplazamiento. Volver a calculadora conserva entradas y estado.
7. Cambiar claro/oscuro desde la esquina superior derecha. El tema inicial es azul oscuro con lavanda.
8. Limpiar y pulsar Deshacer para recuperar entradas y cálculo sin cambiar la operación seleccionada. Deshacer conserva hasta 50 estados en memoria, sin persistencia al cerrar. Si el cálculo recuperado corresponde a otra operación, queda marcado como anterior y hay que recalcular.
9. Escribir `1/0` en una celda: debe identificar su posición sin borrar los datos ni el cálculo anterior. Corregir y calcular otra vez.
10. Reutilizar el resultado como A o B. Para redimensionar, pulsar Aplicar; ampliar conserva datos y reducir solicita confirmación por el recorte. Hay desplazamiento para tamaños grandes.
11. Consultar Teoremas desde el encabezado; la ventana de consulta es de solo lectura.
12. Seleccionar Escalar · kA y cargar el ejemplo. k = -3/2 produce `[[-1/2, -3/20], [3, -6]]`. La tarjeta central pide solo k: B queda oculta, conserva sus datos y no se valida para kA. Volver a Suma/Resta restaura B.
13. Probar k = 0, k = 1 y un decimal como 0.1. Un k inválido enfoca ese campo y conserva el cálculo anterior. Editar k detiene el recorrido; Deshacer recupera también el escalar y el cálculo conservando la operación seleccionada.
14. Cambiar varias veces entre Calculadora y Todos los pasos. La nueva vista se revela mediante un desvanecimiento breve, con sus tarjetas ya preparadas. La transición no debe dejar una capa sobre la aplicación ni continuar después de cerrar.
15. Elegir Transpuesta · Aᵀ, cargar ejemplo y calcular: `[[1/3, 0], [-2, 4], [5, 1/2]]` (3×2). A es 2×3. B y k no se leen para esta operación y conservan sus datos. El panel central indica el intercambio de tamaños.
16. Recorrer Identificar → Ubicar → Guardar. Para R[i,j], el borde de origen debe estar en A[j,i], incluso con matrices rectangulares. Todos los pasos muestra el origen y el destino. Reutilizar como A y calcular otra vez recupera la matriz original; Limpiar/Deshacer y cambiar de tema conservan el contrato previo.
17. Elegir Producto · AB y cargar el ejemplo 2×3 por 3×2. Resultado: `[[5, 11], [14, 23]]` (2×2). Primero se señalan la fila de A y la columna de B, después sus pares; el borde más marcado indica el par activo. Las etiquetas escriben A[i,k] y B[k,j]. Se muestran las multiplicaciones, las simplificaciones necesarias y la suma antes de guardar R[i,j]. Anterior reconstruye correctamente la etapa previa.
18. Probar A de 2×3 y B de 2×3: el mensaje debe explicar columnas de A = filas de B, identificando tamaños. El cálculo anterior se conserva. B inválida o con tamaño pendiente también debe rechazarse. El escalar oculto no participa. Reutilizar una respuesta de otro tamaño requiere volver a validar las dimensiones de la nueva operación.

## Dónde cambiar cada cosa

| Archivo | Responsabilidad |
|---|---|
| gui.py | Lanzador opcional y mensaje si falta Tkinter |
| interfaz/ventana.py | Composición, pestañas, acciones, historial y estado de sesión |
| interfaz/tema.py | Paletas y estilos; modificar colores aquí |
| interfaz/notacion.py | Dibujo de fracciones, matrices e icono de Matrices |
| interfaz/cuadricula.py | Edición, dimensiones, foco, resaltado y errores de casillas |
| interfaz/desarrollo.py | Tarjetas de pasos, equivalencias visuales y desplazamiento |
| interfaz/recorrido.py | Temporizador cancelable, pausa y navegación de pasos |
| interfaz/explicacion.py | Datos didácticos sin widgets: operandos, etapas, equivalencias y destino |
| interfaz/transicion.py | Capa transitoria de navegación y su desvanecimiento cancelable |
| interfaz/datos.py | Conversión exacta común a consola y ventana |
| interfaz/formato.py | Presentación de texto para consola |
| modulos/modulo_matrices.py | Algoritmos existentes, independientes de Tkinter |
| tests/test_ventana.py | Recorridos con widgets reales y conservación de datos |
| tests/test_recorrido.py | Navegación y cancelación con reloj controlado |
| tests/test_explicacion.py | Significado matemático de las etapas y sus coordenadas |
| tests/test_transicion.py | Limpieza de capas, transparencia y cambios rápidos con reloj controlado |

## Contratos

- El cálculo llama a `sumar_matrices`, `restar_matrices` y, en la etapa local, `multiplicar_por_escalar` y `transponer_matriz`; recibe listas independientes y no importa la interfaz. La consola tampoco importa Tkinter.
- `multiplicar_por_escalar(matriz, escalar)` acepta una matriz rectangular no vacía y k entero/Fraction, rechazando bool y float; devuelve una matriz nueva del mismo tamaño. El campo gráfico se convierte con `convertir_numero`, igual que la consola.
- El editor admite 1–10 filas/columnas; ese límite es visual y no se extiende al núcleo o la consola.
- Las entradas se convierten desde texto directamente a Fraction, sin pasar por float. Las fracciones apiladas representan esos valores exactos, sin generar imágenes ni usar bibliotecas matemáticas externas.
- El desarrollo recibe operandos y resultados del núcleo. Las equivalencias visuales usan denominador común y numeradores sin simplificar para explicar cada posición; no sustituyen la respuesta del núcleo ni vuelven a solicitar resultados intermedios.
- El último cálculo válido se conserva ante errores. Editar lo marca como anterior y deshabilita su reproducción; la pestaña amplia también avisa si está desactualizado.
- La reproducción usa `after`, nunca sleep ni un bucle bloqueante. Editar, cargar, limpiar, cambiar operación o cerrar cancela el evento pendiente. Cambiar de pestaña pausa el recorrido.
- Cada editor mantiene sus variables Tk mientras existan sus casillas. Durante reconstrucciones se suprimen avisos intermedios que podrían acceder a widgets destruidos.
- El historial guarda copias de entradas, dimensiones pendientes, operación y último resultado. La operación guardada permite detectar cálculos anteriores; restaurar datos conserva la selección actual y no inicia reproducción.
- La Calculadora mantiene explicaciones breves. Todos los pasos dibuja cada fórmula de identificación, operación, simplificación necesaria y destino, para todas las celdas, sin truncar la cantidad. En AB muestra cada par y desarrolla la suma fraccionaria con denominador común; las notas se limitan a aclaraciones necesarias, sin repetir lo que ya expresa la fórmula. `etapas_completas` amplía únicamente esta vista, sin alargar el recorrido animado.
- El historial incluye el texto de k, incluso si todavía es inválido. El cálculo guardado conserva sus propios operandos; cambiar el formulario no cambia una explicación anterior.
- Los datos internos del cálculo son `(A, operando, signo)`: operando es B para `+`/`-` y k para `×`. Los pasos conservan `(fila, columna, operando_izquierdo, operando_derecho, resultado, signo)`. En kA, los operandos del paso son k y A[i,j]; no se construye una matriz B artificial para escalar.
- Para la transpuesta se guarda `(A, None, 'T')`. Las coordenadas del paso son las de R; el origen es A[columna][fila]. Sus datos son `(fila_R, columna_R, valor_origen, None, valor_resultado, 'T')`. Se recorren las celdas de R por filas, sin introducir una operación aritmética ficticia. La notación visible es Aᵀ y los valores exactos no cambian. `transponer_matriz(A)` valida A y devuelve filas nuevas, de tamaño columnas_A×filas_A.
- Para producto se guarda `(A, B, 'AB')`. `producto_matricial(A, B)` valida m×n por n×p y devuelve una nueva matriz m×p con tres bucles propios. Los pasos son `(fila_R, columna_R, tupla_fila_A, tupla_columna_B, resultado, 'AB')`. La respuesta final viene del núcleo; la interfaz calcula productos individuales únicamente para explicar cómo se forma cada celda. No se comparte memoria mutable con los editores.
- `EtapaVisual.par` indica el índice común activo en el producto; es None para identificar la fila/columna, sumar y guardar. La cuadrícula señala el grupo completo con borde de contexto y el par con borde más marcado. Los valores de origen se escriben en las instrucciones, por lo que no dependen solo del color. Las fórmulas extensas conservan desplazamiento horizontal y el desarrollo largo, vertical.
- `explicacion.py` convierte los pasos guardados en `EtapaVisual`: origen, fórmula, explicación y posición. La respuesta final siempre procede del núcleo. `ReproductorPasos.preparar(pasos, etapas=None)` conserva las celdas en `pasos` y navega por `secuencia`; sin etapas explícitas mantiene su comportamiento anterior. El índice de reproducción se refiere a la etapa, no a la celda. Dibujar una etapa reconstruye el resultado parcial según su posición, también al retroceder.
- Las coordenadas se escriben en las cabeceras activas y en las instrucciones; un borde rodea origen y destino. El color no es la única señal.
- La transición usa una capa Tk solo dentro del área cliente de esta aplicación, nunca reduce la opacidad de la ventana principal ni captura la pantalla. Deja que la geometría se complete debajo y retira la capa en aproximadamente 180 ms con `after`. Cambiar otra vez, editar o cerrar cancela la capa anterior y su temporizador. Si Tk rechaza transparencia, continúa con un cambio limpio. No se inicia al abrir inicialmente la aplicación ni en una raíz retirada.
- Los temas se cambian sobre los mismos widgets; no se reconstruye la sesión para cambiar colores. No se persisten preferencias al cerrar.
- Main y su versión publicada no cambian. No hay servidor ni migración a una interfaz web.

## Añadir otra operación

Implementar y probar primero el algoritmo en su módulo, según COMO_AGREGAR.md. Después conectar su opción en ventana.py. Reutilizar el editor, la notación y la vista de desarrollo. Una operación unaria debe pedir solo sus entradas reales. Ampliar el contenido de los pasos cuando sea necesario sin introducir algoritmos nuevos dentro del dibujo.

Los colores se ajustan en tema.py; la representación matemática en notacion.py; las etapas y textos en explicacion.py; los pasos completos en desarrollo.py; el cambio entre vistas en transicion.py. No reescribir toda la ventana para añadir un estilo o un paso. Los futuros temas se habilitarán únicamente cuando tengan funcionalidad real.

## Verificación y límites

Ejecutar `python -m unittest discover -s tests -v`, `python herramientas/comprobar_reglas.py` y `git diff --check`. Las pruebas de ventana usan widgets reales; en Linux requieren Xvfb. CI usa CALCULADORA_EXIGIR_GUI=1 para impedir omisiones silenciosas.

La revisión visual local se hace en Windows; no implica haber revisado macOS, todas las escalas o lectores de pantalla. Tkinter tiene un árbol de accesibilidad limitado en Windows. Las fórmulas largas y matrices grandes tienen desplazamiento; la ventana requiere al menos 1120×760 unidades de Tk. No hay instalador, exportación ni guardado de sesiones.


## Inicio y navegación compacta aprobados

La continuación local abre primero un Inicio con tarjetas agrupadas en Álgebra lineal y Métodos numéricos. Temas es un menú plegable y Biblioteca reúne Guardados/Historial desde la cabecera. Cambiar despliega las dimensiones; ⋯ agrupa herramientas de entrada y reutilización. Las tres tarjetas, los recorridos y Todos los pasos se conservan. Ver [INICIO_Y_NAVEGACION.md](INICIO_Y_NAVEGACION.md). En Numéricos se retira el encabezado duplicado para que los campos de bisección sigan cabiendo en el tamaño mínimo.
