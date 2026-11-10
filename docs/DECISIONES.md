# Decisiones y pendientes

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
- Base: Python 3.11 o posterior; verificado localmente con Python 3.12.14. CI configurada para 3.11 y 3.13 en Windows y Linux; revisar sus resultados en el PR.
- Confirmar Python en la computadora del segundo integrante.
- Alcance del próximo avance y tiempo disponible para reconstruir lo anterior.

La primera implementación ya incluye suma/resta y ejemplos. Los datos del segundo integrante y grupo siguen pendientes de confirmar.

## Decisiones que pueden esperar

Empaquetado como ejecutable, guardado permanente del historial, exportación automática a PDF y gráficas. El núcleo independiente facilitará esas mejoras, pero no se incorporarán todas en la primera entrega.

## 2026-11-03 — Interfaz gráfica opcional

El usuario pidió incorporar una UI antes de continuar el siguiente bloque matemático. Se añade Tkinter/ttk de biblioteca estándar con un lanzador gui.py, conservando main.py y su consola por los requisitos académicos. Ambas interfaces utilizan las mismas funciones de cálculo, conversión exacta y presentación de pasos.

El primer editor gráfico se limita a 10x10 para mantener una cuadrícula manejable y desplazable. La restricción no se aplica al núcleo ni a la consola. Se documenta en INTERFAZ_GRAFICA.md y se probará en la issue #8 y su PR. No se cambia la versión publicada hasta la decisión humana.

## Cómo registrar cambios importantes

Cada decisión nueva incluye fecha, problema, solución elegida, archivos afectados y alternativa descartada solo si ayuda a entender el motivo. Si cambia una regla académica, añadir enlace y página de la indicación nueva. No borrar la historia de la regla anterior ni presentarla como si siempre hubiera sido igual.
