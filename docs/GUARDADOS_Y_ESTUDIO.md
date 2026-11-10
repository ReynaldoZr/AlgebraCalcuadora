# Guardados y herramientas de estudio

**Actualización de semana 12:** la biblioteca usa ahora formato 2 para conservar parámetros numéricos y sus aproximaciones. Lee los guardados exactos del formato 1 sin cambiar sus números. Los ejercicios numéricos se recuperan y exportan completos, aunque no tengan una matriz de entrada o resultado. No se convierten aproximaciones en matrices exactas. Véase [SEMANA_12.md](SEMANA_12.md).

Esta ampliación permanece local en `feat/guardados-y-practica-local`, sin push, PR ni versión publicada. El usuario autorizó una pestaña adicional para guardar matrices y ejercicios y las mejoras de estudio propuestas. No se incluye semana 12/Métodos Numéricos. Se mantienen las tres tarjetas, los colores y las vistas Calculadora/Todos los pasos; se añade **Guardados**, sin pestañas anidadas.

## Uso

1. Para una matriz, introduce o pega sus valores y abre **Guardar / Estudio → Guardar matriz A/B/b/C** según el método. No hace falta calcular para guardar una entrada.
2. Para un ejercicio completo, pulsa **Calcular → Guardar / Estudio → Guardar ejercicio completo**. Se conservan método, entradas, escalar cuando corresponde, resumen, resultado y todos los pasos.
3. Para guardar solo la respuesta matricial, usa **Guardar matriz resultado**. El nombre y el símbolo sugeridos corresponden a la operación calculada.
4. Puedes dejar el nombre vacío para generar **Transpuesta 1**, **Transpuesta 2**, etc.; editar el símbolo sugerido **Aᵀ**; o escribir tu propio nombre, símbolo y notas. Los nombres se comparan sin distinguir mayúsculas para evitar duplicados. El contador automático no se reinicia al eliminar elementos.
5. En **Guardados**, busca por nombre, operación, símbolo, tema o notas. Selecciona un elemento para ver su resumen y matriz. **Nombre y notas** permite modificar también el símbolo sin cambiar los datos matemáticos.
6. **Abrir ejercicio** recupera su método y entradas y recalcula en la calculadora. Abrirlo no crea otra entrada idéntica en el historial. El desarrollo guardado original permanece independiente, aunque los algoritmos cambien en el futuro.
7. **Usar matriz** permite elegir una entrada o el resultado del guardado y el destino A/B/b/C del método que estabas usando. Se copia como una edición deshacible. Los límites de cuadrícula siguen siendo 10×10.
8. **Ver desarrollo** amplía el contenido de Guardados con todas las fórmulas y matrices conservadas; **Volver a la lista** regresa sin perder la selección. **Eliminar** solicita confirmación y quita únicamente ese elemento.

Los ejercicios modificados necesitan volver a calcular antes de guardar o exportar la versión actual. Esto evita etiquetar resultados anteriores como si correspondieran a las nuevas entradas. Puedes recuperar un cálculo anterior desde el historial.

### Guardar directamente desde el resultado

La tarjeta de respuesta ofrece **Guardar resultado…**: abre el mismo diálogo de nombre, símbolo y notas y crea un guardado matricial en la biblioteca. Al confirmar permaneces en la calculadora, con las entradas y la respuesta intactas. Puedes usar ese guardado más adelante en cualquier tema. El botón no se habilita para resultados anteriores sin recalcular ni para ejercicios que no producen una matriz.

Se conservan **Usar como A/B** y **Usar resultado como A** para encadenar operaciones inmediatamente. Guardar no copia ni reemplaza las entradas. Guardados sirve para organizar y recuperar elementos permanentes; Historial permite encontrar cálculos anteriores y también convertirlos en guardados.

Los temas de la barra lateral llevan símbolos propios (sistema A|b, vector, |A|, A⁻¹, L·U y propiedades). El icono de Matrices es una cuadrícula de nueve casillas en tres filas y tres columnas. Los símbolos respetan la paleta y la selección sin cambiar la distribución de las tarjetas.

## Historial y permanencia

**Historial** conserva los últimos cien cálculos válidos de todos los temas, con su procedimiento completo. No se registran pulsaciones, entradas inválidas ni cálculos fallidos. Para conservar uno sin que salga al superar el límite, selecciónalo y pulsa **Guardar del historial**. Esto crea una copia independiente con nombre, símbolo y notas propios.

Los guardados y el historial sobreviven al cierre. Windows utiliza `%LOCALAPPDATA%/CuadernoAlgebra/biblioteca.json`; en Linux se usa `$XDG_DATA_HOME/CuadernoAlgebra/biblioteca.json` o `~/.local/share/CuadernoAlgebra/biblioteca.json`. Son archivos del usuario, fuera del repositorio y sin sincronización con GitHub. No se envían a ningún servicio.

