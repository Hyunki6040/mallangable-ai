<!-- LANG-BAR -->
[English](../../en/research/harness2-analysis.md) · [한국어](../../ko/research/harness2-analysis.md) · **简体中文** · [日本語](../../ja/research/harness2-analysis.md) · [Español](../../es/research/harness2-analysis.md)
<!-- /LANG-BAR -->

# 调研笔记 — Harness² (google-research/harness2)

> 本笔记的结论：Harness² 是一个**针对每个任务改写执行框架（harness）本身的研究框架**。Mallangable 的执行框架（5.6）是包裹智能体并对其进行*强制*约束的外壳，因此方向不同。可以直接引入的有三点。第一，**确保评分信息绝不进入方法（method）一侧上下文的隔离机制**。第二，**把评分失败当作未评分（unscored）而不是 0 分的报告规则**。第三，**隐藏候选来源的评判**。这些都补强了 Mallang-Bench（10.2）和 G4（5.8）。反之，让智能体连策略钩子、护栏都一并修改的自我编辑，我们不予接受。

- 确认日期：2026-10-30
- 调研对象：https://github.com/google-research/harness2（公开仓库，已确认存在）
- 固定提交：`1cfe254e8d25b15f37048c3730134686abe60335`（2026-10-13）。下文所有源码链接均以此提交为准。
- 方法：用 `git clone --depth 1` 拉取到空的临时目录，**只做阅读**（未执行代码）。论文通过网络获取 arXiv 摘要页与 HTML 正文进行阅读。
- 记法：`B` = `https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335`

## 0. 已确认与未完成的事项

