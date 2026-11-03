# Historial de cambios

## Sin publicar

- Diseño local aprobado: fondo azul oscuro, acentos lavanda, icono cuadrado de Matrices, fracciones apiladas y alternativa clara. Vista previa breve y pestaña amplia con todo el desarrollo, desplazamiento y aviso de cálculo anterior.
- Recorrido con Anterior, Reproducir/Pausar, Siguiente y Reiniciar, intervalo fijo de tres segundos sin selector y cancelación al editar. Deshacer conserva hasta 50 estados locales, incluidos limpieza y último cálculo.
- PR #9 cerrado sin integrar; el usuario autorizó subir la nueva propuesta como PR abierto para revisión humana. No se cambia la versión publicada ni se incorpora un servidor web; integración y publicación siguen pendientes de decisión humana.
- Interfaz gráfica opcional con Tkinter/ttk: matrices editables de hasta 10x10, suma/resta, procedimiento y teoremas, ejemplo y reutilización de resultados.
- Lectura numérica y presentación compartidas entre consola y ventana; se conservan los algoritmos y la versión publicados.
- Pruebas con widgets reales y pantalla virtual para la CI de Linux; la falta de pantalla/Tk no puede omitir silenciosamente las pruebas gráficas en CI.
- Instrucciones de IA y colaboración: issue, rama, comprobaciones y PR abierto; integración y publicación reservadas a decisión humana. Guía paso a paso y plantilla de PR actualizadas.

## v0.1.0 — 2026-11-03

- Menú de consola y módulo de matrices con cabecera ASCII y opción 0 de teoremas.
- Entrada validada de matrices rectangulares, enteros, fracciones y decimales exactos.
- Suma y resta mediante funciones propias; procedimiento por posición.
- Reutilización del último resultado mientras la aplicación permanece abierta.
- Ejemplos, pruebas matemáticas y recorridos de consola.
- Comprobaciones de estructura, plantillas de issue y PR y flujo de integración continua.
- Guías de organización, restricciones por unidad y ampliación progresiva.

Primera entrega funcional. Publicación identificada por la etiqueta v0.1.0; integración mediante PR #5. Las siguientes correcciones compatibles usarán v0.1.1, v0.1.2, etc.
