<!-- LANG-BAR -->
[English](../../en/research/adversarial-review.md) · [한국어](../../ko/research/adversarial-review.md) · **简体中文** · [日本語](../../ja/research/adversarial-review.md) · [Español](../../es/research/adversarial-review.md)
<!-- /LANG-BAR -->

# 对抗性评审 — Mallangable-AI v0.1 (2026-10-30)

评审对象：`README.md`、`docs/01~10`、`docs/glossary.md`、`docs/references.md`、`schemas/*.json`、`examples/*.yaml`、`tools/design_space.py`。
视角：程序委员会、安全评审者、只看这份规范就要动手实现的工程师。除本文档外，没有修改任何文件。

验证环境：Python 3 (stdlib)，`/tmp/mreview/venv` 中装有 `jsonschema 4.26.0` 和 `pyyaml 6.0.3`。辅助脚本全部位于 `/tmp/mreview/*.py`（仓库之外）。

---

## 0. 摘要

数值计算、模式（schema）是否通过、配置表、BM 矩阵，在**机械层面全部正确**。问题在于，这些数字和模式并不能保证规范正文所*主张*的内容。最大的缺陷有五个。

1. 在 `A5=own` 的情况下，仍把上层产出物交给对话式生成者（generator）。这正面违反了 I6 和 3.2 的核心原理。P2 和 P6 属于这种情况。
2. **契约（contract，κ）没有可执行的表示。** 契约是模型的中心，但模式里只有自由文本，而且编写契约的一方正是生成者自己。因此 I2、I7、I10、G2、B9、SBR 全都失去依据。
3. **合规定义与推荐配置相互矛盾。** Core 等级要求"在设计上"保证 I1~I10（含 I8）。但 P1 和 P5 正如 4.8 自己承认的那样没有服务器，因此无法保证 I8。
4. 如果严格按照 2.6 的深度（depth）定义（D3=声明式，D4=沙箱代码），头条数字（70,516）以及 7 个配置中 5 个的"推荐"判定都会崩塌。
5. 传播（propagation）算法（6.5）和契约保持合并（contract-preserving merge，6.7）无法照原样实现。它们忽略中间层，在等待批准的父节点之下子节点的作业会停滞，而且契约单调性与"迁移到上游方式"相互冲突。

---

## 1. 经机械验证的事实

### 1.1 计算器输出与文档数值 — 全部一致

`python3 tools/design_space.py --markdown`（2.6 秒）：

| 项目 | 工具输出 | README | docs/03 | docs/01 |
| --- | ---: | ---: | ---: | ---: |
| 原始组合 | 1,944,000 | ✓ :65 | ✓ :224 | ✓ :40 |
| 通过 L | 193,725 (9.97%) | ✓ :66 | ✓ :225 | — |
| 通过 L+N | 124,102 (6.38%) | ✓ :67 | ✓ :226 | — |
| 推荐 | 70,516 (3.63%) | ✓ :68 | ✓ :227 | ✓ :40 |
| 结构族 | 1,618 | ✓ :69 | ✓ :229 | ✓ :40 |
| 平均补全 | 43.58 / 75 (58%) | ✓ :70 | ✓ :230 | — |
| 各规则首次违反数 L1~L11、N1~N5、S1~S7 | （表） | — | ✓ :237-247 全部 | — |
| 各深度推荐数 D1 8,616 / D2 8,616 / D3 37,968 / D4 14,968 / D5 348 | ✓ | — | ✓ :256 | — |
| 补全分布 72:224、57:224、42:322、28:270、24:171 | ✓（60:48、48:48、40:48、38:106、36:69、32:88 以"等"省略） | — | ✓ :231 | — |
| "没有任何族拥有 credits·none 补全（N3）" | 对应族 0 个 | — | ✓ :231 | — |
| Ω = 5×3×3×4×3×4×4×3×5×5×3 | 1,944,000 | — | ✓ :224 | — |

- `--check all`：P1~P7 全部 `clean`，无违反、无警告。与 03:268 一致。
- `--profile` 示例（README:111）：`"result": "logical", "violated": "L1"`。与 README:112 一致。
- 将 `--bm` 的 7×20 矩阵与 docs/09:60-79 逐格比对，全部一致（`/tmp/mreview/bmdiff.py`）。
- `--bm-stats` 的 20 行全部与 docs/09:85-99 一致。
- `examples/profiles.yaml` 与 `PROFILES` 的名称、11 个轴的取值在 P1~P7 上全部一致。

### 1.2 模式验证

`Draft202012Validator.check_schema` 的结果显示 5 个模式全部有效。示例文件在开启 `FormatChecker` 的情况下对多文档逐一检查。

```
capability-map.example.yaml[doc 0]      OK
change.example.yaml[doc 0], [doc 1]     OK
extension-manifest.example.yaml[doc 0]  OK
lexicon.ko.yaml[doc 0], [doc 1]         OK
policy.example.yaml[doc 0..2]           OK
```

