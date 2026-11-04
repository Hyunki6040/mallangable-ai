<!-- LANG-BAR -->
**English** · [한국어](../../ko/research/prior-art-survey.md) · [简体中文](../../zh-CN/research/prior-art-survey.md) · [日本語](../../ja/research/prior-art-survey.md) · [Español](../../es/research/prior-art-survey.md)
<!-- /LANG-BAR -->

# Research note — Prior-art survey (open source, specifications, agent standards)

> Conclusion of this note: **no standard overlaps** with what this spec newly defines (contract-preserving merge, lineage propagation, range delegation, floor rights). The surrounding parts, however, are already standardized, and the spec currently either does not use their names or cites them through secondary sources. There are five things to take. ① Fix the default meaning of declarative layer composition `⊕` as **JSON Merge Patch (RFC 7396)**, and have **the schema declare** list-merge rules, as in Kubernetes Server-Side Apply. ② Add an **integrity axis** to the information-flow labels (7.5) (FIDES, CaMeL). ③ Machine-check monotonic policy narrowing (I5) with **Cedar's policy-implication verification**. ④ Align telemetry (5.11) with **OpenTelemetry GenAI attribute names**. ⑤ Reflect the latest MCP revision's (2026-07-28) **URL-mode elicitation** and the deprecation of Sampling in model connection (8.10).

- Checked on: 2026-10-30
- Method: for repositories, metadata, license files and specification sources were read with `gh api`; web documents were fetched from official sites only. No code was run. Every cited URL was confirmed to return 200 with `curl -L` (the ACM Digital Library blocks automated requests with 403, so only the DOI is given).
- Scope: this chapter does not modify existing documents. Whether to apply the edits in section 3 is decided separately.

## 0. What was checked and what was not

| Item | Status | Notes |
| --- | --- | --- |
| Latest MCP revision | Confirmed | `2026-07-28` (released 2026-07-28). Source: `docs/specification/2026-07-28/changelog.mdx` in the repository |
| MCP Apps | Confirmed | `specification/2026-01-26/apps.mdx` in `modelcontextprotocol/ext-apps`. Extension id `io.modelcontextprotocol/ui` |
| OpenTelemetry GenAI conventions | Confirmed | **Moved** from `open-telemetry/semantic-conventions` **to the `semantic-conventions-genai` repository**. All documents have status Development |
| A2UI | Confirmed | Repository moved to `a2ui-project/a2ui`. Currently v0.9.1, v1.0 is at RC |
| Cedar decision rules and verifier | Confirmed | Official documentation and the `cedar-policy-symcc` README |
| Patchwork internals | Partial | Only the project page and experiment notebook 07 were read. The `inkandswitch/patchwork-system` repository has no license notice |
| Boxer original | Not read | ACM blocks automated requests. Only the bibliographic data was confirmed |
| Licenses of Chrome, Figma and VS Code documentation | Not checked | Product documentation, so it is only cited and no wording is copied |

## 1. Survey by item

Verdict: **Adopt** = cite it and align field names and meaning / **Reference** = cite only as related work / **Not relevant** = leave out.
The "Maps to" column gives this spec's section numbers and schema files.

### 1.1 Malleable software research

| Item | What it is | Primary source | License | Maps to | Verdict |
| --- | --- | --- | --- | --- | --- |
| Malleable software essay (Ink & Switch, 2025) | An essay on reclaiming user agency from locked-down apps. Sets out the concepts of the gentle slope and the local developer | https://www.inkandswitch.com/essay/malleable-software/ | Essay (no notice) | 1.5, 2.6 | Already cited. Keep |
| Potluck (2022) | Overlays search, formulas and dynamic annotations on text to add structure gradually. Annotations are an overlay layer that does not change the original text | https://www.inkandswitch.com/potluck/ | Essay | 2.3 layers, 2.6 D1~D3 | **Reference**. A precedent for "an overlay layer that does not touch the original" |
| Embark (2023) | Puts data, computation and views together in one travel-planning document, dissolving the app | https://www.inkandswitch.com/embark/ | Essay | 10.1 O8 (tools that span apps) | **Reference** |
| Patchwork (2024~) | General-purpose version control for non-code documents such as writing and drawings. In the experiment notebook, **an AI bot edits on a branch, a person reviews the diff and merges only part of it, and the bot's edits are marked in the history** | https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/ | No notice in repository | 6.4 `exp/*` branches, 6.11 `Agent:` trailer, 8.6 receipts | **Reference**. The current "Universal Version Control" link in references.md is the lab's list page, so replacing it with the Patchwork page is more accurate |
| Cambria (2020) | Converts data between schema versions with bidirectional lenses | https://www.inkandswitch.com/cambria/ · https://github.com/inkandswitch/cambria-project | MIT | 5.9 `migrate(prev)`, `extension-manifest` `state.migrate_from` | **Reference**. The current design, which hands over state through a one-way `migrate`, is sufficient. A basis if bidirectionality becomes necessary |
| Webstrates (UIST 2015) | Synchronizes DOM changes and blurs the line between document and app. Four principles: malleability, shareability, distributability, computability | https://webstrates.net/ · https://github.com/Webstrates/Webstrates | Apache-2.0 | 6.13 risks of code on top of CRDTs | **Reference**. A precedent for sharing executable code in real time, so a good supporting case for S7 |
| Boxer (diSessa & Abelson, CACM 29(9), 1986) | A computational medium that non-experts can reconstruct | DOI 10.1145/6592.6595 | Paper | 1.5 | **Reference**. The Smalltalk lineage is excluded because no primary source was located |

