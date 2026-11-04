<!-- LANG-BAR -->
[English](../en/references.md) · [한국어](../ko/references.md) · [简体中文](../zh-CN/references.md) · [日本語](../ja/references.md) · **Español**
<!-- /LANG-BAR -->

# Referencias

Fecha de consulta: 2026-10-30. Los documentos web pueden cambiar después.

## Software maleable y programación por usuarios finales

- Geoffrey Litt, Josh Horowitz, Peter van Hardenberg, Todd Matthews. *Malleable Software: Restoring User Agency in a World of Locked-Down Apps.* Ink & Switch, 2025. https://www.inkandswitch.com/essay/malleable-software/
  - En el texto principal se citan, a través de este ensayo, la pendiente suave de MacLean et al. (1990) "User-Tailorable Systems: Pressing the Issues with Buttons" y la observación de los "desarrolladores locales" de Nardi & Miller.
- Ink & Switch. *Patchwork* (nota de experimento 07: edición en ramas por bots de IA y fusión selectiva). https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · código (Apache-2.0): https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark.* 2023. https://www.inkandswitch.com/embark/
- W3C TAG. *The Rule of Least Power.* https://www.w3.org/2001/tag/doc/leastPower.html

## Líneas de productos de software y variabilidad

- R. Capilla, J. Bosch, P. Trinidad, A. Ruiz-Cortés, M. Hinchey. "An overview of Dynamic Software Product Line architectures and techniques: Observations from research and industry." *Journal of Systems and Software* 91, 2014. https://research.chalmers.se/publication/198081

## UI generativa y estándares de extensión

- SEP-1865. *MCP Apps — Interactive User Interfaces for MCP.* https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp · especificación (2026-01-26): https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx
- Especificación de Model Context Protocol 2026-07-28 (cambios, annotations de herramientas, elicitation). https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/server/tools · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- A2UI: especificación Agent-to-User Interface v0.9.1 (`createSurface`·`catalogId`). Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
- Lynx, documentación de integración de A2UI (renderizado progresivo). https://lynxjs.org/react/genui/a2ui
- AG-UI: Agent-User Interaction Protocol (eventos, interrupt). MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
- Especificación de Agent Skills (encabezado de SKILL.md; allowed-tools es Experimental). Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills
- Referencia del manifiesto de plugins de Claude Code. https://code.claude.com/docs/en/plugins-reference
- Referencia de hooks de Claude Code. https://code.claude.com/docs/en/hooks.md

## Aislamiento de ejecución

- Endo / Hardened JavaScript (SES: lockdown, harden, Compartment). https://github.com/endojs/endo
- Referencia de Capability de Tauri v2. https://v2.tauri.app/reference/acl/capability

## Motores de políticas

- Semántica de autorización de Cedar (prioridad de forbid, denegación por defecto, diagnóstico de las políticas que determinan la decisión). https://docs.cedarpolicy.com/auth/authorization.html · código (Apache-2.0): https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler (SymCC): verificación de inclusión, equivalencia y ausencia de errores en políticas. https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Registros de decisiones de Open Policy Agent. https://www.openpolicyagent.org/docs/management-decision-logs

## Fusión

- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
- Kubernetes. *Server-Side Apply* (propiedad de campos, marcadores de fusión `x-kubernetes-list-type`·`x-kubernetes-list-map-keys`). https://kubernetes.io/docs/reference/using-api/server-side-apply/
- Automerge. *Conflicts* (ganador determinista de las escrituras simultáneas y conservación de los valores perdedores). MIT. https://automerge.org/docs/reference/documents/conflicts/
- Mergiraf: controlador de fusión de Git consciente de la sintaxis. GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf

## Mejora y evaluación del harness

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · código (Apache-2.0): https://github.com/google-research/harness2
  - Fundamento del aislamiento de comprobaciones ocultas, el informe de elementos sin puntuar (unscored), el juicio con evaluación ciega al origen (source-blind judging) y la huella del harness (5.6, 5.8, 10.2). Notas de investigación: [research/harness2-analysis.md](research/harness2-analysis.md)
- JetBrains. *ThinkRail*: anfitrión de IDE de agentes que envuelve al agente `pi`. Apache-2.0. https://github.com/JetBrains/thinkrail (commit `c10f8808`, consultado el 2026-11-03)
  - Fundamento de la reversión basada en lo visto (5.5), la señal de finalización y la gestión de tablas de correspondencia (5.6), el tratamiento de la salida del juicio (5.8), el aislamiento por funcionalidad (5.9), el ámbito y la huella de las aprobaciones (4.8), la atribución en generaciones simultáneas, los fallos de lectura y el alcance de aceptación de lo compartido (6.4·6.5·6.9), las listas sin efectos secundarios (7.11) y el almacenamiento y origen del paquete de léxico (8.9). Notas de investigación: [research/thinkrail-analysis.md](research/thinkrail-analysis.md)

## Seguridad de agentes

- E. Debenedetti et al. "Defeating Prompt Injections by Design" (CaMeL). arXiv:2503.18813, 2025. https://arxiv.org/abs/2503.18813 · código (Apache-2.0): https://github.com/google-research/camel-prompt-injection
- L. Beurer-Kellner et al. "Design Patterns for Securing LLM Agents against Prompt Injections." arXiv:2506.08837, 2025. https://arxiv.org/abs/2506.08837 · resumen: https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/
- Simon Willison. "The lethal trifecta for AI agents: private data, untrusted content, and external communication." 2025-06-16. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · notebook (MIT): https://github.com/microsoft/fides
- Unit 42. "OpenClaw's Skill Marketplace and the Emerging AI Supply Chain Threat." 2026-06-23. https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/
- The Hacker News. "Researchers Find 341 Malicious ClawHub Skills Stealing Data from OpenClaw Users." 2026-02. https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html

## Cadena de suministro

- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance

## Observabilidad

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/

## Diseño de la experiencia

- Jakob Nielsen. "Response Times: The 3 Important Limits." NN/g. https://www.nngroup.com/articles/response-times-3-important-limits/

## Productos y proyectos similares

- n.codes: el usuario genera funcionalidades dentro de la aplicación mediante prompts. MIT. https://github.com/yungookim/n.codes
- Noticia del lanzamiento de Raycast Glaze. Implicator, 2026-03. https://www.implicator.ai/raycast-launches-glaze-a-platform-for-building-desktop-apps-through-ai-prompts/

## Políticas de los proveedores de modelos (cambian a menudo)

- The Register. "Anthropic clarifies ban on third-party Claude access." 2026-02-20. https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access
- D. Falcão da Silva. "Anthropic's Third-Party Claude Crackdown: How It Hit OpenCode, Zed, and the Wider Tooling Ecosystem." 2026-05-24. https://falcao.org/posts/anthropic-claude-access-crackdown-ecosystem-fallout/
