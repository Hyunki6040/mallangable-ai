<!-- LANG-BAR -->
**English** · [한국어](../../ko/research/harness2-analysis.md) · [简体中文](../../zh-CN/research/harness2-analysis.md) · [日本語](../../ja/research/harness2-analysis.md) · [Español](../../es/research/harness2-analysis.md)
<!-- /LANG-BAR -->

# Research note — Harness² (google-research/harness2)

> Conclusion of this note: Harness² is **a research framework that rewrites the harness itself for each task**. Mallangable's harness (5.6) is an outer shell that wraps the agent and *enforces* rules, so the two point in different directions. Three things can be taken over as they are. First, **an isolation mechanism that keeps scoring information out of the method-side context entirely**. Second, **a reporting rule that treats a scoring failure as unscored, not as a score of 0**. Third, **judging with the candidate's source hidden**. All three strengthen Mallang-Bench (10.2) and G4 (5.8). Conversely, we do not accept self-editing in which the agent also modifies policy hooks and guardrails.

- Checked on: 2026-10-30
- Subject: https://github.com/google-research/harness2 (public repository, existence confirmed)
- Pinned commit: `1cfe254e8d25b15f37048c3730134686abe60335` (2026-10-13). All source links below refer to this commit.
- Method: fetched with `git clone --depth 1` into an empty temporary directory and **only read** it (no code was run). The paper was read from the arXiv abstract page and the HTML full text fetched over the web.
- Notation: `B` = `https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335`

## 0. What was checked and what was not