### 1.2 Extension and plugin manifests

| Item | What it is | Primary source | License | Maps to | Verdict |
| --- | --- | --- | --- | --- | --- |
| VS Code contribution points and activation events | Declares extension points through `contributes` (commands, menus, views, keybindings, configuration, `languageModelTools` etc.). Since 1.74, contribution points imply activation events automatically | https://code.visualstudio.com/api/references/contribution-points · https://code.visualstudio.com/api/references/activation-events | Code MIT, docs not checked | 2.2 extension point `kind`, `capability-map` | **Reference**. Maps naturally to `kind` (token, command, view, hook, service) |
| VS Code Workspace Trust | `capabilities.untrustedWorkspaces.supported: true / false / "limited"`. An untrusted workspace opens in Restricted Mode, which blocks automatic execution | https://code.visualstudio.com/api/extension-guides/workspace-trust | Docs | 4.6 F2 safe mode, 6.9 received shares | **Reference** |
| Chrome MV3 permissions | `permissions`, `optional_permissions`, `host_permissions`, `optional_host_permissions`. **If an update adds a permission that carries a warning, the extension is disabled until the user accepts** | https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions | Docs | I4, 6.5 `delta_permissions`, 6.9 subscribe | **Reference**. A real large-scale precedent for I4. Same direction as the current spec rule (permission increase → proposal) |
| Figma plugin manifest | `networkAccess.allowedDomains` (`["none"]` allowed), `reasoning` (required for wildcards), `devAllowedDomains`, `permissions` | https://developers.figma.com/docs/plugins/manifest/ | Docs | `extension-manifest` `network.allow` | **Reference**. The "reason for allowing" field is a section 4 candidate |
| Obsidian community plugins | The official documentation states that "plugins cannot be restricted to specific permissions" and can access files, the network and program installation. Default is Restricted mode | https://obsidian.md/help/plugin-security | App proprietary, `obsidian-api` MIT | 7.6, 7.7 | **Reference**. Worth citing as a counterexample of extensions without isolation |
| WASM Component Model / WIT | A `world` declares a component's imports and exports, and the host supplies only what is imported. Packages carry versions (`wasi:http@0.2.0`) | https://component-model.bytecodealliance.org/design/wit.html · https://github.com/WebAssembly/component-model | Apache-2.0 | 7.6 object capability, `SandboxHost` `lang` adapter, manifest `permissions` | **Reference**. For `wasm` outputs, manifest `permissions` ↔ world imports can map 1:1 |
| Extism | WASM plugin framework. Manifest has `wasm[].hash`, `memory.max_pages`, `allowed_hosts`, `allowed_paths`, `config` | https://extism.org/docs/concepts/manifest · https://github.com/extism/extism | BSD-3-Clause | `extension-manifest` `artifact.content_hash`, `network.allow`, `resources.memory_mb` | **Reference**. The same concepts already exist. Weak reason to align names |
| Tauri v2 capability | Already cited | (references.md) | | 7.6 | Keep |
| Endo / SES | Already cited | (references.md) | Apache-2.0 | 7.6 | Keep |

### 1.3 Agent protocols and harness events

