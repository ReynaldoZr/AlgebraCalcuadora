# Preparación de Newton-Raphson

Estado al 18 de noviembre de 2026: #33–#35 están integradas y la propuesta de #36 conecta Newton al formulario, resumen y resultado guardable de Numéricos. El PR #39 había preparado adaptadores parciales. **Las mejoras específicas de #37 y #38 siguen pendientes**; esta conexión no significa terminar el Programa 9. Uso y pruebas en [NEWTON_FORMULARIO.md](NEWTON_FORMULARIO.md).

La fuente provisional es la Sesión 22, sobre Newton-Raphson, derivada numérica, convergencia y polinomios, y el Plan semanal 14 del [curso UAM](https://uamvirtual.uam.edu.ni/grado/course/view.php?id=8202&section=14). El plan aún contiene la rúbrica del Programa 8. No se ha confirmado el enunciado, rúbrica ni fecha del Programa 9; no extender permisos académicos a otros módulos.

## Responsabilidades y conexión pendiente

La propuesta de #33 incorpora `modulos/numericos/newton.py`, compatible con los adaptadores preparados. Contrato y tolerancia adicional en [NEWTON_NUCLEO.md](NEWTON_NUCLEO.md). Incorporar el núcleo no cierra las issues de conexión de Roberto.

- #33, Reynaldo: núcleo propio de Newton, contrato Calculo/Paso, validaciones y pruebas matemáticas.
- #34, Reynaldo: proveedores de derivada numérica, validación de h y pruebas de precisión.
- #35, Reynaldo: Horner, derivada y deflación con resto.
- #36, Roberto: formulario, resumen, catálogo, sesiones y reutilización del resultado.
- #37, Roberto: conectar vista previa, todos los pasos y tabla al recorrido existente.
- #38, Roberto: conectar figura y selección de iteraciones a Qt y validar casos reales.

El contrato propuesto está en la [issue #33](https://github.com/ReynaldoZr/AlgebraCalcuadora/issues/33). Los adaptadores se prueban con fixtures dentro de tests; nunca muestran resultados prefabricados en producción. Confirmar contrato y alcance antes de la conexión final.

## Archivos y uso para desarrollo

`interfaz/numericos/newton_adaptador.py` describe campos vacíos, ejemplos explícitos, validación y resumen. `ejecutar_newton_adaptador(parametros, solver=None, proveedor_derivada=None)` utiliza el núcleo y proveedor ya integrados, y conserva inyección para pruebas. Para derivada numérica exige h positivo, finito y distinguible de x0; el proveedor recibe `(funcion, h)` y devuelve una función de derivada. Validar todos los puntos de cada iteración corresponde al módulo numérico; la interfaz no implementa diferencias finitas ni otro bucle de Newton.

`newton_presentacion.py` consume pasos, filas y registros; no resuelve Newton. Falta conectar reproducción manual de 2 segundos, navegación y Mostrar tabla al recorrido existente.

`newton_graficas.py` construye una figura sin abrir ventanas. Usa registros para función, aproximaciones y tangente. Error/cambio y residuo tienen ejes separados; la tolerancia corresponde al error seleccionado, no al residuo. La comparación con cota absoluta de bisección requiere criterio absoluto y se identifica como magnitud distinta. El consumidor debe comprobar que ambas ejecuciones usan la misma función. Una muestra inválida interrumpe la curva; el muestreo no garantiza detectar todas las discontinuidades ni está validado para todos los valores extremos. Falta comprobar navegación, escalas y ejemplos reales al conectar #38.

## Aceptación antes de cerrar #36–#38

1. Confirmar enunciado y contrato con #33–#35.
2. Conectar módulos reales, catálogo y sesiones, sin imports rotos ni fixtures fuera de tests.
3. Probar función → cálculo → resumen → pasos/tabla → gráfica → guardar/reutilizar con el mismo resultado, sin perder entradas al navegar.
4. Comprobar raíz inicial, convergencia, ciclo, fallo de dominio, derivada nula, salto grande y máximo agotado, con causa real y residuo en la función original. Newton real con una semilla no promete todas las raíces ni raíces complejas.
5. Ejecutar pruebas completas y ambas CI de Windows; abrir PR para revisión humana. Los adaptadores aislados no reemplazan estas comprobaciones.
