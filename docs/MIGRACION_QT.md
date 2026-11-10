# Migración local de escritorio a PySide6 + QML

Autorizada por el usuario el 6 de noviembre de 2026 para el avance de la próxima semana. Rama `feat/qt-qml-local`, que conserva el trabajo local previo. No se ha publicado una issue, rama, PR ni versión. La preferencia anterior de mantener Tkinter queda superada por esta autorización explícita. No se atribuye al profesor una autorización de PySide6 que no consta en las fuentes revisadas.

## Ejecutar y volver a la interfaz anterior

Desde `AlgebraCalcuadora`:

```text
python -m pip install -r requirements-interfaz.txt
python -m pip install -r requirements-numericos.txt
python gui.py
```

En IntelliJ se conserva **Calculadora escritorio**, con `.venv/Scripts/python.exe` y `gui.py`. También funciona `gui_qt.py`. Para comparar o volver temporalmente a la interfaz anterior usa `gui_tk.py` o **Calculadora Tkinter (respaldo)**. La consola continúa en `main.py` sin importar Qt ni requerir sus paquetes. No se necesita navegador, servidor ni conexión de red para usar la ventana.

## Encontrar cada responsabilidad

| Lugar | Responsabilidad |
|---|---|
| interfaz/qt/aplicacion.py | QApplication, motor QML y proveedor de imágenes |
| interfaz/qt/controlador.py | Acciones de la pantalla, trabajo de cálculo, biblioteca y reloj |
| interfaz/qt/sesion.py | Entradas por método, último cálculo, revisión y Deshacer |
| interfaz/qt/catalogo.py | Adaptación de los catálogos existentes; llama al núcleo |
| interfaz/qt/presentacion.py | Convierte resultados a tokens visuales exactos |
| interfaz/qt/qml/Principal.qml | Inicio, navegación, tres tarjetas y diálogos |
| Paleta.qml, Boton.qml, Entrada.qml, Selector.qml, Tarjeta.qml | Estilos compartidos |
| Campo.qml y EditorMatriz.qml | Entradas y teclado básico |
| Formula.qml, Fraccion.qml y MatrizVista.qml | Representación matemática |
| Pasos.qml | Tabla y desarrollo completos con listas que reciclan su dibujo |
| Biblioteca.qml | Búsqueda, guardados, historial y reutilización |
| interfaz/numericos/figuras.py | Figuras compartidas, sin dependencia de una ventana |
| interfaz/numericos/graficas_qt.py | Dibujo en memoria para Qt; no modifica bisección |

## Contratos que se conservan

- `modulos/` y `teoremas/` siguen siendo independientes de la interfaz. La consola, sus cabeceras y la opción de teoremas se mantienen.
- QML presenta datos y gestiona interacciones; no resuelve sistemas ni implementa bisección. Python llama a los métodos existentes. No se cambian las restricciones de NumPy/SciPy ni el LU sin permutación.
- Los enteros grandes y Fraction cruzan a QML como cadenas de numerador y denominador; nunca como Number de JavaScript. Los campos conservan el texto original hasta validar.
- Cada método tiene su propia sesión. No se cargan ejercicios automáticamente; navegar conserva entradas y resultados del método correspondiente. Limpiar y Deshacer no cambian de método.
- El teclado reemplaza la selección o inserta en el cursor. Una pulsación es una edición deshacible.
- La vista previa de f(x) y el desarrollo muestran los exponentes enteros en superíndice. Al escribir `x^123 + 45`, solo el 123 queda elevado. En «Todos los pasos», pulsa «Mostrar tabla» para ocupar el área del desarrollo con la tabla. «Volver a los pasos» recupera la lista.
- El recorrido breve reutiliza las etapas originales; el desarrollo mantiene todas las fórmulas, matrices y filas. El reloj es de 2000 ms y se detiene al editar, navegar o cerrar.
- El cálculo se ejecuta sobre copias en un trabajador. QML no accede al JSON ni escribe desde el hilo de cálculo. Durante el trabajo se deshabilitan las entradas.
- La Biblioteca usa el mismo archivo y formato JSON con escritura atómica. Recuperar un ejercicio no duplica el historial. Guardar resultado no cambia las entradas. La reutilización solo admite matrices exactas.
- En Guardados, selecciona un ejercicio y pulsa «Copiar ejercicio». La copia conserva los datos, los pasos, el símbolo y las notas. Puedes cargarla con «Abrir ejercicio».
- En la tarjeta de resultado, «Guardar resultado» conserva la salida del cálculo. Con «Cargar guardado» puedes elegir una matriz o un campo numérico del método activo, o abrir un ejercicio completo de la Biblioteca. Si la salida reúne varios valores, puedes copiar su resumen.
- El PDF usa el exportador existente. Las figuras se construyen con los mismos datos que en Tk y solo se cargan bajo demanda. La migración no exige cambiar los algoritmos de semana 12.

## Comprobar

```text
python -m unittest tests.test_qt_sesion tests.test_qt_interfaz -v
python -m unittest discover -s tests -v
python herramientas/comprobar_reglas.py
git diff --check
```

Las pruebas Qt utilizan `QT_QPA_PLATFORM=offscreen` y bibliotecas temporales o en memoria. No toman capturas, no controlan la pantalla del usuario ni acceden a su archivo personal. CI instala las dependencias gráficas y exige Qt mediante `CALCULADORA_EXIGIR_QT=1`; los errores de carga QML o de enlaces durante los recorridos fallan las pruebas. Las pruebas Tk anteriores se mantienen.

Para probar manualmente: abre Numéricos, escribe una función con el teclado o carga un ejemplo, calcula y consulta las dos vistas. Repite en Matrices con fracciones, cambia dimensiones, prueba Deshacer, guarda y recupera un ejercicio. Comprueba las gráficas y la exportación elegida por ti. La revisión visual de la pantalla real queda pendiente de la prueba del usuario; no se presume realizada por pasar pruebas automáticas.

## Alcance de esta entrega local

Se conectan todos los temas existentes, no se añaden métodos matemáticos. Se conserva Tkinter para comparar mientras se revisa Qt; retirarlo sería otra tarea. No se incluye instalador ni distribución como ejecutable. La publicación y revisión humana siguen el flujo de FLUJO_IA.md.

## Comprobación local del 6 de noviembre

- 11 pruebas nuevas de sesión, carga QML e interacción aprobadas, incluidas gráficas y PDF.
- Batería completa: 177 pruebas aprobadas, conservando las pruebas Tk existentes.
- Reglas verificadas en 83 archivos Python; `git diff --check` sin errores.
- Comparación SHA-256 de todos los archivos Python de modulos/: sin cambios respecto al inicio de la migración. Bisección y los demás algoritmos se reutilizaron intactos.
- No se revisó la pantalla mediante Computer Use. La valoración visual queda para la prueba del usuario. La CI remota no se ejecutó porque no se publicó un PR.
