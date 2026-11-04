<!-- LANG-BAR -->
**English** · [한국어](../../ko/research/adversarial-review.md) · [简体中文](../../zh-CN/research/adversarial-review.md) · [日本語](../../ja/research/adversarial-review.md) · [Español](../../es/research/adversarial-review.md)
<!-- /LANG-BAR -->

# Adversarial review — Mallangable-AI v0.1 (2026-10-30)

Scope: `README.md`, `docs/01~10`, `docs/glossary.md`, `docs/references.md`, `schemas/*.json`, `examples/*.yaml`, `tools/design_space.py`.
Perspectives: a program committee, a security reviewer, and an engineer who wants to implement from this spec alone. No file other than this document was modified.

Verification environment: Python 3 (stdlib), with `jsonschema 4.26.0` and `pyyaml 6.0.3` in `/tmp/mreview/venv`. All helper scripts are in `/tmp/mreview/*.py` (outside the repository).

---

## 0. Summary

The computed numbers, schema pass results, profile table and BM matrix are **all mechanically correct.** The problem is that those numbers and schemas do not guarantee what the spec text *claims*. The five largest defects are:

1. Even with `A5=own`, the conversational generator is given upper-layer artifacts. This directly violates I6 and the core principle of 3.2. P2 and P6 fall into this case.
2. **There is no executable representation of the contract (κ).** The contract is central to the model, yet the schema holds only free text, and the party that writes the contract is the generator itself. As a result I2, I7, I10, G2, B9 and SBR all lose their footing.
3. **The conformance definition contradicts the recommended profiles.** The Core level requires I1~I10 (including I8) to be guaranteed "by design". But P1 and P5 have no server, so, as 4.8 itself admits, they cannot guarantee I8.
4. Applying the depth definitions of 2.6 (D3=declarative, D4=sandboxed code) literally collapses the headline number (70,516) and the 'recommended' verdict for 5 of the 7 profiles.
5. The propagation algorithm (6.5) and the contract-preserving merge (6.7) cannot be implemented as written. They ignore intermediate layers, jobs for children under a parent awaiting approval stall, and contract monotonicity conflicts with "move to the upstream approach".

---

## 1. Mechanically verified facts

### 1.1 Calculator output vs. document figures — all match

`python3 tools/design_space.py --markdown` (2.6 s):

| Item | Tool output | README | docs/03 | docs/01 |
| --- | ---: | ---: | ---: | ---: |
| Raw combinations | 1,944,000 | ✓ :65 | ✓ :224 | ✓ :40 |
| Pass L | 193,725 (9.97%) | ✓ :66 | ✓ :225 | — |
| Pass L+N | 124,102 (6.38%) | ✓ :67 | ✓ :226 | — |
| Recommended | 70,516 (3.63%) | ✓ :68 | ✓ :227 | ✓ :40 |
| Structural families | 1,618 | ✓ :69 | ✓ :229 | ✓ :40 |
| Mean completions | 43.58 / 75 (58%) | ✓ :70 | ✓ :230 | — |
| First-violation counts per rule L1~L11, N1~N5, S1~S7 | (table) | — | ✓ :237-247 all | — |
| Recommended per depth D1 8,616 / D2 8,616 / D3 37,968 / D4 14,968 / D5 348 | ✓ | — | ✓ :256 | — |
| Completion distribution 72:224, 57:224, 42:322, 28:270, 24:171 | ✓ (60:48, 48:48, 40:48, 38:106, 36:69, 32:88 omitted as "etc.") | — | ✓ :231 | — |
| "No family has a credits·none completion (N3)" | 0 such families | — | ✓ :231 | — |
| Ω = 5×3×3×4×3×4×4×3×5×5×3 | 1,944,000 | — | ✓ :224 | — |

- `--check all`: P1~P7 all `clean`, no violations, no warnings. Matches 03:268.
- `--profile` example (README:111): `"result": "logical", "violated": "L1"`. Matches README:112.
- The `--bm` 7×20 matrix was compared cell by cell with docs/09:60-79 and all cells match (`/tmp/mreview/bmdiff.py`).
- All 20 rows of `--bm-stats` match docs/09:85-99.
- The names and 11 axis values of `examples/profiles.yaml` and `PROFILES` match for all of P1~P7.

### 1.2 Schema validation

`Draft202012Validator.check_schema` reports all 5 schemas as valid. The example files were checked with `FormatChecker` enabled, across all documents of each multi-document file.

```
capability-map.example.yaml[doc 0]      OK
change.example.yaml[doc 0], [doc 1]     OK
extension-manifest.example.yaml[doc 0]  OK
lexicon.ko.yaml[doc 0], [doc 1]         OK
policy.example.yaml[doc 0..2]           OK
```

