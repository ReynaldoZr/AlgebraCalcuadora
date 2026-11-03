# Revisión del curso en UAM Virtual

Fecha de consulta: 3 de noviembre de 2026. Curso: MTM0120 — Álgebra Lineal — Grupo 5. Docente: José Andrés Munguía Cortez.

## Alcance y límites de la revisión

Se recorrieron las 16 pestañas semanales, las páginas de las seis tareas de programación y los dos foros generales. Se descargó la exportación de contenido del curso y, por separado, los seis enunciados adjuntos. Se extrajo el texto del sílabo, 12 planes semanales y 19 presentaciones para localizar temas y restricciones. Los seis enunciados de programación se leyeron completos; el plan 12 se leyó completo y se verificó visualmente su página 3.

Esta es una revisión de requisitos y cobertura, no una comprobación matemática de cada ejemplo de las diapositivas. Las fórmulas que son imágenes u objetos de Office pueden no aparecer completas en la extracción: al implementar un tema habrá que consultar visualmente sus páginas o diapositivas correspondientes.

Las semanas 13 a 16 tienen plantillas sin recursos publicados. El foro de consultas no contiene debates. Del foro de avisos se leyó el mensaje específico del proyecto. No se revisaron materiales de otras asignaturas ni se modificaron entregas.

## Requisitos confirmados

