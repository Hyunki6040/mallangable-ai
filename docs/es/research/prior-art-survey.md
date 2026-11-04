<!-- LANG-BAR -->
[English](../../en/research/prior-art-survey.md) · [한국어](../../ko/research/prior-art-survey.md) · [简体中文](../../zh-CN/research/prior-art-survey.md) · [日本語](../../ja/research/prior-art-survey.md) · **Español**
<!-- /LANG-BAR -->

# Nota de investigación — estudio de antecedentes (código abierto, especificaciones, estándares de agentes)

> Conclusión de esta nota: **no hay ningún estándar que se solape** con lo que esta especificación define como nuevo (fusión que preserva contratos, propagación del linaje, delegación por intervalos, derechos mínimos). Sin embargo, las piezas de alrededor ya están estandarizadas, y la especificación actual no usa sus nombres o las cita a través de fuentes secundarias. Hay cinco líneas que tomar. ① Fijar el significado por defecto de la composición de capas declarativas `⊕` en **JSON Merge Patch (RFC 7396)** y hacer que las reglas de fusión de listas las **declare el esquema**, como en Kubernetes Server-Side Apply. ② Añadir un **eje de integridad** a las etiquetas de flujo de información (7.5) (FIDES, CaMeL). ③ Comprobar mecánicamente la reducción monótona de políticas (I5) con la **verificación de inclusión de políticas de Cedar**. ④ Alinear la telemetría (5.11) con los **nombres de atributos de OpenTelemetry GenAI**. ⑤ Reflejar en la conexión de modelos (8.10) la **elicitation en modo URL** y la retirada de Sampling de la última versión de MCP (2026-07-28).

- Fecha de verificación: 2026-10-30
- Método: de los repositorios se leyeron con `gh api` los metadatos, los archivos de licencia y el texto original de las especificaciones; de los documentos web solo se obtuvieron los sitios oficiales. No se ejecutó código. Para todas las URL citadas se comprobó con `curl -L` una respuesta 200 (la biblioteca digital de ACM bloquea las peticiones automáticas con 403, así que solo se anotó el DOI).
- Alcance: este capítulo no modifica los documentos existentes. Si se incorporan las propuestas de edición de la sección 3 se decide por separado.

## 0. Qué se verificó y qué no

| Elemento | Estado | Observaciones |
| --- | --- | --- |
| Última revisión de MCP | Verificado | `2026-07-28` (publicada el 2026-07-28). Texto original de `docs/specification/2026-07-28/changelog.mdx` del repositorio |
| MCP Apps | Verificado | `specification/2026-01-26/apps.mdx` de `modelcontextprotocol/ext-apps`. Id de extensión `io.modelcontextprotocol/ui` |
| Convenciones GenAI de OpenTelemetry | Verificado | **Se trasladaron** de `open-telemetry/semantic-conventions` **al repositorio `semantic-conventions-genai`**. Todos los documentos tienen estado Development |
| A2UI | Verificado | El repositorio se trasladó a `a2ui-project/a2ui`. Versión actual v0.9.1; v1.0 está en RC |
| Reglas de decisión y verificador de Cedar | Verificado | Documentación oficial y README de `cedar-policy-symcc` |
| Estructura interna de Patchwork | Parcial | Solo se leyeron la página del proyecto y la nota de experimento 07. El repositorio `inkandswitch/patchwork-system` no indica licencia |
| Texto original de Boxer | No leído | ACM bloquea las peticiones automáticas. Solo se verificaron los datos bibliográficos |
| Licencia de la documentación de Chrome, Figma y VS Code | No verificada | Al ser documentación de producto, solo se cita y no se copia su texto |

## 1. Estudio por elemento

Veredicto: **adoptar** = se cita y se alinean los nombres y el significado de los campos / **referencia** = solo se cita como trabajo relacionado / **no aplica** = no se incluye.
La columna "Correspondencia" indica los números de sección y los archivos de esquema de esta especificación.

### 1.1 Investigación sobre software maleable

| Elemento | Qué es | Fuente primaria | Licencia | Correspondencia | Veredicto |
| --- | --- | --- | --- | --- | --- |
| Ensayo Malleable software (Ink & Switch, 2025) | Ensayo que propone recuperar la agencia del usuario frente a las aplicaciones cerradas. Sistematiza los conceptos de pendiente suave y desarrollador local | https://www.inkandswitch.com/essay/malleable-software/ | Ensayo (sin indicación) | 1.5, 2.6 | Ya citado. Se mantiene |
| Potluck (2022) | Superpone búsquedas, fórmulas y anotaciones dinámicas sobre texto para añadir estructura de forma gradual. Las anotaciones son una capa superpuesta que no modifica el original | https://www.inkandswitch.com/potluck/ | Ensayo | 2.3 capas, 2.6 D1~D3 | **Referencia**. Precedente de "capa superpuesta que no toca el original" |
| Embark (2023) | Desmonta la aplicación reuniendo datos, cálculos y vistas en un solo documento de planificación de viajes | https://www.inkandswitch.com/embark/ | Ensayo | 10.1 O8 (herramientas que van más allá de la aplicación) | **Referencia** |
| Patchwork (2024~) | Control de versiones genérico para documentos no de código, como textos o dibujos. En las notas de experimento, **un bot de IA edita en una rama, una persona revisa el diff y fusiona solo una parte, y las ediciones del bot quedan marcadas en el historial** | https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/ | El repositorio no indica licencia | 6.4 ramas `exp/*`, 6.11 trailer `Agent:`, 8.6 recibo | **Referencia**. El enlace actual de references.md a "Universal Version Control" es la página de listado del laboratorio, así que es más preciso cambiarlo por la página de Patchwork |
| Cambria (2020) | Transforma datos entre versiones de esquema mediante lentes bidireccionales | https://www.inkandswitch.com/cambria/ · https://github.com/inkandswitch/cambria-project | MIT | 5.9 `migrate(prev)`, `extension-manifest` `state.migrate_from` | **Referencia**. El diseño actual, que deja el traspaso de estado como un `migrate` unidireccional, es suficiente. Es el fundamento si alguna vez hace falta bidireccionalidad |
| Webstrates (UIST 2015) | Sincroniza los cambios del DOM y difumina la frontera entre documento y aplicación. Cuatro principios: maleabilidad, compartición, distribución y computación | https://webstrates.net/ · https://github.com/Webstrates/Webstrates | Apache-2.0 | 6.13 riesgo del código sobre CRDT | **Referencia**. Es un precedente de compartir código ejecutable en tiempo real, por lo que sirve como caso de fundamento para S7 |
| Boxer (diSessa & Abelson, CACM 29(9), 1986) | Medio computacional que los no especialistas pueden recomponer | DOI 10.1145/6592.6595 | Artículo | 1.5 | **Referencia**. El linaje de Smalltalk se excluyó porque no se buscó la fuente primaria |

