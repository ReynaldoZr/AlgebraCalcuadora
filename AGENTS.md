# Reglas de trabajo de la calculadora

## Introducción y límite de la IA

La IA prepara cambios para que una persona pueda revisarlos. Su recorrido es **issue → rama → implementación → comprobaciones → pull request → CI → revisión humana**. Leer [docs/FLUJO_IA.md](docs/FLUJO_IA.md) antes de empezar. La entrega de la IA es un PR abierto y comprobado; la decisión de integrarlo corresponde a Reynaldo u otro humano autorizado.

- Vincular el cambio a una issue y trabajar en una rama propia desde main actualizado. No escribir directamente en main.
- Ejecutar las comprobaciones, abrir el PR y revisar la CI del último commit. Si algo falla, corregir en esa misma rama y volver a comprobar. Si queda un bloqueo, informarlo y mantener el PR como borrador.
- Al terminar, entregar enlaces de issue y PR, resumen del cambio, instrucciones para probarlo, resultados de las comprobaciones y pendientes reales.
- **Detenerse antes de integrar:** no hacer merge, squash o rebase hacia main, no activar auto-merge ni entrar en una cola de integración, no autoaprobar el PR y no usar otra cuenta para aparentar una revisión humana.
- No cerrar la issue como completada, crear etiquetas, publicar releases, adelantar la versión publicada ni desactivar protecciones para terminar la tarea. Registrar la propuesta en «Sin publicar».
- Que las pruebas estén verdes o que se haya pedido «hacer la tarea», «subir los cambios» o «abrir el PR» no autoriza integrarlo. Para una actuación posterior de integración o publicación hace falta una instrucción humana explícita para ese PR, después de su revisión; no inferirla del permiso de desarrollar.
- No sustituir la revisión por una aprobación de la propia IA. Atender correcciones posteriores en la misma rama y dejar que el humano vuelva a decidir sobre el estado actualizado.

## Contexto y lectura inicial

Calculadora local de Álgebra Lineal para dos estudiantes, con funciones comprensibles y defensa individual. Primera implementación: v0.1.0, suma y resta de matrices. Leer README.md, docs/ESTRUCTURA.md y docs/COMO_AGREGAR.md; consultar docs/REVISION_UAM.md y docs/VERSIONES.md según la tarea. Revisar Git y preservar cambios ajenos antes de editar.

## Estructura

- main.py inicia; interfaz/ lee, muestra y navega; modulos/ calcula; teoremas/ contiene enunciados y futuros verificadores; tests/ comprueba comportamiento; docs/ explica decisiones.
- Mantener los nombres exigidos por UAM: main.py, modulos/, teoremas/, modulo_matrices.py y, cuando se implemente, modulo_lu.py. Mantener menús, cabeceras ASCII y opción 0 de teoremas.
- Añadir archivos solo cuando tengan funcionalidad real; el mapa futuro no representa código ya existente.
- Reutilizar funciones existentes. El cálculo no importa interfaz. Usar imports absolutos y evitar dependencias circulares.

## Reglas matemáticas

- Tareas 1–6: algoritmos propios con listas, bucles, condiciones y funciones. Sin NumPy/SciPy/SymPy ni sustitutos externos; sin atajos de math. Fraction está permitido expresamente en tareas 5 y 6.
- Excepción: plan semanal 12 permite NumPy/SciPy en Métodos Numéricos. Los imports externos de esa unidad vivirán en modulos/numericos/ y sus pruebas en tests/numericos/. No importarlos globalmente al iniciar la calculadora ni hacer que el álgebra anterior dependa de ellos.
- Cálculo sin input/print. Operaciones devuelven listas y valores reutilizables, no números dibujados en texto. Conservar entradas originales y evitar compartir filas mutables con los resultados.
- En esta etapa usar enteros/Fraction en el álgebra exacta. Convertir el texto decimal directamente a Fraction, sin pasar por float. La aproximación numérica tendrá contratos y tolerancias separados.
- Antes de cambiar nombres o retornos públicos, localizar consumidores y actualizar llamadas, documentación y pruebas afectadas.
- Los futuros verificadores calculan ambos lados con funciones existentes; no solicitan reingresar resultados intermedios. Validan precondiciones antes del veredicto.
- El futuro LU del Programa 6 es sin permutación. Si necesita intercambio de filas, detener y explicar que requiere PA=LU; no presentar el resultado como A=LU tras pivotear.

## Estilo y documentación

- Nombres descriptivos en español y funciones de una responsabilidad. Unas 25 líneas por función son una orientación, no un límite que justifique fragmentación artificial.
- Docstring inicial por archivo con propósito, tema y autoría confirmada; docstring breve por función con entradas y retorno. No inventar integrantes.
- Comentarios para explicar decisiones matemáticas o casos especiales. Explicaciones amplias en docs; no comentar cada línea ni conservar código viejo comentado.
- Cambios localizados: una operación nueva no autoriza reescribir toda la aplicación, incorporar un servidor o cambiar tecnologías. Separar refactorizaciones amplias y justificar el problema que resuelven.
- La nueva implementación debe ser comprendida por el equipo. No copiar código del equipo anterior para disfrazarlo mediante renombrado.

## Verificación y colaboración

- Ejecutar `python -m unittest discover -s tests -v` y `python herramientas/comprobar_reglas.py` antes del PR. Comprobar manualmente el recorrido de consola afectado cuando cambie la interacción.
- Añadir pruebas de resultados conocidos, límites matemáticos y errores relevantes; no pruebas que solo repitan la implementación.
- Cada mejora usa issue, rama y PR según docs/TRABAJO_EN_EQUIPO.md. El PR debe indicar alcance, fuente, validación y limitaciones. No inventar enlaces ni pruebas ejecutadas.
- Actualizar README/guías si cambia uso o estructura; registrar cambios bajo «Sin publicar» en CHANGELOG. La integración, el cierre definitivo de la issue y la publicación de versiones quedan sujetos a la decisión humana del flujo anterior.
- No subir contraseñas, sesiones, calificaciones, copias privadas de Moodle ni los entregables del grupo anterior. Referenciar fuentes por enlace.
- Si una indicación académica cambia, registrar fuente, fecha y ámbito en docs/DECISIONES.md. Un permiso de una unidad no se extiende a todo el repositorio.
- Al terminar, explicar qué cambió, por qué, cómo se verificó y cualquier pendiente concreto. AGENTS.md y las comprobaciones no sustituyen la revisión del compañero.
