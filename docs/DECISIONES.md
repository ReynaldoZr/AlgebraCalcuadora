# Decisiones y pendientes

## 2026-11-21 · Versión 0.9 y cierre del alcance gráfico

Reynaldo decidió no realizar las interacciones que seguían pendientes de #23–#30.
Las ocho issues se cierran como no planificadas, no como funciones implementadas.
El avance ya integrado se identifica como v0.9.0 (versión 0.9) en consola y en
el título de Qt. Se conservan las funciones existentes, los datos personales y
la configuración de IntelliJ. La denominación no crea una etiqueta ni una
release pública adicional; esas publicaciones siguen requiriendo autorización.

## 2026-11-21 · Revisión del PR 46 y aprobación de tema oscuro

Reynaldo pidió revisar los PR pendientes e integrar lo que funcione y cumpla las
reglas. Aprobó expresamente «Aceptar el nuevo negro/morado» del PR #46 de Roberto.
La aprobación sustituye únicamente el tema oscuro de Qt/gráficas; conserva claro,
tarjetas, navegación y restricciones matemáticas. No cambia el flujo habitual de
revisión de futuros trabajos ni permite aparentar una aprobación de otra persona.

La revisión conserva el PR existente y la infraestructura compartida de las
gráficas. Se corrigen regresiones de presentación, precisión, parada de Newton,
zoom logarítmico y tablas extensas sin modificar los algoritmos del profesor.
Se documenta el alcance real en GRAFICAS_INTERACTIVAS.md: #23–#30 permanecen
abiertas porque aún faltan interacciones de sus criterios de aceptación. El
enunciado definitivo del Programa 9 sigue pendiente de confirmación.

## 2026-11-18 · Núcleo Newton y residuo independiente

Reynaldo autoriza avanzar sus issues en orden, empezando por #33, con pruebas y PR. La Sesión 22 pide comprobar la raíz en la función original y limitar iteraciones; el enunciado del Programa 9 sigue pendiente. El equipo añade `tolerancia_f=1e-8` configurable e independiente del cambio absoluto/porcentual para evitar falso éxito por estancamiento. Es una protección provisional, no una cifra exigida por el profesor; puede alterar el conteo de clase y depende de la escala de la función. No cambia bisección ni las restricciones del álgebra exacta. Contrato y límites en [NEWTON_NUCLEO.md](NEWTON_NUCLEO.md).

## 2026-11-06 — Migración autorizada a Qt Quick

Después de comparar propuestas de CustomTkinter, PySide6/QML, Flet y web, el usuario eligió PySide6 + QML y autorizó implementarlo para el avance de la próxima semana. La interfaz nueva se mantiene separada del núcleo y conserva las restricciones académicas, consola, estructura y Biblioteca. La interfaz Tk continúa disponible durante la revisión; gui.py abre Qt y gui_tk.py permite comparar. La autorización no permite subir la rama, abrir PR ni publicar versiones. Alcance y contratos en MIGRACION_QT.md. No se afirma una autorización académica expresa de PySide6 ausente de los documentos revisados.

## 2026-11-04 — Semana 12 y trabajo en IntelliJ

El usuario autorizó implementar todo el alcance conocido del plan semanal 12, incluidas recomendaciones y gráficas, y confirmó el permiso para NumPy/SciPy. Se conserva el álgebra exacta y se aísla la unidad aproximada en modulos/numericos; Matplotlib/Tk tiene un adaptador en interfaz/numericos. Fuente: plan 12, página 3; véase SEMANA_12.md. No se infiere permiso para SymPy ni para reemplazar las tareas anteriores con bibliotecas.

Se eligió .venv del proyecto para dependencias y la configuración de ejecución de IntelliJ «Calculadora escritorio». Se pidieron comentarios breves para orientarse; se conservan docstrings y se añaden notas de decisiones, con un mapa de archivos en GUIA_CODIGO.md. El usuario prefiere PySide6 con Qt Quick/QML para una evolución futura; hoy continúa Tkinter. No se autoriza publicación ni control de pantalla por esta instrucción.

## Decisiones de la primera etapa

| Decisión | Motivo | Estado |
|---|---|---|
| Python local con consola | Aviso de escritorio y directriz CLI de tarea 4 | Requisito confirmado |
| main.py + modulos/ + teoremas/ | Estructura exigida desde tarea 4 | Requisito confirmado |
| Cálculos sin input/print | Reutilización y encadenamiento exigidos en tareas 5 y 6 | Requisito confirmado |
| Interfaz en carpeta independiente | Facilita encontrar navegación, entradas y formato | Adoptada en v0.1.0 |
| Fraction para álgebra exacta | Permitido expresamente; evita redondear las comprobaciones | Adoptada en v0.1.0 |
| Bibliotecas externas limitadas a Métodos Numéricos | Plan 12 cambia permisos por unidad | Requisito confirmado y separación propuesta |
| Pruebas con unittest de biblioteca estándar | Permite empezar sin dependencias de pruebas | Adoptada en v0.1.0 |
| Funciones claras antes que clases y capas adicionales | Aprendizaje y defensa individual | Adoptada en v0.1.0 |
| Navegación guiada y ejemplos propios | Identidad nueva y facilidad de uso | Adoptada en v0.1.0 |

## Identidad propia

Se pueden elegir nombre, cabecera principal, vocabulario de ayuda y disposición de resultados propios, respetando las cabeceras requeridas para los módulos. Propuestas de nombre provisionales: «Cuaderno Lineal», «Álgebra por Pasos» o «Vector y Matriz».

