# Avance de gráficas y revisión del PR 46

El PR de Roberto incorpora una base compartida para las gráficas #23–#30. Reynaldo autorizó su revisión e integración y aprobó el nuevo tema oscuro negro/morado el 21/11/2026. El tema claro y las tres tarjetas se conservan. Este avance no cierra las ocho issues ni modifica los algoritmos matemáticos.

## Qué se puede probar

1. En Numéricos, cargar explícitamente un ejemplo, calcular y pulsar **Ver gráfica**.
2. En Bisección, Jacobi, Gauss-Seidel y el comparador: usar anterior/siguiente o reproducción manual cada dos segundos. Seleccionar una fila consume los valores ya calculados, sin ejecutar el algoritmo otra vez.
3. En Bisección, ampliar función o error y volver a ambos. El error corresponde al criterio elegido: cota absoluta o porcentaje, con tolerancia de las mismas unidades.
4. Acercar/alejar con botones o rueda y restablecer. En un eje logarítmico el zoom se aplica en logaritmos para conservar límites positivos; en el panel ampliado se mantiene la identidad del panel de error.
5. En el comparador y redondeo/truncamiento, ocultar o restaurar curvas mediante las casillas. Las longitudes originales y los ceros se conservan.
6. En propagación, consultar la función y la aproximación lineal alrededor de x y x+Δx. Las muestras de dominio inválido interrumpen el trazado; esto no garantiza detectar toda discontinuidad de una función arbitraria.
7. En sistemas, comparar barras por variable frente a la solución racional. El error de NumPy se obtiene frente a Fraction, no mediante una conversión que lo redondee artificialmente a cero.
8. En inversas, consultar el mapa n×n y la mayor desviación; la escala logarítmica solo se utiliza si sus datos son positivos. Si hay ceros se conserva escala lineal. Zoom y restablecimiento preservan la orientación de filas/columnas.
9. Guardar la imagen y comprobar ambos temas. Al cerrar, editar o navegar se detiene la reproducción gráfica.

## Resultados y pasos

La tarjeta de resultados admite tablas de otros métodos, con precisión completa en detalles. Una tabla extensa tiene desplazamiento vertical y horizontal; una inversa 10×10 no obliga a alargar la tarjeta con cien filas visibles a la vez.

Newton y bisección distinguen una raíz convergente de la última aproximación sin converger. El motivo de fallo queda visible. La diferencia con SciPy no se etiqueta como cambio entre iteraciones. Con dos raíces de extremos, bisección conserva ambas y señala el valor principal que se guardará.

Los pasos completos de Newton conservan las fórmulas y cifras que entregó el núcleo. Se añade la resta explícita del cambio y se muestra el estado final del núcleo; no se vuelve a decidir convergencia comparando cantidades redondeadas en la interfaz. La asociación entre pasos y registros usa el orden del contrato, no números extraídos de títulos.

## Pendientes de #23–#30

- Consulta de coordenadas/valores al pasar el cursor y arrastre directo del gráfico.
- Consulta individual de barras y celdas, con sus valores exacto, float propio y NumPy; actualmente inversas muestra la desviación máxima.
- Selección/reproducción por iteración de la simulación de redondeo/truncamiento.
- Ampliar aceptación y comprobaciones de cada issue para las interacciones anteriores, dimensiones máximas y casos límite particulares.

No presentar este avance como implementación completa de todos esos requisitos. Las issues conservan sus propios criterios y futuras entregas.

## Comprobación

El renderizador vive en `interfaz/numericos/figuras.py`; Qt consume imágenes mediante `graficas_qt.py` y su controlador. La información estructurada se prepara en `resumen_tabla.py`. QML presenta controles y datos; no ejecuta los cálculos del profesor.

Las pruebas de revisión incluyen estancamiento, ciclo, dominio inválido, máximo insuficiente, dos extremos, precisión de Newton y títulos independientes; Qt comprueba zoom logarítmico, panel ampliado, pausa, series y una tabla de cien filas. Se usa una biblioteca aislada y Qt sin pantalla, sin modificar los guardados personales. Antes de integrar se exige la suite completa, el verificador y ambas CI de Windows 3.11/3.13.
