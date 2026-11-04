<!-- LANG-BAR -->
[English](../../en/research/prior-art-survey.md) · **한국어** · [简体中文](../../zh-CN/research/prior-art-survey.md) · [日本語](../../ja/research/prior-art-survey.md) · [Español](../../es/research/prior-art-survey.md)
<!-- /LANG-BAR -->

# 조사 노트 — 선행 사례 조사 (오픈소스·명세·에이전트 표준)

> 이 노트의 결론: 이 명세가 새로 정의한 것(계약 보존 병합, 계보 전파, 구간 위임, 권리 하한)과 **겹치는 표준은 없다.** 다만 주변 부품은 이미 표준화돼 있고, 지금 명세는 그 이름을 쓰지 않거나 2차 출처로 인용하고 있다. 가져올 것은 다섯 갈래다. ① 선언형 레이어 합성 `⊕`의 기본 의미를 **JSON Merge Patch(RFC 7396)** 로 고정하고, 목록 병합 규칙은 Kubernetes Server-Side Apply처럼 **스키마가 선언**하게 한다. ② 정보 흐름 라벨(7.5)에 **무결성 축**을 더한다(FIDES·CaMeL). ③ 정책 단조 축소(I5)를 **Cedar의 정책 포함 검증**으로 기계 확인한다. ④ 텔레메트리(5.11)를 **OpenTelemetry GenAI 속성 이름**에 맞춘다. ⑤ MCP 최신판(2026-07-28)의 **URL 모드 elicitation**과 Sampling 폐기를 모델 연결(8.10)에 반영한다.

- 확인일: 2026-10-30
- 방법: 저장소는 `gh api`로 메타데이터·라이선스 파일·명세 원문을 읽었고, 웹 문서는 공식 사이트만 가져왔습니다. 코드는 실행하지 않았습니다. 인용한 URL은 모두 `curl -L`로 200 응답을 확인했습니다(ACM 디지털 라이브러리는 자동 요청을 403으로 막아 DOI만 적었습니다).
- 범위: 이 장은 기존 문서를 고치지 않습니다. 3절의 편집안을 반영할지는 따로 결정합니다.

## 0. 확인한 것과 못 한 것

| 항목 | 상태 | 비고 |
| --- | --- | --- |
| MCP 최신 개정판 | 확인 | `2026-07-28`(2026-07-28 릴리스). 저장소 `docs/specification/2026-07-28/changelog.mdx` 원문 |
| MCP Apps | 확인 | `modelcontextprotocol/ext-apps`의 `specification/2026-01-26/apps.mdx`. 확장 id `io.modelcontextprotocol/ui` |
| OpenTelemetry GenAI 규약 | 확인 | `open-telemetry/semantic-conventions`에서 **`semantic-conventions-genai` 저장소로 옮겨짐**. 문서 상태는 전부 Development |
| A2UI | 확인 | 저장소가 `a2ui-project/a2ui`로 옮겨짐. 현재 v0.9.1, v1.0은 RC |
| Cedar 결정 규칙·검증기 | 확인 | 공식 문서와 `cedar-policy-symcc` README |
| Patchwork 내부 구조 | 일부 | 프로젝트 페이지와 실험 노트 07만 읽음. `inkandswitch/patchwork-system` 저장소는 라이선스 표기 없음 |
| Boxer 원문 | 못 읽음 | ACM이 자동 요청 차단. 서지 정보만 확인 |
| Chrome·Figma·VS Code 문서의 라이선스 | 확인 안 함 | 제품 문서이므로 인용만 하고 문구를 옮기지 않음 |

## 1. 항목별 조사

판정: **채택** = 인용하고 필드 이름·의미를 맞춘다 / **참고** = 관련 연구로 인용만 / **무관** = 넣지 않는다.
"대응" 칸은 이 명세의 절 번호와 스키마 파일입니다.

### 1.1 말랑한 소프트웨어 연구

| 항목 | 무엇인가 | 1차 출처 | 라이선스 | 대응 | 판정 |
| --- | --- | --- | --- | --- | --- |
| Malleable software 에세이 (Ink & Switch, 2025) | 잠긴 앱에서 사용자 주체성을 되찾자는 에세이. 완만한 경사·로컬 개발자 개념 정리 | https://www.inkandswitch.com/essay/malleable-software/ | 에세이(표기 없음) | 1.5, 2.6 | 이미 인용됨. 유지 |
| Potluck (2022) | 텍스트 위에 검색·수식·동적 주석을 겹쳐 점진적으로 구조를 더함. 주석은 원문을 바꾸지 않는 겹침 레이어 | https://www.inkandswitch.com/potluck/ | 에세이 | 2.3 레이어, 2.6 D1~D3 | **참고**. "원본을 건드리지 않는 겹침 레이어"의 선례 |
| Embark (2023) | 여행 계획 문서 하나에 데이터·계산·뷰를 함께 둬 앱을 해체 | https://www.inkandswitch.com/embark/ | 에세이 | 10.1 O8 (앱을 넘는 도구) | **참고** |
| Patchwork (2024~) | 글·그림 등 비코드 문서의 범용 버전 관리. 실험 노트에서 **AI 봇이 브랜치에서 편집하고, 사람이 diff를 보고 일부만 병합하며, 이력에 봇 편집이 표시**됨 | https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/ | 저장소 표기 없음 | 6.4 `exp/*` 브랜치, 6.11 `Agent:` 트레일러, 8.6 영수증 | **참고**. 현재 references.md의 "Universal Version Control" 링크는 연구실 목록 페이지라 Patchwork 페이지로 바꾸는 편이 정확 |
| Cambria (2020) | 양방향 렌즈로 스키마 버전 사이 데이터를 변환 | https://www.inkandswitch.com/cambria/ · https://github.com/inkandswitch/cambria-project | MIT | 5.9 `migrate(prev)`, `extension-manifest` `state.migrate_from` | **참고**. 상태 인계를 단방향 `migrate`로 둔 현재 설계는 충분. 양방향이 필요해지면 근거 |
| Webstrates (UIST 2015) | DOM 변경을 동기화해 문서와 앱의 경계를 흐림. 말랑함·공유·분산·계산 4원칙 | https://webstrates.net/ · https://github.com/Webstrates/Webstrates | Apache-2.0 | 6.13 CRDT 위의 코드 위험 | **참고**. 실행 코드를 실시간 공유한 선례라 S7의 근거 사례로 적합 |
| Boxer (diSessa & Abelson, CACM 29(9), 1986) | 비전문가가 다시 짜 맞출 수 있는 계산 매체 | DOI 10.1145/6592.6595 | 논문 | 1.5 | **참고**. Smalltalk 계보는 1차 출처를 찾지 않아 제외 |