| Item | What it is | Primary source | License | Maps to | Verdict |
| --- | --- | --- | --- | --- | --- |
| MCP 2026-07-28 | Made stateless (`initialize` removed, version and client capabilities in `_meta` on every request), `server/discover`, multi-round-trip requests (MRTR: `resultType: "input_required"`), tasks moved to an official extension, **Roots, Sampling and Logging slated for deprecation**, `traceparent` convention in `_meta` (SEP-414) | https://modelcontextprotocol.io/specification/2026-07-28/changelog | Apache-2.0 (spec, transitioning from MIT), docs CC-BY-4.0 | 5.3 `ModelPort`, 5.6, 8.10 | **Adopt**. The 8.10 `sub` path must not be designed on top of MCP Sampling |
| MCP tool annotations | `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`. **Unless the server is trusted, the client MUST NOT trust annotations** | https://modelcontextprotocol.io/specification/2026-07-28/server/tools | Same as above | `capability-map` `capability.risk` | **Adopt**. Provide a mapping table to `risk` values (section 3, E-10) |
| MCP elicitation | Form mode and URL mode. **Secrets and credentials MUST NOT be collected in form mode; URL mode MUST be used** | https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation | Same as above | 8.10 connection key, I6 | **Adopt** |
| MCP authorization | OAuth 2.1, Protected Resource Metadata (RFC 9728), resource indicators (RFC 8707), `iss` validation (RFC 9207) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | Same as above | 2.1 delegation, 7.2 | **Reference**. Implementation basis for the I4 and I9 description of agent α as "a short-lived principal holding a human's delegation" |
| MCP Apps (SEP-1865) | `ui://` resources, `text/html;profile=mcp-app`, mandatory sandboxed iframe, `_meta.ui.csp` (`connectDomains`, `resourceDomains`, `frameDomains`, `baseUriDomains`), `permissions` (camera, microphone, geolocation, clipboardWrite) | https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx | Same as above | 3.2 A4 `frame`, `extension-manifest` `network` | Already cited. **Keep as Adopt**. Pin the link to the dated spec path |
| MCP-UI | Prototype of MCP Apps. Now an MCP Apps-compatible SDK | https://github.com/MCP-UI-Org/mcp-ui | Apache-2.0 | | **Not relevant** (MCP Apps is enough) |
| AG-UI | Agent↔frontend event protocol. `RUN_STARTED`/`RUN_FINISHED`/`RUN_ERROR`, `STEP_*`, `TOOL_CALL_*`, `STATE_SNAPSHOT`/`STATE_DELTA` (**RFC 6902 JSON Patch**), `SUBAGENT_*`. Human approval is a new run with `resume[]` after `outcome: { type: "interrupt" }` in `RunFinished` | https://docs.ag-ui.com/concepts/events · https://docs.ag-ui.com/concepts/interrupts · https://github.com/ag-ui-protocol/ag-ui | MIT | 5.6 event model, 8.5 progress display, 2.8 `pending approval` | **Adopt** (mapping table). Usable as is as the transport between the experience plane and the generation plane |
| A2A v1.0 | Task protocol between opaque agents. `AgentCard`, task states `TASK_STATE_SUBMITTED / WORKING / INPUT_REQUIRED / AUTH_REQUIRED / COMPLETED / FAILED / CANCELED / REJECTED` | https://a2a-protocol.org/latest/specification/ · https://github.com/a2aproject/A2A | Apache-2.0 | 5.3 `JobOrchestrator`, 2.8 lifecycle | **Reference**. Adapter candidate for handing server merge and promotion jobs to external agents |
| OpenTelemetry GenAI conventions | `gen_ai.operation.name` (`invoke_agent`, `execute_tool`, `create_agent`, `invoke_workflow`), `gen_ai.agent.id`, `gen_ai.usage.input_tokens`, `output_tokens`, `gen_ai.tool.name`, MCP attribute `mcp.method.name`. **Status Development** | https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/ | Apache-2.0 | 5.11 telemetry | **Adopt** (attribute names only). Not a stable release, so the version must be pinned |
| OpenAI Agents SDK tracing | trace (`workflow_name`, `trace_id`, `group_id`), span (`agent`, `generation`, `function`, `guardrail`, `handoff`, `custom`), `trace_include_sensitive_data` | https://openai.github.io/openai-agents-python/tracing/ · https://github.com/openai/openai-agents-python | MIT | 5.11, 7.5 declassification rule | **Reference**. Including sensitive data by default (True) is the opposite of this spec's default |
| Claude Code hooks | 32 events, 5 handler types (`command`, `http`, `mcp_tool`, `prompt`, `agent`), `permissionDecision` (`allow`, `deny`, `ask`, `defer`) and `updatedInput` on `PreToolUse`, managed setting `allowManagedHooksOnly` | https://code.claude.com/docs/en/hooks.md | Product docs | 5.6 mapping table | Already cited. `PostToolUseFailure` (E5) and `Elicitation` (E6) can be added to the mapping table |
| Claude Code plugins | `.claude-plugin/plugin.json` (only `name` required; `skills`, `hooks`, `mcpServers`, `sensitive` in `userConfig`), `claude plugin validate` | https://code.claude.com/docs/en/plugins-reference | Product docs | 5.6 harness distribution, 8.10 `sub` | Already cited. **The references.md link is the Spanish edition (`/docs/es/`); replace it with the English reference** |
| Agent Skills specification | `SKILL.md` front matter `name` (64 characters), `description` (1024 characters), `license`, `compatibility`, `metadata`, `allowed-tools` (**Experimental**) | https://agentskills.io/specification · https://github.com/agentskills/agentskills | Apache-2.0 | 5.6 "skills are procedure, the harness is enforcement" | **Adopt**. The current basis is a secondary source (Shiplight), so replace it with the primary spec. The claims match the primary source |

