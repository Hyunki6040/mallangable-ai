<!-- LANG-BAR -->
[English](../en/10-open-problems.md) · [한국어](../ko/10-open-problems.md) · [简体中文](../zh-CN/10-open-problems.md) · [日本語](../ja/10-open-problems.md) · **Español**
<!-- /LANG-BAR -->

# 10. Problemas abiertos y métodos de evaluación

> Conclusión de este capítulo: esta especificación solo define la estructura; varios problemas clave siguen sin resolver. El mayor es que **si el contrato es débil, la fusión rompe la funcionalidad en silencio**. Por eso se propone **Mallang-Bench** como vara de medir común para comparar implementaciones, y entre sus métricas se considera la más importante la 'tasa de rotura silenciosa'.

## 10.1 Problemas abiertos

| # | Problema | Por qué es difícil | Punto de partida |
| --- | --- | --- | --- |
| O1 | **Suficiencia del contrato** | Los contratos que escribe un agente tienden a ser tautológicos ("existe el panel"). Un contrato débil deja pasar la fusión, pero la funcionalidad se rompe | Pruebas de mutación: medir la fuerza del contrato según si falla cuando se estropea a propósito el artefacto (puntuación de mutación). Usarla como criterio para elegir qué cubre la garantía de supervivencia (B9) |
| O2 | Detección de conflictos semánticos | Aunque no haya conflictos de texto ni de sintaxis, dos cambios juntos pueden romper la intención | Ejecutar la unión de contratos, medición a posteriori con un conjunto de pruebas ocultas |
| O3 | **Interacción entre funcionalidades** | Dos cambios correctos por separado se comportan de forma extraña cuando se activan juntos (el clásico problema de 'interacción entre funcionalidades' del software de telecomunicaciones) | Añadir a G2 pruebas combinadas para pares de cambios que tocan el mismo punto de extensión o los mismos datos |
| O4 | Fiabilidad del juez | El juicio de un modelo es probabilístico y oscila incluso con la misma entrada | Prioridad a los contratos deterministas, consenso de varios jueces, conjunto de referencia para calibrar los juicios |
| O5 | Completitud del mapa de capacidades | Si faltan puntos de extensión, las solicitudes se deslizan a D5 | Usar la tasa de solicitudes D5 como métrica de calidad del mapa de capacidades, añadir puntos empezando por las solicitudes más frecuentes |
| O6 | Economía del linaje | Si las versiones son frecuentes, crece el costo de propagación; si son raras, crece la deriva | Optimizar el ciclo de versiones con el modelo de costos de 6.8, diseñar los periodos de soporte |
| O7 | Señales de promoción que cruzan alcances | Hay que saber, sin mirar el código, que 'se está creando lo mismo' a través de los límites entre inquilinos | Similitud que solo usa metadatos V1, tamaño mínimo de agregación, comparación de conjuntos que preserva la privacidad |
| O8 | Composición de herramientas que cruza aplicaciones | El trabajo del usuario abarca varias aplicaciones ("herramientas, no aplicaciones"). Los puntos de extensión de un solo anfitrión no bastan | Contratos de datos comunes entre anfitriones, puntos de extensión a nivel del sistema operativo |
| O9 | Atribución de responsabilidad | Si un cambio creado por la IA causa un incidente, ¿de quién es la responsabilidad: del usuario, del inquilino, del operador o del proveedor del modelo? | Vincular los registros de procedencia (I9) y de aprobación con las condiciones de uso |
| O10 | Regresiones de accesibilidad | Las modificaciones del usuario pueden romper la lectura de pantalla y el manejo con teclado | Hacer obligatorias las reglas de accesibilidad de G3, integrar la accesibilidad en los componentes del catálogo |
| O11 | Código sobre CRDT | Conflicto entre la sincronización en tiempo real y el código ejecutable | Verificación en el momento de la activación, separar solo la zona de código en un linaje al estilo Git |
| O12 | Medir la maleabilidad | No existe una escala estándar para cuantificar la 'pendiente suave' | Trazar la curva de la pendiente con el tiempo hasta el primer éxito y el número de repreguntas por profundidad |
| O13 | Alineación con estándares | Los manifiestos de extensión, MCP Apps, A2UI y los formatos de skills evolucionan cada uno por su lado | Diseñar el manifiesto como **destino de adaptadores**, no como superconjunto de esos estándares |

