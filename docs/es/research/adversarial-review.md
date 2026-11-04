<!-- LANG-BAR -->
[English](../../en/research/adversarial-review.md) · [한국어](../../ko/research/adversarial-review.md) · [简体中文](../../zh-CN/research/adversarial-review.md) · [日本語](../../ja/research/adversarial-review.md) · **Español**
<!-- /LANG-BAR -->

# Revisión adversarial — Mallangable-AI v0.1 (2026-10-30)

Objeto de revisión: `README.md`, `docs/01~10`, `docs/glossary.md`, `docs/references.md`, `schemas/*.json`, `examples/*.yaml`, `tools/design_space.py`.
Perspectiva: comité de programa, revisor de seguridad e ingeniero que quiere implementar viendo solo esta especificación. No se modificó ningún archivo salvo este documento.

Entorno de verificación: Python 3 (stdlib), `jsonschema 4.26.0` y `pyyaml 6.0.3` en `/tmp/mreview/venv`. Todos los scripts auxiliares están en `/tmp/mreview/*.py` (fuera del repositorio).

---

## 0. Resumen

Los cálculos numéricos, la aprobación de los esquemas, la tabla de perfiles y la matriz de BM son **todos mecánicamente correctos.** El problema es que esas cifras y esos esquemas no garantizan *lo que afirma* el cuerpo de la especificación. Los defectos más grandes son cinco.

1. Aun con `A5=own`, se entregan al generador (generator) conversacional los artefactos de las capas (layer) superiores. Eso viola de frente I6 y el principio central de 3.2. P2 y P6 caen en este caso.
2. **No hay una representación ejecutable del contrato (contract, κ).** El contrato es el centro del modelo, pero en el esquema solo hay texto libre, y quien escribe el contrato es el propio generador. Por eso I2, I7, I10, G2, B9 y la SBR pierden todos su fundamento.
3. **La definición de conformidad y los perfiles recomendados se contradicen.** El nivel Core exige garantizar "por diseño" I1~I10 (incluido I8). Pero P1 y P5, como reconoce el propio 4.8, no tienen servidor y no pueden garantizar I8.
4. Si se sigue al pie de la letra la definición de profundidad (depth) de 2.6 (D3=declarativo, D4=código en sandbox), se derrumban la cifra principal (70,516) y la calificación de 'recomendado' de 5 de los 7 perfiles.
5. El algoritmo de propagación (propagation, 6.5) y la fusión que preserva contratos (contract-preserving merge, 6.7) no se pueden implementar tal cual. Ignoran las capas intermedias, los trabajos de los hijos de un padre que espera aprobación se detienen, y la monotonía de los contratos choca con "pasarse al método superior".

---

## 1. Hechos verificados mecánicamente

### 1.1 Salida de la calculadora frente a cifras de los documentos — todo coincide

`python3 tools/design_space.py --markdown` (2.6 segundos):

| Elemento | Salida de la herramienta | README | docs/03 | docs/01 |
| --- | ---: | ---: | ---: | ---: |
| Combinaciones brutas | 1,944,000 | ✓ :65 | ✓ :224 | ✓ :40 |
| Pasan L | 193,725 (9.97%) | ✓ :66 | ✓ :225 | — |
| Pasan L+N | 124,102 (6.38%) | ✓ :67 | ✓ :226 | — |
| Recomendadas | 70,516 (3.63%) | ✓ :68 | ✓ :227 | ✓ :40 |
| Familias estructurales | 1,618 | ✓ :69 | ✓ :229 | ✓ :40 |
| Completaciones promedio | 43.58 / 75 (58%) | ✓ :70 | ✓ :230 | — |
| Número de primeras violaciones por regla L1~L11, N1~N5, S1~S7 | (tabla) | — | ✓ :237-247 todas | — |
| Recomendadas por profundidad D1 8,616 / D2 8,616 / D3 37,968 / D4 14,968 / D5 348 | ✓ | — | ✓ :256 | — |
| Distribución de completaciones 72:224, 57:224, 42:322, 28:270, 24:171 | ✓ (60:48, 48:48, 40:48, 38:106, 36:69, 32:88 omitidos con "etc.") | — | ✓ :231 | — |
| "Ninguna familia tiene una completación credits·none (N3)" | 0 familias en ese caso | — | ✓ :231 | — |
| Ω = 5×3×3×4×3×4×4×3×5×5×3 | 1,944,000 | — | ✓ :224 | — |

- `--check all`: P1~P7 todos `clean`, sin violaciones ni advertencias. Coincide con 03:268.
- Ejemplo de `--profile` (README:111): `"result": "logical", "violated": "L1"`. Coincide con README:112.
- Se comparó celda por celda la matriz 7×20 de `--bm` con docs/09:60-79 y todo coincide (`/tmp/mreview/bmdiff.py`).
- Las 20 filas de `--bm-stats` coinciden con docs/09:85-99.
- Los nombres y los valores de los 11 ejes de `examples/profiles.yaml` y `PROFILES` coinciden para todos los P1~P7.

### 1.2 Validación de esquemas

Según `Draft202012Validator.check_schema`, los 5 esquemas son válidos. Los archivos de ejemplo se revisaron completos, con `FormatChecker` activado y todos los documentos múltiples.

```
capability-map.example.yaml[doc 0]      OK
change.example.yaml[doc 0], [doc 1]     OK
extension-manifest.example.yaml[doc 0]  OK
lexicon.ko.yaml[doc 0], [doc 1]         OK
policy.example.yaml[doc 0..2]           OK
```

