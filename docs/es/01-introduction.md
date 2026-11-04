<!-- LANG-BAR -->
[English](../en/01-introduction.md) · [한국어](../ko/01-introduction.md) · [简体中文](../zh-CN/01-introduction.md) · [日本語](../ja/01-introduction.md) · **Español**
<!-- /LANG-BAR -->

# 1. Introducción: por qué hace falta una 'arquitectura de software maleable' propia

> Conclusión de este capítulo: la IA ha abaratado el código, pero todavía no existe un estándar para **la estructura que mete ese código dentro de una aplicación existente, lo ejecuta de forma segura y lo hace resistir a las actualizaciones**. Mallangable-AI define esa estructura.

## 1.1 El problema: el código se abarató, pero el software sigue siendo rígido

El software producido en masa se hace para el usuario promedio. Cuanto más se aleja alguien del promedio, más adapta su forma de trabajar al software. Ink & Switch compara este estado con "un electrodoméstico comprado en una tienda" y llama **software maleable (malleable software)** al ecosistema en el que los usuarios adaptan sus herramientas ([Ink & Switch, 2025](https://www.inkandswitch.com/essay/malleable-software/)).

En 2025~2026 el costo de generar código cayó bruscamente. Pero, como señala ese mismo ensayo, **la generación de código con IA no basta para que el software se vuelva maleable.** Los generadores de aplicaciones solo crean aplicaciones nuevas; no pueden modificar las que ya se están usando. En la práctica, el bloqueo está en tres puntos.

| Carencia | Síntoma | Dónde lo trata este documento |
| --- | --- | --- |
| **No hay dónde encajarlo** (carencia de superficie) | Aunque la IA cree una funcionalidad, la aplicación existente no tiene un hueco donde insertarla. Al final se parchea directamente el código fuente del núcleo | Capítulo 2, puntos de extensión · profundidad; capítulo 5, runtime |
| **No resiste las actualizaciones** (carencia de persistencia) | Cuando el proveedor publica una nueva versión, las modificaciones del usuario se rompen. Se repite con miles de usuarios × cada versión | Capítulo 6, linaje · fusión que preserva contratos |
| **No se puede controlar** (carencia de gobernanza) | No se sabe quién cambió qué, a qué accede ese código ni quién paga el costo | Capítulo 4, espectro de control; capítulo 7, confianza; capítulo 9, negocio |

La tercera carencia no es teórica: es un incidente que ya ocurrió. A principios de 2026, en un mercado de skills para agentes, se confirmó que 341 de las 2,857 skills auditadas eran maliciosas ([The Hacker News, 2026.02](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)), e incluso después de introducir un escáner seguían quedando skills que eludían la revisión inflando el tamaño de sus archivos ([Unit 42, 2026.06](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/)). La causa de fondo era estructural: "las skills se ejecutan con todos los permisos del agente".

## 1.2 Definición

> **Software Mallangable** es el software en el que, cuando el usuario expresa una intención mediante lenguaje natural, señalando la pantalla o con una demostración, un agente de IA crea un cambio **dentro de los puntos de extensión que la aplicación anfitriona definió de antemano**, y ese cambio **se verifica mediante contratos, se registra de forma reversible y se gestiona para que sobreviva a las actualizaciones de la línea base superior**.

Origen del nombre: el coreano **말랑(mallang)**, que significa blando o esponjoso, + el inglés **-able**. Se eligió para que suene igual que el inglés *malleable* (maleable, que se puede extender a golpes).

### Diferencias con enfoques parecidos

| Enfoque | Qué se cambia | Quién lo cambia | Modifica la aplicación existente | Supervivencia a actualizaciones | Control de riesgos |
| --- | --- | --- | --- | --- | --- |
| Ajustes (Settings) | Valores que el proveedor expuso de antemano | Usuario | Sí (de forma limitada) | Alta | Alto |
| Plugins | Partes abiertas por la API del proveedor | Desarrollador | Sí | Media (se rompe si cambia la API) | Varía según el ecosistema |
| Constructores no-code | Una aplicación nueva dentro del constructor | Usuario | No | Depende de la plataforma | Depende de la plataforma |
| Generadores de aplicaciones (vibe coding) | Una aplicación nueva completa | Usuario + IA | No | No aplica | Bajo~medio |
| UI generativa (efímera) | La pantalla de esta conversación | IA | No (volátil) | No aplica | Limitado por un catálogo |
| **Mallangable** | Funcionalidades, pantallas y comportamientos dentro de los puntos de extensión | Usuario + IA (+ organización) | **Sí** | **Objetivo de diseño** | **Ajustable por política** |

## 1.3 Contribuciones de este documento

1. **Modelo formal**: define anfitrión (host), capa (layer), cambio (change), contrato (contract) y política (policy), y presenta 10 invariantes (invariants) que la arquitectura debe cumplir (capítulo 2).
2. **Jerarquía de profundidad de cambio D1~D5**: una escala de riesgo que aplica a los cambios del usuario el principio de mínimo poder (Rule of Least Power), "resuélvelo con la expresión más débil" (capítulo 2).
3. **Espacio de diseño (design space)**: filtra las **1,944,000** combinaciones en bruto de 11 ejes con restricciones lógicas, normativas y de recomendación hasta **36,772 (1.89%)**, organizadas en **863** familias estructurales (structural families), y publica junto con ello una herramienta para volver a calcularlas (capítulo 3, `tools/design_space.py`).
4. **Espectro de control**: define con un modelo de 'delegación de intervalos' el rango que se permite al usuario y el rango que controla el operador, y establece **un piso de derechos del usuario que ninguna política puede quitar** (capítulo 4).
5. **Arquitectura de referencia**: define 6 planos (planes), interfaces de puertos y adaptadores, un modelo de eventos de harness neutral respecto al proveedor y puertas de verificación (verification gates) (capítulo 5).
6. **Fusión que preserva contratos y propagación de linaje**: presenta las condiciones y el modelo de costos para que las modificaciones del usuario resistan las actualizaciones de la línea base (capítulo 6).
7. **Convenciones de diseño de la experiencia**: define las superficies de entrada, los niveles de tiempo (T0~T4), la representación del proceso de generación, los paquetes de léxico (lexicon packs) y el flujo de conexión de modelos (capítulo 8).
8. **Matriz de acoplamiento con el negocio**: relaciona de forma calculable qué decisiones de arquitectura requiere cada uno de los 20 BM (capítulo 9).

## 1.4 Alcance y fuera de alcance

**Lo que cubre**
- Los conceptos, límites, interfaces y opciones necesarios para volver maleable el software existente (SaaS web, escritorio, móvil, herramientas internas de trabajo).
- Las estructuras de control, visibilidad y cobro desde el usuario individual hasta entornos empresariales y públicos.

**Lo que no cubre**
- Implementaciones en un lenguaje o framework concreto. Este documento define solo interfaces y convenciones.
- Técnicas de prompting para un modelo concreto. Los modelos se tratan como piezas intercambiables.
- Asesoramiento legal. Los temas de datos personales, trabajo y derechos de autor se recogen solo como consideraciones de diseño; su aplicación real requiere revisar la legislación de cada jurisdicción.

## 1.5 Trabajo relacionado y diferencias

| Línea | Idea central | Lo que se toma | En qué se diferencia |
| --- | --- | --- | --- |
| Malleable software ([Ink & Switch](https://www.inkandswitch.com/essay/malleable-software/)) | Una pendiente suave de usuario → creador, centrada en herramientas | La motivación de la jerarquía de profundidad, la creación comunitaria | Define como arquitectura también los agentes de IA, la gobernanza empresarial y el cobro |
| Medios computacionales · documentos dinámicos (Boxer, 1986 · [Webstrates](https://webstrates.net/), 2015 · [Potluck](https://www.inkandswitch.com/potluck/), 2022 · [Embark](https://www.inkandswitch.com/embark/), 2023) | Eliminar el límite entre documento y aplicación y dejar que el usuario superponga cálculo | Capas superpuestas que no tocan el original (2.3), herramientas que cruzan aplicaciones (O8) | Se define sobre aplicaciones comerciales existentes, con una estructura que resiste las actualizaciones del proveedor |
| Pendiente suave (MacLean et al., 1990, citado en el ensayo anterior) | Al crecer la capacidad de personalización, el aprendizaje necesario debe aumentar solo poco a poco | D1~D5 diseñados como una 'pendiente sin precipicios' | Cada tramo de la pendiente se asocia a un nivel de riesgo y de rigor de verificación |
| [Rule of Least Power](https://www.w3.org/2001/tag/doc/leastPower.html) (W3C TAG) | Cuanto menos expresivo es un lenguaje, más fácil es analizarlo, reutilizarlo y asegurarlo | La regla "construye con la mínima profundidad necesaria" | Obliga a que sea el agente, y no una persona, quien elija la profundidad |
| Líneas de productos de software dinámicas (DSPL) · modelos de características ([Capilla et al., 2014](https://research.chalmers.se/publication/198081)) | Configuración de funcionalidades en ejecución, restricciones entre funcionalidades | Calcular el espacio de diseño como un modelo de configuración con restricciones | Quien configura no es el proveedor, sino el usuario + la IA |
| Local-first · CRDT · Patchwork ([Ink & Switch](https://www.inkandswitch.com/project/patchwork/)) | Datos propiedad del usuario, control de versiones de uso general | Opciones de topología, rama = experimento · poner las ediciones de la IA en ramas y que una persona elija y fusione (notas de experimentos de Patchwork) | Añade el linaje (jerarquía de líneas base) y la fusión que preserva contratos |
| Estándares de UI generativa ([A2UI](https://a2ui.org/), [MCP Apps](https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp)) | UI declarativa en lugar de código, UI en iframe con sandbox | Formato de los artefactos D3 | Cambios persistentes y versionados, no efímeros |
| Skills y plugins de agentes ([Agent Skills](https://agentskills.io/specification)) | Empaquetar procedimientos en carpetas, portables entre agentes | Formato de distribución del harness | Una skill es solo un procedimiento; la imposición de permisos le corresponde a la arquitectura |
| Defensa contra la inyección de prompts ([CaMeL](https://arxiv.org/abs/2503.18813), [patrones de diseño](https://arxiv.org/abs/2506.08837), [tríada letal](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)) | Separar el flujo de control de los datos no confiables, separar permisos | Separación de roles de agentes, etiquetas de flujo de información | Se aplica al contexto de generación y fusión de código |
| Generación dentro de la aplicación ([n.codes](https://github.com/yungookim/n.codes), [Glaze](https://www.implicator.ai/raycast-launches-glaze-a-platform-for-building-desktop-apps-through-ai-prompts/)) | Generar UI por usuario a partir del mapa de funcionalidades de la aplicación, compartir y hacer fork de aplicaciones | Mapa de capacidades (capability map), flujo de compartición | Define como modelo general la supervivencia a actualizaciones, el linaje y el espectro de control |

## 1.6 Convenciones de notación

- **DEBE (MUST)**: si no se cumple, la implementación no es conforme con Mallangable-AI.
- **DEBERÍA (SHOULD)**: se puede no cumplir si hay una razón válida, pero esa razón debe documentarse.
- **PUEDE (MAY)**: es opcional.
- Los ejes se escriben `A1`~`A11`, las restricciones `L` (lógicas) · `N` (normativas) · `S` (advertencias), las invariantes `I1`~`I10`, los perfiles `P1`~`P7` y los BM `B1`~`B20`.
- Las cifras sin enlace a una fuente (p. ej., topes de tamaño, pesos de puntuación) son **valores de diseño propuestos** y deben ajustarse con experimentos.

Siguiente capítulo: [2. Modelo central](02-core-model.md)
