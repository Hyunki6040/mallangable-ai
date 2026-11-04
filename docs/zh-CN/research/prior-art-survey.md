<!-- LANG-BAR -->
[English](../../en/research/prior-art-survey.md) · [한국어](../../ko/research/prior-art-survey.md) · **简体中文** · [日本語](../../ja/research/prior-art-survey.md) · [Español](../../es/research/prior-art-survey.md)
<!-- /LANG-BAR -->

# 调研笔记 — 先行案例调研（开源、规范、智能体标准）

> 本笔记的结论：与本规范新定义的内容（契约保持合并（contract-preserving merge）、谱系（lineage）传播、区间委托、权利底线）**重合的标准并不存在。** 不过周边部件已经标准化，而目前的规范要么没有使用它们的名称，要么以二手出处引用。可以引入的有五个方向。① 将声明式层（layer）合成 `⊕` 的基本语义固定为 **JSON Merge Patch（RFC 7396）**，列表合并规则则像 Kubernetes Server-Side Apply 那样**由模式声明**。② 在信息流标签（7.5）中加入**完整性轴**（FIDES、CaMeL）。③ 用 **Cedar 的策略包含验证**对策略（policy）单调收缩（I5）进行机器确认。④ 让遥测（5.11）对齐 **OpenTelemetry GenAI 属性名称**。⑤ 把 MCP 最新版（2026-07-28）的 **URL 模式 elicitation** 和 Sampling 弃用反映到模型连接（8.10）中。

- 确认日期：2026-10-30
- 方法：仓库通过 `gh api` 读取元数据、许可证文件和规范原文，网页文档只取自官方网站。未执行代码。所引用的 URL 都用 `curl -L` 确认返回 200（ACM 数字图书馆以 403 拦截自动请求，因此只记录了 DOI）。
- 范围：本章不修改现有文档。是否采纳第 3 节的编辑方案另行决定。

## 0. 已确认与未完成的事项

| 项目 | 状态 | 备注 |
| --- | --- | --- |
| MCP 最新修订版 | 已确认 | `2026-07-28`（2026-07-28 发布）。仓库 `docs/specification/2026-07-28/changelog.mdx` 原文 |
| MCP Apps | 已确认 | `modelcontextprotocol/ext-apps` 的 `specification/2026-01-26/apps.mdx`。扩展 id `io.modelcontextprotocol/ui` |
| OpenTelemetry GenAI 约定 | 已确认 | 已从 `open-telemetry/semantic-conventions` **迁移到 `semantic-conventions-genai` 仓库**。文档状态全部为 Development |
| A2UI | 已确认 | 仓库已迁移至 `a2ui-project/a2ui`。当前为 v0.9.1，v1.0 处于 RC |
| Cedar 决策规则与验证器 | 已确认 | 官方文档和 `cedar-policy-symcc` README |
| Patchwork 内部结构 | 部分 | 只读了项目页面和实验笔记 07。`inkandswitch/patchwork-system` 仓库没有许可证标注 |
| Boxer 原文 | 未能阅读 | ACM 拦截自动请求。只确认了书目信息 |
| Chrome、Figma、VS Code 文档的许可证 | 未确认 | 属于产品文档，因此只引用，不搬运文字 |

## 1. 分项调研

判定：**采纳** = 引用并对齐字段名称与语义 / **参考** = 仅作为相关研究引用 / **无关** = 不纳入。
"对应"栏是本规范的章节编号和模式文件。

### 1.1 可塑软件研究

| 项目 | 是什么 | 一手出处 | 许可证 | 对应 | 判定 |
| --- | --- | --- | --- | --- | --- |
| Malleable software 随笔（Ink & Switch，2025） | 主张从被锁定的应用中夺回用户主体性的随笔。整理了平缓坡度、本地开发者等概念 | https://www.inkandswitch.com/essay/malleable-software/ | 随笔（无标注） | 1.5，2.6 | 已被引用。保留 |
| Potluck（2022） | 在文本之上叠加搜索、公式、动态注释，逐步增加结构。注释是不改动原文的叠加层 | https://www.inkandswitch.com/potluck/ | 随笔 | 2.3 层，2.6 D1~D3 | **参考**。"不触碰原件的叠加层"的先例 |
| Embark（2023） | 在一份旅行计划文档中同时放置数据、计算和视图，从而拆解应用 | https://www.inkandswitch.com/embark/ | 随笔 | 10.1 O8（跨越应用的工具） | **参考** |
| Patchwork（2024~） | 面向文字、图画等非代码文档的通用版本管理。实验笔记中，**AI 机器人在分支上编辑，人查看 diff 后只合并一部分，历史中会标出机器人的编辑** | https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/ | 仓库无标注 | 6.4 `exp/*` 分支，6.11 `Agent:` 尾注，8.6 回执 | **参考**。目前 references.md 中"Universal Version Control"链接指向实验室列表页，改为 Patchwork 页面更准确 |
| Cambria（2020） | 用双向透镜在模式版本之间转换数据 | https://www.inkandswitch.com/cambria/ · https://github.com/inkandswitch/cambria-project | MIT | 5.9 `migrate(prev)`，`extension-manifest` `state.migrate_from` | **参考**。目前把状态交接设计为单向 `migrate` 已经足够。若需要双向，可作为依据 |
| Webstrates（UIST 2015） | 同步 DOM 变更，模糊文档与应用的边界。可塑、共享、分布、计算四项原则 | https://webstrates.net/ · https://github.com/Webstrates/Webstrates | Apache-2.0 | 6.13 CRDT 之上的代码风险 | **参考**。是实时共享可执行代码的先例，适合作为 S7 的依据案例 |
| Boxer（diSessa & Abelson, CACM 29(9), 1986） | 非专业人员可以重新组装的计算媒介 | DOI 10.1145/6592.6595 | 论文 | 1.5 | **参考**。Smalltalk 谱系未查找一手出处，故排除 |

