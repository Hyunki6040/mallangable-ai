<!-- LANG-BAR -->
[English](../../en/research/harness2-analysis.md) · [한국어](../../ko/research/harness2-analysis.md) · [简体中文](../../zh-CN/research/harness2-analysis.md) · [日本語](../../ja/research/harness2-analysis.md) · **Español**
<!-- /LANG-BAR -->

# Nota de investigación — Harness² (google-research/harness2)

> Conclusión de esta nota: Harness² es **un marco de investigación que reescribe el propio harness para cada tarea**. El harness de Mallangable (5.6) es una envoltura que rodea al agente para *imponer* reglas, así que la dirección es distinta. Hay tres cosas que tomar casi tal cual. Primera, **un mecanismo de aislamiento que impide que la información de puntuación entre jamás en el contexto del lado del método (method)**. Segunda, **una regla de informe que trata un fallo de puntuación no como 0 puntos sino como sin puntuar (unscored)**. Tercera, **un juicio que oculta el origen del candidato**. Las tres refuerzan Mallang-Bench (10.2) y G4 (5.8). En cambio, no aceptamos la autoedición en la que el agente modifica incluso los hooks de política y las barreras de protección (guardrails).

- Fecha de verificación: 2026-10-30
- Objeto de estudio: https://github.com/google-research/harness2 (repositorio público, existencia verificada)
- Commit fijado: `1cfe254e8d25b15f37048c3730134686abe60335` (2026-10-13). Todos los enlaces a código fuente de abajo se refieren a este commit.
- Método: se descargó con `git clone --depth 1` en un directorio temporal vacío y **solo se leyó** (sin ejecutar código). El artículo se leyó obteniendo de la web la página de resumen de arXiv y el cuerpo en HTML.
- Notación: `B` = `https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335`

## 0. Qué se verificó y qué no