### 1.2 확장·플러그인 매니페스트

| 항목 | 무엇인가 | 1차 출처 | 라이선스 | 대응 | 판정 |
| --- | --- | --- | --- | --- | --- |
| VS Code 기여 지점·활성화 이벤트 | `contributes`(commands·menus·views·keybindings·configuration·`languageModelTools` 등)로 확장 지점을 선언. 1.74부터 기여 지점이 활성화 이벤트를 자동 암시 | https://code.visualstudio.com/api/references/contribution-points · https://code.visualstudio.com/api/references/activation-events | 코드 MIT, 문서 확인 안 함 | 2.2 확장 지점 `kind`, `capability-map` | **참고**. `kind`(token·command·view·hook·service)와 대응이 자연스러움 |
| VS Code Workspace Trust | `capabilities.untrustedWorkspaces.supported: true / false / "limited"`. 신뢰 안 된 작업 공간은 Restricted Mode로 열려 자동 실행이 막힘 | https://code.visualstudio.com/api/extension-guides/workspace-trust | 문서 | 4.6 F2 세이프 모드, 6.9 받은 공유 | **참고** |
| Chrome MV3 권한 | `permissions`·`optional_permissions`·`host_permissions`·`optional_host_permissions`. **경고가 붙는 권한을 업데이트에서 추가하면 사용자가 수락할 때까지 확장이 꺼짐** | https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions | 문서 | I4, 6.5 `delta_permissions`, 6.9 subscribe | **참고**. I4의 실제 대규모 선례. 현재 명세 규칙(권한 증가 → 제안)과 같은 방향 |
| Figma 플러그인 매니페스트 | `networkAccess.allowedDomains`(`["none"]` 가능)·`reasoning`(와일드카드면 필수)·`devAllowedDomains`, `permissions` | https://developers.figma.com/docs/plugins/manifest/ | 문서 | `extension-manifest` `network.allow` | **참고**. "허용 사유" 필드는 4절 후보 |
| Obsidian 커뮤니티 플러그인 | 공식 문서가 "플러그인을 특정 권한으로 제한할 수 없다", 파일·네트워크·프로그램 설치 접근 가능하다고 명시. 기본은 Restricted mode | https://obsidian.md/help/plugin-security | 앱 독점, `obsidian-api` MIT | 7.6, 7.7 | **참고**. 격리 없는 확장의 반례로 인용 가치 |
| WASM Component Model / WIT | `world`가 컴포넌트의 import·export를 선언하고 호스트는 import한 것만 공급. 패키지에 버전(`wasi:http@0.2.0`) | https://component-model.bytecodealliance.org/design/wit.html · https://github.com/WebAssembly/component-model | Apache-2.0 | 7.6 객체 권한, `SandboxHost` `lang` 어댑터, 매니페스트 `permissions` | **참고**. `wasm` 산출물이라면 매니페스트 `permissions` ↔ world import로 1:1 대응 가능 |
| Extism | WASM 플러그인 프레임워크. 매니페스트에 `wasm[].hash`, `memory.max_pages`, `allowed_hosts`, `allowed_paths`, `config` | https://extism.org/docs/concepts/manifest · https://github.com/extism/extism | BSD-3-Clause | `extension-manifest` `artifact.content_hash`, `network.allow`, `resources.memory_mb` | **참고**. 같은 개념이 이미 있음. 이름을 맞출 이유는 약함 |
| Tauri v2 capability | 이미 인용됨 | (references.md) | | 7.6 | 유지 |
| Endo / SES | 이미 인용됨 | (references.md) | Apache-2.0 | 7.6 | 유지 |

### 1.3 에이전트 프로토콜·하네스 이벤트

