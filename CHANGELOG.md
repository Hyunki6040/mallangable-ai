<!-- LANG-BAR -->
**English** · [한국어](CHANGELOG.ko.md) · [简体中文](CHANGELOG.zh-CN.md) · [日本語](CHANGELOG.ja.md) · [Español](CHANGELOG.es.md)
<!-- /LANG-BAR -->

# Changelog

## v0.2.4 — 2026-11-05

Multilingual editions. The spec content, design-space numbers and schema contracts did not change.

* The default README is now English, and the language editions are split out: English (`README.md`) · Korean (`README.ko.md`, original) · Simplified Chinese (`README.zh-CN.md`) · Japanese (`README.ja.md`) · Spanish (`README.es.md`). CHANGELOG and CONTRIBUTING follow the same pattern.

* The spec chapters and research notes moved to `docs/<language>/` and are written in five languages (`docs/en`, `docs/ko`, `docs/zh-CN`, `docs/ja`, `docs/es`). The Korean edition is the original; where a translation differs, the original prevails.

* Schema descriptions, example documents and tool messages and help text are now in English. The lexicon pack example exists per language (`examples/lexicon.{en,ko,zh-CN,ja,es}.yaml`). `check_schemas.py` validates all of them.

## v0.2.3 — 2026-11-05

Adversarial security review of the whole repository with the Cloudflare security-audit skill (quick profile, `docs/en/research/security-audit-2026-11-05.md`). Design-space numbers did not change.

### Control and reference architecture (chapters 4 and 5)

* The floor-action exception in the PDP's `decide()` is narrowed to `floor_scoped(req)`. It is a floor only when the owner is a human, the layer is their own, the target is a previous state, and neither permissions nor depth increase; any other revert (one called by an agent, redo, "turn back on", releasing a hold) goes through the same decision as activation. A destructive-feature branch (G5) was also added (4.8, 5.5).

### Versioning and trust (chapters 6 and 7)

* Automatic application during baseline propagation goes through `activate()` (E10), and drops to a proposal when approval is required. `delta_permissions` is recomputed rather than self-reported (6.5).

* The security checklist gained items for floor-exception scope, automatic propagation application, permission-change recomputation, egress declarations and tool-output escaping (7.11).

### Schema contracts

* `change-record`: at least one deterministic contract item must be in executable form. Records with only descriptive items are rejected.

* `extension-manifest` and `policy`: `network.allow` and `allowlist` reject IP literals. Public-suffix wildcards, existence of an egress permission, and `setKnob` default ⊆ ceiling are stated as conformance validator MUSTs, with regression cases added (expecting `False`).

### Tools and CI

* `check_schemas.py`: escapes control characters in output, rejects YAML aliases and files over 1 MiB, isolates exceptions per document.

* `design_space.py`: `--profile` and `--check` exit with code 1 on `normative`, `logical` or input errors, and reject duplicate keys and non-object JSON.

* The CI token is restricted to `contents: read`.

## v0.2.2 — 2026-11-04

Preparation for the open-source release. The spec chapters, design-space numbers and schemas did not change.

* Licenses finalized: documents CC BY 4.0 (`LICENSE-docs`), schemas, examples and tools Apache-2.0 (`LICENSE`).

* Added `CITATION.cff`, `CONTRIBUTING.md` and `requirements.txt`.

* The tools accept files from other projects: `design_space.py --profile FILE.json`, `check_schemas.py <schema> FILE...`.

* Added "Applying it to your project" to the README (six steps: vocabulary → design space → extending the calculator → data contracts → architecture → conformance claim) and a citation format.