### 1.2 扩展与插件清单

| 项目 | 是什么 | 一手出处 | 许可证 | 对应 | 判定 |
| --- | --- | --- | --- | --- | --- |
| VS Code 贡献点与激活事件 | 用 `contributes`（commands、menus、views、keybindings、configuration、`languageModelTools` 等）声明扩展点。从 1.74 起，贡献点会自动隐含激活事件 | https://code.visualstudio.com/api/references/contribution-points · https://code.visualstudio.com/api/references/activation-events | 代码 MIT，文档未确认 | 2.2 扩展点 `kind`，`capability-map` | **参考**。与 `kind`（token、command、view、hook、service）对应得很自然 |
| VS Code Workspace Trust | `capabilities.untrustedWorkspaces.supported: true / false / "limited"`。不受信任的工作区以 Restricted Mode 打开，自动执行被阻止 | https://code.visualstudio.com/api/extension-guides/workspace-trust | 文档 | 4.6 F2 安全模式，6.9 收到的共享 | **参考** |
| Chrome MV3 权限 | `permissions`、`optional_permissions`、`host_permissions`、`optional_host_permissions`。**若在更新中新增会附带警告的权限，扩展会被停用，直到用户接受** | https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions | 文档 | I4，6.5 `delta_permissions`，6.9 subscribe | **参考**。I4 的真实大规模先例。与目前规范的规则（权限增加 → 提议）方向相同 |
| Figma 插件清单 | `networkAccess.allowedDomains`（可为 `["none"]`）、`reasoning`（使用通配符时必填）、`devAllowedDomains`，`permissions` | https://developers.figma.com/docs/plugins/manifest/ | 文档 | `extension-manifest` `network.allow` | **参考**。"允许理由"字段是第 4 节的候选 |
| Obsidian 社区插件 | 官方文档明确写明"不能把插件限制在特定权限内"，插件可访问文件、网络和安装程序。默认是 Restricted mode | https://obsidian.md/help/plugin-security | 应用为专有，`obsidian-api` MIT | 7.6，7.7 | **参考**。作为无隔离扩展的反例有引用价值 |
| WASM Component Model / WIT | `world` 声明组件的 import 和 export，宿主（host）只提供被 import 的内容。包带有版本（`wasi:http@0.2.0`） | https://component-model.bytecodealliance.org/design/wit.html · https://github.com/WebAssembly/component-model | Apache-2.0 | 7.6 对象能力，`SandboxHost` `lang` 适配器，清单 `permissions` | **参考**。若产出物为 `wasm`，清单 `permissions` ↔ world import 可以 1:1 对应 |
| Extism | WASM 插件框架。清单中有 `wasm[].hash`、`memory.max_pages`、`allowed_hosts`、`allowed_paths`、`config` | https://extism.org/docs/concepts/manifest · https://github.com/extism/extism | BSD-3-Clause | `extension-manifest` `artifact.content_hash`、`network.allow`、`resources.memory_mb` | **参考**。同样的概念已经存在。对齐名称的理由不强 |
| Tauri v2 capability | 已被引用 | （references.md） | | 7.6 | 保留 |
| Endo / SES | 已被引用 | （references.md） | Apache-2.0 | 7.6 | 保留 |

### 1.3 智能体协议与执行框架事件

