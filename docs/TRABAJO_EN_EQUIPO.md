# Trabajo entre dos y control del repositorio

## Reparto de la primera versión

| Persona A | Persona B | Ambos |
|---|---|---|
| Suma/resta, dimensiones y ejemplos matemáticos | Lectura de matrices, menús y formato | Acordar nombres y retornos, revisar PR y ensayar explicación |

Después se rotan responsabilidades. En la siguiente etapa A puede hacer entrada o teoremas y B producto matricial. El profesor exige defensa individual; el reparto facilita avanzar, pero los dos deben comprender todas las partes.

Las tareas fáciles tienen valor: preparar ejemplos y respuestas verificadas, redactar ayuda, ordenar evidencias, mejorar mensajes y comprobar dimensiones. Cada una debe dejar un resultado concreto. No asignar a una persona solo documentación durante todo el proyecto.

## Flujo propuesto

1. Abrir una tarea por cambio pequeño: «Producto rectangular con validación».
2. Partir de main actualizado y crear una rama descriptiva, por ejemplo feat/producto-matrices.
3. Trabajar y hacer commits que expliquen cambios concretos.
4. Ejecutar las pruebas del área y los consumidores afectados. Antes de integrar, comprobar el conjunto del proyecto y el recorrido de consola pertinente.
5. Abrir un pull request a main con problema, cambio y validación.
6. La otra persona revisa el cálculo, los límites del módulo, las restricciones y cómo se usa.
7. Integrar al pasar las comprobaciones. Publicar etiqueta cuando el hito esté listo.

Para dos personas no hace falta añadir una rama develop permanente. main representa el estado integrado; las ramas de trabajo duran lo necesario para su PR.

## Configuración y estado

- Repositorio público elegido por el usuario: ReynaldoZr/AlgebraCalcuadora. El segundo integrante todavía debe confirmarse.
- Plantillas de función, error y PR incluidas en .github/.
- main protegida: exige PR, rama actualizada, las cuatro comprobaciones de CI y conversaciones resueltas. Las reglas se aplican también al administrador; no se permiten force-push ni borrado de main.
- La aprobación formal obligatoria está en 0 hasta confirmar e incorporar la cuenta del segundo integrante. La revisión del compañero sigue siendo el acuerdo de trabajo; al incorporarlo se podrá exigir una aprobación.
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
