# Guía corta para trabajar en el código desde IntelliJ

Abre la carpeta `AlgebraCalcuadora`. Los archivos tienen una descripción inicial, cada función tiene una docstring breve y los comentarios de línea explican decisiones que no son evidentes. No es necesario comentar cada asignación. Para orientarte, busca el nombre de la función o archivo indicado abajo.

## Por dónde empieza la aplicación

| Quiero entender | Archivo y punto de entrada |
|---|---|
| Inicio en ventana Qt | gui.py → gui_qt.py → iniciar en interfaz/qt/aplicacion.py |
| Pantallas y componentes Qt | interfaz/qt/qml/Principal.qml y sus componentes reutilizables |
| Conexión QML/Python | interfaz/qt/controlador.py; recibe acciones y emite señales |
| Estado de cada ejercicio Qt | interfaz/qt/sesion.py; conserva entradas, cálculo y Deshacer |
| Interfaz anterior | gui_tk.py → iniciar_ventana en interfaz/ventana.py |
| Inicio en consola | main.py → menu_principal en interfaz/menus.py |
| Distribución, temas y navegación | CalculadoraVentana; métodos _crear_*, abrir_tema y _cambiar_pestana |
| Qué ocurre al pulsar Calcular | calcular del panel correspondiente; llama al núcleo y después presenta el resultado |
| Qué ocurre al editar datos | marcar_cambio invalida pasos antiguos; _edicion agrupa una carga en una sola acción |
| Deshacer | _capturar guarda datos independientes; deshacer restaura datos manteniendo el método seleccionado |

## Dónde se hace cada cálculo

| Tema | Lugar |
|---|---|
| Suma, resta, escalar, producto, transpuesta, inversas | modulos/modulo_matrices.py |
| Operaciones de filas compartidas | modulos/eliminacion.py; reducir y reemplazar_fila |
| Clasificación y solución general Ax=b | modulos/modulo_sistemas.py; resolver_sistema |
| Combinación e independencia | modulos/modulo_vectores.py |
| Cofactores, Sarrus y triangularización | modulos/modulo_determinantes.py |
| A=LU y sustituciones | modulos/modulo_lu.py |
| Propiedades calculadas por ambos miembros | teoremas/verificadores.py |
| Bisección y SciPy | modulos/numericos/biseccion.py |
| Errores y experimentos | modulos/numericos/errores.py |
| Fraction frente a float y NumPy | modulos/numericos/comparadores.py |

Los módulos calculan y devuelven datos; no piden información ni dibujan botones. Al corregir una fórmula, empezar aquí y en sus pruebas, no en la pantalla.

## Dónde se ve o se guarda

| Parte | Lugar y responsabilidad |
|---|---|
| Catálogo de métodos exactos | interfaz/operaciones.py; entradas, ejemplo y adaptación del resultado |
| Catálogo de semana 12 | interfaz/metodos_numericos.py; campos y despacho al método |
| Formulario exacto | interfaz/panel_algebra.py |
| Formulario aproximado y tabla | interfaz/panel_numerico.py |
| Botones de signos para f(x) | interfaz/numericos/teclado.py; inserta texto sin calcular |
| Entrada de matrices | interfaz/cuadricula.py; cargar y leer |
| Interpretar bloques pegados | interfaz/pegado.py |
| Fracciones e iconos | interfaz/notacion.py; los datos ya llegan calculados |
| Colores | interfaz/tema.py |
| Recorrido breve y temporizador | interfaz/explicacion.py y recorrido.py |
| Todos los pasos | interfaz/desarrollo.py y procedimiento.py |
| Gráficas | interfaz/numericos/graficas.py; se abren solo al solicitarlas |
| Guardado y recuperación entre temas | interfaz/cuaderno.py |
| Archivo personal y nombres | interfaz/biblioteca.py |
| Lista Guardados/Historial | interfaz/guardados.py |
| PDF | interfaz/exportar_pdf.py |

## Antes de cambiar algo

1. Localiza el archivo responsable y lee la docstring de la función.
2. Busca quién la llama antes de cambiar sus parámetros o retorno.
3. Conserva las listas originales: resultados y pasos deben tener sus propias copias.
4. Añade un comentario corto cuando expliques por qué se intercambian filas, se limita un pivote, se protege un archivo o se separa precisión exacta/aproximada. No escribas un comentario que solo repita la línea siguiente.
5. Prueba un ejemplo conocido y un error relevante. Ejecuta las comprobaciones de README antes del PR.

El flujo sigue siendo issue → rama → implementación → comprobaciones → PR → revisión humana cuando se autorice publicar. La IA no integra ni publica automáticamente. El 6 de noviembre el usuario autorizó PySide6 + QML para el próximo avance. La interfaz Tkinter se conserva como respaldo; véase MIGRACION_QT.md.


## Inicio y navegación compacta

`interfaz/inicio.py` contiene las tarjetas por unidad, el menú plegable y las rutas. `ventana.py` abre las sesiones existentes y Biblioteca. `herramientas.py` agrupa botones secundarios sin duplicar su validación. `cuadricula.py` despliega Filas/Columnas desde Cambiar. Consultar [INICIO_Y_NAVEGACION.md](INICIO_Y_NAVEGACION.md) antes de añadir temas. Los comentarios breves explican conservación de sesión y reutilización de acciones.


Para ajustar el ritmo fijo, editar INTERVALO_PASOS_MS en interfaz/recorrido.py (2 segundos). El lenguaje de las dos vistas se adapta en interfaz/lenguaje_pasos.py; los datos y fórmulas originales no se recortan en la vista completa. parametros_vacios en interfaz/metodos_numericos.py distingue datos del ejercicio de tolerancias y ajustes; parametros_defecto sigue reservado a los ejemplos y usos existentes de consola.
