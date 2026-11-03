# Cómo debe trabajar la IA hasta la revisión humana

La IA desarrolla y deja una propuesta comprobable. Reynaldo u otro humano autorizado revisa el pull request y decide si se integra, se corrige o se descarta. Una comprobación automática aprobada es evidencia técnica, no autorización humana.

## 1. Leer y definir la issue

Antes de editar, leer AGENTS.md, README.md y las guías relevantes. Revisar el estado real del código y de Git para conservar trabajo ajeno. Usar la issue indicada o crear una pequeña si el trabajo autorizado todavía no tiene una. Evitar duplicados.

La issue debe indicar objetivo, fuente de clase, módulos afectados, entradas, resultados esperados y criterios de aceptación. Si se propone una versión, dejar claro que todavía no está publicada. Un alcance nuevo se trata aparte.

## 2. Preparar una rama

Partir de main actualizado sin sobrescribir cambios locales. Crear una rama descriptiva vinculada al número de issue, por ejemplo `feat/2-producto-matrices`, `fix/8-validar-fracciones` o `docs/6-flujo-ia-revision-humana`. Si se continúa un PR existente, trabajar en su rama en vez de duplicarlo.

main representa lo integrado. La IA no hace commits directos allí, no fuerza su historial y no modifica las protecciones para eludir el PR.

## 3. Implementar y documentar

Hacer el cambio mínimo que satisfaga la issue, respetando la separación entre cálculo e interfaz, los contratos de datos y las restricciones de cada unidad. Reutilizar funciones. Añadir pruebas relevantes si cambia comportamiento y actualizar las guías afectadas.

Registrar los cambios en «Sin publicar» de CHANGELOG.md. No cambiar main.VERSION ni anunciar una versión como publicada para que una propuesta parezca terminada.

## 4. Comprobar antes de subir la rama

Desde la raíz ejecutar:

```text
python -m unittest discover -s tests -v
python herramientas/comprobar_reglas.py
git diff --check
```

Si cambia la interacción, probar también el recorrido de consola con datos válidos e inválidos. Revisar el diff, las dependencias, la documentación y los archivos que se incluirán; excluir credenciales y datos privados. No afirmar que una prueba se ejecutó si no se hizo.

Corregir los fallos relacionados con el cambio. Un problema que no pueda resolverse se explica con su causa y evidencia; no se oculta ni se desactiva la prueba para que todo parezca aprobado.

## 5. Abrir el pull request

Hacer commits comprensibles y publicar únicamente la rama de trabajo. Abrir el PR hacia main con la plantilla. Incluir `Closes #N`: es un vínculo que cerrará la issue al integrar, no una orden para que la IA la cierre ahora.

El PR debe explicar problema, comportamiento resultante, alcance, fuente de clase, comprobaciones ejecutadas, instrucciones para probar y limitaciones. Si la implementación está incompleta o bloqueada, mantenerlo como borrador. Si está lista y comprobada, puede quedar abierto para revisión.

## 6. Revisar las comprobaciones de GitHub

Consultar las cuatro combinaciones de CI: Windows/Linux con Python 3.11/3.13. Deben corresponder al último commit del PR. Si se añaden commits, las comprobaciones anteriores no prueban por sí solas el estado nuevo.

La IA puede reparar su rama, subir la corrección y comprobar de nuevo. No puede integrar, activar auto-merge, autoaprobarse, simular otra persona ni rebajar las reglas de protección. Si la CI no está disponible o falla por una causa externa, reportarlo y dejar el PR como borrador.

## 7. Entregar el PR y detenerse

La respuesta final debe incluir:

- Enlace de la issue y del PR abierto.
- Qué cambió y por qué.
- Cómo probarlo, con un ejemplo cuando corresponda.
- Resultado real de las pruebas locales y de la CI del último commit.
- Cualquier limitación o fallo pendiente.
- La indicación de que está pendiente de revisión humana.

El trabajo de desarrollo de la IA termina aquí. No hacer merge, cerrar la issue como completada, crear etiquetas ni publicar releases. El permiso de desarrollar o subir una rama no autoriza esos pasos.

## 8. Decisión humana

Reynaldo u otro humano autorizado abre el PR, revisa el diff y las comprobaciones y prueba el comportamiento relevante. Puede pedir cambios, rechazar la propuesta o decidir integrarla. Si pide cambios, la IA los prepara en la misma rama y devuelve el PR actualizado para otra revisión.

Integrar y publicar son decisiones distintas. Después de revisar, el humano puede integrar desde GitHub o dar una instrucción explícita de integración para ese PR. Las etiquetas y releases requieren también autorización expresa para la publicación correspondiente. Ante dudas sobre el alcance de esa autorización, mantener el PR abierto y pedir la aclaración concreta.

## Qué controla GitHub y qué controlan estas instrucciones

main tiene PR, rama actualizada, CI y conversaciones resueltas como requisitos; también bloquea force-push y borrado. Actualmente no exige una aprobación formal de otra cuenta, porque falta incorporar al segundo integrante. Eso no elimina la revisión humana de este flujo.

GitHub no distingue si una operación con la misma cuenta y credenciales la ejecutó una persona o una IA. Estas instrucciones fijan el límite de la IA; no se presenta la CI como una barrera de aprobación humana. Cuando haya dos cuentas colaboradoras, se podrá configurar una aprobación obligatoria de una cuenta distinta del autor. GitHub no permite que el autor apruebe su propio PR; véase la [documentación oficial sobre revisiones](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews).
