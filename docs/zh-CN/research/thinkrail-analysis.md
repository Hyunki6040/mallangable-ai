<!-- LANG-BAR -->
[English](../../en/research/thinkrail-analysis.md) · [한국어](../../ko/research/thinkrail-analysis.md) · **简体中文** · [日本語](../../ja/research/thinkrail-analysis.md) · [Español](../../es/research/thinkrail-analysis.md)
<!-- /LANG-BAR -->

# 调研笔记 — ThinkRail (JetBrains/thinkrail)

> 本笔记的结论：ThinkRail 是包裹 `pi` 编码智能体的**智能体 IDE 宿主（host）**。它与修改用户应用的 Mallangable 对象不同，但"让人能安全接受智能体所做变更（change）的宿主"这一问题是相同的。可以照搬的有五点。① **以所见为依据的回退（revert）**（CAS）。② **不信任评判输出**（格式错误即失败，宿主字段由宿主填写）。③ **批准（approval）绑定到目标指纹，并且有明确范围。** ④ **接受的信任只适用于当时的内容**（之后新增的条目需重新确认）。⑤ **存储数据中不放译文，术语包（lexicon pack）只是数据，共享物不能改变它。** 反过来，"宿主不组装提示词"这一原则不予采纳，因为 Mallangable 的执行框架（harness）是负责强制的一方。

- 确认日期：2026-11-03
- 调研对象：https://github.com/JetBrains/thinkrail（公开，Apache-2.0，JetBrains 孵化项目）。搜索结果中出现的多个同名仓库都是这个仓库的分叉。
- 固定提交：`c10f8808cee693e4abffeeb1844a132ed0a91cc5`（2026-11-03）。以下所有链接均以此提交为准。
- 方法：用 `git clone --depth 1` 克隆到空的临时目录，只**阅读了**规范文档（`SPEC.md`·`architecture.md`·`goal-and-requirements.md`）。没有运行代码。

## 0. 已确认与未确认

| 项目 | 状态 | 依据 |
| --- | --- | --- |
| 仓库是否存在·是否公开 | 已确认 | `gh repo view JetBrains/thinkrail`，克隆成功 |
| 许可证 | 已确认 | [`LICENSE`](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/LICENSE) Apache 2.0。与本仓库的模式·工具方针（Apache-2.0）不冲突 |
| 产品目标·架构文档 | 直接阅读 | `goal-and-requirements.md`、`architecture.md` |
| 服务器子模块规范 | 部分阅读 | `changes`、`host/planReview`、`agent`、`agent/mcp`、`agent/packages`、`extensions`、`todos`、`spec-graph`。其余 `SPEC.md` 未读 |
| 规范与实现是否一致 | 未确认 | 只读了规范文档，没有读源码·测试。下文引用的意思是"ThinkRail 规范是这样规定的" |
| 运行·复现 | 未进行 | 超出调研范围 |

## 1. ThinkRail 是什么

它是在进程内运行 `pi` 智能体，并在其上叠加编辑器·diff·终端·评审 UI 的宿主（[`goal-and-requirements.md` L10-16](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L10-L16)）。它分为三环：引擎宿主、带版本号的通信契约（wire）、UI 客户端（[`architecture.md` L19-28](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L19-L28)）。工作空间是 git worktree，因此多个智能体可以互不冲突地并行工作（[`architecture.md` L107-122](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L107-L122)）。

其原则中与 Mallangable 重合与分歧之处：

| ThinkRail 原则 | 与 Mallangable 的关系 |
| --- | --- |
| **信任是显式的**：克隆的仓库能放进智能体的东西（技能·扩展·MCP 服务器）只在项目级信任批准之后才加载。仓库定义的 MCP 服务器需要另行逐项批准，条目一旦变化批准即失效（[L62-65](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L62-L65)） | 方向相同。对应共享接收的功能（6.9）和 I4 |
| **只通过供给而非注入施加影响**：宿主不组装提示词（[L57-58](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L57-L58)） | 分歧。Mallangable 执行框架（5.6）强制策略，并按角色挑选上下文（5.10） |
| **不重新计算，只展示**：宿主原样展示引擎报告的值（[L59](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L59)） | 方向相同。费用显示（8.10）使用 `ModelPort` 的计量值 |