| 项目 | 是什么 | 一手出处 | 许可证 | 对应 | 判定 |
| --- | --- | --- | --- | --- | --- |
| MCP 2026-07-28 | 无状态化（移除 `initialize`，每个请求在 `_meta` 中携带版本和客户端能力），`server/discover`，多轮往返请求（MRTR：`resultType: "input_required"`），tasks 移至官方扩展，**Roots、Sampling、Logging 计划弃用**，`_meta` 的 `traceparent` 约定（SEP-414） | https://modelcontextprotocol.io/specification/2026-07-28/changelog | Apache-2.0（规范，正从 MIT 转换中），文档 CC-BY-4.0 | 5.3 `ModelPort`，5.6，8.10 | **采纳**。不应在 MCP Sampling 之上设计 8.10 的 `sub` 路径 |
| MCP 工具 annotations | `readOnlyHint`、`destructiveHint`、`idempotentHint`、`openWorldHint`。**如果不是受信任的服务器，客户端不得信任 annotations（MUST）** | https://modelcontextprotocol.io/specification/2026-07-28/server/tools | 同上 | `capability-map` `capability.risk` | **采纳**。为 `risk` 值设对应表（第 3 节 E-10） |
| MCP elicitation | form 模式和 URL 模式。**机密值和凭据不得用 form 模式接收，必须使用 URL 模式（MUST）** | https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation | 同上 | 8.10 连接密钥，I6 | **采纳** |
| MCP 授权 | OAuth 2.1，Protected Resource Metadata（RFC 9728），资源指示符（RFC 8707），`iss` 验证（RFC 9207） | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | 同上 | 2.1 委托，7.2 | **参考**。为 I4、I9 中"智能体 α 是获得人类委托的短期主体"这一说明提供实现依据 |
| MCP Apps (SEP-1865) | `ui://` 资源，`text/html;profile=mcp-app`，强制使用沙箱 iframe，`_meta.ui.csp`（`connectDomains`、`resourceDomains`、`frameDomains`、`baseUriDomains`），`permissions`（camera、microphone、geolocation、clipboardWrite） | https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx | 同上 | 3.2 A4 `frame`，`extension-manifest` `network` | 已被引用。**保持采纳**。把链接固定到带日期的规范路径 |
| MCP-UI | MCP Apps 的原型。现在是兼容 MCP Apps 的 SDK | https://github.com/MCP-UI-Org/mcp-ui | Apache-2.0 | | **无关**（MCP Apps 已足够） |
| AG-UI | 智能体↔前端事件协议。`RUN_STARTED`/`RUN_FINISHED`/`RUN_ERROR`，`STEP_*`，`TOOL_CALL_*`，`STATE_SNAPSHOT`/`STATE_DELTA`（**RFC 6902 JSON Patch**），`SUBAGENT_*`。人工批准在 `RunFinished` 的 `outcome: { type: "interrupt" }` 之后以 `resume[]` 开启新的运行 | https://docs.ag-ui.com/concepts/events · https://docs.ag-ui.com/concepts/interrupts · https://github.com/ag-ui-protocol/ag-ui | MIT | 5.6 事件模型，8.5 进度表达，2.8 `等待批准` | **采纳**（对应表）。可直接用作体验平面↔生成平面之间的传输规范 |
| A2A v1.0 | 不透明智能体之间的作业协议。`AgentCard`，作业状态 `TASK_STATE_SUBMITTED / WORKING / INPUT_REQUIRED / AUTH_REQUIRED / COMPLETED / FAILED / CANCELED / REJECTED` | https://a2a-protocol.org/latest/specification/ · https://github.com/a2aproject/A2A | Apache-2.0 | 5.3 `JobOrchestrator`，2.8 生命周期 | **参考**。把服务器合并、晋升作业交给外部智能体时的适配器候选 |
| OpenTelemetry GenAI 约定 | `gen_ai.operation.name`（`invoke_agent`、`execute_tool`、`create_agent`、`invoke_workflow`），`gen_ai.agent.id`，`gen_ai.usage.input_tokens`、`output_tokens`，`gen_ai.tool.name`，MCP 属性 `mcp.method.name`。**状态为 Development** | https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/ | Apache-2.0 | 5.11 遥测 | **采纳**（仅属性名称）。并非稳定版，需要固定版本 |
| OpenAI Agents SDK 追踪 | trace（`workflow_name`、`trace_id`、`group_id`），span（`agent`、`generation`、`function`、`guardrail`、`handoff`、`custom`），`trace_include_sensitive_data` | https://openai.github.io/openai-agents-python/tracing/ · https://github.com/openai/openai-agents-python | MIT | 5.11，7.5 解除规则 | **参考**。默认包含敏感数据（True）与本规范的默认值相反 |
| Claude Code 钩子 | 32 个事件，5 种处理器（`command`、`http`、`mcp_tool`、`prompt`、`agent`），`PreToolUse` 的 `permissionDecision`（`allow`、`deny`、`ask`、`defer`）和 `updatedInput`，托管设置 `allowManagedHooksOnly` | https://code.claude.com/docs/en/hooks.md | 产品文档 | 5.6 对应表 | 已被引用。对应表中可加入 `PostToolUseFailure`（E5）、`Elicitation`（E6） |
| Claude Code 插件 | `.claude-plugin/plugin.json`（只有 `name` 必填，`skills`、`hooks`、`mcpServers`、`userConfig` 的 `sensitive`），`claude plugin validate` | https://code.claude.com/docs/en/plugins-reference | 产品文档 | 5.6 执行框架分发，8.10 `sub` | 已被引用。**references.md 的链接是西班牙语版（`/docs/es/`），替换为英文版参考文档** |
| Agent Skills 规范 | `SKILL.md` 头部的 `name`（64 字符）、`description`（1024 字符）、`license`、`compatibility`、`metadata`、`allowed-tools`（**Experimental**） | https://agentskills.io/specification · https://github.com/agentskills/agentskills | Apache-2.0 | 5.6 "技能是流程，执行框架是强制" | **采纳**。目前依据是二手出处（Shiplight），替换为一手规范。所主张的内容与一手出处一致 |

### 1.4 策略引擎与提示词注入防御

