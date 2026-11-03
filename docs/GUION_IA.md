# Guion para trabajar con una IA

Este texto se puede copiar al iniciar una tarea. Se reemplaza la línea del objetivo por una operación concreta. AGENTS.md debe ubicarse en la raíz del repositorio definitivo; en otras herramientas se adjunta o se pide expresamente su lectura. El README orienta a las personas; AGENTS.md resume reglas para el agente.

```text
Estamos desarrollando entre dos estudiantes una calculadora local de Álgebra Lineal en Python.

Objetivo de esta tarea: [operación concreta y ejemplo esperado].

Antes de modificar archivos, lee AGENTS.md, README.md y las secciones relevantes de docs/REVISION_UAM.md, docs/ESTRUCTURA.md y docs/COMO_AGREGAR.md. Comprueba el estado real del código y de Git; no supongas que las funciones del plan ya existen.

Localiza la operación en el módulo correspondiente y reutiliza las funciones existentes. Conserva las entradas y los retornos públicos salvo que el objetivo requiera cambiarlos; en ese caso explica y actualiza sus consumidores.

Los módulos algebraicos de tareas 1–6 usan algoritmos propios en Python estándar. El permiso de NumPy/SciPy del plan 12 se limita al ámbito de Métodos Numéricos y no reemplaza los cálculos anteriores.

Separa cálculo de interfaz. Las funciones de cálculo reciben datos y devuelven resultados reutilizables; no usan input ni print. Conserva las matrices originales para las comprobaciones.

Haz el cambio más pequeño que resuelva el objetivo, con nombres claros y docstrings breves. Explica las decisiones matemáticas necesarias. No reestructures todo el programa ni añadas servidores o dependencias ajenas al alcance.

Comprueba casos correctos e inválidos relevantes. Actualiza la documentación que cambie y resume qué se hizo, por qué, cómo se verificó y qué falta. Si una regla académica resulta ambigua, señala la fuente concreta y sigue avanzando en las partes independientes.

No inventes autores, calificaciones, evidencias, resultados de pruebas, enlaces de PR ni funciones terminadas. No incluyas credenciales o datos privados de UAM en archivos o commits.
```

## Cómo evitar instrucciones demasiado largas

Mantener las reglas esenciales en AGENTS.md y los detalles en las guías enlazadas. Cuando una regla cambie, actualizar su fuente y los documentos que la referencian. Pedir a la IA que resuma qué reglas aplican al módulo antes de una tarea importante permite detectar malentendidos.

AGENTS.md es una guía reconocida por Codex, no una garantía de que cualquier IA cumpla todo. La revisión del compañero y las comprobaciones automáticas siguen siendo necesarias. Referencia: [documentación oficial de instrucciones de proyecto](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
