<!-- LANG-BAR -->
[English](CHANGELOG.md) · [한국어](CHANGELOG.ko.md) · [简体中文](CHANGELOG.zh-CN.md) · [日本語](CHANGELOG.ja.md) · **Español**
<!-- /LANG-BAR -->

# Registro de cambios

## v0.2.4 — 2026-11-05

Ediciones multilingües. No cambian el contenido de la especificación, las cifras del espacio de diseño ni los contratos de los esquemas.

* El README predeterminado pasa a estar en inglés y las ediciones por idioma se separan: English (`README.md`) · 한국어 (`README.ko.md`, original) · 简体中文 (`README.zh-CN.md`) · 日本語 (`README.ja.md`) · Español (`README.es.md`). CHANGELOG y CONTRIBUTING siguen el mismo esquema.

* El cuerpo de la especificación y las notas de investigación se trasladan a `docs/<idioma>/` y se redactan en cinco idiomas (`docs/en`, `docs/ko`, `docs/zh-CN`, `docs/ja`, `docs/es`). La edición coreana es la original; si una traducción difiere, prevalece el original.

* Las descripciones de los esquemas, los documentos de ejemplo y los mensajes y la ayuda de las herramientas pasan a estar en inglés. Los ejemplos de paquete de léxico (lexicon pack) se separan por idioma (`examples/lexicon.{en,ko,zh-CN,ja,es}.yaml`). `check_schemas.py` los valida todos.

## v0.2.3 — 2026-11-05

Revisión de seguridad adversarial de todo el repositorio con la skill security-audit de Cloudflare (perfil quick, `docs/es/research/security-audit-2026-11-05.md`). Las cifras del espacio de diseño no cambian.

### Control · arquitectura de referencia (capítulos 4 y 5)

* La excepción de las acciones de piso en `decide()` del PDP se restringe a `floor_scoped(req)`. Solo cuentan como piso cuando hay un propietario humano · la propia capa · un estado anterior · sin aumento de permisos ni de profundidad; cualquier otra reversión (invocada por un agente, rehacer, "volver a activar", liberar una retención) pasa por el mismo juicio que la activación. También se añade la rama de funcionalidades destructivas (G5) (4.8, 5.5).

### Versiones · confianza (capítulos 6 y 7)

* La aplicación automática en la propagación de la línea base pasa por `activate()` (E10) y, si requiere aprobación, se degrada a propuesta. `delta_permissions` se vuelve a calcular en lugar de fiarse de lo autodeclarado (6.5).

* Se añaden a la lista de verificación de seguridad el alcance de la excepción de piso, la aplicación automática en la propagación, el recálculo del cambio de permisos, la declaración de egress y el escape de la salida de las herramientas (7.11).

### Contratos de esquema

* `change-record`: al menos uno de los contratos deterministas debe tener forma ejecutable. Se rechazan los registros que solo tienen contratos descriptivos.

* `extension-manifest` · `policy`: `network.allow` · `allowlist` rechazan literales IP. Los comodines sobre sufijos públicos, la existencia del permiso de egress y que `setKnob` cumpla default ⊆ ceiling quedan explícitos como MUST del validador de conformidad (conformance validator), y se añaden casos de regresión (que esperan `False`).

### Herramientas · CI

* `check_schemas.py`: escape de caracteres de control en la salida, rechazo de alias YAML y de archivos de más de 1 MiB, aislamiento de excepciones por documento.

* `design_space.py`: `--profile` · `--check` terminan con código de salida 1 ante `normative` · `logical` · errores de entrada; se rechazan claves duplicadas y JSON que no sea un objeto.

* El token de CI se limita a `contents: read`.

## v0.2.2 — 2026-11-04

Preparación de la publicación como código abierto. No cambian el cuerpo de la especificación, las cifras del espacio de diseño ni los esquemas.

* Licencias definidas: documentos CC BY 4.0 (`LICENSE-docs`), esquemas · ejemplos · herramientas Apache-2.0 (`LICENSE`).

* Se añaden `CITATION.cff`, `CONTRIBUTING.md` y `requirements.txt`.

* Las herramientas aceptan archivos de otros proyectos: `design_space.py --profile FILE.json`, `check_schemas.py <schema> FILE...`.

