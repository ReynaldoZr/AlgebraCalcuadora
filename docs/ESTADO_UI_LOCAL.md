# Propuesta de interfaz para revisión humana

El usuario pidió cerrar el PR #9 sin integrar y continuar la issue #8 localmente. Su código se conserva como base; la rama remota y la issue no se eliminaron.

Tras aprobar el diseño y probar la implementación local, el usuario autorizó subir esta propuesta como un nuevo pull request vinculado a la issue #8. La rama es `feat/8-interfaz-animada-local`. **La autorización cubre esta subida y las correcciones de sus comprobaciones; no autoriza integrar, activar auto-merge, autoaprobar, publicar etiquetas ni cambiar la versión publicada.** Dejar el PR abierto para revisión humana. El PR #9 permanece cerrado sin integrar. Las propuestas futuras siguen necesitando su autorización correspondiente.

## Diseño aprobado e implementado localmente

- Fondo azul oscuro, tarjetas azules, acentos lavanda y texto claro; sin acentos verdes.
- Tema Matrices con icono cuadrado de cuatro casillas. No se ofrecen temas futuros como si estuvieran implementados.
- Pestañas internas Calculadora y Todos los pasos. La segunda reduce la barra lateral y aprovecha el ancho para el desarrollo completo, con desplazamiento vertical.
- Matrices editables con fracciones apiladas: clic o Tab enfoca una entrada de texto real. El resultado es de solo lectura; no tiene controles de dimensiones.
- La vista previa conserva tres puntos clave y una igualdad. El desarrollo amplio incluye cada posición, equivalencias de denominador común y simplificación, y el resultado final.
- Reproducir/Pausar, Anterior, Siguiente y Reiniciar; intervalo fijo de 3000 ms, sin selector. No arranca automáticamente.
- Deshacer conserva hasta 50 estados de la sesión, incluidas entradas pendientes, carga, limpieza y último cálculo.
- Alternancia clara/oscura en la esquina superior derecha sin perder datos.
- Editar, cambiar operación, cargar o limpiar cancela temporizadores e invalida el recorrido. El desarrollo anterior se identifica hasta volver a calcular.
- Sin servidor web, dependencias nuevas ni modificaciones de los algoritmos, la consola o la versión publicada.

## Cómo comprobar

Ejecutar `python gui.py`, pulsar Cargar ejemplo y Calcular. Debe producir `[[1/2, 3/10], [3, 3]]`. Avanzar y retroceder; reproducir y pausar; abrir Todos los pasos y volver. Probar el tema claro y oscuro. Limpiar y deshacer para recuperar el cálculo. Editar durante la reproducción: el reloj se cancela y los pasos anteriores quedan marcados como desactualizados. Probar dimensiones 10×10 y el desplazamiento.

Verificación local realizada: 42 pruebas aprobadas, verificador de reglas aprobado en 25 archivos Python y `git diff --check` sin errores. Revisión visual en Windows: ejemplo exacto, navegación entre pestañas, desplazamiento hasta el resultado y alternancia clara/oscura. Las pruebas incluyen conservación de datos, deshacer, equivalencias de fracciones y controles visibles en el tamaño mínimo.

Consultar las comprobaciones del último commit en el nuevo PR; la CI del PR #9 no certifica esta propuesta. La revisión humana de código y uso sigue pendiente aunque todas las comprobaciones automáticas aprueben.
