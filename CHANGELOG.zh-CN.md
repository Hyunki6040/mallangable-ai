<!-- LANG-BAR -->
[English](CHANGELOG.md) · [한국어](CHANGELOG.ko.md) · **简体中文** · [日本語](CHANGELOG.ja.md) · [Español](CHANGELOG.es.md)
<!-- /LANG-BAR -->

# 变更记录

## v0.2.4 — 2026-11-05

多语言版本。规范内容·设计空间数值·schema 契约均未改变。

* 将默认 README 改为英语，并拆分出各语言版本：English（`README.md`）· 韩语（`README.ko.md`，原文）· 简体中文（`README.zh-CN.md`）· 日本語（`README.ja.md`）· Español（`README.es.md`）。CHANGELOG·CONTRIBUTING 也采用同样方式。

* 将规范正文和调研笔记移到 `docs/<语言>/`，并用五种语言撰写（`docs/en`、`docs/ko`、`docs/zh-CN`、`docs/ja`、`docs/es`）。韩语版为原文，译文与之不一致时以原文为准。

* 将 schema 说明、示例文档、工具消息·帮助改为英语。术语包示例按语言分别放置（`examples/lexicon.{en,ko,zh-CN,ja,es}.yaml`）。`check_schemas.py` 会全部验证。

## v0.2.3 — 2026-11-05

用 Cloudflare security-audit 技能对整个仓库做了对抗性安全审查（quick 配置，`docs/zh-CN/research/security-audit-2026-11-05.md`）。设计空间数值未改变。

### 管控·参考架构（第 4·5 章）

* 把 PDP `decide()` 的底线行为例外收窄为 `floor_scoped(req)`。只有在人类所有者 · 自己的层 · 先前状态 · 权限·深度不增加时才属于底线，其他回退（智能体调用的、重做、"重新开启"、解除搁置）都要经过与激活相同的判定。还加入了破坏性功能分支（G5）（4.8、5.5）。

### 版本·信任（第 6·7 章）

* 基线版传播的自动应用要经过 `activate()`（E10），需要批准时降级为提案。`delta_permissions` 不再采信自我申报，而是重新计算（6.5）。

* 在安全检查清单中增加了底线例外范围、传播自动应用、权限变化重新计算、egress 声明、工具输出转义等项目（7.11）。

### schema 契约

* `change-record`：确定性契约中至少有一项必须是可执行形式。只有叙述形式的记录会被拒绝。

* `extension-manifest`·`policy`：`network.allow`·`allowlist` 拒绝 IP 字面量。公共后缀通配符、egress 权限的存在、`setKnob` default ⊆ ceiling 被明确为合规校验器（conformance validator）的 MUST，并新增了回归用例（期望 `False`）。

### 工具·CI

* `check_schemas.py`：转义输出中的控制字符，拒绝 YAML 别名·超过 1 MiB 的文件，按文档隔离异常。

* `design_space.py`：`--profile`·`--check` 在 `normative`·`logical`·输入错误时退出码为 1，拒绝重复键·非对象 JSON。

* 将 CI 令牌限制为 `contents: read`。

## v0.2.2 — 2026-11-04

为开源发布做准备。规范正文·设计空间数值·schema 均未改变。

* 确定许可证：文档 CC BY 4.0（`LICENSE-docs`），schema·示例·工具 Apache-2.0（`LICENSE`）。

* 添加了 `CITATION.cff`、`CONTRIBUTING.md`、`requirements.txt`。

* 工具可以接收其他项目的文件。`design_space.py --profile FILE.json`、`check_schemas.py <schema> FILE...`。

* 在 README 中添加了"应用到我的项目"（词汇 → 设计空间 → 扩展计算器 → 数据契约 → 架构 → 合规声明 6 个步骤）和引用格式。

* 以 GitHub 公开仓库发布（https://github.com/Hyunki6040/mallangable-ai）。把 README 开头按问题意识（三种缺失）→ 6 个核心思想 → 工作方式 → 变更示例的顺序重写，并添加了在每次 push·PR 时运行 schema 回归检查和 P1~P7 检查的 CI。

## v0.2.1 — 2026-11-03

调研并吸收了 ThinkRail（JetBrains/thinkrail，Apache-2.0）的规范文档（`docs/zh-CN/research/thinkrail-analysis.md`）。设计空间数值和 schema 未改变。

### 管控·参考架构（第 4·5 章）

* 为批准设置范围（仅此一次 · 本次任务期间 · 始终），"始终"绑定到功能 content\_hash 和权限列表。不是肯定的答复即视为拒绝（4.8）。

* 回退以用户看到的状态 id 为依据。状态不同时什么也不改，重做是同一种操作（5.5）。

* 添加了评判输出处理规则。格式错误即失败，记录由执行框架重新生成，没有指出问题的失败会被拒绝，存在未关闭的指出项时不确认通过，重试上限由所有入口共享（5.8）。

* 完成信号只有 E11 一个，等待批准是电平信号。对应表的每一项都写明已确认的行为·重新确认条件·移除条件（5.6）。

* 监视者的隔离单位是整个功能（5.9）。