| 项目 | 是什么 | 一手出处 | 许可证 | 对应 | 判定 |
| --- | --- | --- | --- | --- | --- |
| Cedar | 主体、动作、资源、上下文构成的请求。**forbid 优先于 permit，没有匹配的 permit 则 Deny**。响应中包含做出决策的策略 id（determining policies）和错误列表。出错的策略会被跳过 | https://docs.cedarpolicy.com/auth/authorization.html · https://github.com/cedar-policy/cedar | Apache-2.0 | 4.8 `decide(req)`，`PolicyDecisionPoint` | **采纳**（PDP 适配器） |
| Cedar SymCC | 把策略集合转换为 SMT，连同反例验证**包含（`check_implies`）、等价、始终拒绝、无错误**。验证器本身用 Lean 做了形式化验证 | https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc | Apache-2.0 | **I5 `p_child ⊑ p_parent`** | **采纳**。把 I5 从"策略存储检查"提升为可证明的检查 |
| OPA / Rego | CNCF 毕业项目。决策日志中有 `decision_id`、`bundles.revision`、`path`、`input`、`result`、`erased`、`masked`（JSON Pointer）、`trace_id`、`span_id` | https://www.openpolicyagent.org/docs/management-decision-logs · https://github.com/open-policy-agent/opa | Apache-2.0 | 5.11，7.9 假名化 | **采纳**（决策日志字段名称）。作为策略语言，可分析性弱于 Cedar，因此不是 PDP 首选 |
| CaMeL（DeepMind 2025） | 已被引用。代码已公开 | https://github.com/google-research/camel-prompt-injection | Apache-2.0 | 7.4 | 保留。加上代码链接 |
| FIDES（Microsoft 2025） | 规划者通过动态污点追踪跟随**机密性和完整性标签**，以确定性方式强制执行策略。提出了选择性隐藏信息的基本操作 | https://arxiv.org/abs/2505.23643 · https://github.com/microsoft/fides | 笔记本 MIT | **7.5 信息流标签** | **采纳**。7.5 只有机密性（V0~V3），没有完整性轴 |
| Dual LLM 模式（Willison 2023） | 特权 LLM 与隔离 LLM，以及二者之间的非 LLM 控制器。不可信的值只以 `$VAR1` 这样的引用传递 | https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | 博客 | 7.3 隔离读取者 | **采纳**（引用）。7.4 目前是经由设计模式论文间接引用 |
| 致命三要素（Willison 2025） | 已被引用 | | | 7.3 | 保留 |

### 1.5 合并与谱系

| 项目 | 是什么 | 一手出处 | 许可证 | 对应 | 判定 |
| --- | --- | --- | --- | --- | --- |
| JSON Merge Patch（RFC 7396） | 对象键覆盖，`null` 删除，**数组整体替换** | https://www.rfc-editor.org/rfc/rfc7396 | IETF Trust | **2.3 `⊕`**，6.6 R2 | **采纳**。`⊕` 的"按键覆盖"恰好就是这个语义，只是没有名称 |
| JSON Patch（RFC 6902） | 操作列表（add、remove、replace、move、copy、test） | https://www.rfc-editor.org/rfc/rfc6902 | IETF Trust | 8.5 部分预览，AG-UI `STATE_DELTA` | **参考** |
| Kubernetes Server-Side Apply | 字段管理者记录字段所有权（`managedFields`）。通过模式标记 `x-kubernetes-list-type: atomic / set / map`、`x-kubernetes-list-map-keys`、`x-kubernetes-map-type: atomic / granular`，**由模式声明**合并方式。修改其他管理者拥有的字段会产生冲突 | https://kubernetes.io/docs/reference/using-api/server-side-apply/ | 文档 | **6.6 R2**"由模式声明规则"，6.11 `Overrides:` | **采纳**。R2 只有说法而没有模式字段 |
| Kustomize | base、overlay、component。component 是可以混入多个 overlay 的可复用功能包。`patches` 支持 strategic merge 和 JSON 6902 | https://kubectl.docs.kubernetes.io/guides/config_management/components/ · https://github.com/kubernetes-sigs/kustomize | Apache-2.0 | 6.2 lineage，6.9 按功能单位共享 | **参考**。"基线版之上的叠加"的实务先例 |
| Automerge | CRDT。对同一键的并发写入按操作 id 确定性地选出胜者，但**落败的值通过 `getConflicts()` 保留** | https://automerge.org/docs/reference/documents/conflicts/ · https://github.com/automerge/automerge | MIT | 6.13 CRDT 语义冲突 | **参考**。目前 3.2 A6 的链接指向 Ink & Switch 列表页，改为 Automerge |
| Yjs | CRDT 共享类型 | https://yjs.dev/ · https://github.com/yjs/yjs | MIT | 3.2 A6 `crdt` | **参考** |
| Mergiraf | 基于 tree-sitter 的语法感知合并驱动 | https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf | **GPL-3.0-only**（`Cargo.toml`） | 6.6 R1 | 已被引用。把链接从 docs.rs 改为官方网站并注明许可证。它是 6.6 中"强 copyleft"警告的实际对象 |