- `profiles.yaml` no tiene esquema correspondiente, así que solo se compararon sus valores con la herramienta (ver 1.1).
- También se verificaron las referencias entre ejemplos. Los 5 `lexicon_id` de `capability-map` y el `label` del manifiesto están en el paquete de léxico (lexicon pack), y todos los id que sobrescribe el paquete de educación existen en el paquete base. Los `points` y `permissions_delta.add` del ejemplo de cambio (change) también están en capability-map. Ninguna palabra de `basic_forbidden` aparece en las expresiones basic ni en los textos de explicación.

**Pruebas negativas** (`/tmp/mreview/neg.py`). Documentos que la especificación prohíbe pero que el esquema deja pasar.

```
ACCEPTED :: D4 + permissions_delta.add, no G5, no approved_by (I4)
ACCEPTED :: judge_instance == generator_instance (I7)
ACCEPTED :: G4 pass but no judge_instance (I7)
ACCEPTED :: contract = single judge item, deterministic defaulted true (2.5)
ACCEPTED :: D5 record with only G0 (5.8 requires G0-G5)
ACCEPTED :: points with invalid id
ACCEPTED :: intent = 4 spaces (I9)
ACCEPTED :: manifest D3 + form native (2.6 D3=declarativo)
ACCEPTED :: manifest D4 + native (2.6 D4=código en sandbox)
ACCEPTED :: network allow '*' with no egress capability
ACCEPTED :: D4 sandboxed with no state/migrate (5.9)
ACCEPTED :: depth ceiling D9 / default banana
ACCEPTED :: org depth ceiling D5 > tenant D3 (I5 not checkable)
ACCEPTED :: default outside ceiling
rejected :: provenance.at = 'yesterday'
rejected :: floors missing 6 of 7
```

### 1.3 Referencias cruzadas (`/tmp/mreview/xref.py`)

- Enlaces relativos: 0 enlaces rotos.
- Referencias a números de sección (`2.6`, `6.11`, etc.): todas tienen su encabezado correspondiente. Lo único marcado como discrepancia fueron porcentajes (9.97, etc.), así que son falsos positivos.
- Familias de id A1~A11, I1~I10, F1~F7, G0~G5, R0~R5, P1~P7, B1~B20, O1~O13, E1~E16, L1~L11, N1~N5, S1~S7, T0~T4, X1~X6: no hay id fuera de rango ni id definidos pero sin usar (`L0` es un nombre de nodo de mermaid y no cuenta).
- URL que está solo en references.md y que el cuerpo no cita: `https://code.claude.com/docs/es/plugins/overview` (references.md:22).
- URL que el cuerpo cita pero que no está en references.md: ninguna.
- Estado HTTP: 23 de 24 devuelven 200. Solo `thehackernews.com/...341-malicious-clawhub.html` devolvió 403 (bloqueo de bots) y no se pudo verificar.

### 1.4 Verificación de fuentes externas (WebFetch)

| Afirmación (ubicación) | Resultado de la verificación |
| --- | --- |
| Hooks de Claude Code: 30+ eventos, 5 tipos de manejador, bloqueo por administrador, `onFailure:"block"`, `updatedToolOutput`, `PostToolBatch` (05:261-274) | Todo existe. Los eventos son 33. Existe `allowManagedHooksOnly`. `onFailure` solo funciona en hooks command·http de v2.1.295 o superior y **no tiene efecto en `Stop` ni `SubagentStop`** → L-07 |
| CaMeL 77% frente a 84% (07:104) | Coincide (AgentDojo). Al documento le falta el nombre del benchmark |
| Unit 42: inflado de 22MB, análisis de febrero a mayo de 2026, "falta de aislamiento entre skill logic y agent authority" (07:162) | Coincide (2026-06-23) |
| 341 maliciosos, Koi Security (01:17, 07:162) | Se confirmaron 341 y Koi mediante el artículo de Unit 42. **La cifra de 2,857 auditados no se pudo verificar por el 403** |
| Ensayo de Ink & Switch, 2025, "la generación de código por IA no basta por sí sola", MacLean 1990, Nardi & Miller (01:7-9, 01:63) | Coincide (junio de 2025). La metáfora del original es "appliances: built far away, sealed, unchangeable", así que "comprado en la tienda" es una paráfrasis |
| The Register: prohibición del uso por terceros de tokens OAuth de Free·Pro·Max, incluido el Agent SDK (03:135, 08:272, 09:132) | Coincide (revisión del 2026-02-20; la política en sí existe desde 2024-02) |
| Cronología de falcao.org (09:132) | Correcta en general. El artículo sigue el orden: bloqueo del lado del servidor el 9 de enero, formalización el 4 de abril, **créditos del Agent SDK** el 15 de junio (precio de lista, sin traspaso). El documento omite el bloqueo de enero y lo generaliza como "uso programático fuera de Claude Code" |
| MCP Apps: iframe en sandbox obligatorio (03:67) | Coincide como "Mandatory iframe sandboxing". El estado del SEP es Final |
| Shiplight: `allowed-tools` es experimental (05:236) | Coincide (2026-08-10) |

### 1.5 Valores calculados adicionalmente con herramientas (`/tmp/mreview/indep.py`, `alt.py`, `more.py`, `q.py`)

