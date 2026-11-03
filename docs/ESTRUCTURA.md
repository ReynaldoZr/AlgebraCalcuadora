# Dónde va cada cosa

La primera etapa ya contiene main.py, modulos/validaciones.py, modulos/modulo_matrices.py, interfaz/, teoremas/resumen_teoremas.py, ejemplos/, tests/ y herramientas/comprobar_reglas.py.

La propuesta de UI añade gui.py como lanzador separado e interfaz/ventana.py, cuadricula.py y datos.py. Su flujo y límites se explican en [INTERFAZ_GRAFICA.md](INTERFAZ_GRAFICA.md); la consola y los contratos matemáticos siguen disponibles.

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

Ya implementado en v0.1.0: main.py; interfaz con entradas, formato, cabeceras y menús; modulos con validaciones y suma/resta; pruebas de cálculo, consola y reglas; README, AGENTS, CHANGELOG y plantillas de colaboración. LU y Métodos Numéricos se crearán cuando corresponda. La estructura completa es un mapa, no una obligación de fabricar archivos vacíos.