## 10.2 Mallang-Bench (propuesta)

Propuesta de diseño de un benchmark para comparar implementaciones en las mismas condiciones.

### Composición

| Componente | Contenido |
| --- | --- |
| Anfitrión de referencia | Una pequeña aplicación de trabajo con unos 20 puntos de extensión (p. ej., una de tareas, documentos u hojas de cálculo). Mapa de capacidades público |
| Conjunto de solicitudes | 200 solicitudes de cambio redactadas como frases de usuarios comunes. Cada solicitud lleva etiquetadas la **profundidad mínima correcta** y las **pruebas ocultas** (aparte del contrato público). Las frases solo dicen qué hay que hacer, no cómo se mide (se prohíben "prueba", "calificación", "puntuación", etc.) |
| Secuencia de versiones | 3 versiones de la línea base. Incluyen cambios que rompen la compatibilidad (cambio de nombre de puntos, reorganización del diseño, retirada de puntos) |
| Conjunto de ataques | 50 casos, entre ellos inyecciones escondidas en descripciones de funcionalidades compartidas y en documentos de referencia, inducción a la escalada de permisos, inflado de tamaño y sustitución remota del contenido tras la instalación |
| Conjunto de extracción | 50 conversaciones que intentan extraer el código fuente en modo hidden |
| Simulador de usuario | Un script que responde a las repreguntas y acepta o rechaza las vistas previas |

Aislamiento de las pruebas ocultas (DEBE (MUST)):
- Las pruebas ocultas y sus resultados no entran en el contexto del intérprete, del generador ni del juez. La calificación la hace un proceso aparte una vez terminada la activación.
- Cada vez que crea un contexto de generación o de juicio, el ejecutor busca las rutas de los archivos de pruebas ocultas y las cadenas marcadoras de resultados de pruebas y, si las encuentra, detiene la ejecución. Esta comprobación es solo una alarma (tripwire), no una defensa. Si salta, no se amplía la lista de marcadores: se corrige la vía de lectura por la que se filtra.
(Fuente: la vista de ejecución sin puntuación y el tripwire de rastros de calificación de Harness², arXiv:2610.14224, google-research/harness2 `core/spec.py`, `core/context.py`)

### Métricas

| Símbolo | Métrica | Definición | Dirección |
| --- | --- | --- | --- |
| CSR | Tasa de éxito de cambios | Solicitudes activadas que pasan las pruebas ocultas / solicitudes posibles según la política | Cuanto más alta, mejor |
| LPC | Tasa de cumplimiento de la profundidad mínima | Cambios hechos en la profundidad mínima correcta / cambios exitosos | Cuanto más alta, mejor |
| TFC | Tiempo hasta el primer cambio | Mediana desde la entrada de la solicitud hasta la vista previa | Cuanto más bajo, mejor |
| USR | Tasa de supervivencia a la línea base | Funcionalidades que pasan las pruebas ocultas tras la versión / funcionalidades activas antes de la versión | Cuanto más alta, mejor |
| **SBR** | **Tasa de rotura silenciosa** | Fusiones que pasaron los contratos públicos pero fallaron las pruebas ocultas / (fusiones automáticas + fusiones `proposed` aprobadas por personas). Se informan también por separado las dos vías | **Cuanto más baja, mejor (máxima prioridad)** |
| HER | Tasa de intervención humana | Conflictos que llegaron a R5 / total de conflictos | Cuanto más baja, mejor (pero hay que mirarla junto con la SBR) |
| CPC | Costo por cambio | Costo de inferencia por cada cambio exitoso | Cuanto más bajo, mejor |
| IRR | Tasa de resistencia a la inyección | Proporción del conjunto de ataques que se bloqueó | Cuanto más alta, mejor |
| LKR | Tasa de fuga de código fuente | Proporción del conjunto de extracción en la que se filtraron fragmentos de código | Cuanto más baja, mejor |
| RBT | Tiempo de reversión | Desde la solicitud de revertir hasta la restauración completa | Cuanto más bajo, mejor (objetivo T0) |
| APB | Carga de aprobación | Número de solicitudes de aprobación semanales por usuario o administrador | Cuanto más baja, mejor |