| Cálculo | Resultado |
| --- | --- |
| Número de violaciones **independientes** por regla (sin importar el orden) | L3 518,400 · L5 486,000 · **L1 432,000** · L4 388,800 · L8 364,500 · L10 324,000 · L7 324,000 · L2 259,200 · L11 162,000 · L6 162,000 · L9 121,500 |
| Número de **violaciones únicas** por regla (solo se viola esa regla) | L3 129,150 · L5 116,235 · L7 77,490 · L4 64,575 · **L1 60,750** · L2 39,150 · … |
| Distribución de A2 en las combinaciones D3 recomendadas | sandboxed 21,588 · decl 8,616 · **native 7,764** |
| Número de combinaciones D4+native entre las recomendadas | **4,044** |
| A6 de las 348 combinaciones D5 recomendadas | **Todas snapshot**. De ellas, 104 tienen A8=public (client 32 · server 48 · hybrid 24) |
| Al añadir las reglas `D3⇒decl` y `D4⇒¬native` según la definición de 2.6 | Recomendadas **37,120**, 875 familias. **P1, P2, P5, P6 y P7 quedan descartados como `logical`** |
| Al añadir la regla `A5=own ⇒ A3=server` | 52,264 recomendadas, 1,246 familias. **P2 y P6 quedan descartados** |
| Configuraciones recomendadas que quedan al colapsar los valores que ninguna regla distingue (D1≡D2, V0≡…≡V3, preview≡gated, proposed≡auto) | **8,969** (al colapsar, la clasificación no cambia) |
| Diferencia máxima·mínima del número promedio de completaciones por valor de eje estructural | **A1 23.2** > A3 21.7 > A2 13.6 > A4 13.4 > A8 12.1 > A5 11.5 > A6 11.3 > A7 1.2 |

### 1.6 Robustez de la herramienta

```
--check P9                → KeyError: 'P9' (traceback)
--profile '{bad'          → json.decoder.JSONDecodeError (traceback)
añadir "A12":"x" a --profile → clean sin errores
```

En ningún lugar del repositorio hay un self-check ni un assert para la calculadora.

---

## 2. Hallazgos (por orden de gravedad)

### CRITICAL

| # | Ubicación | Evidencia | Corrección mínima |
| --- | --- | --- | --- |
| C-01 | docs/05:363, docs/05:45, docs/03:83, docs/02:198 (I6), tools/design_space.py:64 | En la tabla de 5.10, la celda "artefactos de capas superiores" del generador es ● `con own/open`. 5.2 sitúa la generación conversacional de hybrid en "el dispositivo". Pero 3.2 A5 dice que "el código que un agente puede leer acaba pudiendo leerlo también quien le habla a ese agente", e I6 exige lo mismo. En resumen, con `own` (ver solo lo propio) el generador conversacional ve el código superior. La herramienta no tiene una restricción como `own ⇒ server` (L10 solo limita la topología (topology)). Si se añade esa regla, **P2 y P6 quedan descartados** (1.5) | Cambiar la celda del generador en 5.10, con `own`, a **"solo tipos·mapa de capacidades (capability map), artefactos —"**. Si no es posible, añadir L12 `A5=own ⇒ A3∈{server}`, o especificar que en hybrid la generación que lee artefactos superiores se fuerza al servidor. Recalcular las calificaciones de P2 y P6 y las cifras de 3.4 |
| C-02 | docs/02:92-108, schemas/change-record.schema.json:81-91, docs/05:286, docs/06:157-167, docs/09:114 | El contrato se define como "`k_i : A → {verdadero, falso}`", pero en el `contractItem` del esquema `given` y `expect` son **texto libre** (p. ej., "primera visualización del panel en menos de 200ms"). No hay campos para la consulta a ejecutar, el fixture ni la fijación del entorno. Además, 5.7 pone como autor del contrato al **generador** ("generar artefacto·contrato"). Así, aunque exista I7 (separación entre generación y juicio), el generador escribe él mismo el criterio de juicio de G2. I2, I10, B9 (venta de garantía de supervivencia) y la SBR dependen todos de esta representación, pero el juicio automático es imposible. Como el valor predeterminado de `deterministic` es `true`, también pasa un contrato de un solo elemento `check: judge` (1.2) | ① Poner en `contractItem`, con `oneOf`, formas ejecutables por máquina como `tree-query{selector, fixture_ref, assert}`, `unit{entry, input, expected}` y `snapshot{env_ref, baseline_ref}`. ② Si `check: judge`, fijar `deterministic: const false` y poner en `contract` `contains: {properties: {check: {enum: [tree-query, unit, snapshot]}}}` para forzar el "≥1 contrato determinista" de 2.5. ③ Añadir a 5.7 **"el borrador del contrato lo escribe el intérprete en la fase de especificación de la tarea, y el generador no puede borrar ni debilitar el contrato"**, para extender el alcance de I7 hasta el contrato |
| C-03 | docs/10:64-65, docs/02:200·204, docs/04:166-167, docs/03:268 | El nivel Core es "garantizar por diseño I1~I10". I8 es "la aplicación final solo en la frontera del operador". Pero 4.8 escribe él mismo que "en el modo personal sin conexión (P1) no hay servidor, por lo que el PDP del dispositivo es el único". Por tanto, **P1 y P5 (A3=client, sin servidor) no cumplen Core por definición.** Aun así, 03:268 los presenta como 'recomendados'. Viendo que Governed vuelve a exigir I8 como "Core + verificación de recepción (receive-check) en servidor (I8)", parece que el autor también pensaba que I8 no estaba en Core. La imposición de aprobación (approval) humana de I4 también se puede eludir en el cliente | Sacar I8 de Core y moverlo a los requisitos de Governed. Corregir la definición de Core a "I1~I7, I9, I10", y corregir también la frase de juicio de conformidad de 2.9:204. Especificar en 3.5 "P1·P5 llegan hasta el nivel Core; Governed no es posible" |

### HIGH

