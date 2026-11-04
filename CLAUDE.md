# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **specification**, not an implementation: Mallangable-AI, a reference architecture for AI-driven malleable software. The deliverables are spec chapters (`docs/<lang>/`), JSON Schemas (`schemas/`), examples that validate against them (`examples/`), and two Python checkers (`tools/`). There is no app, no package manager, no build step. Not a git repository.

### Languages

- Spec docs live in `docs/<lang>/`. `docs/ko` is the source of truth; `docs/en`, `docs/zh-CN`, `docs/ja` and `docs/es` are translations.
- `README.md` is English; other languages are `README.<lang>.md`. `CHANGELOG` and `CONTRIBUTING` follow the same pattern.
- Schemas, examples and tools are in English. Exception: `examples/lexicon.<lang>.yaml` are per-language data packs; `check_schemas.py` validates every `examples/lexicon.*.yaml`.

## Commands

```bash
python3 tools/design_space.py                 # full enumeration stats (JSON), stdlib only
python3 tools/design_space.py --markdown      # same stats as tables used in docs/03
python3 tools/design_space.py --check all     # validate reference profiles P1~P7 (or --check P3)
python3 tools/design_space.py --bm            # profile × business-model matrix (docs/09)
python3 tools/design_space.py --bm-stats      # BM feasibility over all recommended combos
python3 tools/design_space.py --profile '{"A1":"D3",...all 11 axes...}'
python3 tools/check_schemas.py                # needs jsonschema + pyyaml; exit 1 on any failure
python3 tools/check_schemas.py policy FILE... # validate external docs against one schema (skips self-test)
python3 tools/design_space.py --profile FILE.json  # --profile accepts a path or inline JSON
```

"Build verification" for this repo = both tools run clean: every P1~P7 stays `clean`, and `check_schemas.py` ends with `ALL OK`.

## How the pieces connect

- **Identifiers are the cross-file contract.** Axes `A1~A11`, constraints `L`/`N`/`S`, invariants `I1~I10`, user floors `F1~F7`, gates `G0~G5`, resolution steps `R0~R5`, profiles `P1~P7`, business models `B1~B20`. They appear in docs prose, schema constraints, `design_space.py` rule tables, and `check_schemas.py` case names. Renaming or renumbering one means grepping all four places.
- **Numbers in the docs are computed, not authored.** `design_space.py` produces the counts (1,944,000 raw → 36,772 recommended, 863 families, 57% …). Those figures are copied into `README.md` and every `README.<lang>.md`, `docs/*/01-introduction.md`, `docs/*/03-design-space.md`, `docs/*/09-business-coupling.md`, and `CHANGELOG.md` and every `CHANGELOG.<lang>.md`, in every language. Any change to `AXES`, `LOGICAL_RULES`, `normative()`, `soft()`, or `BMS` requires rerunning the tool and updating every one of those files.
- **`LOGICAL_RULES` order is load-bearing**: it defines the "first violation" counts. Don't reorder; independent/unique counts are order-free and are what claims should cite.
- **Profiles are duplicated by hand**: `PROFILES` in `design_space.py`, `examples/profiles.yaml`, and the README profile table. Keep them in sync.
- **`check_schemas.py` has two halves**: (1) every document in `examples/*.yaml` must validate against its schema (multi-doc YAML, mapping in `EX`); (2) `CASES` mutate those examples into spec-forbidden documents and assert the schema rejects them. Cases expecting `False` are cross-document rules JSON Schema can't express — they document that a runtime validator MUST check them. Changing an example's structure can silently break the mutation paths in `CASES`.
- Depth rules (D1~D3 declarative, D4 sandboxed, D5 native/core) are enforced in three places: `docs/*/02-core-model.md` 2.6, `design_space.py` L3/L4/N6, and `extension-manifest.schema.json`.

## Writing conventions

- Any change to `docs/ko` must be mirrored in all translations (`docs/en`, `docs/zh-CN`, `docs/ja`, `docs/es`).
- Spec prose is plain-language. Korean source uses requirement levels 반드시(MUST) · 해야 함(SHOULD) · 할 수 있음(MAY); translations use MUST · SHOULD · MAY.
- Any number without a source link is a **설계 제안값** (design proposal value) — mark new ones the same way.
- Translations take terms from the English column of `docs/ko/glossary.md`.
- `docs/*/references.md` prefers primary sources; `docs/*/research/` holds the survey/adversarial-review notes that later edits cite (e.g. `adversarial-review 1.2, H-06`).
- `CHANGELOG.*` records major spec revisions only (numbers changing, new rules/invariants, schema contract changes), grouped by chapter.

## Ignore

`graft/` (generated code-graph cards), `.tybre/`, `.remember/`, `tools/__pycache__/`.