- `profiles.yaml` 没有对应的模式，因此只与工具比对了取值（见 1.1）。
- 也检查了示例之间的引用。`capability-map` 的 5 个 `lexicon_id` 和 manifest 的 `label` 都在术语包（lexicon pack）中，教育包覆盖的 id 也全部存在于默认包中。change 示例中的 `points` 和 `permissions_delta.add` 也都在 capability-map 中。basic 表述和 explain 文案中没有出现任何 `basic_forbidden` 词。

**反向测试**（`/tmp/mreview/neg.py`）。这些是规范禁止、但模式却放行的文档。

```
ACCEPTED :: D4 + permissions_delta.add, no G5, no approved_by (I4)
ACCEPTED :: judge_instance == generator_instance (I7)
ACCEPTED :: G4 pass but no judge_instance (I7)
ACCEPTED :: contract = single judge item, deterministic defaulted true (2.5)
ACCEPTED :: D5 record with only G0 (5.8 requires G0-G5)
ACCEPTED :: points with invalid id
ACCEPTED :: intent = 4 spaces (I9)
ACCEPTED :: manifest D3 + form native (2.6 D3=声明式)
ACCEPTED :: manifest D4 + native (2.6 D4=沙箱代码)
ACCEPTED :: network allow '*' with no egress capability
ACCEPTED :: D4 sandboxed with no state/migrate (5.9)
ACCEPTED :: depth ceiling D9 / default banana
ACCEPTED :: org depth ceiling D5 > tenant D3 (I5 not checkable)
ACCEPTED :: default outside ceiling
rejected :: provenance.at = 'yesterday'
rejected :: floors missing 6 of 7
```

### 1.3 交叉引用（`/tmp/mreview/xref.py`）

- 相对链接：失效链接 0 个。
- 章节编号引用（`2.6`、`6.11` 等）：所有引用都有对应的标题。被判为不一致的只有百分比（9.97 等），属于误报。
- id 系列 A1~A11、I1~I10、F1~F7、G0~G5、R0~R5、P1~P7、B1~B20、O1~O13、E1~E16、L1~L11、N1~N5、S1~S7、T0~T4、X1~X6：既没有超出范围的 id，也没有只定义未使用的 id（`L0` 是 mermaid 节点名，无关）。
- 只出现在 references.md、正文未引用的 URL：`https://code.claude.com/docs/es/plugins/overview`（references.md:22）。
- 正文引用但 references.md 中没有的 URL：无。
- HTTP 状态：24 个中 23 个为 200。只有 `thehackernews.com/...341-malicious-clawhub.html` 返回 403（拦截机器人），未能确认。

### 1.4 外部来源核对（WebFetch）

| 主张（位置） | 核对结果 |
| --- | --- |
| Claude Code 钩子 30+ 事件、5 种处理器、管理员拦截、`onFailure:"block"`、`updatedToolOutput`、`PostToolBatch`（05:261-274） | 全部存在。事件为 33 个。存在 `allowManagedHooksOnly`。`onFailure` 只在 v2.1.295 及以上的 command·http 钩子中生效，**对 `Stop`、`SubagentStop` 无效** → L-07 |
| CaMeL 77% 对 84%（07:104） | 一致（AgentDojo）。文档中漏掉了基准测试名称 |
| Unit 42：22MB 膨胀、2026 年 2~5 月分析、"skill logic 与 agent authority 之间缺乏隔离"（07:162） | 一致（2026-06-23） |
| 341 个恶意、Koi Security（01:17、07:162） | 通过 Unit 42 文章确认了 341 个和 Koi。**2,857 个审计数因 403 未能确认** |
| Ink & Switch 随笔、2025、"仅靠 AI 代码生成不够"、MacLean 1990、Nardi & Miller（01:7-9、01:63） | 一致（2025 年 6 月）。原文的比喻是 "appliances: built far away, sealed, unchangeable"，"从商店买来的"属于意译 |
| The Register：禁止第三方使用 Free·Pro·Max OAuth 令牌，包括 Agent SDK（03:135、08:272、09:132） | 一致（2026-02-20 修订。该政策本身自 2024-02 起就存在） |
| falcao.org 时间线（09:132） | 大体正确。文章的顺序是 1 月 9 日服务器端拦截、4 月 4 日正式化、6 月 15 日 **Agent SDK 额度**（按原价，不结转）。文档漏掉了 1 月的拦截，并泛化为"Claude Code 之外的程序化使用" |
| MCP Apps：强制沙箱 iframe（03:67） | 与 "Mandatory iframe sandboxing" 一致。SEP 状态为 Final |
| Shiplight：`allowed-tools` 为实验性（05:236） | 一致（2026-08-10） |

### 1.5 用工具额外计算的值（`/tmp/mreview/indep.py`、`alt.py`、`more.py`、`q.py`）