### 1.4 Policy engines and prompt-injection defenses

| Item | What it is | Primary source | License | Maps to | Verdict |
| --- | --- | --- | --- | --- | --- |
| Cedar | Requests of principal, action, resource and context. **forbid beats permit, and Deny if no permit matches**. The response contains the ids of the policies that produced the decision (determining policies) and a list of errors. Policies that error are skipped | https://docs.cedarpolicy.com/auth/authorization.html · https://github.com/cedar-policy/cedar | Apache-2.0 | 4.8 `decide(req)`, `PolicyDecisionPoint` | **Adopt** (PDP adapter) |
| Cedar SymCC | Translates policy sets to SMT and verifies **implication (`check_implies`), equivalence, always-deny and never-errors**, with counterexamples. The verifier is formally verified in Lean | https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc | Apache-2.0 | **I5 `p_child ⊑ p_parent`** | **Adopt**. Raises I5 from a "policy store check" to a provable check |
| OPA / Rego | CNCF graduated project. Decision logs carry `decision_id`, `bundles.revision`, `path`, `input`, `result`, `erased`, `masked` (JSON Pointer), `trace_id`, `span_id` | https://www.openpolicyagent.org/docs/management-decision-logs · https://github.com/open-policy-agent/opa | Apache-2.0 | 5.11, 7.9 pseudonymization | **Adopt** (decision-log field names). As a policy language it is less analyzable than Cedar, so it is not the first choice for the PDP |
| CaMeL (DeepMind 2025) | Already cited. Code is public | https://github.com/google-research/camel-prompt-injection | Apache-2.0 | 7.4 | Keep. Add the code link |
| FIDES (Microsoft 2025) | The planner tracks **confidentiality and integrity labels** with dynamic taint tracking and enforces policy deterministically. Presents primitives for selectively hiding information | https://arxiv.org/abs/2505.23643 · https://github.com/microsoft/fides | Notebooks MIT | **7.5 information-flow labels** | **Adopt**. 7.5 has only confidentiality (V0~V3) and no integrity axis |
| Dual LLM pattern (Willison 2023) | A privileged LLM and a quarantined LLM, with a non-LLM controller between them. Untrusted values are passed only as references such as `$VAR1` | https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | Blog | 7.3 quarantined reader | **Adopt** (citation). 7.4 currently cites it indirectly through the design-patterns paper |
| Lethal trifecta (Willison 2025) | Already cited | | | 7.3 | Keep |

### 1.5 Merge and lineage

| Item | What it is | Primary source | License | Maps to | Verdict |
| --- | --- | --- | --- | --- | --- |
| JSON Merge Patch (RFC 7396) | Object keys are overwritten, `null` deletes, **arrays are replaced wholesale** | https://www.rfc-editor.org/rfc/rfc7396 | IETF Trust | **2.3 `⊕`**, 6.6 R2 | **Adopt**. The "per-key override" of `⊕` is exactly this meaning, but it has no name |
| JSON Patch (RFC 6902) | List of operations (add, remove, replace, move, copy, test) | https://www.rfc-editor.org/rfc/rfc6902 | IETF Trust | 8.5 partial preview, AG-UI `STATE_DELTA` | **Reference** |
| Kubernetes Server-Side Apply | Field managers record field ownership (`managedFields`). With the schema markers `x-kubernetes-list-type: atomic / set / map`, `x-kubernetes-list-map-keys` and `x-kubernetes-map-type: atomic / granular`, **the schema declares** the merge strategy. Changing a field owned by another manager is a conflict | https://kubernetes.io/docs/reference/using-api/server-side-apply/ | Docs | **6.6 R2** "the schema declares the rule", 6.11 `Overrides:` | **Adopt**. R2 only states it and has no schema field |
| Kustomize | base, overlay, component. A component is a reusable feature bundle mixed into several overlays. `patches` are strategic merge and JSON 6902 | https://kubectl.docs.kubernetes.io/guides/config_management/components/ · https://github.com/kubernetes-sigs/kustomize | Apache-2.0 | 6.2 lineage, 6.9 per-feature sharing | **Reference**. A practical precedent for "overlays on a baseline" |
| Automerge | CRDT. Concurrent writes to the same key pick a deterministic winner by operation id, but **the losing values are preserved via `getConflicts()`** | https://automerge.org/docs/reference/documents/conflicts/ · https://github.com/automerge/automerge | MIT | 6.13 CRDT semantic conflicts | **Reference**. The current 3.2 A6 link is the Ink & Switch list page, so change it to Automerge |
| Yjs | CRDT shared types | https://yjs.dev/ · https://github.com/yjs/yjs | MIT | 3.2 A6 `crdt` | **Reference** |
| Mergiraf | Syntax-aware merge driver based on tree-sitter | https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf | **GPL-3.0-only** (`Cargo.toml`) | 6.6 R1 | Already cited. Change the link from docs.rs to the official site and state the license. The actual subject of the "strong copyleft" warning in 6.6 |