### 1.2 Manifiestos de extensiones y plugins

| Elemento | Qué es | Fuente primaria | Licencia | Correspondencia | Veredicto |
| --- | --- | --- | --- | --- | --- |
| Puntos de contribución y eventos de activación de VS Code | Declara puntos de extensión (extension points) con `contributes` (commands, menus, views, keybindings, configuration, `languageModelTools`, etc.). Desde 1.74 los puntos de contribución implican automáticamente eventos de activación | https://code.visualstudio.com/api/references/contribution-points · https://code.visualstudio.com/api/references/activation-events | Código MIT, documentación no verificada | 2.2 `kind` del punto de extensión, `capability-map` | **Referencia**. La correspondencia con `kind` (token, command, view, hook, service) es natural |
| VS Code Workspace Trust | `capabilities.untrustedWorkspaces.supported: true / false / "limited"`. Los espacios de trabajo no confiables se abren en Restricted Mode y se bloquea la ejecución automática | https://code.visualstudio.com/api/extension-guides/workspace-trust | Documentación | 4.6 F2 modo seguro, 6.9 compartidos recibidos | **Referencia** |
| Permisos de Chrome MV3 | `permissions`, `optional_permissions`, `host_permissions`, `optional_host_permissions`. **Si una actualización añade un permiso que lleva advertencia, la extensión se desactiva hasta que el usuario lo acepte** | https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions | Documentación | I4, 6.5 `delta_permissions`, 6.9 subscribe | **Referencia**. Precedente real a gran escala de I4. Va en la misma dirección que la regla actual de la especificación (aumento de permisos → propuesta) |
| Manifiesto de plugins de Figma | `networkAccess.allowedDomains` (se admite `["none"]`), `reasoning` (obligatorio si hay comodín), `devAllowedDomains`, `permissions` | https://developers.figma.com/docs/plugins/manifest/ | Documentación | `extension-manifest` `network.allow` | **Referencia**. El campo de "motivo del permiso" es candidato de la sección 4 |
| Plugins comunitarios de Obsidian | La documentación oficial declara que "no se puede limitar un plugin a permisos concretos" y que puede acceder a archivos, a la red y a instalar programas. Por defecto, Restricted mode | https://obsidian.md/help/plugin-security | Aplicación propietaria, `obsidian-api` MIT | 7.6, 7.7 | **Referencia**. Merece citarse como contraejemplo de extensiones sin aislamiento |
| WASM Component Model / WIT | Un `world` declara los import y export del componente y el anfitrión (host) solo suministra lo importado. Los paquetes llevan versión (`wasi:http@0.2.0`) | https://component-model.bytecodealliance.org/design/wit.html · https://github.com/WebAssembly/component-model | Apache-2.0 | 7.6 capacidad de objeto (object capability), adaptador `lang` de `SandboxHost`, `permissions` del manifiesto | **Referencia**. Para productos `wasm`, puede haber correspondencia 1:1 entre `permissions` del manifiesto ↔ imports del world |
| Extism | Marco de plugins WASM. El manifiesto tiene `wasm[].hash`, `memory.max_pages`, `allowed_hosts`, `allowed_paths`, `config` | https://extism.org/docs/concepts/manifest · https://github.com/extism/extism | BSD-3-Clause | `extension-manifest` `artifact.content_hash`, `network.allow`, `resources.memory_mb` | **Referencia**. Los mismos conceptos ya existen. Hay pocos motivos para alinear los nombres |
| Tauri v2 capability | Ya citado | (references.md) | | 7.6 | Se mantiene |
| Endo / SES | Ya citado | (references.md) | Apache-2.0 | 7.6 | Se mantiene |

### 1.3 Protocolos de agentes y eventos del harness