* Se añaden al README "Aplicarlo a tu proyecto" (6 pasos: vocabulario → espacio de diseño → ampliar la calculadora → contratos de datos → arquitectura → declarar conformidad) y el formato de cita.

* Se publica como repositorio público en GitHub (https://github.com/Hyunki6040/mallangable-ai). La parte inicial del README se reescribe en el orden planteamiento del problema (tres carencias) → 6 ideas clave → cómo funciona → ejemplo de cambio, y se añade una CI que ejecuta la regresión de esquemas y la verificación de P1~P7 en cada push y PR.

## v0.2.1 — 2026-11-03

Se estudian e incorporan los documentos de especificación de ThinkRail (JetBrains/thinkrail, Apache-2.0) (`docs/es/research/thinkrail-analysis.md`). Las cifras del espacio de diseño y los esquemas no cambian.

### Control · arquitectura de referencia (capítulos 4 y 5)

* La aprobación (approval) tiene alcance (solo esta vez · durante esta tarea · siempre), y "siempre" queda ligado al content\_hash de la funcionalidad y a la lista de permisos. Cualquier respuesta que no sea afirmativa es un rechazo (4.8).

* Revertir se basa en el id del estado que vio el usuario. Si el estado difiere, no se cambia nada; rehacer es la misma operación (5.5).

* Se añaden reglas para procesar la salida del juez. Formato incorrecto es fallo, el registro lo crea de nuevo el harness, un fallo sin observaciones se rechaza, si hay observaciones abiertas no se confirma la aprobación, y el tope de reintentos es compartido por todos los puntos de entrada (5.8).

* La señal de finalización es solo E11, y la espera de aprobación es una señal de nivel. En cada entrada de la tabla de correspondencia se anotan el comportamiento verificado, la condición para volver a verificar y la condición para eliminarla (5.6).

* La unidad de aislamiento del vigilante es la funcionalidad completa (5.9).

### Versiones · confianza · experiencia (capítulos 6\~8)

* Las tareas de generación concurrentes tienen cada una su propia copia de trabajo y solo registran las rutas que cambiaron (6.4).

* Un fallo al leer una entrada de la fusión no se trata como ausencia (`null`, es decir, eliminación) (6.5).

* Aceptar algo compartido cubre solo el contenido de ese momento, y una funcionalidad recibida no puede apropiarse de los nombres de mis comandos ni atajos (6.9).

* Las listas, vistas previas y la visualización de permisos no ejecutan código de extensiones (7.11).

* Paquete de léxico: en los datos guardados solo se pone `id de concepto + argumentos`, una funcionalidad compartida no puede cambiar el paquete de léxico, y se fija el orden de sustitución a nivel de cadena (8.9).

## v0.2 — 2026-10-30

Se incorporan tres estudios (`docs/es/research/`): el análisis de Harness², el estudio de casos previos (MCP · AG-UI · OTel · Cedar · RFC 7396, etc.) y la evaluación adversarial.

### Espacio de diseño (capítulo 3, `tools/design_space.py`): las cifras cambian

* La definición de profundidad de 2.6 se impone como regla. L3 es `A1∈{D1,D2,D3} ⇒ decl` y L4 es `D4 ⇒ sandboxed`.

* Nueva N6: D5 no se comparte y no puede usar la topología snapshot (I1).

* Combinaciones recomendadas 70,516 → **36,772**, familias estructurales 1,618 → **863**, opciones de negocio 58% → **57%**. La matriz de acoplamiento con BM de 7×20 no cambia.

* P1 · P6 pasan a D4, y P2 · P5 · P7 a D3 declarativo. Los siete perfiles siguen siendo clean.

* Se añaden a las estadísticas de reglas los recuentos de violaciones independientes y únicas, que no dependen del orden. Se retira la afirmación "L1 es la que más filtra".

* Se rechazan entradas incorrectas: perfiles inexistentes, errores de JSON y ejes desconocidos.

### Modelo central · control (capítulos 2 y 4)

* La composición de capas `⊕` se define como RFC 7396 JSON Merge Patch. También se explicita su relación con la fusión 3-way.

* El paso de retenido → activo pasa por una nueva verificación.

* I8 se traslada a requisito del nivel Governed. P1 · P5, que no tienen servidor, solo llegan al nivel Core.

* Se añade un adaptador para el motor de políticas Cedar, e I5 se demuestra con SymCC. Los derechos mínimos del usuario (F1\~F7) se evalúan antes que el motor.

### Arquitectura de referencia (capítulo 5)

* Con visibilidad `own`, el generador solo recibe los tipos de las capas superiores y el mapa de capacidades (I6).

* La activación pasa por el PDP y G5. Antes de la aprobación, el código D4 solo se monta con permisos 0.

* G4: se aplica la evaluación ciega al origen (source-blind judging) y los candidatos se presentan con ids anónimos basados en semilla.

* G1: si falla, devuelve un motivo corregible y, tras reintentar, mantiene el estado actual.

* Se añade la tabla de correspondencia de eventos de harness. Se incluyen las tablas para AG-UI, A2A y MCP `input_required`; Codex requiere verificación en la documentación oficial.

* Se advierte del problema de que una configuración incorrecta de hooks deje el sistema en permitir por defecto. Se explicita que los hooks `Stop`/`SubagentStop` no son puertas que bloqueen.

* Los campos de observabilidad se renombran con los nombres de OTel GenAI y se añaden `policy.decision_id` y `traceparent`.

### Versiones · confianza · experiencia · negocio (capítulos 6\~9)

* Se reescribe el algoritmo de propagación.

  * Usa la unión de los contratos de toda la ruta.

  * Un padre en espera de aprobación no detiene a sus hijos.

  * El canario es una muestra aleatoria basada en semilla.

* Debilitar un contrato solo se permite con consentimiento explícito de una persona, y se registra como `Contract-Migrated`.

* Se añade un eje de integridad a las etiquetas de flujo de información (FIDES).

* Se añaden 3 amenazas: contaminación de contratos y juicios, contaminación de la caché de resoluciones y compromiso de versiones del proyecto original o del operador.

* La firma del publicador se define en formato in-toto/SLSA.

* Los secretos solo se reciben mediante elicitation en modo URL de MCP. ModelPort no se monta sobre MCP Sampling.

* Los artefactos de clientes solo entran en la línea base oficial con opt-in y consentimiento de licencia (B10 · B19).

### Mallang-Bench (capítulo 10)

* Las pruebas ocultas se aíslan y se ponen detectores de filtración (tripwires).

* Los elementos en los que falla el juicio se informan como sin puntuar (unscored) y se excluyen del denominador.

* Se informan también las condiciones de ejecución: restricción de red, número de llamadas, estado de la caché.

* El denominador de la SBR incluye las fusiones aprobadas por personas.

### Esquemas (`schemas/`, nuevo `tools/check_schemas.py`)

* Los elementos de contrato se definen en forma ejecutable (`tree-query` · `unit` · `snapshot` · `judge`). Debe haber al menos 1 elemento determinista, y `judge` debe ser no determinista. El formato de descripción libre se mantiene solo por compatibilidad hacia atrás.

* Se fijan las puertas obligatorias por profundidad. Si aumentan los permisos, deben estar G5 y `approved_by`.

* Se rechazan las declaraciones de intención con solo espacios en blanco y los ids y fechas incorrectos.

* Campos añadidos:

  * `provenance.harness_digest`

  * `extensionPoint.merge`

  * `catalog_id`

  * `destructive`

* Las perillas de política deben cumplir piso ≤ valor predeterminado ≤ techo.

* Los artefactos D1\~D3 del manifest solo admiten forma declarativa.

* De los 17 documentos que la especificación prohíbe, el esquema rechaza 15. Para los 2 restantes, que requieren comparar documentos entre sí, se explicita que el validador DEBE (MUST) verificarlos.

### Referencias

* Las fuentes secundarias se sustituyen por fuentes primarias: especificación de Agent Skills, documentación de plugins en inglés, A2UI v0.9.1, Mergiraf (GPL-3.0-only).

* Se añaden secciones nuevas: motores de políticas, observabilidad, cadena de suministro, mejora y evaluación de harness.
