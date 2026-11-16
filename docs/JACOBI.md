# Jacobi · Programa 8 · Issue #14

El núcleo se encuentra en modulos/numericos/iterativos.py. Recibe A cuadrada,
B y X₀ como vectores planos, tolerancia positiva y máximo entero entre 1 y 10000.
Acepta listas o tuplas con valores convertibles a números finitos, incluidos
enteros, Fraction y textos decimales. La aritmética de esta unidad es aproximada.

Cada componente nueva se calcula usando el vector anterior completo.
El error es la mayor diferencia absoluta entre componentes consecutivas.
Se detiene cuando ese error es menor o igual que la tolerancia.
La dominancia diagonal estricta es una condición suficiente de convergencia.
Cuando falta, el cálculo sigue con una advertencia y su límite de iteraciones.
Una diagonal nula se rechaza explicando que se necesita reordenar ecuaciones.
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

Los casos disponibles son «Diagonal dominante», «Reordenar 2×2», «Diagonal con cero» y «Sin convergencia». En «Gauss-Seidel · sistemas iterativos» y «Comparar Jacobi y Gauss-Seidel» se admite reordenar ecuaciones (aplicando la misma permutación a A y b y verificando el residuo sobre el sistema original), factor de relajación `0 < λ < 2`, tablas completas de ambos métodos sin rellenar ni recortar y gráfica comparativa de error.

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

Fuentes del alcance inicial y del enunciado definitivo
[plan semanal 13](https://uamvirtual.uam.edu.ni/grado/mod/resource/view.php?id=1037473) y
[Tarea 8](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=1043170).
El contrato de esta primera etapa se publica para que Roberto pueda
reutilizarlo en Gauss-Seidel y revisar su comportamiento antes de integrarlo.

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
