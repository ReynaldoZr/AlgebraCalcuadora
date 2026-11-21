# Reglas de trabajo de la calculadora

## Estado de la interfaz y siguiente etapa

Actualización del 15 de noviembre de 2026. El PR #12 integró el avance de álgebra, biblioteca, métodos numéricos e interfaz PySide6 + QML en main, con la excepción de revisión autorizada por Reynaldo para ese PR. Las nuevas tareas siguen el flujo habitual de PR y revisión humana.

El PR #17 integró Jacobi y sus validaciones compartidas (#14), por autorización de Reynaldo tras verificar las pruebas. La #15, asignada a Roberto, añade Gauss-Seidel y reordenamiento. La #16 conecta los métodos a la interfaz. Reynaldo asume la corrección de extremos de bisección en #13 por indicación del 15 de noviembre. Consultar el estado real de GitHub antes de comenzar y conservar cambios locales ajenos. Leer docs/JACOBI.md, docs/SEMANA_12.md y docs/GUIA_CODIGO.md.

## Introducción y límite de la IA

La IA prepara cambios para que una persona pueda revisarlos. Su recorrido es **issue → rama → implementación → comprobaciones → pull request → CI → revisión humana**. Leer [docs/FLUJO_IA.md](docs/FLUJO_IA.md) antes de empezar. La entrega de la IA es un PR abierto y comprobado; la decisión de integrarlo corresponde a Reynaldo u otro humano autorizado.

- Vincular el cambio a una issue y trabajar en una rama propia desde main actualizado. No escribir directamente en main.
- Ejecutar las comprobaciones, abrir el PR y revisar la CI del último commit. Si algo falla, corregir en esa misma rama y volver a comprobar. Si queda un bloqueo, informarlo y mantener el PR como borrador.
- Al terminar, entregar enlaces de issue y PR, resumen del cambio, instrucciones para probarlo, resultados de las comprobaciones y pendientes reales.
- **Detenerse antes de integrar:** no hacer merge, squash o rebase hacia main, no activar auto-merge ni entrar en una cola de integración, no autoaprobar el PR y no usar otra cuenta para aparentar una revisión humana.
- No cerrar la issue como completada, crear etiquetas, publicar releases, adelantar la versión publicada ni desactivar protecciones para terminar la tarea. Registrar la propuesta en «Sin publicar».
- Que las pruebas estén verdes o que se haya pedido «hacer la tarea», «subir los cambios» o «abrir el PR» no autoriza integrarlo. Para una actuación posterior de integración o publicación hace falta una instrucción humana explícita para ese PR, después de su revisión; no inferirla del permiso de desarrollar.
- No sustituir la revisión por una aprobación de la propia IA. Atender correcciones posteriores en la misma rama y dejar que el humano vuelva a decidir sobre el estado actualizado.

## Contexto y lectura inicial

Calculadora local de Álgebra Lineal para dos estudiantes, con funciones comprensibles y defensa individual. Primera implementación: v0.1.0, suma y resta de matrices. Leer README.md, docs/ESTRUCTURA.md y docs/COMO_AGREGAR.md; consultar docs/REVISION_UAM.md y docs/VERSIONES.md según la tarea. Revisar Git y preservar cambios ajenos antes de editar.

## Estructura

- main.py inicia; interfaz/ lee, muestra y navega; modulos/ calcula; teoremas/ contiene enunciados y futuros verificadores; tests/ comprueba comportamiento; docs/ explica decisiones.
- Mantener los nombres exigidos por UAM: main.py, modulos/, teoremas/, modulo_matrices.py y, cuando se implemente, modulo_lu.py. Mantener menús, cabeceras ASCII y opción 0 de teoremas.
- Añadir archivos solo cuando tengan funcionalidad real; el mapa futuro no representa código ya existente.
- Reutilizar funciones existentes. El cálculo no importa interfaz. Usar imports absolutos y evitar dependencias circulares.

## Reglas matemáticas

