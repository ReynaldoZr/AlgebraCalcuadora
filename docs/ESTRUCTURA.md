# Dónde va cada cosa

La semana 12 ya está implementada localmente en `modulos/numericos/` (funciones, bisección, errores y comparadores), `interfaz/panel_numerico.py`, `metodos_numericos.py`, `menu_numerico.py` e `interfaz/numericos/graficas.py`. Su guía es [SEMANA_12.md](SEMANA_12.md); para orientarse en IntelliJ consultar [GUIA_CODIGO.md](GUIA_CODIGO.md). No se importa la unidad desde los módulos exactos.

La biblioteca y las herramientas de estudio viven en `interfaz/biblioteca.py`, `cuaderno.py`, `guardados.py`, `pegado.py`, `ejemplos_casos.py` y `exportar_pdf.py`. El usuario autorizó Guardados como tercera pestaña; las dos vistas de cálculo y sus tarjetas se conservan. La persistencia nunca se importa en los módulos matemáticos. Consulte [GUARDADOS_Y_ESTUDIO.md](GUARDADOS_Y_ESTUDIO.md) antes de cambiar su esquema o ubicación; los datos personales no van al repositorio.

La ampliación actual de tareas 1 a 6 ya implementa eliminación, sistemas, vectores, determinantes, inversas, LU y verificadores. `modulos/procedimientos.py` define los resultados y pasos compartidos. `interfaz/operaciones.py` conecta los métodos con consola (`menu_algebra.py`) y escritorio (`panel_algebra.py` y `procedimiento.py`). Mantener las tres tarjetas y las dos vistas existentes; no introducir pestañas anidadas. Contratos completos en [ALGEBRA_TAREAS_1_A_6.md](ALGEBRA_TAREAS_1_A_6.md). `modulos/numericos/` continúa siendo solo una reserva futura.

La primera etapa ya contiene main.py, modulos/validaciones.py, modulos/modulo_matrices.py, interfaz/, teoremas/resumen_teoremas.py, ejemplos/, tests/ y herramientas/comprobar_reglas.py.

La propuesta de UI añade gui.py como lanzador separado e interfaz/ventana.py, cuadricula.py y datos.py. Su flujo y límites se explican en [INTERFAZ_GRAFICA.md](INTERFAZ_GRAFICA.md); la consola y los contratos matemáticos siguen disponibles.

La continuación local separa los colores en `interfaz/tema.py`, el dibujo de fracciones y matrices en `interfaz/notacion.py`, el desarrollo amplio en `interfaz/desarrollo.py` y el temporizador en `interfaz/recorrido.py`. La composición y el historial de sesión permanecen en `ventana.py`. Para cambiar el diseño, empezar por ese archivo específico, sin tocar los algoritmos.

