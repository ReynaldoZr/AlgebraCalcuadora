# Estado de la interfaz y avance local

## Actualización 2026-11-04: semana 12

La rama actual es `feat/semana-12-numericos`. El usuario autorizó incorporar Numéricos, incluidos gráficas y comparación con bibliotecas; el estado previo que decía «pendiente» queda superado. Son nueve métodos accesibles por ventana y consola, integrados con tabla, pasos, guardados e historial. La biblioteca utiliza formato 2 y admite los registros exactos de formato 1. Se mantiene Tkinter; PySide6/Qt Quick se reserva para el futuro. Se preparó .venv y «Calculadora escritorio» para IntelliJ, con guía de código y comentarios cortos. No se publica la rama ni se crea PR.

La suite general de esta etapa aprobó 153 pruebas en Windows con las dependencias instaladas. Tras incorporar la referencia racional de propagación volvieron a aprobar las 18 pruebas numéricas. El verificador aprobó 65 archivos Python y el diff no presentó errores de espacios. Se usa revisión y pruebas del código, sin Computer Use o capturas de pantalla. El detalle de límites y criterios está en [SEMANA_12.md](SEMANA_12.md).

## Estado actual: tareas 1 a 6, guardados y estudio, sin publicar

La rama actual es `feat/guardados-y-practica-local`, continuación local de `feat/3-algebra-tareas-1-a-6`. Conserva escalar/transpuesta/producto, sistemas por Gauss/Gauss-Jordan, vectores, determinantes, inversas, LU y 21 verificaciones de propiedades. Añade biblioteca personal persistente, historial, ejemplos por caso, ayudas, copiar/pegar y exportación PDF. La semana 12/Métodos Numéricos queda expresamente pendiente. No se hizo push, PR, integración ni publicación de versión.

El usuario corrigió una ampliación visual excesiva. Se conservan las tres tarjetas, resumen inferior, colores y controles originales. Después autorizó expresamente añadir **Guardados** junto a Calculadora/Todos los pasos y las pequeñas herramientas de estudio. Cada tema conserva sus datos sin introducir pestañas anidadas. Matrices mantiene su sesión original. Véanse [cobertura matemática](ALGEBRA_TAREAS_1_A_6.md) y [biblioteca y estudio](GUARDADOS_Y_ESTUDIO.md).

La primera comprobación general de esta ampliación aprobó 111 pruebas. Después se ajustó la distribución visual por indicación del usuario y aprobaron 26 comprobaciones afectadas: seis de los paneles (incluido tamaño mínimo en los seis temas), dos de la ventana original, cuatro de catálogo/consola y catorce de álgebra. El verificador aprobó 43 archivos Python y el diff no presentó errores de espacios. Estos resultados son locales; no hay CI de una rama publicada ni revisión humana del conjunto. Las comprobaciones definitivas de la última revisión deben acompañar al futuro PR.

La ampliación de biblioteca/estudio aprobó una suite general de 131 pruebas en Windows y una nueva comprobación específica de nombres de propiedades/estado del menú, además de repetir la recuperación de transpuestas tras el último ajuste. El verificador aprobó 52 archivos Python y `git diff --check` no encontró errores de espacios. La exportación real de un ejercicio de inversa produjo un PDF A4 de dos páginas; ambas se renderizaron y revisaron como archivos, sin capturas ni control de pantalla. La prueba de paginación extensa conserva también el último de 110 pasos. Estas comprobaciones no equivalen a CI ni a una publicación.

Último ajuste solicitado: guardar una respuesta directamente desde su tarjeta sin cambiar de pestaña, conservando los atajos Usar como A/B; símbolos junto a los temas y cuadrícula 3×3 para Matrices. Aprobaron trece comprobaciones afectadas de biblioteca, guardado directo, reutilización, iconos, temas y tamaño mínimo. Reglas aprobadas en 52 archivos Python y diff sin errores de espacios. No se usó Computer Use ni se publicó el cambio.

