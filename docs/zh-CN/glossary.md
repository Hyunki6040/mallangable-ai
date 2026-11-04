<!-- LANG-BAR -->
[English](../en/glossary.md) · [한국어](../ko/glossary.md) · **简体中文** · [日本語](../ja/glossary.md) · [Español](../es/glossary.md)
<!-- /LANG-BAR -->

# 术语表

这里同时列出了开发·设计文档用的术语，以及在普通用户界面中使用的表达（术语包 basic 级别）。用户界面用的完整词典见 [`examples/lexicon.zh-CN.yaml`](../../examples/lexicon.zh-CN.yaml)。

| 术语 | 英文 | 定义 | 用户界面表达 | 首次出现 |
| --- | --- | --- | --- | --- |
| 可塑软件 | malleable software | 用户能够以较小阻力按自己的需要改着用的软件 | — | 1.1 |
| Mallangable | Mallangable | 在扩展点内由 AI 生成变更，并用契约验证·记录·传播的软件 | — | 1.2 |
| 宿主 | host | 要变得可塑的目标应用。`H = ⟨C, X, K, Σ⟩` | 应用 | 2.2 |
| 核心 | core | 供应商发布的不可变部分 | — | 2.2 |
| 扩展点 | extension point | 宿主允许修改的位置 | 可以改的位置 | 2.2 |
| 能力 | capability | 扩展可以使用的能力的名牌 | 允许范围 | 2.2 |
| 能力图 | capability map | 扩展点·权限·schema 的机器可读清单 | — | 2.2 |
| 层 | layer | 一组变更。基线版·用户层等 | — | 2.3 |
| 有效应用 | effective app | 在核心之上合成各层的结果 | — | 2.3 |
| 变更 | change (δ) | 意图·产出物·契约·权限·深度·扩展点·来源的组合 | 改动 | 2.4 |
| 功能 | feature | 源自同一意图的一系列变更 | 我做的功能 | 2.4 |
| 意图 | intent (ι) | 对人所说目的的概括 | — | 2.4 |
| 契约 | contract (κ) | 针对有效应用可观察行为的验收条件 | 承诺清单 | 2.5 |
| 深度 | depth D1~D5 | 产出物的表达力，同时也是风险等级 | 改动程度 | 2.6 |
| 最小深度原则 | least-depth rule | 以满足契约的最低深度来生成 | — | 2.6 |
| 策略 | policy | 每个旋钮的允许区间 | 公司允许的范围 | 2.7 |
| 不变式 | invariant I1~I10 | 实现在设计上不得破坏的性质 | — | 2.9 |
| 设计轴 | design axis A1~A11 | 架构选择的维度 | — | 3.2 |
| 结构族 | structural family | 结构轴 A1~A8 的一种组合 | — | 3.4 |
| 参考配置 | reference profile P1~P7 | 设计空间中的代表点 | — | 3.5 |
| 旋钮 | knob | 可以管控的一个维度 | 设置 | 4.2 |
| 上限 · 下限 | ceiling · floor | 允许区间中风险一侧的端点 · 保障一侧的端点 | — | 4.2 |
| 用户权利底线 | floor rights F1~F7 | 任何策略都无法删除的用户权利 | — | 4.6 |
| PDP · PEP | policy decision/enforcement point | 判定策略的地方 · 执行策略的地方 | — | 4.8, 7.2 |
| 平面 | plane | 架构的 6 个职责区域 | — | 5.1 |
| 执行框架(harness) | harness | 包裹智能体、强制执行流程·工具·策略·预算·输出的确定性外壳 | — | 5.6 |
| 验证门 | gate G0~G5 | 激活前必须通过的检查阶段 | 确认 | 5.8 |
| 来源盲评 | source-blind judging | 让评判者不知道产出物的生成者·执行框架·模型路径的 G4 规则 | — | 5.8 |
| 热替换 | hot swap | 不重启核心，只替换扩展槽 | — | 5.9 |
| 安全模式 | safe mode | 关闭所有用户层后启动 | 以基本模式启动 | 5.9 |
| 拓扑 | topology | 变更历史的结构（snapshot·fork·lineage·crdt） | — | 6.2 |
| 谱系 | lineage | 多级基线版层次构成的分叉网络 | — | 6.3 |
| 基线版 | baseline | 作为下级层出发点的版本 | 基本版 | 6.3 |
| 漂移 | drift | 与最新上游发布之间的距离 | 落后于基本版 | 6.3 |
| 解决阶梯 | resolution ladder R0~R5 | 从便宜的开始依次尝试冲突解决方法的顺序 | — | 6.6 |
| 契约保持合并 | contract-preserving merge | 同时满足双方契约的合并 | 合并 | 6.7 |
| 意图冲突 | intent conflict | 无法同时满足双方契约的状态 | 需要选择的部分 | 6.7 |
| 解决缓存 | resolution cache | 在可见性范围内复用已验证的冲突解决方案 | — | 6.8 |
| 契约迁移 | contract migration | 仅在用户同意或扩展点废弃对应表下才允许的契约削弱·移动。用 `Contract-Migrated` 尾注记录 | — | 6.7 |
| 晋升 | promotion | 把在下级收敛的功能提升到上级基线版 | 采纳为正式功能 | 6.10 |
| 致命三要素 | lethal trifecta | 私密数据·不可信输入·对外通信的组合 | — | 7.3 |
| 可见性标签 | visibility label | 数据的范围与等级（V0~V3） | 管理员能看到的范围 | 7.5 |
| 完整性标签 | integrity label | 标签 λ 的第三个分量（trusted > untrusted）。决定权限增加·对外发送·扩展点选择的值必须是 trusted | — | 7.5 |
| 输出门 | output gate | 降低标签的唯一位置（降密器，declassifier） | — | 7.5 |
| 对象能力 | object capability | 只凭交给自己的权限对象行动的安全模型 | — | 7.6 |
| 时间等级 | time tier T0~T4 | 按响应时间段划分的体验模式 | — | 8.4 |
| 变更回执 | change receipt | 写明改了什么、如何回退的卡片 | 回执 | 8.6 |
| 术语包 | lexicon pack | 按概念 id 组织的级别·领域·语言表达词典 | — | 8.9 |
| 模型获取 | model sourcing | 推理用谁的账户·由谁付费 | AI 引擎连接方式 | 3.2 A9, 8.10 |
| 静默破损率 | silent breakage rate (SBR) | 通过了公开契约、却未通过隐藏检查的合并比例 | — | 10.2 |
| 未评分 | unscored | 评分本身失败的请求。不记为 0 分，从分母中剔除并单独报告件数 | — | 10.2 |