| 항목 | 무엇인가 | 1차 출처 | 라이선스 | 대응 | 판정 |
| --- | --- | --- | --- | --- | --- |
| MCP 2026-07-28 | 무상태화(`initialize` 제거, 요청마다 `_meta`에 버전·클라이언트 능력), `server/discover`, 다중 왕복 요청(MRTR: `resultType: "input_required"`), tasks는 공식 확장으로 이동, **Roots·Sampling·Logging 폐기 예정**, `_meta`의 `traceparent` 규약(SEP-414) | https://modelcontextprotocol.io/specification/2026-07-28/changelog | Apache-2.0(명세, MIT에서 전환 중), 문서 CC-BY-4.0 | 5.3 `ModelPort`, 5.6, 8.10 | **채택**. 8.10 `sub` 경로를 MCP Sampling 위에 설계하면 안 됨 |
| MCP 도구 annotations | `readOnlyHint`·`destructiveHint`·`idempotentHint`·`openWorldHint`. **신뢰된 서버가 아니면 클라이언트는 annotations를 믿으면 안 됨(MUST)** | https://modelcontextprotocol.io/specification/2026-07-28/server/tools | 위와 같음 | `capability-map` `capability.risk` | **채택**. `risk` 값과 대응표를 둠(3절 E-10) |
| MCP elicitation | form 모드와 URL 모드. **비밀값·자격 증명은 form 모드로 받으면 안 되고 URL 모드를 써야 함(MUST)** | https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation | 위와 같음 | 8.10 연결 열쇠, I6 | **채택** |
| MCP 권한 부여 | OAuth 2.1, Protected Resource Metadata(RFC 9728), 자원 지시자(RFC 8707), `iss` 검증(RFC 9207) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | 위와 같음 | 2.1 위임, 7.2 | **참고**. 에이전트 α가 "사람 위임을 받은 단기 주체"라는 I4·I9 설명의 구현 근거 |
| MCP Apps (SEP-1865) | `ui://` 자원, `text/html;profile=mcp-app`, 샌드박스 iframe 의무, `_meta.ui.csp`(`connectDomains`·`resourceDomains`·`frameDomains`·`baseUriDomains`), `permissions`(camera·microphone·geolocation·clipboardWrite) | https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx | 위와 같음 | 3.2 A4 `frame`, `extension-manifest` `network` | 이미 인용됨. **채택 유지**. 날짜 붙은 명세 경로로 링크를 고정 |
| MCP-UI | MCP Apps의 원형. 지금은 MCP Apps 호환 SDK | https://github.com/MCP-UI-Org/mcp-ui | Apache-2.0 | | **무관**(MCP Apps로 충분) |
| AG-UI | 에이전트↔프런트엔드 이벤트 프로토콜. `RUN_STARTED`/`RUN_FINISHED`/`RUN_ERROR`, `STEP_*`, `TOOL_CALL_*`, `STATE_SNAPSHOT`/`STATE_DELTA`(**RFC 6902 JSON Patch**), `SUBAGENT_*`. 사람 승인은 `RunFinished`의 `outcome: { type: "interrupt" }` 후 `resume[]`로 새 실행 | https://docs.ag-ui.com/concepts/events · https://docs.ag-ui.com/concepts/interrupts · https://github.com/ag-ui-protocol/ag-ui | MIT | 5.6 이벤트 모델, 8.5 진행 표현, 2.8 `승인대기` | **채택**(대응표). 경험면↔생성면 사이의 전송 규격으로 그대로 쓸 수 있음 |
| A2A v1.0 | 불투명한 에이전트 사이의 작업 프로토콜. `AgentCard`, 작업 상태 `TASK_STATE_SUBMITTED / WORKING / INPUT_REQUIRED / AUTH_REQUIRED / COMPLETED / FAILED / CANCELED / REJECTED` | https://a2a-protocol.org/latest/specification/ · https://github.com/a2aproject/A2A | Apache-2.0 | 5.3 `JobOrchestrator`, 2.8 생애주기 | **참고**. 서버 병합·승격 잡을 외부 에이전트에 맡길 때의 어댑터 후보 |
| OpenTelemetry GenAI 규약 | `gen_ai.operation.name`(`invoke_agent`·`execute_tool`·`create_agent`·`invoke_workflow`), `gen_ai.agent.id`, `gen_ai.usage.input_tokens`·`output_tokens`, `gen_ai.tool.name`, MCP 속성 `mcp.method.name`. **상태 Development** | https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/ | Apache-2.0 | 5.11 텔레메트리 | **채택**(속성 이름만). 안정판이 아니므로 버전 고정 필요 |
| OpenAI Agents SDK 트레이싱 | trace(`workflow_name`·`trace_id`·`group_id`), span(`agent`·`generation`·`function`·`guardrail`·`handoff`·`custom`), `trace_include_sensitive_data` | https://openai.github.io/openai-agents-python/tracing/ · https://github.com/openai/openai-agents-python | MIT | 5.11, 7.5 해제 규칙 | **참고**. 민감 데이터 기본 포함(True)은 이 명세의 기본값과 반대 |
| Claude Code 훅 | 이벤트 32개, 처리기 5종(`command`·`http`·`mcp_tool`·`prompt`·`agent`), `PreToolUse`의 `permissionDecision`(`allow`·`deny`·`ask`·`defer`)·`updatedInput`, 관리 설정 `allowManagedHooksOnly` | https://code.claude.com/docs/en/hooks.md | 제품 문서 | 5.6 대응표 | 이미 인용됨. 대응표에 `PostToolUseFailure`(E5), `Elicitation`(E6) 추가 가능 |
| Claude Code 플러그인 | `.claude-plugin/plugin.json`(`name`만 필수, `skills`·`hooks`·`mcpServers`·`userConfig`의 `sensitive`), `claude plugin validate` | https://code.claude.com/docs/en/plugins-reference | 제품 문서 | 5.6 하네스 배포, 8.10 `sub` | 이미 인용됨. **references.md 링크가 스페인어판(`/docs/es/`)이라 영어판 레퍼런스로 교체** |
| Agent Skills 명세 | `SKILL.md` 앞부분 `name`(64자)·`description`(1024자)·`license`·`compatibility`·`metadata`·`allowed-tools`(**Experimental**) | https://agentskills.io/specification · https://github.com/agentskills/agentskills | Apache-2.0 | 5.6 "스킬은 절차, 하네스는 강제" | **채택**. 현재 근거가 2차 출처(Shiplight)라 1차 명세로 교체. 주장 내용은 1차 출처와 일치 |

### 1.4 정책 엔진·프롬프트 인젝션 방어

