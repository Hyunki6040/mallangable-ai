<!-- LANG-BAR -->
**English** · [한국어](../../ko/research/security-audit-2026-11-05.md) · [简体中文](../../zh-CN/research/security-audit-2026-11-05.md) · [日本語](../../ja/research/security-audit-2026-11-05.md) · [Español](../../es/research/security-audit-2026-11-05.md)
<!-- /LANG-BAR -->

# Security audit report — 2026-11-05

Tool: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) (`.claude/skills/security-audit/`, pinned to the `UPSTREAM` commit)

## 1. Scope of the run

- Profile: **quick**, a partial audit. Only one hunt and one final coverage critique were run, and the 6 units the critique found were left as `deferred` (`quick_profile_final_critic`). No claim of full coverage is made.
- Target: the whole repository, source at `a69ddbf`. This is the first audit, so there are no prior results.
- Budget: none set separately. There were 11 agents in total: 1 recon, 5 hunt, 4 verification, 1 critique. One verification (`v-propagate`) returned results in the wrong format, so it was discarded and redone with a new verifier.
- Execution boundary: target code ran only inside Docker. The conditions were `--network none`, target read-only, uid 65534, `cap-drop ALL`, 256 MiB, 60 seconds, `env -i`, and writes were allowed only to each agent's scratch. Outputs were moved only through a parent-side no-follow promoter. No deployment environment or external service was touched.

## 2. Summary

This is a specification repository, so there is no running server. There are two real boundaries: (a) the checker tools that take external documents, and (b) normative pseudo-code that implementers will copy as is. Both confirmed defects are low. One defect was judged to need further validation, and its dependency was closed with spec text in this revision.

## 3. Confirmed defects

| Severity | Title | Boundary | Observed result |
| --- | --- | --- | --- |
| low | The floor action exception in `decide()` does not look at the actor or direction | agent or other-layer actor → PDP active state transition | for the same state S1, `activate` is denied (depth), `revert(target=S1)` is allowed [log] |
| low | `check_schemas.py` prints control characters in document keys and file names as is | external document author → checker terminal and CI log | 2 raw ESC bytes, a standalone `::error title=forged::` line produced. The exit code stays 1 |

### 3.1 Scope of the floor action exception (`docs/04-control-spectrum.md:153`)

- Lower-trust actors: a delegated agent (prompt-injectable), a watcher, a user of another layer.
- Reproduction: the 4.8 pseudo-code was copied as is. The policy is depth ceiling D3, permissions `[tasks.read]`, `gated`, and the recorded state S1 has `net.slack.post` at D4. The result is `activate(S1)` returning `('deny','depth')` and `revert(target=S1)` returning `('allow',['log'])` regardless of the actor.
- Condition: it holds when the host implements 4.8 as is and `revert` accepts an arbitrary StateId and is also used as redo (5.5). Whether the runtime broker's per-call PDP check blocks actual permission use depends on the implementation, so no claim is made about it.
- Impact: this state transition skips the tenant ceiling, G5, and hold re-validation. It contradicts I4 and 5.4 (E10).
- Fix (this revision): added `floor_scoped(req)`. A request counts as a floor action only when it satisfies all of: human owner, own layer, previous state, and no increase in permissions or depth. Any other `revert` goes through the same decision via `as_activate`. A `uses_destructive` branch was also added, and the same rule was written into 5.5 and 7.11.

### 3.2 Checker tool output injection (`tools/check_schemas.py:29`, `:26`)

- Lower-trust actor: the author of an external document or file name passed to the `check_schemas.py <schema> FILE` command.
- Reproduction: a `concepts` key in a lexicon-pack was crafted as `"x\e]0;PWNED\a\e[2K\rOK   forged.yaml[0]\n::error title=forged::…"`. This key went into `json_path` unchanged and was printed.
- Impact: only output and logs are forged (window title, a fake `OK` line, a GitHub Actions annotation). The verdict, exit code, files, and credentials are unaffected.
- Fix (this revision): every printed string goes through `safe()` (repr escaping, truncation at 300 characters). One assert was added as a regression check. Rerunning in the sandbox gave 0 ESC bytes and 0 `::` lines.

## 4. Needs further validation

| Title | Location | Blocker | Status |
| --- | --- | --- | --- |
| Automatic apply in baseline propagation checks only for no permission change | `docs/06-versioning-and-lineage.md:121-122` | the spec did not define whether `apply(merged)` goes through `ChangeStore.activate` (E10) | defined by the spec owner in this revision: automatic apply also goes through `activate()`, and becomes PROPOSED if approval is required. `delta_permissions` is recomputed |

The first verifier dismissed this item. Its rationale was that activation always goes through the PDP per 05:150, 05:205, and 07:77. But its result had a format error, so it was discarded per the rules, and the new verifier treated the absence of any sentence tying 06:122 to `activate` as a blocker and judged it `needs_validation`. Both readings reach the same conclusion that 6.5 needs an explicit sentence, so that sentence was added.

## 5. Hardening notes (not defects, whether applied)

- Applied: a change-record deterministic contract must have at least one executable form. Records with only descriptive forms are now rejected.
- Applied: `permissions_delta` is recomputed, and `approved_by` is a human actor and must differ from `agent`. Added to the schema description and 7.11.
- Applied: `network.allow` and policy `allowlist` reject IP literals. Public-suffix wildcards, presence of the egress permission, and `setKnob` default ⊆ ceiling were written as conformance validator MUSTs, and regression cases expecting `False` were added.
- Applied: YAML aliases and files over 1 MiB are rejected. The problem of a 555 B alias bomb producing 75.5 MB of output and the OOM on a 601 B input are gone. Per-document exceptions are isolated (non-string keys).
- Applied: `design_space.py --profile` and `--check` exit with code 1 on a failing verdict, and reject duplicate keys and non-object JSON.
- Applied: CI `permissions: contents: read`. `net.allowlist` in the 4.7 excerpt was corrected to `net.slack.post` (L-04).
- Not applied (proposals): pin Actions to commit SHAs, pin `requirements.txt` hashes, define the meaning of capability id `*`, make `content_hash` mandatory on sharing, an approval fingerprint field.

Positive patterns: use of `yaml.safe_load`. A regression structure that exposes cross-document rules as `ACCEPTED (validator MUST check)`. Enforcement of the depth-to-form mapping in three places.

## 6. Coverage

17 units in the ledger: covered 8 · candidate 3 (all with final verdicts) · blocked 0 · deferred 6.

Units the final critique found and deferred:
1. Binding approvals and consent to the recomputed permission change, content_hash, and `Contract-Migrated` consent
2. Capability id `*` and per-call PDP versus grant at mount time
3. The `check_schemas.py` OK verdict and differences in the YAML→JSON data model (non-string keys, duplicate keys)
4. Release signature pinning, revocation, downgrade
5. R3 resolution cache poisoning (Sybil nodes within the same tenant)
6. 7.3 role separation and the 7.5 label action rule (indirect injection)

The next audit should use the standard profile and start with these 6.