| # | Ubicación | Evidencia | Corrección mínima |
| --- | --- | --- | --- |
| H-01 | docs/02:118-119, docs/07:113, tools/design_space.py:48-53, schemas/extension-manifest.schema.json:63-76, docs/03:272-273 | 2.6 define D3 como "árbol de UI declarativo" y D4 como "código arbitrario dentro de un sandbox". Pero 5 de los 7 perfiles son `A1=D3, A2=sandboxed`. Entre las combinaciones recomendadas también hay 7,764 D3+native y 4,044 D4+native. El esquema del manifiesto también admite D3+native y D4+native (1.2). Si se aplica a D3 la lógica de L3 ("permitir artefactos de código en una profundidad que no necesita código es redundante"), las recomendadas bajan a 37,120 y quedan descartados P1, P2, P5, P6 y P7 (1.5). Por otro lado, 7.6 escribe "marco … panel (D3)" y el `format` del ejemplo de manifiesto tiene `html-panel`. La especificación está dividida consigo misma sobre si D3 admite código | Unificar. (a) Redefinir D3 como "declarativo de catálogo **o** código de panel aislado en marco" y rebajar "análisis previo a la ejecución: la mayoría" de la tabla de 2.6 a "solo declarativo", o (b) ampliar L3 a `A1∈{D1,D2,D3} ⇒ A2=decl` y corregir los perfiles. En cualquier caso, añadir una regla L que bloquee D3/D4+native y una condición `allOf` en el manifiesto |
| H-02 | docs/02:142 (separación de D5 MUST), docs/02:193 (I1), tools/design_space.py:25 | A1=D5 es "el usuario puede cambiar incluso el núcleo". Esto contradice directamente I1 (la capa de usuario no cambia C) y "D5 no es una capa de usuario" de 2.6. Aun así, la herramienta califica como 'recomendadas' 348 combinaciones D5. Todas son snapshot, e incluyen 104 parches nativos del núcleo compartidos públicamente (1.5) | Añadir `N6: A1=D5 ⇒ (A8=none ∧ A6≠snapshot)`, o reducir el dominio de A1 a D1~D4 y mover D5 a un concepto fuera de los ejes llamado 'proceso de fork del núcleo'. Recalcular las cifras de 3.4 y del README |
| H-03 | README:72, docs/03:261, docs/03:233 | Son las afirmaciones "el 90% de las combinaciones brutas … no tiene sentido", "la regla que más filtra es L1" y "significa que es la contradicción de diseño más frecuente". Sin embargo: ① L3 y L5 son reglas de normalización (eliminación de redundancia), no reglas que filtren 'combinaciones sin sentido'. Sus violaciones independientes son L3 518,400 y L5 486,000, más que L1 432,000. ② Que L1 quede primera se debe al orden de conteo de 'primera violación'. Por violaciones únicas, L1 es quinta con 60,750 (1.5). 03:233 advierte directamente de la dependencia del orden y acto seguido la usa para interpretar. ③ El número de combinaciones no es la frecuencia de las necesidades de los diseñadores. Por eso "la contradicción de diseño más frecuente" es una afirmación irrefutable. ④ 70,516 incluye una parte inflada por valores que ninguna regla distingue (V0~V3, etc.); al colapsarlos queda en 8,969 | Corregir la interpretación 1 a "si se excluyen las reglas de normalización (L3, L5) …" y publicar en la tabla también los números de violaciones independientes·únicas. Cambiar "la más frecuente" de README:72 por "representativa". Añadir en 3.4 una nota al pie: "sensible a la resolución de valores; las configuraciones que las reglas distinguen son 8,969" |
| H-04 | docs/06:99-120 | El pseudocódigo de propagación no se puede implementar tal cual. ① `merge(..., theirs=r)` fusiona también en los nodos nietos la **release original r**, así que se pierden los cambios de las capas intermedias (inquilino (tenant), organización). ② `contracts = κ(r) ∪ κ(m)` también omite los contratos de las capas intermedias. ③ Por la condición `where parent(m) has applied r`, si el padre espera aprobación en estado `proposed`, el hijo nunca se procesa en este bucle, y no hay mecanismo para volver a dispararlo. ④ El significado de `return` dentro del cuerpo de `parallel_for` no está definido. ⑤ `canary(descendants_in_topo_order…, ratios)` elige el primer 5% en orden topológico, así que el canario no es una muestra aleatoria sino un bloque de nodos superiores. ⑥ No hay criterio de clasificación de causas para la tasa de fallos de "misma causa". ⑦ "Un trabajo por nodo, cancelar si hay nueva release" produce inanición (starvation) si el ciclo de releases es más corto que el retraso de aprobación | Cambiar a `theirs = parent(m).main@after_apply(r)` y definir los contratos como `⋃_{a ∈ ancestors(m)} κ(a) ∪ κ(m)`. Reescribir de forma dirigida por eventos, de modo que el evento de aplicación del padre (`baseline.applied`) cree el trabajo del hijo, y definir el canario como "muestra aleatoria entre nodos de la misma profundidad". La clave de causa de fallo es `(id de puerta, id de contrato, punto de extensión)`. Añadir una máquina de estados a 6.5 |
| H-05 | docs/02:54·71, docs/06:83-95, docs/06:157-169 | Hay dos modelos de fusión. 2.3 **compone** las capas en tiempo de ejecución **por sobrescritura (⊕)**, y 6.4 trata el repositorio del usuario como **fork** de la línea base (baseline) con **fusión de 3 vías**. Si las capas se componen, el cambio superior debería ser objeto de nueva verificación de contratos y no de fusión; si es un fork, ⊕ no hace falta. El implementador no puede decidir cuál de los dos construir. Además, "el contrato solo puede volverse más fuerte" de 6.7:165 choca con la opción "pasarse al método superior" de 6.7:169 (hay que abandonar el contrato de usuario 'panel de barra lateral') y con la retirada de puntos de 6.12 (κ_down es imposible de satisfacer por principio). Aun así, 8.8 muestra "6 de 7 se trasladaron tal cual" como si fuera el caso general. Tampoco se define dónde se almacena el contrato upstream κ(r) (no hay esquema) | Unificar en 2.3: "el almacenamiento es delta por capa, la composición es ⊕, la fusión solo para modificaciones simultáneas *dentro de la misma capa*". Añadir a la regla 2 de 6.7: "son excepción los casos en que la persona elige en R5 y la migración de contrato (contract migration, rename map) por retirada de punto. Se deja `Contract-Migrated` en el registro". Añadir `baseline-release.schema.json` para contener los contratos de release |
| H-06 | schemas/change-record.schema.json:7·33-46·61-76, schemas/extension-manifest.schema.json:31-41, schemas/policy.schema.json:92-99 | Pasan 14 pruebas negativas (1.2). En concreto: un registro con más permisos pero sin G5 ni `approved_by` (I4), `judge_instance == generator_instance` (I7), G4 en pass pero sin registro de juez (judge), D5 con solo G0 (5.8), una intent (intención) hecha solo de espacios (I9), D3/D4 native, `network.allow:["*"]` sin permiso de egress, `depth.ceiling: D9` y un default fuera del techo (ceiling). Son cosas que el esquema puede bloquear y no bloquea | Corregir solo lo que se puede corregir dentro del esquema. Si `permissions_delta.add` tiene `minItems:1`, hacer `required` `gates.G5 const approved` y `provenance.approved_by` (`if/then`). `validation.gates` con `required` por profundidad. `pattern: "\\S"` en `intent`. En `points.items`, el mismo patrón que capability-map. orderedKnob como `enum` por perilla (knob). En el manifiesto, escribir en la description que si `network.allow` no está vacío se exige permiso de egress en permissions (porque es una verificación entre documentos). Las comparaciones de valores y entre documentos, como el 'ser distintos' de I5 e I7, se trasladan a la **herramienta de verificación de conformidad** y se documenta así |
| H-07 | docs/07:18-28, docs/05:286-288, docs/06:167·196 | Faltan tres casos en el modelo de amenazas. ① **Contaminación de contrato·juez**: un generador que sufrió inyección puede escribir un contrato que deja pasar un comportamiento malicioso, o plantar en el artefacto instrucciones dirigidas al juez ("este panel cumple la intención"). El juez no tiene comunicación externa, pero queda totalmente expuesto a ataques de *integridad*. ② **Contaminación de la caché de resoluciones (resolution cache)**: un usuario malicioso dentro del mismo inquilino puede crear una resolución 'verificada' solo con sus propios contratos, que luego se reutiliza para todo el inquilino a través de R3. La limitación de alcance de 6.8 solo impide filtraciones *entre* inquilinos y no el movimiento lateral *dentro* del inquilino. ③ **Release superior·operador comprometido**: no se tratan la gestión de claves de firma (06:91), la revocación, el alcance del daño con aplicación `auto`, ni el caso en que el operador distribuye un cambio malicioso como línea base oficial | Añadir tres filas a la tabla de atacantes de 7.1. Los controles son, respectivamente: ① el contrato es propiedad del intérprete y la entrada del juez solo se recibe con un esquema fijo (el texto original del artefacto queda fuera del contexto del juez). ② La caché solo se carga después de que la resolución se haya reverificado en k o más nodos distintos del usuario que la creó. ③ Fijar (pin) la clave de firma de releases por PEP, hacer obligatorio el canario también en la aplicación `auto` y dar al inquilino el derecho a rechazar la release superior |
| H-08 | docs/06:273 vs docs/09:116·119 | 6.10 promete: "**no incluimos en la línea base oficial artefactos creados por clientes** … prometer este principio por escrito es la premisa de la confianza de los clientes empresariales". Pero B19 es "promover funcionalidades ampliamente compartidas a extensiones oficiales de pago y repartir ingresos con el autor original", y B10 es "recompensa si se adopta en la línea base de la organización·**oficial**". Dentro de la misma especificación, la promesa y el modelo de negocio (business model) chocan de frente | Corregir la frase de 6.10 a "no se incluyen artefactos de clientes **sin consentimiento**. Lo compartido públicamente (A8=public) solo se promueve con el consentimiento explícito de licencia del autor original", y referenciarlo en la columna de condiciones de B10 y B19 |
| H-09 | docs/02:180-181·187, docs/05:189, docs/05:338 | ① 2.8 escribe "**todo camino hacia activo pasa por la verificación**", pero `en espera --> activo: re-resolución por elección del usuario` de la misma figura no pasa por la verificación. ② El último paso del flujo 1 de 5.4, `E->>S: activate(estado)`, hace que la superficie de experiencia llame directamente al almacén sin pasar por el PDP, E10 `activate.before` ni G5. En este flujo no hay ninguna ruta de aprobación. ③ El paso 1 del intercambio en caliente (hot swap) de 5.9 "pre-monta en una ranura oculta al pasar G2". Código D4 previo a la aprobación (G5) puede recibir permisos y ejecutarse | ① Cambiar a `en espera --> verificando`. ② Insertar en 5.4 el paso `S->>P: decisión de activate` y dibujar la rama G5. ③ Condicionar el montaje en ranura oculta a "después de pasar G5, o solo con 0 permisos" |