| 항목 | 무엇인가 | 1차 출처 | 라이선스 | 대응 | 판정 |
| --- | --- | --- | --- | --- | --- |
| Cedar | 주체·행동·자원·맥락 요청. **forbid가 permit을 이기고, 맞는 permit이 없으면 Deny**. 응답에 결정을 만든 정책 id(determining policies)와 오류 목록. 오류 난 정책은 건너뜀 | https://docs.cedarpolicy.com/auth/authorization.html · https://github.com/cedar-policy/cedar | Apache-2.0 | 4.8 `decide(req)`, `PolicyDecisionPoint` | **채택**(PDP 어댑터) |
| Cedar SymCC | 정책 집합을 SMT로 옮겨 **포함(`check_implies`)·동치·항상 거부·오류 없음**을 반례와 함께 검증. 검증기는 Lean으로 형식 검증됨 | https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc | Apache-2.0 | **I5 `p_child ⊑ p_parent`** | **채택**. I5를 "정책 저장소 검사"에서 증명 가능한 검사로 올림 |
| OPA / Rego | CNCF 졸업 프로젝트. 결정 로그에 `decision_id`, `bundles.revision`, `path`, `input`, `result`, `erased`·`masked`(JSON Pointer), `trace_id`·`span_id` | https://www.openpolicyagent.org/docs/management-decision-logs · https://github.com/open-policy-agent/opa | Apache-2.0 | 5.11, 7.9 가명화 | **채택**(결정 로그 필드 이름). 정책 언어로는 Cedar보다 분석성이 약해 PDP 1순위는 아님 |
| CaMeL (DeepMind 2025) | 이미 인용됨. 코드 공개 | https://github.com/google-research/camel-prompt-injection | Apache-2.0 | 7.4 | 유지. 코드 링크 추가 |
| FIDES (Microsoft 2025) | 계획자가 **기밀성과 무결성 라벨**을 동적 오염 추적으로 따라가며 정책을 결정적으로 강제. 정보를 선택적으로 숨기는 기본 연산 제시 | https://arxiv.org/abs/2505.23643 · https://github.com/microsoft/fides | 노트북 MIT | **7.5 정보 흐름 라벨** | **채택**. 7.5는 기밀성(V0~V3)만 있고 무결성 축이 없음 |
| Dual LLM 패턴 (Willison 2023) | 특권 LLM과 격리 LLM, 그 사이의 비-LLM 제어기. 신뢰 불가 값은 `$VAR1` 같은 참조로만 전달 | https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | 블로그 | 7.3 격리 판독자 | **채택**(인용). 7.4가 설계 패턴 논문을 거쳐 간접 인용 중 |
| 치명적 3요소 (Willison 2025) | 이미 인용됨 | | | 7.3 | 유지 |

### 1.5 병합·계보

| 항목 | 무엇인가 | 1차 출처 | 라이선스 | 대응 | 판정 |
| --- | --- | --- | --- | --- | --- |
| JSON Merge Patch (RFC 7396) | 객체 키는 덮어쓰고, `null`은 삭제, **배열은 통째로 교체** | https://www.rfc-editor.org/rfc/rfc7396 | IETF Trust | **2.3 `⊕`**, 6.6 R2 | **채택**. `⊕`의 "키 단위 덮어쓰기"가 정확히 이 의미인데 이름이 없음 |
| JSON Patch (RFC 6902) | 연산 목록(add·remove·replace·move·copy·test) | https://www.rfc-editor.org/rfc/rfc6902 | IETF Trust | 8.5 부분 미리보기, AG-UI `STATE_DELTA` | **참고** |
| Kubernetes Server-Side Apply | 필드 관리자가 필드 소유권을 기록(`managedFields`). 스키마 표지 `x-kubernetes-list-type: atomic / set / map`, `x-kubernetes-list-map-keys`, `x-kubernetes-map-type: atomic / granular`로 병합 방식을 **스키마가 선언**. 다른 관리자 소유 필드를 바꾸면 충돌 | https://kubernetes.io/docs/reference/using-api/server-side-apply/ | 문서 | **6.6 R2** "스키마가 규칙을 선언", 6.11 `Overrides:` | **채택**. R2가 말만 하고 스키마 필드가 없음 |
| Kustomize | base·overlay·component. component는 여러 overlay에 섞어 넣는 재사용 기능 묶음. `patches`는 strategic merge와 JSON 6902 | https://kubectl.docs.kubernetes.io/guides/config_management/components/ · https://github.com/kubernetes-sigs/kustomize | Apache-2.0 | 6.2 lineage, 6.9 기능 단위 공유 | **참고**. "기준판 위의 오버레이" 실무 선례 |
| Automerge | CRDT. 같은 키 동시 쓰기는 연산 id로 결정적 승자를 고르되 **진 값은 `getConflicts()`로 보존** | https://automerge.org/docs/reference/documents/conflicts/ · https://github.com/automerge/automerge | MIT | 6.13 CRDT 의미 충돌 | **참고**. 현재 3.2 A6 링크가 Ink & Switch 목록 페이지라 Automerge로 바꿈 |
| Yjs | CRDT 공유 타입 | https://yjs.dev/ · https://github.com/yjs/yjs | MIT | 3.2 A6 `crdt` | **참고** |
| Mergiraf | tree-sitter 기반 구문 인식 병합 드라이버 | https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf | **GPL-3.0-only** (`Cargo.toml`) | 6.6 R1 | 이미 인용됨. 링크를 docs.rs에서 공식 사이트로 바꾸고 라이선스를 명시. 6.6의 "강한 카피레프트" 경고의 실제 대상 |

### 1.6 생성형 UI