| Elemento | Estado | Fundamento |
| --- | --- | --- |
| Existencia del repositorio y si es público | Verificado | `gh repo view google-research/harness2`, clonado con éxito |
| Licencia | Verificado | [`LICENSE`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/LICENSE) Apache 2.0, [`pyproject.toml`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/pyproject.toml#L9) `license = "Apache-2.0"` |
| Código fuente principal (`harness2/core/*`, `substrate/*`) | Leído directamente | Enlaces en el texto |
| Artículo | Existencia y resumen verificados, parte del cuerpo verificada | [arXiv:2610.14224](https://arxiv.org/abs/2610.14224), enviado el 2026-10-09. El cuerpo HTML se leyó con una herramienta de resumen, así que **los números de sección y las citas deben cotejarse de nuevo con el PDF original** |
| Sitio del proyecto | Existencia verificada | https://harness2.github.io (enlazado desde el README) |
| Artículo en el blog de Google Research | **No encontrado** | No hay enlace a un blog ni en el sitio, ni en el README, ni en el artículo |
| Reproducción de las cifras experimentales | No realizada | Las llamadas al modelo tienen coste y quedan fuera del alcance de la investigación |
| Texto completo de `prompts.py` (1,163 líneas) | Leído solo en parte | Solo se verificaron las instrucciones de aislamiento y las secciones INV/DOM |
| Adaptadores de benchmark (`benchmarks/*.py`) | No leídos | Código de conexión ajeno a la metodología |

## 1. Qué es Harness²

### 1.1 Propósito

El README define el harness como "el sistema circundante (prompts, herramientas, memoria, skills, orquestación, etc.) que hace que un modelo actúe como agente", y *harnessing* como el proceso de optimizar ese sistema ([README L19-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L19-L21)). Harness² corrige el harness con dos niveles de recursión **manteniendo fijos los pesos del modelo** ([README L23-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L23-L33)).

- **Recursión a nivel de tarea**: pule el harness de ejecución de la tarea actual mediante etapas contrastivas **Propose–Probe–Compose**. No usa retroalimentación de respuestas correctas; su único fundamento es el contraste de comportamiento entre ejecuciones.
- **Recursión a nivel de harnessing**: acumula, por tarea, el harness adoptado y las lecciones respaldadas por evidencia en un *harness de mejora* (biblioteca) persistente, para usarlo en la siguiente tarea.

El resumen del artículo da dos motivaciones. Las tareas de mundo abierto no se vieron en tiempo de diseño, por lo que **no hay un verificador de respuestas correctas**, y la automejora recursiva existente es específica de la tarea y no generaliza ([resumen en arXiv](https://arxiv.org/abs/2610.14224)).

### 1.2 Estructura y abstracciones principales

| Abstracción | Definición | Fuente |
| --- | --- | --- |
| Separación en tres ejes | No mezcla método (recursión, prompts, selección, biblioteca), sustrato (substrate: marco de agentes) y benchmark (valor `BenchSpec` + adaptador) | [`core/spec.py` L15-20](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L15-L20) |
| 8 componentes editables c1..c8 | Prompt de sistema, barreras de protección, memoria, guía de herramientas, subagentes, skills, scripts, plugins | [README L68-73](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L68-L73) |
| `SurfaceSpec` | Superficie de edición por marco (rutas, archivos de inyección permanente, límite de longitud, archivo de hooks, eventos de hook permitidos) | [`core/tree.py` L40-60](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L40-L60) |
| Límite de inyección permanente (always-on) | OpenCode 24,000 caracteres, Codex 8,000 caracteres. Deja escrito el motivo: Codex inyecta `AGENTS.md` en cada turno y lo recorta en silencio a 32,768 bytes | [`substrate/opencode.py` L42-51](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L42-L51), [`substrate/codex.py` L39-47](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L39-L47) |
| Convención de edición | "Omitir es heredar": una propuesta solo entrega los archivos que cambia | [`core/tree.py` L15-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L15-L21) |
| Rechazo de escape de rutas | Rechaza rutas absolutas y rutas que contienen `..` | [`core/tree.py` L82-89](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L82-L89) |
| `BenchmarkAdapter` | Todo lo que un benchmark debe rellenar: `tasks`, `task_prompt` (sin criterios de puntuación), `execute`, `trajectory`, `validate_tree`, `score`, etc. | [`core/spec.py` L200-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L200-L250) |
| `Substrate` | `surface`, `materialise`, `execute`, `read_trajectory`, `preflight` | [`substrate/base.py` L47-80](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L47-L80) |
| Roles | Ejecutor (executor), editor del harness (dos dimensiones, INV y DOM), compositor (composer), selector (selector), reflector de experiencia (experience reflector). El evaluador (judge) está fuera del método | Descripción de la figura en [README L37](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L37), [`core/recursion.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py), [`core/selection.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py), [`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19) |

### 1.3 Propose–Probe–Compose

1. **Propose**: el editor genera candidatos en dos dimensiones. INV es "cómo trabaja el agente" (herramientas, procedimientos) y DOM es "lo que sabe un profesional de ese campo" ([`core/prompts.py` L347-373](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L347-L373)). El §2.2.1 del artículo lo explica como defectos independientes del dominio y defectos específicos del dominio.
2. **Probe**: ejecuta cada candidato **en la misma tarea** y compara trayectorias y productos con la ejecución de referencia (§2.2.1 del artículo).
3. **Compose**: combina los cambios respaldados por la evidencia, corrige las ediciones en conflicto y adopta un candidato o mantiene el harness actual (§2.2.1 del artículo). La instrucción de composición fija como resultado esperado la combinación de ediciones INV y ediciones DOM ([`core/prompts.py` L934](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L934)).

Hay dos modos de expansión ([`core/recursion.py` L343-566](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L343-L566)).

- **Paralelo (`agg`)**: genera y ejecuta k candidatos INV + k candidatos DOM a partir de la misma evidencia de referencia, y luego crea k composiciones independientes entre sí.
- **Secuencial (`seq`)**: encadena k rondas de Propose–Probe–Compose, pasando a la siguiente etapa el harness pulido y la evidencia acumulada.

Una propuesta inválida se **reintenta una vez** y, si sigue fallando, se hereda el harness actual tal cual ([`core/recursion.py` L15-19, L36](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L36), [L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L242-L251)). En el reintento se devuelve literalmente el texto del error de validación. La convención de adaptadores también exige: "los mensajes de error se pasan tal cual como retroalimentación del reintento, así que escríbelos como frases accionables" ([`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245)).

### 1.4 Modelo de eventos y trayectorias

Harness² **no tiene un modelo de eventos de ciclo de vida** como el de Mallangable 5.6. En su lugar tiene dos cosas.

- **Gramática común de trayectorias**: representa los distintos formatos de registro de cada sustrato como líneas `[ACTION]` / `[OBSERVATION]` / `[ERROR]` ([`core/spec.py` L230-231](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L230-L231), [`substrate/codex.py` L386-389](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L386-L389), [`substrate/opencode.py` L384-388](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L384-L388)). Entrega la trayectoria completa como archivo y solo recorta cada observación individual con un límite de longitud (50,000 caracteres por defecto, prohibido por debajo de 10,000) ([`core/spec.py` L163-167](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L163-L167), [`core/context.py` L15-27](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L15-L27)).
- **La evidencia en archivos, el prompt como puntero**: el editor lee desde disco, bajo `context/`, la tarea, las trayectorias, los productos, el harness, la biblioteca y los candidatos, y debe citar el punto de la trayectoria que fundamenta cada edición ([`core/context.py` L521-544](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L521-L544)).
- **Los hooks son objeto de edición**: en el sustrato Codex, `.codex/hooks.json` forma parte de la superficie de edición. Los eventos permitidos son `PreToolUse`, `PostToolUse`, `PermissionRequest`, `PreCompact`, `PostCompact`, `SessionStart`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, `Stop` ([`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72)). El validador solo acepta el formato `command`. Deja escrito que, como un hook con formato incorrecto **simplemente no se ejecuta** y sin dar error, el formato se impone en el momento en que el proponente lo ve ([`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251)).

### 1.5 Metodología de evaluación

| Mecanismo | Contenido | Fuente |
| --- | --- | --- |
| Vista de ejecución sin puntuación | `RunView`, la información de ejecución que conoce el método, "nunca lleva puntuación" | [`core/spec.py` L176-187](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L187) |
| Puntuar solo después de la selección | `score()` solo lo llama `core.judge`, y solo después de confirmada la selección. Ningún módulo del lado del método importa `judge` | [`core/spec.py` L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L247-L250), [`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19), [BENCHMARKS L34](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L34) |
| Fallo de puntuación ≠ 0 puntos | El fallo es `None`, se excluye del denominador y no se guarda en caché como 0. Los casos sin puntuar se informan por separado | [`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18), [EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118), [BENCHMARKS L67-68](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L67-L68) |
| Bloqueo de rutas a las respuestas | Lanza una excepción si los `leak_globs` declarados por el benchmark entran en el contexto | [`core/context.py` L399-416](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L416) |
| Cable trampa de rastros de puntuación | Rechaza si las cadenas marcadoras de la salida del puntuador aparecen en nombres o cuerpos de archivos de contexto, o en el harness escrito por el agente. "Es un cable trampa, no la defensa en sí. Si salta, no amplíes la lista de marcadores; busca la ruta de lectura que tiene la fuga" | [`core/context.py` L419-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L419-L518) |
| Prohibición de palabras de medición | Rechaza el texto del benchmark visible para el agente si contiene benchmark, evaluation, grader, rubric o score: "describe el trabajo, no describas la medición" | [`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126) |
| Instrucción explícita de ausencia de puntuación | En los prompts del editor y del selector: "en el contexto no hay criterios de puntuación, respuestas ni puntuaciones. No intentes adivinar lo que quiere el evaluador" | [`core/prompts.py` L41-53](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L41-L53), apéndice H del artículo |
| Selección anónima | Etiqueta los candidatos como A, B, … y los baraja con la semilla `task_id\|k\|mode` (igual al volver a ejecutar). El conjunto de selección son solo los k candidatos finales; no incluye la ejecución de referencia | [`core/selection.py` L71-76](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L76), [L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L93-L111) |
| Sustituto si falla el selector | Si el selector falla, elige un sustituto neutral (la ejecución de referencia recibida o, si no la hay, el primer candidato final) y lo registra como `fallback` | [`core/selection.py` L237-252](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L237-L252) |
| Identidad presupuestaria | Ejecuciones por tarea R = 4k (k de referencia + 2k candidatos + k finales), sesiones de mejora P = 3k. Si las etiquetas se repiten lo trata como sobrescritura y falla antes de la comprobación numérica | [`core/ledger.py` L15-33, L89-113](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L113) |
| Identidad de ejecución | Incluye la huella del árbol del harness en el marcador de finalización, para no reutilizar ejecuciones salidas de otra configuración | [`core/runmark.py` L15-20, L41-61, L91-102](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L102) |
| Diversidad de candidatos | Mide con Jaccard por líneas entre harnesses candidatos si convergen en uno solo | [`core/tree.py` L407-427](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L407-L427) |
| Advertencia sobre acceso web | Al ser benchmarks públicos, los criterios de puntuación están en línea. En una ejecución de validación, una ejecución de Codex **descargó sin instrucción los criterios de puntuación de su propia tarea**. Recomienda un bloqueo a nivel de red en el host de ejecución y pide informar las restricciones usadas junto con los resultados | [EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109), [README L166-171](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L166-L171) |
| Alcance de la biblioteca | Separada por ejecución, modo y dominio; cada ejecución empieza con todos los dominios vacíos. Dentro del mismo dominio solo lee tareas anteriores | [`core/library.py` L15-24](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L15-L24), [EXPERIMENTS L16-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L16-L19) |
| Entradas de experiencia | Solo se guardan si tienen `cue`, `lesson` y `evidence` (`confidence` opcional). Si falta alguno no entran en la biblioteca | [`core/library.py` L43-47, L106-123](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L43-L123), [`core/selection.py` L494-501](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L494-L501) |

Los benchmarks son tres: JobBench, LAB y WorkBuddy-Bench ([README L129-133](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L129-L133)). Los resultados que declaran el README y el resumen son, con GLM-5 y Gemini 3.5 Flash en una sola etapa, mejoras de hasta 11.5 puntos en WorkBuddy-Bench, 4.5 puntos en JobBench y 11.8 puntos porcentuales en la tasa de aprobación parcial de LAB ([README L41-45](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L41-L45)). El apéndice F del artículo señala dos limitaciones. Al aumentar el presupuesto de recursión aumenta el coste de inferencia, y como no hay supervisión con respuestas correctas, el juicio es sensible a la variación entre ejecuciones y a los sesgos comunes de los modelos. Estas cifras no se reprodujeron directamente.

### 1.6 Licencia

- Cuerpo principal: Apache 2.0 ([README L199-204](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L199-L204)). No entra en conflicto con la Apache-2.0 que este repositorio prevé usar para esquemas y herramientas (sección «Licencia» del README).
- `third_party/`, los benchmarks y los conjuntos de datos siguen cada uno la licencia de su origen. WorkBuddy-Bench usa **una licencia propia de Tencent con restricciones regionales** ([BENCHMARKS L80-83](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L80-L83)).
- Esta nota solo usa citas de frases breves y enlaces; no copia código. Los textos propuestos de abajo también reescriben los conceptos con nuestras palabras y solo conservan la atribución de la fuente.

## 2. Tabla de correspondencias — conceptos de Harness² → Mallangable

Veredicto: **adoptar** (casi tal cual), **adaptar** (se toma solo la intención), **rechazar**.

| # | Concepto de Harness² | Ubicación en Mallangable | Veredicto | Motivo |
| --- | --- | --- | --- | --- |
| M1 | Harness = árbol editable c1..c8 | Definición de 5.6 (envoltura determinista) | **Rechazar** (a nivel de definición) | Nuestro harness es el lado que *impone* la política (policy). Una estructura en la que el agente modifica barreras de protección y hooks contradice I8 (solo el plano de control ejecuta con autoridad) y la regla de 7.11 "los archivos de política son inmutables". Sí es posible pulir fuera de línea solo los procedimientos (skills, prompts) |
| M2 | Si el formato del hook es incorrecto no se ejecuta en silencio; validación de formato en el momento de escritura | 5.6 «Atención», 7.2 hooks del harness del dispositivo | **Adoptar** | Deja al descubierto una ruta más que queda abierta cuando un hook falla (fail-open). Refuerza el principio existente: la configuración de hooks del dispositivo se valida contra el esquema al escribirse, y la verificación de recepción (receive-check) del servidor es la autoridad final |
| M3 | Lista de eventos de hook de Codex | 5.6 «Ejemplo de correspondencia» | **Adaptar** | Candidata a segunda tabla de correspondencias además de Claude Code. Pero la fuente es el validador de Harness², no la documentación oficial de Codex, así que se marca "pendiente de verificar" |
| M4 | `RunView` sin puntuación, puntuar después de la selección, cable trampa de rastros de puntuación, `leak_globs` | 10.2 pruebas ocultas, I7 | **Adoptar** | La SBR de Mallang-Bench solo tiene sentido si las pruebas ocultas están realmente ocultas. Si las pruebas ocultas se filtran al contexto de generación o de juicio, la SBR se distorsiona en sentido optimista |
| M5 | Fallo de puntuación es `None`, excluido del denominador, informado por separado | 10.2 «Formato de informe» | **Adoptar** | Si los fallos cuentan como 0, la CSR baja; si se excluyen y se ocultan, sube. Ninguna de las dos cosas es honesta |
| M6 | Fuga de criterios de puntuación por acceso web, informe de restricciones de red | 10.2 composición e informe, 7.3 lista de permitidos de comunicación externa | **Adoptar** | Si se publican el conjunto de ataques, el conjunto de extracción o las pruebas ocultas, surge el mismo problema. Se exige la regla de lista de permitidos de 7.3 también como condición de ejecución del benchmark |
| M7 | Prohibición de palabras de medición (describe el trabajo) | 10.2 conjunto de solicitudes | **Adoptar** | Si las frases del conjunto de solicitudes contienen palabras como "prueba" o "puntuación", el agente puede apuntar a la medición en sí |
| M8 | Selección anónima barajada con semilla, sin la ejecución de referencia | 5.8 juicio G4, 5.7 juez | **Adaptar** | Hace que el juez (judge) no sepa de qué generador, harness o ruta de modelo procede el candidato. Añade la "evaluación ciega al origen" (source-blind judging) a I7 (otra instancia) |
| M9 | Identidad presupuestaria R=4k, P=3k, verificación de etiquetas duplicadas | 10.2 CPC, 5.6 presupuesto | **Adaptar** | Para que la comparación de costes sea justa hay que informar a la vez "cuántas ejecuciones y cuántos juicios hubo". La identidad exacta solo vale para el método de Harness², así que se toman solo los *elementos del informe* |
| M10 | Identidad de ejecución mediante huella del harness | `change-record.schema.json` `provenance` | **Adoptar** | Hoy `agent` es solo una cadena "rol@harness", así que el registro es igual aunque cambie la *configuración* del harness. Con un hash de contenido se pueden reproducir, auditar y comparar bancos de prueba |
| M11 | Una propuesta inválida se reintenta 1 vez y luego se mantiene el estado actual | 5.8 G1 «Si falla», 5.6 presupuesto | **Adoptar** | G1 solo dice "devolver el motivo al agente"; no tiene límite ni estado final. Pensando en el atacante de costes (7.1), hacen falta un límite y una terminación "sin cambio" |
| M12 | Biblioteca de experiencia por dominio (cue, lesson, evidence) | 5.3 `ResolutionCache`, capítulo 6 caché de resoluciones, 7.5 separación de alcance | **Adaptar** | La separación de alcance ya está en 7.5. Lo que se toma es la condición de almacenamiento "no se guarda una lección sin campo de evidencia", y un elemento de informe que diga si en el banco de pruebas la caché empezó vacía |
| M13 | Propose–Probe–Compose (mejora por contraste sin respuestas correctas) | 10.1 O1, O4, 5.7 fusionador y promotor | **Adaptar (opcional)** | 4k ejecuciones para un solo cambio (change) conversacional no encajan con los niveles de tiempo (time tier) (8.4) ni con el coste. Se deja solo como punto de partida para trabajos de servidor (fusión, promoción) o para la investigación de O4 sobre la fiabilidad del juez |
| M14 | Gramática de trayectorias `[ACTION]/[OBSERVATION]/[ERROR]` | 5.11 telemetría, evidencia de G4 | **En espera** | La misma información puede construirse con los eventos E4 y E5. Se revisará al definir el formato de entrada del juez |
| M15 | Diversidad de candidatos (Jaccard) | — | **Rechazar** | Nuestra especificación no tiene una etapa que genere múltiples candidatos (YAGNI) |
| M16 | Límite de longitud de inyección permanente y su motivo | 5.10 suministro de contexto | **En espera** | Es una cifra de referencia para cuando se defina el presupuesto de contexto por rol. Por ahora el fundamento para meterla en la especificación es débil |

## 3. Lista de ediciones propuestas (por prioridad, máximo 10)

Cada elemento es una edición mínima. Los textos no traducen frases de Harness², sino que reescriben sus conceptos.

### E-1. Añadir a 10.2 Mallang-Bench la regla de aislamiento de pruebas ocultas (M4)

- Archivo: `docs/10-open-problems.md`, justo debajo de la tabla «### Composición»
- Fundamento: [`core/spec.py` L176-187, L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L250), [`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19), [`core/context.py` L399-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L518)
- Texto propuesto:

```markdown
Aislamiento de pruebas ocultas (DEBE (MUST)):
- Las pruebas ocultas y sus resultados no entran en el contexto del intérprete, del generador ni del juez. La puntuación la hace un proceso aparte una vez terminada la activación.
- Cada vez que el ejecutor construye un contexto de generación o de juicio, busca las rutas de archivo de las pruebas ocultas y las cadenas marcadoras de resultados de prueba y, si las encuentra, detiene la ejecución. Esta comprobación es solo una alarma, no una defensa. Si salta, no se amplía la lista de marcadores; se corrige la ruta de lectura que tiene la fuga.
(Fuente: la vista de ejecución sin puntuación y el cable trampa de rastros de puntuación de Harness², google-research/harness2 `core/spec.py`, `core/context.py`)
```

### E-2. Añadir a 10.2 «Formato de informe» la regla de sin puntuar (M5)

- Archivo: `docs/10-open-problems.md`, al final del párrafo «### Formato de informe»
- Fundamento: [`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18), [EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118)
- Texto propuesto:

```markdown
Una solicitud cuya puntuación falló (error al ejecutar las pruebas ocultas, error del modelo juez) no vale 0 puntos sino que queda **sin puntuar**. Se excluye del denominador de la métrica y el número de casos sin puntuar se informa junto a la métrica. Ejemplo: "CSR 0.71 (n=192, sin puntuar 8)".
```

### E-3. Añadir a 10.2 «Formato de informe» elementos de informe del entorno de ejecución (M6, M9, M12)

- Archivo: `docs/10-open-problems.md`, después del párrafo de E-2
- Fundamento: [EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109), [`core/ledger.py` L15-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L33), [`core/library.py` L21-23](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L21-L23)
- Texto propuesto:

```markdown
Condiciones de ejecución que se informan a la vez:
- **Restricción de red**: lista de hosts a los que podía acceder el agente generador. Las direcciones que alojan las pruebas ocultas, el conjunto de ataques o el conjunto de extracción se bloquean durante la ejecución. Se ha informado de casos en benchmarks públicos en los que el agente descargó sin instrucción los criterios de puntuación (guía de experimentos de Harness²).
- **Número de llamadas**: número de ejecuciones de generación y de sesiones de juicio por cada cambio exitoso (reintentos incluidos). Con la CPC sola no se pueden comparar con justicia harnesses distintos.
- **Estado de la caché**: si la caché de resoluciones y las lecciones aprendidas empezaron vacías, o si se permitió usar los resultados de solicitudes anteriores.
```

### E-4. Añadir a 5.8 G4 la evaluación ciega al origen (M8)

- Archivo: `docs/05-reference-architecture.md`, celda "Contenido" de la fila `G4 Juicio` de la tabla de puertas de 5.8
- Fundamento: [`core/selection.py` L71-76, L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L111), §2.2.2 del artículo
- Actual: `El juez determina por capturas de pantalla e intención si se cumple el significado`
- Propuesta: `El juez determina por capturas de pantalla e intención si se cumple el significado. El juez no sabe de qué generador, harness o ruta de modelo procede el producto (evaluación ciega al origen). Si hay varios candidatos, se presentan con id anónimos barajados con una semilla reproducible`

### E-5. Explicitar en 5.8 G1 el límite de reintentos en caso de fallo (M11)

- Archivo: `docs/05-reference-architecture.md`, celda "Si falla" de la fila `G1 Análisis estático` de la tabla de puertas de 5.8
- Fundamento: [`core/recursion.py` L15-19, L36, L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L251), [`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245)
- Actual: `Devuelve el motivo al agente`
- Propuesta: `Devuelve el motivo al agente como una frase que permita corregirlo. Si se supera el límite de reintentos (valor propuesto: 1 vez), termina manteniendo el estado actual sin cambios`

### E-6. Añadir a 5.6 «Atención» la advertencia de hooks que quedan abiertos al fallar (M2)

- Archivo: `docs/05-reference-architecture.md`, después del último párrafo «Atención:» de 5.6
- Fundamento: [`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251)
- Texto propuesto:

```markdown
En muchos entornos de ejecución, una configuración de hooks con formato incorrecto **simplemente no se ejecuta**, sin dar error. Es decir, si falla, queda abierta. El plugin del harness valida la configuración de hooks en el momento de escribirla contra los nombres de evento y el formato de manejador que acepta el entorno de ejecución, y al iniciar la sesión (E1) comprueba que los hooks se hayan registrado de verdad. El agente no puede modificar los archivos de hooks de política ni de barreras de protección (frontera de herramientas, E4).
(Referencia: Harness² valida los archivos de hooks de Codex en el momento de escribirlos por la misma razón. google-research/harness2 `core/tree.py`)
```

### E-7. Añadir a `change-record.schema.json` un campo de huella del harness (M10)

- Archivo: `schemas/change-record.schema.json`, en `properties.provenance.properties`, después de `prompt_hash`
- Fundamento: [`core/runmark.py` L15-20, L41-61](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L61), [`substrate/base.py` L26-32](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L26-L32)
- Campo propuesto (no cambia `required`; campo opcional):

```json
"harness_digest": {
  "type": "string",
  "pattern": "^sha256:[0-9a-f]{64}$",
  "description": "Hash de contenido de la configuración del harness (skills, hooks, copia de la política, lista de herramientas) que produjo el cambio. Aunque la cadena agent sea la misma, el valor difiere si la configuración es distinta"
}
```

- Observación: Harness² usa los 16 primeros caracteres de SHA-1. Aquí se propone el SHA-256 completo, alineado con el formato existente de `prompt_hash`. Si se incorpora, hay que volver a ejecutar la validación de `examples/change.example.yaml` (al ser un campo opcional, lo normal es que los ejemplos existentes sigan pasando tal cual).

### E-8. Añadir al conjunto de solicitudes de 10.2 la prohibición de palabras de medición (M7)

- Archivo: `docs/10-open-problems.md`, al final de la celda "Contenido" de la fila `conjunto de solicitudes` de la tabla «### Composición»
- Fundamento: [`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126)
- Texto a añadir: `. Las frases de la solicitud solo dicen qué hay que hacer, no hablan de la medición (prohibido "prueba", "puntuar", "puntuación", etc.)`

### E-9. Añadir a la tabla de correspondencias de 5.6 una columna candidata para Codex (M3)

- Archivo: `docs/05-reference-architecture.md`, un párrafo breve después de la tabla «### Ejemplo de correspondencia: hooks de Claude Code»
- Fundamento: [`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72) (fuente secundaria, no la documentación oficial de Codex)
- Texto propuesto:

```markdown
Codex CLI se corresponde de la misma manera (E1 `SessionStart`, E2 `UserPromptSubmit`, E4 `PreToolUse`, E5 `PostToolUse`, E6 `PermissionRequest`, E11 `Stop`, E12 `SubagentStop`, E15 `PreCompact`). Esta lista procede del conjunto de eventos que valida Harness², por lo que debe cotejarse con la documentación oficial de Codex antes de incorporarla.
```

### E-10. Añadir Harness² a las referencias

- Archivo: `docs/references.md`, nueva sección antes de «## Seguridad de agentes»
- Texto propuesto:

```markdown
## Mejora y evaluación del harness

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · Código (Apache-2.0): https://github.com/google-research/harness2
  - Fundamento del aislamiento de pruebas ocultas, del informe de casos sin puntuar, del juicio con evaluación ciega al origen y de la huella del harness (5.6, 5.8, 10.2). Nota de investigación: [research/harness2-analysis.md](harness2-analysis.md)
```

## 4. Lo que no se incluyó

- **Harness autoeditable (M1)**: si el agente que modifica la aplicación del usuario modifica también sus propios hooks de política, desaparece la razón por la que 5.6 definió el harness ("una envoltura determinista que rodea a un agente no determinista").
- **Meter Propose–Probe–Compose en el flujo de generación por defecto (5.4)**: un solo cambio costaría 4k ejecuciones y no se podrían respetar los niveles de tiempo T0~T2. Su lugar es como opción experimental de los trabajos de servidor y en la investigación de O4.
- **Citar las cifras de los benchmarks**: no se reprodujeron directamente, y la distribución de tareas es distinta de nuestro problema (modificar aplicaciones).
