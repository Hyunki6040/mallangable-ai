<!-- LANG-BAR -->
**English** · [한국어](CONTRIBUTING.ko.md) · [简体中文](CONTRIBUTING.zh-CN.md) · [日本語](CONTRIBUTING.ja.md) · [Español](CONTRIBUTING.es.md)
<!-- /LANG-BAR -->

# Contributing

This repository is a **specification**, not an implementation. Contributions fall into three broad kinds: spec text changes, schema and example changes, and calculator rule changes.

## Before you start

```bash
pip install -r requirements.txt               # for check_schemas.py
python3 tools/design_space.py --check all     # P1~P7 must all be clean
python3 tools/check_schemas.py                # the last line must be ALL OK
```

Please send PRs with both commands passing. The full enumeration (`python3 tools/design_space.py`) takes a few minutes.

## Rules to follow

- **Identifiers are the contract between files.** Axes `A1~A11`, constraints `L`/`N`/`S`, invariants `I1~I10`, floors `F1~F7`, gates `G0~G5`, resolution steps `R0~R5`, profiles `P1~P7` and business models `B1~B20` appear together in the docs, the schemas, `design_space.py` and `check_schemas.py`. Do not renumber or delete them; append new items at the end. When retiring one, leave its number empty and mark it "retired".
- **Numbers in the docs are computed results.** If you change `AXES`, `LOGICAL_RULES`, `normative()`, `soft()` or `BMS`, rerun the tool and update every figure in `README.md`, `docs/01`, `docs/03`, `docs/09` and `CHANGELOG.md`.
- **Do not change the order of `LOGICAL_RULES`.** The "first violation" counts depend on it.
- **Profiles live in three places**: `PROFILES` in `design_space.py`, `examples/profiles.yaml`, and the README table.
- **If you change an example's structure**, the mutation paths in `CASES` in `check_schemas.py` can silently drift. Confirm that all forbidden-document checks are `OK`.
- **Language editions**: the Korean edition (`docs/ko/`, `*.ko.md`) is the original. English (`docs/en/`, the default README), Simplified Chinese (`zh-CN`), Japanese (`ja`) and Spanish (`es`) are translations and use the same file names. When you change the original, update the translations in the same PR, or list the languages you could not update in the PR description. Identifiers, numbers and code are not translated. Schema descriptions, examples and tool messages are written in English.
- Write the spec text in plain language. Requirement levels are **MUST** · **SHOULD** · **MAY**. Mark numbers without a source as **design proposal values**. Prefer primary sources ([docs/en/references.md](docs/en/references.md)).

## Issues and PRs

- Put the chapter and rule id in the title or body (e.g. `3.3 L7`, `I10`, `6.5 R2`).
- To argue against a rule, the fastest route is to show, with `--profile`, **one combination the rule filters out wrongly**.
- Propose large changes (a new axis, a new invariant, a schema contract change) as an issue first. Once incorporated, they are recorded in `CHANGELOG.md`.

## License

Contributions follow the repository licenses. Documents (`docs/`, `README.md` and others) are CC BY 4.0 ([LICENSE-docs](LICENSE-docs)); schemas, examples and tools (`schemas/`, `examples/`, `tools/`) are Apache-2.0 ([LICENSE](LICENSE)).