| 항목 | 무엇인가 | 1차 출처 | 라이선스 | 대응 | 판정 |
| --- | --- | --- | --- | --- | --- |
| A2UI v0.9.1 | 선언형 JSON UI. 메시지 4종 `createSurface`·`updateComponents`·`updateDataModel`·`deleteSurface`. 표면마다 **`catalogId`**(URI 형식 문자열)를 고정. 승인된 카탈로그 컴포넌트만 렌더 | https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md | Apache-2.0 | 2.6 D3, `capability-map` `catalog`, 8.5 | **채택**. 현재 근거가 보도 기사(The Decoder)라 1차 출처로 교체 |
| json-render (Vercel Labs) | 카탈로그(컴포넌트 props를 zod로 정의) 안에서만 AI가 UI를 생성. 점진 렌더 | https://json-render.dev/ · https://github.com/vercel-labs/json-render | Apache-2.0 | 2.6 D3, `capability-map` `catalog.props_schema` | **참고**. 카탈로그 = 승인 목록이라는 같은 설계 |

### 1.7 공급망

| 항목 | 무엇인가 | 1차 출처 | 라이선스 | 대응 | 판정 |
| --- | --- | --- | --- | --- | --- |
| in-toto Attestation | 대상 다이제스트 + 술어 타입으로 된 서명 진술(Statement) 틀 | https://github.com/in-toto/attestation | Apache-2.0 | 7.7 "게시자 출처 서명" | **채택**(형식 지정) |
| SLSA Provenance v1 | `predicateType: https://slsa.dev/provenance/v1`. `buildDefinition`(`buildType`·`externalParameters`·`resolvedDependencies`), `runDetails.builder.id` | https://slsa.dev/spec/v1.1/provenance | Community Specification License 1.0 | 7.7, `change-record` `provenance` | **채택**. 하네스를 builder로 보면 공유 기능의 출처 증명이 됨 |

## 2. 갭 표 — 명세에 없고 선행 사례가 푼 것

| # | 빠진 개념 | 지금 명세 | 선행 사례의 해법 | 반영 |
| --- | --- | --- | --- | --- |
| P1 | 선언형 레이어 합성의 정확한 의미 | 2.3 "같은 키는 뒤 레이어가 덮어씀"만 있음. 배열·삭제 의미 미정 | RFC 7396: `null` 삭제, 배열 통째 교체 | E-3 |
| P2 | 스키마가 선언하는 병합 규칙 | 6.6 R2 "스키마가 규칙을 선언"이라고만 쓰고 필드가 없음 | SSA `list-type: map` + `list-map-keys`, `map-type: atomic/granular` | E-4 |
| P3 | 무결성 라벨 | 7.5는 기밀성 V0~V3만 | FIDES·CaMeL: 신뢰 불가 값이 행동 선택에 영향을 못 주게 무결성 추적 | E-1 |
| P4 | 정책 단조 축소의 기계 검증 | I5 집행 지점 "정책 저장소 검사"(방법 없음) | Cedar SymCC `check_implies`, `check_never_errors` | E-2 |
| P5 | 결정 근거의 표준 기록 | 4.8 "이유=(k, 상한을 정한 층)" | Cedar determining policies, OPA 결정 로그 `decision_id`·`bundles.revision`·`erased`·`masked` | E-2, E-5 |
| P6 | 텔레메트리 공통 어휘 | 5.11 `tokens_in`·`tokens_out` 등 자체 이름 | OTel `gen_ai.usage.input_tokens` 등, MCP `_meta.traceparent` | E-5 |
| P7 | 경험면 전송 규격 | 5.6은 하네스 쪽 이벤트만. 경험면이 무엇으로 진행·승인 대기를 받는지 없음 | AG-UI 이벤트·interrupt, A2A `INPUT_REQUIRED`, MCP MRTR | E-6 |
| P8 | 비밀값 입력 경로 | 8.10 "열쇠는 보안 저장소에"만. 에이전트 대화 경로로 받는 경우 미정 | MCP URL 모드 elicitation(MUST) | E-7 |
| P9 | D3 카탈로그 식별·버전 | `capability-map.catalog`는 목록만 있고 id·버전 없음 | A2UI `catalogId` | E-8 |
| P10 | 기능 권한 ↔ 에이전트 도구 힌트 | `capability.risk`만 | MCP `readOnlyHint`·`destructiveHint`·`idempotentHint`·`openWorldHint` | E-9 |
| P11 | 공유물 출처 증명 형식 | 7.7 "게시자 출처 서명"(형식 없음), 매니페스트 `content_hash` | in-toto Statement + SLSA provenance | E-10 |
| P12 | 네트워크 허용 사유 | `network.allow` 목록만 | Figma `networkAccess.reasoning` | 4절(보류) |

## 3. 제안 편집 목록 (우선순위순, 최대 12)

각 항목은 최소 편집입니다. 스키마 항목은 모두 **선택 필드 추가**라 `required`가 바뀌지 않고, 기존 `examples/*.yaml`은 그대로 통과해야 정상입니다. 반영 후 예시 검증을 다시 돌려야 합니다.

### E-1. 7.5에 무결성 축 추가 (P3)

- 파일: `docs/07-trust-and-security.md`, 7.5의 `라벨 λ = (범위, 등급)` 코드 블록과 그 아래 예 문단
- 제안 문구(코드 블록 교체):

```text
라벨 λ = (범위, 등급, 무결성)
  범위   : 테넌트 / 조직 / 사용자 식별자
  등급   : V0 집계 < V1 메타데이터 < V2 설명 < V3 코드          # 기밀성
  무결성 : trusted(사람 의도·검증된 기준판) > untrusted(공유물·외부 문서·모델이 신뢰 불가 입력을 보고 만든 값)

파생 규칙:  λ(f(x, y)) = λ(x) ⊔ λ(y)          # 기밀성은 더 민감한 쪽, 무결성은 더 낮은 쪽
열람 규칙:  보는 사람 s가 x를 볼 수 있다  ⇔  λ(x) ⊑ 권한(s)
행동 규칙:  권한 증가·외부 전송·확장 지점 선택을 결정하는 값은 무결성이 trusted여야 한다
해제 규칙:  라벨을 낮추는 것은 출력 게이트(해제기 declassifier)만 할 수 있고, 규칙과 기록을 남긴다
```

