<!-- LANG-BAR -->
[English](../../en/research/security-audit-2026-11-05.md) · [한국어](../../ko/research/security-audit-2026-11-05.md) · **简体中文** · [日本語](../../ja/research/security-audit-2026-11-05.md) · [Español](../../es/research/security-audit-2026-11-05.md)
<!-- /LANG-BAR -->

# 安全审计报告 — 2026-11-05

工具:[cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill)(`.claude/skills/security-audit/`,固定于 `UPSTREAM` 提交)

## 1. 执行范围

- 配置:**quick**,属于部分审计。只做了 1 次狩猎和 1 次最终覆盖率评审,评审发现的 6 个单元留作 `deferred`(`quick_profile_final_critic`)。不主张完整覆盖。
- 对象:整个仓库,以源码 `a69ddbf` 为准。这是首次审计,没有以往结果。
- 预算:没有另行规定。智能体共 11 个:侦察 1、狩猎 5、验证 4、评审 1。其中一个验证(`v-propagate`)因结果格式错误被丢弃,由新的验证者重做。
- 执行边界:目标代码只在 Docker 内运行。条件为 `--network none`、目标只读、uid 65534、`cap-drop ALL`、256 MiB、60 秒、`env -i`,写入只允许各智能体自己的 scratch。产物只通过父侧的 no-follow 提升器移出。未触及部署环境或外部服务。

## 2. 摘要

这是规格仓库,没有运行中的服务器。实际边界有两处:(a) 接收外部文档的检查工具;(b) 实现者会原样照搬的规范性伪代码。已确认的 2 个缺陷都是 low。另有 1 个缺陷被判定为需要进一步验证,其依赖事项已在本次修订中以规格语句闭合。

## 3. 已确认的缺陷

| 严重度 | 标题 | 边界 | 观测结果 |
| --- | --- | --- | --- |
| low | `decide()` 的底线行为例外不看主体·方向 | 智能体·其他层的主体 → PDP 激活状态转移 | 对同一状态 S1,`activate` 被拒绝(深度),`revert(target=S1)` 被允许[记录] |
| low | `check_schemas.py` 原样输出文档键·文件名中的控制字符 | 外部文档作者 → 检查者终端·CI 日志 | 生成 2 个原始 ESC 字节、独立的 `::error title=forged::` 行。退出码保持为 1 |

### 3.1 底线行为例外的范围(`docs/04-control-spectrum.md:153`)

- 低信任主体:被委托的智能体(可被提示注入)、监视者、其他层的用户。
- 复现:原样照搬 4.8 的伪代码。策略为深度上限 D3、权限 `[tasks.read]`、`gated`,已记录的状态 S1 在 D4 拥有 `net.slack.post`。结果是 `activate(S1)` 为 `('deny','depth')`,`revert(target=S1)` 无论主体为何都是 `('allow',['log'])`。
- 条件:当宿主原样实现 4.8,且 `revert` 接受任意 StateId 并也用作重做时(5.5)成立。运行时代理人的逐次调用 PDP 检查能否阻止实际的权限使用取决于实现,因此不做主张。
- 影响:该状态转移绕过了租户上限、G5、搁置重新验证。违反 I4 与 5.4(E10)。
- 措施(本次修订):新增 `floor_scoped(req)`。只有同时满足人类所有者、自己的层、之前的状态、权限·深度不增加时才视为底线。除此之外的 `revert` 通过 `as_activate` 经过相同的判定。还新增了 `uses_destructive` 分支,并在 5.5 和 7.11 中写入了同样的规则。

### 3.2 检查工具输出注入(`tools/check_schemas.py:29`、`:26`)

- 低信任主体:传给 `check_schemas.py <schema> FILE` 命令的外部文档或文件名的作者。
- 复现:把 lexicon-pack 的 `concepts` 键构造成 `"x\e]0;PWNED\a\e[2K\rOK   forged.yaml[0]\n::error title=forged::…"`。该键原样进入 `json_path` 并被输出。
- 影响:只有输出与日志被伪造(窗口标题、伪造的 `OK` 行、GitHub Actions 注解)。对判定、退出码、文件、凭据没有影响。
- 措施(本次修订):所有输出的字符串都使用 `safe()`(repr 转义,截断为 300 字符)。加入了一个 assert 作为回归检查。在沙箱中重新运行的结果为 ESC 0 个、`::` 行 0 个。

## 4. 需要进一步验证

| 标题 | 位置 | 卡住的地方 | 状态 |
| --- | --- | --- | --- |
| 基线版传播自动应用只检查了权限无变化 | `docs/06-versioning-and-lineage.md:121-122` | 规格中未定义 `apply(merged)` 是否经过 `ChangeStore.activate`(E10) | 规格所有者在本次修订中定义:自动应用也经过 `activate()`,若需要批准则为 PROPOSED。`delta_permissions` 重新计算 |

第一位验证者驳回了此项。依据是根据 05:150、05:205、07:77,激活总是经过 PDP。但该结果是格式错误,按规则被丢弃;新的验证者把 06:122 缺少与 `activate` 绑定的语句视为卡住的地方,判定为 `needs_validation`。两种解读在"6.5 需要明确语句"这一点上结论一致,因此加入了该语句。

## 5. 加固备忘(非缺陷,是否已反映)

- 已反映:change-record 的确定性契约必须至少有一种可执行形式。现在只有叙述形式的记录会被拒绝。
- 已反映:`permissions_delta` 重新计算,`approved_by` 是人类主体且必须与 `agent` 不同。已写入 schema 说明与 7.11。
- 已反映:`network.allow` 与策略 `allowlist` 拒绝 IP 字面量。公共后缀通配符、存在 egress 权限、`setKnob` default ⊆ ceiling 已写为合规校验器(conformance validator)的 MUST,并添加了期望 `False` 的回归用例。
- 已反映:拒绝 YAML 别名和超过 1 MiB 的文件。555 B 的别名炸弹输出 75.5 MB 的问题和 601 B 输入导致 OOM 的问题已消除。按文档的异常已隔离(非字符串键)。
- 已反映:`design_space.py --profile`·`--check` 在失败判定时返回退出码 1,并拒绝重复键和非对象 JSON。
- 已反映:CI `permissions: contents: read`。把 4.7 摘录中的 `net.allowlist` 改为 `net.slack.post`(L-04)。
- 未反映(建议):把 Actions 固定为提交 SHA、固定 `requirements.txt` 哈希、定义 capability id `*` 的含义、共享时强制 `content_hash`、批准指纹字段。

正面模式:使用 `yaml.safe_load`。以 `ACCEPTED (validator MUST check)` 暴露跨文档规则的回归结构。在三处强制深度与形态的对应。

## 6. 覆盖率

账本 17 个单元:covered 8 · candidate 3(均已完成最终判定)· blocked 0 · deferred 6。

最终评审发现并推迟的单元:
1. 把批准·同意绑定到重新计算的权限变化、content_hash、`Contract-Migrated` 同意的问题
2. capability id `*` 与逐次调用 PDP 对比挂载时授予
3. `check_schemas.py` 的 OK 判定与 YAML→JSON 数据模型的差异(非字符串键、重复键)
4. 发布签名固定、吊销、降级
5. R3 解决缓存污染(同一租户的 Sybil 节点)
6. 7.3 的角色分离与 7.5 的标签行为规则(间接注入)

下一次审计应以 standard 配置从这 6 项开始。