- Tareas 1–6: algoritmos propios con listas, bucles, condiciones y funciones. Sin NumPy/SciPy/SymPy ni sustitutos externos; sin atajos de math. Fraction está permitido expresamente en tareas 5 y 6.
- Excepción: plan semanal 12 permite NumPy/SciPy y gráficas opcionales con Matplotlib. Sus algoritmos viven en modulos/numericos/ y pruebas en tests/numericos/. El adaptador Matplotlib/Tk está en interfaz/numericos/. No cargar dependencias al iniciar la calculadora ni hacer que el álgebra anterior dependa de ellas. SymPy/pandas no quedan autorizados por esta excepción.
- Ampliación del 15 de noviembre, Programa 8, apartado 2: se permiten NumPy para operaciones y validación, Pandas para tablas, Matplotlib para gráficas y SymPy cuando se necesite manejo simbólico en la unidad numérica. El verificador admite estos imports dentro de su ámbito numérico. Incorporar una dependencia solo cuando la funcionalidad la necesite. Jacobi y Gauss-Seidel conservan ciclos propios; los solucionadores de referencia verifican su resultado. Fuente y contrato actualizado en docs/JACOBI.md.
- Cálculo sin input/print. Operaciones devuelven listas y valores reutilizables, no números dibujados en texto. Conservar entradas originales y evitar compartir filas mutables con los resultados.
- En esta etapa usar enteros/Fraction en el álgebra exacta. Convertir el texto decimal directamente a Fraction, sin pasar por float. La aproximación numérica tendrá contratos y tolerancias separados.
- Antes de cambiar nombres o retornos públicos, localizar consumidores y actualizar llamadas, documentación y pruebas afectadas.
- Los futuros verificadores calculan ambos lados con funciones existentes; no solicitan reingresar resultados intermedios. Validan precondiciones antes del veredicto.
- El futuro LU del Programa 6 es sin permutación. Si necesita intercambio de filas, detener y explicar que requiere PA=LU; no presentar el resultado como A=LU tras pivotear.

## Estilo y documentación

- Nombres descriptivos en español y funciones de una responsabilidad. Unas 25 líneas por función son una orientación, no un límite que justifique fragmentación artificial.
- Docstring inicial por archivo con propósito, tema y autoría confirmada; docstring breve por función con entradas y retorno. No inventar integrantes.
- Comentarios para explicar decisiones matemáticas o casos especiales. Explicaciones amplias en docs; no comentar cada línea ni conservar código viejo comentado.
- El usuario pidió comentarios cortos que le permitan orientarse y trabajar desde IntelliJ. Conservar docstrings por función y comentarios de decisiones en validación, pivotes, guardado y navegación; no inflar cada línea. El mapa práctico está en docs/GUIA_CODIGO.md.
- Cambios localizados: una operación nueva no autoriza reescribir toda la aplicación, incorporar un servidor o cambiar tecnologías. Separar refactorizaciones amplias y justificar el problema que resuelven.
- El usuario aprobó el 4 de noviembre de 2026 la propuesta combinada: inicio por unidades con tarjetas, menú Temas plegable, Biblioteca desde la cabecera y herramientas secundarias agrupadas. `interfaz/inicio.py` coordina la navegación; conservar las sesiones al volver al inicio o cambiar de tema. Las dos vistas de cálculo permanecen; Guardados/Historial se abre como Biblioteca. Detalles en docs/INICIO_Y_NAVEGACION.md.
- El usuario exige conservar la base del diseño aprobado: tres tarjetas (entrada A, segunda entrada o regla, resultado), resumen inferior y colores azul/lavanda. Autorizó expresamente una tercera pestaña «Guardados» junto a Calculadora/Todos los pasos y herramientas pequeñas de estudio. No introducir pestañas anidadas ni reorganizar las tarjetas por añadir temas. Las nuevas operaciones se adaptan al diseño existente; cambios visuales amplios requieren una propuesta previa.
- La tarjeta de resultado mantiene tanto el guardado directo en la biblioteca (sin navegar a otra vista) como los atajos Usar como A/B. Guardar no debe modificar entradas o perder el cálculo vigente. Los temas llevan símbolos matemáticos y Matrices usa una cuadrícula 3×3; conservarlos al ajustar el diseño.
- Biblioteca e historial son datos personales locales: JSON exacto fuera del repositorio, sin pickle, eval ni carga dinámica de clases. Conservar los archivos originales ante errores y usar sustitución atómica. No hacer que los tests accedan a la biblioteca real: inyectar `Biblioteca()` en memoria o una ruta temporal. Los algoritmos matemáticos continúan sin entrada/salida ni dependencia de la biblioteca, el PDF o Tk.
- La nueva implementación debe ser comprendida por el equipo. No copiar código del equipo anterior para disfrazarlo mediante renombrado.
- El 6 de noviembre el usuario autorizó expresamente la migración de escritorio a PySide6 + Qt Quick/QML y los ajustes necesarios para el avance de la próxima semana. `gui.py`/`gui_qt.py` abren Qt; `gui_tk.py` conserva la interfaz anterior durante la transición. La presentación y sus adaptadores viven en `interfaz/qt/`, los componentes en `interfaz/qt/qml/`. Conservar Python como única fuente de los cálculos; no resolver ni redondear el álgebra en JavaScript/QML. Las fracciones cruzan el puente como texto exacto. El permiso de interfaz no cambia las restricciones matemáticas ni autoriza publicación.