### 1.6 生成式 UI

| 项目 | 是什么 | 一手出处 | 许可证 | 对应 | 判定 |
| --- | --- | --- | --- | --- | --- |
| A2UI v0.9.1 | 声明式 JSON UI。4 种消息 `createSurface`、`updateComponents`、`updateDataModel`、`deleteSurface`。每个表面固定一个 **`catalogId`**（URI 格式字符串）。只渲染已批准目录中的组件 | https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md | Apache-2.0 | 2.6 D3，`capability-map` `catalog`，8.5 | **采纳**。目前依据是新闻报道（The Decoder），替换为一手出处 |
| json-render（Vercel Labs） | AI 只在目录（用 zod 定义组件 props）范围内生成 UI。渐进渲染 | https://json-render.dev/ · https://github.com/vercel-labs/json-render | Apache-2.0 | 2.6 D3，`capability-map` `catalog.props_schema` | **参考**。同样是"目录 = 批准列表"的设计 |

### 1.7 供应链

| 项目 | 是什么 | 一手出处 | 许可证 | 对应 | 判定 |
| --- | --- | --- | --- | --- | --- |
| in-toto Attestation | 由目标摘要 + 谓词类型构成的签名声明（Statement）框架 | https://github.com/in-toto/attestation | Apache-2.0 | 7.7"发布者来源签名" | **采纳**（指定格式） |
| SLSA Provenance v1 | `predicateType: https://slsa.dev/provenance/v1`。`buildDefinition`（`buildType`、`externalParameters`、`resolvedDependencies`），`runDetails.builder.id` | https://slsa.dev/spec/v1.1/provenance | Community Specification License 1.0 | 7.7，`change-record` `provenance` | **采纳**。把执行框架视为 builder，就成为共享功能的来源证明 |

## 2. 缺口表 — 规范中没有、而先行案例已经解决的问题

| # | 缺失的概念 | 现有规范 | 先行案例的解法 | 反映 |
| --- | --- | --- | --- | --- |
| P1 | 声明式层合成的精确语义 | 2.3 只有"同一键由后面的层覆盖"。数组、删除的语义未定 | RFC 7396：`null` 删除，数组整体替换 | E-3 |
| P2 | 由模式声明的合并规则 | 6.6 R2 只写了"由模式声明规则"，没有字段 | SSA `list-type: map` + `list-map-keys`，`map-type: atomic/granular` | E-4 |
| P3 | 完整性标签 | 7.5 只有机密性 V0~V3 | FIDES、CaMeL：追踪完整性，使不可信的值无法影响行动选择 | E-1 |
| P4 | 策略单调收缩的机器验证 | I5 执行点"策略存储检查"（无方法） | Cedar SymCC `check_implies`、`check_never_errors` | E-2 |
| P5 | 决策依据的标准记录 | 4.8"原因=(k, 决定上限的层)" | Cedar determining policies，OPA 决策日志 `decision_id`、`bundles.revision`、`erased`、`masked` | E-2，E-5 |
| P6 | 遥测通用词汇 | 5.11 使用 `tokens_in`、`tokens_out` 等自定义名称 | OTel `gen_ai.usage.input_tokens` 等，MCP `_meta.traceparent` | E-5 |
| P7 | 体验平面传输规范 | 5.6 只有执行框架一侧的事件。没有说明体验平面通过什么接收进度和等待批准 | AG-UI 事件与 interrupt，A2A `INPUT_REQUIRED`，MCP MRTR | E-6 |
| P8 | 机密值输入路径 | 8.10 只有"密钥放在安全存储中"。通过智能体对话路径接收的情况未定 | MCP URL 模式 elicitation（MUST） | E-7 |
| P9 | D3 目录的标识与版本 | `capability-map.catalog` 只有列表，没有 id 和版本 | A2UI `catalogId` | E-8 |
| P10 | 能力（capability）↔ 智能体工具提示 | 只有 `capability.risk` | MCP `readOnlyHint`、`destructiveHint`、`idempotentHint`、`openWorldHint` | E-9 |
| P11 | 共享物来源证明格式 | 7.7"发布者来源签名"（无格式），清单 `content_hash` | in-toto Statement + SLSA provenance | E-10 |
| P12 | 网络允许理由 | 只有 `network.allow` 列表 | Figma `networkAccess.reasoning` | 第 4 节（暂缓） |

## 3. 建议编辑列表（按优先级，最多 12 项）

每项都是最小编辑。模式相关项全部是**添加可选字段**，因此 `required` 不变，既有的 `examples/*.yaml` 应照常通过。采纳后需要重新运行示例验证。

### E-1. 在 7.5 中加入完整性轴 (P3)

- 文件：`docs/07-trust-and-security.md`，7.5 的 `标签 λ = (范围, 等级)` 代码块及其下方的示例段落
- 建议文字（替换代码块）：

