<!-- LANG-BAR -->
[English](../en/07-trust-and-security.md) · [한국어](../ko/07-trust-and-security.md) · [简体中文](../zh-CN/07-trust-and-security.md) · [日本語](../ja/07-trust-and-security.md) · **Español**
<!-- /LANG-BAR -->

# 7. Confianza y seguridad: decidir primero en quién no confiar

> Conclusión de este capítulo: el agente generador de un sistema Mallangable tiene por defecto, todo a la vez, **datos privados, entradas no confiables y una vía para enviar datos al exterior**. Si estas tres cosas se juntan en un mismo contexto, una sola inyección de prompt basta para que se filtren datos. La solución no es un filtro más listo, sino una **separación estructural**: dividir los roles, poner etiquetas de visibilidad a los datos, dar a las extensiones solo los permisos que se les entregan de forma explícita y hacer la aplicación final en el límite del operador.

## 7.1 Modelo de amenazas

### Activos que hay que proteger

| Activo | Ejemplo | Propietario |
| --- | --- | --- |
| Datos del usuario | Documentos y registros dentro de la aplicación anfitriona | Usuario, inquilino |
| Artefactos de capa | Pantallas y automatizaciones de la línea base de la organización (conocimiento interno) | Inquilino, organización |
| Propiedad intelectual del núcleo | Código fuente del anfitrión | Proveedor |
| Credenciales | Claves de API del modelo, tokens de servicios externos | Usuario, inquilino |
| Presupuesto | Créditos de inferencia, coste de nube del inquilino | Inquilino, operador |
| Integridad | "Mi app funciona solo como yo la aprobé" | Usuario |

### Atacantes

| Atacante | Objetivo | Vía principal |
| --- | --- | --- |
| Compartidor malicioso | Robar datos y credenciales del receptor | Funcionalidades compartidas, mercado público |
| Inyector indirecto | Manipular el comportamiento del agente plantando instrucciones en el contenido que lee | Documentos, páginas web, textos descriptivos de elementos compartidos, cuerpo de incidencias |
| Usuario interno curioso | Ver el código fuente oculto de capas superiores | Pedir al agente "enséñame el código fuente" |
| Cliente comprometido | Colar en el servidor cambios que se saltan la política | Desactivar los hooks del dispositivo, escribir directamente en el repositorio |
| Administrador excesivo | Vigilar a los miembros | Subir la visibilidad de gestión |
| Persona interna del operador | Ver el código de los clientes | Herramientas de soporte |
| Atacante de costes | Agotar el presupuesto | Provocar reintentos infinitos, generación masiva |
| Contaminador de contratos o del juez | Un contrato que deja pasar comportamiento malicioso, un veredicto de aprobado obtenido engañando al juez | Contratos escritos por un generador que sufrió una inyección, instrucciones dirigidas al juez plantadas en los artefactos ("este panel cumple la intención") |
| Envenenador de la caché de resoluciones (dentro del mismo inquilino) | Crear una resolución "verificada" solo con su propio contrato y difundirla a todo el inquilino | Reutilización de la caché de resoluciones R3 (6.8). El límite de ámbito solo impide la fuga *entre* inquilinos |
| Versión superior u operador comprometidos | Distribuir cambios maliciosos a todos los nodos inferiores a través de la línea base | Robo de la clave de firma de versiones, persona interna del operador, aplicación `auto` (6.5) |

Controles para las tres últimas filas:
- **Contaminación de contratos o del juez**: el borrador del contrato lo escribe el intérprete en la fase de especificación del trabajo, y el generador no puede borrar ni debilitar elementos del contrato (se extiende la separación de I7 hasta el contrato, regla 2 de 6.7). El juez (judge) (G4) solo recibe entradas con un esquema fijo (intención, contrato, capturas de pantalla, observaciones) y no se pone el texto original de los artefactos en su contexto. Los artefactos tienen integridad `untrusted` (7.5).
- **Envenenamiento de la caché de resoluciones**: una resolución solo se carga en la caché después de pasar la reverificación κ_up ∧ κ_down en k o más nodos distintos del usuario que la creó (valor propuesto 3) (R3, 6.8).
- **Versión superior u operador comprometidos**: la clave de firma de versiones se fija (pin) en cada punto de aplicación (verificación de recepción) y se consulta la lista de revocación. Incluso la aplicación `auto` pasa por el canario (6.5), y el inquilino puede rechazar una versión superior y mantener la actual. Las versiones también llevan la atestación de procedencia de 7.7.