| Elemento | Qué es | Fuente primaria | Licencia | Correspondencia | Veredicto |
| --- | --- | --- | --- | --- | --- |
| MCP 2026-07-28 | Paso a sin estado (se elimina `initialize`; en cada petición, versión y capacidades del cliente en `_meta`), `server/discover`, peticiones de múltiples idas y vueltas (MRTR: `resultType: "input_required"`), tasks pasa a extensión oficial, **Roots, Sampling y Logging quedan en vías de retirada**, convención de `traceparent` en `_meta` (SEP-414) | https://modelcontextprotocol.io/specification/2026-07-28/changelog | Apache-2.0 (especificación, en transición desde MIT), documentación CC-BY-4.0 | 5.3 `ModelPort`, 5.6, 8.10 | **Adoptar**. La ruta `sub` de 8.10 no debe diseñarse sobre MCP Sampling |
| Annotations de herramientas de MCP | `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`. **Si el servidor no es de confianza, el cliente no debe fiarse de las annotations (MUST)** | https://modelcontextprotocol.io/specification/2026-07-28/server/tools | Igual que arriba | `capability-map` `capability.risk` | **Adoptar**. Se pone una tabla de correspondencias con los valores de `risk` (sección 3, E-10) |
| Elicitation de MCP | Modo form y modo URL. **Los secretos y credenciales no deben recibirse en modo form; debe usarse el modo URL (MUST)** | https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation | Igual que arriba | 8.10 clave de conexión, I6 | **Adoptar** |
| Autorización de MCP | OAuth 2.1, Protected Resource Metadata (RFC 9728), indicadores de recurso (RFC 8707), verificación de `iss` (RFC 9207) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | Igual que arriba | 2.1 delegación, 7.2 | **Referencia**. Fundamento de implementación para la explicación de I4 e I9 de que el agente α es "un sujeto de corta duración con delegación humana" |
| MCP Apps (SEP-1865) | Recursos `ui://`, `text/html;profile=mcp-app`, iframe en sandbox obligatorio, `_meta.ui.csp` (`connectDomains`, `resourceDomains`, `frameDomains`, `baseUriDomains`), `permissions` (camera, microphone, geolocation, clipboardWrite) | https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx | Igual que arriba | 3.2 A4 `frame`, `extension-manifest` `network` | Ya citado. **Se mantiene la adopción**. Se fija el enlace a la ruta de la especificación con fecha |
| MCP-UI | Prototipo de MCP Apps. Hoy es un SDK compatible con MCP Apps | https://github.com/MCP-UI-Org/mcp-ui | Apache-2.0 | | **No aplica** (MCP Apps es suficiente) |
| AG-UI | Protocolo de eventos agente↔frontend. `RUN_STARTED`/`RUN_FINISHED`/`RUN_ERROR`, `STEP_*`, `TOOL_CALL_*`, `STATE_SNAPSHOT`/`STATE_DELTA` (**RFC 6902 JSON Patch**), `SUBAGENT_*`. La aprobación humana es una nueva ejecución con `resume[]` tras `outcome: { type: "interrupt" }` de `RunFinished` | https://docs.ag-ui.com/concepts/events · https://docs.ag-ui.com/concepts/interrupts · https://github.com/ag-ui-protocol/ag-ui | MIT | 5.6 modelo de eventos, 8.5 expresión del progreso, 2.8 `pendiente de aprobación` | **Adoptar** (tabla de correspondencias). Se puede usar tal cual como norma de transporte entre el plano de experiencia y el plano de generación |
| A2A v1.0 | Protocolo de tareas entre agentes opacos. `AgentCard`, estados de tarea `TASK_STATE_SUBMITTED / WORKING / INPUT_REQUIRED / AUTH_REQUIRED / COMPLETED / FAILED / CANCELED / REJECTED` | https://a2a-protocol.org/latest/specification/ · https://github.com/a2aproject/A2A | Apache-2.0 | 5.3 `JobOrchestrator`, 2.8 ciclo de vida | **Referencia**. Candidato a adaptador cuando los trabajos de fusión y promoción del servidor se encarguen a agentes externos |
| Convenciones GenAI de OpenTelemetry | `gen_ai.operation.name` (`invoke_agent`, `execute_tool`, `create_agent`, `invoke_workflow`), `gen_ai.agent.id`, `gen_ai.usage.input_tokens`, `output_tokens`, `gen_ai.tool.name`, atributo MCP `mcp.method.name`. **Estado Development** | https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/ | Apache-2.0 | 5.11 telemetría | **Adoptar** (solo los nombres de atributos). Como no es una versión estable, hay que fijar la versión |
| Trazas de OpenAI Agents SDK | trace (`workflow_name`, `trace_id`, `group_id`), span (`agent`, `generation`, `function`, `guardrail`, `handoff`, `custom`), `trace_include_sensitive_data` | https://openai.github.io/openai-agents-python/tracing/ · https://github.com/openai/openai-agents-python | MIT | 5.11, 7.5 regla de desclasificación | **Referencia**. Incluir datos sensibles por defecto (True) es lo contrario del valor por defecto de esta especificación |
| Hooks de Claude Code | 32 eventos, 5 tipos de manejador (`command`, `http`, `mcp_tool`, `prompt`, `agent`), `permissionDecision` de `PreToolUse` (`allow`, `deny`, `ask`, `defer`) y `updatedInput`, ajuste gestionado `allowManagedHooksOnly` | https://code.claude.com/docs/en/hooks.md | Documentación de producto | Tabla de correspondencias de 5.6 | Ya citado. Se pueden añadir a la tabla `PostToolUseFailure` (E5) y `Elicitation` (E6) |
| Plugins de Claude Code | `.claude-plugin/plugin.json` (solo `name` obligatorio; `skills`, `hooks`, `mcpServers`, `sensitive` de `userConfig`), `claude plugin validate` | https://code.claude.com/docs/en/plugins-reference | Documentación de producto | 5.6 distribución del harness, 8.10 `sub` | Ya citado. **El enlace de references.md es la edición en español (`/docs/es/`), así que se sustituye por la referencia en inglés** |
| Especificación Agent Skills | Cabecera de `SKILL.md`: `name` (64 caracteres), `description` (1024 caracteres), `license`, `compatibility`, `metadata`, `allowed-tools` (**Experimental**) | https://agentskills.io/specification · https://github.com/agentskills/agentskills | Apache-2.0 | 5.6 "las skills son procedimiento, el harness impone" | **Adoptar**. El fundamento actual es una fuente secundaria (Shiplight), así que se sustituye por la especificación primaria. El contenido de la afirmación coincide con la fuente primaria |

### 1.4 Motores de políticas y defensa contra inyección de prompts

