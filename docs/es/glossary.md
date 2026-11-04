<!-- LANG-BAR -->
[English](../en/glossary.md) · [한국어](../ko/glossary.md) · [简体中文](../zh-CN/glossary.md) · [日本語](../ja/glossary.md) · **Español**
<!-- /LANG-BAR -->

# Glosario

Se recogen juntos los términos para documentos de desarrollo y diseño y las expresiones que se usan en las pantallas para usuarios generales (nivel basic del paquete de léxico). El diccionario completo para pantallas de usuario está en [`examples/lexicon.es.yaml`](../../examples/lexicon.es.yaml).

| Término | Inglés | Definición | Expresión en pantalla de usuario | Primera aparición |
| --- | --- | --- | --- | --- |
| software maleable | malleable software | Software que el usuario puede adaptar a sus propias necesidades con poca fricción | — | 1.1 |
| Mallangable | Mallangable | Software en el que la IA crea cambios dentro de los puntos de extensión y estos se verifican, registran y propagan mediante contratos | — | 1.2 |
| anfitrión (host) | host | La aplicación que se quiere volver maleable. `H = ⟨C, X, K, Σ⟩` | aplicación | 2.2 |
| núcleo | core | La parte inmutable que distribuye el proveedor | — | 2.2 |
| punto de extensión | extension point | Un lugar donde el anfitrión permite modificaciones | lugar que se puede cambiar | 2.2 |
| capacidad | capability | Etiqueta con nombre de una facultad que una extensión puede usar | lo permitido | 2.2 |
| mapa de capacidades | capability map | Lista legible por máquina de puntos de extensión, permisos y esquemas | — | 2.2 |
| capa | layer | Un conjunto de cambios. Línea base, capa de usuario, etc. | — | 2.3 |
| aplicación efectiva | effective app | El resultado de componer las capas sobre el núcleo | — | 2.3 |
| cambio | change (δ) | Conjunto de intención, artefacto, contrato, permisos, profundidad, punto y procedencia | lo que cambié | 2.4 |
| funcionalidad | feature | Una sucesión de cambios que provienen de la misma intención | función que creé | 2.4 |
| intención | intent (ι) | Resumen del propósito expresado por una persona | — | 2.4 |
| contrato | contract (κ) | Condiciones de aceptación sobre el comportamiento observable de la aplicación efectiva | lista de promesas | 2.5 |
| profundidad | depth D1~D5 | Poder expresivo del artefacto y, a la vez, su nivel de riesgo | cuánto se cambia | 2.6 |
| regla de profundidad mínima | least-depth rule | Construir en la profundidad más baja que satisfaga el contrato | — | 2.6 |
| política | policy | Intervalo permitido para cada perilla | lo que permite la empresa | 2.7 |
| invariante | invariant I1~I10 | Propiedad que una implementación no debe romper por diseño | — | 2.9 |
| eje de diseño | design axis A1~A11 | Una dimensión de las decisiones de arquitectura | — | 3.2 |
| familia estructural | structural family | Una combinación de los ejes estructurales A1~A8 | — | 3.4 |
| perfil de referencia | reference profile P1~P7 | Punto representativo del espacio de diseño | — | 3.5 |
| perilla | knob | Una dimensión que se puede controlar | ajuste | 4.2 |
| techo · piso | ceiling · floor | Extremo del lado del riesgo · extremo del lado de la garantía del intervalo permitido | — | 4.2 |
| derechos mínimos del usuario | floor rights F1~F7 | Derechos del usuario que ninguna política puede eliminar | — | 4.6 |
| PDP · PEP | policy decision/enforcement point | Lugar donde se juzga la política · lugar donde se aplica | — | 4.8, 7.2 |
| plano | plane | Las 6 zonas de responsabilidad de la arquitectura | — | 5.1 |
| harness | harness | Envoltorio determinista que rodea al agente e impone procedimientos, herramientas, políticas, presupuesto y salidas | — | 5.6 |
| puerta de verificación | gate G0~G5 | Etapas de comprobación que hay que pasar antes de la activación | comprobación | 5.8 |
| evaluación ciega al origen | source-blind judging | Regla de G4 por la que el juez no conoce el generador, el harness ni la ruta de modelos del artefacto | — | 5.8 |
| intercambio en caliente | hot swap | Sustituir solo la ranura de extensión sin reiniciar el núcleo | — | 5.9 |
| modo seguro | safe mode | Iniciar con todas las capas de usuario apagadas | iniciar en modo básico | 5.9 |
| topología | topology | La estructura del historial de cambios (snapshot · fork · lineage · crdt) | — | 6.2 |
| linaje | lineage | Red de forks de una jerarquía de líneas base de varios niveles | — | 6.3 |
| línea base | baseline | La versión que sirve de punto de partida a las capas inferiores | versión base | 6.3 |
| deriva | drift | La distancia respecto a la última versión del nivel superior | atrasado respecto a la versión base | 6.3 |
| escalera de resolución | resolution ladder R0~R5 | El orden en que se prueban los métodos de resolución de conflictos, del más barato al más caro | — | 6.6 |
| fusión que preserva contratos | contract-preserving merge | Una fusión que satisface los contratos de ambas partes | unir | 6.7 |
| conflicto de intención | intent conflict | Estado en el que no se pueden satisfacer a la vez los contratos de ambas partes | parte que necesita una elección | 6.7 |
| caché de resoluciones | resolution cache | Reutilizar resoluciones de conflictos verificadas dentro del alcance de visibilidad | — | 6.8 |
| migración de contrato | contract migration | Debilitamiento o traslado de un contrato, permitido solo con consentimiento del usuario o mediante una tabla de correspondencia por retirada de un punto. Se registra con el trailer `Contract-Migrated` | — | 6.7 |
| promoción | promotion | Subir a la línea base superior una funcionalidad que ha convergido en los niveles inferiores | adoptado como función oficial | 6.10 |
| tríada letal | lethal trifecta | La combinación de datos privados, entrada no confiable y comunicación externa | — | 7.3 |
| etiqueta de visibilidad | visibility label | El alcance y la clase de los datos (V0~V3) | lo que ve el administrador | 7.5 |
| etiqueta de integridad | integrity label | El tercer componente de la etiqueta λ (trusted > untrusted). Los valores que deciden aumentos de permisos, envíos externos y la elección de punto de extensión deben ser trusted | — | 7.5 |
| puerta de salida | output gate | El único punto que puede rebajar una etiqueta (desclasificador) | — | 7.5 |
| capacidad de objeto | object capability | Modelo de seguridad en el que solo se actúa a través de objetos de permiso recibidos | — | 7.6 |
| nivel de tiempo | time tier T0~T4 | Patrones de experiencia según la franja de tiempo de respuesta | — | 8.4 |
| recibo de cambio | change receipt | Una tarjeta que indica qué cambió y cómo revertirlo | recibo | 8.6 |
| paquete de léxico | lexicon pack | Diccionario de expresiones por nivel, dominio e idioma para cada id de concepto | — | 8.9 |
| obtención de modelos | model sourcing | Con qué cuenta y a costa de quién se hace la inferencia | forma de conexión del motor de IA | 3.2 A9, 8.10 |
| tasa de rotura silenciosa | silent breakage rate (SBR) | Proporción de fusiones que pasaron los contratos públicos pero fallaron las pruebas ocultas | — | 10.2 |
| sin puntuar | unscored | Solicitud cuya puntuación misma falló. No se cuenta como 0 puntos; se excluye del denominador y se informa su número por separado | — | 10.2 |