### Límites de confianza

```mermaid
flowchart LR
  subgraph UNTRUSTED["No confiable"]
    EXT["Contenido externo<br/>web · documentos · descripciones de elementos compartidos"]
    SH["Funcionalidades creadas por otros"]
    DEVC["Todo el dispositivo del usuario<br/>hooks · copias · runtime"]
  end
  subgraph SEMI["Confianza condicional"]
    AGT["Salida del agente<br/>siempre sujeta a verificación"]
  end
  subgraph TRUSTED["Límite del operador · aplicación con autoridad"]
    RCV["Verificación de recepción"]
    PDPx["PDP"]
    SBX["Sandbox del servidor"]
    STO["Repositorio original · registro de auditoría"]
  end
  EXT --> AGT
  SH --> AGT
  DEVC --> RCV
  AGT --> RCV
  RCV --> PDPx
  RCV --> STO
  SBX --> STO
```

Cómo leerlo: tanto el dispositivo del usuario como la salida del agente están **sujetos a verificación**. No significa que haya que sospechar del propio usuario, sino que el repositorio original no debe contaminarse aunque el dispositivo esté comprometido o el agente haya sufrido una inyección.

## 7.2 Puntos de aplicación y punto de decisión

| Punto de aplicación (PEP) | Ubicación | Autoridad | Qué impide |
| --- | --- | --- | --- |
| Hooks del harness del dispositivo | Dispositivo del usuario | Orientativa | Errores, la mayoría de los intentos de inyección |
| Broker del runtime | Dentro del anfitrión | Autoridad en tiempo de ejecución | Uso de permisos no aprobados |
| Verificación de recepción | Límite del operador | **Autoridad final** | Registros que violan el formato o la política, manipulación de archivos de política |
| Sandbox del servidor | Límite del operador | Autoridad final | Accesos fuera del alcance del trabajo, comunicación externa |
| Puerta de salida | Plano de generación → plano de experiencia | Autoridad final (modo hidden) | Fuga de código y secretos |

Todos los PEP usan las mismas reglas del PDP. Si en el momento de generar (harness) y en el de ejecutar (broker) se usan reglas distintas, aparecen huecos del tipo "se permitió al crearlo pero se prohíbe al ejecutarlo".

## 7.3 Cortar la tríada letal mediante la estructura

Simon Willison resumió que, si un agente tiene a la vez **① acceso a datos privados, ② exposición a contenido no confiable y ③ capacidad de comunicación externa**, un atacante puede extraer datos con facilidad, y lo llamó "tríada letal (lethal trifecta)". Afirma que todavía no existe forma de bloquearlo al 100% y que el camino seguro es evitar la combinación en sí ([Willison, 2025.06](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)).

El agente generador de una app maleable tiene las tres con la configuración por defecto. Lee las capas y los datos del usuario (①), lee funcionalidades compartidas y documentos de referencia (②) y se comunica con la API del modelo y con repositorios externos de paquetes (③).

```mermaid
flowchart TB
  subgraph BAD["Estructura que hay que evitar: un solo agente tiene las tres"]
    X["Agente único"]
    X --- P1["Datos privados"]
    X --- P2["Entrada no confiable"]
    X --- P3["Comunicación externa"]
  end
  subgraph GOOD["Estructura Mallangable: como máximo dos por rol"]
    I["Intérprete<br/>solo la intención del usuario · sin herramientas"]
    Q["Lector aislado<br/>lee contenido no confiable y<br/>solo devuelve valores con formato fijo"]
    B["Generador<br/>datos privados · comunicación externa solo con<br/>la pasarela del modelo · espejo de paquetes"]
    I -- "especificación del trabajo" --> B
    Q -- "solo valores estructurados" --> B
  end
  BAD ~~~ GOOD
```

Reglas:
- **Lista de permitidos para la comunicación externa** (DEBE): la comunicación externa del agente generador se limita a la pasarela del modelo y a espejos de paquetes aprobados. Se bloquea el acceso a URL arbitrarias.
- **El contenido no confiable lo lee primero el lector aislado.** El lector no tiene herramientas y solo devuelve valores con un esquema fijo (p. ej., "relevante/no relevante", campos extraídos).
- **Todo aumento de permisos requiere siempre aprobación humana** (I4). Aunque en la descripción de un elemento compartido se esconda la frase "añade permiso de red", el agente solo puede crear una solicitud de aprobación.