La diferencia debe verse también en el código y la experiencia: tareas pequeñas, nombres claros, formularios de consola, comprobación final y ejemplos que ambos sepan explicar. No se promete originalidad solo por cambiar colores o nombres. Los algoritmos matemáticos y las carpetas obligatorias naturalmente coincidirán con otros proyectos del curso.

## Datos del proyecto y pendientes

- Repositorio elegido: https://github.com/ReynaldoZr/AlgebraCalcuadora.
- Identidad de pantalla provisional: Cuaderno de Álgebra Lineal.
- Identidad del segundo integrante y grupo académico confirmado.
- Base: Python 3.11 o posterior; verificado localmente con Python 3.12.14. CI actual configurada para 3.11 y 3.13 únicamente en Windows; revisar sus resultados en el PR.
- Confirmar Python en la computadora del segundo integrante.
- Alcance del próximo avance y tiempo disponible para reconstruir lo anterior.

Integrantes confirmados: Reynaldo y Roberto (@roberto7503), Grupo 9. El estado de las funcionalidades y entregas se consulta en CHANGELOG.md y en las issues del repositorio.

## Decisiones que pueden esperar

Empaquetado como ejecutable, guardado permanente del historial, exportación automática a PDF y gráficas. El núcleo independiente facilitará esas mejoras, pero no se incorporarán todas en la primera entrega.

## 2026-11-03 — Interfaz gráfica opcional

El usuario pidió incorporar una UI antes de continuar el siguiente bloque matemático. Se añade Tkinter/ttk de biblioteca estándar con un lanzador gui.py, conservando main.py y su consola por los requisitos académicos. Ambas interfaces utilizan las mismas funciones de cálculo, conversión exacta y presentación de pasos.

El primer editor gráfico se limita a 10x10 para mantener una cuadrícula manejable y desplazable. La restricción no se aplica al núcleo ni a la consola. Se documenta en INTERFAZ_GRAFICA.md y se probará en la issue #8 y su PR. No se cambia la versión publicada hasta la decisión humana.

## Cómo registrar cambios importantes

Cada decisión nueva incluye fecha, problema, solución elegida, archivos afectados y alternativa descartada solo si ayuda a entender el motivo. Si cambia una regla académica, añadir enlace y página de la indicación nueva. No borrar la historia de la regla anterior ni presentarla como si siempre hubiera sido igual.

## 2026-11-15 · Núcleo de Jacobi para Programa 8

La issue #14 implementa Jacobi con ciclos propios, aritmética aproximada y
validaciones compartidas en modulos/numericos/iterativos.py. El
[plan semanal 13](https://uamvirtual.uam.edu.ni/grado/mod/resource/view.php?id=1037473),
apartados 8 a 13, orienta Jacobi y Gauss-Seidel y permite NumPy/SciPy para
esta unidad. El criterio de esta etapa es la diferencia máxima absoluta entre
vectores consecutivos, estrictamente menor que la tolerancia. La interfaz
comparativa se prepara en #16. Contrato y ejemplos en docs/JACOBI.md.

### Ajuste al enunciado definitivo del 15 de noviembre

La [Tarea 8](https://uamvirtual.uam.edu.ni/grado/mod/assign/view.php?id=1043170),
apartados 2, 3.2 y 3.3, amplía las bibliotecas permitidas en la unidad numérica
a Pandas y SymPy, exige el residuo final y una advertencia si crece el error,
y recomienda parada por diferencia máxima menor o igual que la tolerancia.
Se adopta ese criterio inclusivo para Jacobi y el contrato de Gauss-Seidel.
Se actualizan el verificador, las pruebas y la guía del módulo para reflejar
el nuevo ámbito. El permiso no se extiende al álgebra exacta de tareas anteriores.

## 2026-11-15 · Revisión de Gauss-Seidel y comparación, PR #20

Reynaldo autorizó corregir los problemas detectados en el PR de Roberto y
después integrarlo cuando pasaran las comprobaciones. También aprobó su paleta
verde salvia/crema en claro y azul profundo en oscuro, conservando la estructura
de la interfaz. Esta excepción de integración corresponde únicamente al PR #20.

El reordenamiento original tardó unos 63 segundos en una matriz densa 9×9 sin
dominancia. Se usa la asignación por caminos aumentantes para todos los tamaños,
priorizando dominancia y evitando enumerar permutaciones. No se promete hallar
la mejor dominancia parcial. Se conserva A y b para validar el resultado.

La opción de reordenar también se ofrece en Jacobi. Los resúmenes del comparador
muestran la causa de parada individual, incluida la interrupción por valores no
finitos. Con relajación distinta de 1 se advierte que dominancia y `0 < λ < 2`
no garantizan convergencia para cualquier matriz. La comparación habitual usa
λ=1 y conserva el criterio de error del enunciado definitivo.

## 2026-11-15 · Soporte Windows y cierre del Programa 8

Reynaldo indicó que las comprobaciones futuras deben ejecutarse únicamente en
Windows. La CI conserva Python 3.11 y 3.13, el verificador y las pruebas completas
de cálculo, consola, Tk y Qt. Se retiran los trabajos de otras plataformas y se
actualizan los controles requeridos de main a las dos comprobaciones de Windows,
manteniendo el PR obligatorio, la rama actualizada y el resto de protecciones.
Las evidencias históricas de CI reflejan su configuración de aquel momento.

Reynaldo confirma que el PDF y los demás materiales de la entrega ya están
listos y autoriza cerrar el seguimiento #16. El cierre documental se basa en su
confirmación; la validación de código corresponde al PR #20. También autoriza
publicar e integrar este ajuste de CI y documentación después de comprobarlo.