| Elemento | Qué es | Fuente primaria | Licencia | Correspondencia | Veredicto |
| --- | --- | --- | --- | --- | --- |
| Cedar | Petición de sujeto, acción, recurso y contexto. **forbid gana a permit, y si no hay ningún permit que coincida, Deny**. La respuesta incluye los id de las políticas que produjeron la decisión (determining policies) y la lista de errores. Las políticas con error se saltan | https://docs.cedarpolicy.com/auth/authorization.html · https://github.com/cedar-policy/cedar | Apache-2.0 | 4.8 `decide(req)`, `PolicyDecisionPoint` | **Adoptar** (adaptador PDP) |
| Cedar SymCC | Traduce el conjunto de políticas a SMT y verifica, con contraejemplos, **inclusión (`check_implies`), equivalencia, denegación siempre y ausencia de errores**. El verificador está verificado formalmente en Lean | https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc | Apache-2.0 | **I5 `p_child ⊑ p_parent`** | **Adoptar**. Eleva I5 de "verificación en el almacén de políticas" a una verificación demostrable |
| OPA / Rego | Proyecto graduado de la CNCF. El registro de decisiones tiene `decision_id`, `bundles.revision`, `path`, `input`, `result`, `erased` y `masked` (JSON Pointer), `trace_id` y `span_id` | https://www.openpolicyagent.org/docs/management-decision-logs · https://github.com/open-policy-agent/opa | Apache-2.0 | 5.11, 7.9 seudonimización | **Adoptar** (nombres de campos del registro de decisiones). Como lenguaje de políticas es menos analizable que Cedar, así que no es la primera opción de PDP |
| CaMeL (DeepMind 2025) | Ya citado. Código publicado | https://github.com/google-research/camel-prompt-injection | Apache-2.0 | 7.4 | Se mantiene. Se añade el enlace al código |
| FIDES (Microsoft 2025) | El planificador sigue **etiquetas de confidencialidad e integridad** mediante rastreo dinámico de contaminación e impone la política de forma determinista. Propone operaciones básicas para ocultar información de forma selectiva | https://arxiv.org/abs/2505.23643 · https://github.com/microsoft/fides | Notebooks MIT | **7.5 etiquetas de flujo de información** | **Adoptar**. 7.5 solo tiene confidencialidad (V0~V3) y carece de eje de integridad |
| Patrón Dual LLM (Willison 2023) | Un LLM privilegiado y un LLM en cuarentena, con un controlador que no es LLM entre ambos. Los valores no confiables solo se pasan como referencias del tipo `$VAR1` | https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | Blog | 7.3 lector aislado | **Adoptar** (cita). 7.4 lo cita indirectamente a través del artículo de patrones de diseño |
| Tríada letal (Willison 2025) | Ya citado | | | 7.3 | Se mantiene |

### 1.5 Fusión y linaje

| Elemento | Qué es | Fuente primaria | Licencia | Correspondencia | Veredicto |
| --- | --- | --- | --- | --- | --- |
| JSON Merge Patch (RFC 7396) | Las claves de objeto se sobrescriben, `null` elimina y **los arrays se reemplazan enteros** | https://www.rfc-editor.org/rfc/rfc7396 | IETF Trust | **2.3 `⊕`**, 6.6 R2 | **Adoptar**. La "sobrescritura por clave" de `⊕` tiene exactamente este significado, pero no tiene nombre |
| JSON Patch (RFC 6902) | Lista de operaciones (add, remove, replace, move, copy, test) | https://www.rfc-editor.org/rfc/rfc6902 | IETF Trust | 8.5 vista previa parcial, `STATE_DELTA` de AG-UI | **Referencia** |
| Kubernetes Server-Side Apply | Los gestores de campos registran la propiedad de los campos (`managedFields`). Con los marcadores de esquema `x-kubernetes-list-type: atomic / set / map`, `x-kubernetes-list-map-keys` y `x-kubernetes-map-type: atomic / granular`, **el esquema declara** el modo de fusión. Cambiar un campo propiedad de otro gestor provoca un conflicto | https://kubernetes.io/docs/reference/using-api/server-side-apply/ | Documentación | **6.6 R2** "el esquema declara la regla", 6.11 `Overrides:` | **Adoptar**. R2 solo lo dice de palabra y no tiene campo de esquema |
| Kustomize | base, overlay y component. Un component es un paquete reutilizable de funcionalidades que se mezcla en varios overlays. `patches` admite strategic merge y JSON 6902 | https://kubectl.docs.kubernetes.io/guides/config_management/components/ · https://github.com/kubernetes-sigs/kustomize | Apache-2.0 | 6.2 lineage, 6.9 compartición por funcionalidad | **Referencia**. Precedente práctico de "overlays sobre una línea base" |
| Automerge | CRDT. Ante escrituras simultáneas en la misma clave elige un ganador determinista por id de operación, pero **conserva los valores perdedores con `getConflicts()`** | https://automerge.org/docs/reference/documents/conflicts/ · https://github.com/automerge/automerge | MIT | 6.13 conflictos semánticos en CRDT | **Referencia**. El enlace actual de 3.2 A6 es la página de listado de Ink & Switch, así que se cambia por Automerge |
| Yjs | Tipos compartidos CRDT | https://yjs.dev/ · https://github.com/yjs/yjs | MIT | 3.2 A6 `crdt` | **Referencia** |
| Mergiraf | Controlador de fusión con reconocimiento sintáctico basado en tree-sitter | https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf | **GPL-3.0-only** (`Cargo.toml`) | 6.6 R1 | Ya citado. Se cambia el enlace de docs.rs al sitio oficial y se indica la licencia. Es el destinatario real de la advertencia de "copyleft fuerte" de 6.6 |

### 1.6 UI generativa