### 版本·信任·体验（第 6\~8 章）

* 并发生成任务各自持有工作副本，只记录改动过的路径（6.4）。

* 合并输入读取失败不视为缺失（`null`，即删除）（6.5）。

* 接受共享只针对那一时刻的内容，接收到的功能不能抢占我的命令·快捷键名称（6.9）。

* 列表·预览·权限显示不执行扩展代码（7.11）。

* 术语包：存储数据中只放 `概念 id + 参数`，共享功能不能更改术语包，并规定了字符串级替换的顺序（8.9）。

## v0.2 — 2026-10-30

吸收了三项调研（`docs/zh-CN/research/`）：Harness² 分析、先行案例调研（MCP·AG-UI·OTel·Cedar·RFC 7396 等）、对抗性评估。

### 设计空间（第 3 章，`tools/design_space.py`）— 数值有变化

* 把 2.6 的深度定义作为规则强制执行。L3 为 `A1∈{D1,D2,D3} ⇒ decl`，L4 为 `D4 ⇒ sandboxed`。

* 新增 N6：D5 不共享，且不能使用 snapshot 拓扑（I1）。

* 推荐组合 70,516 个 → **36,772 个**，结构族 1,618 个 → **863 个**，业务选项 58% → **57%**。BM 耦合矩阵 7×20 未改变。

* 将 P1·P6 改为 D4，将 P2·P5·P7 改为声明式 D3。七个配置仍全部为 clean。

* 在规则统计中添加了与顺序无关的独立违规数和唯一违规数。撤回了"L1 过滤得最多"的说法。

* 拒绝错误输入。对象包括不存在的配置、JSON 错误、未知的轴。

### 核心模型·管控（第 2·4 章）

* 把层合成 `⊕` 定义为 RFC 7396 JSON Merge Patch，并明确了它与 3-way 合并的关系。

* 从搁置 → 激活时要重新验证。

* 将 I8 移为 Governed 等级的要求。没有服务器的 P1·P5 最多只能获得 Core 等级。

* 添加了 Cedar 策略引擎适配器，并用 SymCC 证明 I5。用户权利底线（F1\~F7）先于引擎评估。

### 参考架构（第 5 章）

* 在 `own` 可见性下，只向生成者提供上级层的类型和能力图（I6）。

* 激活要经过 PDP 和 G5。批准前的 D4 代码只以零权限挂载。

* G4：采用来源盲评，并以基于种子的匿名 id 呈现候选。

* G1：失败时返回可修正的原因，重试后保持当前状态。

* 添加了执行框架事件对应表。AG-UI、A2A、MCP `input_required` 已加入对应表，Codex 需要确认官方文档。

* 警告了钩子配置错误时会进入默认允许状态的问题。明确 `Stop`/`SubagentStop` 钩子不是阻断型的门。

* 把观测字段改为 OTel GenAI 名称，并添加了 `policy.decision_id` 和 `traceparent`。

### 版本·信任·体验·业务（第 6\~9 章）

* 重写了传播算法。

  * 使用整条路径上契约的并集。

  * 等待批准中的父级不会阻塞子级。

  * 金丝雀是基于种子的随机样本。

* 只有在有人明确同意时才允许削弱契约，并记录为 `Contract-Migrated`。

* 为信息流标签增加了完整性轴（FIDES）。

* 新增了 3 个威胁：契约·评判污染、解决缓存污染、上游发布·运营方被攻破。

* 将发布者签名定为 in-toto/SLSA 格式。

* 秘密值只通过 MCP URL 模式 elicitation 接收。不在 MCP Sampling 之上构建 ModelPort。

* 客户产出物须经选择加入和许可同意才能进入官方基线版（B10·B19）。

### Mallang-Bench（第 10 章）

* 隔离隐藏检查，并设置泄漏检测装置（绊线）。

* 评判失败的项目报告为未评分，并从分母中剔除。

* 一并报告执行条件：网络限制、调用次数、缓存状态。

* SBR 分母包含人工批准的合并。

### schema（`schemas/`，新建 `tools/check_schemas.py`）

* 把契约项定义为可执行形式（`tree-query`·`unit`·`snapshot`·`judge`）。至少要有 1 个确定性项，`judge` 必须是非确定性的。自由叙述形式只为向下兼容而保留。

* 规定了各深度的必需门。权限增加时必须有 G5 和 `approved_by`。

* 拒绝只有空白的意图文本以及错误的 id·日期。

* 新增字段：

  * `provenance.harness_digest`

  * `extensionPoint.merge`

  * `catalog_id`

  * `destructive`

* 策略旋钮必须满足下限 ≤ 默认值 ≤ 上限。

* manifest 中 D1\~D3 的产出物只允许声明式。

* 规范所禁止的 17 种文档中，schema 拒绝其中 15 种。其余 2 种需要在文档之间比较，因此明确规定验证器必须(MUST)检查。

### 参考文献

* 将二手来源替换为一手来源：Agent Skills 规范、英文版 plugins 文档、A2UI v0.9.1、Mergiraf（GPL-3.0-only）。

* 新增章节：策略引擎、观测、供应链、执行框架改进与评估。
