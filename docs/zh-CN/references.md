<!-- LANG-BAR -->
[English](../en/references.md) · [한국어](../ko/references.md) · **简体中文** · [日本語](../ja/references.md) · [Español](../es/references.md)
<!-- /LANG-BAR -->

# 参考文献

确认日期：2026-10-30。网页文档此后可能发生变化。

## 可塑软件与最终用户编程

- Geoffrey Litt, Josh Horowitz, Peter van Hardenberg, Todd Matthews. *Malleable Software: Restoring User Agency in a World of Locked-Down Apps.* Ink & Switch, 2025. https://www.inkandswitch.com/essay/malleable-software/
  - 正文转引了这篇文章所引用的 MacLean et al.（1990）"User-Tailorable Systems: Pressing the Issues with Buttons"中的平缓坡度，以及 Nardi & Miller 关于"本地开发者"的观察。
- Ink & Switch. *Patchwork*（实验笔记 07：AI 机器人的分支编辑与选择性合并）。https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · 代码（Apache-2.0）：https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark.* 2023. https://www.inkandswitch.com/embark/
- W3C TAG. *The Rule of Least Power.* https://www.w3.org/2001/tag/doc/leastPower.html

## 软件产品线与可变性

- R. Capilla, J. Bosch, P. Trinidad, A. Ruiz-Cortés, M. Hinchey. "An overview of Dynamic Software Product Line architectures and techniques: Observations from research and industry." *Journal of Systems and Software* 91, 2014. https://research.chalmers.se/publication/198081

## 生成式 UI·扩展标准

- SEP-1865. *MCP Apps — Interactive User Interfaces for MCP.* https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp · 规范（2026-01-26）：https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx
- Model Context Protocol 规范 2026-07-28（变更内容、工具 annotations、elicitation）。https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/server/tools · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- A2UI: Agent-to-User Interface 规范 v0.9.1（`createSurface`·`catalogId`）。Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
- Lynx，A2UI 集成文档（渐进式渲染）。https://lynxjs.org/react/genui/a2ui
- AG-UI: Agent-User Interaction Protocol（事件、interrupt）。MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
- Agent Skills 规范（SKILL.md 前置部分，allowed-tools 为 Experimental）。Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills
- Claude Code 插件清单参考。https://code.claude.com/docs/en/plugins-reference
- Claude Code 钩子参考。https://code.claude.com/docs/en/hooks.md

## 执行隔离

- Endo / Hardened JavaScript（SES：lockdown、harden、Compartment）。https://github.com/endojs/endo
- Tauri v2 Capability 参考。https://v2.tauri.app/reference/acl/capability

## 策略引擎

- Cedar 授权语义（forbid 优先、默认拒绝、决策策略诊断）。https://docs.cedarpolicy.com/auth/authorization.html · 代码（Apache-2.0）：https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler（SymCC）：策略包含·等价·无错误验证。https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Open Policy Agent 决策日志。https://www.openpolicyagent.org/docs/management-decision-logs

## 合并

- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
- Kubernetes. *Server-Side Apply*（字段所有权，`x-kubernetes-list-type`·`x-kubernetes-list-map-keys` 合并标记）。https://kubernetes.io/docs/reference/using-api/server-side-apply/
- Automerge. *Conflicts*（并发写入的确定性胜者与落败值的保留）。MIT. https://automerge.org/docs/reference/documents/conflicts/
- Mergiraf：语法感知的 Git 合并驱动。GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf

## 执行框架的改进与评估

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · 代码（Apache-2.0）：https://github.com/google-research/harness2
  - 隐藏检查隔离、未评分报告、来源盲评、执行框架指纹（5.6、5.8、10.2）的依据。调研笔记：[research/harness2-analysis.md](research/harness2-analysis.md)
- JetBrains. *ThinkRail*——包裹 `pi` 智能体的智能体 IDE 宿主。Apache-2.0. https://github.com/JetBrains/thinkrail（提交 `c10f8808`，2026-11-03 确认）
  - 依据所见内容回退（5.5）、完成信号与对应表管理（5.6）、评判输出处理（5.8）、以功能为单位的隔离（5.9）、批准范围·指纹（4.8）、并发生成的归属·读取失败·共享接受范围（6.4·6.5·6.9）、无副作用的列表（7.11）、术语包的存储·来源（8.9）的依据。调研笔记：[research/thinkrail-analysis.md](research/thinkrail-analysis.md)

## 智能体安全

- E. Debenedetti et al. "Defeating Prompt Injections by Design" (CaMeL). arXiv:2503.18813, 2025. https://arxiv.org/abs/2503.18813 · 代码（Apache-2.0）：https://github.com/google-research/camel-prompt-injection
- L. Beurer-Kellner et al. "Design Patterns for Securing LLM Agents against Prompt Injections." arXiv:2506.08837, 2025. https://arxiv.org/abs/2506.08837 · 摘要：https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/
- Simon Willison. "The lethal trifecta for AI agents: private data, untrusted content, and external communication." 2025-06-16. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · 笔记本（MIT）：https://github.com/microsoft/fides
- Unit 42. "OpenClaw's Skill Marketplace and the Emerging AI Supply Chain Threat." 2026-06-23. https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/
- The Hacker News. "Researchers Find 341 Malicious ClawHub Skills Stealing Data from OpenClaw Users." 2026-02. https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html

## 供应链

- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance

## 可观测性

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/

## 体验设计

- Jakob Nielsen. "Response Times: The 3 Important Limits." NN/g. https://www.nngroup.com/articles/response-times-3-important-limits/

## 类似产品·项目

- n.codes——在应用内由用户通过提示生成功能。MIT. https://github.com/yungookim/n.codes
- Raycast Glaze 发布报道。Implicator, 2026-03. https://www.implicator.ai/raycast-launches-glaze-a-platform-for-building-desktop-apps-through-ai-prompts/

## 模型供应商政策（变动频繁）

- The Register. "Anthropic clarifies ban on third-party Claude access." 2026-02-20. https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access
- D. Falcão da Silva. "Anthropic's Third-Party Claude Crackdown: How It Hit OpenCode, Zed, and the Wider Tooling Ecosystem." 2026-05-24. https://falcao.org/posts/anthropic-claude-access-crackdown-ecosystem-fallout/
