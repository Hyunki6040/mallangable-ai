<!-- LANG-BAR -->
**English** · [한국어](../ko/references.md) · [简体中文](../zh-CN/references.md) · [日本語](../ja/references.md) · [Español](../es/references.md)
<!-- /LANG-BAR -->

# References

Checked on: 2026-10-30. Web documents may change afterward.

## Malleable software and end-user programming

- Geoffrey Litt, Josh Horowitz, Peter van Hardenberg, Todd Matthews. *Malleable Software: Restoring User Agency in a World of Locked-Down Apps.* Ink & Switch, 2025. https://www.inkandswitch.com/essay/malleable-software/
  - The gentle slope from MacLean et al. (1990) "User-Tailorable Systems: Pressing the Issues with Buttons" and Nardi & Miller's observation of 'local developers', both cited in this essay, are re-cited in the main text.
- Ink & Switch. *Patchwork* (lab notebook 07: branch editing by AI bots and selective merge). https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · code (Apache-2.0): https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark.* 2023. https://www.inkandswitch.com/embark/
- W3C TAG. *The Rule of Least Power.* https://www.w3.org/2001/tag/doc/leastPower.html

## Software product lines and variability

- R. Capilla, J. Bosch, P. Trinidad, A. Ruiz-Cortés, M. Hinchey. "An overview of Dynamic Software Product Line architectures and techniques: Observations from research and industry." *Journal of Systems and Software* 91, 2014. https://research.chalmers.se/publication/198081

## Generative UI and extension standards

- SEP-1865. *MCP Apps — Interactive User Interfaces for MCP.* https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp · specification (2026-01-26): https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx
- Model Context Protocol specification 2026-07-28 (changelog, tool annotations, elicitation). https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/server/tools · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- A2UI: Agent-to-User Interface specification v0.9.1 (`createSurface`, `catalogId`). Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
- Lynx, A2UI integration documentation (progressive rendering). https://lynxjs.org/react/genui/a2ui
- AG-UI: Agent-User Interaction Protocol (events, interrupt). MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
- Agent Skills specification (SKILL.md frontmatter, allowed-tools is Experimental). Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills
- Claude Code plugin manifest reference. https://code.claude.com/docs/en/plugins-reference
- Claude Code hooks reference. https://code.claude.com/docs/en/hooks.md

## Execution isolation

- Endo / Hardened JavaScript (SES: lockdown, harden, Compartment). https://github.com/endojs/endo
- Tauri v2 Capability reference. https://v2.tauri.app/reference/acl/capability

## Policy engines

- Cedar authorization semantics (forbid overrides, default deny, determining-policy diagnostics). https://docs.cedarpolicy.com/auth/authorization.html · code (Apache-2.0): https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler (SymCC): verifying policy implication, equivalence, and absence of errors. https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Open Policy Agent decision logs. https://www.openpolicyagent.org/docs/management-decision-logs

## Merging

- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
- Kubernetes. *Server-Side Apply* (field ownership, `x-kubernetes-list-type` and `x-kubernetes-list-map-keys` merge markers). https://kubernetes.io/docs/reference/using-api/server-side-apply/
- Automerge. *Conflicts* (deterministic winner of concurrent writes and preservation of losing values). MIT. https://automerge.org/docs/reference/documents/conflicts/
- Mergiraf: syntax-aware Git merge driver. GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf

## Harness improvement and evaluation

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · code (Apache-2.0): https://github.com/google-research/harness2
  - Basis for hidden-check isolation, unscored reporting, source-blind judging, and harness fingerprints (5.6, 5.8, 10.2). Research notes: [research/harness2-analysis.md](research/harness2-analysis.md)
- JetBrains. *ThinkRail* — an agent IDE host that wraps the `pi` agent. Apache-2.0. https://github.com/JetBrains/thinkrail (commit `c10f8808`, checked 2026-11-03)
  - Basis for revert based on what was seen (5.5), completion signal and mapping table maintenance (5.6), judge output handling (5.8), feature-level quarantine (5.9), approval scope and fingerprint (4.8), attribution of concurrent generation, read failures, and share acceptance scope (6.4, 6.5, 6.9), side-effect-free listing (7.11), and lexicon pack storage and provenance (8.9). Research notes: [research/thinkrail-analysis.md](research/thinkrail-analysis.md)

## Agent security

- E. Debenedetti et al. "Defeating Prompt Injections by Design" (CaMeL). arXiv:2503.18813, 2025. https://arxiv.org/abs/2503.18813 · code (Apache-2.0): https://github.com/google-research/camel-prompt-injection
- L. Beurer-Kellner et al. "Design Patterns for Securing LLM Agents against Prompt Injections." arXiv:2506.08837, 2025. https://arxiv.org/abs/2506.08837 · summary: https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/
- Simon Willison. "The lethal trifecta for AI agents: private data, untrusted content, and external communication." 2025-06-16. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · notebooks (MIT): https://github.com/microsoft/fides
- Unit 42. "OpenClaw's Skill Marketplace and the Emerging AI Supply Chain Threat." 2026-06-23. https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/
- The Hacker News. "Researchers Find 341 Malicious ClawHub Skills Stealing Data from OpenClaw Users." 2026-02. https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html

## Supply chain

- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance

## Observability

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/

## Experience design

- Jakob Nielsen. "Response Times: The 3 Important Limits." NN/g. https://www.nngroup.com/articles/response-times-3-important-limits/

## Similar products and projects

- n.codes — users generate features with prompts inside the app. MIT. https://github.com/yungookim/n.codes
- Raycast Glaze launch coverage. Implicator, 2026-03. https://www.implicator.ai/raycast-launches-glaze-a-platform-for-building-desktop-apps-through-ai-prompts/

## Model provider policies (change often)

- The Register. "Anthropic clarifies ban on third-party Claude access." 2026-02-20. https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access
- D. Falcão da Silva. "Anthropic's Third-Party Claude Crackdown: How It Hit OpenCode, Zed, and the Wider Tooling Ecosystem." 2026-05-24. https://falcao.org/posts/anthropic-claude-access-crackdown-ecosystem-fallout/