### MEDIUM

| # | Ubicación | Evidencia | Corrección mínima |
| --- | --- | --- | --- |
| M-01 | schemas/capability-map.schema.json:5·45-61, docs/02:24-40, docs/06:202-212, docs/05:372-383, docs/06:288 | Hay varios objetos que los documentos definen pero que no tienen esquema: compartición (YAML de 6.9), release de línea base·nodo de linaje (lineage) (6.3), trabajo de propagación, `AccessRequest`·`Decision` (4.8, 5.3), evento de telemetría (JSON de 5.11) y el archivo `contract.yaml` al que se refieren los registros. El esquema de capability-map menciona en su description un "esquema de estado", pero **no tiene un campo Σ.** Los nombres `in/out` de 2.2 también difieren de `input_schema/output_schema` del esquema, y `d_max` y `version`, que están en el esquema, no están en la definición de 2.2. change-record no tiene un campo de estado del ciclo de vida (en espera·reemplazado), y `parent_state` es opcional, por lo que no se puede imponer el 'estado anterior registrado' de I3 | Añadir primero solo dos: `share.schema.json` y `baseline-release.schema.json` (el resto en v0.2). Poner `state_schema` en capability-map y alinear la tupla de 2.2 con los nombres de campo del esquema. Hacer `required` el `provenance.parent_state` de change-record y añadir un enum `status` |
| M-02 | docs/02:147-161, docs/04:14-24·46-64·77-83, schemas/policy.schema.json:55-68·65 | La retícula de políticas (policy) tiene cuatro huecos. ① `valueKnob` (code_visibility, model_route, admin_visibility) no tiene orden, así que no se puede juzgar I5 (`p_child ⊑ p_parent`). ② No se define para quién es el 'riesgo' de cada perilla. La visibilidad de administración es un riesgo para el usuario, pero el techo lo fija el inquilino. Así, si `p_U` participa en la intersección, el usuario puede rebajar la visibilidad del administrador. El preset 'bloqueo' pone la aplicación de la línea base en `auto`, la de mayor riesgo. ③ No hay regla para el caso en que la intersección de intervalos queda vacía (piso (floor) inferior > techo superior). ④ Las perillas que usan los presets, 'generación directa', 'profundidad de instalación', 'aprobador de puerta' (`p.gate_approver`, 04:161) e 'intensidad de verificación', no están en el esquema. Además, F6 ("se detiene al superarlo", DEBE (MUST)) tiene `notify` en el enum `on_exceed`, lo que puede violar el piso | Añadir a la tabla `order` y `risk_bearer` (user/tenant/operator) por perilla, y designar por perilla los actores que participan en la intersección. Si la intersección queda vacía, tratarla como "prioridad superior + evento de auditoría". En el esquema, añadir `create`, `install_depth` y `gate_approver`, y quitar `notify` de `on_exceed` o redefinir `notify` como 'avisar tras detenerse' |
| M-03 | docs/03:202-203, tools/design_space.py:78-81, docs/09:35·44 | N3 (credits ⇒ A10≠none) y N4 (public ⇒ A10≠none) mezclan la **visibilidad del administrador del inquilino** (A10) con la **medición·auditoría del operador** (MeteringPort, 5.3). El cobro por créditos basta con que lo mida el operador, y no tiene que ver con lo que vea el administrador del inquilino. Esta confusión entra en el filtrado de 7,659 de N3 y 6,540 de N4, y en los juicios de B12 y B16 | Tratar la medición del operador como premisa permanente fuera de los ejes y eliminar N3, o crear un eje de 'nivel de auditoría del operador' separado de `A10`. Como mínimo, corregir el texto de justificación de N3 y N4 a "medición del operador" y revisar de nuevo las condiciones |
| M-04 | docs/07:121-131 | En el ⊔ de la etiqueta de flujo de información `λ=(alcance, grado)` no se define cómo se combinan los *alcances* (inquilino A y B, alcances de usuario mezclados por compartición). Los grados V0~V3 reutilizan tal cual los niveles de visibilidad de administración como sensibilidad de datos, así que no se puede determinar en qué grado están los datos de trabajo del usuario (el cuerpo de una tarea pendiente) | Tratar el alcance como conjunto, definir ⊔ como unión y la condición de lectura como 'alcance de quien mira ⊇ λ.alcance'. Añadir a los grados `D` (datos de usuario) como elemento no comparable con V3 |
| M-05 | docs/03:320, docs/03:343-347 | En el diagrama de flujo de 3.6, `público → A4≥frame` contradice a los artefactos declarativos (L5: decl ⇒ A4=none) y a P4 (public, decl, none). Las etiquetas de las flechas del diagrama de evolución de 3.7 también difieren de las diferencias reales entre ejes (diff de 1.5). P3→P7 solo dice "A10 V3", pero en realidad también cambia **A1 D4→D3**. P4→P6 dice "A6 fork", pero P6 es `lineage`, y en realidad cambian 8 ejes (A1~A7, A11). P1→P2 omite A5, A9 y A10, y P2→P3 omite A1, A4, A9 y A11 | Corregir a `V1["si es artefacto de código, A4≥frame …"]`. Sustituir las etiquetas de las flechas por un diff generado con la herramienta, y corregir "A6 fork" de P4→P6 a "A6 lineage" |
| M-06 | docs/03:263 | "**La ubicación del agente es la decisión estructural que más restringe el modelo de negocio**". Según el número promedio de completaciones de la herramienta, el eje estructural con mayor diferencia es A1 (23.2), y A3 es segundo con 21.7 (1.5). A3 queda primero solo cuando se mira A9 (obtención de modelos (model sourcing)) | Acotar el alcance a "la que más restringe la obtención de modelos (A9)" y publicar como justificación la tabla de completaciones promedio por eje |
| M-07 | docs/02:195 (I3), docs/05:119·338-341, schemas/extension-manifest.schema.json:44-51, docs/06:318-323 | I3 dice que revertir es "tiempo constante, sin generación", pero ① revertir una extensión cuyo esquema de estado cambió requiere un traspaso de estado en sentido *inverso*, y `migrate_from` solo expresa el sentido directo. ② En la topología CRDT, revertir no es mover un puntero sino fusionar operaciones inversas. ③ El texto para el usuario (8.7 "al instante, gratis") oculta que revertir no deshace efectos externos (un mensaje de Slack ya enviado) | Corregir I3 a "revertir el **estado de capa** es de tiempo constante. El estado interno de la extensión se reinicia si no hay `migrate_to_prev`, y los efectos externos no se revierten", y añadir `migrate_to` al manifiesto |
| M-08 | docs/10:40-58·62-66, docs/02:204 | ① El denominador de la SBR es solo "fusión automática", así que no se mide el caso en que, en el modo `proposed`, una persona aprueba sin darse cuenta una fusión rota (¡el valor recomendado por defecto de A7!). ② No hay protocolo de reproducibilidad: cómo se crean las pruebas ocultas, semillas y número de repeticiones, fijación de la versión del modelo. ③ No hay un conjunto de pruebas de conformidad para juzgar la "garantía por diseño" (se pospone a v0.3), así que los niveles de conformidad actuales son irrefutables | Cambiar el denominador de la SBR a "fusiones automáticas + fusiones aprobadas por propuesta" e informar de ambas por separado. Añadir a 10.2 elementos de reproducibilidad (k ejecuciones, hash de modelo·prompt). Escribir ya en el documento al menos 3 vectores de prueba por nivel de conformidad (p. ej., rechazar si aumentan los permisos sin aprobación, rechazar si judge==generator, rechazar si el contrato está vacío) |
| M-09 | docs/03:192, tools/design_space.py:62-63 | L9 (`crdt ⇒ A7≠manual`, "CRDT es fusión automática") confunde categorías. A7 es la **propagación de la línea base superior hacia abajo**, y CRDT es la **sincronización entre réplicas**. Un documento CRDT también puede aceptar manualmente una nueva release de la plantilla superior | Eliminar L9, o definir "en crdt, A7 significa la propagación de la plantilla superior" y volver a fijar la condición |
| M-10 | docs/06:208·230, docs/02:118, examples/capability-map.example.yaml:50-55, docs/07:150 | ① En la compartición por suscripción, cada vez que el remitente modifica la funcionalidad se generan trabajos de propagación y costes del lado del receptor. Un atacante de costes (07:28) puede usar esta vía y no hay control. ② Si un componente declarativo D3 (chart, card) renderiza imágenes·URL remotas, eso ya es egress, pero el catálogo y las reglas de G1 no tienen restricciones de red | Añadir a 6.9 "el coste de propagación de subscribe dentro del techo del receptor, limitado a n veces al día". Poner `fetches_remote: boolean` en el esquema del catálogo y hacer que los componentes que traen recursos remotos exijan permiso de egress |
| M-11 | docs/02:199 (I7), docs/04:103 | I7 solo exige "otra instancia". No hay fundamento de que otra instancia con el mismo modelo, el mismo prompt y el mismo contexto reduzca el sesgo de autocalificación. Es una afirmación sin fundamento | Reforzarlo a "otra instancia + no ve el razonamiento ni el historial de conversación del generador + (si es posible) otra ruta de modelo", y poner el efecto en O4 como tarea de medición |
| M-12 | docs/02:54·71 | ⊕ solo define "gana la capa más cercana al usuario". No hay medio (`final`, bloqueo) para impedir que se sobrescriban elementos que el inquilino debe mantener obligatoriamente (avisos normativos, banners de auditoría), así que la capa de usuario puede sobrescribir elementos normativos | Poner `overridable: false` en los elementos del mapa de capacidades o de la línea base y rechazarlo en G0 |
| M-13 | docs/05:310-314, docs/02:106 (2.5), docs/02:194 (I2) | En D1, G2 (ejecución del contrato) es opcional. Por eso el contrato que exige I2 existe, pero puede usarse como fundamento de una fusión (I10) sin haberse ejecutado nunca. La condición de G5 en D2, "si incluye comandos externos", también es más estrecha que "el aumento de permisos requiere aprobación humana **incondicionalmente**" de 7.3 | Hacer G2 obligatorio también en D1, o especificar que antes del juicio de I10 se ejecutan primero los 'contratos nunca ejecutados'. Unificar todas las celdas de G5 de 5.8 a "si aumentan los permisos (I4)" |

