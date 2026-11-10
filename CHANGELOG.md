# Historial de cambios

## Sin publicar

- La tabla y el listado de pasos ocupan el mismo espacio en Qt. En Tk, los procedimientos largos usan tarjetas separadas dentro del área desplazable, conservando todas las fórmulas.

- «Guardar resultado» conserva la salida del cálculo. «Cargar guardado» permite elegir la matriz o el campo numérico donde reutilizarla.

- «Cargar ejercicio» abre la lista de ejercicios guardados desde la calculadora. Las copias creadas en Biblioteca quedan preseleccionadas al abrir la lista.

- En Guardados, «Copiar ejercicio» crea una copia independiente con nombre propio y la selecciona para abrirla.

- La vista previa de f(x) y el desarrollo muestran exponentes enteros en superíndice. Las tarjetas de pasos tienen más espacio vertical. En «Todos los pasos», «Mostrar tabla» usa toda el área del desarrollo y «Volver a los pasos» recupera la lista.

- Migración local autorizada a PySide6 + Qt Quick/QML: inicio por temas, tres tarjetas, edición de matrices, teclado, sesiones por método, cálculo en trabajador, pasos completos y tabla, reloj de dos segundos, Biblioteca compatible, PDF y gráficas. gui.py abre Qt; gui_tk.py conserva la interfaz anterior. Se reutiliza el núcleo sin modificar biseccion.py ni otros algoritmos; dependencias y pruebas Qt separadas. Sin publicación.

- Interfaz numérica: teclado básico para f(x) con cursor, selección y Deshacer; casillas vacías de matrices visibles, ayuda pertinente a cada método y primer paso visible al calcular. Al cambiar de método se retira el resultado anterior; al editar se identifica como desactualizado. Sin modificar biseccion.py ni los algoritmos.

- Bisección: líneas cortas, bloques separados y comentarios breves para facilitar la exposición desde IntelliJ; sin cambios en el cálculo.

- Comentarios breves en los bloques principales de bisección para orientar su explicación: validación, extremos, repetición, cambio de signo y condiciones de parada. Sin cambios en el código ejecutable.

- Ajuste local solicitado: formularios inicialmente vacíos y ejemplos solo por acción explícita; Limpiar vacía datos y escalar sin precargar otro ejercicio. Recorrido fijo de 2 segundos; explicaciones esenciales en la previa y aclaraciones sencillas con fórmulas y matrices completas en Todos los pasos. Sin cambios de diseño o algoritmos matemáticos.

- Diseño combinado aprobado: inicio con tarjetas por unidades y todos los temas actuales, menú Temas plegable sin comprimir las matrices y Biblioteca desde la cabecera. Las sesiones y los pasos se conservan al navegar. Operaciones en un selector; dimensiones detrás de Cambiar y herramientas secundarias en ⋯. Comentarios breves y guía de navegación. Trabajo local en feat/inicio-temas-local, sin publicar.

- Semana 12 local: bisección con tabla, predicción, criterios separados y contraste SciPy; errores, propagación con derivada numérica y referencia racional cuando es aplicable; simulación de truncamiento/redondeo, épsilon/overflow/underflow, bases y estabilidad. Comparación de inversas/sistemas con Fraction, float propio y NumPy, residuos y condición; ejemplos de Hilbert y gráficas Matplotlib bajo demanda.
- Nuevo tema Numéricos y opción 8 de consola, conservando tarjetas y navegación. Biblioteca formato 2 para parámetros aproximados, compatible con registros exactos anteriores; historial y PDF conservan todo el procedimiento sin fingir matrices exactas. Entorno .venv, requisitos, configuración de IntelliJ y guía de código con comentarios esenciales. PySide6/Qt Quick se registra como preferencia futura, sin migración actual. Sin subir rama ni publicar versión.

- Atajo «Guardar resultado…» en la tarjeta de respuesta de Matrices y los demás temas. Usa la misma biblioteca, nombre/símbolo/notas y numeración, sin abrir Guardados ni modificar entradas; se conservan Usar como A/B y la reutilización. Se deshabilita si el resultado está desactualizado o no es matricial. Barra de temas con símbolos matemáticos y cuadrícula 3×3 para Matrices, conservando selección y paleta.

- Biblioteca local en nueva pestaña Guardados: matrices y ejercicios completos con símbolos por operación, nombres automáticos numerados, nombre/símbolo personalizados, notas, búsqueda, recuperación, reutilización entre temas y eliminación confirmada. Persistencia JSON exacta fuera del repositorio con escritura atómica y protección del original ante errores.
- Historial persistente de los últimos cien cálculos válidos, promoción a guardado permanente sin duplicar al abrir, ejemplos por caso, ayudas breves y copiar/pegar matrices como una edición deshacible. Exportación PDF A4 de texto con todos los pasos, sin dependencias externas. Se conservan las tarjetas y el diseño existentes; semana 12 continúa fuera y no se publica la rama.