## 2. 对照表 — ThinkRail 概念 → Mallangable

判定：**采纳**（几乎照搬）、**变形**（只取其意）、**确认**（已有，仅补充依据）、**拒绝**、**搁置**。

| # | ThinkRail 概念 | 出处 | Mallangable 位置 | 判定 | 理由 |
| --- | --- | --- | --- | --- | --- |
| T1 | 回退请求携带"用户所见内容"的哈希，若与当前状态不同则返回 `STALE_VIEW`，什么也不写。客户端不发送内容 | [`changes/SPEC.md` L39-43, L116-118](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/changes/SPEC.md#L39-L43) | 5.5、I3 | **采纳** | 基线版传播、其他设备、监视器自动恢复都可能移动激活状态。如果"把刚才那个回退掉"回退的是另一个状态，F1 反而会变成事故 |
| T2 | 回退回执 id 即重做令牌。重做也是同一个操作。未知 id 不会被悄悄跳过，而是返回 `RECEIPT_UNKNOWN` | [`changes/SPEC.md` L81-112](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/changes/SPEC.md#L81-L112) | 5.5、8.7 | **变形** | Mallangable 的回退是指针移动，不需要字节环。要借鉴的是"重做 = 同一操作"和"做不到时显式告知" |
| T3 | 读取原件失败不等于不存在。若当作不存在，整文件回退会把用户文件送进回收站 | [`changes/SPEC.md` L119-122](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/changes/SPEC.md#L119-L122) | 6.5、2.3（`null` = 删除） | **采纳** | 在 ⊕ 中 `null` 表示删除键。若把读不到上层当作"没有"，传播就会删除用户的功能 |
| T4 | 不信任评审者输出：判定词严格检查，格式错误时不是批准而是失败。结果对象显式重建，丢弃模型编造的宿主专用字段。没有指出问题的"修改请求"予以拒绝 | [`host/planReview.SPEC.md` L62-81](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L62-L81) | 5.8 G4、E12 | **采纳** | E12 只有"判定结果模式检查"，检查失败时的结果没有规定 |
| T5 | 批准是判定而不是确定：只要还有未关闭的问题，approve 也不确定 | [`host/planReview.SPEC.md` L102-106](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L102-L106) | 5.8 G4 | **采纳** | 堵住重新评判轮次覆盖先前问题的路径 |
| T6 | 两个入口（智能体工具·人工按钮）共享同一个修改次数上限。若不共享，修改→评判→修改会无限循环 | [`host/planReview.SPEC.md` L117-119](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L117-L119) | 5.8 G1 重试上限 | **采纳** | 若 G1 上限只挂在一条路径上，成本攻击者（7.1）会绕到另一条路径 |
| T7 | 把评判者作为返回结果的子任务而非会话：结束即返回结果，失败即拒绝，恢复只在一处 | [`host/planReview.SPEC.md` L21-42](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L21-L42) | 5.7 评判者 | **确认** | 评判者已经是只读的，唯一可写的只有判定结果。仅作为依据引用 |
| T8 | MCP 工具调用确认：只询问没有 `readOnlyHint` 的调用。选项为拒绝·仅此一次·在本对话中·始终。"始终"是项目范围，且仅在目标（`command`+`args` 或 `url`）的 SHA-256 相同时有效。所有非肯定的答复（关闭、其他消息、中断）都视为拒绝 | [`agent/mcp/SPEC.md` L129-150](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/mcp/SPEC.md#L129-L150) | 4.8、G5、8.5 | **变形** | 在减轻批准疲劳（4.10）的同时，防止批准泄漏到其他目标。Mallangable 没有批准范围·寿命规则 |
| T9 | 授予信任时，**只把当时存在的内容**视为已确认。之后通过 pull·分支新增的技能为 `pending-ack` | [`agent/SPEC.md` L993-1000](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/SPEC.md#L993-L1000) | 6.9 `subscribe` 共享 | **采纳** | 订阅式共享在发送方每次修改时内容都会变化。如果第一次接受覆盖了之后的内容，就会出现与 7.7 "安装后在远程修改了内容"相同的漏洞 |
| T10 | 同名时信任高的一方获胜：内置 → 个人 → 项目的顺序。仓库无法遮盖我的技能。内置扩展在启用期间，在同名工具冲突中获胜 | [`agent/SPEC.md` L991-992](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/SPEC.md#L991-L992)、[`extensions/SPEC.md` L32-37](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/extensions/SPEC.md#L32-L37) | 6.9、O3 | **变形** | Mallangable 的层合成是"离用户更近的一方获胜"。保持该规则不变，只在**接收的共享物**劫持命令·快捷键等标识符时适用 |
| T11 | 关闭开关会一并关闭扩展贡献的全部内容（工厂·工具·技能）。保留渲染器，使历史记录仍可见 | [`architecture.md` L376-382](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L376-L382) | 5.9 监视器·安全模式（safe mode） | **采纳** | 一个功能跨多个槽位·命令·钩子时，只关掉一个槽位的隔离只做了一半 |
| T12 | 列表查询没有副作用：目录既不安装，也不运行扩展代码。工具名称从实际加载所记录的内容中读取。每次列出都运行工厂的方式被否决 | [`agent/packages/SPEC.md` L23-25, L128-131](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/packages/SPEC.md#L23-L25) | 7.7、7.11 | **采纳** | 若在共享·市场的预览界面运行 D4 代码，就成了批准前执行（违反 5.9 "批准前的 D4 权限为 0"） |
| T13 | 每个计划步骤打开一个工作窗口（开始时的基准线），结束时**只提交该步骤改变的路径**。与其他对话的窗口重叠时标记为 `shared`，不猜测归属 | [`todos/SPEC.md` L64-80](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/todos/SPEC.md#L64-L80) | 6.4、记录者 | **变形** | 同一用户的两个生成作业在一个层中重叠时，就分不清是哪个功能的变更（I9） |
| T14 | `agent_end` 只是尝试边界（重试·压缩后可能继续工作）。只有 `agent_settled` 才是完成。等待输入是电平信号，不会因为看了一眼就被清除 | [`architecture.md` L141-156](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L141-L156) | 5.6 AG-UI 对应、8.5 状态词 | **采纳** | 若在重试中途显示"准备好了"，就会破坏状态词固定规则（8.5） |
| T15 | 兼容性台账：每个弥补引擎缺陷·缺失 API 的适配都写明"升级时要复查的内容"和"可以删除的条件"。规范不重写版本号，而是写明确认了什么 | [`pi-compatibility.md` L11-16](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/pi-compatibility.md#L11-L16)、[`architecture.md` L205-211](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L205-L211) | 5.6 对照表 | **采纳** | 就像 5.6 Claude Code 表中 `onFailure` 的版本条件一样，对照表条目会随运行时版本而过时 |
| T16 | UI 字符串是键目录。硬编码字符串会被 lint 判失败。存储·通信数据中不放译文，渲染时才成句。用户语言文件只从全局数据文件夹读取（使克隆的仓库无法改写 UI）。回落顺序：本地精确 → 内置精确 → 内置默认 → 英语 | [`architecture.md` L430-454](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L430-L454) | 8.9 术语包 | **采纳** | 键目录·lint 已经有了。缺的是存储规则、来源限制、回落顺序。没有来源限制，共享物就能把权限警告文案（"访问患者信息"）改成温和的说法 |
| T17 | 不翻译智能体·工具输出 | [`architecture.md` L443-444](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L443-L444) | 8.9 适用位置（E13 解说者） | **拒绝** | ThinkRail 的用户是开发者。对 Mallangable 的 basic 用户，解说者必须用通俗用语重写 |
| T18 | 子智能体的信任既不能超过父节点**加载的**信任，也不能超过当前记录。撤销时子节点随之撤销 | [`agent/SPEC.md` L1443-1452](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/SPEC.md#L1443-L1452) | 5.7 角色、I4 | **确认** | 已由 I4·角色分离保证。仅作为依据引用 |
| T19 | 评审批注用引擎中立的选择器（`lineRange`·`textQuote`·`json-pointer`·`region` 等）挂接，由渲染器报告"已放置/未能放置" | [`architecture.md` L330-346](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L330-L346) | 8.2 界面指认、6.12 | **搁置** | 这与基线版变化后指认锚点悄悄贴到其他元素上的问题相同。在确定能力图（capability map）格式时（10.4 路线图）再看 |
| T20 | 宿主不组装提示词 | [`goal-and-requirements.md` L57-58](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L57-L58) | 5.6、5.10 | **拒绝** | 执行框架是"包裹非确定性智能体的确定性外壳"（5.6）。上下文供给（5.10）是守护 I6 的手段 |

## 3. 已反映的编辑

措辞并非照搬 ThinkRail 的句子，而是重写了概念，并在每处留下了出处。

| # | 对应 | 文件·位置 | 内容 |
| --- | --- | --- | --- |
| E-1 | T4·T5·T6 | `docs/05-reference-architecture.md` 5.8「评判输出处理」 | 格式错误 = 失败，宿主字段由宿主填写，拒绝没有指出问题的修改请求，有未关闭问题时不确定，重试上限由所有入口共享 |
| E-2 | T1·T2 | 5.5「回退以所见为依据」 | `revert(expect=所见状态 id)`，不一致则什么也不做并展示当前状态，重做 = 同一操作，做不到时显式告知 |
| E-3 | T11 | 5.9「监视器与安全模式」 | 隔离·关闭单位是整个功能。回执·记录仍然可见 |
| E-4 | T14 | 5.6 AG-UI 对应之下 | 尝试边界 ≠ 完成，等待批准是电平信号 |
| E-5 | T15 | 5.6 映射示例之下 | 对照表每个条目写明已确认的行为·复查条件·删除条件 |
| E-6 | T8 | `docs/04-control-spectrum.md` 4.8 部署原则 | 三种批准范围，批准 = 绑定到目标指纹，非肯定的答复即拒绝，只读操作不询问 |
| E-7 | T3 | `docs/06-versioning-and-lineage.md` 6.5 规则 | 不把读取失败当作删除（`null`） |
| E-8 | T13 | 6.4 | 并发生成各用独立的工作副本，记录只含自己的路径，重叠时禁止猜测归属 |
| E-9 | T9·T10 | 6.9 规则 | 接受只针对当时的内容，接收的共享物不能劫持标识符 |
| E-10 | T12 | `docs/07-trust-and-security.md` 7.11 | 列表·预览·权限显示不运行代码，只依据清单（manifest） |
| E-11 | T16 | `docs/08-experience-design.md` 8.9「存储与来源」 | 以概念 id + 参数存储，术语包来源限制，回落顺序 |

## 4. 未纳入的内容

- **模式变更**：把 E-6 的"批准 = 目标指纹"作为模式字段加入一事已推迟。目前的规则可以用现有的 `permissions_delta`·`approved_by` 表达。等到确定将批准记录与变更记录分开存储的格式时再加入。
- **照搬基于 worktree 的工作空间**：Mallangable 的隔离单位是仓库，作业单位是分支（6.4）。如何创建工作副本（worktree·临时克隆）留作实现选择。
- **精确的版本固定规则（architecture 决定 10）**：这是仓库运营规则，不是规范内容。只把"规范不重写版本，而是写明确认了什么"这一主旨反映在 E-5 中。
- **回执环上限（20 个·64 MiB）**：Mallangable 的回退是指针移动，因此不适用。
