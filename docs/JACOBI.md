# Jacobi · Programa 8 · Issue #14

## Lectura de resultados en Qt · Issue #32

Jacobi, Gauss-Seidel y su comparador muestran una fila por variable, referencia NumPy y estado/iteraciones por método dentro de la tarjeta existente. «Referencia para comparar» es una aproximación independiente, no una solución exacta. El redondeo es solo visual y aumenta su precisión cuando ocultaría diferencias; cálculos y guardados conservan sus valores originales.

El residuo comprueba el ajuste de las ecuaciones y se distingue del cambio entre iteraciones y de la diferencia con NumPy. Los motivos de fallo, desbordamiento y advertencias de relajación se muestran sin abrir «Ver detalles técnicos». Ese botón despliega tolerancia, orden, dominancia, vectores completos y referencia. Los demás métodos conservan sus resúmenes anteriores.

## Núcleo y criterios

El núcleo se encuentra en modulos/numericos/iterativos.py. Recibe A cuadrada,
B y X₀ como vectores planos, tolerancia positiva y máximo entero entre 1 y 10000.
Acepta listas o tuplas con valores convertibles a números finitos, incluidos
enteros, Fraction y textos decimales. La aritmética de esta unidad es aproximada.

Cada componente nueva se calcula usando el vector anterior completo.
El error es la mayor diferencia absoluta entre componentes consecutivas.
Se detiene cuando ese error es menor o igual que la tolerancia.
La dominancia diagonal estricta es una condición suficiente de convergencia.
Cuando falta, el cálculo sigue con una advertencia y su límite de iteraciones.
Una diagonal nula exige reordenar ecuaciones antes de iterar. Si la persona
desactiva el reordenamiento, se explica esa condición sin dividir por cero.
Si el error crece entre dos iteraciones, se registra una advertencia sin concluir
automáticamente divergencia ni interrumpir una posible convergencia posterior.
Al terminar se calcula el residuo máximo de Ax−b sobre el sistema original.

## Probar el ejemplo del plan

Desde la raíz del proyecto, con el intérprete configurado en IntelliJ, ejecutar
este fragmento en una consola Python.

```python
from modulos.numericos.iterativos import jacobi

a = [[4, -1, 1], [4, -8, 1], [-2, 1, 5]]
b = [7, -21, 15]
calculo = jacobi(a, b, [0, 0, 0])
print(calculo.valor)
print(calculo.datos['motivo'])
print(calculo.datos['residuo'])
print(calculo.datos['advertencias'])
print(len(calculo.datos['filas']))
```

La primera fila contiene k=1, X=(1.75, 2.625, 3) y error máximo 3.
Se alcanza aproximadamente (2, 4, 3) en 11 iteraciones con tolerancia 0.0001.
Repetir con max_iteraciones=1 devuelve el primer vector e indica el límite.

## Contrato para Gauss-Seidel y la integración

- validar_datos_iterativos devuelve copias de A, B, X₀ y la tolerancia convertida.
- dominancia_diagonal recibe la matriz numérica cuadrada validada y devuelve
  una tupla de indicadores por fila.
- jacobi devuelve el Calculo existente del proyecto. Su valor es el último
  vector finito. Los pasos explican el método y conservan cada iteración.
- datos contiene metodo, matriz, vector_b, inicial, tolerancia, max_iteraciones,
  dominantes, convergio, error, motivo, columnas, filas, residuo y advertencias.
- Cada fila es (k, x1, ..., xn, error máximo). Las columnas se adaptan al orden
  de A. Las entradas y los vectores de la tabla tienen copias independientes.
- convergio solo es verdadero al cumplir la tolerancia. Al agotar el máximo
  se conserva la aproximación. Ante desbordamiento se conserva la última
  iteración finita y se explica la interrupción. error es None si ninguna
  iteración pudo completarse.
- residuo_sistema recibe A, B y el vector aproximado validados y devuelve
  la norma máxima de Ax−b. Devuelve None si el cálculo del residuo desborda
  y se registra una advertencia explícita. Un error pequeño entre iteraciones
  se interpreta junto con ese residuo al verificar la solución.

## Integración local de la issue #16

En Numéricos, elegir «Jacobi · sistemas iterativos». La primera tarjeta permite
editar A. La segunda recibe b, X₀, tolerancia y máximo de iteraciones. Los
vectores se escriben con comas entre componentes y punto para los decimales.
Los formularios empiezan vacíos. «Cargar ejemplo» coloca el sistema del plan.

El resumen muestra vector, estado, error, residuo y contraste independiente con
numpy.linalg.solve. Si la referencia es singular o no finita, el resultado de
Jacobi se conserva con la explicación correspondiente. «Todos los pasos» y
«Mostrar tabla» contienen todas las iteraciones. «Ver gráfica» muestra el error
de Jacobi. Guardar un ejercicio conserva A, b, X₀ y parámetros.