- `profiles.yaml` has no corresponding schema, so only its values were compared with the tool (see 1.1).
- References between examples were also checked. The 5 `lexicon_id`s in `capability-map` and the manifest's `label` exist in the lexicon pack, and every id the education pack overrides exists in the base pack. The change example's `points` and `permissions_delta.add` exist in the capability-map. No `basic_forbidden` word appears in any basic expression or explain phrase.

**Negative tests** (`/tmp/mreview/neg.py`). These are documents the spec forbids but the schemas accept.

```
ACCEPTED :: D4 + permissions_delta.add, no G5, no approved_by (I4)
ACCEPTED :: judge_instance == generator_instance (I7)
ACCEPTED :: G4 pass but no judge_instance (I7)
ACCEPTED :: contract = single judge item, deterministic defaulted true (2.5)
ACCEPTED :: D5 record with only G0 (5.8 requires G0-G5)
ACCEPTED :: points with invalid id
ACCEPTED :: intent = 4 spaces (I9)
ACCEPTED :: manifest D3 + form native (2.6 D3=declarative)
ACCEPTED :: manifest D4 + native (2.6 D4=sandboxed code)
ACCEPTED :: network allow '*' with no egress capability
ACCEPTED :: D4 sandboxed with no state/migrate (5.9)
ACCEPTED :: depth ceiling D9 / default banana
ACCEPTED :: org depth ceiling D5 > tenant D3 (I5 not checkable)
ACCEPTED :: default outside ceiling
rejected :: provenance.at = 'yesterday'
rejected :: floors missing 6 of 7
```

### 1.3 Cross-references (`/tmp/mreview/xref.py`)

- Relative links: 0 broken links.
- Section-number references (`2.6`, `6.11`, etc.): every reference has a matching heading. The only mismatches flagged were percentages (9.97 etc.), which are false positives.
- Id families A1~A11, I1~I10, F1~F7, G0~G5, R0~R5, P1~P7, B1~B20, O1~O13, E1~E16, L1~L11, N1~N5, S1~S7, T0~T4, X1~X6: no out-of-range ids, and no ids that are defined but unused (`L0` is a mermaid node name and unrelated).
- URL present only in references.md and not cited in the text: `https://code.claude.com/docs/es/plugins/overview` (references.md:22).
- URLs cited in the text but missing from references.md: none.
- HTTP status: 23 of 24 return 200. Only `thehackernews.com/...341-malicious-clawhub.html` returned 403 (bot blocking) and could not be checked.

### 1.4 External source checks (WebFetch)

| Claim (location) | Result |
| --- | --- |
| Claude Code hooks: 30+ events, 5 handler types, admin blocking, `onFailure:"block"`, `updatedToolOutput`, `PostToolBatch` (05:261-274) | All exist. There are 33 events. `allowManagedHooksOnly` exists. `onFailure` works only on command and http hooks in v2.1.295 or later, and **has no effect on `Stop` and `SubagentStop`** → L-07 |
| CaMeL 77% vs 84% (07:104) | Matches (AgentDojo). The document omits the benchmark name |
| Unit 42: 22MB inflation, analysis of Feb~May 2026, "no isolation between skill logic and agent authority" (07:162) | Matches (2026-06-23) |
| 341 malicious, Koi Security (01:17, 07:162) | 341 and Koi confirmed via the Unit 42 article. **The audit count of 2,857 could not be checked because of the 403** |
| Ink & Switch essay, 2025, "AI code generation alone is not enough", MacLean 1990, Nardi & Miller (01:7-9, 01:63) | Matches (June 2025). The original metaphor is "appliances: built far away, sealed, unchangeable", so "bought from a store" is a paraphrase |
| The Register: Free·Pro·Max OAuth tokens banned for third-party use, including the Agent SDK (03:135, 08:272, 09:132) | Matches (revised 2026-02-20; the policy itself dates from 2024-02) |
| falcao.org timeline (09:132) | Broadly correct. The article's order is: server-side blocking on January 9, formalized on April 4, **Agent SDK credits** on June 15 (list price, no rollover). The document leaves out the January blocking and generalizes it to "programmatic use outside Claude Code" |
| MCP Apps: mandatory sandboxed iframe (03:67) | Matches as "Mandatory iframe sandboxing". The SEP status is Final |
| Shiplight: `allowed-tools` is experimental (05:236) | Matches (2026-08-10) |

### 1.5 Additional values computed with the tool (`/tmp/mreview/indep.py`, `alt.py`, `more.py`, `q.py`)