### 1.6 Generative UI

| Item | What it is | Primary source | License | Maps to | Verdict |
| --- | --- | --- | --- | --- | --- |
| A2UI v0.9.1 | Declarative JSON UI. Four message types `createSurface`, `updateComponents`, `updateDataModel`, `deleteSurface`. Each surface pins a **`catalogId`** (URI-formatted string). Renders only approved catalog components | https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md | Apache-2.0 | 2.6 D3, `capability-map` `catalog`, 8.5 | **Adopt**. The current basis is a news article (The Decoder), so replace it with the primary source |
| json-render (Vercel Labs) | The AI generates UI only within a catalog (component props defined with zod). Progressive rendering | https://json-render.dev/ · https://github.com/vercel-labs/json-render | Apache-2.0 | 2.6 D3, `capability-map` `catalog.props_schema` | **Reference**. The same design: catalog = approved list |

### 1.7 Supply chain

| Item | What it is | Primary source | License | Maps to | Verdict |
| --- | --- | --- | --- | --- | --- |
| in-toto Attestation | A signed Statement framework made of a subject digest + predicate type | https://github.com/in-toto/attestation | Apache-2.0 | 7.7 "publisher provenance signature" | **Adopt** (specifies the format) |
| SLSA Provenance v1 | `predicateType: https://slsa.dev/provenance/v1`. `buildDefinition` (`buildType`, `externalParameters`, `resolvedDependencies`), `runDetails.builder.id` | https://slsa.dev/spec/v1.1/provenance | Community Specification License 1.0 | 7.7, `change-record` `provenance` | **Adopt**. Treating the harness as the builder gives a provenance attestation for shared features |

## 2. Gap table — what the spec lacks and prior art has solved

| # | Missing concept | Current spec | Prior-art solution | Applied in |
| --- | --- | --- | --- | --- |
| P1 | Exact meaning of declarative layer composition | 2.3 says only "for the same key, the later layer overrides". Array and deletion semantics undefined | RFC 7396: `null` deletes, arrays replaced wholesale | E-3 |
| P2 | Merge rules declared by the schema | 6.6 R2 only says "the schema declares the rule" and has no field | SSA `list-type: map` + `list-map-keys`, `map-type: atomic/granular` | E-4 |
| P3 | Integrity label | 7.5 has only confidentiality V0~V3 | FIDES, CaMeL: integrity tracking so untrusted values cannot influence action selection | E-1 |
| P4 | Machine verification of monotonic policy narrowing | I5 enforcement point "policy store check" (no method) | Cedar SymCC `check_implies`, `check_never_errors` | E-2 |
| P5 | Standard record of decision grounds | 4.8 "reason = (k, the layer that set the ceiling)" | Cedar determining policies, OPA decision log `decision_id`, `bundles.revision`, `erased`, `masked` | E-2, E-5 |
| P6 | Common telemetry vocabulary | 5.11 uses its own names such as `tokens_in`, `tokens_out` | OTel `gen_ai.usage.input_tokens` etc., MCP `_meta.traceparent` | E-5 |
| P7 | Experience-plane transport | 5.6 covers only harness-side events. Nothing says how the experience plane receives progress and pending approval | AG-UI events and interrupt, A2A `INPUT_REQUIRED`, MCP MRTR | E-6 |
| P8 | Secret input path | 8.10 says only "keys go in secure storage". The case of receiving them through the agent conversation path is undefined | MCP URL-mode elicitation (MUST) | E-7 |
| P9 | D3 catalog identity and version | `capability-map.catalog` has only a list, with no id or version | A2UI `catalogId` | E-8 |
| P10 | Capability ↔ agent tool hints | Only `capability.risk` | MCP `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` | E-9 |
| P11 | Provenance attestation format for shared items | 7.7 "publisher provenance signature" (no format), manifest `content_hash` | in-toto Statement + SLSA provenance | E-10 |
| P12 | Reason for network allowance | Only the `network.allow` list | Figma `networkAccess.reasoning` | Section 4 (deferred) |

## 3. Proposed edits (by priority, at most 12)

Each item is a minimal edit. The schema items are all **additions of optional fields**, so `required` does not change and the existing `examples/*.yaml` should still pass. After applying them, rerun the example validation.

### E-1. Add an integrity axis to 7.5 (P3)

- File: `docs/07-trust-and-security.md`, the `label λ = (scope, grade)` code block in 7.5 and the example paragraph below it
- Proposed wording (replaces the code block):

