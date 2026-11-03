# Trabajo entre dos y control del repositorio

## Reparto de la primera versión

| Persona A | Persona B | Ambos |
|---|---|---|
| Suma/resta, dimensiones y ejemplos matemáticos | Lectura de matrices, menús y formato | Acordar nombres y retornos, revisar PR y ensayar explicación |

Después se rotan responsabilidades. En la siguiente etapa A puede hacer entrada o teoremas y B producto matricial. El profesor exige defensa individual; el reparto facilita avanzar, pero los dos deben comprender todas las partes.

Las tareas fáciles tienen valor: preparar ejemplos y respuestas verificadas, redactar ayuda, ordenar evidencias, mejorar mensajes y comprobar dimensiones. Cada una debe dejar un resultado concreto. No asignar a una persona solo documentación durante todo el proyecto.

## Flujo obligatorio de trabajo y revisión

1. Crear o tomar una issue pequeña con criterios de aceptación.
2. Partir de main actualizado y crear una rama descriptiva con el número de issue, por ejemplo feat/2-producto-matrices.
3. Implementar, documentar y hacer commits que expliquen cambios concretos.
4. Ejecutar pruebas, comprobador de reglas y revisión del diff; probar la consola si cambia la interacción.
5. Publicar la rama y abrir un pull request a main, vinculado a la issue y con instrucciones de prueba.
6. Comprobar la CI del último commit y corregir fallos en esa misma rama. Si hay un bloqueo, dejar el PR como borrador y explicarlo.
7. **La IA entrega el PR abierto y se detiene.** No integra, autoaprueba, activa auto-merge, cierra la issue como completada ni publica versiones.
8. Reynaldo u otro humano autorizado revisa, prueba y decide si pide cambios, descarta o integra. Las pruebas aprobadas no sustituyen su decisión.
9. Solo tras la decisión humana se integra. El cierre de la issue y la publicación de etiqueta/release corresponden al resultado autorizado; publicar necesita autorización expresa.

El procedimiento completo, incluidos los límites de la IA, está en [FLUJO_IA.md](FLUJO_IA.md). Una petición general de desarrollar, subir cambios o abrir un PR no autoriza a la IA a integrarlo.

Para dos personas no hace falta añadir una rama develop permanente. main representa el estado integrado; las ramas de trabajo duran lo necesario para su PR.

## Configuración y estado

- Repositorio público elegido por el usuario: ReynaldoZr/AlgebraCalcuadora. El segundo integrante todavía debe confirmarse.
- Plantillas de función, error y PR incluidas en .github/.
- main protegida: exige PR, rama actualizada, las cuatro comprobaciones de CI y conversaciones resueltas. Las reglas se aplican también al administrador; no se permiten force-push ni borrado de main.
- La aprobación formal obligatoria está en 0 hasta confirmar e incorporar la cuenta del segundo integrante. La revisión humana de Reynaldo u otro humano autorizado sigue siendo obligatoria en el flujo de trabajo. Al incorporar otra cuenta se podrá exigir su aprobación formal; el autor no puede aprobar su propio PR.
- CI incluida para pruebas y reglas de imports/docstrings en Windows y Linux. Consultar el resultado real de cada ejecución en GitHub.
- No subir credenciales, sesiones, copias de Moodle, entornos virtuales ni datos académicos personales. El repositorio contiene código propio, guías y referencias a las fuentes.
- Elegir una versión de Python y usarla en ambos equipos y en las comprobaciones.

El repositorio ya existe. Las plantillas y el flujo de comprobaciones acompañan la primera implementación. La protección de main está configurada con los controles anteriores. Falta confirmar e incorporar al segundo integrante para exigir su aprobación formal.

## Automatización que conviene añadir

herramientas/comprobar_reglas.py analiza el AST de Python: comprueba docstrings, imports externos según ámbito, aliases básicos, input/print y dependencias de interfaz desde cálculo. Sus límites se revisan con pruebas. No realiza un análisis completo de todas las dependencias transitivas o comportamientos dinámicos; la revisión del PR debe comprobar también esos aspectos.

Los controles automáticos ayudan a mantener reglas concretas. No garantizan corrección matemática ni sustituyen la revisión humana o la comprensión del código.

## Modelo de tarea

```text
Objetivo:
Fuente de clase / requisito:
Módulo que se modificará:
Nombre, entradas y retorno de la función:
Ejemplo con respuesta esperada:
Datos inválidos que debe manejar:
Qué debe funcionar para cerrar la tarea:
Responsable y revisor:
```

## Modelo de pull request

```text
Problema y comportamiento nuevo:
Requisito de clase que satisface:
Cómo se comprobó (casos y resultado):
Cambios en retornos, dependencias o estructura:
Limitaciones conocidas:
Tarea relacionada:
```

## Entregas

Guardar informe y capturas por número de entrega. Crear el ZIP desde una etiqueta conocida; registrar etiqueta y commit en la guía de entrega. El número y los nombres del grupo se toman de los datos confirmados del nuevo equipo, nunca de los archivos del grupo anterior.