### LOW

| # | Ubicación | Evidencia | Corrección mínima |
| --- | --- | --- | --- |
| L-01 | docs/05:194-196 | La secuencia de 5.4 tiene **21 mensajes** (:169-189). El cuerpo hace referencia a "especificación de tarea en el paso 9" (en realidad 7), "G1 en el paso 12" (en realidad 11), "juicio en los pasos 14~15" (en realidad 12~13), "registro en el paso 17" (en realidad 15) y "activación en el paso 22" (no existe; en realidad 21) | Corregir los números a 7·11·12~13·15·21 |
| L-02 | tools/design_space.py:286-321, :9-14 | `--check P9` termina en KeyError, el JSON inválido en traceback, y un eje desconocido (`A12`) se acepta en silencio. El uso del docstring no incluye `--bm` ni `--bm-stats`, y tampoco hay self-check | Poner en `check()` una verificación `extra=[k for k in c if k not in AXES]`. En `--check`, `if a.check not in PROFILES and a.check!="all": ap.error(...)`, y tratar `json.loads` con try/except y luego `ap.error`. Hacer assert de las cifras de 1.1 con `--selftest` |
| L-03 | docs/references.md:22, :40, docs/01:17, docs/07:104, docs/09:132 | `docs/es/plugins/overview` no se cita y es la edición en español. 2,857 no se pudo verificar por el 403 (de Unit 42 solo se confirmó 341). A CaMeL le falta el benchmark (AgentDojo). El resumen de falcao omite el bloqueo del 9 de enero y generaliza los "créditos del Agent SDK" | Eliminar la entrada, o cambiarla a `/en/` y citarla en el cuerpo. Añadir a la cifra de 2,857 el enlace al original de Koi. Añadir "en AgentDojo" y ajustar la frase de 9.6 a la expresión del artículo |
| L-04 | docs/04:131-143 vs examples/policy.example.yaml:23-34 | El extracto de 4.7 usa `net.allowlist` (un permiso que no está en capability-map), pero el archivo de ejemplo usa `net.slack.post`. También faltan `currency` y `retention_days` | Igualar el extracto al archivo de ejemplo |
| L-05 | docs/08:196, docs/glossary.md:20, examples/lexicon.ko.yaml:33-37, README:142 | La tabla de correspondencias de 8.9 dice "profundidad D1~D4", pero el glosario y el developer del paquete de léxico dicen D1~D5, y tampoco existe el concepto `depth_d5` (una petición D5 debería mostrarse al usuario como "petición de funcionalidad del núcleo"). A la lista de notaciones del README le faltan las familias E, O, T y X | Añadir `depth_d5: { basic: petición que cambia la propia aplicación }` y añadir E1~E16, O1~O13, T0~T4, X1~X6 en README:142 |
| L-06 | docs/09:103 | Agrupa B8, B9, B10 y B18 diciendo "solo es posible en aproximadamente la mitad", pero B8 es 26.3% y B10 es 11.0% | Corregir a "B9 y B18 aproximadamente la mitad, B8 una cuarta parte, B10 una décima parte" |
| L-07 | docs/05:271-272, docs/05:253 | `onFailure:"block"` no tiene efecto en `Stop` ni en `SubagentStop` (documentación oficial). Por eso E11 (rechazar la finalización si no está verificado) y E12 funcionan abiertos (fail-open) si falla el hook. También falta el requisito de v2.1.295 o superior | Añadir una nota al pie en la tabla de correspondencias y escribir que E11 y E12 "también se imponen del lado de la herramienta MCP" |