| Computation | Result |
| --- | --- |
| **Independent** violation count per rule (order-free) | L3 518,400 · L5 486,000 · **L1 432,000** · L4 388,800 · L8 364,500 · L10 324,000 · L7 324,000 · L2 259,200 · L11 162,000 · L6 162,000 · L9 121,500 |
| **Unique violation** count per rule (violates only that rule) | L3 129,150 · L5 116,235 · L7 77,490 · L4 64,575 · **L1 60,750** · L2 39,150 · … |
| A2 distribution among recommended D3 combinations | sandboxed 21,588 · decl 8,616 · **native 7,764** |
| Number of recommended D4+native combinations | **4,044** |
| A6 of the 348 recommended D5 combinations | **all snapshot**. Of these, 104 have A8=public (client 32 · server 48 · hybrid 24) |
| Adding rules `D3⇒decl` and `D4⇒¬native` per the 2.6 definitions | recommended **37,120**, families 875. **P1, P2, P5, P6, P7 drop out as `logical`** |
| Adding rule `A5=own ⇒ A3=server` | recommended 52,264, families 1,246. **P2 and P6 drop out** |
| Recommended configurations left after folding values no rule distinguishes (D1≡D2, V0≡…≡V3, preview≡gated, proposed≡auto) | **8,969** (the classification is unchanged by folding) |
| Max–min spread of mean completions per value, by structural axis | **A1 23.2** > A3 21.7 > A2 13.6 > A4 13.4 > A8 12.1 > A5 11.5 > A6 11.3 > A7 1.2 |

### 1.6 Tool robustness

```
--check P9                → KeyError: 'P9' (traceback)
--profile '{bad'          → json.decoder.JSONDecodeError (traceback)
--profile with "A12":"x" added → clean, no error
```

There is no self-check or assert for the calculator anywhere in the repository.

---

## 2. Findings (by severity)

### CRITICAL

| # | Location | Evidence | Minimal fix |
| --- | --- | --- | --- |
| C-01 | docs/05:363, docs/05:45, docs/03:83, docs/02:198 (I6), tools/design_space.py:64 | In the 5.10 table, the generator's "upper-layer artifacts" cell is ● `when own/open`. 5.2 places conversational generation for hybrid "on the device". Yet 3.2 A5 says "code an agent can read can eventually be read by the person talking to that agent", and I6 makes the same demand. So with `own` (see only your own), the conversing generator still sees upper-layer code. The tool has no constraint such as `own ⇒ server` (L10 only restricts topology). Adding this rule **drops P2 and P6** (1.5) | Change the generator cell in 5.10 to **"types and capability map only, artifacts —"** when `own`. If that is not possible, add L12 `A5=own ⇒ A3∈{server}`, or state that in hybrid, any generation that reads upper-layer artifacts is forced onto the server. Recompute the P2 and P6 verdicts and the 3.4 figures |
| C-02 | docs/02:92-108, schemas/change-record.schema.json:81-91, docs/05:286, docs/06:157-167, docs/09:114 | The contract is defined as "`k_i : A → {true, false}`", but the schema's `contractItem` has `given` and `expect` as **free text** (e.g. "panel first shown within 200ms"). There is no field for the query to run, the fixture, or pinned environment details. On top of that, 5.7 makes the **generator** the contract author ("generate artifacts and contracts"). So even with I7 (separating generation and judging), the generator writes the G2 judging criteria itself. I2, I10, B9 (selling survival guarantees) and SBR all rely on this representation, yet machine judging is impossible. Because `deterministic` defaults to `true`, a contract with a single `check: judge` item also passes (1.2) | ① Give `contractItem` machine-executable forms via `oneOf`, such as `tree-query{selector, fixture_ref, assert}`, `unit{entry, input, expected}`, `snapshot{env_ref, baseline_ref}`. ② When `check: judge`, fix `deterministic: const false`, and put `contains: {properties: {check: {enum: [tree-query, unit, snapshot]}}}` in `contract` to enforce the "≥1 deterministic contract" of 2.5. ③ Add to 5.7: **"The interpreter drafts the contract at the task-spec stage, and the generator cannot delete or weaken the contract"**, extending the scope of I7 to contracts |
| C-03 | docs/10:64-65, docs/02:200·204, docs/04:166-167, docs/03:268 | The Core level is "I1~I10 guaranteed by design". I8 is "final enforcement only at the operator boundary". Yet 4.8 itself writes that "offline personal mode (P1) has no server, so the device's PDP is the only one". Therefore **P1 and P5 (A3=client, no server) are by definition not Core-conformant.** Even so, 03:268 presents both as 'recommended'. Since Governed requires I8 again as "Core + server receive-check (I8)", the authors also appear to think I8 is not part of Core. The mandatory human approval of I4 can also be bypassed on the client | Remove I8 from Core and move it to the Governed requirements. Change the Core definition to "I1~I7, I9, I10", and fix the conformance statement at 2.9:204 accordingly. State in 3.5: "P1·P5 can reach the Core level, not Governed" |

