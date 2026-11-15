# Jacobi · Programa 8 · Issue #14

El núcleo se encuentra en modulos/numericos/iterativos.py. Recibe A cuadrada,
B y X₀ como vectores planos, tolerancia positiva y máximo entero entre 1 y 10000.
Acepta listas o tuplas con valores convertibles a números finitos, incluidos
enteros, Fraction y textos decimales. La aritmética de esta unidad es aproximada.

Cada componente nueva se calcula usando el vector anterior completo.
El error es la mayor diferencia absoluta entre componentes consecutivas.
Se detiene cuando ese error es estrictamente menor que la tolerancia.
La dominancia diagonal estricta es una condición suficiente de convergencia.
Cuando falta, el cálculo sigue con una advertencia y su límite de iteraciones.
Una diagonal nula se rechaza explicando que se necesita reordenar ecuaciones.

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
  dominantes, convergio, error, motivo, columnas y filas.
- Cada fila es (k, x1, ..., xn, error máximo). Las columnas se adaptan al orden
  de A. Las entradas y los vectores de la tabla tienen copias independientes.
- convergio solo es verdadero al cumplir la tolerancia. Al agotar el máximo
  se conserva la aproximación. Ante desbordamiento se conserva la última
  iteración finita y se explica la interrupción. error es None si ninguna
  iteración pudo completarse.

La conexión visual corresponde a #16. La referencia NumPy puede incorporarse
en la comparación de esa etapa. El orden de filas se tratará en #15.

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

Fuente del alcance y permiso de NumPy/SciPy en esta unidad
[plan semanal 13](https://uamvirtual.uam.edu.ni/grado/mod/resource/view.php?id=1037473).
El contrato de esta primera etapa se publica para que Roberto pueda
reutilizarlo en Gauss-Seidel y revisar su comportamiento antes de integrarlo.