```text
标签 λ = (范围, 等级, 完整性)
  范围   : 租户 / 组织 / 用户标识符
  等级   : V0 汇总 < V1 元数据 < V2 说明 < V3 代码          # 机密性
  完整性 : trusted(人的意图·已验证的基线版) > untrusted(共享物·外部文档·模型看了不可信输入后生成的值)

派生规则:  λ(f(x, y)) = λ(x) ⊔ λ(y)          # 机密性取更敏感的一方,完整性取更低的一方
查看规则:  查看者 s 可以查看 x  ⇔  λ(x) ⊑ 权限(s)
行为规则:  决定权限增加·外部发送·扩展点选择的值,其完整性必须为 trusted
解除规则:  降低标签只能由输出门(解除器 declassifier)进行,并留下规则与记录
```

- 追加句子：`完整性轴沿用 FIDES（Costa et al., 2025）在规划者层面同时追踪机密性和完整性标签、以确定性方式强制执行策略的做法。这是把 7.4 的"先规划后执行"写成了标签规则。`
- references.md（「## 智能体安全」末尾）：

```markdown
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · 笔记本(MIT): https://github.com/microsoft/fides
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
```

### E-2. 在 4.8 中加入 PDP 适配器与 I5 机器验证 (P4, P5)

- 文件：`docs/04-control-spectrum.md`，4.8「布局原则」列表末尾
- 建议文字：

```markdown
- **策略引擎适配器**（可以(MAY)）：可以把旋钮区间转换为策略语言来实现 PDP。Cedar 中 forbid 优先于 permit，没有匹配的 permit 则拒绝，并一并返回做出决策的策略 id。把这个 id 用作 `deny(原因·层)` 和回执（8.6）的依据。
- **I5 机器验证**（应当(SHOULD)）：保存策略时检查 `p_child ⊑ p_parent`。转换为 Cedar 时，可以用 SymCC 的包含检查（`check_implies`）连同反例一起证明。同时也运行同一工具的 `check_never_errors`。因为 Cedar 会跳过发生求值错误的策略，出错的 forbid 会静默地保持放开。
- **底线先于引擎**：由于 forbid 优先规则，若把权利底线（F1~F7）作为普通 permit 放入，上层 forbid 就能把它抹掉。像上面的伪代码那样，把 `FLOOR_ACTIONS` 判定放在引擎调用之前。
```

- references.md（新节「## 策略引擎」，置于「## 合并」之前）：

```markdown
## 策略引擎

- Cedar 授权语义（forbid 优先、默认拒绝、决策策略诊断）。https://docs.cedarpolicy.com/auth/authorization.html · 代码(Apache-2.0): https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler(SymCC)：策略包含、等价、无错误验证。https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Open Policy Agent 决策日志。https://www.openpolicyagent.org/docs/management-decision-logs
```

### E-3. 把 2.3 `⊕` 的基本语义固定为 RFC 7396 (P1)

- 文件：`docs/02-core-model.md`，2.3 的 `⊕` 条目
- 现在：`` `⊕`（层合成）：触及同一键时，后面的层**覆盖（override）**前面的层。声明式数据按键合成，代码扩展按扩展点的槽位合成。 ``
- 建议：`` `⊕`（层合成）：触及同一键时，后面的层**覆盖（override）**前面的层。声明式数据的基本语义是 JSON Merge Patch（RFC 7396）。对象按键覆盖，`null` 删除该键，数组整体替换。若要按条目合并数组，扩展点模式必须声明合并键（6.6 R2）。代码扩展按扩展点的槽位合成。 ``
- 备注：要满足下一行的结合律要求（"预先合并基线版并缓存"），在层与层预先合并时，不能删除 `null`（删除标记），而要保留它。这样以后再应用合并后的层，结果才与逐个应用相同。采纳前用小例子确认。
- references.md（「## 合并」）：

```markdown
- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
```

### E-4. 在 `capability-map` 扩展点中加入合并规则字段 (P2)

- 文件：`schemas/capability-map.schema.json`，`$defs.extensionPoint.properties` 中 `output_schema` 之后
- 建议字段：

```json
"merge": {
  "type": "object",
  "description": "在层之间合并此扩展点声明式产出物的规则（规范 2.3、6.6 R2）。键是产出物内的 JSON Pointer。未声明的数组为 atomic",
  "propertyNames": { "pattern": "^(/[^/]*)*$" },
  "additionalProperties": {
    "type": "object",
    "required": ["strategy"],
    "additionalProperties": false,
    "properties": {
      "strategy": { "type": "string", "enum": ["atomic", "set", "map"] },
      "keys": { "type": "array", "items": { "type": "string" }, "minItems": 1, "description": "strategy=map 时用于标识条目的字段名" }
    }
  }
}
```

- 在 6.6 R2 表格行"示例"栏后追加的文字：`（模式字段：capability-map 的 extension_points[].merge。值的名称沿用 Kubernetes Server-Side Apply 的 x-kubernetes-list-type）`
- references.md（「## 合并」）：

```markdown
- Kubernetes. *Server-Side Apply*（字段所有权，`x-kubernetes-list-type`、`x-kubernetes-list-map-keys` 合并标记）。https://kubernetes.io/docs/reference/using-api/server-side-apply/
```

### E-5. 让 5.11 遥测名称对齐 OTel GenAI 和 OPA (P5, P6)