El JSON incluye versión de formato, identificadores, fechas UTC, números como cadenas exactas y fórmulas tipadas. La lista muestra fechas en Nicaragua (UTC−6). No se utiliza pickle ni se ejecuta código del archivo. La escritura termina en un archivo temporal y después sustituye el anterior. Si falla la lectura o se detecta una versión incompatible, se preserva el original y se bloquea su sobrescritura. Un fallo del historial no invalida el cálculo: se informa en el estado. Para respaldar datos, cerrar la calculadora y copiar este archivo personal; no incluirlo en commits o ZIP académicos sin revisar su contenido.

## Ejemplos por caso y ayudas

Desde **Guardar / Estudio → Ejemplos por caso** se cargan datos del método actual, sin cambiarlo ni calcular automáticamente. Hay casos de solución única, infinitas, inconsistencia, intercambio, independencia/dependencia, pertenencia, singularidad, triangularidad y LU que requiere PA=LU, según corresponda. La carga se puede deshacer.

**Ayudas de estudio** explica bajo demanda pivotes, variables libres, solución general, combinación, independencia, cofactores, singularidad, transpuesta, adjunta, LU y «No aplicable». Las explicaciones del recorrido breve no se alargan.

## Copiar y pegar matrices

Cada tarjeta editable añade **Copiar** y **Pegar**, sin cambiar su distribución. Copiar produce filas tabuladas con fracciones exactas. Pegar acepta:

```text
1/3  0.1
-2   4
```

También admite tabuladores de una hoja de cálculo, columnas separadas por comas, filas separadas por `;` y listas como `[[1/3,0.1],[-2,4]]`. Los decimales usan punto; la coma separa columnas. Primero se valida el bloque completo: un dato inválido, una fila irregular o un tamaño excesivo no modifica las casillas. Pegar constituye una edición deshacible y cancela cualquier recorrido anterior.

## Exportación PDF

Se puede exportar el ejercicio vigente desde el menú o cualquier instantánea de la biblioteca/historial desde **Exportar PDF**. El archivo contiene nombre, símbolo, notas, entradas, resultado y todos los pasos, paginados sin límite de cantidad. La ubicación y cualquier reemplazo de un archivo existente se eligen mediante el diálogo del usuario.

El exportador utiliza únicamente Python estándar; no incorpora bibliotecas matemáticas ni dependencias nuevas. Es un PDF A4 de texto monoespaciado, con fracciones `a/b` y notación equivalente `A^T`, `A^(-1)`, `->`, etc. No pretende reproducir las fracciones apiladas de la ventana ni sustituir el informe académico. Los caracteres personales fuera de la codificación del PDF se conservan como escapes Unicode legibles; en la biblioteca mantienen su símbolo original.

## Dónde cambiar cada parte

| Responsabilidad | Archivo |
|---|---|
| Esquema, nombres, símbolos, persistencia atómica e historial | interfaz/biblioteca.py |
| Captura y recuperación entre temas, menú de estudio y diálogos | interfaz/cuaderno.py |
| Lista, búsqueda, vista previa y desarrollo guardado | interfaz/guardados.py |
| Lectura de matrices pegadas y formato para copiar | interfaz/pegado.py |
| Casos conocidos y glosario breve | interfaz/ejemplos_casos.py |
| PDF completo y paginación | interfaz/exportar_pdf.py |

Para añadir otro método se amplía el catálogo habitual y, si corresponde, sus casos y etiqueta/símbolo de guardado. No duplicar algoritmos dentro de la biblioteca. El formato JSON tiene versión propia y no se cambia silenciosamente para añadir retornos nuevos.

## Verificación

Las pruebas usan memoria o directorios temporales, sin leer ni modificar datos personales o el portapapeles de la persona. Cubren reinicio, fracciones exactas, nombres y símbolos propios, duplicados, historial acotado, errores de escritura/lectura, recuperación entre temas, pegado deshacible, casos conocidos y PDF multipágina. Se comprueban los widgets mediante pruebas de código; no se usa Computer Use ni control de la pantalla, conforme a la instrucción vigente del usuario.

Antes de un futuro PR ejecutar la suite completa, el comprobador de reglas y `git diff --check`. La CI y la publicación siguen pendientes de autorización humana.

Comprobación local de esta etapa: suite general de 131 pruebas aprobada; comprobaciones finales específicas de la etiqueta de propiedades y recuperación de transpuestas aprobadas; reglas verificadas en 52 archivos Python y diff sin errores de espacios. Un PDF real de dos páginas se renderizó y verificó como documento. No se usó control de pantalla.