| Item | Status | Basis |
| --- | --- | --- |
| Repository exists and is public | Confirmed | `gh repo view google-research/harness2`, clone succeeded |
| License | Confirmed | [`LICENSE`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/LICENSE) Apache 2.0, [`pyproject.toml`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/pyproject.toml#L9) `license = "Apache-2.0"` |
| Core sources (`harness2/core/*`, `substrate/*`) | Read directly | Links in the body |
| Paper | Existence and abstract confirmed, part of the body checked | [arXiv:2610.14224](https://arxiv.org/abs/2610.14224), submitted 2026-10-09. The body was read from HTML through a summarization tool, so **section numbers and quotations must be re-checked against the original PDF** |
| Project site | Existence confirmed | https://harness2.github.io (linked from the README) |
| Google Research blog post | **Not found** | No blog link on the site, in the README or in the paper |
| Reproduction of experimental figures | Not done | It costs model calls and is outside the scope of this survey |
| Full text of `prompts.py` (1,163 lines) | Partly read | Only the isolation instructions and the INV/DOM sections were checked |
| Benchmark adapters (`benchmarks/*.py`) | Not read | Glue code unrelated to the methodology |

## 1. What Harness² is

### 1.1 Purpose

The README defines a harness as "the surrounding system that makes a model act as an agent (prompts, tools, memory, skills, orchestration, etc.)", and *harnessing* as the process of optimizing that system ([README L19-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L19-L21)). Harness² modifies the harness through two levels of recursion **while keeping the model weights fixed** ([README L23-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L23-L33)).

- **Task-level recursion**: refines the execution harness of the current task through contrastive **Propose–Probe–Compose** steps. It uses no ground-truth feedback, only behavioral contrasts between runs.
- **Harnessing-level recursion**: accumulates the harness adopted for each task and lessons backed by evidence into a persistent *improvement harness* (library) for use on later tasks.

The paper's abstract gives two motivations. Open-world tasks are unseen at design time, so **there is no ground-truth verifier**, and existing recursive self-improvement is task-specific and does not generalize ([arXiv abstract](https://arxiv.org/abs/2610.14224)).

### 1.2 Structure and core abstractions

| Abstraction | Definition | Source |
| --- | --- | --- |
| Separation of three axes | Does not mix method (recursion, prompts, selection, library), substrate (agent framework) and benchmark (`BenchSpec` values + adapter) | [`core/spec.py` L15-20](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L15-L20) |
| Eight editable components c1..c8 | System prompt, guardrails, memory, tool guidance, sub-agents, skills, scripts, plugins | [README L68-73](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L68-L73) |
| `SurfaceSpec` | Per-framework edit surface (paths, always-on injected files, length limits, hook files, allowed hook events) | [`core/tree.py` L40-60](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L40-L60) |
| Always-on injection limit | OpenCode 24,000 characters, Codex 8,000 characters. The stated reason is that Codex injects `AGENTS.md` on every turn and silently truncates it at 32,768 bytes | [`substrate/opencode.py` L42-51](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L42-L51), [`substrate/codex.py` L39-47](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L39-L47) |
| Edit convention | "Omission means inheritance": a proposal emits only the files it changes | [`core/tree.py` L15-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L15-L21) |
| Path escape rejection | Rejects absolute paths and paths containing `..` | [`core/tree.py` L82-89](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L82-L89) |
| `BenchmarkAdapter` | Everything a benchmark must supply: `tasks`, `task_prompt` (scoring criteria removed), `execute`, `trajectory`, `validate_tree`, `score`, etc. | [`core/spec.py` L200-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L200-L250) |
| `Substrate` | `surface`, `materialise`, `execute`, `read_trajectory`, `preflight` | [`substrate/base.py` L47-80](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L47-L80) |
| Roles | Executor, harness editor (two dimensions, INV and DOM), composer, selector, experience reflector. The judge sits outside the method | [README L37](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L37) figure caption, [`core/recursion.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py), [`core/selection.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py), [`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19) |

### 1.3 Propose–Probe–Compose

1. **Propose**: the editor produces candidates in two dimensions. INV is "how the agent works" (tools, procedures), DOM is "what a practitioner in that field knows" ([`core/prompts.py` L347-373](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L347-L373)). The paper's §2.2.1 describes these as domain-independent defects and domain-specific defects.
2. **Probe**: runs each candidate **on the same task** and compares its trajectory and outputs with the baseline run (paper §2.2.1).
3. **Compose**: merges changes the evidence supports, repairs conflicting edits, and either adopts one candidate or keeps the current harness (paper §2.2.1). The compose instructions set the expected result as combining INV edits and DOM edits ([`core/prompts.py` L934](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L934)).

There are two ways to scale ([`core/recursion.py` L343-566](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L343-L566)).

- **Parallel (`agg`)**: builds and runs k INV + k DOM candidates from the same baseline evidence, then builds k mutually independent compositions.
- **Sequential (`seq`)**: chains k rounds of Propose–Probe–Compose, passing the refined harness and the accumulated evidence to the next round.

An invalid proposal is **retried once**; if it still fails, the current harness is inherited unchanged ([`core/recursion.py` L15-19, L36](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L36), [L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L242-L251)). On retry, the validation error text is fed back verbatim. The adapter contract also requires: "error messages go straight into retry feedback, so write them as actionable sentences" ([`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245)).

### 1.4 Event and trajectory model

Harness² has **no lifecycle event model like Mallangable 5.6.** Instead it has two things.

- **Common trajectory grammar**: renders each substrate's different log format as `[ACTION]` / `[OBSERVATION]` / `[ERROR]` lines ([`core/spec.py` L230-231](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L230-L231), [`substrate/codex.py` L386-389](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L386-L389), [`substrate/opencode.py` L384-388](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L384-L388)). The whole trajectory is given as a file, and only individual observations are truncated to a length limit (default 50,000 characters, values under 10,000 characters forbidden) ([`core/spec.py` L163-167](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L163-L167), [`core/context.py` L15-27](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L15-L27)).
- **Evidence as files, prompts as pointers**: the editor reads the task, trajectories, outputs, harness, library and candidates from disk under `context/`, and must cite the trajectory point that justifies every edit ([`core/context.py` L521-544](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L521-L544)).
- **Hooks are edit targets**: on the Codex substrate, `.codex/hooks.json` is part of the edit surface. The allowed events are `PreToolUse`, `PostToolUse`, `PermissionRequest`, `PreCompact`, `PostCompact`, `SessionStart`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, `Stop` ([`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72)). The validator accepts only the `command` form. The code notes that a malformed hook **does not run at all**, with no error, so the form is enforced at the moment the proposer sees it ([`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251)).

### 1.5 Evaluation methodology

| Mechanism | Content | Source |
| --- | --- | --- |
| Score-free run view | `RunView`, the run information the method knows, "never carries a score" | [`core/spec.py` L176-187](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L187) |
| Scoring only after selection | `score()` is called only by `core.judge`, and only after selection is final. No module on the method side imports `judge` | [`core/spec.py` L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L247-L250), [`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19), [BENCHMARKS L34](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L34) |
| Scoring failure ≠ 0 | A failure is `None`, excluded from the denominator, not cached as 0. Unscored items are reported separately | [`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18), [EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118), [BENCHMARKS L67-68](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L67-L68) |
| Answer-path blocking | Raises an exception if `leak_globs` declared by the benchmark enter the context | [`core/context.py` L399-416](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L416) |
| Scoring-trace tripwire | Rejects if a grader output marker string appears in a context file name or body, or in a harness the agent wrote. "This is a tripwire, not the defense itself. If it trips, do not widen the marker list; find the leaking read path" | [`core/context.py` L419-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L419-L518) |
| Measurement-word ban | Rejects agent-visible benchmark text containing benchmark, evaluation, grader, rubric or score: "describe the work, not the measurement" | [`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126) |
| Explicit no-scoring instruction | Editor and selector prompts say "the context contains no scoring criteria, answers or scores. Do not guess what the grader wants" | [`core/prompts.py` L41-53](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L41-L53), paper Appendix H |
| Anonymous selection | Labels candidates A, B, … and shuffles them with a `task_id\|k\|mode` seed (same result on re-run). The selection pool is only the k final candidates; the baseline run is not included | [`core/selection.py` L71-76](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L76), [L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L93-L111) |
| Fallback on selector failure | If the selector fails, picks a neutral fallback (the baseline run passed in, or else the first final candidate) and records it as `fallback` | [`core/selection.py` L237-252](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L237-L252) |
| Budget identity | Runs per task R = 4k (baseline k + candidates 2k + final k), improvement sessions P = 3k. Overlapping labels are treated as overwrites and fail before the numeric check | [`core/ledger.py` L15-33, L89-113](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L113) |
| Run identity | Puts the harness tree fingerprint into the completion marker, so a run from a different configuration is not reused | [`core/runmark.py` L15-20, L41-61, L91-102](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L102) |
| Candidate diversity | Measures with line-level Jaccard between candidate harnesses whether they converge into one | [`core/tree.py` L407-427](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L407-L427) |
| Web-access warning | Public benchmarks have their scoring criteria online. In a validation run, a Codex run **downloaded its own task's scoring criteria without being told to**. Recommends network-level blocking on the execution host, and reporting the restrictions used alongside the results | [EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109), [README L166-171](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L166-L171) |
| Library scope | Separated per run, mode and domain; each run starts with every domain empty. Within a domain, only earlier tasks are read | [`core/library.py` L15-24](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L15-L24), [EXPERIMENTS L16-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L16-L19) |
| Experience entries | Stored only if `cue`, `lesson` and `evidence` are all present (`confidence` optional). Otherwise not added to the library | [`core/library.py` L43-47, L106-123](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L43-L123), [`core/selection.py` L494-501](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L494-L501) |

There are three benchmarks: JobBench, LAB and WorkBuddy-Bench ([README L129-133](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L129-L133)). The results stated in the README and abstract are, on GLM-5 and Gemini 3.5 Flash with a single round, gains of up to 11.5 points on WorkBuddy-Bench, 4.5 points on JobBench and 11.8 percentage points in partial pass rate on LAB ([README L41-45](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L41-L45)). The paper's Appendix F lists two limitations. Inference cost grows as the recursion budget grows, and with no ground-truth supervision the judgments are sensitive to run variance and to biases shared across models. These figures were not reproduced here.

### 1.6 License

- Main body: Apache 2.0 ([README L199-204](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L199-L204)). It does not conflict with Apache-2.0, which this repository intends to use for schemas and tools (README "License").
- `third_party/`, benchmarks and datasets follow their respective upstream licenses. WorkBuddy-Bench is under **Tencent's own license with regional restrictions** ([BENCHMARKS L80-83](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L80-L83)).
- This note uses only short quotations and links and copies no code. The proposed wording below is also a restatement of the concepts in our own words; only the attribution remains.

## 2. Mapping table — Harness² concepts → Mallangable

Verdict: **Adopt** (almost as is), **Adapt** (take only the intent), **Reject**.

| # | Harness² concept | Mallangable location | Verdict | Reason |
| --- | --- | --- | --- | --- |
| M1 | Harness = editable c1..c8 tree | 5.6 definition (deterministic shell) | **Reject** (at the definition level) | Our harness is the side that *enforces* policy. A structure in which the agent modifies guardrails and hooks contradicts I8 (authoritative enforcement only in the control plane) and 7.11 "policy files immutable". Refining only procedures (skills, prompts) offline is possible |
| M2 | A malformed hook silently does not run; check the form at write time | 5.6 "Caution", 7.2 device harness hooks | **Adopt** | Exposes one more path that stays open on failure (fail-open). Strengthens the existing principle that device hook configuration is schema-checked at write time and the server receive-check is the final authority |
| M3 | Codex hook event list | 5.6 "Mapping example" | **Adapt** | A candidate for a second mapping table besides Claude Code. But its source is Harness²'s validator, not official Codex documentation, so mark it "needs confirmation" |
| M4 | No score in `RunView`, scoring after selection, scoring-trace tripwire, `leak_globs` | 10.2 hidden checks, I7 | **Adopt** | Mallang-Bench's SBR is meaningful only if the hidden checks are really hidden. If hidden checks leak into the generation or judging context, SBR is skewed optimistically |
| M5 | Scoring failure is `None`, excluded from the denominator, reported separately | 10.2 "Report format" | **Adopt** | Counting failures as 0 lowers CSR; dropping and hiding them raises it. Neither is honest |
| M6 | Scoring criteria leaked through web access; report network restrictions | 10.2 composition and reporting, 7.3 egress allowlist | **Adopt** | The same problem arises if the attack set, extraction set or hidden checks are public. Require the 7.3 allowlist rule as a benchmark execution condition as well |
| M7 | Measurement-word ban (describe the work) | 10.2 request set | **Adopt** | If request-set sentences contain words like "check" or "score", the agent may target the measurement itself |
| M8 | Anonymous, seed-shuffled selection, baseline run excluded | 5.8 G4 judging, 5.7 judge | **Adapt** | Keeps the judge from knowing which generator, harness or model path a candidate came from. This adds "source-blind judging" to I7 (a different instance) |
| M9 | Budget identity R=4k, P=3k, label-overlap check | 10.2 CPC, 5.6 budget | **Adapt** | A fair cost comparison must also report "how many runs and how many judgments". The exact identity fits only Harness²'s method, so take only the *reporting items* |
| M10 | Run identity by harness fingerprint | `change-record.schema.json` `provenance` | **Adopt** | Today `agent` is only a "role@harness" string, so the record stays the same even when the harness *configuration* changes. A content hash enables reproduction, audit and benchmark comparison |
| M11 | Invalid proposal retried once, then current state kept | 5.8 G1 "On failure", 5.6 budget | **Adopt** | G1 only says "return the reason to the agent" and has no limit or terminal state. Considering the cost attacker (7.1), a limit and a "no change" termination are needed |
| M12 | Per-domain experience library (cue, lesson, evidence) | 5.3 `ResolutionCache`, chapter 6 resolution cache, 7.5 scope separation | **Adapt** | Scope separation is already in 7.5. What to take is the storage condition "do not store a lesson without an evidence field", and a reporting item stating whether the benchmark started with an empty cache |
| M13 | Propose–Probe–Compose (contrastive improvement without ground truth) | 10.1 O1·O4, 5.7 merger and promoter | **Adapt (optional)** | 4k runs for one interactive change fits neither the time tiers (8.4) nor the cost. Keep it only as a starting point for server jobs (merge, promotion) or for O4 research on judge reliability |
| M14 | `[ACTION]/[OBSERVATION]/[ERROR]` trajectory grammar | 5.11 telemetry, G4 evidence | **Deferred** | E4 and E5 events can produce the same information. Revisit when defining the judge input format |
| M15 | Candidate diversity (Jaccard) | — | **Reject** | Our spec has no step that produces many candidates (YAGNI) |
| M16 | Always-on injection length limit and its reason | 5.10 context supply | **Deferred** | A useful figure when setting per-role context budgets. The case for putting it in the spec now is weak |

## 3. Proposed edits (by priority, at most 10)

Each item is a minimal edit. The wording is not copied from Harness² text; it restates the concepts.

### E-1. Add hidden-check isolation rules to 10.2 Mallang-Bench (M4)

- File: `docs/10-open-problems.md`, right below the "### Composition" table
- Basis: [`core/spec.py` L176-187, L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L250), [`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19), [`core/context.py` L399-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L518)
- Proposed wording:

```markdown
Hidden-check isolation (MUST):
- Hidden checks and their results never enter the context of the interpreter, generator or judge. Scoring is done by a separate process after activation completes.
- Each time the runner builds a generation or judging context, it looks for hidden-check file paths and check-result marker strings, and stops the run if it finds any. This check is only an alarm, not a defense. If it trips, do not widen the marker list; fix the leaking read path.
(Source: Harness²'s score-free run view and scoring-trace tripwire, google-research/harness2 `core/spec.py`, `core/context.py`)
```

### E-2. Add the unscored rule to 10.2 "Report format" (M5)

- File: `docs/10-open-problems.md`, end of the "### Report format" paragraph
- Basis: [`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18), [EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118)
- Proposed wording:

```markdown
A request whose scoring failed (hidden-check execution error, judge model error) is **unscored**, not 0. Remove it from the metric's denominator and report the unscored count next to the metric. Example: "CSR 0.71 (n=192, unscored 8)".
```

### E-3. Add execution-environment reporting items to 10.2 "Report format" (M6, M9, M12)

- File: `docs/10-open-problems.md`, after the E-2 paragraph
- Basis: [EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109), [`core/ledger.py` L15-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L33), [`core/library.py` L21-23](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L21-L23)
- Proposed wording:

```markdown
Execution conditions to report alongside:
- **Network restrictions**: the list of hosts the generation agent could reach. Addresses hosting hidden checks, the attack set or the extraction set are blocked during the run. On public benchmarks, a case has been reported in which an agent downloaded the scoring criteria without being told to (Harness² experiments guide).
- **Call counts**: the number of generation runs and judging sessions per successful change (including retries). CPC alone cannot compare different harnesses fairly.
- **Cache state**: whether the resolution cache and learned lessons started empty, or were allowed to use results from earlier requests.
```

### E-4. Add source-blind judging to 5.8 G4 (M8)

- File: `docs/05-reference-architecture.md`, the "Content" cell of the `G4 judging` row in the 5.8 gate table
- Basis: [`core/selection.py` L71-76, L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L111), paper §2.2.2
- Current: `Judge decides whether the meaning is satisfied from screenshots and intent`
- Proposed: `Judge decides whether the meaning is satisfied from screenshots and intent. The judge does not know which generator, harness or model path the output came from (source-blind judging). When there are several candidates, present them under anonymous ids shuffled with a reproducible seed`

### E-5. State the retry limit in 5.8 G1 on failure (M11)

- File: `docs/05-reference-architecture.md`, the "On failure" cell of the `G1 static check` row in the 5.8 gate table
- Basis: [`core/recursion.py` L15-19, L36, L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L251), [`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245)
- Current: `Return the reason to the agent`
- Proposed: `Return the reason to the agent as an actionable sentence. Past the retry limit (proposal value: 1), keep the current state with no change and terminate`

### E-6. Add a fail-open warning for hooks to 5.6 "Caution" (M2)

- File: `docs/05-reference-architecture.md`, after the last "Caution:" paragraph of 5.6
- Basis: [`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251)
- Proposed wording:

```markdown
In many runtimes a malformed hook configuration **does not run at all**, with no error. That is, on failure it stays open. The harness plugin checks the hook configuration at write time against the event names and handler format the runtime accepts, and at session start (E1) confirms that the hooks were actually registered. The agent cannot modify policy hook or guardrail files (tool boundary, E4).
(Reference: Harness² checks Codex hook files at write time for the same reason. google-research/harness2 `core/tree.py`)
```

### E-7. Add a harness fingerprint field to `change-record.schema.json` (M10)

- File: `schemas/change-record.schema.json`, in `properties.provenance.properties` after `prompt_hash`
- Basis: [`core/runmark.py` L15-20, L41-61](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L61), [`substrate/base.py` L26-32](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L26-L32)
- Proposed field (`required` unchanged, optional field):

```json
"harness_digest": {
  "type": "string",
  "pattern": "^sha256:[0-9a-f]{64}$",
  "description": "Content hash of the harness configuration (skills, hooks, policy copy, tool list) that produced the change. Even with the same agent string, a different configuration gives a different value"
}
```

- Note: Harness² uses the first 16 characters of SHA-1. Here, full SHA-256 is proposed to match the existing `prompt_hash` format. If applied, the `examples/change.example.yaml` validation must be rerun (since it is an optional field, the existing example should still pass).

### E-8. Add the measurement-word ban to the 10.2 request set (M7)

- File: `docs/10-open-problems.md`, end of the "Content" cell of the `Request set` row in the "### Composition" table
- Basis: [`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126)
- Text to append: `. Request sentences state only the work to do, never the measurement ("check", "scoring", "score" etc. are forbidden)`

### E-9. Add a candidate Codex column to the 5.6 mapping table (M3)

- File: `docs/05-reference-architecture.md`, a short paragraph after the "### Mapping example: Claude Code hooks" table
- Basis: [`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72) (a secondary source, not official Codex documentation)
- Proposed wording:

```markdown
Codex CLI maps in the same way (E1 `SessionStart`, E2 `UserPromptSubmit`, E4 `PreToolUse`, E5 `PostToolUse`, E6 `PermissionRequest`, E11 `Stop`, E12 `SubagentStop`, E15 `PreCompact`). This list is taken from the event set Harness² validates, so it must be checked against official Codex documentation before it is applied.
```

### E-10. Add Harness² to the references

- File: `docs/references.md`, a new section before "## Agent security"
- Proposed wording:

```markdown
## Harness improvement and evaluation

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · Code (Apache-2.0): https://github.com/google-research/harness2
  - Basis for hidden-check isolation, unscored reporting, source-blind judging and harness fingerprints (5.6, 5.8, 10.2). Research note: [research/harness2-analysis.md](harness2-analysis.md)
```

## 4. What was left out

- **Self-editing harness (M1)**: if the agent that modifies the user's app also modifies its own policy hooks, the reason 5.6 defines a harness ("a deterministic shell around a non-deterministic agent") disappears.
- **Putting Propose–Probe–Compose into the default generation flow (5.4)**: one change would cost 4k runs, and the T0~T2 time tiers could not be kept. Its place is as an experimental option for server jobs and in O4 research.
- **Citing benchmark figures**: we did not reproduce them, and the task distribution differs from our problem (app modification).