```text
label λ = (scope, grade, integrity)
  scope     : tenant / org / user identifier
  grade     : V0 aggregate < V1 metadata < V2 description < V3 code          # confidentiality
  integrity : trusted (human intent, verified baseline) > untrusted (shared items, external documents, values a model produced after seeing untrusted input)

derivation rule:     λ(f(x, y)) = λ(x) ⊔ λ(y)          # confidentiality takes the more sensitive side, integrity the lower side
viewing rule:        viewer s may see x  ⇔  λ(x) ⊑ permission(s)
action rule:         values that decide a permission increase, an external send or the choice of an extension point must have integrity trusted
declassification:    only the output gate (declassifier) may lower a label, and it leaves a rule and a record
```

- Sentence to add: `The integrity axis follows the approach of FIDES (Costa et al., 2025), which tracks confidentiality and integrity labels together at the planner level and enforces policy deterministically. It writes 7.4's "plan, then execute" as a label rule.`
- references.md (end of "## Agent security"):

```markdown
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · Notebooks (MIT): https://github.com/microsoft/fides
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
```

### E-2. Add a PDP adapter and I5 machine verification to 4.8 (P4, P5)

- File: `docs/04-control-spectrum.md`, end of the "Placement principles" list in 4.8
- Proposed wording:

```markdown
- **Policy engine adapter** (MAY): the PDP can be implemented by translating knob ranges into a policy language. In Cedar, forbid beats permit, the request is denied if no permit matches, and the ids of the policies that produced the decision are returned with it. Use these ids as the grounds for `deny(reason, layer)` and for the receipt (8.6).
- **I5 machine verification** (SHOULD): check `p_child ⊑ p_parent` when a policy is stored. If translated to Cedar, SymCC's implication check (`check_implies`) can prove it, with counterexamples. Run the same tool's `check_never_errors` as well. Cedar skips policies that hit evaluation errors, so a forbid that errors silently stays open.
- **Floors before the engine**: because of the forbid-first rule, if the floor rights (F1~F7) are entered as ordinary permits, a higher forbid can erase them. As in the pseudo-code above, place the `FLOOR_ACTIONS` decision before the engine call.
```

- references.md (new section "## Policy engines", before "## Merging"):

```markdown
## Policy engines

- Cedar authorization semantics (forbid first, default deny, determining-policy diagnostics). https://docs.cedarpolicy.com/auth/authorization.html · Code (Apache-2.0): https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler (SymCC): verification of policy implication, equivalence and never-errors. https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Open Policy Agent decision logs. https://www.openpolicyagent.org/docs/management-decision-logs
```

### E-3. Fix the default meaning of `⊕` in 2.3 as RFC 7396 (P1)

- File: `docs/02-core-model.md`, the `⊕` item in 2.3
- Current: `` `⊕` (layer composition): when the same key is touched, the later layer **overrides** the earlier one. Declarative data is composed per key, code extensions per extension-point slot. ``
- Proposed: `` `⊕` (layer composition): when the same key is touched, the later layer **overrides** the earlier one. The default meaning for declarative data is JSON Merge Patch (RFC 7396). Objects are overwritten per key, `null` deletes that key, and arrays are replaced wholesale. To merge arrays item by item, the extension point's schema must declare a merge key (6.6 R2). Code extensions are composed per extension-point slot. ``
- Note: to keep the associativity requirement on the next line ("pre-merge and cache the baseline"), layers merged in advance must keep `null` (the deletion marker) rather than drop it. Only then does applying the merged layer later give the same result as applying them one by one. Confirm with a small example before applying.
- references.md ("## Merging"):

```markdown
- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
```

### E-4. Add a merge-rule field to `capability-map` extension points (P2)

- File: `schemas/capability-map.schema.json`, in `$defs.extensionPoint.properties` after `output_schema`
- Proposed field:

```json
"merge": {
  "type": "object",
  "description": "Rules for merging this point's declarative outputs across layers (spec 2.3, 6.6 R2). Keys are JSON Pointers into the output. Arrays without a declaration are atomic",
  "propertyNames": { "pattern": "^(/[^/]*)*$" },
  "additionalProperties": {
    "type": "object",
    "required": ["strategy"],
    "additionalProperties": false,
    "properties": {
      "strategy": { "type": "string", "enum": ["atomic", "set", "map"] },
      "keys": { "type": "array", "items": { "type": "string" }, "minItems": 1, "description": "Field names that identify items when strategy=map" }
    }
  }
}
```

- Wording to append after the "Example" cell of the 6.6 R2 table row: `(Schema field: extension_points[].merge in capability-map. Value names follow Kubernetes Server-Side Apply's x-kubernetes-list-type)`
- references.md ("## Merging"):

```markdown
- Kubernetes. *Server-Side Apply* (field ownership, `x-kubernetes-list-type` and `x-kubernetes-list-map-keys` merge markers). https://kubernetes.io/docs/reference/using-api/server-side-apply/
```

### E-5. Align 5.11 telemetry names with OTel GenAI and OPA (P5, P6)