| Fuente | Requisito y consecuencias |
|---|---|
| [Aviso del 26 de agosto](https://uamvirtual.uam.edu.ni/grado/mod/forum/discuss.php?d=60638) | Aplicación de escritorio. La adaptación web solo se plantea como opción posterior a finalizar el proyecto. |
| [Tarea 1](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=965262) | Resolver Ax=b por eliminación, mostrar matriz aumentada y escalonamiento, clasificar solución única/infinitas/sin solución y comprobar resultados en el sistema original. Python estándar; prohibidos NumPy, SciPy y atajos de álgebra. |
| [Tarea 2](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=982676) | Gauss-Jordan/RREF; columnas pivote, variables básicas y libres; solución única o estructura de solución general. Mostrar también el caso inconsistente. |
| [Tarea 3](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=990114) | Suma/resta/escalar de vectores; combinación lineal; suma/resta/escalar/producto de matrices y Ax=b. Validar dimensiones. |
| [Tarea 4](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=1001328) | Independencia de k vectores de dimensión n a partir de Ax=0, reducción, pivotes y variables libres. Estructura modular, main.py, modulos/ y teoremas/. Menús de consola, cabeceras ASCII y opción 0 para teoremas. |
| [Tarea 5](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=1007311) | modulos/modulo_matrices.py importado desde main.py. Operaciones básicas y transpuesta; determinantes por cofactores, Sarrus en 3×3 y reducción; inversas por Gauss-Jordan y adjunta; comprobación A·A⁻¹=I; propiedades calculadas por ambos lados. |
| [Tarea 6](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=1014338) | modulos/modulo_lu.py: L m×m, U m×n, registrar multiplicadores, verificar LU=A. Resolver mediante Ly=b y Ux=y para matrices cuadradas. Reutilizar funciones existentes y transferir resultados como listas, sin pedir reingresar resultados intermedios. |
| Tareas 5 y 6 | Cálculo separado de interfaz, sin input/print en los módulos matemáticos. Docstrings por archivo y función, comentarios para explicar decisiones. Fraction permitido. |
| [Plan de la semana 12](https://uamvirtual.uam.edu.ni/grado/mod/resource/view.php?id=1031827), p. 3 | Orienta Tarea 7 de Métodos Numéricos. Permite NumPy y SciPy en esta unidad; bisección obligatoria y menú de errores. Defensa en semana 13, sin día concreto indicado en ese párrafo. |

## Política de dependencias por ámbito

1. **Álgebra de las tareas 1 a 6:** cálculos con listas, condiciones, bucles y funciones propias. Sin NumPy/SciPy, sin SymPy como sustituto de algoritmos y sin atajos de álgebra de otras bibliotecas. `Fraction` está expresamente permitido en las tareas 5 y 6.
2. **Métodos Numéricos:** el plan 12 permite NumPy/SciPy y pide contrastar la bisección con `scipy.optimize.bisect`. También menciona `numpy.finfo`, `numpy.float32`, comparaciones con `numpy.linalg.inv`/`cond` y gráficas opcionales con matplotlib.
3. **Separación propuesta:** los imports externos vivirán en la parte numérica y sus comparadores. Los módulos anteriores deben poder ejecutarse y probarse sin instalar esas bibliotecas.
4. **No confundir permisos:** el sílabo contempla herramientas adicionales en etapas posteriores; no es autorización para reemplazar hoy Gauss, determinantes o inversas de las tareas anteriores.

## Detalles fáciles de pasar por alto

- LU del programa 6 es **sin permutación**. Si continuar requiere intercambiar filas, debe detenerse y explicar que haría falta PA=LU. No añadir pivoteo silencioso y presentarlo como A=LU.
- El enunciado 6 mezcla en un punto de verificación de factorización la expresión Ax=b. El objetivo, la salida y las demás secciones permiten distinguir dos comprobaciones: LU=A para la factorización y Ax=b para la solución. Se documentará esa interpretación.
- Tarea 4 pide estructura por carpetas y después conserva un nombre de archivo único en el apartado de entrega. Las tareas 5 y 6 especifican claramente el proyecto completo. Para rehacer entregas antiguas se verificará el formato correspondiente; no fusionar archivos por suposición.
- Las primeras tareas pedían comentarios explicativos; desde la tarea 5 la guía indica comentarios con criterio y docstrings. Aplicaremos esta guía más reciente al código nuevo, conservando explicaciones extensas en documentación de estudio.
- El límite de unas 25 líneas por función es orientativo en la tarea 5, no una razón para fragmentar artificialmente un algoritmo.
- En el plan 12 hay distinta numeración de sesiones respecto a los nombres de los archivos publicados. Para localizar fuentes se usarán título y semana, además del número.
- El sílabo y el plan 12 no usan exactamente igual la numeración de los programas posteriores. Los hitos internos se vincularán a fuentes concretas, sin asumir que cada versión equivale a un número de tarea.

## Contenido por incorporar

| Semanas | Contenido publicado | Clasificación para el proyecto |
|---|---|---|
| 1–2 | Matrices, operaciones por filas, sistemas, REF/RREF y existencia/unicidad | Requisitos de tareas 1 y 2 |
| 3–5 | Ecuaciones vectoriales, combinación, Ax=b, independencia y aplicaciones | Tareas 3 y 4; aplicaciones según se necesiten |
| 6–8 | Producto, transpuesta, inversa, determinantes y LU | Tareas 5 y 6 |
| 9–11 | Espacios/subespacios, generadores, base, dimensión, transformaciones, rango y nulidad | Temario confirmado; definir alcance concreto con la próxima indicación de entrega |
| 12 | Errores, punto flotante y bisección | Tarea 7 orientada en el plan semanal |
| Posterior, en sílabo | Métodos abiertos como Newton-Raphson e integración final | Reserva futura; no presentarlo como tarea ya publicada |

## Verificadores requeridos

Se documentarán precondiciones, ambos miembros calculados y veredicto. Una propiedad no aplicable por dimensiones o singularidad se informará como no aplicable; no se fingirá una comprobación.

- Transpuesta doble; transpuesta de suma, de escalar y de producto.
- Distributividad A(B+C)=AB+AC y asociatividad (AB)C=A(BC).
- Inversa de inversa, de producto y de transpuesta; AA⁻¹=I.
- Determinante de transpuesta, de producto y de inversa; det(kA)=kⁿdet(A).
- Efecto de intercambio, reemplazo y escalado de filas; producto diagonal en triangular.
- Coincidencia de métodos de determinante y de inversa.
- LU=A y sustitución Ax=b con funciones reutilizadas.

## Entregables y defensa

Los enunciados piden ZIP con código e informe PDF. Los nombres exactos cambian por tarea. Los informes incluyen portada, explicación algorítmica breve y evidencias según cada programa. La modalidad es grupal, máximo cuatro personas, con defensa individual: ambos integrantes deben comprender el proyecto completo.

## Pendientes académicos

- Registrar el nuevo grupo y la modalidad de entrega que el profesor indique para el equipo de dos.
- Comprobar si aparece un enunciado específico de Tarea 7 que precise o cambie el plan 12.
- Revisar visualmente fórmulas y ejemplos al implementar cada tema.
- Verificar cualquier aclaración nueva sin asumir que cambia retroactivamente todas las reglas.