| 计算 | 结果 |
| --- | --- |
| 各规则**独立**违反数（与顺序无关） | L3 518,400 · L5 486,000 · **L1 432,000** · L4 388,800 · L8 364,500 · L10 324,000 · L7 324,000 · L2 259,200 · L11 162,000 · L6 162,000 · L9 121,500 |
| 各规则**唯一违反**数（只违反该规则） | L3 129,150 · L5 116,235 · L7 77,490 · L4 64,575 · **L1 60,750** · L2 39,150 · … |
| 推荐中 D3 组合的 A2 分布 | sandboxed 21,588 · decl 8,616 · **native 7,764** |
| 推荐中 D4+native 组合数 | **4,044** |
| 推荐中 348 个 D5 组合的 A6 | **全部为 snapshot**。其中 A8=public 的有 104 个（client 32 · server 48 · hybrid 24） |
| 按 2.6 定义加入 `D3⇒decl`、`D4⇒¬native` 规则时 | 推荐 **37,120**，族 875。**P1、P2、P5、P6、P7 落为 `logical` 被淘汰** |
| 加入 `A5=own ⇒ A3=server` 规则时 | 推荐 52,264，族 1,246。**P2 和 P6 被淘汰** |
| 将任何规则都不区分的取值折叠后（D1≡D2、V0≡…≡V3、preview≡gated、proposed≡auto）剩余的推荐构型数 | **8,969**（折叠后分类不变） |
| 结构轴各取值的平均补全数最大·最小差 | **A1 23.2** > A3 21.7 > A2 13.6 > A4 13.4 > A8 12.1 > A5 11.5 > A6 11.3 > A7 1.2 |

### 1.6 工具健壮性

```
--check P9                → KeyError: 'P9' (traceback)
--profile '{bad'          → json.decoder.JSONDecodeError (traceback)
--profile 中添加 "A12":"x" → 无报错，clean
```

仓库中没有任何针对计算器的 self-check 或 assert。

---

## 2. 发现事项（按严重程度排序）

### CRITICAL

| # | 位置 | 证据 | 最小修改 |
| --- | --- | --- | --- |
| C-01 | docs/05:363、docs/05:45、docs/03:83、docs/02:198 (I6)、tools/design_space.py:64 | 5.10 表中生成者的"上层产出物"一栏在 `own/open 时` 为 ●。5.2 把 hybrid 的对话式生成位置放在"设备"上。然而 3.2 A5 说"智能体能读到的代码，最终和该智能体对话的人也能读到"，I6 也有同样的要求。结果是在 `own`（只看自己的）情况下，对话中的生成者却能看到上层代码。工具里没有 `own ⇒ server` 这样的约束（L10 只限制拓扑（topology））。加入这条规则后 **P2 和 P6 会被淘汰**（1.5） | 将 5.10 中生成者一栏在 `own` 时改为 **"仅类型·能力图，产出物为 —"**。若做不到，则添加 L12 `A5=own ⇒ A3∈{server}`，或明确规定在 hybrid 下读取上层产出物的生成强制在服务器上进行。重新计算 P2 和 P6 的判定以及 3.4 的数值 |
| C-02 | docs/02:92-108、schemas/change-record.schema.json:81-91、docs/05:286、docs/06:157-167、docs/09:114 | 契约被定义为"`k_i : A → {真, 假}`"，但模式中的 `contractItem` 的 `given` 和 `expect` 是**自由文本**（例："面板首次显示在 200ms 以内"）。没有字段可以承载要执行的查询、测试夹具（fixture）和环境固定信息。而且 5.7 把契约的编写者定为**生成者**（"生成产出物·契约"）。因此即便有 I7（生成与评判分离），G2 的评判标准也由生成者亲自编写。I2、I10、B9（出售存活保证）、SBR 都依赖这一表示，却无法进行机器评判。`deterministic` 的默认值是 `true`，所以只有一个 `check: judge` 项的契约也能通过（1.2） | ① 在 `contractItem` 中用 `oneOf` 提供 `tree-query{selector, fixture_ref, assert}`、`unit{entry, input, expected}`、`snapshot{env_ref, baseline_ref}` 这类可由机器执行的形式。② 当 `check: judge` 时将 `deterministic` 固定为 `const false`，并在 `contract` 中加入 `contains: {properties: {check: {enum: [tree-query, unit, snapshot]}}}`，以强制 2.5 的"确定性契约 ≥1"。③ 在 5.7 中加入 **"契约草稿由解释者在任务说明阶段编写，生成者不得删除或削弱契约"**，把 I7 的范围扩展到契约 |
| C-03 | docs/10:64-65、docs/02:200·204、docs/04:166-167、docs/03:268 | Core 等级是"在设计上保证 I1~I10"。I8 是"最终执行只在运营方边界进行"。然而 4.8 自己写道："离线个人模式（P1）没有服务器，因此设备上的 PDP 是唯一的"。因此 **P1 和 P5（A3=client，无服务器）按定义不符合 Core。** 可 03:268 仍把两者作为"推荐"介绍。从 Governed 以"Core + 服务器接收检查（receive-check，I8）"再次要求 I8 来看，作者似乎也认为 Core 中并不包含 I8。I4 的人工批准（approval）强制在客户端也可以被绕过 | 把 I8 从 Core 中移出，改为 Governed 的要求。将 Core 定义改为"I1~I7、I9、I10"，并同时修改 2.9:204 的合规判定语句。在 3.5 中明确"P1·P5 最高到 Core 等级，不能达到 Governed" |

