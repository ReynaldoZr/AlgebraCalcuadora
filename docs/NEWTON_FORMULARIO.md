# Newton en la calculadora · issue 36

La propuesta conecta el núcleo y los proveedores de #33–#35 al catálogo existente de Numéricos. No cambia las tres tarjetas, paleta, navegación ni esquema de Biblioteca. La instrucción de Reynaldo del 18/11/2026 autoriza trabajar esta primera conexión, antes asignada a Roberto. Las mejoras específicas de pasos/tabla (#37) y gráfica (#38) conservan su alcance y siguen pendientes.

Las orientaciones académicas disponibles son Sesión 22 y Plan semanal 14; el enunciado definitivo del Programa 9 todavía debe confirmarse. Las tolerancias adicionales y valores iniciales de ajuste se explican en [NEWTON_NUCLEO.md](NEWTON_NUCLEO.md).

## Cómo probar en IntelliJ

1. Ejecutar la configuración **Calculadora escritorio**, que abre `gui.py`.
2. Abrir **Numéricos** y seleccionar **Newton-Raphson · raíces de funciones**.
3. La función, x0 y derivada comienzan vacías. Escribir un ejercicio o pulsar **Cargar ejemplo**. El primer ejemplo es exp(-x)-x desde 0, con derivada -exp(-x)-1.
4. Elegir derivada analítica o numérica. En analítica se muestra f'(x); en numérica se oculta y aparece h (por ejemplo 1e-5). El cálculo de derivadas vive en `modulos/numericos/`, no en QML.
5. Elegir criterio absoluto (cambio en x) o porcentual (cambio en %), tolerancia del cambio, tolerancia de residuo y máximo. Pulsar **Calcular**.
6. El ejemplo exp(-x)-x, tolerancia 0.0001 y residuo 1e-8 converge aproximadamente a 0.5671432904 en cuatro iteraciones. El resumen identifica estado, motivo, iteraciones y comprobación en la función.
7. **Guardar resultado…** guarda el escalar para reutilizarlo en un campo numérico compatible. Cambiar de método conserva la sesión en Qt; Limpiar y Deshacer mantienen el método seleccionado. Guardar un ejercicio completo desde Biblioteca conserva modo, h y ambas tolerancias sin guardar funciones Python.

El ejemplo **Ciclo cúbico** muestra no convergencia y «Última aproximación», no una raíz válida. Un fallo de dominio sin punto evaluado no se guarda como escalar ficticio. Las entradas inválidas dan un diagnóstico y exigen corregir/recalcular. Un ejercicio que no converge puede consultarse con su causa e historial; su último valor, si existe, se identifica como aproximación sin converger.

Los pasos y la tabla genéricos ya consumen Calculo/Paso. No se presenta esta conexión como cumplimiento de la mejora didáctica específica #37. **Ver gráfica** permanece deshabilitado para Newton hasta la conexión y revisión de #38; no se dibuja un gráfico de otro método bajo su nombre.

## Organización y compatibilidad

- `interfaz/metodos_numericos.py`: registro del método, ejemplos y despacho al adaptador; comparte etiquetas, opciones y visibilidad condicional.
- `newton_adaptador.py`: valida la entrada, recibe el proveedor real de derivada y prepara el resumen. Expresiones de función y derivada pasan por el analizador seguro existente.
- `interfaz/qt/`: formulario y sesión, invalidación al editar, retorno de navegación y resultado guardable. QML presenta; no resuelve Newton ni convierte el resultado para calcular.
- Consola y Tk reciben el mismo método y etiquetas. Bisección conserva criterio intervalo/porcentual; Newton usa absoluto/porcentual. Tk adapta las opciones al cambiar de método sin cargar un ejercicio.
- Biblioteca mantiene su JSON existente. Pruebas con memoria o rutas temporales; sin datos personales ni modificaciones de las dependencias.

Pruebas de aceptación: ambos modos, entradas vacías/ejemplos explícitos, error de tolerancia, expresiones inválidas, ciclo/dominio, navegación, Limpiar/Deshacer, persistencia y reutilización del escalar; regresiones completas y CI de Windows Python 3.11 y 3.13. Ninguna prueba controla la pantalla de la persona.