| Elemento | Qué es | Fuente primaria | Licencia | Correspondencia | Veredicto |
| --- | --- | --- | --- | --- | --- |
| A2UI v0.9.1 | UI declarativa en JSON. Cuatro tipos de mensaje: `createSurface`, `updateComponents`, `updateDataModel`, `deleteSurface`. Cada superficie fija un **`catalogId`** (cadena con formato URI). Solo renderiza componentes de catálogos aprobados | https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md | Apache-2.0 | 2.6 D3, `capability-map` `catalog`, 8.5 | **Adoptar**. El fundamento actual es un artículo de prensa (The Decoder), así que se sustituye por la fuente primaria |
| json-render (Vercel Labs) | La IA genera UI solo dentro de un catálogo (props de componentes definidas con zod). Renderizado progresivo | https://json-render.dev/ · https://github.com/vercel-labs/json-render | Apache-2.0 | 2.6 D3, `capability-map` `catalog.props_schema` | **Referencia**. Mismo diseño: catálogo = lista de aprobados |

### 1.7 Cadena de suministro

| Elemento | Qué es | Fuente primaria | Licencia | Correspondencia | Veredicto |
| --- | --- | --- | --- | --- | --- |
| in-toto Attestation | Marco de declaración firmada (Statement) compuesto por el digest del sujeto + un tipo de predicado | https://github.com/in-toto/attestation | Apache-2.0 | 7.7 "firma de procedencia del publicador" | **Adoptar** (especificación de formato) |
| SLSA Provenance v1 | `predicateType: https://slsa.dev/provenance/v1`. `buildDefinition` (`buildType`, `externalParameters`, `resolvedDependencies`), `runDetails.builder.id` | https://slsa.dev/spec/v1.1/provenance | Community Specification License 1.0 | 7.7, `change-record` `provenance` | **Adoptar**. Si se considera el harness como builder, se obtiene una prueba de procedencia de las funcionalidades compartidas |

## 2. Tabla de huecos — lo que falta en la especificación y ya resolvieron los antecedentes

| # | Concepto ausente | Especificación actual | Solución de los antecedentes | Incorporación |
| --- | --- | --- | --- | --- |
| P1 | Significado exacto de la composición de capas declarativas | 2.3 solo dice "si es la misma clave, la capa posterior sobrescribe". Significado de arrays y eliminación sin definir | RFC 7396: `null` elimina, los arrays se reemplazan enteros | E-3 |
| P2 | Reglas de fusión declaradas por el esquema | 6.6 R2 solo dice "el esquema declara la regla" y no hay campo | SSA `list-type: map` + `list-map-keys`, `map-type: atomic/granular` | E-4 |
| P3 | Etiqueta de integridad | 7.5 solo tiene confidencialidad V0~V3 | FIDES, CaMeL: rastreo de integridad para que los valores no confiables no influyan en la elección de acciones | E-1 |
| P4 | Verificación mecánica de la reducción monótona de políticas | Punto de aplicación de I5: "verificación en el almacén de políticas" (sin método) | Cedar SymCC `check_implies`, `check_never_errors` | E-2 |
| P5 | Registro estándar del fundamento de la decisión | 4.8 "motivo=(k, capa que fijó el techo)" | Determining policies de Cedar, registro de decisiones de OPA `decision_id`, `bundles.revision`, `erased`, `masked` | E-2, E-5 |
| P6 | Vocabulario común de telemetría | 5.11 usa nombres propios como `tokens_in` y `tokens_out` | OTel `gen_ai.usage.input_tokens`, etc., MCP `_meta.traceparent` | E-5 |
| P7 | Norma de transporte del plano de experiencia | 5.6 solo tiene los eventos del lado del harness. No dice por qué medio recibe el plano de experiencia el progreso y la espera de aprobación | Eventos e interrupt de AG-UI, `INPUT_REQUIRED` de A2A, MRTR de MCP | E-6 |
| P8 | Ruta de entrada de secretos | 8.10 solo dice "las claves en un almacén seguro". Sin definir el caso en que se reciben por la ruta de conversación del agente | Elicitation en modo URL de MCP (MUST) | E-7 |
| P9 | Identificación y versión del catálogo D3 | `capability-map.catalog` solo tiene una lista, sin id ni versión | `catalogId` de A2UI | E-8 |
| P10 | Capacidad ↔ pistas de herramientas del agente | Solo `capability.risk` | MCP `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` | E-9 |
| P11 | Formato de prueba de procedencia de lo compartido | 7.7 "firma de procedencia del publicador" (sin formato), `content_hash` del manifiesto | in-toto Statement + SLSA provenance | E-10 |
| P12 | Motivo del permiso de red | Solo la lista `network.allow` | `networkAccess.reasoning` de Figma | Sección 4 (en espera) |

## 3. Lista de ediciones propuestas (por prioridad, máximo 12)

Cada elemento es una edición mínima. Todos los elementos de esquema son **adiciones de campos opcionales**, así que `required` no cambia y lo normal es que los `examples/*.yaml` existentes sigan pasando tal cual. Después de incorporarlos hay que volver a ejecutar la validación de los ejemplos.

### E-1. Añadir a 7.5 el eje de integridad (P3)

- Archivo: `docs/07-trust-and-security.md`, el bloque de código `etiqueta λ = (ámbito, nivel)` de 7.5 y el párrafo de ejemplo que hay debajo
- Texto propuesto (sustituye el bloque de código):

```text
etiqueta λ = (ámbito, nivel, integridad)
  ámbito     : identificador de inquilino / organización / usuario
  nivel      : V0 agregados < V1 metadatos < V2 descripción < V3 código          # confidencialidad
  integridad : trusted (intención humana, línea base verificada) > untrusted (elementos compartidos, documentos externos, valores que creó un modelo tras ver entradas no confiables)

regla de derivación:  λ(f(x, y)) = λ(x) ⊔ λ(y)          # confidencialidad: la más sensible; integridad: la más baja
regla de lectura:     quien mira s puede ver x  ⇔  λ(x) ⊑ permisos(s)
regla de acción:      los valores que deciden un aumento de permisos, un envío externo o la elección de un punto de extensión deben tener integridad trusted
regla de liberación:  solo la puerta de salida (desclasificador, declassifier) puede rebajar una etiqueta, y deja reglas y registro
```