---

## 3. Juicio (opinión no verificada mecánicamente)

- **El peso de la contribución**: las cifras del espacio de diseño (design space) son la aritmética *de haber elegido así las reglas y la resolución de valores*. Las frases que hacen que estas cifras se lean como resultados empíricos ("la mayoría de las combinaciones no tiene sentido", "la contradicción más frecuente", "estructura y negocio están en general separados") son motivo de rechazo en un comité de programa. Es más seguro afirmar las cifras solo como demostración de la coherencia interna del sistema de reglas.
- **El mayor riesgo sin resolver no es O1 sino C-02.** El capítulo 10 trata la suficiencia de los contratos como un problema de 'calidad'. Pero mientras el generador escriba los contratos, es un problema de *seguridad*. Un generador que sufrió inyección escribe un contrato que lo deja pasar.
- **La tensión entre I8 y la 'maleabilidad'**: la honestidad de rebajar la imposición del lado del dispositivo del usuario a nivel orientativo es buena. Pero presentar P1 y P5 como perfiles representativos y prometer a la vez conformidad Core confunde al lector. Separar los niveles (corrección de C-03) es lo honesto.
- **Alcance de los esquemas**: los esquemas solo verifican la 'forma', y las garantías centrales de la especificación (I4, I5, I7, I10) requieren verificaciones entre documentos. Pero no se dice quién hace esa verificación ni dónde (verificación de recepción, herramienta de verificación de conformidad). Bastaría con un pequeño validador de conformidad (conformance validator) en `tools/` antes de v0.2 para que "garantía por diseño" se convierta en una afirmación refutable.
- **B20 (valor predeterminado patrocinado)** daña estructuralmente la neutralidad de las recomendaciones del agente. La sola obligación de señalizarlo no impide que la información de patrocinio que entra en el contexto del modelo incline las recomendaciones. Si se incluye, es más seguro "la información de patrocinio no entra en el contexto del agente y solo se muestra en la UI".
- **La interpretación centrada en D3 (03:262)** no se puede mantener hasta que se resuelva H-01. Como D3 mezcla sandboxed y native, la interpretación "aunque solo se abra hasta la pantalla declarativa" no encaja con los datos.
- **Lo que está bien hecho** (por justicia): la reproducibilidad de las cifras, la aprobación de esquemas y ejemplos, la generación basada en código de los perfiles y de la matriz de BM, 0 enlaces rotos, 23 de 24 fuentes accesibles, la notación "las cifras sin fuente son valores propuestos", la tabla de niveles de garantía de 7.8 y el aviso de los límites del PDP del cliente en 4.8. Para un borrador v0.1, es una estructura verificable poco común.

---

## 4. Comandos de reproducción

```bash
cd mallangable-ai   # raíz del repositorio
python3 tools/design_space.py --markdown
python3 tools/design_space.py --check all
python3 tools/design_space.py --bm
python3 tools/design_space.py --bm-stats
# scripts auxiliares (fuera del repositorio)
python3 -I /tmp/mreview/indep.py     # violaciones independientes·únicas, número de D3/D4 native
python3 -I /tmp/mreview/alt.py       # variante que prohíbe D3/D4 native
python3 -I /tmp/mreview/more.py      # diferencias de completaciones por eje, variantes own⇒server·D3⇒decl, verificación cruzada del paquete de léxico
python3 -I /tmp/mreview/q.py         # cociente de equivalencia de reglas 8,969, distribución de D5
python3 -I /tmp/mreview/bmdiff.py    # contraste de la matriz de BM, diff de perfiles
/tmp/mreview/venv/bin/python -I /tmp/mreview/validate.py   # ejemplos frente a esquemas
/tmp/mreview/venv/bin/python -I /tmp/mreview/neg.py        # pruebas negativas
python3 -I /tmp/mreview/xref.py      # referencias cruzadas de secciones·enlaces·id·URL
```
