# Interfaz gráfica de escritorio

La ventana se incorpora por solicitud del usuario del 3 de noviembre de 2026, antes de continuar las operaciones de la issue #2. El trabajo se sigue en la [issue #8](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/8). Es una interfaz alternativa y no reemplaza la consola exigida por el profesor.

## Ejecutar y probar

1. Ejecutar `python gui.py` desde la raíz del proyecto.
2. Pulsar Cargar ejemplo y después Calcular.
3. Resultado de suma esperado: [[1/2, 3/10], [3, 3]]. Revisar el procedimiento.
4. Elegir Resta y volver a calcular. Resultado: [[1/6, -1/10], [-7, 5]].
5. Escribir `1/0` en una celda: debe aparecer la posición del error sin borrar entradas ni el último cálculo.
6. Corregirla y volver a calcular; usar el resultado como A o B para encadenar operaciones.
7. Cambiar dimensiones y pulsar Aplicar. Al ampliar, se conservan las celdas coincidentes; al reducir se solicita confirmación por el recorte.
8. Consultar Teoremas clave y probar Tab, Ctrl+Enter y desplazamiento horizontal/vertical.

## Archivos y responsabilidades

| Archivo | Responsabilidad |
|---|---|
| gui.py | Lanzador opcional; explica si Tkinter no está instalado |
| interfaz/ventana.py | Composición, estilos, eventos y estado gráfico |
| interfaz/cuadricula.py | Tamaños, casillas, desplazamiento y posición de errores |
| interfaz/datos.py | Conversión numérica exacta compartida con consola |
| interfaz/formato.py | Texto de matrices y pasos compartido con consola |
| modulos/modulo_matrices.py | Algoritmos existentes; no cambian por añadir la ventana |
| tests/test_ventana.py | Recorridos con widgets reales, resultados y recuperación de errores |

La interfaz gráfica llama a sumar_matrices/restar_matrices y recibe listas. El procedimiento presenta esos resultados; no introduce un segundo algoritmo. No importa ni inicia la consola. La consola tampoco importa Tkinter: el ordenador sin Tk puede seguir usando main.py.

## Contratos y decisiones

- Tkinter/ttk pertenece a la biblioteca estándar y depende de Tcl/Tk. Es un componente opcional de algunas distribuciones de Python; la instalación disponible en este equipo incluye Tk 8.6. Fuentes: [Tkinter](https://docs.python.org/3/library/tkinter.html) y [ttk](https://docs.python.org/3/library/tkinter.ttk.html).
- Se admiten de 1 a 10 filas y columnas por editor. Es un límite de presentación para esta primera UI; no limita los algoritmos o la consola.
- Todas las celdas se convierten desde texto a Fraction sin pasar por float. Los resultados siguen siendo listas independientes.
- La sesión conserva el último cálculo válido. Un cambio de entradas u operación lo marca como anterior; una operación inválida no lo reemplaza ni borra los datos.
- Los cambios de tamaño requieren Aplicar antes de calcular. Reducir una matriz pide confirmación. Limpiar reinicia entradas y memoria de esta ventana.
- Las variables de Tk se mantienen mientras existan sus casillas; de lo contrario Tkinter puede perder el texto y los avisos de modificación.
- Se usan clases únicamente para agrupar widgets y su estado. Las operaciones matemáticas siguen siendo funciones pequeñas del núcleo.
- No se cambia main.VERSION ni se publica una etiqueta al abrir el PR.

## Cómo añadir otra operación después

Primero implementar y probar la función matemática en su módulo según COMO_AGREGAR.md. Después añadir su opción y evento en ventana.py. Reutilizar EditorMatriz para leer entradas y las funciones de formato para presentar salidas. Si la operación es unaria, no obligar a completar B: adaptar el formulario a sus datos reales.

Añadir pruebas de interacción y de errores que sean nuevos para esa operación. No duplicar los cálculos dentro de callbacks y no añadir botones que prometan operaciones aún no implementadas.

## Comprobaciones y límites

Las pruebas generales cubren consola y cálculo. Las de ventana crean widgets reales para comprobar suma/resta, fracciones, errores, dimensiones pendientes, crecimiento/recorte, limpieza y reutilización. En Linux necesitan pantalla virtual Xvfb. En CI la variable CALCULADORA_EXIGIR_GUI obliga a que se ejecuten; una omisión local no debe presentarse como interfaz verificada.

La revisión visual se realiza en Windows. No se afirma haber revisado visualmente Linux, macOS, lectores de pantalla ni todos los ajustes de escala. Tkinter en Windows expone un árbol de accesibilidad limitado; antes de ampliar mucho la aplicación conviene evaluar accesibilidad con el uso real del equipo. Los resultados no se guardan al cerrar y aún no hay instalador o archivo ejecutable distribuido.