- Frase a añadir: `El eje de integridad sigue el método de FIDES (Costa et al., 2025), que rastrea juntas las etiquetas de confidencialidad e integridad en el nivel del planificador y aplica las políticas de forma determinista. Es el "planificar y luego ejecutar" de 7.4 escrito como reglas de etiquetas.`
- references.md (al final de «## Seguridad de agentes»):

```markdown
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · Notebooks (MIT): https://github.com/microsoft/fides
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
```

### E-2. Añadir a 4.8 el adaptador PDP y la verificación mecánica de I5 (P4, P5)

- Archivo: `docs/04-control-spectrum.md`, al final de la lista «Principios de ubicación» de 4.8
- Texto propuesto:

```markdown
- **Adaptador de motor de políticas** (PUEDE (MAY)): se puede implementar el PDP trasladando los intervalos de las perillas (knob) a un lenguaje de políticas. En Cedar, forbid gana a permit, se deniega si no hay ningún permit que coincida, y se devuelve junto con la decisión el id de la política que la produjo. Este id se usa como fundamento de `deny(reason·layer)` y del recibo (8.6).
- **Verificación mecánica de I5** (DEBERÍA (SHOULD)): al guardar una política se comprueba `p_child ⊑ p_parent`. Si se ha trasladado a Cedar, se puede demostrar con un contraejemplo mediante la comprobación de inclusión de SymCC (`check_implies`). Se ejecuta también `check_never_errors` de la misma herramienta, porque Cedar omite las políticas que producen errores de evaluación, de modo que un forbid que falla queda abierto en silencio.
- **El piso va antes que el motor**: por la regla de prioridad de forbid, si los derechos mínimos (F1~F7) se meten como permit normales, un forbid superior puede borrarlos. Como en el pseudocódigo anterior, el juicio de `FLOOR_ACTIONS` se coloca antes de llamar al motor.
```

- references.md (nueva sección «## Motores de políticas», antes de «## Fusión»):

```markdown
## Motores de políticas

- Semántica de autorización de Cedar (prioridad de forbid, denegación por defecto, diagnóstico de políticas determinantes). https://docs.cedarpolicy.com/auth/authorization.html · Código (Apache-2.0): https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler (SymCC): verificación de inclusión, equivalencia y ausencia de errores de políticas. https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Registro de decisiones de Open Policy Agent. https://www.openpolicyagent.org/docs/management-decision-logs
```

### E-3. Fijar el significado por defecto de `⊕` de 2.3 en RFC 7396 (P1)

- Archivo: `docs/02-core-model.md`, el elemento `⊕` de 2.3
- Actual: `` `⊕` (composición de capas): si dos capas tocan la misma clave, la capa posterior **sobrescribe (override)** a la anterior. Los datos declarativos se componen por clave, y las extensiones de código por slot del punto de extensión. ``
- Propuesta: `` `⊕` (composición de capas): si dos capas tocan la misma clave, la capa posterior **sobrescribe (override)** a la anterior. El significado por defecto de los datos declarativos es JSON Merge Patch (RFC 7396). Los objetos se sobrescriben por clave, `null` elimina esa clave y los arrays se sustituyen enteros. Para combinar los arrays elemento a elemento, el esquema del punto de extensión debe declarar una clave de fusión (6.6 R2). Las extensiones de código se componen por slot del punto de extensión. ``
- Observación: para cumplir el requisito de asociatividad de la línea siguiente ("combinar la línea base de antemano y guardarla en caché"), al combinar capas de antemano no hay que borrar los `null` (marcadores de eliminación), sino conservarlos. Solo así aplicar después la capa combinada da el mismo resultado que aplicarlas una a una. Verificarlo con un ejemplo pequeño antes de incorporarlo.
- references.md («## Fusión»):

```markdown
- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
```

### E-4. Añadir a los puntos de extensión de `capability-map` un campo de reglas de fusión (P2)

- Archivo: `schemas/capability-map.schema.json`, en `$defs.extensionPoint.properties`, después de `output_schema`
- Campo propuesto:

```json
"merge": {
  "type": "object",
  "description": "Regla para combinar entre capas los productos declarativos de este punto (especificación 2.3, 6.6 R2). Las claves son JSON Pointer dentro del producto. Los arrays sin declaración son atomic",
  "propertyNames": { "pattern": "^(/[^/]*)*$" },
  "additionalProperties": {
    "type": "object",
    "required": ["strategy"],
    "additionalProperties": false,
    "properties": {
      "strategy": { "type": "string", "enum": ["atomic", "set", "map"] },
      "keys": { "type": "array", "items": { "type": "string" }, "minItems": 1, "description": "Nombres de campo que identifican los elementos cuando strategy=map" }
    }
  }
}
```

- Texto a añadir después de la celda "Ejemplo" de la fila R2 de la tabla de 6.6: `(campo de esquema: extension_points[].merge de capability-map. Los nombres de valor siguen x-kubernetes-list-type de Kubernetes Server-Side Apply)`
- references.md («## Fusión»):

```markdown
- Kubernetes. *Server-Side Apply* (propiedad de campos, marcadores de fusión `x-kubernetes-list-type`·`x-kubernetes-list-map-keys`). https://kubernetes.io/docs/reference/using-api/server-side-apply/
```

### E-5. Alinear los nombres de telemetría de 5.11 con OTel GenAI y OPA (P5, P6)

- Archivo: `docs/05-reference-architecture.md`, el ejemplo JSON de 5.11 y el párrafo que hay debajo
- Propuesta: sustituir `"model_cost"` del JSON por lo siguiente y añadir la clave `"policy"`.

```json
  "gen_ai": {"operation.name": "invoke_agent", "agent.id": "builder@harness-x", "usage.input_tokens": 18200, "usage.output_tokens": 2100},
  "model_cost": {"unit_cost_ref": "route:standard"},
  "policy": {"decision_id": "dec_7Q2…", "revision": "tenant/acme@42"},
  "trace": {"traceparent": "00-…-…-01"},
```

- Frase a añadir: `Los atributos de uso del modelo siguen los nombres de las convenciones semánticas GenAI de OpenTelemetry. Como estas convenciones siguen en estado Development, la implementación registra también la versión de las convenciones que sigue. Las decisiones de política dejan, como el registro de decisiones de OPA, el id de decisión y la revisión de la política (revision), y los campos borrados por seudonimización se indican como una lista de JSON Pointer (7.9). Las llamadas que pasan por un servidor MCP se vinculan a la misma traza con la convención traceparent de `_meta` de MCP.`
- references.md (nueva sección «## Observabilidad», antes de «## Diseño de la experiencia»):

```markdown
## Observabilidad

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/
```

### E-6. Añadir a 5.6 una tabla de correspondencias de transporte del plano de experiencia (P7)

- Archivo: `docs/05-reference-architecture.md`, después de la tabla «### Ejemplo de correspondencia: hooks de Claude Code» y antes del párrafo «Atención:»
- Texto propuesto:

```markdown
El plano de experiencia no recibe los eventos del harness tal cual, sino como señales de progreso para el usuario. Si se usa AG-UI como norma de transporte, la correspondencia es la siguiente.

| Mallangable | AG-UI | Observaciones |
| --- | --- | --- |
| E2 recepción ~ E11 finalización | `RUN_STARTED` · `RUN_FINISHED` · `RUN_ERROR` | |
| Las 4 palabras de estado (8.5) | `STEP_STARTED` · `STEP_FINISHED` | El nombre del step se fija al id de la palabra de estado |
| Vista previa parcial (8.5) | `STATE_SNAPSHOT` · `STATE_DELTA` (RFC 6902) | Se mantiene la indicación "aún sin verificar" |
| E6 `permission.request`, `pendiente de aprobación` de 2.8 | `outcome.type = "interrupt"` de `RUN_FINISHED` → `resume[]` de la siguiente ejecución | La aprobación continúa como una nueva ejecución |

Cuando los trabajos del servidor se encargan a agentes externos, ocupan ese mismo lugar los estados de tarea de A2A (`TASK_STATE_INPUT_REQUIRED`·`TASK_STATE_AUTH_REQUIRED`), y dentro de las herramientas MCP, las peticiones de múltiples idas y vueltas (`resultType: "input_required"`). A la tabla de correspondencias de Claude Code también se pueden añadir `PostToolUseFailure` (E5) y `Elicitation` (E6).
```

- references.md («## UI generativa y estándares de extensión»):

```markdown
- AG-UI: Agent-User Interaction Protocol (eventos, interrupt). MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
```

### E-7. Añadir a 8.10 la regla de entrada de secretos por la ruta MCP (P8)

- Archivo: `docs/08-experience-design.md`, después del primer elemento de «### Seguridad e indicación de costes» de 8.10
- Texto propuesto:

```markdown
- Cuando se funciona como herramienta MCP dentro de un asistente oficial, como en la ruta `sub`, las claves de conexión o los tokens de servicios externos no se reciben por la conversación ni por entradas en modo form. La especificación MCP exige usar elicitation en modo URL para secretos y credenciales (versión 2026-07-28). I6 solo se cumple si la clave no entra ni una sola vez en el contexto del agente.
- En esa misma versión, MCP Sampling está en vías de retirada. No se construye el adaptador `ModelPort` delegando las llamadas al modelo en el cliente MCP.
```

- references.md («## UI generativa y estándares de extensión»):

```markdown
- Especificación de Model Context Protocol 2026-07-28 (cambios, annotations de herramientas, elicitation). https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
```

### E-8. Añadir a `capability-map` el id y la versión del catálogo (P9)

- Archivo: `schemas/capability-map.schema.json`, en las `properties` de nivel superior, antes de `catalog`
- Campo propuesto:

```json
"catalog_id": {
  "type": "string",
  "description": "Identificador del catálogo D3. Es una cadena con formato URI y no necesita poder descargarse. Si cambia el contenido del catálogo, también cambia el valor (mismo significado que catalogId de A2UI)",
  "examples": ["https://todo.example/catalogs/v3"]
}
```

- Dónde añadir también: en `artifact.properties` de `schemas/extension-manifest.schema.json`, `"catalog_id": { "type": "string", "description": "Catálogo que presupone el producto D3. Si difiere del catalog_id del mapa de capacidades, se rechaza en G1" }`
- references.md: sustituir la línea `Google A2UI: cobertura de prensa. The Decoder.` de «## UI generativa y estándares de extensión» por la siguiente.

```markdown
- A2UI: especificación Agent-to-User Interface v0.9.1 (`createSurface`·`catalogId`). Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
```

### E-9. Correspondencia entre las capacidades de `capability-map` y las pistas de herramientas MCP (P10)

- Archivo: `schemas/capability-map.schema.json`, la `description` de `$defs.capability.properties.risk`
- Actual: `"egress=envío externo, sensitive=datos de terceros o sensibles"`
- Propuesta: `"egress=envío externo, sensitive=datos de terceros o sensibles. Al exponer una capacidad como herramienta MCP, read se exporta como readOnlyHint=true y egress como openWorldHint=true. No se confía en las annotations MCP del lado receptor; este valor es el que tiene autoridad (I8)"`
- Añadir un campo opcional: `"destructive": { "type": "boolean", "description": "Escritura irreversible. Mismo significado que destructiveHint de MCP. Si es true, G5 con independencia de la política de activación" }`
- Añadir a la celda "Contenido" de la fila G5 de 5.8 `· al usar capacidades de escritura irreversible (destructive)`.
- references.md: en el elemento de la especificación MCP de E-7, anotar también `https://modelcontextprotocol.io/specification/2026-07-28/server/tools`.

### E-10. Especificar en 7.7 Cadena de suministro el formato de la prueba de procedencia (P11)

- Archivo: `docs/07-trust-and-security.md`, celda "Control" de la fila `Una sola cuenta subía en masa` de la tabla de controles de 7.7
- Actual: `Firma de procedencia del publicador, límites para publicadores nuevos, niveles de curación`
- Propuesta: `Firma de procedencia del publicador (predicado SLSA provenance en un Statement de in-toto. El sujeto es el content_hash del manifiesto y builder.id es el id del harness), límites para publicadores nuevos, niveles de curación`
- references.md (al final de «## Seguridad de agentes» o en una nueva sección «## Cadena de suministro»):

```markdown
- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance
```

### E-11. Reforzar los precedentes de medios maleables en el trabajo relacionado de 1.5

- Archivo: `docs/01-introduction.md`, después de la primera fila (Malleable software) de la tabla de 1.5
- Fila propuesta:

```markdown
| Medios computacionales y documentos dinámicos (Boxer, 1986 · [Webstrates](https://webstrates.net/), 2015 · [Potluck](https://www.inkandswitch.com/potluck/), 2022 · [Embark](https://www.inkandswitch.com/embark/), 2023) | Eliminan la frontera entre documento y aplicación, y el usuario superpone cálculos | Capas superpuestas que no tocan el original (2.3), herramientas que van más allá de la aplicación (O8) | Definido sobre aplicaciones comerciales existentes, con una estructura que resiste las actualizaciones del proveedor |
```

- En la misma tabla, cambiar el enlace de la fila Local-first por `https://www.inkandswitch.com/project/patchwork/` y añadir a la celda "Lo que se tomó" `· las ediciones de IA se dejan en una rama y una persona elige qué fusionar (nota de experimento de Patchwork)`.
- references.md («## Software maleable y programación por el usuario final»):

```markdown
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · Código (Apache-2.0): https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck: Dynamic documents as personal software.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark: Dynamic documents for making plans.* 2023. https://www.inkandswitch.com/embark/
- Ink & Switch. *Patchwork* (nota de experimento 07 "AI bots in version control"). https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
```

- Observación: los subtítulos de Potluck y Embark deben cotejarse una vez más con el original antes de copiar literalmente el título de la página (se leyeron con una herramienta de resumen).

### E-12. Sustituir en references.md las fuentes secundarias por fuentes primarias

- Archivo: `docs/references.md`
- Líneas a cambiar:

| Actual | Sustitución |
| --- | --- |
| `Resumen del estándar Agent Skills. Shiplight, 2026. https://www.shiplight.ai/blog/agent-skills` | `Especificación Agent Skills (cabecera de SKILL.md; allowed-tools es Experimental). Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills` |
| `Visión general de los plugins de Claude Code. https://code.claude.com/docs/es/plugins/overview` | `Referencia del manifiesto de plugins de Claude Code. https://code.claude.com/docs/en/plugins-reference` |
| `Mergiraf: controlador de fusión de Git con reconocimiento sintáctico. https://docs.rs/crate/mergiraf/latest` | `Mergiraf: controlador de fusión de Git con reconocimiento sintáctico. GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf` |
| `SEP-1865. *MCP Apps …* https://modelcontextprotocol.io/seps/1865-…` | Se deja tal cual y se añade al final ` · especificación (2026-01-26): https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx` |
| Elemento de CaMeL | Se añade al final ` · código (Apache-2.0): https://github.com/google-research/camel-prompt-injection` |

- También se cambian los enlaces del texto: `[Shiplight, 2026]` de 5.6 → `[especificación Agent Skills](https://agentskills.io/specification)`, los enlaces de A2UI y Agent Skills de 1.5, el enlace de Automerge de 3.2 A6 → `https://automerge.org/docs/reference/documents/conflicts/`, y el enlace de Mergiraf de 6.6 R1 → `https://mergiraf.org/`.
- Se actualiza la `fecha de verificación` a la fecha de incorporación.

## 4. Lo que no se incluyó

- **Un campo de motivo del permiso al estilo `networkAccess.reasoning` de Figma (P12)**: tiene utilidad, pero hoy quien escribe `network.allow` no es una persona sino el agente generador. Un motivo escrito por el agente no puede servir de fundamento para la tarjeta de aprobación. Se revisará al diseñar la tarjeta de aprobación (G5).
- **Alinear los nombres de campo con WIT y Extism**: los mismos conceptos ya existen en el manifiesto, y sería una alineación para un único formato de producto (`wasm`). Al escribir la documentación del adaptador `lang` de D4 basta con una tabla de correspondencias.
- **Eventos de activación de VS Code**: la carga diferida es un problema de implementación del runtime y no tiene relación con los contratos ni con la fusión. El presupuesto de tiempo de arranque de G3 cumple el mismo propósito.
- **`optional_permissions` al estilo de Chrome**: "pedir cuando haga falta" ya se expresa con el flujo de aprobación humana de I4 (E6). Añadir otra declaración estática haría que las dos rutas divergieran.
- **OPA como PDP por defecto**: se toma el formato del registro de decisiones, pero Cedar, que permite la verificación de inclusión de I5, encaja mejor con el requisito de monotonía de esta especificación.
- **Alinear MCP-UI y Yjs por separado**: basta con citar MCP Apps y Automerge, respectivamente.
- **Linaje de Smalltalk**: no se buscó la fuente primaria. Para citarlo hay que verificar el artículo original.
