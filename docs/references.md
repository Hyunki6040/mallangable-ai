# 참고 문헌

확인일: 2026-10-30. 웹 문서는 이후 바뀔 수 있습니다.

## 말랑한 소프트웨어와 최종 사용자 프로그래밍

- Geoffrey Litt, Josh Horowitz, Peter van Hardenberg, Todd Matthews. *Malleable Software: Restoring User Agency in a World of Locked-Down Apps.* Ink & Switch, 2025. https://www.inkandswitch.com/essay/malleable-software/
  - 이 에세이가 인용하는 MacLean et al.(1990) "User-Tailorable Systems: Pressing the Issues with Buttons"의 완만한 경사, Nardi & Miller의 '로컬 개발자' 관찰을 본문에서 재인용했습니다.
- Ink & Switch. *Patchwork* (실험 노트 07: AI 봇의 브랜치 편집과 선택 병합). https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · 코드(Apache-2.0): https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark.* 2023. https://www.inkandswitch.com/embark/
- W3C TAG. *The Rule of Least Power.* https://www.w3.org/2001/tag/doc/leastPower.html

## 소프트웨어 제품군과 가변성

- R. Capilla, J. Bosch, P. Trinidad, A. Ruiz-Cortés, M. Hinchey. "An overview of Dynamic Software Product Line architectures and techniques: Observations from research and industry." *Journal of Systems and Software* 91, 2014. https://research.chalmers.se/publication/198081

## 생성형 UI·확장 표준

- SEP-1865. *MCP Apps — Interactive User Interfaces for MCP.* https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp · 명세(2026-01-26): https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx
- Model Context Protocol 명세 2026-07-28 (변경 사항, 도구 annotations, elicitation). https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/server/tools · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
- A2UI: Agent-to-User Interface 명세 v0.9.1 (`createSurface`·`catalogId`). Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
- Lynx, A2UI 통합 문서(점진적 렌더링). https://lynxjs.org/react/genui/a2ui
- AG-UI: Agent-User Interaction Protocol (이벤트, interrupt). MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
- Agent Skills 명세 (SKILL.md 앞부분, allowed-tools는 Experimental). Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills
- Claude Code 플러그인 매니페스트 레퍼런스. https://code.claude.com/docs/en/plugins-reference
- Claude Code 훅 레퍼런스. https://code.claude.com/docs/en/hooks.md

## 실행 격리

- Endo / Hardened JavaScript (SES: lockdown, harden, Compartment). https://github.com/endojs/endo
- Tauri v2 Capability 레퍼런스. https://v2.tauri.app/reference/acl/capability

## 정책 엔진

- Cedar 권한 부여 의미론(forbid 우선, 기본 거부, 결정 정책 진단). https://docs.cedarpolicy.com/auth/authorization.html · 코드(Apache-2.0): https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler(SymCC): 정책 포함·동치·오류 없음 검증. https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Open Policy Agent 결정 로그. https://www.openpolicyagent.org/docs/management-decision-logs

## 병합

- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
- Kubernetes. *Server-Side Apply* (필드 소유권, `x-kubernetes-list-type`·`x-kubernetes-list-map-keys` 병합 표지). https://kubernetes.io/docs/reference/using-api/server-side-apply/
- Automerge. *Conflicts* (동시 쓰기의 결정적 승자와 진 값 보존). MIT. https://automerge.org/docs/reference/documents/conflicts/
- Mergiraf: 구문 인식 Git 병합 드라이버. GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf

## 하네스 개선과 평가

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · 코드(Apache-2.0): https://github.com/google-research/harness2
  - 숨은 검사 격리, 미채점 보고, 출처 맹검 판정, 하네스 지문(5.6, 5.8, 10.2)의 근거. 조사 노트: [research/harness2-analysis.md](research/harness2-analysis.md)
- JetBrains. *ThinkRail* — `pi` 에이전트를 감싸는 에이전트 IDE 호스트. Apache-2.0. https://github.com/JetBrains/thinkrail (커밋 `c10f8808`, 2026-11-03 확인)
  - 본 것을 근거로 한 되돌리기(5.5), 완료 신호와 대응표 관리(5.6), 판정 출력 처리(5.8), 기능 단위 격리(5.9), 승인 범위·지문(4.8), 동시 생성 귀속·읽기 실패·공유 수락 범위(6.4·6.5·6.9), 부작용 없는 목록(7.11), 용어팩 저장·출처(8.9)의 근거. 조사 노트: [research/thinkrail-analysis.md](research/thinkrail-analysis.md)

## 에이전트 보안

- E. Debenedetti et al. "Defeating Prompt Injections by Design" (CaMeL). arXiv:2503.18813, 2025. https://arxiv.org/abs/2503.18813 · 코드(Apache-2.0): https://github.com/google-research/camel-prompt-injection
- L. Beurer-Kellner et al. "Design Patterns for Securing LLM Agents against Prompt Injections." arXiv:2506.08837, 2025. https://arxiv.org/abs/2506.08837 · 요약: https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/
- Simon Willison. "The lethal trifecta for AI agents: private data, untrusted content, and external communication." 2025-06-16. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · 노트북(MIT): https://github.com/microsoft/fides
- Unit 42. "OpenClaw's Skill Marketplace and the Emerging AI Supply Chain Threat." 2026-06-23. https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/
- The Hacker News. "Researchers Find 341 Malicious ClawHub Skills Stealing Data from OpenClaw Users." 2026-02. https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html

## 공급망

- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance

## 관측

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/

## 경험 설계

- Jakob Nielsen. "Response Times: The 3 Important Limits." NN/g. https://www.nngroup.com/articles/response-times-3-important-limits/

## 유사 제품·프로젝트

- n.codes — 앱 안에서 사용자가 프롬프트로 기능을 생성. MIT. https://github.com/yungookim/n.codes
- Raycast Glaze 출시 보도. Implicator, 2026-03. https://www.implicator.ai/raycast-launches-glaze-a-platform-for-building-desktop-apps-through-ai-prompts/

## 모델 공급사 정책 (변동 잦음)

- The Register. "Anthropic clarifies ban on third-party Claude access." 2026-02-20. https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access
- D. Falcão da Silva. "Anthropic's Third-Party Claude Crackdown: How It Hit OpenCode, Zed, and the Wider Tooling Ecosystem." 2026-05-24. https://falcao.org/posts/anthropic-claude-access-crackdown-ecosystem-fallout/
