<!-- LANG-BAR -->
[English](../en/references.md) · [한국어](../ko/references.md) · [简体中文](../zh-CN/references.md) · **日本語** · [Español](../es/references.md)
<!-- /LANG-BAR -->

# 参考文献

確認日: 2026-10-30。Web 文書はその後変わることがあります。

## マリアブル・ソフトウェアとエンドユーザープログラミング

- Geoffrey Litt, Josh Horowitz, Peter van Hardenberg, Todd Matthews. *Malleable Software: Restoring User Agency in a World of Locked-Down Apps.* Ink & Switch, 2025. https://www.inkandswitch.com/essay/malleable-software/
  - このエッセイが引用する MacLean et al.(1990) "User-Tailorable Systems: Pressing the Issues with Buttons" のなだらかな勾配と、Nardi & Miller の「ローカル開発者」の観察を、本文で再引用しました。
- Ink & Switch. *Patchwork* (実験ノート 07: AI ボットによるブランチ編集と選択マージ)。https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · コード(Apache-2.0): https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark.* 2023. https://www.inkandswitch.com/embark/
- W3C TAG. *The Rule of Least Power.* https://www.w3.org/2001/tag/doc/leastPower.html

## ソフトウェアプロダクトラインと可変性

- R. Capilla, J. Bosch, P. Trinidad, A. Ruiz-Cortés, M. Hinchey. "An overview of Dynamic Software Product Line architectures and techniques: Observations from research and industry." *Journal of Systems and Software* 91, 2014. https://research.chalmers.se/publication/198081

## 生成 UI・拡張標準

- SEP-1865. *MCP Apps — Interactive User Interfaces for MCP.* https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp · 仕様(2026-01-26): https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx
- Model Context Protocol 仕様 2026-07-28 (変更点、ツール annotations、elicitation)。https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/server/tools · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- A2UI: Agent-to-User Interface 仕様 v0.9.1 (`createSurface`・`catalogId`)。Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
- Lynx、A2UI 統合ドキュメント(段階的レンダリング)。https://lynxjs.org/react/genui/a2ui
- AG-UI: Agent-User Interaction Protocol (イベント、interrupt)。MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
- Agent Skills 仕様 (SKILL.md の冒頭部分、allowed-tools は Experimental)。Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills
- Claude Code プラグインマニフェスト・リファレンス。https://code.claude.com/docs/en/plugins-reference
- Claude Code フック・リファレンス。https://code.claude.com/docs/en/hooks.md

## 実行の隔離

- Endo / Hardened JavaScript (SES: lockdown, harden, Compartment)。https://github.com/endojs/endo
- Tauri v2 Capability リファレンス。https://v2.tauri.app/reference/acl/capability

## ポリシーエンジン

- Cedar の認可セマンティクス(forbid 優先、デフォルト拒否、決定ポリシーの診断)。https://docs.cedarpolicy.com/auth/authorization.html · コード(Apache-2.0): https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler(SymCC): ポリシーの包含・同値・エラーなしの検証。https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Open Policy Agent の決定ログ。https://www.openpolicyagent.org/docs/management-decision-logs

## マージ

- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
- Kubernetes. *Server-Side Apply* (フィールド所有権、`x-kubernetes-list-type`・`x-kubernetes-list-map-keys` のマージ標識)。https://kubernetes.io/docs/reference/using-api/server-side-apply/
- Automerge. *Conflicts* (同時書き込みの決定的な勝者と、負けた値の保存)。MIT. https://automerge.org/docs/reference/documents/conflicts/
- Mergiraf: 構文を認識する Git マージドライバー。GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf

## ハーネスの改善と評価

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · コード(Apache-2.0): https://github.com/google-research/harness2
  - 隠しテストの隔離、未採点の報告、出所ブラインド判定、ハーネス指紋(5.6, 5.8, 10.2)の根拠。調査ノート: [research/harness2-analysis.md](research/harness2-analysis.md)
- JetBrains. *ThinkRail* — `pi` エージェントを包むエージェント IDE ホスト。Apache-2.0. https://github.com/JetBrains/thinkrail (コミット `c10f8808`、2026-11-03 確認)
  - 見たものを根拠とする取り消し(5.5)、完了シグナルと対応表の管理(5.6)、判定出力の処理(5.8)、機能単位の隔離(5.9)、承認範囲・指紋(4.8)、同時生成の帰属・読み取り失敗・共有受け入れ範囲(6.4・6.5・6.9)、副作用のない一覧(7.11)、用語パックの保存・出所(8.9)の根拠。調査ノート: [research/thinkrail-analysis.md](research/thinkrail-analysis.md)

## エージェントセキュリティ

- E. Debenedetti et al. "Defeating Prompt Injections by Design" (CaMeL). arXiv:2503.18813, 2025. https://arxiv.org/abs/2503.18813 · コード(Apache-2.0): https://github.com/google-research/camel-prompt-injection
- L. Beurer-Kellner et al. "Design Patterns for Securing LLM Agents against Prompt Injections." arXiv:2506.08837, 2025. https://arxiv.org/abs/2506.08837 · 要約: https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/
- Simon Willison. "The lethal trifecta for AI agents: private data, untrusted content, and external communication." 2025-06-16. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · ノートブック(MIT): https://github.com/microsoft/fides
- Unit 42. "OpenClaw's Skill Marketplace and the Emerging AI Supply Chain Threat." 2026-06-23. https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/
- The Hacker News. "Researchers Find 341 Malicious ClawHub Skills Stealing Data from OpenClaw Users." 2026-02. https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html

## サプライチェーン

- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance

## 観測

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/

## 体験設計

- Jakob Nielsen. "Response Times: The 3 Important Limits." NN/g. https://www.nngroup.com/articles/response-times-3-important-limits/

## 類似の製品・プロジェクト

- n.codes — アプリ内でユーザーがプロンプトで機能を生成する。MIT. https://github.com/yungookim/n.codes
- Raycast Glaze のリリース報道。Implicator, 2026-03. https://www.implicator.ai/raycast-launches-glaze-a-platform-for-building-desktop-apps-through-ai-prompts/

## モデルベンダーのポリシー (変動が多い)

- The Register. "Anthropic clarifies ban on third-party Claude access." 2026-02-20. https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access
- D. Falcão da Silva. "Anthropic's Third-Party Claude Crackdown: How It Hit OpenCode, Zed, and the Wider Tooling Ecosystem." 2026-05-24. https://falcao.org/posts/anthropic-claude-access-crackdown-ecosystem-fallout/