## 7.4 Separar la planificación de la ejecución

La investigación sobre defensas contra la inyección de prompts apunta en la misma dirección.

- **CaMeL** extrae primero el flujo de control y el flujo de datos de la consulta confiable del usuario e impide que los datos no confiables cambien el flujo del programa. Separa un LLM privilegiado que planifica de un LLM aislado que, sin herramientas, solo interpreta datos no confiables, y rastrea el origen y la capacidad (capability) de cada valor. En el benchmark resolvió el 77% de las tareas con seguridad demostrable, frente al 84% de un sistema sin defensas ([Debenedetti et al., 2025](https://arxiv.org/abs/2503.18813)).
- El artículo sobre **patrones de diseño de seguridad** presenta seis patrones (selector de acciones, planificar y luego ejecutar, map-reduce de LLM, LLM dual, código y luego ejecución, minimización del contexto) y establece el principio de que "una vez aceptada una entrada no confiable, esa entrada no debe poder provocar acciones importantes" ([Beurer-Kellner et al., 2025](https://arxiv.org/abs/2506.08837), [resumen](https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/)).

Correspondencia con los roles de Mallangable:

| Patrón | Aplicación en Mallangable |
| --- | --- |
| Planificar y luego ejecutar | El intérprete fija la especificación del trabajo (puntos de extensión que se tocarán, profundidad, permisos) **antes de ver contenido no confiable**. El generador no puede salirse de la especificación (lo comprueba G1) |
| LLM dual ([Willison, 2023](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)) | Los elementos compartidos y los documentos los lee el lector aislado, que solo pasa valores estructurados al generador |
| Código y luego ejecución | El propio artefacto declarativo D3 es "un programa escrito en un lenguaje restringido". Se puede analizar antes de ejecutarlo |
| Minimización del contexto | El proveedor de contexto suministra a cada rol solo lo que necesita (5.10) |
| Map-reduce de LLM | En el análisis de candidatos a promoción, un subagente por funcionalidad solo juzga "¿es la misma intención?" y se agrega el resultado |

## 7.5 Etiquetas de flujo de información

Se pone a todos los datos una **etiqueta de visibilidad (visibility label)** y se definen las reglas para cuando las etiquetas se mezclan.

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

El eje de integridad sigue el método de FIDES ([Costa et al., 2025](https://arxiv.org/abs/2505.23643)), que rastrea juntas las etiquetas de confidencialidad e integridad (integrity label) en el nivel del planificador y aplica las políticas de forma determinista. Es el "planificar y luego ejecutar" de 7.4 escrito como reglas de etiquetas.

Ejemplo: una resolución que crea el agente de fusión tras leer código del inquilino A (V3) lleva la etiqueta V3. Por eso, al meterla en la caché de resoluciones, entra solo en el ámbito del inquilino A (6.8). Cuando el panel muestra la "distribución de métodos de resolución", la puerta de salida deja solo los recuentos y la rebaja a V0.

Elementos que comprueba la puerta de salida (output gate) en modo hidden:

| Señal | Veredicto |
| --- | --- |
| Violación del esquema de salida, exceso de longitud | Bloquear, regenerar |
| Bloques de código o líneas consecutivas que parecen código | Eliminar |
| Coincidencia larga y continua con el contenido del repositorio (comparación con el índice de huellas) | Eliminar + evento de seguridad |
| Densidad excesiva de rutas e identificadores internos | Eliminar |
| Patrones de secretos | Bloquear + alerta |

## 7.6 Seguridad de la ejecución de extensiones

**Principio de capacidad de objeto (object-capability)**: las extensiones no tienen autoridad ambiental (ambient authority). Solo pueden usar los objetos de permiso que se les entregan de forma explícita al montarse. Hardened JavaScript congela los objetos integrados con `lockdown()` para impedir la contaminación de prototipos y separa el ámbito global con `Compartment` para que solo se usen los objetos entregados ([Endo/SES](https://github.com/endojs/endo)).

| Nivel de aislamiento | Qué impide | Qué no impide | Dónde conviene usarlo |
| --- | --- | --- | --- |
| Lenguaje (SES·Wasm) | Contaminación global, API no entregadas | Agotamiento de recursos por bucles infinitos, temporización | Ejecución ligera de hooks de eventos (D4) |
| Marco (iframe de origen cruzado, webview) | DOM, almacenamiento y cookies del anfitrión | Pantallas que engañan al usuario (botones falsos) | Código de paneles (D4), elementos compartidos públicos |
| Proceso, microVM | Memoria, sistema de archivos, red (si se configura) | Fugas a través de canales permitidos | Código nativo compartido, trabajos del servidor |

Si el anfitrión es un framework de escritorio, compruebe el sistema de permisos por webview. Por ejemplo, Tauri v2 usa capabilities por ventana y por webview, y una webview que no coincide con ninguna capability no tiene ningún acceso a la capa IPC ([Tauri v2](https://v2.tauri.app/reference/acl/capability)). En sistemas así, la configuración por defecto es **no dar ninguna capability a las webviews de extensión** y dejar el broker como única vía.

Reglas del broker:
- Consulta todas las llamadas al PDP y deja registro de auditoría.
- Pone límites a la frecuencia de llamadas y al tamaño de las respuestas (limitación de la velocidad de fuga).
- Excluye del catálogo las pantallas que pueden engañar al usuario (imitaciones de campos de inicio de sesión, etc.) y añade a las pantallas de extensión la marca "esta parte es una funcionalidad que añadí yo".

## 7.7 Cadena de suministro

Cuando se abre la compartición (A8), las extensiones se convierten en una cadena de suministro. En febrero de 2026, la empresa de seguridad Koi Security reveló 341 skills maliciosas de las 2,857 que auditó en un mercado de skills para agentes ([The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)). Después se introdujeron escáneres, pero en el análisis de febrero a mayo de 2026 todavía quedaban skills que evitaban la detección, por ejemplo inflando archivos hasta 22MB para superar el límite de inspección. Los analistas señalaron como causa raíz "la falta de aislamiento entre la lógica de la skill y los permisos del agente" ([Unit 42, 2026.06](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/)).

Convertidas las lecciones en controles:

| Lección | Control |
| --- | --- |
| Las skills se ejecutaban con los permisos del agente | Las funcionalidades compartidas vuelven a pasar desde cero por el sandbox y la aprobación de permisos del receptor |
| Se inducía a ejecutar comandos de shell con la excusa de una "instalación previa" | Las funcionalidades compartidas no tienen scripts de instalación. Los artefactos son solo declarativos o código en sandbox |
| Se inflaban archivos para esquivar el escáner | Los elementos compartidos que superan el límite de tamaño se **rechazan** (no se omiten). La inspección cubre todos los bytes |
| Se cambiaba el contenido en remoto después de la instalación | Los elementos compartidos se fijan por hash de contenido. Traer datos externos durante la ejecución se muestra como permiso y requiere aprobación |
| Una sola cuenta subía en masa | Firma de procedencia del publicador (predicado [SLSA provenance](https://slsa.dev/spec/v1.1/provenance) en un Statement de [in-toto](https://github.com/in-toto/attestation). El sujeto es el content_hash del manifiesto y builder.id es el id del harness), límites para publicadores nuevos, niveles de curación |

## 7.8 Hasta dónde se garantiza la confidencialidad del código fuente

**El código que un agente puede leer acaba pudiéndolo leer también quien habla con ese agente.** Por eso hay que distinguir con honestidad el nivel de garantía según la amenaza.

| Amenaza | Modo client | Modo server · hidden |
| --- | --- | --- |
| Lectura casual (abrirlo por curiosidad) | No lo impide | Lo impide: el usuario no tiene el repositorio |
| Extracción intencionada (inducir al agente a mostrarlo) | No se puede impedir | Lo impide en su mayor parte: el intérprete nunca ha visto el código y la puerta de salida filtra |
| Ingeniería inversa de artefactos (análisis del paquete ejecutable descargado) | No aplica | **Riesgo residual**: el código que llega al dispositivo se puede leer |
| Petición de rodeo ("crea un panel que me muestre mi código fuente") | No aplica | Se reduce con reglas estáticas (prohibido acceder al código fuente) + juez, pero no es perfecto |
| Exfiltración por personas internas | Registro de auditoría | Registro de auditoría + procedimiento de aprobación de acceso de emergencia |

El texto de compromiso con el cliente debe ser preciso, por ejemplo "la prevención de la extracción intencionada es de mejor esfuerzo". Se recomienda colocar la lógica clave en puntos de extensión del lado del servidor (puntos de servicio), no en extensiones que bajan al dispositivo.

## 7.9 Visibilidad de gestión y privacidad

- Los niveles de visibilidad V0~V3 (A10 de 3.2) y sus valores por defecto se fijan en el capítulo 4. El usuario siempre puede ver su nivel actual (piso F3).
- Los campos de identificación personal de la telemetría se guardan separados con una clave seudónima, de modo que ante una solicitud de borrado basta con destruir la clave para romper el vínculo.
- Cuando el operador accede en emergencia (break-glass) a datos de clientes: consignar motivo, alcance y duración → aprobación del administrador del cliente → sesión de solo lectura → mostrar todas las consultas en tiempo real en el panel del cliente → revocación automática al vencer el plazo → informe posterior.
- Los metadatos de commits y los resúmenes de intención pueden convertirse en datos personales si se vinculan a una persona, y la supervisión de la actividad de los miembros está sujeta a normativas laborales y de privacidad que varían de un país a otro. Es necesario revisar la legislación aplicable antes del despliegue.

## 7.10 Uso indebido

Las apps maleables también permiten que un usuario cree **funcionalidades dañinas para otras personas**. Ejemplos: un panel que registra a escondidas la actividad de un compañero, una automatización que envía datos de clientes al exterior.
- Los permisos para leer datos de otras personas y para enviar datos al exterior se limitan con el techo del inquilino y requieren aprobación.
- Se añade a los elementos que comprueba el juez si hay "recopilación o envío ocultos".
- Se informa al usuario, en términos comunes, de que los usos prohibidos por la política de uso del proveedor del modelo pueden rechazarse en la fase de generación.

## 7.11 Lista de comprobación de seguridad (DEBE)

- [ ] Las extensiones no llegan a funciones del anfitrión por ninguna vía que no sea el broker
- [ ] La comunicación externa del agente generador se limita a la lista de permitidos
- [ ] Un aumento de permisos no se activa sin aprobación humana
- [ ] El generador y el juez son instancias distintas
- [ ] La verificación de recepción comprueba el formato de registro, la existencia del contrato, la inmutabilidad de los archivos de política y el tamaño
- [ ] Las funcionalidades compartidas se vuelven a verificar y a aprobar en el lado receptor
- [ ] Los elementos compartidos que superan el límite de tamaño se rechazan
- [ ] Las listas de compartición y del mercado, las vistas previas antes de instalar y la indicación de permisos se leen del manifiesto sin ejecutar código de la extensión. Ejecutar antes de la aprobación rompe el "D4 antes de la aprobación tiene permisos 0" de 5.9 (ThinkRail también rechaza el método de ejecutar las extensiones cada vez que se listan y usa listados sin efectos secundarios, [`agent/packages/SPEC.md`](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/packages/SPEC.md#L23-L25))
- [ ] La caché de resoluciones, el índice de huellas y los sandboxes se separan por ámbito de visibilidad
- [ ] En modo hidden, el intérprete no accede al código y toda salida pasa por la puerta de salida
- [ ] Los derechos mínimos del usuario (user floor rights) F1~F7 no se pueden desactivar con ninguna política
- [ ] Las excepciones de acciones de piso solo se aplican cuando el propietario es humano, la capa es la propia y los permisos no aumentan. Rehacer, "volver a activar", levantar una suspensión y una reversión invocada por el agente pasan por el mismo juicio que la activación (4.8)
- [ ] La aplicación automática de la propagación de línea base también pasa por activate (E10). Si es gated, usa una funcionalidad destructiva o tiene una aprobación ligada a huella, baja a propuesta (6.5)
- [ ] `permissions_delta` no se fía de lo que se declara a sí mismo, sino que se recalcula a partir del manifiesto y del estado del padre
- [ ] Si `network.allow` del manifiesto no está vacío, en `permissions` hay una funcionalidad con risk=egress. Se rechazan los literales IP y los comodines de sufijos públicos
- [ ] La salida de las herramientas de inspección escapa los caracteres de control de los nombres de documentos y archivos, y el veredicto se comunica mediante el código de salida

Siguiente capítulo: [8. Diseño de la experiencia](08-experience-design.md)