El usuario confirmó que funciona y pidió no volver a usar Computer Use («ChatGPT is using your computer») para verificar hasta nuevo aviso. No reactivar control de pantalla ni capturas por iniciativa propia. Continuar con pruebas del código cuando corresponda.

## Registro histórico de las etapas anteriores

Los párrafos siguientes describen estados anteriores; sus pendientes, ramas y cantidades de pruebas no sustituyen el estado actual de arriba.

Roberto (`roberto7503`) integró el [PR #10](https://github.com/ReynaldoZr/AlgebraCalcuadora/pull/10) en main el 3 de noviembre de 2026 a las 12:59 (Nicaragua). La issue #8 quedó cerrada. El PR #9 se mantiene cerrado sin integrar. La interfaz azul/lavanda descrita abajo pertenece ahora a la base integrada; no se ha publicado una nueva release.

## Continuación local: escalar y transpuesta (issue #2)

Se trabaja desde el main integrado en `feat/2-escalar-matrices`, sin seguimiento remoto. Esta rama añade multiplicación por escalar y transpuesta: núcleo exacto, consola, interfaz, resumen, pasos, reproducción y Deshacer. Ambas usan solo A, además de k en el producto por escalar. B conserva sus datos. La paleta, los editores y la navegación existentes se reutilizan.

El permiso de subida anterior correspondía al PR #10; esta nueva propuesta permanece local hasta autorización expresa. No hacer push, abrir PR, integrar ni publicar una versión por inferir ese permiso anterior. La issue #2 todavía requiere producto matricial: no debe cerrarse por terminar escalar y transpuesta.

Verificación de escalar en Windows: suite de 51 pruebas aprobada, verificador de reglas aprobado en 25 archivos y diff sin errores. Se amplió y comprobó la prueba del tamaño mínimo también con k visible; las siete pruebas de consola volvieron a aprobar tras actualizar la cabecera. Recorrido real de consola con k inválido y decimal correcto; revisión visual de la tarjeta k, resultado y pestaña de desarrollo completo. No se ha ejecutado CI de esta rama local.

## Mejora local terminada: transición y recorrido didáctico

- Cambio entre vistas con una capa que oculta el redibujado y se desvanece en unos 180 ms; temporizador separado del recorrido y cancelable. No se cambia la opacidad de la ventana principal.
- Cada celda avanza por Identificar, Operar, Simplificar cuando procede y Guardar. Intervalo fijo de dos segundos por etapa; Anterior/Siguiente y Reiniciar permiten leer sin reproducción automática.
- Etiquetas de origen y coordenadas, bordes activos y destino R[i,j]. El resultado parcial se revela al guardar; retroceder reconstruye la etapa anterior. La multiplicación desarrolla numeradores y denominadores.
- Todos los pasos conserva la explicación completa con origen, equivalencias, simplificación y destino; no espera la reproducción del recorrido.
- Verificación final: 62 pruebas aprobadas; comprobaciones específicas de pestañas y etapas volvieron a aprobar tras los últimos ajustes. Verificador aprobado en 29 archivos Python y diff sin errores. Revisión visual de identificación, operación y desarrollo completo en Windows; registro de errores de la ventana vacío.

Esta parte queda terminada localmente. No se añaden más operaciones, no se hace push ni se abre un PR. La CI y la publicación de esta rama siguen pendientes de autorización.

## Transpuesta añadida después del recorrido

Por instrucción del usuario se añade Transpuesta · Aᵀ. El ejemplo es A = `[[1/3, -2, 5], [0, 4, 1/2]]` (2×3) y Aᵀ = `[[1/3, 0], [-2, 4], [5, 1/2]]` (3×2). El panel central presenta A[i,j] → R[j,i] y el intercambio de tamaños. La consola incorpora la opción 5 sin renumerar las existentes.

El recorrido visita las posiciones de R por filas: para R[i,j], marca A[j,i]. Sus etapas son Identificar, Ubicar y Guardar, a dos segundos por etapa. No se modifica ni simplifica el valor. Reutilizar el resultado como A permite comprobar la doble transpuesta. B y k no se leen; sus valores se conservan al cambiar de modo. Véase ejemplos/transpuesta.md.

Verificación de esta etapa: 71 pruebas aprobadas en Windows, con matriz rectangular, fila/columna únicas, fracciones, transpuesta doble, conservación de datos, entrada unaria, coordenadas del recorrido y regresión de las operaciones anteriores. Verificador aprobado en 29 archivos Python y diff sin errores. Recorrido real de consola con error recuperable y doble transpuesta; revisión visual de Calculadora y Todos los pasos, con el ejemplo abierto para probar. No hay subida ni PR de esta etapa y todavía falta producto matricial para completar la issue #2.

## Diseño base integrado mediante PR #10

- Fondo azul oscuro, tarjetas azules, acentos lavanda y texto claro; sin acentos verdes.
- Tema Matrices con icono cuadrado de cuatro casillas. No se ofrecen temas futuros como si estuvieran implementados.
- Pestañas internas Calculadora y Todos los pasos. La segunda reduce la barra lateral y aprovecha el ancho para el desarrollo completo, con desplazamiento vertical.
- Matrices editables con fracciones apiladas: clic o Tab enfoca una entrada de texto real. El resultado es de solo lectura; no tiene controles de dimensiones.
- La vista previa conserva tres puntos clave y una igualdad. El desarrollo amplio incluye cada posición, equivalencias de denominador común y simplificación, y el resultado final.
- Reproducir/Pausar, Anterior, Siguiente y Reiniciar; intervalo fijo de 2000 ms, sin selector. No arranca automáticamente.
- Deshacer conserva hasta 50 estados de la sesión, incluidas entradas pendientes, carga, limpieza y último cálculo.
- Alternancia clara/oscura en la esquina superior derecha sin perder datos.
- Editar, cambiar operación, cargar o limpiar cancela temporizadores e invalida el recorrido. El desarrollo anterior se identifica hasta volver a calcular.
- Sin servidor web, dependencias nuevas ni modificaciones de los algoritmos, la consola o la versión publicada.

## Cómo comprobar

Ejecutar `python gui.py`, pulsar Cargar ejemplo y Calcular. Debe producir `[[1/2, 3/10], [3, 3]]`. Avanzar y retroceder; reproducir y pausar; abrir Todos los pasos y volver. Probar el tema claro y oscuro. Limpiar y deshacer para recuperar el cálculo. Editar durante la reproducción: el reloj se cancela y los pasos anteriores quedan marcados como desactualizados. Probar dimensiones 10×10 y el desplazamiento.

La base del PR #10 aprobó 42 pruebas locales y las cuatro combinaciones de CI Windows/Linux con Python 3.11/3.13. El verificador aprobó 25 archivos Python. La revisión visual en Windows incluyó ejemplo, pestañas, desplazamiento y temas. Estas comprobaciones corresponden a la interfaz integrada, no certifican automáticamente las modificaciones posteriores de escalar.

Para comprobar escalar: seleccionar Escalar · kA y cargar el ejemplo; resultado esperado `[[-1/2, -3/20], [3, -6]]`. Probar k = 0, fracciones y errores; editar k durante reproducción, deshacer y volver a Suma/Resta sin perder B. Ejecutar las pruebas y reglas antes de solicitar autorización de subida; no presentar la CI de la base como CI de esta nueva etapa.


## Inicio por unidades · continuación local

La rama `feat/inicio-temas-local` implementa la propuesta combinada aprobada: tarjetas de entrada por unidad, menú Temas plegable, Biblioteca y acciones secundarias compactas. Se conservan los tres paneles, todas las operaciones y los pasos completos. No se ha subido ni abierto PR; ver INICIO_Y_NAVEGACION.md.