Escalar (parte local de issue #2) usa los mismos archivos: `multiplicar_por_escalar(matriz, escalar)` en modulo_matrices.py, lectura y opción 4 en menus.py, texto en formato.py, tarjeta k y estado en ventana.py, equivalencias gráficas en desarrollo.py. No se añade otra estructura ni una matriz B artificial para una operación unaria.

Transpuesta usa `transponer_matriz(matriz)` en el mismo módulo matemático, opción 5 en menus.py y su formato de texto en formato.py. Su tarjeta de regla y el formulario se conectan en ventana.py; las etapas de traslado viven en explicacion.py. El origen y el destino tienen coordenadas diferentes y se documentan en INTERFAZ_GRAFICA.md. Los widgets compartidos se reutilizan.

El recorrido didáctico se amplía en `interfaz/explicacion.py`, sin widgets ni nuevos cálculos del resultado final. `interfaz/transicion.py` contiene únicamente el desvanecimiento entre vistas. La composición los conecta desde ventana.py: las instrucciones matemáticas no administran temporizadores o ventanas.

El árbol siguiente es la estructura objetivo a medida que avancemos; incluye archivos futuros. Solo se crearán carpetas y archivos cuando tengan una función real; los nombres de archivos de cálculo y teoremas indicados por el profesor se conservan.

```text
Calculadora_Algebra_Lineal/
├── main.py                       Arranque y menú principal
├── gui.py                        Arranque opcional de la ventana
├── modulos/                      Funciones matemáticas reutilizables
│   ├── __init__.py
│   ├── eliminacion.py            Operaciones de fila y reducción compartida
│   ├── modulo_sistemas.py        Gauss, Gauss-Jordan y clasificación
│   ├── modulo_vectores.py        Operaciones, combinación e independencia
│   ├── modulo_matrices.py        Operaciones, inversas y acceso al módulo III
│   ├── modulo_determinantes.py   Cofactores, Sarrus y reducción
│   ├── modulo_lu.py              Factorización y sustituciones
│   ├── validaciones.py           Dimensiones y precondiciones matemáticas
│   └── numericos/                Se crea al comenzar la nueva unidad
│       ├── __init__.py
│       ├── biseccion.py          Algoritmo e iteraciones
│       ├── errores.py            Errores y experimentos numéricos
│       ├── funciones.py          Lectura limitada de f(x) desde texto
│       └── comparadores.py       Contrastes con NumPy/SciPy permitidos
├── interfaz/                     Pedir, mostrar y navegar
│   ├── __init__.py
│   ├── menus.py                  Menús internos y opciones de teoremas
│   ├── entradas.py               Lectura y reintentos por datos incorrectos
│   ├── formato.py                Matrices alineadas, fracciones y pasos
│   ├── cabeceras.py              Identidad ASCII de los módulos
│   ├── datos.py                  Conversión numérica común a consola y GUI
│   ├── ventana.py                Composición y eventos de escritorio
│   ├── cuadricula.py             Editor de matriz y sus validaciones gráficas
│   └── memoria.py                Datos y resultados de la sesión
├── teoremas/
│   ├── __init__.py
│   ├── resumen_teoremas.py       Enunciados por módulo
│   └── verificadores.py          Calcula ambos lados con funciones existentes
├── ejemplos/                     Casos pequeños, entradas y respuestas revisadas
├── tests/                        Pruebas de resultados y errores importantes
├── docs/                         Guías, requisitos y decisiones
├── entregas/                     Informes y capturas organizados por entrega
├── .github/                      Plantillas de PR/tareas y comprobaciones
├── README.md                     Entrada para las personas
├── AGENTS.md                     Reglas de trabajo para IA
├── CHANGELOG.md                  Cambios publicados por versión
└── .gitignore                    Archivos locales excluidos del repositorio
```

## Regla para encontrar un cambio

| Quiero… | Lugar |
|---|---|
| Añadir una operación de matrices | modulos/modulo_matrices.py |
| Añadir un método de determinante | modulos/modulo_determinantes.py |
| Corregir reducción usada por varios temas | modulos/eliminacion.py y pruebas de sus consumidores |
| Cambiar cómo se piden números | interfaz/entradas.py |
| Cambiar la ventana o sus casillas | interfaz/ventana.py e interfaz/cuadricula.py |
| Cambiar colores o los temas claro/oscuro | interfaz/tema.py |
| Cambiar fracciones apiladas, matrices dibujadas o el icono | interfaz/notacion.py |
| Cambiar el desarrollo completo y su desplazamiento | interfaz/desarrollo.py |
| Cambiar reproducción y navegación de pasos | interfaz/recorrido.py |
| Cambiar etiquetas, etapas y explicación de una cuenta | interfaz/explicacion.py |
| Cambiar el desvanecimiento entre vistas | interfaz/transicion.py |
| Cambiar conversión numérica común | interfaz/datos.py |
| Cambiar cómo se ven matrices y fracciones | interfaz/formato.py |
| Añadir una opción a un menú | interfaz/menus.py; main.py solo si es un tema nuevo |
| Añadir un teorema | teoremas/resumen_teoremas.py |
| Comprobar una propiedad | teoremas/verificadores.py |
| Añadir un caso de práctica | ejemplos/ y su respuesta revisada |
| Añadir bisección o comparar con SciPy | modulos/numericos/ |
| Cambiar una regla común | docs/DECISIONES.md y AGENTS.md si afecta a la IA |

## Cómo se relacionan las partes

`main → interfaz → modulos` es el recorrido normal. La interfaz también consulta `teoremas`; los verificadores llaman a módulos matemáticos. El cálculo nunca importa la interfaz.

`eliminacion.py` y `validaciones.py` son piezas comunes. Sistemas, vectores e inversas reutilizan la misma reducción. Determinantes puede apoyarse en operaciones de fila comunes, sin importar modulo_matrices.py. Matrices puede importar determinantes. LU reutiliza el producto de matrices; matrices no importa LU. Esto evita dependencias circulares.

El menú de matrices ofrecerá también determinantes e inversas como exige la tarea 5, aunque sus implementaciones se repartan internamente. Una función se calcula en un solo lugar.

## Acuerdo sobre datos

- Matriz: lista de filas; cada fila es una lista del mismo tamaño. Ejemplo: `[[1, 2], [3, 4]]`.
- Vector: lista de componentes. Al usarlo como matriz columna se convierte explícitamente a `[[1], [2]]`.
- Las funciones de operaciones devuelven matrices/listas y escalares; no texto con números dibujados.
- Una operación no modifica la matriz original recibida. Se trabaja con una copia para conservarla y comprobar después.
- Se propone usar `Fraction` desde la entrada para las operaciones exactas. Para texto decimal, convertir el texto directamente a Fraction; no pasar antes por float.
- Los algoritmos con información adicional documentan su retorno antes de programarse: por ejemplo, matriz reducida, pivotes y pasos en una tupla. No cambiarlo sin actualizar sus llamadas y pruebas.
- Los pasos se guardan como datos independientes; no se usa print para producirlos dentro del algoritmo. La interfaz decide cuándo mostrarlos.
- Con decimales en el módulo numérico se registran tolerancia, criterio de paro, límite de iteraciones y motivo de terminación. No mezclar igualdad exacta y aproximada sin aclararlo.

## Alcance de la primera etapa

Publicado en v0.1.0: main.py, validaciones, suma/resta, consola y controles iniciales. Las ampliaciones locales posteriores incluyen las tareas 1 a 6, biblioteca y ahora semana 12. Las piezas futuras del árbol son un mapa, no una obligación de fabricar archivos vacíos.


## Navegación local aprobada

La propuesta combinada se implementa en `interfaz/inicio.py`: tarjetas por unidades y menú plegable. `interfaz/herramientas.py` agrupa acciones secundarias. Biblioteca sustituye el acceso permanente a la tercera pestaña; mantiene el mismo almacenamiento y las dos vistas de cada cálculo. La unidad numérica ya está implementada, como se explica en SEMANA_12.md; las menciones anteriores a reserva futura describen etapas previas.