- 文件：`docs/05-reference-architecture.md`，5.11 的 JSON 示例及其下方段落
- 建议：把 JSON 中的 `"model_cost"` 改为如下内容，并加入 `"policy"` 键。

```json
  "gen_ai": {"operation.name": "invoke_agent", "agent.id": "builder@harness-x", "usage.input_tokens": 18200, "usage.output_tokens": 2100},
  "model_cost": {"unit_cost_ref": "route:standard"},
  "policy": {"decision_id": "dec_7Q2…", "revision": "tenant/acme@42"},
  "trace": {"traceparent": "00-…-…-01"},
```

- 追加句子：`模型用量属性沿用 OpenTelemetry GenAI 语义约定的名称。该约定仍处于 Development 状态，因此实现需同时记录所遵循的约定版本。策略决策像 OPA 决策日志一样留下决策 id 和策略版本（revision），假名化中抹去的字段以 JSON Pointer 列表标示（7.9）。经过 MCP 服务器的调用，用 MCP `_meta` 的 traceparent 约定归入同一条追踪。`
- references.md（新节「## 观测」，置于「## 体验设计」之前）：

```markdown
## 观测

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/
```

### E-6. 在 5.6 中加入体验平面传输对应表 (P7)

- 文件：`docs/05-reference-architecture.md`，「### 映射示例：Claude Code 钩子」表格之后、「注意：」段落之前
- 建议文字：

```markdown
体验平面不直接接收执行框架事件，而是以面向用户的进度信号接收。若以 AG-UI 作为传输规范，对应如下。

| Mallangable | AG-UI | 备注 |
| --- | --- | --- |
| E2 受理 ~ E11 结束 | `RUN_STARTED` · `RUN_FINISHED` · `RUN_ERROR` | |
| 4 个状态词（8.5） | `STEP_STARTED` · `STEP_FINISHED` | 把 step 名固定为状态词 id |
| 部分预览（8.5） | `STATE_SNAPSHOT` · `STATE_DELTA`（RFC 6902） | 保持"尚未确认"标示 |
| E6 `permission.request`，2.8 `等待批准` | `RUN_FINISHED` 的 `outcome.type = "interrupt"` → 下一次运行的 `resume[]` | 批准以新的运行延续 |

把服务器作业交给外部智能体时，由 A2A 作业状态（`TASK_STATE_INPUT_REQUIRED`、`TASK_STATE_AUTH_REQUIRED`）承担同一角色；在 MCP 工具内部，则由多轮往返请求（`resultType: "input_required"`）承担。Claude Code 对应表中也可以加入 `PostToolUseFailure`（E5）、`Elicitation`（E6）。
```

- references.md（「## 生成式 UI 与扩展标准」）：

```markdown
- AG-UI: Agent-User Interaction Protocol（事件、interrupt）。MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
```

### E-7. 在 8.10 中加入 MCP 路径的机密值输入规则 (P8)

- 文件：`docs/08-experience-design.md`，8.10「### 安全与费用显示」第一项之后
- 建议文字：

```markdown
- 像 `sub` 路径那样在官方助手内部以 MCP 工具运行时，不通过对话或 form 模式输入接收连接密钥或外部服务令牌。MCP 规范要求机密值和凭据使用 URL 模式 elicitation（2026-07-28 版）。密钥一次都不进入智能体上下文，I6 才能得到遵守。
- 在同一版本中，MCP Sampling 计划弃用。不要用把模型调用推给 MCP 客户端的方式来构建 `ModelPort` 适配器。
```

- references.md（「## 生成式 UI 与扩展标准」）：

```markdown
- Model Context Protocol 规范 2026-07-28（变更说明、工具 annotations、elicitation）。https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
```

### E-8. 在 `capability-map` 中加入目录 id 与版本 (P9)

- 文件：`schemas/capability-map.schema.json`，顶层 `properties` 中 `catalog` 之前
- 建议字段：

```json
"catalog_id": {
  "type": "string",
  "description": "D3 目录标识符。为 URI 格式字符串，不必可下载。目录内容变化时值也随之变化（与 A2UI catalogId 语义相同）",
  "examples": ["https://todo.example/catalogs/v3"]
}
```

- 追加位置：在 `schemas/extension-manifest.schema.json` 的 `artifact.properties` 中加入 `"catalog_id": { "type": "string", "description": "D3 产出物所预设的目录。与能力图的 catalog_id 不同则在 G1 拒绝" }`
- references.md：把「## 生成式 UI 与扩展标准」中的 `Google A2UI 报道。The Decoder.` 一行替换为如下内容。

```markdown
- A2UI: Agent-to-User Interface 规范 v0.9.1（`createSurface`、`catalogId`）。Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
```

### E-9. `capability-map` 能力与 MCP 工具提示的对应 (P10)