- File: `docs/05-reference-architecture.md`, the JSON example in 5.11 and the paragraph below it
- Proposed: replace `"model_cost"` in the JSON with the following, and add a `"policy"` key.

```json
  "gen_ai": {"operation.name": "invoke_agent", "agent.id": "builder@harness-x", "usage.input_tokens": 18200, "usage.output_tokens": 2100},
  "model_cost": {"unit_cost_ref": "route:standard"},
  "policy": {"decision_id": "dec_7Q2…", "revision": "tenant/acme@42"},
  "trace": {"traceparent": "00-…-…-01"},
```

- Sentence to add: `Model usage attributes follow the names of the OpenTelemetry GenAI semantic conventions. These conventions are still in Development status, so implementations also record the convention version they follow. Policy decisions leave a decision id and policy revision, as in OPA decision logs, and fields erased by pseudonymization are marked as a list of JSON Pointers (7.9). Calls that pass through an MCP server are tied into the same trace with the traceparent convention in MCP `_meta`.`
- references.md (new section "## Observability", before "## Experience design"):

```markdown
## Observability

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/
```

### E-6. Add an experience-plane transport mapping table to 5.6 (P7)

- File: `docs/05-reference-architecture.md`, after the "### Mapping example: Claude Code hooks" table, before the "Caution:" paragraph
- Proposed wording:

```markdown
The experience plane does not receive harness events as they are; it receives user-facing progress signals. With AG-UI as the transport, the mapping is as follows.

| Mallangable | AG-UI | Notes |
| --- | --- | --- |
| E2 intake ~ E11 end | `RUN_STARTED` · `RUN_FINISHED` · `RUN_ERROR` | |
| The four status words (8.5) | `STEP_STARTED` · `STEP_FINISHED` | Fix the step name to the status-word id |
| Partial preview (8.5) | `STATE_SNAPSHOT` · `STATE_DELTA` (RFC 6902) | Keep the "not yet checked" indicator |
| E6 `permission.request`, 2.8 `pending approval` | `outcome.type = "interrupt"` in `RUN_FINISHED` → `resume[]` of the next run | Approval continues as a new run |

When server jobs are handed to external agents, A2A task states (`TASK_STATE_INPUT_REQUIRED`, `TASK_STATE_AUTH_REQUIRED`) fill the same role; inside MCP tools, multi-round-trip requests (`resultType: "input_required"`) do. `PostToolUseFailure` (E5) and `Elicitation` (E6) can also be added to the Claude Code mapping table.
```

- references.md ("## Generative UI and extension standards"):

```markdown
- AG-UI: Agent-User Interaction Protocol (events, interrupt). MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
```

### E-7. Add a secret-input rule for the MCP path to 8.10 (P8)

- File: `docs/08-experience-design.md`, after the first item of "### Security and cost display" in 8.10
- Proposed wording:

```markdown
- When running as an MCP tool inside an official assistant, as on the `sub` path, connection keys and external service tokens are not collected through the conversation or form-mode input. The MCP specification requires URL-mode elicitation for secrets and credentials (2026-07-28 revision). I6 holds only if the key never once enters the agent's context.
- In the same revision, MCP Sampling is slated for deprecation. Do not build a `ModelPort` adapter that offloads model calls to the MCP client.
```

- references.md ("## Generative UI and extension standards"):

```markdown
- Model Context Protocol specification 2026-07-28 (changes, tool annotations, elicitation). https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
```

### E-8. Add a catalog id and version to `capability-map` (P9)

- File: `schemas/capability-map.schema.json`, in top-level `properties` before `catalog`
- Proposed field:

```json
"catalog_id": {
  "type": "string",
  "description": "D3 catalog identifier. A URI-formatted string that need not be downloadable. When the catalog contents change, the value changes too (same meaning as A2UI catalogId)",
  "examples": ["https://todo.example/catalogs/v3"]
}
```

- Also add to: `artifact.properties` in `schemas/extension-manifest.schema.json`: `"catalog_id": { "type": "string", "description": "The catalog a D3 output assumes. Rejected at G1 if it differs from the capability map's catalog_id" }`
- references.md: replace the `Google A2UI coverage. The Decoder.` line in "## Generative UI and extension standards" with the following.

```markdown
- A2UI: Agent-to-User Interface specification v0.9.1 (`createSurface`, `catalogId`). Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
```

### E-9. Map `capability-map` capabilities to MCP tool hints (P10)

- File: `schemas/capability-map.schema.json`, the `description` of `$defs.capability.properties.risk`
- Current: `"egress=external send, sensitive=other people's or sensitive data"`
- Proposed: `"egress=external send, sensitive=other people's or sensitive data. When a capability is exposed as an MCP tool, export read as readOnlyHint=true and egress as openWorldHint=true. MCP annotations received from the other side are not trusted; this value is authoritative (I8)"`
- Add one optional field: `"destructive": { "type": "boolean", "description": "Irreversible write. Same meaning as MCP destructiveHint. If true, G5 regardless of the activation policy" }`
- Add `· when an irreversible-write (destructive) capability is used` to the "Content" cell of the 5.8 G5 row.
- references.md: list `https://modelcontextprotocol.io/specification/2026-07-28/server/tools` together with the MCP specification entry from E-7.