- Ajuste posterior del usuario: los formularios nuevos comienzan sin datos de ejercicio ni escalar precargados. Los ejemplos se cargan solo por acción explícita; conservar el trabajo introducido o cargado por la persona al navegar. El recorrido tiene ritmo fijo de 2 segundos (INTERVALO_PASOS_MS); la previa explica lo esencial y Todos los pasos mantiene todas las fórmulas con lenguaje sencillo.

## Verificación y colaboración

- Por indicación de Reynaldo del 15 de noviembre, el soporte y las comprobaciones automáticas se centran únicamente en Windows, con Python 3.11 y 3.13. No añadir trabajos de Linux ni exigirlos para integrar. Conservar el resto de protecciones y exigir ambas comprobaciones de Windows en el último commit. Las menciones históricas de otras plataformas no son requisitos actuales.

- El 15 de noviembre Reynaldo aprobó la nueva paleta propuesta por Roberto en el PR #20: verde salvia/crema en claro y azul profundo en oscuro. Esta autorización sustituye únicamente la restricción anterior de colores azul/lavanda; conservar las tarjetas, navegación y demás reglas de diseño. La autorización de corregir e integrar este PR es puntual y no elimina la revisión humana para trabajos posteriores.

- El 21 de noviembre Reynaldo aprobó expresamente el tema oscuro negro/morado (obsidiana/amatista) del PR #46. Sustituye el azul oscuro de Qt y su gráfica; conserva el claro salvia/crema y la estructura de tarjetas y navegación. La autorización de revisar e integrar este PR es puntual; no elimina las comprobaciones ni autoriza cambios visuales futuros sin revisión.

- Última indicación del usuario (4 de noviembre de 2026): no volver a usar Computer Use («ChatGPT is using your computer»), ayuda visual, capturas ni control de pantalla hasta que él indique que es necesario. La autorización anterior para abrir desde IntelliJ ya no habilita nuevas acciones visuales. Continuar con revisión y pruebas del código.
- Ejecutar `python -m unittest discover -s tests -v` y `python herramientas/comprobar_reglas.py` antes del PR. Comprobar manualmente el recorrido de consola afectado cuando cambie la interacción.
- Añadir pruebas de resultados conocidos, límites matemáticos y errores relevantes; no pruebas que solo repitan la implementación.
- Cada mejora usa issue, rama y PR según docs/TRABAJO_EN_EQUIPO.md. El PR debe indicar alcance, fuente, validación y limitaciones. No inventar enlaces ni pruebas ejecutadas.
- Actualizar README/guías si cambia uso o estructura; registrar cambios bajo «Sin publicar» en CHANGELOG. La integración, el cierre definitivo de la issue y la publicación de versiones quedan sujetos a la decisión humana del flujo anterior.
- No subir contraseñas, sesiones, calificaciones, copias privadas de Moodle ni los entregables del grupo anterior. Referenciar fuentes por enlace.
- Si una indicación académica cambia, registrar fuente, fecha y ámbito en docs/DECISIONES.md. Un permiso de una unidad no se extiende a todo el repositorio.
- Al terminar, explicar qué cambió, por qué, cómo se verificó y cualquier pendiente concreto. AGENTS.md y las comprobaciones no sustituyen la revisión del compañero.