- Ampliación local de tareas 1 a 6: reducción exacta compartida; Gauss/Gauss-Jordan con clasificación y solución general verificada; operaciones vectoriales, combinación e independencia con relación no trivial; determinantes por cofactores, Sarrus y reducción; inversas por Jordan/adjunta; LU rectangular sin permutación y solución Ax=b. Añadidas 21 comprobaciones de propiedades con ambos miembros y diagnóstico «No aplicable».
- Acceso desde consola y barra lateral, catálogo compartido, ejemplos y procedimientos completos con matrices aumentadas. Se conserva la distribución original de tres tarjetas y únicamente las vistas Calculadora/Todos los pasos; sin pestañas anidadas. Semana 12 y sus bibliotecas quedan fuera. Sin publicación ni cambio de versión.

- Corrección local: Limpiar y Deshacer conservan la operación seleccionada. Si se recupera un cálculo de otra operación, se marca como anterior hasta recalcular. Todos los pasos dibuja las fórmulas de cada etapa y desarrolla el denominador común y la simplificación de sumas fraccionarias del producto; el recorrido breve no se amplía.

- Producto matricial local: validación m×n por n×p y algoritmo propio de tres bucles, opción 6 de consola y Producto · AB en la ventana. Recorrido de fila/columna y pares, productos intermedios, suma y guardado, con fracciones exactas, Deshacer y reutilización. Escalar, transpuesta y producto quedan preparados localmente para revisión de la issue #2, sin publicar una versión.

- Transpuesta local como parte de issue #2: algoritmo propio con listas, opción 5 de consola y opción Aᵀ en la interfaz. Panel de intercambio de tamaños, origen A[j,i] y destino R[i,j] señalados; etapas Identificar/Ubicar/Guardar, reutilización, Deshacer y desarrollo completo. B y k se conservan y no participan. Producto matricial aún pendiente.

- Mejora local del recorrido: etiquetas de origen y destino, bordes activos, etapas de identificación/operación/simplificación/guardado y tres segundos por etapa. El resultado parcial se revela al guardar cada celda, con navegación reversible. Desarrollo completo con productos de numeradores/denominadores e instrucciones explícitas.
- Cambio entre Calculadora y Todos los pasos con desvanecimiento breve de una vista preparada, sin ver la construcción de tarjetas; capa y temporizador cancelables al navegar, editar y cerrar. La ventana principal conserva su opacidad.

- En preparación local (parte de issue #2): producto por escalar con algoritmo propio, entrada exacta y validaciones; opción 4 de consola y tarjeta k en lugar de B en la ventana. Vista previa, desarrollo completo, reproducción y Deshacer adaptados a kA. Transpuesta y producto matricial se añaden en esta misma rama.
- Interfaz anterior integrada en main por Roberto mediante PR #10; issue #8 cerrada. Esta integración no crea una release ni cambia la versión publicada.

- Diseño local aprobado: fondo azul oscuro, acentos lavanda, icono cuadrado de Matrices, fracciones apiladas y alternativa clara. Vista previa breve y pestaña amplia con todo el desarrollo, desplazamiento y aviso de cálculo anterior.
- Recorrido con Anterior, Reproducir/Pausar, Siguiente y Reiniciar, intervalo fijo de tres segundos sin selector y cancelación al editar. Deshacer conserva hasta 50 estados locales, incluidos limpieza y último cálculo.
- PR #9 cerrado sin integrar; el usuario autorizó subir la nueva propuesta como PR abierto para revisión humana. No se cambia la versión publicada ni se incorpora un servidor web; integración y publicación siguen pendientes de decisión humana.
- Interfaz gráfica opcional con Tkinter/ttk: matrices editables de hasta 10x10, suma/resta, procedimiento y teoremas, ejemplo y reutilización de resultados.
- Lectura numérica y presentación compartidas entre consola y ventana; se conservan los algoritmos y la versión publicados.
- Pruebas con widgets reales y pantalla virtual para la CI de Linux; la falta de pantalla/Tk no puede omitir silenciosamente las pruebas gráficas en CI.
- Instrucciones de IA y colaboración: issue, rama, comprobaciones y PR abierto; integración y publicación reservadas a decisión humana. Guía paso a paso y plantilla de PR actualizadas.

## v0.1.0 — 2026-11-03

- Menú de consola y módulo de matrices con cabecera ASCII y opción 0 de teoremas.
- Entrada validada de matrices rectangulares, enteros, fracciones y decimales exactos.
- Suma y resta mediante funciones propias; procedimiento por posición.
- Reutilización del último resultado mientras la aplicación permanece abierta.
- Ejemplos, pruebas matemáticas y recorridos de consola.
- Comprobaciones de estructura, plantillas de issue y PR y flujo de integración continua.
- Guías de organización, restricciones por unidad y ampliación progresiva.

Primera entrega funcional. Publicación identificada por la etiqueta v0.1.0; integración mediante PR #5. Las siguientes correcciones compatibles usarán v0.1.1, v0.1.2, etc.