### HIGH

| # | 位置 | 证据 | 最小修改 |
| --- | --- | --- | --- |
| H-01 | docs/02:118-119、docs/07:113、tools/design_space.py:48-53、schemas/extension-manifest.schema.json:63-76、docs/03:272-273 | 2.6 把 D3 定义为"声明式 UI 树"，把 D4 定义为"沙箱中的任意代码"。然而 7 个配置中有 5 个是 `A1=D3, A2=sandboxed`。推荐组合中还有 7,764 个 D3+native 和 4,044 个 D4+native。manifest 模式也允许 D3+native 和 D4+native（1.2）。若把 L3 的逻辑（"在不需要代码的深度上允许代码产出物是冗余的"）也套用到 D3，推荐会降到 37,120，P1、P2、P5、P6、P7 被淘汰（1.5）。另一方面，7.6 写着"框架 … 面板（D3）"，manifest 示例的 `format` 中有 `html-panel`。关于 D3 是否允许代码，规范自身存在分歧 | 统一为一种。(a) 将 D3 重新定义为"目录式声明 **或** 经框架隔离的面板代码"，并把 2.6 表中的"执行前分析：大部分"降为"仅限声明式"；或者 (b) 将 L3 扩展为 `A1∈{D1,D2,D3} ⇒ A2=decl` 并修改配置。无论哪种，都要加入阻止 D3/D4+native 的 L 规则以及 manifest 的 `allOf` 条件 |
| H-02 | docs/02:142（D5 分离 MUST）、docs/02:193 (I1)、tools/design_space.py:25 | A1=D5 表示"用户可以一直改到核心（core）"。这直接违反 I1（用户层不改变 C）以及 2.6 的"D5 不是用户层"。然而工具仍把 348 个 D5 组合判为"推荐"。它们全部是 snapshot，其中包括 104 个公开共享的原生核心补丁（1.5） | 加入 `N6: A1=D5 ⇒ (A8=none ∧ A6≠snapshot)`，或把 A1 的取值范围缩小到 D1~D4，并把 D5 移到轴之外，作为"核心分叉流程"这一独立概念。重新计算 3.4 和 README 的数值 |
| H-03 | README:72、docs/03:261、docs/03:233 | 主张为"原始组合中 90% … 不合理"、"过滤最多的规则是 L1"、"意味着最常见的设计矛盾"。但是 ① L3 和 L5 是规范化（去重）规则，而不是过滤"不合理组合"的规则。独立违反数 L3 为 518,400、L5 为 486,000，都多于 L1 的 432,000。② L1 排第一是"首次违反"统计顺序造成的。按唯一违反数看，L1 是 60,750，排第 5（1.5）。03:233 刚亲自警告过顺序依赖性，紧接着就把它用于解读。③ 组合数并不是设计者的需求频率。因此"最常见的设计矛盾"是无法证伪的主张。④ 70,516 中有一部分是被任何规则都不区分的取值（V0~V3 等）撑大的，折叠后为 8,969 | 将解读 1 改为"除去规范化规则（L3、L5）后 …"，并在表中同时列出独立·唯一违反数。把 README:72 的"最常见的"改为"代表性的"。在 3.4 加脚注："对取值分辨率敏感，规则所区分的构型为 8,969" |
| H-04 | docs/06:99-120 | 传播伪代码无法照原样实现。① `merge(..., theirs=r)` 对孙节点也合并**原始发布 r**，因此中间（租户、组织）层的变更被遗漏。② `contracts = κ(r) ∪ κ(m)` 也遗漏了中间层的契约。③ 由于 `where parent(m) has applied r` 条件，父节点若处于 `proposed` 状态等待批准，子节点在这个循环中将永远得不到处理，也没有重新触发的机制。④ `parallel_for` 循环体内的 `return` 语义未定义。⑤ `canary(descendants_in_topo_order…, ratios)` 取拓扑顺序前 5%，因此金丝雀不是随机样本，而是一组上层节点。⑥ "相同原因"失败率缺少原因分类标准。⑦ "每个节点 1 个作业，有新发布就取消"在发布周期短于批准延迟时会造成饥饿（starvation） | 改为 `theirs = parent(m).main@after_apply(r)`，并把契约定义为 `⋃_{a ∈ ancestors(m)} κ(a) ∪ κ(m)`。改写为事件驱动方式，由父节点应用事件（`baseline.applied`）生成子节点作业；金丝雀定义为"同一深度节点中的随机样本"。失败原因键设为 `(门 id, 契约 id, 扩展点)`。在 6.5 中补充一个状态机 |
| H-05 | docs/02:54·71、docs/06:83-95、docs/06:157-169 | 存在两种合并模型。2.3 在运行时以**覆盖（⊕）合成**各层，而 6.4 把用户仓库作为基线版（baseline）的**分叉并做三方合并**。如果层是合成的，上游变更就应当是契约复检的对象而不是合并；如果是分叉，就不需要 ⊕。实现者无法决定要做哪一种。此外，6.7:165 的"契约只能变强"与 6.7:169 的选项"迁移到上游方式"（必须放弃用户契约"侧边栏面板"）以及 6.12 的扩展点废弃（κ_down 原理上无法满足）相冲突。然而 8.8 却把"7 个中有 6 个原样迁移了"当作一般情况来展示。上游契约 κ(r) 存放在哪里（没有模式）也没有定义 | 在 2.3 中统一为"存储为分层差量，合成用 ⊕，合并只用于*同一层内*的并发修改"。在 6.7 规则 2 中加入"人在 R5 中做出选择的情况、以及因扩展点废弃引起的契约迁移（contract migration，rename map）属于例外。记录中留下 `Contract-Migrated`"。新增用于承载发布契约的 `baseline-release.schema.json` |
| H-06 | schemas/change-record.schema.json:7·33-46·61-76、schemas/extension-manifest.schema.json:31-41、schemas/policy.schema.json:92-99 | 14 个反向测试通过（1.2）。具体包括：权限增加却没有 G5 和 `approved_by` 的记录（I4）、`judge_instance == generator_instance`（I7）、G4 为 pass 却没有评判者记录、D5 只有 G0（5.8）、只由空白构成的 intent（I9）、D3/D4 native、`network.allow:["*"]` 却没有 egress 权限、`depth.ceiling: D9`、超出上限的 default。这些都是模式能拦住却没有拦住的 | 只修复模式内部能修复的部分。若 `permissions_delta.add` 有 `minItems:1`，则把 `gates.G5 const approved` 和 `provenance.approved_by` 设为 `required`（`if/then`）。`validation.gates` 按 depth 设定 `required`。`intent` 加上 `pattern: "\\S"`。`points.items` 使用与 capability-map 相同的模式。orderedKnob 改为按旋钮（knob）分别设 `enum`。在 manifest 的 description 中写明：`network.allow` 非空时要求 permissions 中有 egress 权限（因为这是跨文档检查）。I5 和 I7 的"彼此不同"这类跨文档·值比较交给**合规校验工具**，并写入文档 |
| H-07 | docs/07:18-28、docs/05:286-288、docs/06:167·196 | 威胁模型漏掉了三种情况。① **契约·评判者污染**：被注入的生成者可以编写放行恶意行为的契约，或在产出物中植入针对评判者的指令（"此面板满足意图"）。评判者没有外部通信，但仍完全暴露于*完整性*攻击之下。② **解决缓存（resolution cache）污染**：同一租户内的恶意用户仅凭自己的契约制造出"已验证"的解决方案后，会通过 R3 被该租户的所有人复用。6.8 的范围限制只能阻止租户*之间*的泄露，挡不住租户*内部*的横向移动。③ **受损的上游发布·运营方**：没有讨论签名（06:91）的密钥管理与吊销、`auto` 应用时的影响范围，以及运营方以官方基线版下发恶意变更的情况 | 在 7.1 攻击者表中增加三行。控制措施分别如下。① 契约归解释者所有，评判者的输入只按既定模式接收（产出物原文不进入评判者上下文）。② 只有在由创建该解决方案的用户以外的 k 个以上节点重新验证之后，才写入缓存。③ 按 PEP 钉住发布签名密钥，`auto` 应用也强制金丝雀，并赋予租户拒绝上游发布的权利 |
| H-08 | docs/06:273 vs docs/09:116·119 | 6.10 承诺"**不把客户制作的产出物放进官方基线版** … 用文档承诺这一原则是企业客户信任的前提"。然而 B19 是"把广泛共享的功能晋升（promotion）为官方付费扩展，并与原作者分成"，B10 是"被组织·**官方**基线版采纳即给予奖励"。同一份规范内承诺与商业模式正面冲突 | 将 6.10 的句子改为"不放入**未经同意的**客户产出物。公开（A8=public）共享物只有在获得原作者明确的许可同意时才晋升"，并在 B10 和 B19 的条件栏中引用此条 |
| H-09 | docs/02:180-181·187、docs/05:189、docs/05:338 | ① 2.8 写道"**通往激活的所有路径都经过验证**"，但同一张图中的 `搁置 --> 激活：按用户选择重新解决` 并不经过验证。② 5.4 流程 1 的最后一步 `E->>S: activate(状态)` 不经过 PDP、E10 `activate.before`、G5，由体验平面直接调用存储。这个流程中完全没有批准路径。③ 5.9 热替换（hot swap）第 1 步是"通过 G2 后预先挂载到隐藏槽位"。批准（G5）之前的 D4 代码可能获得权限并被执行 | ① 改为 `搁置 --> 验证中`。② 在 5.4 中加入 `S->>P: activate 决定` 一步并画出 G5 分支。③ 隐藏槽位挂载附加条件"G5 通过后，或仅以 0 个权限" |

