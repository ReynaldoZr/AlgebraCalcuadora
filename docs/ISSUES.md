# Primeras tareas del repositorio

## Tarea local: migración a PySide6 + QML

Autorizada el 6 de noviembre para el próximo avance, en `feat/qt-qml-local`. Objetivo: sustituir la presentación principal conservando la consola, cálculos, entradas vacías, Biblioteca, todos los pasos y ritmo de dos segundos. Criterios: los métodos existentes calculan, QML carga sin errores, las fracciones siguen exactas, la recuperación no duplica historial y Tk permanece como respaldo. Alcance, archivos y comprobaciones en [MIGRACION_QT.md](MIGRACION_QT.md). Issue remota y PR pendientes de autorización; no se inventa número.

La continuación local actual es `feat/semana-12-numericos`: el alcance matemático y sus criterios se registran en [SEMANA_12.md](SEMANA_12.md). La semana 12 fue autorizada el 4 de noviembre; sus estados anteriores «fuera de alcance» quedan superados. No se inventa una issue remota, se publica la rama ni se abre PR mientras el usuario no lo autorice.

La rama actual `feat/guardados-y-practica-local` continúa los cambios matemáticos y prepara la tarea local de biblioteca y estudio: persistencia exacta, nombres/símbolos, historial, recuperación, PDF, casos y pegado. Sus criterios y comprobaciones están en [GUARDADOS_Y_ESTUDIO.md](GUARDADOS_Y_ESTUDIO.md). La issue remota y el PR correspondientes se prepararán cuando el usuario autorice subir; no se inventa un número ni se publica ahora.

La ampliación local `feat/3-algebra-tareas-1-a-6` reúne los cálculos de #2, #3 y #4 y los siguientes bloques: vectores, determinantes, inversas, LU y verificadores. Para esos bloques posteriores se prepararán issues revisables al autorizar el trabajo remoto; no se inventan números ni enlaces. No se cerraron issues, no se abrió un PR y no se publicó la rama. Alcance y comprobaciones en [ALGEBRA_TAREAS_1_A_6.md](ALGEBRA_TAREAS_1_A_6.md). Métodos Numéricos de semana 12 no se incluye.

| Versión | Issue | Alcance |
|---|---|---|
| v0.1.0 | [#1](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/1) | Base, suma/resta, documentación y controles |
| v0.2.0 | [#2](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/2) | Escalar, producto y transpuesta |
| v0.3.0 | [#3](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/3) | Gauss, clasificación y comprobación |
| v0.4.0 | [#4](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/4) | Gauss-Jordan, pivotes y solución general |
| UI integrada, sin release nueva | [#8](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/8) | Cerrada al integrar PR #10: ventana de escritorio, conservando consola |

Las issues son tareas de trabajo; una fila no significa que la función ya esté implementada. Cada issue incluye criterios de aceptación. Las correcciones se registran con la plantilla de errores y se vinculan a un PR. Una etiqueta como v0.1.1 se publica solo cuando la corrección se integra y verifica.

La issue #2 reúne escalar, transpuesta y producto matricial, preparados en la rama local con consola e interfaz. Su cierre y la publicación de v0.2.0 siguen pendientes de revisión y decisión humana. La autorización anterior del PR #10 no autoriza subir esta nueva propuesta.

Los siguientes temas del curso están en VERSIONES.md y se convertirán en issues pequeñas cuando se acerque su implementación. El responsable y el revisor se acuerdan entre ambos integrantes; no se asignan a una cuenta que todavía no está confirmada.


## Tarea local: inicio por unidades y navegación compacta

Rama `feat/inicio-temas-local`; continúa sin descartar los cambios locales anteriores. Objetivo: implementar el boceto combinado aprobado por Reynaldo. Criterios: inicio con todos los temas actuales, menú plegable, conservación de sesiones, Biblioteca desde cualquier vista, acciones compactas y todos los pasos intactos. Fuente: autorización de diseño del usuario del 4 de noviembre de 2026; se conservan las restricciones académicas existentes. Alcance y pruebas en INICIO_Y_NAVEGACION.md. No tiene todavía número de issue remota: no se crean issues ni PR hasta nueva autorización.