### HIGH

| # | Location | Evidence | Minimal fix |
| --- | --- | --- | --- |
| H-01 | docs/02:118-119, docs/07:113, tools/design_space.py:48-53, schemas/extension-manifest.schema.json:63-76, docs/03:272-273 | 2.6 defines D3 as a "declarative UI tree" and D4 as "arbitrary code inside a sandbox". But 5 of the 7 profiles are `A1=D3, A2=sandboxed`. The recommended combinations also include 7,764 D3+native and 4,044 D4+native. The manifest schema also allows D3+native and D4+native (1.2). Applying the logic of L3 ("allowing code artifacts at a depth that needs no code is redundant") to D3 as well reduces the recommended count to 37,120 and drops P1, P2, P5, P6, P7 (1.5). Meanwhile 7.6 writes "frame … panel (D3)", and the manifest example's `format` includes `html-panel`. The spec is split with itself on whether D3 allows code | Settle on one. Either (a) redefine D3 as "catalog-declarative **or** frame-isolated panel code" and lower "pre-execution analysis: mostly" in the 2.6 table to "declarative only", or (b) widen L3 to `A1∈{D1,D2,D3} ⇒ A2=decl` and fix the profiles. Either way, add an L rule and a manifest `allOf` condition that block D3/D4+native |
| H-02 | docs/02:142 (D5 separation MUST), docs/02:193 (I1), tools/design_space.py:25 | A1=D5 means "the user can change even the core". This directly contradicts I1 (a user layer does not change C) and "D5 is not a user layer" in 2.6. Even so, the tool judges 348 D5 combinations as 'recommended'. All are snapshot, and they include 104 publicly shared native core patches (1.5) | Add `N6: A1=D5 ⇒ (A8=none ∧ A6≠snapshot)`, or shrink the value range of A1 to D1~D4 and move D5 to a separate off-axis concept, a 'core fork process'. Recompute the 3.4 and README figures |
| H-03 | README:72, docs/03:261, docs/03:233 | The claims are "90% of raw combinations … make no sense", "the rule that filters out the most is L1", and "this means it is the most common design contradiction". However, ① L3 and L5 are normalization (deduplication) rules, not rules that filter out 'combinations that make no sense'. Their independent violation counts, L3 518,400 and L5 486,000, exceed L1's 432,000. ② L1 ranks first because of the ordering of the 'first violation' count. By unique violations, L1 is 5th at 60,750 (1.5). 03:233 itself warns about the order dependence and then immediately uses it in an interpretation. ③ The number of combinations is not how often designers need something. So "the most common design contradiction" is an unfalsifiable claim. ④ 70,516 includes a share inflated by values no rule distinguishes (V0~V3 etc.); folding them gives 8,969 | Change interpretation 1 to "excluding the normalization rules (L3, L5), …", and add the independent and unique violation counts to the table. Change "most common" in README:72 to "representative". Add a footnote to 3.4: "sensitive to value resolution; the configurations the rules distinguish number 8,969" |
| H-04 | docs/06:99-120 | The propagation pseudo-code cannot be implemented as written. ① `merge(..., theirs=r)` merges the **original release r** into grandchild nodes as well, so changes from intermediate (tenant, org) layers are lost. ② `contracts = κ(r) ∪ κ(m)` also drops the intermediate layers' contracts. ③ Because of the `where parent(m) has applied r` condition, if a parent is waiting for approval in the `proposed` state, the child is never processed in this loop, and there is no mechanism to retrigger it. ④ The meaning of `return` inside the `parallel_for` body is undefined. ⑤ `canary(descendants_in_topo_order…, ratios)` picks the first 5% in topological order, so the canary is a bundle of upper nodes, not a random sample. ⑥ There is no criterion for classifying the cause in the "same cause" failure rate. ⑦ "One job per node, cancel on a new release" causes starvation when the release cycle is shorter than the approval delay | Change to `theirs = parent(m).main@after_apply(r)` and define contracts as `⋃_{a ∈ ancestors(m)} κ(a) ∪ κ(m)`. Rewrite it in an event-driven style where the parent-applied event (`baseline.applied`) creates the child job, and define the canary as "a random sample of nodes at the same depth". Use `(gate id, contract id, extension point)` as the failure cause key. Append a state machine to 6.5 |
| H-05 | docs/02:54·71, docs/06:83-95, docs/06:157-169 | There are two merge models. 2.3 **composes** layers at run time by **override (⊕)**, while 6.4 keeps the user repository as a **fork** of the baseline and does a **3-way merge**. If layers are composed, an upstream change should be a target for contract re-checking, not merging; if they are forks, ⊕ is not needed. An implementer cannot decide which of the two to build. Also, "contracts can only get stronger" in 6.7:165 conflicts with the option "move to the upstream approach" in 6.7:169 (which requires dropping the user contract 'sidebar panel'), and with point deprecation in 6.12 (κ_down cannot in principle be satisfied). Yet 8.8 shows "6 of 7 carried over as is" as if it were the usual case. Where the upstream contract κ(r) is stored (no schema) is also undefined | Settle on one in 2.3: "storage is per-layer deltas, composition is ⊕, merging applies only to concurrent edits *within the same layer*". Add to rule 2 of 6.7: "Exceptions are when a human chooses at R5, and contract migration (rename map) due to point deprecation. Leave `Contract-Migrated` in the record". Add `baseline-release.schema.json` to hold release contracts |
| H-06 | schemas/change-record.schema.json:7·33-46·61-76, schemas/extension-manifest.schema.json:31-41, schemas/policy.schema.json:92-99 | 14 negative tests pass (1.2). Specifically: a record whose permissions grew but has no G5 and no `approved_by` (I4), `judge_instance == generator_instance` (I7), G4 pass with no judge record, D5 with only G0 (5.8), an intent made only of blanks (I9), D3/D4 native, `network.allow:["*"]` with no egress capability, `depth.ceiling: D9`, and a default outside the ceiling. The schemas could block these but do not | Fix only what can be fixed inside the schemas. If `permissions_delta.add` has `minItems:1`, make `gates.G5 const approved` and `provenance.approved_by` `required` (`if/then`). Make `validation.gates` `required` per depth. `pattern: "\\S"` on `intent`. The same pattern as capability-map on `points.items`. Turn orderedKnob into a per-knob `enum`. In the manifest, state in the description that a non-empty `network.allow` requires an egress capability in permissions (since this is a cross-document check). Hand cross-document and value-comparison checks such as the 'must differ' of I5 and I7 to a **conformance validator**, and document that |
| H-07 | docs/07:18-28, docs/05:286-288, docs/06:167·196 | Three cases are missing from the threat model. ① **Contract and judge poisoning**: an injected generator can write a contract that passes malicious behavior, or plant judge-targeted instructions in the artifact ("this panel satisfies the intent"). The judge has no external communication, but it is fully exposed to *integrity* attacks. ② **Resolution cache poisoning**: a malicious user within the same tenant can create a 'verified' resolution using only their own contracts, which R3 then reuses for everyone in the tenant. The scope limit in 6.8 only blocks leakage *between* tenants and does not block lateral movement *within* a tenant. ③ **Compromised upstream release or operator**: key management for signing (06:91), revocation, the blast radius under `auto` application, and an operator pushing a malicious change down as the official baseline are not covered | Add three rows to the attacker table in 7.1. The controls are, respectively: ① the interpreter owns the contract, and judge input is accepted only in a fixed schema (the raw artifact stays outside the judge's context). ② Cache loading happens only after re-verification on k or more nodes other than the user who created the resolution. ③ Release signing keys are pinned per PEP, canaries are mandatory even for `auto` application, and tenants get the right to refuse an upstream release |
| H-08 | docs/06:273 vs docs/09:116·119 | 6.10 promises: "**We do not put customer-made artifacts into the official baseline** … committing to this principle in writing is a precondition for enterprise customer trust". But B19 is "promote widely shared features to official paid extensions and share revenue with the original author", and B10 is "reward when adopted into an org or **official** baseline". Within the same spec, the promise and the business models collide head-on | Change the 6.10 sentence to "Customer artifacts are not included **without consent**. Public (A8=public) shares are promoted only with the original author's explicit license consent", and reference this in the condition cells of B10 and B19 |
| H-09 | docs/02:180-181·187, docs/05:189, docs/05:338 | ① 2.8 says "**every path to active goes through verification**", but `On hold --> Active: re-resolved by user choice` in the same diagram does not go through verification. ② In the last step of flow 1 in 5.4, `E->>S: activate(state)`, the experience plane calls the store directly without going through the PDP, E10 `activate.before`, or G5. This flow has no approval path at all. ③ Step 1 of hot swap in 5.9 "pre-mounts in a hidden slot once G2 passes". D4 code can receive permissions and run before approval (G5) | ① Change to `On hold --> Verifying`. ② Insert a `S->>P: activate decision` step in 5.4 and draw the G5 branch. ③ Add the condition "only after G5 passes, or with 0 permissions" to hidden-slot mounting |

### MEDIUM

| # | Location | Evidence | Minimal fix |
| --- | --- | --- | --- |
| M-01 | schemas/capability-map.schema.json:5·45-61, docs/02:24-40, docs/06:202-212, docs/05:372-383, docs/06:288 | Several objects are defined in the documents but have no schema: sharing (6.9 YAML), baseline release and lineage node (6.3), propagation job, `AccessRequest`·`Decision` (4.8, 5.3), telemetry event (5.11 JSON), and the `contract.yaml` file that records reference. The capability-map schema mentions a "state schema" in its description but has **no Σ field.** The `in/out` names in 2.2 also differ from the schema's `input_schema/output_schema`, and `d_max` and `version`, which are in the schema, are not in the 2.2 definition. change-record has no lifecycle status field (on hold, superseded), and `parent_state` is optional, so the 'recorded previous state' of I3 cannot be enforced | For now add only two: `share.schema.json` and `baseline-release.schema.json` (the rest in v0.2). Add `state_schema` to capability-map and align the 2.2 tuple with the schema field names. Make change-record's `provenance.parent_state` `required` and add a `status` enum |
| M-02 | docs/02:147-161, docs/04:14-24·46-64·77-83, schemas/policy.schema.json:55-68·65 | The policy lattice has four gaps. ① `valueKnob`s (code_visibility, model_route, admin_visibility) have no order, so I5 (`p_child ⊑ p_parent`) cannot be decided. ② For each knob, it is not specified whom the 'risk' is a risk to. Admin visibility is a risk to the user, yet the tenant sets the ceiling. So if `p_U` takes part in the intersection, the user can lower admin visibility. The 'locked' preset sets baseline application to `auto`, the highest-risk value. ③ There is no rule for an empty interval intersection (child floor > parent ceiling). ④ The knobs the presets use — 'direct creation', 'install depth', 'gate approver' (`p.gate_approver`, 04:161), 'verification strength' — are not in the schema. Also F6 ("stop when exceeded", MUST), yet the `on_exceed` enum contains `notify`, which can violate the floor | Add `order` and `risk_bearer` (user/tenant/operator) per knob to the table, and specify per knob which actors take part in the intersection. Handle an empty intersection as "parent wins + audit event". In the schema, add `create`, `install_depth`, `gate_approver`, and either remove `notify` from `on_exceed` or redefine `notify` as 'notify after stopping' |
| M-03 | docs/03:202-203, tools/design_space.py:78-81, docs/09:35·44 | N3 (credits ⇒ A10≠none) and N4 (public ⇒ A10≠none) mix up **tenant admin visibility** (A10) and **operator metering and audit** (MeteringPort, 5.3). Credit billing only needs operator metering and has nothing to do with what the tenant admin sees. This confusion feeds into the filtering of 7,659 by N3 and 6,540 by N4, and into the B12 and B16 verdicts | Either treat operator metering as an always-on premise outside the axes and delete N3, or add an 'operator audit level' axis separate from `A10`. At minimum, change the rationale text of N3 and N4 to "operator metering" and review the conditions again |
| M-04 | docs/07:121-131 | For the information-flow label `λ=(scope, grade)`, ⊔ does not define how *scopes* combine (tenants A and B, user scopes mixed through sharing). Grades V0~V3 reuse the admin visibility levels directly as data sensitivity, so the grade of user work data (the body of a to-do) cannot be determined | Make scope a set, with ⊔ as union, and define the read condition as 'viewer scope ⊇ λ.scope'. Add `D` (user data) to the grades as an element incomparable with V3 |
| M-05 | docs/03:320, docs/03:343-347 | `Public → A4≥frame` in the 3.6 flowchart contradicts declarative artifacts (L5: decl ⇒ A4=none) and P4 (public, decl, none). The arrow labels in the 3.7 evolution diagram also differ from the actual axis differences (diff in 1.5). P3→P7 says only "A10 V3", but **A1 D4→D3** also changes. P4→P6 says "A6 fork", but P6 is `lineage`, and in fact 8 axes (A1~A7, A11) change. P1→P2 omits A5, A9, A10, and P2→P3 omits A1, A4, A9, A11 | Change to `V1["If code artifact, A4≥frame …"]`. Replace the arrow labels with diffs generated by the tool, and change "A6 fork" on P4→P6 to "A6 lineage" |
| M-06 | docs/03:263 | "**Agent placement is the structural decision that constrains the business model most strongly**". By the tool's mean completions, the structural axis with the largest spread is A1 (23.2), with A3 second at 21.7 (1.5). A3 is first only when looking at A9 (model sourcing) alone | Narrow the scope to "constrains model sourcing (A9) most strongly", and include the table of mean completions per axis as evidence |
| M-07 | docs/02:195 (I3), docs/05:119·338-341, schemas/extension-manifest.schema.json:44-51, docs/06:318-323 | I3 says revert is "constant time, without generation", but ① reverting an extension whose state schema changed needs *reverse* state handover, while `migrate_from` expresses only the forward direction. ② Revert in a CRDT topology is not a pointer move but a merge of inverse operations. ③ The user-facing wording (8.7 "instant, free") hides that revert cannot undo external effects (a Slack message already sent) | Change I3 to "Revert of **layer state** is constant time. Extension-internal state is reset if there is no `migrate_to_prev`, and external effects are not undone", and add `migrate_to` to the manifest |
| M-08 | docs/10:40-58·62-66, docs/02:204 | ① The SBR denominator counts only "automatic merges", so the case where a human carelessly approves a broken merge in `proposed` mode (the recommended default for A7!) is not measured. ② There is no reproducibility protocol: how hidden checks are made, seeds and repetition counts, model version pinning. ③ There is no conformance test set to decide "guaranteed by design" (deferred to v0.3), so the current conformance levels are unfalsifiable | Change the SBR denominator to "automatic + approved-proposal merges" and report the two separately. Add reproducibility items to 10.2 (k runs, model and prompt hashes). Write down now, for each conformance level, at least 3 test vectors (e.g. reject if permissions grew without approval, reject if judge==generator, reject if the contract is empty) |
| M-09 | docs/03:192, tools/design_space.py:62-63 | L9 (`crdt ⇒ A7≠manual`, "CRDT merges automatically") confuses categories. A7 is **propagation from the upstream baseline downward**, while CRDT is **synchronization between replicas**. A CRDT document can still accept a new release of an upstream template manually | Delete L9, or define "under crdt, A7 means upstream template propagation" and then redo the condition |
| M-10 | docs/06:208·230, docs/02:118, examples/capability-map.example.yaml:50-55, docs/07:150 | ① In subscription sharing, each time the sender edits the feature, propagation jobs and costs arise on the recipient side. A cost attacker (07:28) can use this path, and there is no control. ② If D3 declarative components (chart, card) render remote images or URLs, that is itself egress, yet the catalog and the G1 rules have no network restrictions | Add to 6.9: "subscribe propagation cost stays within the recipient's cap, limited to n times per day". Add `fetches_remote: boolean` to the catalog schema, and require an egress capability for components that fetch remote resources |
| M-11 | docs/02:199 (I7), docs/04:103 | I7 requires only "a different instance". There is no evidence that a different instance of the same model, with the same prompt and the same context, reduces self-grading bias. The claim is unsupported | Strengthen to "a different instance + does not see the generator's reasoning or conversation history + (where possible) a different model route", and add the effect to O4 as a measurement task |
| M-12 | docs/02:54·71 | ⊕ only defines "the layer closer to the user wins". There is no means (`final`, lock) for a tenant to prevent overriding of items it must keep (regulatory notices, audit banners), so a user layer can override regulatory items | Add `overridable: false` to capability map or baseline items and reject at G0 |
| M-13 | docs/05:310-314, docs/02:106 (2.5), docs/02:194 (I2) | For D1, G2 (contract execution) is optional. So a contract required by I2 can exist yet be used as the basis for a merge (I10) without ever having been run. The D2 G5 condition "when it includes external commands" is also narrower than 7.3's "permission increase **always** needs human approval" | Make G2 mandatory for D1 too, or state that a 'never-run contract' is run first before the I10 decision. Unify all G5 cells in 5.8 as "on permission increase (I4)" |

### LOW

| # | Location | Evidence | Minimal fix |
| --- | --- | --- | --- |
| L-01 | docs/05:194-196 | The 5.4 sequence has **21** messages (:169-189). The text refers to "step 9 task spec" (actually 7), "step 12 G1" (actually 11), "steps 14~15 judging" (actually 12~13), "step 17 record" (actually 15), and "step 22 activation" (does not exist; actually 21) | Change the numbers to 7·11·12~13·15·21 |
| L-02 | tools/design_space.py:286-321, :9-14 | `--check P9` ends in a KeyError, invalid JSON ends in a traceback, and an unknown axis (`A12`) is silently accepted. The docstring usage lacks `--bm` and `--bm-stats`, and there is no self-check | Add an `extra=[k for k in c if k not in AXES]` check to `check()`. For `--check`, `if a.check not in PROFILES and a.check!="all": ap.error(...)`; wrap `json.loads` in try/except and handle it with `ap.error`. Assert the 1.1 figures with `--selftest` |
| L-03 | docs/references.md:22, :40, docs/01:17, docs/07:104, docs/09:132 | `docs/es/plugins/overview` is not cited and is the Spanish edition. 2,857 could not be checked because of the 403 (Unit 42 confirms only 341). The benchmark (AgentDojo) is missing for CaMeL. The falcao summary omits the January 9 blocking and generalizes "Agent SDK credits" | Delete the entry, or change it to `/en/` and cite it in the text. Add a link to the Koi original for the 2,857 figure. Add "on AgentDojo", and align the 9.6 sentence with the article's wording |
| L-04 | docs/04:131-143 vs examples/policy.example.yaml:23-34 | The 4.7 excerpt uses `net.allowlist` (a capability not in capability-map), but the example file uses `net.slack.post`. `currency` and `retention_days` are also missing | Make the excerpt match the example file |
| L-05 | docs/08:196, docs/glossary.md:20, examples/lexicon.ko.yaml:33-37, README:142 | The 8.9 matching table says "depth D1~D4", but the glossary and the lexicon pack's developer entry say D1~D5, and there is no `depth_d5` concept (a D5 request should appear to the user as a "core feature request"). The README list of notations is missing the E, O, T, X families | Add `depth_d5: { basic: a request that changes the app itself }` and add E1~E16, O1~O13, T0~T4, X1~X6 to README:142 |
| L-06 | docs/09:103 | It groups B8, B9, B10, B18 and says "possible in only about half", but B8 is 26.3% and B10 is 11.0% | Change to "B9 and B18 about half, B8 a quarter, B10 a tenth" |
| L-07 | docs/05:271-272, docs/05:253 | `onFailure:"block"` has no effect on `Stop` and `SubagentStop` (official docs). So E11 (refuse to stop if unverified) and E12 stay open when the hook fails (fail-open). The v2.1.295-or-later requirement is also missing | Add a footnote to the mapping table and state that E11 and E12 are "also enforced on the MCP tool side" |

---

## 3. Judgment (opinions not mechanically verified)

- **Weight of the contribution**: the design space figures are arithmetic *given this choice of rules and value resolution*. Sentences that make these figures read like empirical results ("most combinations make no sense", "the most common contradiction", "structure and business are largely separate") are grounds for rejection at a program committee. It is safer to claim the figures only as a demonstration of the internal consistency of the rule system.
- **The largest open risk is C-02, not O1.** Chapter 10 treats contract sufficiency as a 'quality' problem. But as long as the generator writes the contract, it is a *security* problem. An injected generator writes a contract that lets itself pass.
- **The tension between I8 and 'malleability'**: the honesty of downgrading enforcement on the user's device to guidance level is good. But promoting P1 and P5 as representative profiles while also promising Core conformance misleads readers. Splitting the levels (the C-03 fix) is the honest option.
- **Schema scope**: the schemas check only 'shape', while the spec's core guarantees (I4, I5, I7, I10) need cross-document checks. Yet there is nothing saying who performs these checks and where (receive-check, conformance validator). Even one small conformance validator in `tools/` before v0.2 would make "guaranteed by design" a falsifiable claim.
- **B20 (sponsored defaults)** structurally undermines the neutrality of agent recommendations. A disclosure duty alone does not stop sponsorship information in the model context from tilting recommendations. If it is included, "sponsorship information is not put into the agent context and is shown only in the UI" is safer.
- **The D3-centered interpretation (03:262)** cannot stand until H-01 is resolved. D3 mixes sandboxed and native, so the interpretation "even opening up only to declarative screens" does not match the data.
- **What was done well** (for fairness): reproducible figures, schemas and examples that pass, code-generated profile and BM matrices, 0 broken links, 23 of 24 sources reachable, the convention that "figures without a source are proposal values", the guarantee-level table in 7.8, and the disclosure of client PDP limits in 4.8. For a v0.1 draft, the structure is unusually verifiable.

---

## 4. Reproduction commands

```bash
cd mallangable-ai   # repository root
python3 tools/design_space.py --markdown
python3 tools/design_space.py --check all
python3 tools/design_space.py --bm
python3 tools/design_space.py --bm-stats
# helper scripts (outside the repository)
python3 -I /tmp/mreview/indep.py     # independent and unique violation counts, D3/D4 native counts
python3 -I /tmp/mreview/alt.py       # variant forbidding D3/D4 native
python3 -I /tmp/mreview/more.py      # per-axis completion spread, own⇒server·D3⇒decl variants, lexicon pack cross-check
python3 -I /tmp/mreview/q.py         # rule-equivalence quotient 8,969, D5 distribution
python3 -I /tmp/mreview/bmdiff.py    # BM matrix comparison, profile diff
/tmp/mreview/venv/bin/python -I /tmp/mreview/validate.py   # examples vs. schemas
/tmp/mreview/venv/bin/python -I /tmp/mreview/neg.py        # negative tests
python3 -I /tmp/mreview/xref.py      # section, link, id and URL cross-references
```