| 项目 | 状态 | 依据 |
| --- | --- | --- |
| 仓库是否存在、是否公开 | 已确认 | `gh repo view google-research/harness2`，克隆成功 |
| 许可证 | 已确认 | [`LICENSE`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/LICENSE) Apache 2.0，[`pyproject.toml`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/pyproject.toml#L9) `license = "Apache-2.0"` |
| 核心源码（`harness2/core/*`、`substrate/*`） | 直接阅读 | 见正文链接 |
| 论文 | 已确认存在及摘要，正文部分确认 | [arXiv:2610.14224](https://arxiv.org/abs/2610.14224)，2026-10-09 提交。正文是用摘要工具读取 HTML 的，因此**章节编号与引文需要再与原文 PDF 核对** |
| 项目网站 | 已确认存在 | https://harness2.github.io（README 中有链接） |
| Google Research 博客文章 | **未找到** | 网站、README、论文中均无博客链接 |
| 复现实验数据 | 未进行 | 需要模型调用费用，且超出调研范围 |
| `prompts.py`（1,163 行）全文 | 只读了部分 | 只确认了隔离指令和 INV/DOM 部分 |
| 基准适配器（`benchmarks/*.py`） | 未阅读 | 与方法论无关的连接代码 |

## 1. Harness² 是什么

### 1.1 目的

README 把执行框架定义为"让模型作为智能体行动的周边系统（提示词、工具、记忆、技能、编排等）"，把 *harnessing* 定义为优化该系统的过程（[README L19-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L19-L21)）。Harness² 在**模型权重固定不变**的前提下，通过两级递归来改进执行框架（[README L23-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L23-L33)）。

- **任务级递归**：通过对比式的 **Propose–Probe–Compose** 步骤打磨当前任务的执行框架。不使用正确答案反馈，只以多次运行之间的行为对比作为依据。
- **harnessing 级递归**：把每个任务中采纳的执行框架和附有证据的经验教训累积到持久的*改进执行框架*（库）中，供后续任务使用。

论文摘要列出了两点动机。开放世界中的任务是设计时未曾见过的，因此**没有正确答案验证器**；而现有的递归式自我改进是任务特化的，无法泛化（[arXiv 摘要](https://arxiv.org/abs/2610.14224)）。

### 1.2 结构与核心抽象

| 抽象 | 定义 | 出处 |
| --- | --- | --- |
| 三轴分离 | 方法（递归、提示词、选择、库）、基底（substrate：智能体框架）、基准（`BenchSpec` 值 + 适配器）互不混杂 | [`core/spec.py` L15-20](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L15-L20) |
| 8 个可编辑组件 c1..c8 | 系统提示词、护栏、记忆、工具说明、子智能体、技能、脚本、插件 | [README L68-73](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L68-L73) |
| `SurfaceSpec` | 各框架的编辑表面（路径、常驻注入文件、长度上限、钩子文件、允许的钩子事件） | [`core/tree.py` L40-60](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L40-L60) |
| 常驻注入（always-on）上限 | OpenCode 24,000 字符，Codex 8,000 字符。注明的理由是 Codex 每轮都注入 `AGENTS.md`，并在 32,768 字节处静默截断 | [`substrate/opencode.py` L42-51](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L42-L51)，[`substrate/codex.py` L39-47](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L39-L47) |
| 编辑约定 | "省略即继承"：提案只给出要修改的文件 | [`core/tree.py` L15-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L15-L21) |
| 拒绝路径逃逸 | 拒绝绝对路径和含 `..` 的路径 | [`core/tree.py` L82-89](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L82-L89) |
| `BenchmarkAdapter` | 基准需要填写的全部内容：`tasks`、`task_prompt`（去掉评分标准）、`execute`、`trajectory`、`validate_tree`、`score` 等 | [`core/spec.py` L200-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L200-L250) |
| `Substrate` | `surface`、`materialise`、`execute`、`read_trajectory`、`preflight` | [`substrate/base.py` L47-80](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L47-L80) |
| 角色 | 执行者（executor）、执行框架编辑者（INV、DOM 两个维度）、组合者（composer）、选择者（selector）、经验反思者（experience reflector）。评分者（judge）在方法之外 | [README L37](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L37) 图示说明，[`core/recursion.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py)，[`core/selection.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py)，[`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19) |

### 1.3 Propose–Probe–Compose

1. **Propose**：编辑者提出两个维度的候选。INV 是"智能体的工作方式"（工具、流程），DOM 是"该领域从业者所知道的东西"（[`core/prompts.py` L347-373](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L347-L373)）。论文 §2.2.1 将其解释为与领域无关的缺陷和领域特有的缺陷。
2. **Probe**：将每个候选**在同一任务上**运行，并与基准运行比较轨迹和产出物（论文 §2.2.1）。
3. **Compose**：合并有证据支撑的变更，修正相互冲突的编辑，采纳某一个候选或保留当前执行框架（论文 §2.2.1）。组合指令把合并 INV 编辑与 DOM 编辑作为期望结果（[`core/prompts.py` L934](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L934)）。

扩展方式有两种（[`core/recursion.py` L343-566](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L343-L566)）。

- **并行（`agg`）**：基于同一份基准证据生成 INV k 个 + DOM k 个候选并运行，然后产生 k 个彼此独立的组合。
- **顺序（`seq`）**：串联 k 次 Propose–Probe–Compose，把打磨后的执行框架和累积证据传递给下一步。

无效的提案会**重试一次**，仍不成功则原样继承当前执行框架（[`core/recursion.py` L15-19, L36](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L36)，[L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L242-L251)）。重试时会把验证错误的原文直接反馈回去。适配器约定也要求"错误消息会原样作为重试反馈，所以要写成可执行的句子"（[`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245)）。

### 1.4 事件与轨迹模型

Harness² **没有** Mallangable 5.6 那样的**生命周期事件模型**。取而代之的是两样东西。

- **通用轨迹语法**：把各基底不同的记录格式渲染为 `[ACTION]` / `[OBSERVATION]` / `[ERROR]` 行（[`core/spec.py` L230-231](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L230-L231)，[`substrate/codex.py` L386-389](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L386-L389)，[`substrate/opencode.py` L384-388](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L384-L388)）。整个轨迹以文件形式提供，只对单条观测按长度上限（默认 50,000 字符，不得低于 10,000 字符）截断（[`core/spec.py` L163-167](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L163-L167)，[`core/context.py` L15-27](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L15-L27)）。
- **证据放文件，提示词放指针**：编辑者从磁盘读取 `context/` 下的任务、轨迹、产出物、执行框架、库和候选，并且必须引用作为每项编辑依据的轨迹位置（[`core/context.py` L521-544](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L521-L544)）。
- **钩子是编辑对象**：在 Codex 基底上，`.codex/hooks.json` 属于编辑表面。允许的事件为 `PreToolUse`、`PostToolUse`、`PermissionRequest`、`PreCompact`、`PostCompact`、`SessionStart`、`SubagentStart`、`SubagentStop`、`UserPromptSubmit`、`Stop`（[`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72)）。检查器只接受 `command` 格式。代码中注明：格式错误的钩子不会报错，而是**根本不会执行**，因此在提案者可见的时点强制检查格式（[`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251)）。

### 1.5 评估方法论

| 机制 | 内容 | 出处 |
| --- | --- | --- |
| 无分数的运行视图 | 方法所知的运行信息 `RunView` "绝不携带分数" | [`core/spec.py` L176-187](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L187) |
| 只在选择之后评分 | `score()` 只由 `core.judge` 调用，且只在选择确定后调用。方法一侧任何模块都不 import `judge` | [`core/spec.py` L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L247-L250)，[`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19)，[BENCHMARKS L34](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L34) |
| 评分失败 ≠ 0 分 | 失败记为 `None`，从分母中剔除，不以 0 分缓存。未评分单独报告 | [`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18)，[EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118)，[BENCHMARKS L67-68](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L67-L68) |
| 阻断答案路径 | 基准声明的 `leak_globs` 一旦进入上下文即抛出异常 | [`core/context.py` L399-416](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L416) |
| 评分痕迹绊线 | 若评分器输出的标记字符串出现在上下文文件名、正文或智能体写的执行框架中，则拒绝。"这是绊线，不是防御本身。触发时不要扩大标记列表，而要找出泄漏的读取路径" | [`core/context.py` L419-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L419-L518) |
| 禁用测量类词语 | 智能体可见的基准文案中若含 benchmark、evaluation、grader、rubric、score 则拒绝："描述工作，不要描述测量" | [`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126) |
| 明确的无评分指示 | 编辑者、选择者提示词中写明"上下文中没有评分标准、答案和分数。不要猜测评分者想要什么" | [`core/prompts.py` L41-53](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L41-L53)，论文附录 H |
| 匿名选择 | 为候选标上 A、B、…，并以 `task_id\|k\|mode` 为种子打乱（重跑结果相同）。选择池只有最终的 k 个候选，不放入基准运行 | [`core/selection.py` L71-76](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L76)，[L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L93-L111) |
| 选择者失败时的替代 | 选择者失败时选取中性替代（传入的基准运行，没有则取第一个最终候选），并记为 `fallback` | [`core/selection.py` L237-252](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L237-L252) |
| 预算恒等式 | 每个任务的运行次数 R = 4k（基准 k + 候选 2k + 最终 k），改进会话 P = 3k。标签重复视为覆盖，在数值检查之前先判为失败 | [`core/ledger.py` L15-33, L89-113](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L113) |
| 运行同一性 | 在完成标记中加入执行框架树的指纹，不复用来自其他配置的运行 | [`core/runmark.py` L15-20, L41-61, L91-102](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L102) |
| 候选多样性 | 用候选执行框架之间按行计算的 Jaccard 衡量它们是否收敛为同一个 | [`core/tree.py` L407-427](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L407-L427) |
| 网络访问警告 | 由于是公开基准，评分标准在网上可以找到。在验证运行中，Codex 运行**在没有指示的情况下下载了自己任务的评分标准**。建议在运行主机上进行网络层面的阻断，并把所用限制与结果一同报告 | [EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109)，[README L166-171](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L166-L171) |
| 库的范围 | 按运行、模式、领域分开，每次运行所有领域都从空状态开始。在同一领域内只读取之前的任务 | [`core/library.py` L15-24](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L15-L24)，[EXPERIMENTS L16-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L16-L19) |
| 经验条目 | `cue`、`lesson`、`evidence` 必须齐全才会保存（`confidence` 可选）。缺少则不放入库 | [`core/library.py` L43-47, L106-123](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L43-L123)，[`core/selection.py` L494-501](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L494-L501) |

基准有 JobBench、LAB、WorkBuddy-Bench 三个（[README L129-133](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L129-L133)）。README 和摘要给出的结果是：在 GLM-5 和 Gemini 3.5 Flash 上，单步即可使 WorkBuddy-Bench 最多提升 11.5 分、JobBench 提升 4.5 分、LAB 部分通过率提升 11.8 个百分点（[README L41-45](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L41-L45)）。论文附录 F 的局限有两点：递归预算增加会使推理成本上升；由于没有正确答案监督，判断容易受运行波动和模型共有偏差的影响。这些数值我们没有亲自复现。

### 1.6 许可证

- 主体：Apache 2.0（[README L199-204](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L199-L204)）。与本仓库打算用于模式和工具的 Apache-2.0（README「许可证」）不冲突。
- `third_party/`、基准和数据集遵循各自上游的许可证。WorkBuddy-Bench 是**带有地区限制的 Tencent 自有许可证**（[BENCHMARKS L80-83](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L80-L83)）。
- 本笔记只使用简短引文和链接，未搬运代码。下文的建议文字也是用我们自己的话重写的概念，只保留出处标注。

## 2. 对应表 — Harness² 概念 → Mallangable

判定：**采纳**（几乎原样）、**变形**（只取其要旨）、**拒绝**。

| # | Harness² 概念 | Mallangable 位置 | 判定 | 理由 |
| --- | --- | --- | --- | --- |
| M1 | 执行框架 = 可编辑的 c1..c8 树 | 5.6 定义（确定性外壳） | **拒绝**（定义层面） | 我们的执行框架是*强制*执行策略（policy）的一方。让智能体修改护栏、钩子的结构违背 I8（权威执行只在控制平面）和 7.11"策略文件不可变"。只在离线状态下打磨流程（技能、提示词）是可以的 |
| M2 | 钩子格式错误时静默不执行，写入时点检查格式 | 5.6「注意」，7.2 设备执行框架钩子 | **采纳** | 暴露了又一条钩子失败时保持放开（fail-open）的路径。补强既有原则：设备钩子配置在写入时点进行模式检查，服务器的接收检查（receive-check）是最终权威 |
| M3 | Codex 钩子事件列表 | 5.6「映射示例」 | **变形** | 是 Claude Code 之外第二张对应表的候选。但出处是 Harness² 的检查器而非 Codex 官方文档，因此标注"需确认" |
| M4 | `RunView` 中无分数，评分在选择之后，评分痕迹绊线，`leak_globs` | 10.2 隐藏检查，I7 | **采纳** | Mallang-Bench 的 SBR 只有在隐藏检查真正隐藏时才有意义。隐藏检查一旦泄漏到生成、评判上下文，SBR 就会被乐观地扭曲 |
| M5 | 评分失败记为 `None`，剔除出分母，单独报告 | 10.2「报告格式」 | **采纳** | 把失败计为 0 会拉低 CSR，剔除后隐瞒则会抬高 CSR。两者都不诚实 |
| M6 | 通过网络访问泄漏评分标准，报告网络限制 | 10.2 构成与报告，7.3 外部通信允许列表 | **采纳** | 攻击集、提取集、隐藏检查一旦公开，就会出现同样的问题。把 7.3 的允许列表规则也作为基准运行条件来要求 |
| M7 | 禁用测量类词语（描述工作） | 10.2 请求集 | **采纳** | 请求集的句子里如果有"检查""评分"之类的词，智能体可能会去瞄准测量本身 |
| M8 | 匿名、种子打乱的选择，排除基准运行 | 5.8 G4 评判，5.7 评判者 | **变形** | 让评判者不知道候选来自哪个生成者、执行框架、模型路径。这是在 I7（不同实例）之上再加"来源盲评（source-blind judging）" |
| M9 | 预算恒等式 R=4k、P=3k，标签重复检查 | 10.2 CPC，5.6 预算 | **变形** | 要让成本比较公平，必须同时报告"运行了几次、评判了几次"。精确的恒等式只适用于 Harness² 的方法，因此只引入*报告项* |
| M10 | 用执行框架指纹判别运行同一性 | `change-record.schema.json` `provenance` | **采纳** | 目前 `agent` 只是"角色@执行框架"字符串，执行框架的*配置*变了记录也一样。加上内容哈希就能做到复现、审计和基准比较 |
| M11 | 无效提案重试 1 次后保持当前状态 | 5.8 G1「失败时」，5.6 预算 | **采纳** | G1 只有"把原因返回给智能体"，没有上限和终止状态。考虑到成本攻击者（7.1），需要上限和"无变更"终止 |
| M12 | 按领域划分的经验库（cue、lesson、evidence） | 5.3 `ResolutionCache`，第 6 章解决缓存，7.5 范围分离 | **变形** | 范围分离在 7.5 中已有。要引入的是"缺少证据字段的教训不保存"这一保存条件，以及说明基准中缓存是否从空状态开始的报告项 |
| M13 | Propose–Probe–Compose（无正确答案的对比式改进） | 10.1 O1·O4，5.7 合并者、晋升者 | **变形（可选）** | 一个交互式变更要运行 4k 次，不符合时间等级（8.4）和成本。只作为服务器作业（合并、晋升）或 O4 评判者可信度研究的起点保留 |
| M14 | `[ACTION]/[OBSERVATION]/[ERROR]` 轨迹语法 | 5.11 遥测，G4 证据 | **暂缓** | 用 E4、E5 事件可以生成同样的信息。确定评判者输入格式时再看 |
| M15 | 候选多样性（Jaccard） | — | **拒绝** | 我们的规范中没有生成多个候选的步骤（YAGNI） |
| M16 | 常驻注入长度上限及其理由 | 5.10 上下文供给 | **暂缓** | 是确定各角色上下文预算时可参考的数值。目前写入规范的依据较弱 |

## 3. 建议编辑列表（按优先级，最多 10 项）

每项都是最小编辑。文字不是照搬 Harness² 的句子，而是对概念的重写。

### E-1. 在 10.2 Mallang-Bench 中加入隐藏检查隔离规则 (M4)

- 文件：`docs/10-open-problems.md`，「### 构成」表格正下方
- 依据：[`core/spec.py` L176-187, L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L250)，[`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19)，[`core/context.py` L399-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L518)
- 建议文字：

```markdown
隐藏检查隔离（必须(MUST)）：
- 隐藏检查及其结果不进入解释者、生成者、评判者的上下文。评分在激活完成之后由独立进程进行。
- 运行器每次构建生成、评判上下文时，都查找隐藏检查的文件路径和检查结果标记字符串，一旦发现即停止运行。这项检查只是报警装置，不是防御。触发时不要扩大标记列表，而要修复泄漏的读取路径。
（出处：Harness² 的无分数运行视图与评分痕迹绊线，google-research/harness2 `core/spec.py`、`core/context.py`）
```

### E-2. 在 10.2「报告格式」中加入未评分规则 (M5)

- 文件：`docs/10-open-problems.md`，「### 报告格式」段落末尾
- 依据：[`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18)，[EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118)
- 建议文字：

```markdown
评分失败的请求（隐藏检查运行错误、评判模型错误）不是 0 分，而是**未评分**。将其从指标的分母中剔除，并把未评分件数与指标并列报告。例："CSR 0.71 (n=192, 未评分 8)"。
```

### E-3. 在 10.2「报告格式」中加入运行环境报告项 (M6, M9, M12)

- 文件：`docs/10-open-problems.md`，E-2 段落之后
- 依据：[EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109)，[`core/ledger.py` L15-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L33)，[`core/library.py` L21-23](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L21-L23)
- 建议文字：

```markdown
需一并报告的运行条件：
- **网络限制**：生成智能体可以访问的主机列表。托管隐藏检查、攻击集、提取集的地址在运行期间予以阻断。在公开基准中，已有智能体在没有指示的情况下下载评分标准的案例报告（Harness² 实验指南）。
- **调用次数**：每个成功变更对应的生成运行次数和评判会话次数（含重试）。仅凭 CPC 无法在不同执行框架之间公平比较。
- **缓存状态**：解决缓存、已学到的教训是否从空状态开始，是否允许使用前面请求的结果。
```

### E-4. 在 5.8 G4 中加入来源盲评 (M8)

- 文件：`docs/05-reference-architecture.md`，5.8 门表中 `G4 评判` 行的"内容"栏
- 依据：[`core/selection.py` L71-76, L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L111)，论文 §2.2.2
- 现在：`评判者根据截图和意图判定是否满足语义`
- 建议：`评判者根据截图和意图判定是否满足语义。评判者不知道产出物来自哪个生成者、执行框架、模型路径（来源盲评）。候选有多个时，以用可复现种子打乱后的匿名 id 呈现`

### E-5. 在 5.8 G1 失败时明确重试上限 (M11)

- 文件：`docs/05-reference-architecture.md`，5.8 门表中 `G1 静态检查` 行的"失败时"栏
- 依据：[`core/recursion.py` L15-19, L36, L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L251)，[`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245)
- 现在：`把原因返回给智能体`
- 建议：`把原因以可修正的句子返回给智能体。超过重试上限（建议值：1 次）则不做变更，保持当前状态并终止`

### E-6. 在 5.6「注意」中加入钩子失败时放开的警告 (M2)

- 文件：`docs/05-reference-architecture.md`，5.6 最后的「注意：」段落之后
- 依据：[`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251)
- 建议文字：

```markdown
格式错误的钩子配置在许多运行时中不会报错，而是**根本不会执行。** 也就是说，失败时保持放开。执行框架插件在写入钩子配置的时点，按运行时接受的事件名和处理器格式进行检查，并在会话开始（E1）时确认钩子是否真正注册。智能体不能修改策略钩子和护栏文件（工具边界，E4）。
（参考：Harness² 出于同样的理由，在写入时点检查 Codex 钩子文件。google-research/harness2 `core/tree.py`）
```

### E-7. 在 `change-record.schema.json` 中加入执行框架指纹字段 (M10)

- 文件：`schemas/change-record.schema.json`，`properties.provenance.properties` 中 `prompt_hash` 之后
- 依据：[`core/runmark.py` L15-20, L41-61](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L61)，[`substrate/base.py` L26-32](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L26-L32)
- 建议字段（不改动 `required`，为可选字段）：

```json
"harness_digest": {
  "type": "string",
  "pattern": "^sha256:[0-9a-f]{64}$",
  "description": "产生该变更的执行框架配置（技能、钩子、策略副本、工具列表）的内容哈希。即使 agent 字符串相同，配置不同则值也不同"
}
```

- 备注：Harness² 使用 SHA-1 的前 16 个字符。这里为与既有 `prompt_hash` 格式保持一致，建议使用完整的 SHA-256。若采纳，需要重新运行 `examples/change.example.yaml` 的验证（因是可选字段，既有示例应照常通过）。

### E-8. 在 10.2 请求集中加入禁用测量类词语 (M7)

- 文件：`docs/10-open-problems.md`，「### 构成」表格 `请求集` 行"内容"栏末尾
- 依据：[`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126)
- 追加文字：`。请求句子只说要做的事，不说测量（禁止"检查""评分""分数"等）`

### E-9. 在 5.6 对应表中加入 Codex 列候选 (M3)

- 文件：`docs/05-reference-architecture.md`，「### 映射示例：Claude Code 钩子」表格之后的一段短文
- 依据：[`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72)（不是 Codex 官方文档，而是二手出处）
- 建议文字：

```markdown
Codex CLI 也可以用同样的方式对应（E1 `SessionStart`、E2 `UserPromptSubmit`、E4 `PreToolUse`、E5 `PostToolUse`、E6 `PermissionRequest`、E11 `Stop`、E12 `SubagentStop`、E15 `PreCompact`）。该列表取自 Harness² 所检查的事件集合，因此在采纳前必须与 Codex 官方文档核对。
```

### E-10. 在参考文献中加入 Harness²

- 文件：`docs/references.md`，在「## 智能体安全」之前新增一节
- 建议文字：

```markdown
## 执行框架改进与评估

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · 代码(Apache-2.0): https://github.com/google-research/harness2
  - 隐藏检查隔离、未评分报告、来源盲评评判、执行框架指纹（5.6、5.8、10.2）的依据。调研笔记：[research/harness2-analysis.md](harness2-analysis.md)
```

## 4. 未纳入的内容

- **自我编辑的执行框架（M1）**：如果修改用户应用的智能体连自己的策略钩子也一并修改，5.6 定义执行框架的理由（"包裹非确定性智能体的确定性外壳"）就不复存在了。
- **把 Propose–Probe–Compose 放进默认生成流程（5.4）**：一个变更需要运行 4k 次，无法满足 T0~T2 时间等级。可用之处是服务器作业中的实验性选项和 O4 研究。
- **引用基准数值**：我们没有亲自复现，而且任务分布与我们的问题（修改应用）不同。