### MEDIUM

| # | 位置 | 证据 | 最小修改 |
| --- | --- | --- | --- |
| M-01 | schemas/capability-map.schema.json:5·45-61、docs/02:24-40、docs/06:202-212、docs/05:372-383、docs/06:288 | 有多个对象文档中有定义却没有模式。共享（6.9 YAML）、基线版发布·谱系（lineage）节点（6.3）、传播作业、`AccessRequest`·`Decision`（4.8、5.3）、遥测事件（5.11 JSON）、记录所引用的 `contract.yaml` 文件。capability-map 模式在 description 中写了"状态模式"，但**没有 Σ 字段。** 2.2 中的 `in/out` 名称也与模式的 `input_schema/output_schema` 不同，而模式中的 `d_max` 和 `version` 在 2.2 的定义里没有。change-record 没有生命周期状态（搁置·已被取代）字段，`parent_state` 是可选字段，因此无法强制 I3 的"已记录的上一状态" | 先只新增 `share.schema.json` 和 `baseline-release.schema.json` 两个（其余放到 v0.2）。在 capability-map 中加入 `state_schema`，并让 2.2 的元组对齐模式字段名。将 change-record 的 `provenance.parent_state` 改为 `required`，并新增 `status` enum |
| M-02 | docs/02:147-161、docs/04:14-24·46-64·77-83、schemas/policy.schema.json:55-68·65 | 策略（policy）格中有四处漏洞。① `valueKnob`（code_visibility、model_route、admin_visibility）没有顺序，无法判定 I5（`p_child ⊑ p_parent`）。② 没有规定每个旋钮的"风险"是对谁的风险。管理可见性对用户有风险，上限却由租户设定。因此如果 `p_U` 参与求交，用户就能调低管理员可见性。"锁定"预设把基线版应用设为风险最高的 `auto`。③ 没有处理区间交集为空（下级下限 > 上级上限）的规则。④ 预设使用的旋钮"直接生成"、"安装深度"、"门批准者"（`p.gate_approver`，04:161）、"验证强度"在模式中不存在。另外 F6（"超过即停止"，必须）的 `on_exceed` enum 中有 `notify`，可能违反下限 | 在表中为每个旋钮增加 `order` 和 `risk_bearer`（user/tenant/operator），并按旋钮指定参与求交的行为者。交集为空时按"上级优先 + 审计事件"处理。在模式中新增 `create`、`install_depth`、`gate_approver`，并从 `on_exceed` 中删除 `notify`，或将 `notify` 重新定义为"停止后通知" |
| M-03 | docs/03:202-203、tools/design_space.py:78-81、docs/09:35·44 | N3（credits ⇒ A10≠none）和 N4（public ⇒ A10≠none）把**租户管理员可见性**（A10）与**运营方计量·审计**（MeteringPort，5.3）混为一谈。额度计费由运营方计量即可，与租户管理员能看到什么无关。这一混淆被带进了 N3 的 7,659 个和 N4 的 6,540 个过滤结果，以及 B12 和 B16 的判定 | 把运营方计量作为轴之外的常设前提并删除 N3，或在 `A10` 之外另设"运营方审计级别"轴。至少要把 N3 和 N4 的依据措辞改为"运营方计量"，并重新审视条件 |
| M-04 | docs/07:121-131 | 信息流标签 `λ=(范围, 等级)` 的 ⊔ 没有定义*范围*如何合并（租户 A 与 B、因共享而混在一起的用户范围）。等级 V0~V3 直接把管理可见性档位重用为数据敏感度，因此无法确定用户业务数据（待办事项正文）属于哪个等级 | 把范围定义为集合，⊔ 为并集，查看条件为"查看者范围 ⊇ λ.范围"。在等级中加入 `D`（用户数据），作为与 V3 不可比较的元素 |
| M-05 | docs/03:320、docs/03:343-347 | 3.6 流程图中的 `公开 → A4≥frame` 与声明式产出物（L5：decl ⇒ A4=none）以及 P4（public、decl、none）相矛盾。3.7 演进图的箭头标签也与实际的轴差异不符（1.5 的 diff）。P3→P7 只写了"A10 V3"，实际上 **A1 D4→D3** 也变了。P4→P6 写的是"A6 fork"，但 P6 是 `lineage`，实际上有 8 个轴（A1~A7、A11）发生变化。P1→P2 漏掉了 A5、A9、A10，P2→P3 漏掉了 A1、A4、A9、A11 | 改为 `V1["若为代码产出物则 A4≥frame …"]`。把箭头标签换成由工具生成的 diff，并把 P4→P6 的"A6 fork"改为"A6 lineage" |
| M-06 | docs/03:263 | "**智能体位置是对商业模式约束最强的结构决定**"。按工具的平均补全数看，结构轴中差异最大的是 A1（23.2），A3 以 21.7 排第 2（1.5）。只有在只看 A9（模型获取（model sourcing））时，A3 才排第 1 | 把范围收窄为"对模型获取（A9）约束最强的"，并以各轴平均补全数表作为依据 |
| M-07 | docs/02:195 (I3)、docs/05:119·338-341、schemas/extension-manifest.schema.json:44-51、docs/06:318-323 | I3 说回退"无需生成、常数时间"，但 ① 回退一个状态模式已改变的扩展时，需要*反向*的状态交接，而 `migrate_from` 只能表达正向。② CRDT 拓扑中的回退不是指针移动，而是逆操作合并。③ 回退无法撤销外部效果（已发送的 Slack 消息），用户文案（8.7"立即、免费"）把这一点掩盖了 | 将 I3 改为"**层状态**的回退是常数时间。扩展内部状态在没有 `migrate_to_prev` 时会被初始化，外部效果不予撤销"，并在 manifest 中新增 `migrate_to` |
| M-08 | docs/10:40-58·62-66、docs/02:204 | ① SBR 的分母只有"自动合并"，因此 `proposed` 模式下人随手批准了有问题的合并的情况（A7 的默认推荐值！）不被测量。② 没有可复现性规约，例如如何构造隐藏检查、种子与重复次数、模型版本固定。③ 没有用于判定"在设计上保证"的合规测试集（推迟到 v0.3），因此现在的合规等级无法证伪 | 把 SBR 分母改为"自动 + 提议后批准的合并"，并分别报告二者。在 10.2 中加入可复现性条目（运行 k 次、模型·提示词哈希）。现在就在文档中为每个合规等级写下至少 3 个测试向量（例：权限增加但未批准则拒绝、judge==generator 则拒绝、空契约则拒绝） |
| M-09 | docs/03:192、tools/design_space.py:62-63 | L9（`crdt ⇒ A7≠manual`，"CRDT 是自动合并"）混淆了范畴。A7 是**从上游基线版到下游的传播**，CRDT 是**副本之间的同步**。CRDT 文档同样可以手动接受上游模板的新发布 | 删除 L9，或先定义"在 crdt 中 A7 指上游模板传播"，再重新确定条件 |
| M-10 | docs/06:208·230、docs/02:118、examples/capability-map.example.yaml:50-55、docs/07:150 | ① 在订阅式共享中，发送方每次修改功能（feature），接收方都会产生传播作业和费用。成本攻击者（07:28）可以利用这条路径，却没有控制措施。② D3 声明式组件（chart、card）渲染远程图片·URL 本身就是 egress，但目录和 G1 规则中没有网络限制 | 在 6.9 中加入"subscribe 传播成本在接收方上限之内，每天限 n 次"。在目录模式中设 `fetches_remote: boolean`，让获取远程资源的组件必须要求 egress 权限 |
| M-11 | docs/02:199 (I7)、docs/04:103 | I7 只要求"不同的实例"。没有依据表明，同一模型、同一提示词、同一上下文的另一个实例就能减少自评偏差。这是没有依据的主张 | 强化为"不同实例 + 不查看生成者的推理·对话记录 + （尽可能）不同的模型路径"，并把效果作为测量课题放入 O4 |
| M-12 | docs/02:54·71 | ⊕ 只定义了"离用户更近的层获胜"。没有手段（`final`、锁定）阻止覆盖租户必须保留的项目（法规告知、审计横幅），因此用户层可以覆盖法规项目 | 在能力图或基线版条目上设置 `overridable: false`，并在 G0 拒绝 |
| M-13 | docs/05:310-314、docs/02:106 (2.5)、docs/02:194 (I2) | D1 的 G2（执行契约）是可选的。因此 I2 要求的契约虽然存在，却可能在一次都没执行的情况下被用作合并（I10）的依据。D2 的 G5 条件"包含外部命令时"也比 7.3 的"权限增加**无条件**需要人工批准"更窄 | D1 也将 G2 设为必需，或明确规定在 I10 判定之前先执行"从未执行过的契约"。将 5.8 的 G5 一栏全部统一为"权限增加时（I4）" |