* Published as a public GitHub repository (https://github.com/Hyunki6040/mallangable-ai). The opening of the README was rewritten in the order problem statement (three gaps) → six core ideas → how it works → change example, and CI was added that runs the schema regression checks and the P1~P7 checks on every push and PR.

## v0.2.1 — 2026-11-03

Surveyed and incorporated the ThinkRail (JetBrains/thinkrail, Apache-2.0) specification documents (`docs/en/research/thinkrail-analysis.md`). Design-space numbers and schemas did not change.

### Control and reference architecture (chapters 4 and 5)

* Approvals have a scope (this time only · for this task · always), and "always" is bound to the feature's content\_hash and permission list. Anything other than an affirmative answer is a denial (4.8).

* Revert is based on the state id the user saw. If the state differs, nothing changes; redo is the same operation (5.5).

* Added rules for handling judge output. Malformed output fails, the record is rebuilt by the harness, a failure with no findings is rejected, a pass is not finalized while findings are open, and the retry cap is shared by all entry points (5.8).

* E11 is the only completion signal, and awaiting-approval is a level signal. Each mapping-table entry records the behavior verified, the re-verification condition and the removal condition (5.6).

* The watchdog's isolation unit is the whole feature (5.9).

### Versioning, trust and experience (chapters 6\~8)

* Concurrent generation jobs each get their own working copy and record only the paths they changed (6.4).

* A read failure on a merge input is not treated as absence (`null`, i.e. deletion) (6.5).

* Accepting a share applies only to the content at that moment, and received features cannot hijack my command or shortcut names (6.9).

* Lists, previews and permission displays do not execute extension code (7.11).

* Lexicon packs: stored data holds only `concept id + args`, shared features cannot change the lexicon pack, and the order of string-level substitution is defined (8.9).

## v0.2 — 2026-10-30

Incorporated three studies (`docs/en/research/`): the Harness² analysis, the prior-art survey (MCP, AG-UI, OTel, Cedar, RFC 7396 and others) and the adversarial review.

### Design space (chapter 3, `tools/design_space.py`) — numbers changed

* The depth definitions of 2.6 are enforced as rules. L3 is `A1∈{D1,D2,D3} ⇒ decl`, L4 is `D4 ⇒ sandboxed`.

* New N6: D5 is not shared and cannot use the snapshot topology (I1).

* Recommended combinations 70,516 → **36,772**, structural families 1,618 → **863**, business options 58% → **57%**. The 7×20 BM coupling matrix did not change.

* P1 and P6 moved to D4, and P2, P5 and P7 to declarative D3. All seven profiles remain clean.

* Rule statistics now include order-independent independent violation counts and unique violation counts. The claim "L1 filters the most" was withdrawn.

* Invalid input is rejected: nonexistent profiles, JSON errors and unknown axes.

### Core model and control (chapters 2 and 4)

* Layer composition `⊕` is defined as RFC 7396 JSON Merge Patch. Its relation to 3-way merge is stated as well.

* Moving from on hold → active goes through re-verification.

* I8 moved to a requirement of the Governed level. P1 and P5, which have no server, can reach only the Core level.

* Added a Cedar policy engine adapter, with I5 proved via SymCC. User floor rights (F1\~F7) are evaluated before the engine.

### Reference architecture (chapter 5)

* Under `own` visibility, the generator receives only the types and capability map of upper layers (I6).

* Activation goes through the PDP and G5. D4 code is mounted only with zero permissions before approval.

* G4: source-blind judging applies, and candidates are presented under seed-based anonymous ids.

* G1: on failure, returns a fixable reason and keeps the current state after retrying.

* Added harness event mapping tables. AG-UI, A2A and MCP `input_required` have mapping tables; Codex needs confirmation against official documentation.

* Warned that a misconfigured hook falls back to default-allow. Stated that `Stop`/`SubagentStop` hooks are not blocking gates.

* Observability fields were renamed to OTel GenAI names, and `policy.decision_id` and `traceparent` were added.

### Versioning, trust, experience and business (chapters 6\~9)

* The propagation algorithm was rewritten.

  * It uses the union of the contracts along the whole path.

  * A parent awaiting approval does not stall its children.

  * Canaries are seed-based random samples.

* Weakening a contract is allowed only with a person's explicit consent and is recorded as `Contract-Migrated`.

* An integrity axis was added to information-flow labels (FIDES).

* Three threats were added: contract and judgment poisoning, resolution cache poisoning, and compromise of upstream releases or the operator.

* Publisher signatures use the in-toto/SLSA format.

* Secrets are received only through MCP URL-mode elicitation. ModelPort is not built on top of MCP Sampling.

* Customer artifacts enter the official baseline only with opt-in and license consent (B10, B19).

### Mallang-Bench (chapter 10)

* Hidden checks are isolated, with leak-detection tripwires.

* Items whose judging failed are reported as unscored and removed from the denominator.

* Run conditions are reported as well: network restrictions, call counts, cache state.

* The SBR denominator includes merges approved by a person.

### Schemas (`schemas/`, new `tools/check_schemas.py`)

* Contract items are defined in executable form (`tree-query`, `unit`, `snapshot`, `judge`). At least one deterministic item is required, and `judge` must be non-deterministic. The free-text form remains only for backward compatibility.

* Required gates per depth are defined. When permissions increase, G5 and `approved_by` are required.

* Intent statements that are whitespace only, and invalid ids and dates, are rejected.

* Added fields:

  * `provenance.harness_digest`

  * `extensionPoint.merge`

  * `catalog_id`

  * `destructive`

* Policy knobs must satisfy floor ≤ default ≤ ceiling.

* In a manifest, D1\~D3 artifacts may only be declarative.

* Of the 17 documents the spec forbids, the schemas reject 15. The remaining 2 require comparison across documents, so the spec states that a validator **MUST** check them.

### References

* Secondary sources were replaced with primary ones: the Agent Skills specification, the English plugins documentation, A2UI v0.9.1, Mergiraf (GPL-3.0-only).

* New sections were added: policy engines, observability, supply chain, harness improvement and evaluation.