Los casos disponibles son «Diagonal dominante», «Reordenar 2×2», «Diagonal con
cero» y «Sin convergencia». Jacobi, Gauss-Seidel y el comparador permiten elegir
si se reordenan ecuaciones. Se aplica la misma permutación a A y b; el residuo
y la referencia se verifican sobre las entradas originales.

El reordenamiento asigna una fila diferente a cada posición diagonal mediante
caminos aumentantes. Prioriza los coeficientes dominantes y conserva posiciones
cuando es posible. No enumera todas las permutaciones ni promete un orden óptimo
si no existe dominancia estricta. Si ningún emparejamiento evita los ceros,
se explica por qué no se puede continuar. Las variables y X₀ no se permutan.

Gauss-Seidel admite un factor opcional `0 < λ < 2`; `λ=1` ejecuta el algoritmo
habitual. Con otros valores se combina el componente nuevo con el anterior:
`x_nuevo = λ * x_GS + (1 - λ) * x_anterior`. El intervalo admitido no garantiza
convergencia para cualquier matriz, incluso si es diagonal dominante. Los pasos
y el resumen lo advierten. El comparador usa Gauss-Seidel habitual (`λ=1`).

El comparador conserva las tablas completas sin rellenar ni recortar y dibuja
las dos curvas de error. Cada método muestra su propio motivo de terminación,
incluido el desbordamiento sin perder el último vector finito. No se confunde
esa interrupción con agotar el máximo de iteraciones.

## Verificación

```text
python -m unittest tests.numericos.test_iterativos -v
python -m unittest discover -s tests -v
python herramientas/comprobar_reglas.py
git diff --check
```

Las pruebas incluyen solución conocida, primera iteración con X₀ no nulo,
parada, dimensiones inválidas, diagonal nula, números no finitos,
divergencia y conservación de entradas.

### Casos de comprobación del Programa 8

En el comparador, con X₀ nulo y ε=0.0001, los ejemplos explícitos permiten
repetir las siguientes comprobaciones desde consola, Qt y Tk:

| Caso | Resultado esperado | Iteraciones Jacobi / Gauss-Seidel |
| --- | --- | --- |
| Diagonal dominante | X ≈ (2, 4, 3), ambos convergen | 11 / 7 |
| Reordenar 2×2 | Orden (2, 1), X ≈ (32/17, 31/17) | 7 / 5 |
| Diagonal con cero | Orden (2, 1), X = (1, 2) | 3 / 3 |
| Sin convergencia | Ambos conservan tabla, vector y advertencias | 20 / 20, máximo |

Consultar «Todos los pasos», «Mostrar tabla» y «Ver gráfica». En el primer caso
debe haber 18 filas en total y curvas de 11 y 7 puntos, respectivamente.
Guardar y recuperar el ejercicio debe conservar el reordenamiento elegido.
Para una diagonal imposible, A=[[0,1],[0,2]], se explica la validación sin forzar
un resultado. Las pruebas de desbordamiento distinguen esa parada del límite.

Reynaldo confirmó el 15 de noviembre que el PDF y los demás materiales de la
entrega ya están listos y autorizó cerrar el seguimiento #16. Esa confirmación
del equipo completa el seguimiento documental; las comprobaciones técnicas
anteriores corresponden al código y conservan su evidencia por separado.

Fuentes del alcance inicial y del enunciado definitivo
[plan semanal 13](https://uamvirtual.uam.edu.ni/grado/mod/resource/view.php?id=1037473) y
[Tarea 8](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=1043170).
El núcleo y la presentación comparten este contrato entre ambos métodos.

## Entrega confirmada en UAM

El cierre publicado es el martes 17 de noviembre de 2026 a las 09:00.
El Programa 8 exige tres casos documentados de convergencia, reordenamiento
y advertencia o falta de convergencia. La comparación debe informar el residuo,
la diferencia respecto a Gauss-Jordan o numpy.linalg.solve, las iteraciones
y las diferencias entre ambos métodos. La gráfica compara errores cuando
ambos métodos tienen datos válidos.

El ZIP debe contener el código actualizado, informe PDF y evidencias
(tablas, gráficas y validación). El PDF incluye portada, objetivo, explicación
breve, validaciones, comparación y capturas legibles de los tres casos.
Nombre indicado por el enunciado
`Programa 8_Grupo X_Apellido1_Apellido2.zip`.

El apartado 2 permite NumPy, Pandas, Matplotlib y SymPy cuando sea necesario.
Los algoritmos iterativos siguen implementados por el equipo.
Newton-Raphson figura como contenido de estudio en la Semana 14.
