# Inicio por unidades y navegación compacta

Diseño combinado aprobado por Reynaldo el 4 de noviembre de 2026. Implementación local en `feat/inicio-temas-local`, conservando los cambios matemáticos y de semana 12 anteriores. Sin issue remota, push, PR ni nueva versión publicada; la autorización actual es desarrollar y probar localmente.

## Qué hace cada pantalla

Al ejecutar `gui.py` se muestra Inicio. Álgebra lineal reúne Matrices, Sistemas, Vectores, Determinantes, Inversas y LU; Propiedades y teoremas tiene su acceso propio. Métodos numéricos abre los nueve métodos actuales de semana 12. Las tarjetas muestran descripciones cortas, no cálculos ni datos inventados.

Elegir una tarjeta sustituye Inicio por el formulario de ese tema. Matrices conserva A, B o regla y Resultado. Sistemas muestra sus entradas y métodos correspondientes; no utiliza el formulario de suma como sustituto. Las operaciones se seleccionan en un desplegable. Calculadora y Todos los pasos siguen siendo dos vistas de la misma sesión, sin pestañas anidadas.

Temas abre un menú superpuesto que no comprime las tarjetas. Elegir un tema lo cierra y recupera su sesión. El botón × cierra el menú sin cambiar de vista. Inicio pausa los recorridos y conserva entradas, método, resultado, historial de deshacer y pasos; volver no calcula de nuevo ni añade entradas al historial. Ctrl+Enter no calcula desde Inicio o Biblioteca.

Biblioteca abre Guardados/Historial desde cualquier pantalla con la misma persistencia personal. El último tema elegido sigue siendo la fuente de las acciones de estudio y reutilización. Para volver al cálculo, elegirlo desde Temas. Guardar directamente desde el resultado continúa sin abandonar el ejercicio.

## Controles compactos

- Cada matriz muestra su tamaño aplicado y Cambiar. Este botón despliega Filas/Columnas y Aplicar; abrirlo no redimensiona. Aplicar mantiene las validaciones anteriores y solicita confirmación si se recortan celdas. Un error conserva los controles para corregirlo.
- El menú ⋯ de cada entrada ofrece Copiar matriz/Pegar matriz. El de Resultado conserva Usar como A/B según el tema. Los comandos reutilizan las acciones y los estados de los botones originales; no eluden validaciones.
- Estudio mantiene guardar ejercicio, exportar PDF, ejemplos por caso y ayudas. Modo claro/oscuro conserva los datos y actualiza también el inicio y los símbolos.
- La vista previa y su recorrido de dos segundos siguen disponibles. Todos los pasos mantiene el desarrollo completo, sin limitar filas, fórmulas o iteraciones.

## Dónde cambiar cada parte

| Archivo | Responsabilidad |
|---|---|
| `interfaz/inicio.py` | Catálogo visual TEMAS, tarjetas, cabecera y menú plegable |
| `interfaz/ventana.py` | Composición; mostrar_matrices, abrir_tema, mostrar_biblioteca |
| `interfaz/herramientas.py` | Menús que invocan botones existentes respetando su estado |
| `interfaz/cuadricula.py` | Tamaño compacto, desplegar dimensiones y copiar/pegar |
| `interfaz/cuaderno.py` | Misma biblioteca y estudio; acceso desde cabecera |
| `interfaz/panel_algebra.py` | Selector de métodos y tres tarjetas de cada tema exacto |
| `tests/test_inicio.py` | Inicio, accesos, conservación de sesiones y tamaño explícito |

Para agregar un tema real, crear primero su cálculo y adaptador siguiendo COMO_AGREGAR.md. Después añadir su nombre y descripción a TEMAS y su icono en notacion.py, ubicar su tarjeta en el grupo apropiado y conectar abrir_tema al panel correspondiente. No crear botones para funciones inexistentes. El inicio no importa NumPy/SciPy/Matplotlib ni contiene algoritmos matemáticos.

## Cómo comprobar

Ejecutar la suite general, el verificador de reglas y `git diff --check`. Las pruebas usan bibliotecas en memoria o rutas temporales. Para probar a mano en IntelliJ, usar Calculadora escritorio: Inicio → Matrices → cargar ejemplo → Calcular → Todos los pasos → Inicio → Sistemas → regresar a Matrices. El resultado anterior debe conservarse. Revisar Biblioteca y Cambiar; no se deben perder datos al abrir/cerrar los menús.

La consola y los algoritmos de las tareas 1–6 no cambian. Continúan sin bibliotecas numéricas externas; semana 12 conserva su excepción limitada. Los comentarios son breves y explican decisiones; la explicación amplia permanece en esta guía.


## Resultado de la comprobación local

Se ejecutaron 158 pruebas en Windows: 157 aprobaron en la suite y una detectó que el formulario de bisección recortaba un campo en tamaño mínimo. Se retiró el encabezado numérico duplicado y se repitió esa prueba, que aprobó para los nueve métodos. No se repitió la suite completa después de ese ajuste localizado. La prueba de dimensiones desplegadas también aprobó tras priorizar su barra sobre el lienzo. El verificador aprobó 68 archivos Python y git diff --check terminó sin errores de espacios.

Se ejecutó la versión actual desde el botón Ejecutar de IntelliJ y se confirmó su Inicio. Posteriormente el usuario volvió a prohibir el control visual hasta nueva indicación; esta restricción queda registrada en AGENTS.md. No se publicó la rama ni se abrió un PR.


## Ajuste de formularios y explicaciones

Los temas nuevos comienzan con casillas y datos de ejercicio vacíos, incluido el escalar. Las tolerancias, el máximo de iteraciones y las opciones de cálculo mantienen sus valores iniciales. Cargar ejemplo rellena el ejemplo correspondiente solo por acción de la persona; Limpiar vuelve a dejar vacíos los datos y es deshacible. Navegar conserva el trabajo introducido o cargado expresamente, sin insertar ejercicios por iniciativa de la aplicación.

El ritmo es fijo de 2 segundos por etapa, centralizado en INTERVALO_PASOS_MS de interfaz/recorrido.py. interfaz/lenguaje_pasos.py añade explicaciones sencillas: la previa muestra una frase esencial junto a la cuenta del ejercicio actual; Todos los pasos conserva el detalle original, todas las fórmulas y matrices, con una aclaración cuando ayuda a entender la acción. No se generan ejercicios adicionales dentro del recorrido.


Validación del ajuste posterior: aprobaron 26 pruebas de lenguaje, etapas, inicio y semana 12; nueve casos de matrices/guardado y la comprobación de fórmulas completas de la vista amplia también aprobaron. Verificador: 70 archivos Python; diff sin errores de espacios. Se usaron pruebas del código, sin control de pantalla. No se repitió la suite general completa para este ajuste localizado. Para ver los cambios en una ventana ya abierta, reiniciar Calculadora escritorio desde IntelliJ.