- 文件：`schemas/capability-map.schema.json`，`$defs.capability.properties.risk` 的 `description`
- 现在：`"egress=外部发送, sensitive=他人·敏感数据"`
- 建议：`"egress=外部发送, sensitive=他人·敏感数据。把能力作为 MCP 工具公开时，read 导出为 readOnlyHint=true，egress 导出为 openWorldHint=true。不信任接收方的 MCP annotations，以此值为权威 (I8)"`
- 增加一个可选字段：`"destructive": { "type": "boolean", "description": "不可撤销的写入。与 MCP destructiveHint 语义相同。为 true 时无论激活策略如何都走 G5" }`
- 在 5.8 G5 行"内容"栏加入 `· 使用不可撤销写入（destructive）能力时`。
- references.md：在 E-7 的 MCP 规范条目中一并写上 `https://modelcontextprotocol.io/specification/2026-07-28/server/tools`。

### E-10. 在 7.7 供应链中指定来源证明格式 (P11)

- 文件：`docs/07-trust-and-security.md`，7.7 控制表中 `一个账号进行了大量上传` 行的"控制"栏
- 现在：`发布者来源签名，限制新发布者，策展等级`
- 建议：`发布者来源签名（in-toto Statement 加 SLSA provenance 谓词。目标为清单 content_hash，builder.id 为执行框架 id），限制新发布者，策展等级`
- references.md（「## 智能体安全」末尾，或新节「## 供应链」）：

```markdown
- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance
```

### E-11. 在 1.5 相关研究中补充可塑媒介的先例

- 文件：`docs/01-introduction.md`，1.5 表格第一行（Malleable software）之后
- 建议行：

```markdown
| 计算媒介与动态文档（Boxer, 1986 · [Webstrates](https://webstrates.net/), 2015 · [Potluck](https://www.inkandswitch.com/potluck/), 2022 · [Embark](https://www.inkandswitch.com/embark/), 2023） | 消除文档与应用的边界，让用户在其上叠加计算 | 不触碰原件的叠加层（2.3），跨越应用的工具（O8） | 定义为在现有商业应用之上、能经受供应商更新的结构 |
```

- 把同一表格中 Local-first 行的链接改为 `https://www.inkandswitch.com/project/patchwork/`，并在"引入的内容"栏追加 `· 把 AI 编辑放在分支上，由人挑选后合并（Patchwork 实验笔记）`。
- references.md（「## 可塑软件与终端用户编程」）：

```markdown
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · 代码(Apache-2.0): https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck: Dynamic documents as personal software.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark: Dynamic documents for making plans.* 2023. https://www.inkandswitch.com/embark/
- Ink & Switch. *Patchwork*（实验笔记 07 "AI bots in version control"）。https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
```

- 备注：Potluck、Embark 的副标题在照搬页面标题之前，需要再与原文核对一次（是用摘要工具读取的）。

### E-12. 把 references.md 中的二手出处替换为一手出处

- 文件：`docs/references.md`
- 要修改的行：

| 现在 | 替换为 |
| --- | --- |
| `Agent Skills 标准整理。Shiplight, 2026. https://www.shiplight.ai/blog/agent-skills` | `Agent Skills 规范（SKILL.md 头部，allowed-tools 为 Experimental）。Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills` |
| `Claude Code 插件概览。https://code.claude.com/docs/es/plugins/overview` | `Claude Code 插件清单参考。https://code.claude.com/docs/en/plugins-reference` |
| `Mergiraf：语法感知 Git 合并驱动。https://docs.rs/crate/mergiraf/latest` | `Mergiraf：语法感知 Git 合并驱动。GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf` |
| `SEP-1865. *MCP Apps …* https://modelcontextprotocol.io/seps/1865-…` | 保持不变，在后面加上 ` · 规范(2026-01-26): https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx` |
| CaMeL 条目 | 在后面加上 ` · 代码(Apache-2.0): https://github.com/google-research/camel-prompt-injection` |

- 正文链接也一并修改：5.6 的 `[Shiplight, 2026]` → `[Agent Skills 规范](https://agentskills.io/specification)`，1.5 的 A2UI、Agent Skills 链接，3.2 A6 的 Automerge 链接 → `https://automerge.org/docs/reference/documents/conflicts/`，6.6 R1 的 Mergiraf 链接 → `https://mergiraf.org/`。
- 把 `确认日期` 更新为采纳日期。

## 4. 未纳入的内容

- **Figma `networkAccess.reasoning` 式的允许理由字段（P12）**：有用处，但目前填写 `network.allow` 的主体不是人，而是生成智能体。智能体写的理由不能作为批准卡片的依据。设计批准卡片（G5）时再看。
- **对齐 WIT、Extism 字段名称**：同样的概念在清单中已经存在，而且只是为了一种产出物格式（`wasm`）而对齐。撰写 D4 `lang` 适配器文档时有一张对应表就足够了。
- **VS Code 激活事件**：延迟加载是运行时实现问题，与契约、合并无关。G3 启动时间预算承担同样的目的。
- **Chrome 式 `optional_permissions`**："需要时再申请"已经由 I4 人工批准流程（E6）表达。再加一个静态声明会让两条路径分叉。
- **把 OPA 作为默认 PDP**：引入其决策日志格式，但能做 I5 包含验证的 Cedar 更符合本规范的单调性要求。
- **单独对齐 MCP-UI、Yjs**：分别引用 MCP Apps、Automerge 就足够了。
- **Smalltalk 谱系**：没有查找一手出处。若要引用，需要核实原始论文。