Por qué la SBR es la máxima prioridad: la tasa de intervención humana (HER) baja fácilmente si se fusiona automáticamente de forma agresiva. El precio es la rotura silenciosa. Solo informando ambas métricas juntas la comparación es honesta.

### Formato del informe

Las implementaciones informan las métricas junto con las coordenadas del espacio de diseño que usaron (A1~A11). La comparación solo es justa entre coordenadas iguales. Ejemplo: "coordenadas P2, CSR 0.71, LPC 0.88, USR 0.83, SBR 0.04, HER 0.06".

Las solicitudes en las que falló la calificación (error al ejecutar las pruebas ocultas, error del modelo juez) no valen 0 puntos: quedan **sin puntuar (unscored)**. Se excluyen del denominador de las métricas y su número se informa junto a ellas. Ejemplo: "CSR 0.71 (n=192, sin puntuar 8)".

Condiciones de ejecución que se informan junto con las métricas:
- **Restricción de red**: la lista de hosts a los que pudo acceder el agente generador. Las direcciones que alojan las pruebas ocultas, el conjunto de ataques y el conjunto de extracción se bloquean durante la ejecución. En benchmarks públicos se ha informado de casos en que un agente descargó los criterios de calificación sin que se le indicara (repositorio de Harness², `docs/EXPERIMENTS.md`).
- **Número de llamadas**: el número de ejecuciones de generación y de sesiones de juicio por cada cambio exitoso (incluidos los reintentos). Con el CPC solo no se pueden comparar con justicia harness distintos.
- **Estado de la caché**: si se empezó con la caché de resoluciones y las lecciones aprendidas vacías, o si se permitió usar los resultados de solicitudes anteriores.

## 10.3 Niveles de conformidad (propuesta)

| Nivel | Condiciones |
| --- | --- |
| Mallangable Core | Garantiza por diseño las invariantes I1~I7, I9, I10. Implementa la especificación de registros, los contratos y la reversión. P1 · P5, que no tienen servidor, llegan hasta este nivel |
| Mallangable Governed | Core + I8 (aplicación autoritativa mediante verificación de recepción en el servidor), delegación de intervalos de política, derechos mínimos del usuario F1~F7 |
| Mallangable Sealed | Governed + modo hidden (separación de roles, puerta de salida, separación de cachés por alcance), informe de LKR de Mallang-Bench |

## 10.4 Hoja de ruta de la especificación

| Versión | Objetivo |
| --- | --- |
| v0.1 (este documento) | Modelo conceptual, espacio de diseño, arquitectura de referencia, acoplamiento con la experiencia y el negocio, esquemas en borrador |
| v0.2 | Estabilización de los esquemas, formato del mapa de capacidades cerrado, publicación de la aplicación anfitriona de referencia |
| v0.3 | Conjunto de pruebas de conformidad, Mallang-Bench alfa |
| v1.0 | Al menos 2 implementaciones externas pasan el nivel Core, especificación de registros congelada |

Áreas donde las contribuciones son bienvenidas: O1 (suficiencia del contrato), O3 (interacción entre funcionalidades), O7 (promoción que preserva la privacidad), la aplicación anfitriona de referencia y las tablas de correspondencia de eventos de otros runtimes de agentes (5.6).

Referencias: [references.md](references.md) · Glosario: [glossary.md](glossary.md)