### E-10. Specify the provenance attestation format in 7.7 supply chain (P11)

- File: `docs/07-trust-and-security.md`, the "Control" cell of the `One account uploaded in bulk` row in the 7.7 control table
- Current: `Publisher provenance signature, limits on new publishers, curation tier`
- Proposed: `Publisher provenance signature (SLSA provenance predicate in an in-toto Statement. The subject is the manifest content_hash, builder.id is the harness id), limits on new publishers, curation tier`
- references.md (end of "## Agent security" or a new section "## Supply chain"):

```markdown
- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance
```

### E-11. Strengthen 1.5 related work with malleable-media precedents

- File: `docs/01-introduction.md`, after the first row (Malleable software) of the 1.5 table
- Proposed row:

```markdown
| Computational media and dynamic documents (Boxer, 1986 · [Webstrates](https://webstrates.net/), 2015 · [Potluck](https://www.inkandswitch.com/potluck/), 2022 · [Embark](https://www.inkandswitch.com/embark/), 2023) | Remove the line between document and app, and let users layer computation on top | Overlay layers that do not touch the original (2.3), tools that span apps (O8) | Defined on top of existing commercial apps, as a structure that survives vendor updates |
```

- In the same table, change the link in the Local-first row to `https://www.inkandswitch.com/project/patchwork/`, and append `· AI edits kept on a branch, with a person choosing what to merge (Patchwork experiment notebook)` to the "What we took" cell.
- references.md ("## Malleable software and end-user programming"):

```markdown
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · Code (Apache-2.0): https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck: Dynamic documents as personal software.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark: Dynamic documents for making plans.* 2023. https://www.inkandswitch.com/embark/
- Ink & Switch. *Patchwork* (experiment notebook 07 "AI bots in version control"). https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
```

- Note: the Potluck and Embark subtitles must be checked once more against the originals before copying the page titles as is (they were read through a summarization tool).

### E-12. Replace secondary sources in references.md with primary sources

- File: `docs/references.md`
- Lines to change:

| Current | Replacement |
| --- | --- |
| `Agent Skills standard overview. Shiplight, 2026. https://www.shiplight.ai/blog/agent-skills` | `Agent Skills specification (SKILL.md front matter, allowed-tools is Experimental). Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills` |
| `Claude Code plugins overview. https://code.claude.com/docs/es/plugins/overview` | `Claude Code plugin manifest reference. https://code.claude.com/docs/en/plugins-reference` |
| `Mergiraf: syntax-aware Git merge driver. https://docs.rs/crate/mergiraf/latest` | `Mergiraf: syntax-aware Git merge driver. GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf` |
| `SEP-1865. *MCP Apps …* https://modelcontextprotocol.io/seps/1865-…` | Keep it and append ` · Specification (2026-01-26): https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx` |
| CaMeL entry | Append ` · Code (Apache-2.0): https://github.com/google-research/camel-prompt-injection` |

- Change the body links as well: in 5.6 `[Shiplight, 2026]` → `[Agent Skills specification](https://agentskills.io/specification)`, the A2UI and Agent Skills links in 1.5, the Automerge link in 3.2 A6 → `https://automerge.org/docs/reference/documents/conflicts/`, the Mergiraf link in 6.6 R1 → `https://mergiraf.org/`.
- Update `Checked on` to the date the edits are applied.

## 4. What was left out

- **A Figma `networkAccess.reasoning`-style reason-for-allowing field (P12)**: useful, but the party that writes `network.allow` today is the generation agent, not a person. A reason written by the agent cannot serve as grounds on an approval card. Revisit when designing the approval card (G5).
- **Aligning with WIT and Extism field names**: the same concepts are already in the manifest, and the alignment would serve a single output format (`wasm`). A mapping table is enough when writing the D4 `lang` adapter documentation.
- **VS Code activation events**: lazy loading is a runtime implementation matter, unrelated to contracts and merging. The G3 startup-time budget serves the same purpose.
- **Chrome-style `optional_permissions`**: "request when needed" is already expressed by the I4 human approval flow (E6). Adding one more static declaration would split it into two paths.
- **OPA as the default PDP**: take its decision-log format, but Cedar, which supports I5 implication verification, fits this spec's monotonicity requirement better.
- **Separate alignment with MCP-UI and Yjs**: citing MCP Apps and Automerge respectively is enough.
- **Smalltalk lineage**: no primary source was located. Citing it requires checking the original papers.
