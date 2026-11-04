<!-- LANG-BAR -->
[English](../../en/research/security-audit-2026-11-05.md) · [한국어](../../ko/research/security-audit-2026-11-05.md) · [简体中文](../../zh-CN/research/security-audit-2026-11-05.md) · [日本語](../../ja/research/security-audit-2026-11-05.md) · **Español**
<!-- /LANG-BAR -->

# Informe de auditoría de seguridad: 2026-11-05

Herramienta: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) (`.claude/skills/security-audit/`, commit fijado en `UPSTREAM`)

## 1. Alcance de la ejecución

- Perfil: **quick**; es una auditoría parcial. Solo se hizo 1 ronda de búsqueda y 1 crítica final de cobertura, y las 6 unidades que encontró la crítica quedaron como `deferred` (`quick_profile_final_critic`). No se afirma una cobertura completa.
- Objetivo: todo el repositorio, sobre el código fuente `a69ddbf`. Al ser la primera auditoría, no hay resultados previos.
- Presupuesto: no se fijó por separado. Los agentes fueron 11 en total: 1 de reconocimiento, 5 de búsqueda, 4 de verificación y 1 de crítica. Una verificación (`v-propagate`) tenía un resultado con formato incorrecto, así que se descartó y se repitió con un verificador nuevo.
- Límites de ejecución: el código objetivo solo se ejecutó dentro de Docker. Las condiciones fueron `--network none`, objetivo de solo lectura, uid 65534, `cap-drop ALL`, 256 MiB, 60 segundos y `env -i`, y solo se permitió escribir en el scratch de cada agente. Los artefactos se movieron únicamente con el promotor no-follow del lado padre. No se tocaron entornos de despliegue ni servicios externos.

## 2. Resumen

Al ser un repositorio de especificación, no hay servidores en ejecución. Los límites reales son dos: (a) las herramientas de inspección que reciben documentos externos y (b) el pseudocódigo normativo que los implementadores trasladarán tal cual. Los 2 defectos confirmados son ambos low. Se juzgó que 1 defecto necesita más verificación, y la dependencia correspondiente se cerró con una frase de la especificación en esta revisión.

## 3. Defectos confirmados

| Gravedad | Título | Límite | Resultado observado |
| --- | --- | --- | --- |
| low | La excepción de acciones de piso de `decide()` no mira el sujeto ni la dirección | Agente o sujeto de otra capa → transición de estado activo del PDP | Para el mismo estado S1, `activate` se deniega (profundidad) y `revert(target=S1)` se permite [registro] |
| low | `check_schemas.py` imprime tal cual los caracteres de control de las claves de documentos y de los nombres de archivo | Autor de documentos externos → terminal del revisor, registros de CI | 2 bytes ESC en bruto, se genera una línea independiente `::error title=forged::`. El código de salida se mantiene en 1 |

### 3.1 Alcance de la excepción de acciones de piso (`docs/04-control-spectrum.md:153`)

- Sujetos de confianza inferior: agente delegado (susceptible de inyección de prompt), supervisor, usuarios de otras capas.
- Reproducción: se trasladó tal cual el pseudocódigo de 4.8. La política es techo de profundidad D3, permisos `[tasks.read]` y `gated`, y el estado registrado S1 tiene `net.slack.post` en D4. El resultado es que `activate(S1)` da `('deny','depth')` y `revert(target=S1)` da `('allow',['log'])` con independencia del sujeto.
- Condición: se cumple cuando el anfitrión implementa 4.8 tal cual y `revert` acepta un StateId arbitrario y se usa también para rehacer (5.5). No se afirma si la comprobación del PDP por llamada del broker del runtime impide el uso real de permisos, porque depende de la implementación.
- Impacto: esta transición de estado se salta el techo del inquilino, G5 y la reverificación de suspensiones. Contradice I4 y 5.4 (E10).
- Medida (esta revisión): se añadió `floor_scoped(req)`. Solo se considera piso cuando se cumplen todas estas condiciones: propietario humano, capa propia, estado anterior y sin aumento de permisos ni de profundidad. Cualquier otro `revert` pasa por el mismo juicio mediante `as_activate`. También se añadió la rama `uses_destructive`, y se escribió la misma regla en 5.5 y 7.11.

### 3.2 Inyección en la salida de la herramienta de inspección (`tools/check_schemas.py:29`, `:26`)

