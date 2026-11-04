<!-- LANG-BAR -->
[English](CONTRIBUTING.md) · [한국어](CONTRIBUTING.ko.md) · **简体中文** · [日本語](CONTRIBUTING.ja.md) · [Español](CONTRIBUTING.es.md)
<!-- /LANG-BAR -->

# 贡献指南

本仓库不是实现，而是**规范**。贡献大致分为三类：修改正文、修改 schema·示例、修改计算器规则。

## 开始之前

```bash
pip install -r requirements.txt               # 供 check_schemas.py 使用
python3 tools/design_space.py --check all     # P1~P7 必须全部为 clean
python3 tools/check_schemas.py                # 最后一行必须是 ALL OK
```

请在两条命令都通过的状态下提交 PR。完整枚举（`python3 tools/design_space.py`）需要几分钟。

## 需要遵守的事项

- **标识符是文件之间的契约。** 轴 `A1~A11`、约束 `L`/`N`/`S`、不变式 `I1~I10`、底线 `F1~F7`、门 `G0~G5`、解决步骤 `R0~R5`、配置 `P1~P7`、商业模式 `B1~B20` 会同时出现在文档·schema·`design_space.py`·`check_schemas.py` 中。不要更改或删除编号，新项目请接在后面。废弃时保留编号空位，并注明"已废弃"。
- **文档中的数值是计算结果。** 修改 `AXES`·`LOGICAL_RULES`·`normative()`·`soft()`·`BMS` 后，要重新运行工具，并修正 `README.md`、`docs/01`、`docs/03`、`docs/09`、`CHANGELOG.md` 中的所有数值。
- **不要改变 `LOGICAL_RULES` 的顺序。** "首个违规"统计依赖顺序。
- **配置在三处出现**：`design_space.py` 的 `PROFILES`、`examples/profiles.yaml`、README 表格。
- **修改示例结构时**，`check_schemas.py` 中 `CASES` 的变异路径可能会悄悄错位。请确认禁止文档检查全部为 `OK`。
- **语言版本**：韩语版（`docs/ko/`、`*.ko.md`）是原文。英语（`docs/en/`、默认 README）·简体中文（`zh-CN`）·日本語（`ja`）·Español（`es`）是译文，使用相同的文件名。修改原文时，请在同一个 PR 中一并修改译文，或在 PR 正文中写明未能修改的语言。标识符·数值·代码不翻译。schema 说明·示例·工具消息用英语书写。
- 正文用通俗的语言书写。要求级别为必须(MUST)·应当(SHOULD)·可以(MAY)。没有来源的数值标注为**设计建议值**。来源优先使用一手来源（[docs/references.md](docs/zh-CN/references.md)）。

## Issue·PR

- 请在标题或正文中写明对应章节和规则 id（例如 `3.3 L7`、`I10`、`6.5 R2`）。
- 反对某条规则时，用 `--profile` 展示该规则**错误过滤掉的一个组合**，讨论会最快。
- 大的变更（新轴、新不变式、schema 契约变更）请先通过 issue 提议。被采纳后会记录到 `CHANGELOG.md`。

## 许可证

贡献的内容遵循仓库的许可证。文档（`docs/`、`README.md` 等）为 CC BY 4.0（[LICENSE-docs](LICENSE-docs)），schema·示例·工具（`schemas/`、`examples/`、`tools/`）为 Apache-2.0（[LICENSE](LICENSE)）。
