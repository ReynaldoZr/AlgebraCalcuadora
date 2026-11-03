# Interfaz gráfica de escritorio

La ventana sigue la [issue #8](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/8). Usa Tkinter/ttk de la biblioteca estándar y conserva la consola requerida por el profesor. El PR #9 está cerrado sin integrar; el usuario autorizó presentar esta nueva propuesta como PR **pendiente de revisión humana**, según [ESTADO_UI_LOCAL.md](ESTADO_UI_LOCAL.md).

## Probar

1. Ejecutar `python gui.py` desde la raíz.
2. Pulsar Cargar ejemplo y Calcular. Esperado: `[[1/2, 3/10], [3, 3]]`.
3. Elegir Resta y calcular: `[[1/6, -1/10], [-7, 5]]`.
4. Hacer clic en una fracción para editarla como texto (`1/3`, `0.5`, `-2`). Tab recorre entradas; al salir de ellas vuelve la notación apilada. Ctrl+Enter calcula.
5. Usar Anterior, Reproducir/Pausar, Siguiente y Reiniciar. El intervalo es fijo de tres segundos; Reiniciar deja el primer paso en pausa.
6. Abrir Todos los pasos: muestra todas las posiciones con equivalencias de fracciones y resultado, con desplazamiento. Volver a calculadora conserva entradas y estado.
7. Cambiar claro/oscuro desde la esquina superior derecha. El tema inicial es azul oscuro con lavanda.
8. Limpiar y pulsar Deshacer para recuperar entradas y cálculo. Deshacer conserva hasta 50 estados en memoria, sin persistencia al cerrar.
9. Escribir `1/0` en una celda: debe identificar su posición sin borrar los datos ni el cálculo anterior. Corregir y calcular otra vez.
10. Reutilizar el resultado como A o B. Para redimensionar, pulsar Aplicar; ampliar conserva datos y reducir solicita confirmación por el recorte. Hay desplazamiento para tamaños grandes.
11. Consultar Teoremas desde el encabezado; la ventana de consulta es de solo lectura.

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
| interfaz/datos.py | Conversión exacta común a consola y ventana |
| interfaz/formato.py | Presentación de texto para consola |
| modulos/modulo_matrices.py | Algoritmos existentes, independientes de Tkinter |
| tests/test_ventana.py | Recorridos con widgets reales y conservación de datos |
| tests/test_recorrido.py | Navegación y cancelación con reloj controlado |

## Contratos

- El cálculo llama a `sumar_matrices` y `restar_matrices`, recibe listas independientes y no importa la interfaz. La consola tampoco importa Tkinter.
- El editor admite 1–10 filas/columnas; ese límite es visual y no se extiende al núcleo o la consola.
- Las entradas se convierten desde texto directamente a Fraction, sin pasar por float. Las fracciones apiladas representan esos valores exactos, sin generar imágenes ni usar bibliotecas matemáticas externas.
- El desarrollo recibe operandos y resultados del núcleo. Las equivalencias visuales usan denominador común y numeradores sin simplificar para explicar cada posición; no sustituyen la respuesta del núcleo ni vuelven a solicitar resultados intermedios.
- El último cálculo válido se conserva ante errores. Editar lo marca como anterior y deshabilita su reproducción; la pestaña amplia también avisa si está desactualizado.
- La reproducción usa `after`, nunca sleep ni un bucle bloqueante. Editar, cargar, limpiar, cambiar operación o cerrar cancela el evento pendiente. Cambiar de pestaña pausa el recorrido.
- Cada editor mantiene sus variables Tk mientras existan sus casillas. Durante reconstrucciones se suprimen avisos intermedios que podrían acceder a widgets destruidos.
- El historial guarda copias de entradas, dimensiones pendientes, operación y último resultado. Restaurarlo no inicia reproducción.
- Los temas se cambian sobre los mismos widgets; no se reconstruye la sesión para cambiar colores. No se persisten preferencias al cerrar.
- Main y su versión publicada no cambian. No hay servidor ni migración a una interfaz web.

## Añadir otra operación

Implementar y probar primero el algoritmo en su módulo, según COMO_AGREGAR.md. Después conectar su opción en ventana.py. Reutilizar el editor, la notación y la vista de desarrollo. Una operación unaria debe pedir solo sus entradas reales. Ampliar el contenido de los pasos cuando sea necesario sin introducir algoritmos nuevos dentro del dibujo.

Los colores se ajustan en tema.py; la representación matemática en notacion.py; los pasos completos en desarrollo.py. No reescribir toda la ventana para añadir un estilo o un paso. Los futuros temas se habilitarán únicamente cuando tengan funcionalidad real.

## Verificación y límites

Ejecutar `python -m unittest discover -s tests -v`, `python herramientas/comprobar_reglas.py` y `git diff --check`. Las pruebas de ventana usan widgets reales; en Linux requieren Xvfb. CI usa CALCULADORA_EXIGIR_GUI=1 para impedir omisiones silenciosas.

La revisión visual local se hace en Windows; no implica haber revisado macOS, todas las escalas o lectores de pantalla. Tkinter tiene un árbol de accesibilidad limitado en Windows. Las fórmulas largas y matrices grandes tienen desplazamiento; la ventana requiere al menos 1120×760 unidades de Tk. No hay instalador, exportación ni guardado de sesiones.