- Sujeto de confianza inferior: autor de los documentos externos o de los nombres de archivo que se pasan al comando `check_schemas.py <schema> FILE`.
- Reproducción: se creó la clave `concepts` de un lexicon-pack como `"x\e]0;PWNED\a\e[2K\rOK   forged.yaml[0]\n::error title=forged::…"`. Esta clave entró tal cual en `json_path` y se imprimió.
- Impacto: solo se falsifican la salida y los registros (título de la ventana, una línea `OK` falsa, anotaciones de GitHub Actions). No afecta al veredicto, al código de salida, a los archivos ni a las credenciales.
- Medida (esta revisión): se usa `safe()` (escape con repr, recorte a 300 caracteres) en todas las cadenas que se imprimen. Se añadió un assert como comprobación de regresión. Al volver a ejecutar en el sandbox, el resultado es 0 ESC y 0 líneas `::`.

## 4. Necesita más verificación

| Título | Ubicación | Bloqueo | Estado |
| --- | --- | --- | --- |
| La aplicación automática de la propagación de línea base solo comprueba que no haya cambio de permisos | `docs/06-versioning-and-lineage.md:121-122` | La especificación no definía si `apply(merged)` pasa por `ChangeStore.activate` (E10) | El responsable de la especificación lo definió en esta revisión: la aplicación automática también pasa por `activate()`, y si requiere aprobación, PROPOSED. `delta_permissions` se recalcula |

El primer verificador desestimó este caso. Su argumento era que, según 05:150, 05:205 y 07:77, la activación siempre pasa por el PDP. Sin embargo, ese resultado tenía un error de formato, así que se descartó según las reglas, y el nuevo verificador tomó como bloqueo que en 06:122 no hay ninguna frase que lo ligue a `activate`, y lo juzgó `needs_validation`. Ambas interpretaciones llegan a la misma conclusión de que 6.5 necesita una frase explícita, así que se añadió esa frase.

## 5. Notas de endurecimiento (no son defectos; si se incorporaron o no)

- Incorporado: el contrato determinista de change-record debe tener al menos una forma ejecutable. Los registros que solo tienen forma descriptiva ahora se rechazan.
- Incorporado: recálculo de `permissions_delta`; `approved_by` es un sujeto humano y debe ser distinto de `agent`. Se añadió a la descripción del esquema y a 7.11.
- Incorporado: `network.allow` y el `allowlist` de la política rechazan los literales IP. Los comodines de sufijos públicos, la existencia de permiso de egress y `setKnob` default ⊆ ceiling se escribieron como MUST del validador de conformidad (conformance validator) y se añadieron casos de regresión con expectativa `False`.
- Incorporado: se rechazan los alias YAML y los archivos de más de 1 MiB. Desaparecieron el problema de una bomba de alias de 555 B que generaba 75.5 MB de salida y el OOM con una entrada de 601 B. Se aislaron las excepciones por documento (claves no de tipo cadena).
- Incorporado: `design_space.py --profile` y `--check` devuelven código de salida 1 ante un veredicto de fallo, y rechazan claves duplicadas y JSON que no sea un objeto.
- Incorporado: CI `permissions: contents: read`. Se corrigió `net.allowlist` del extracto de 4.7 a `net.slack.post` (L-04).
- No incorporado (propuesta): fijar Actions por SHA de commit, fijar hashes en `requirements.txt`, definir el significado del id de capacidad `*`, hacer obligatorio `content_hash` al compartir, campo de huella de aprobación.

Patrones positivos: uso de `yaml.safe_load`. Estructura de regresión que expone las reglas entre documentos como `ACCEPTED (validator MUST check)`. La correspondencia entre profundidad y forma se impone en tres lugares.

## 6. Cobertura

17 unidades en el libro mayor: covered 8 · candidate 3 (todas con veredicto final) · blocked 0 · deferred 6.

Unidades que encontró y aplazó la crítica final:
1. Ligar las aprobaciones y los consentimientos al cambio de permisos recalculado, al content_hash y al consentimiento de `Contract-Migrated`
2. El id de capacidad `*` y el PDP por llamada frente a la concesión en el montaje
3. El veredicto OK de `check_schemas.py` y las diferencias del modelo de datos YAML→JSON (claves no de tipo cadena, claves duplicadas)
4. Fijación de la firma de versiones, revocación, degradación de versión
5. Envenenamiento de la caché de resoluciones R3 (nodos Sybil en el mismo inquilino)
6. Separación de roles de 7.3 y regla de acción de las etiquetas de 7.5 (inyección indirecta)

La próxima auditoría debe empezar por estas 6 con el perfil standard.
