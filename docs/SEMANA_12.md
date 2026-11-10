# Semana 12: Métodos Numéricos

Implementación local autorizada el 4 de noviembre de 2026, en `feat/semana-12-numericos`. No es una release ni un PR publicado. Fuente: [plan semanal 12, página 3](https://uamvirtual.uam.edu.ni/grado/mod/resource/view.php?id=1031827). El usuario confirmó el permiso para NumPy y SciPy. Matplotlib corresponde a la ampliación gráfica opcional del mismo plan.

## Cómo probar en IntelliJ IDEA

El proyecto es la carpeta `AlgebraCalcuadora`, no la carpeta superior. Se preparó la configuración compartida **Calculadora escritorio** en `.run/Calculadora escritorio.run.xml`, con `gui.py` y el intérprete local `.venv/Scripts/python.exe`. IntelliJ tiene que utilizar ese entorno para encontrar NumPy, SciPy y Matplotlib. La configuración incluida es para Windows; en otros sistemas se selecciona `.venv/bin/python`.

En la ventana elegir **Numéricos → método → Cargar ejemplo → Calcular**. La pantalla mantiene las tres tarjetas. **Todos los pasos y tabla** muestra todas las iteraciones y fórmulas. **Ver gráfica** abre la figura cuando es aplicable; su barra permite guardar la imagen. El recorrido conserva dos segundos por etapa. Guardar ejercicio conserva entradas, parámetros y procedimiento; no convierte una aproximación flotante en una matriz exacta reutilizable.

La consola mantiene sus opciones previas y añade **8. Métodos numéricos**. En este submenú 0 consulta teoremas y 99 vuelve. Los campos muestran valores por defecto; Enter los conserva.

En los formularios con f(x), el teclado básico inserta x, operaciones, paréntesis y potencias en la posición del cursor; × y ÷ escriben * y /. Una selección se reemplaza y cada pulsación se puede deshacer. No modifica el algoritmo de bisección. Al calcular se muestra el primer paso; el resto puede recorrerse cada dos segundos o consultarse completo. Al cambiar de método se retira la respuesta de la selección anterior, conservando las entradas; editar un cálculo lo marca como anterior hasta recalcular. Punto flotante es una demostración sin datos de entrada: basta pulsar Calcular. Las casillas vacías de las matrices permanecen visibles y editables.

Para preparar otro equipo:

```text
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-numericos.txt
.venv\Scripts\python.exe gui.py
```

Para probar:

```text
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\python.exe herramientas/comprobar_reglas.py
git diff --check
```

La instalación local se comprobó con Python 3.12.14, NumPy 2.5.4, SciPy 1.18.1 y Matplotlib 3.11.2. Las dependencias tienen rangos en requirements-numericos.txt para que pip resuelva versiones compatibles con Python 3.11/3.13 de la CI. La CI se prepara para instalar estas dependencias; sus resultados remotos solo existirán al autorizar publicar el PR.

## Cobertura

| Solicitud del profesor | Implementación |
|---|---|
| Bisección obligatoria | Función como texto, intervalo, tolerancia, predicción de reducciones, tabla completa, paro, residuo y contraste SciPy |
| Error absoluto, relativo y porcentual | Cálculo directo con relativo/porcentual no definidos cuando la referencia es cero |
| Propagación | Derivada central, estimación lineal, cambio directo y referencia racional exacta para polinomios/aritmética compatibles |
| Truncamiento frente a redondeo | Interés compuesto, referencia Decimal de 100 cifras y ambos errores en todas las iteraciones |
| Punto flotante | 0.1+0.2, comparación Fraction, épsilon float32/64 y overflow/underflow float32 deliberados |
| Representación decimal/binaria | Descomposición por potencias de base 2 o 10, cifras y resto exacto de una expansión truncada |
| Estabilidad | Cancelación en sqrt(x+1)−sqrt(x), reformulación racionalizada y referencia Decimal |
| Exacto frente a flotante | Inversa o sistema con nuestros algoritmos Fraction, recorrido Gauss-Jordan float y contraste NumPy; errores, residuos y cond(A) |
| Matriz casi singular | Ejemplos de Hilbert exacta, por defecto 5×5; admite órdenes 1 a 10 en el núcleo |
| Gráficas opcionales | Función y cota de bisección, propagación, acumulación de errores y errores por elemento en comparación matricial |
| Integración y evidencias | Menú, ejemplos, pasos completos, historial, guardados y exportación PDF de parámetros y desarrollo |

Newton-Raphson, Jacobi/Gauss-Seidel y otros métodos de semanas posteriores no se presentan como parte de la tarea 7 ni se añaden sin un alcance concreto.

## Criterios de bisección

Se requiere a<b, valores finitos, tolerancias positivas y cambio de signo, salvo raíz exacta en un extremo. La continuidad es una hipótesis que debe comprobarse matemáticamente: muestrear una función arbitraria no demuestra continuidad. Un fallo de dominio comunica un error; el máximo de iteraciones y el estancamiento flotante no se anuncian como convergencia.

El formulario distingue dos criterios:

- **intervalo**: `(xu-xl)/2 ≤ tolerancia`, en unidades de x;
- **porcentual**: `100·|xr_actual−xr_anterior|/|xr_actual| ≤ tolerancia`, en porcentaje.

En ambos se exige también `|f(xr)|≤tolerancia_f`, o f(xr)=0. El porcentaje de la primera iteración y de xr=0 se muestra como no definido. No se mezcla la tolerancia porcentual con el ancho absoluto.

La fórmula `ceil(log2((b-a)/E))` predice reducciones del intervalo para la tolerancia absoluta. No predice el número exigido por el residuo ni se aplica directamente al porcentaje. En el polinomio del profesor, el ancho predice 13 reducciones; el criterio adicional de residuo puede exigir 14 iteraciones. No se fuerza la tabla a coincidir con un número si las condiciones todavía no se cumplen.

La función admite x, pi, e, +, −, *, /, ^ y sin/sen, cos, tan, exp, log/ln, log10, sqrt y abs. Los ángulos están en radianes. `log` es natural. Se recorre un AST validado, sin eval ni ejecución de instrucciones. Hay límites de longitud, profundidad y exponente para evitar expresiones desproporcionadas. Las entradas escalares son decimales con punto o notación científica; una fracción puede escribirse dentro de la función como `1/3`.

Antes de reproducir ejercicios del material se verifican sus extremos: para x³−4x−1 en [1,2], f(1)=−4 y f(2)=−1, por lo que se informa falta de cambio de signo. Ese intervalo necesita revisión; [2,3] sí lo ofrece. No se altera silenciosamente la función ni se fabrica una tabla de convergencia.

SciPy se ejecuta como referencia independiente con tolerancia absoluta en x, no con el porcentaje del formulario. Se informa la diferencia. Si el contraste externo no termina, se conserva el resultado propio con su diagnóstico; no se inventa una referencia.

## Exactitud, error y persistencia

Los resultados exactos de las tareas 1 a 6 conservan int/Fraction y sus validaciones. La comparación de errores usa Fraction.from_float frente al número exacto original para no ocultar redondeo convirtiendo ambos a float antes de restarlos. Los residuos son `max|A·Ainv−I|` o `max|A·x−b|`. `cond(A)` usa la norma 2 de NumPy por defecto. Un residuo pequeño no garantiza un error pequeño si A está mal condicionada.

La propagación tiene referencia racional exacta para operaciones/polinomios admitidos: x³ en 2.5 y Δx=0.01 produce cambio exacto 188251/1000000. Para funciones trascendentes se indica que el cambio directo también es aproximado; no se lo llama exacto.

La biblioteca pasa al **formato 2** para añadir parámetros numéricos textuales y permitir ejercicios sin matriz de entrada. Lee los registros exactos de formato 1 sin cambiar sus números; solo escribe formato 2 al guardar. Las fórmulas aproximadas se conservan como texto y los datos originales como parámetros, sin una falsa matriz cero. Versiones futuras desconocidas siguen protegidas contra sobrescritura. Un cliente anterior puede rechazar el nuevo formato: no sobrescribirlo con una versión antigua de la aplicación.

## Archivos

- `modulos/numericos/funciones.py`: lectura de funciones y referencias racionales.
- `biseccion.py`: algoritmo, tabla y contraste SciPy.
- `errores.py`: errores, propagación, experimentos, simulación y bases.
- `comparadores.py`: recorrido flotante, Hilbert, errores y NumPy.
- `interfaz/metodos_numericos.py`: catálogo de campos, despacho y resumen.
- `interfaz/panel_numerico.py`: las tres tarjetas, tabla, pasos y sesión.
- `interfaz/numericos/graficas.py`: único puente Matplotlib/Tk.
- `interfaz/menu_numerico.py`: entrada y salida de consola.
- `tests/numericos/`: pruebas numéricas, interfaz y aislamiento de dependencias.

Las bibliotecas se cargan bajo demanda. Importar la consola o la ventana no carga numpy/scipy/matplotlib; el resto de la calculadora puede seguir funcionando sin ellas. No se autorizan SymPy o pandas por esta excepción.

## Comprobación local

La suite general aprobó 153 pruebas en Windows. Tras añadir la referencia racional en propagación se repitieron y aprobaron las 18 pruebas de la unidad numérica, incluidos GUI, guardado/reapertura, tablas, gráficas sin ventanas, consola y aislamiento de imports. El verificador aprobó 65 archivos Python y el diff no presentó errores de espacios. No se usó Computer Use ni control de pantalla. La configuración de ejecución de IntelliJ se validó como XML; se utiliza el intérprete del entorno preparado. No se ha publicado el cambio ni ejecutado una CI remota de esta rama.