- 덧붙일 문장: `무결성 축은 FIDES(Costa et al., 2025)가 계획자 수준에서 기밀성·무결성 라벨을 함께 추적해 정책을 결정적으로 강제한 방식을 따릅니다. 7.4의 "계획 후 실행"을 라벨 규칙으로 쓴 것입니다.`
- references.md (「## 에이전트 보안」 끝):

```markdown
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · 노트북(MIT): https://github.com/microsoft/fides
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
```

### E-2. 4.8에 PDP 어댑터와 I5 기계 검증 추가 (P4, P5)

- 파일: `docs/04-control-spectrum.md`, 4.8 「배치 원칙」 목록 끝
- 제안 문구:

```markdown
- **정책 엔진 어댑터** (할 수 있음): 손잡이 구간을 정책 언어로 옮겨 PDP를 구현할 수 있습니다. Cedar는 forbid가 permit을 이기고 맞는 permit이 없으면 거부하며, 결정을 만든 정책 id를 함께 돌려줍니다. 이 id를 `거부(이유·층)`와 영수증(8.6)의 근거로 씁니다.
- **I5 기계 검증** (해야 함): 정책을 저장할 때 `p_child ⊑ p_parent`를 검사합니다. Cedar로 옮긴 경우 SymCC의 포함 검사(`check_implies`)로 반례와 함께 증명할 수 있습니다. 같은 도구의 `check_never_errors`도 함께 돌립니다. Cedar는 평가 오류가 난 정책을 건너뛰므로, 오류 나는 forbid는 조용히 열린 채로 남기 때문입니다.
- **하한은 엔진보다 먼저**: forbid 우선 규칙 때문에 권리 하한(F1~F7)을 일반 permit으로 넣으면 상위 forbid가 지울 수 있습니다. 위 의사 코드처럼 `FLOOR_ACTIONS` 판정을 엔진 호출 앞에 둡니다.
```

- references.md (새 절 「## 정책 엔진」, 「## 병합」 앞):

```markdown
## 정책 엔진

- Cedar 권한 부여 의미론(forbid 우선, 기본 거부, 결정 정책 진단). https://docs.cedarpolicy.com/auth/authorization.html · 코드(Apache-2.0): https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler(SymCC): 정책 포함·동치·오류 없음 검증. https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Open Policy Agent 결정 로그. https://www.openpolicyagent.org/docs/management-decision-logs
```

### E-3. 2.3 `⊕`의 기본 의미를 RFC 7396으로 고정 (P1)

- 파일: `docs/02-core-model.md`, 2.3의 `⊕` 항목
- 현재: `` `⊕` (레이어 합성): 같은 키를 건드리면 뒤의 레이어가 앞을 **덮어씁니다(override)**. 선언형 데이터는 키 단위로, 코드 확장은 확장 지점의 슬롯 단위로 합성합니다. ``
- 제안: `` `⊕` (레이어 합성): 같은 키를 건드리면 뒤의 레이어가 앞을 **덮어씁니다(override)**. 선언형 데이터의 기본 의미는 JSON Merge Patch(RFC 7396)입니다. 객체는 키 단위로 덮어쓰고, `null`은 그 키를 지우고, 배열은 통째로 바뀝니다. 배열을 항목 단위로 합치려면 확장 지점 스키마가 병합 키를 선언해야 합니다(6.6 R2). 코드 확장은 확장 지점의 슬롯 단위로 합성합니다. ``
- 비고: 다음 줄의 결합법칙 요구("기준판을 미리 합쳐 캐시")를 지키려면, 레이어끼리 미리 합칠 때 `null`(삭제 표지)을 지우지 말고 남겨야 합니다. 그래야 합친 레이어를 나중에 적용해도 하나씩 적용한 결과와 같습니다. 반영 전 작은 예로 확인할 것.
- references.md (「## 병합」):

```markdown
- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
```

### E-4. `capability-map` 확장 지점에 병합 규칙 필드 추가 (P2)

- 파일: `schemas/capability-map.schema.json`, `$defs.extensionPoint.properties`에서 `output_schema` 다음
- 제안 필드:

```json
"merge": {
  "type": "object",
  "description": "이 지점의 선언형 산출물을 레이어끼리 합치는 규칙 (명세 2.3, 6.6 R2). 키는 산출물 안의 JSON Pointer. 선언이 없는 배열은 atomic",
  "propertyNames": { "pattern": "^(/[^/]*)*$" },
  "additionalProperties": {
    "type": "object",
    "required": ["strategy"],
    "additionalProperties": false,
    "properties": {
      "strategy": { "type": "string", "enum": ["atomic", "set", "map"] },
      "keys": { "type": "array", "items": { "type": "string" }, "minItems": 1, "description": "strategy=map일 때 항목을 식별하는 필드 이름" }
    }
  }
}
```

- 6.6 R2 표 행 "예" 칸 뒤에 덧붙일 문구: `(스키마 필드: capability-map의 extension_points[].merge. 값 이름은 Kubernetes Server-Side Apply의 x-kubernetes-list-type을 따름)`
- references.md (「## 병합」):

```markdown
- Kubernetes. *Server-Side Apply* (필드 소유권, `x-kubernetes-list-type`·`x-kubernetes-list-map-keys` 병합 표지). https://kubernetes.io/docs/reference/using-api/server-side-apply/
```

### E-5. 5.11 텔레메트리 이름을 OTel GenAI·OPA에 맞춤 (P5, P6)

- 파일: `docs/05-reference-architecture.md`, 5.11 JSON 예와 그 아래 문단
- 제안: JSON의 `"model_cost"`를 아래로 바꾸고, `"policy"` 키를 추가합니다.

```json
  "gen_ai": {"operation.name": "invoke_agent", "agent.id": "builder@harness-x", "usage.input_tokens": 18200, "usage.output_tokens": 2100},
  "model_cost": {"unit_cost_ref": "route:standard"},
  "policy": {"decision_id": "dec_7Q2…", "revision": "tenant/acme@42"},
  "trace": {"traceparent": "00-…-…-01"},
```

- 덧붙일 문장: `모델 사용량 속성은 OpenTelemetry GenAI 의미 규약의 이름을 따릅니다. 이 규약은 아직 Development 상태이므로 구현은 따른 규약 버전을 함께 기록합니다. 정책 결정은 OPA 결정 로그처럼 결정 id와 정책 판(revision)을 남기고, 가명화로 지운 필드는 JSON Pointer 목록으로 표시합니다(7.9). MCP 서버를 거치는 호출은 MCP `_meta`의 traceparent 규약으로 같은 추적에 묶습니다.`
- references.md (새 절 「## 관측」, 「## 경험 설계」 앞):

```markdown
## 관측

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/
```

### E-6. 5.6에 경험면 전송 대응표 추가 (P7)

- 파일: `docs/05-reference-architecture.md`, 「### 매핑 예: Claude Code 훅」 표 다음, 「주의:」 문단 앞
- 제안 문구:

```markdown
경험면은 하네스 이벤트를 그대로 받지 않고 사용자용 진행 신호로 받습니다. AG-UI를 전송 규격으로 쓰면 다음처럼 대응합니다.

| Mallangable | AG-UI | 비고 |
| --- | --- | --- |
| E2 접수 ~ E11 종료 | `RUN_STARTED` · `RUN_FINISHED` · `RUN_ERROR` | |
| 상태어 4개(8.5) | `STEP_STARTED` · `STEP_FINISHED` | step 이름을 상태어 id로 고정 |
| 부분 미리보기(8.5) | `STATE_SNAPSHOT` · `STATE_DELTA`(RFC 6902) | "아직 확인 전" 표시 유지 |
| E6 `permission.request`, 2.8 `승인대기` | `RUN_FINISHED`의 `outcome.type = "interrupt"` → 다음 실행의 `resume[]` | 승인은 새 실행으로 이어짐 |

서버 잡을 외부 에이전트에 맡길 때는 A2A 작업 상태(`TASK_STATE_INPUT_REQUIRED`·`TASK_STATE_AUTH_REQUIRED`)가, MCP 도구 안에서는 다중 왕복 요청(`resultType: "input_required"`)이 같은 자리를 맡습니다. Claude Code 대응표에는 `PostToolUseFailure`(E5), `Elicitation`(E6)도 더할 수 있습니다.
```

- references.md (「## 생성형 UI·확장 표준」):

```markdown
- AG-UI: Agent-User Interaction Protocol (이벤트, interrupt). MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
```

### E-7. 8.10에 MCP 경로의 비밀값 입력 규칙 추가 (P8)

- 파일: `docs/08-experience-design.md`, 8.10 「### 보안과 비용 표시」 첫 항목 다음
- 제안 문구:

```markdown
- `sub` 경로처럼 공식 도우미 안에서 MCP 도구로 동작할 때, 연결 열쇠나 외부 서비스 토큰을 대화나 form 모드 입력으로 받지 않습니다. MCP 명세는 비밀값·자격 증명에 URL 모드 elicitation을 쓰도록 요구합니다(2026-07-28판). 열쇠가 에이전트 맥락에 한 번도 들어가지 않아야 I6이 지켜집니다.
- 같은 판에서 MCP Sampling은 폐기 예정입니다. 모델 호출을 MCP 클라이언트에 떠넘기는 방식으로 `ModelPort` 어댑터를 만들지 않습니다.
```

- references.md (「## 생성형 UI·확장 표준」):

```markdown
- Model Context Protocol 명세 2026-07-28 (변경 사항, 도구 annotations, elicitation). https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
```

### E-8. `capability-map`에 카탈로그 id·버전 추가 (P9)

- 파일: `schemas/capability-map.schema.json`, 최상위 `properties`에서 `catalog` 앞
- 제안 필드:

```json
"catalog_id": {
  "type": "string",
  "description": "D3 카탈로그 식별자. URI 형식 문자열이며 내려받을 수 있을 필요는 없다. 카탈로그 내용이 바뀌면 값도 바뀐다 (A2UI catalogId와 같은 의미)",
  "examples": ["https://todo.example/catalogs/v3"]
}
```

- 덧붙일 곳: `schemas/extension-manifest.schema.json` `artifact.properties`에 `"catalog_id": { "type": "string", "description": "D3 산출물이 전제한 카탈로그. 기능 지도의 catalog_id와 다르면 G1에서 거부" }`
- references.md: 「## 생성형 UI·확장 표준」의 `Google A2UI 보도. The Decoder.` 줄을 아래로 교체.

```markdown
- A2UI: Agent-to-User Interface 명세 v0.9.1 (`createSurface`·`catalogId`). Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
```

### E-9. `capability-map` 기능 권한과 MCP 도구 힌트 대응 (P10)

- 파일: `schemas/capability-map.schema.json`, `$defs.capability.properties.risk`의 `description`
- 현재: `"egress=외부 전송, sensitive=타인·민감 데이터"`
- 제안: `"egress=외부 전송, sensitive=타인·민감 데이터. 기능을 MCP 도구로 노출할 때 read는 readOnlyHint=true, egress는 openWorldHint=true로 내보낸다. 받은 쪽의 MCP annotations는 신뢰하지 않으며 이 값이 권위 있다 (I8)"`
- 선택 필드 하나 추가: `"destructive": { "type": "boolean", "description": "되돌릴 수 없는 쓰기. MCP destructiveHint와 같은 의미. true면 활성화 정책과 무관하게 G5" }`
- 5.8 G5 행 "내용" 칸에 `· 되돌릴 수 없는 쓰기(destructive) 기능 사용 시` 추가.
- references.md: E-7의 MCP 명세 항목에 `https://modelcontextprotocol.io/specification/2026-07-28/server/tools` 를 함께 적습니다.

### E-10. 7.7 공급망에 출처 증명 형식 지정 (P11)

- 파일: `docs/07-trust-and-security.md`, 7.7 통제 표의 `한 계정이 대량 업로드했다` 행 "통제" 칸
- 현재: `게시자 출처 서명, 신규 게시자 제한, 큐레이션 등급`
- 제안: `게시자 출처 서명(in-toto Statement에 SLSA provenance 술어. 대상은 매니페스트 content_hash, builder.id는 하네스 id), 신규 게시자 제한, 큐레이션 등급`
- references.md (「## 에이전트 보안」 끝 또는 새 절 「## 공급망」):

```markdown
- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance
```

### E-11. 1.5 관련 연구에 말랑한 매체 선례 보강

- 파일: `docs/01-introduction.md`, 1.5 표의 첫 행(Malleable software) 다음
- 제안 행:

```markdown
| 계산 매체·동적 문서 (Boxer, 1986 · [Webstrates](https://webstrates.net/), 2015 · [Potluck](https://www.inkandswitch.com/potluck/), 2022 · [Embark](https://www.inkandswitch.com/embark/), 2023) | 문서와 앱의 경계를 없애고 사용자가 계산을 겹쳐 얹음 | 원본을 건드리지 않는 겹침 레이어(2.3), 앱을 넘는 도구(O8) | 기존 상용 앱 위에서, 제공사 업데이트를 견디는 구조로 정의 |
```

- 같은 표 Local-first 행의 링크를 `https://www.inkandswitch.com/project/patchwork/`로 바꾸고, "가져온 것" 칸에 `· AI 편집을 브랜치에 두고 사람이 골라 병합(Patchwork 실험 노트)`을 덧붙입니다.
- references.md (「## 말랑한 소프트웨어와 최종 사용자 프로그래밍」):

```markdown
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · 코드(Apache-2.0): https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck: Dynamic documents as personal software.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark: Dynamic documents for making plans.* 2023. https://www.inkandswitch.com/embark/
- Ink & Switch. *Patchwork* (실험 노트 07 "AI bots in version control"). https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
```

- 비고: Potluck·Embark 부제는 페이지 제목을 그대로 옮기기 전에 원문과 한 번 더 대조해야 합니다(요약 도구로 읽었음).

### E-12. references.md의 2차 출처를 1차 출처로 교체

- 파일: `docs/references.md`
- 바꿀 줄:

| 현재 | 교체 |
| --- | --- |
| `Agent Skills 표준 정리. Shiplight, 2026. https://www.shiplight.ai/blog/agent-skills` | `Agent Skills 명세 (SKILL.md 앞부분, allowed-tools는 Experimental). Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills` |
| `Claude Code 플러그인 개요. https://code.claude.com/docs/es/plugins/overview` | `Claude Code 플러그인 매니페스트 레퍼런스. https://code.claude.com/docs/en/plugins-reference` |
| `Mergiraf: 구문 인식 Git 병합 드라이버. https://docs.rs/crate/mergiraf/latest` | `Mergiraf: 구문 인식 Git 병합 드라이버. GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf` |
| `SEP-1865. *MCP Apps …* https://modelcontextprotocol.io/seps/1865-…` | 그대로 두고 뒤에 ` · 명세(2026-01-26): https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx` |
| CaMeL 항목 | 뒤에 ` · 코드(Apache-2.0): https://github.com/google-research/camel-prompt-injection` |

- 본문 링크도 같이 바꿉니다: 5.6의 `[Shiplight, 2026]` → `[Agent Skills 명세](https://agentskills.io/specification)`, 1.5의 A2UI·Agent Skills 링크, 3.2 A6의 Automerge 링크 → `https://automerge.org/docs/reference/documents/conflicts/`, 6.6 R1의 Mergiraf 링크 → `https://mergiraf.org/`.
- `확인일`을 반영일로 갱신합니다.

## 4. 넣지 않은 것

- **Figma `networkAccess.reasoning`식 허용 사유 필드(P12)**: 쓸모는 있지만 지금 `network.allow`를 쓰는 주체는 사람이 아니라 생성 에이전트입니다. 에이전트가 쓴 사유는 승인 카드의 근거가 못 됩니다. 승인 카드(G5)를 설계할 때 다시 봅니다.
- **WIT·Extism 필드 이름 맞추기**: 같은 개념이 매니페스트에 이미 있고, 산출물 형식 하나(`wasm`)를 위한 정렬입니다. D4 `lang` 어댑터 문서를 쓸 때 대응표로 충분합니다.
- **VS Code 활성화 이벤트**: 지연 로딩은 런타임 구현 문제이고 계약·병합과 무관합니다. G3 시작 시간 예산이 같은 목적을 맡습니다.
- **Chrome식 `optional_permissions`**: "필요할 때 요청"은 I4 사람 승인 흐름(E6)으로 이미 표현됩니다. 정적 선언을 하나 더 두면 두 경로가 갈라집니다.
- **OPA를 기본 PDP로**: 결정 로그 형식은 가져오되, I5 포함 검증이 되는 Cedar가 이 명세의 단조성 요구에 더 맞습니다.
- **MCP-UI, Yjs 별도 정렬**: 각각 MCP Apps, Automerge 인용으로 충분합니다.
- **Smalltalk 계보**: 1차 출처를 찾지 않았습니다. 인용하려면 원 논문을 확인해야 합니다.