### LOW

| # | 位置 | 证据 | 最小修改 |
| --- | --- | --- | --- |
| L-01 | docs/05:194-196 | 5.4 时序图中的消息共 **21 条**（:169-189）。正文引用了"第 9 步任务说明"（实际为 7）、"第 12 步 G1"（实际为 11）、"第 14~15 步评判"（实际为 12~13）、"第 17 步记录"（实际为 15）、"第 22 步激活"（不存在，实际为 21） | 把编号改为 7·11·12~13·15·21 |
| L-02 | tools/design_space.py:286-321、:9-14 | `--check P9` 以 KeyError 结束，错误的 JSON 以 traceback 结束，未知轴（`A12`）被悄悄接受。docstring 的用法中没有 `--bm` 和 `--bm-stats`，也没有 self-check | 在 `check()` 中加入 `extra=[k for k in c if k not in AXES]` 检查。在 `--check` 中用 `if a.check not in PROFILES and a.check!="all": ap.error(...)` 处理，`json.loads` 用 try/except 包裹后调用 `ap.error`。用 `--selftest` 对 1.1 的数值做 assert |
| L-03 | docs/references.md:22、:40、docs/01:17、docs/07:104、docs/09:132 | `docs/es/plugins/overview` 未被引用，而且是西班牙语版。2,857 因 403 未能确认（Unit 42 只确认了 341）。CaMeL 漏掉了基准测试（AgentDojo）。falcao 的摘要漏掉了 1 月 9 日的拦截，并泛化了"Agent SDK 额度" | 删除该条目，或改为 `/en/` 并在正文中引用。为 2,857 这一数值补上 Koi 原文链接。补上"在 AgentDojo 上"，并让 9.6 的句子与文章表述一致 |
| L-04 | docs/04:131-143 vs examples/policy.example.yaml:23-34 | 4.7 的摘录使用 `net.allowlist`（capability-map 中没有的权限），而示例文件使用 `net.slack.post`。`currency` 和 `retention_days` 也缺失 | 让摘录与示例文件保持一致 |
| L-05 | docs/08:196、docs/glossary.md:20、examples/lexicon.ko.yaml:33-37、README:142 | 8.9 对照表写的是"深度 D1~D4"，而术语表和术语包的 developer 是 D1~D5，并且没有 `depth_d5` 概念（D5 请求应当以"核心功能请求"的形式呈现给用户）。README 的标记列表中漏掉了 E、O、T、X 系列 | 新增 `depth_d5: { basic: 改变应用本身的请求 }`，并在 README:142 中补上 E1~E16、O1~O13、T0~T4、X1~X6 |
| L-06 | docs/09:103 | 把 B8、B9、B10、B18 归在一起写成"只在约一半情况下可行"，但 B8 是 26.3%，B10 是 11.0% | 改为"B9 和 B18 约一半，B8 约四分之一，B10 约十分之一" |
| L-07 | docs/05:271-272、docs/05:253 | `onFailure:"block"` 对 `Stop` 和 `SubagentStop` 无效（官方文档）。因此当钩子失败时，E11（未验证则拒绝结束）和 E12 会以放行方式运行（fail-open）。也缺少 v2.1.295 及以上这一要求 | 在对照表中加脚注，并写明 E11 和 E12 "在 MCP 工具一侧也强制执行" |

---

## 3. 判断（未经机器验证的意见）

- **贡献的分量**：设计空间（design space）数值是*在这样选择规则与取值分辨率时*的算术。让这些数值读起来像实证结果的句子（"大多数组合不合理"、"最常见的矛盾"、"结构与商业大体分离"）在程序委员会那里会成为拒稿理由。较稳妥的做法是，只把数值作为展示规则体系内部一致性的演示来主张。
- **最大的未解决风险不是 O1，而是 C-02。** 第 10 章把契约充分性当作"质量"问题处理。但只要由生成者编写契约，这就是一个*安全*问题。被注入的生成者会写出让自己通过的契约。
- **I8 与"可塑性"之间的张力**：把用户设备一侧的强制降为提示级别，这种坦诚是好的。但一边把 P1 和 P5 作为代表配置推出、一边承诺 Core 合规，会让读者误解。拆分等级（C-03 的修改）更为坦诚。
- **模式的范围**：模式只检查"形状"，而规范的核心保证（I4、I5、I7、I10）需要跨文档检查。可是没有说明由谁、在哪里做这些检查（接收检查、合规校验工具）。在 v0.2 之前，哪怕 `tools/` 中只有一个小型合规校验器（conformance validator），"在设计上保证"也会变成可证伪的主张。
- **B20（赞助默认值）** 在结构上损害智能体推荐的中立性。仅靠标示义务，无法阻止进入模型上下文的赞助信息使推荐发生倾斜。如果要加入，"赞助信息不放入智能体上下文，只在 UI 中显示"更安全。
- **以 D3 为中心的解读（03:262）** 在 H-01 解决之前无法成立。D3 中混有 sandboxed 和 native，因此"只开放到声明式界面"这一解读与数据不符。
- **做得好的地方**（为公平起见）：数值可复现、模式与示例均通过、配置·BM 矩阵基于代码生成、失效链接 0 个、24 个来源中 23 个可访问、"无来源的数值为建议值"的标注、7.8 的保证级别表、4.8 对客户端 PDP 局限的告知。作为 v0.1 草案，这是少见的可验证结构。

---

## 4. 复现命令

```bash
cd mallangable-ai   # 仓库根目录
python3 tools/design_space.py --markdown
python3 tools/design_space.py --check all
python3 tools/design_space.py --bm
python3 tools/design_space.py --bm-stats
# 辅助脚本（仓库之外）
python3 -I /tmp/mreview/indep.py     # 独立·唯一违反数，D3/D4 native 数
python3 -I /tmp/mreview/alt.py       # 禁止 D3/D4 native 的变体
python3 -I /tmp/mreview/more.py      # 各轴补全数差异，own⇒server·D3⇒decl 变体，术语包交叉检查
python3 -I /tmp/mreview/q.py         # 规则等价商 8,969，D5 分布
python3 -I /tmp/mreview/bmdiff.py    # BM 矩阵比对，配置 diff
/tmp/mreview/venv/bin/python -I /tmp/mreview/validate.py   # 示例对模式
/tmp/mreview/venv/bin/python -I /tmp/mreview/neg.py        # 反向测试
python3 -I /tmp/mreview/xref.py      # 章节·链接·id·URL 交叉引用
```
