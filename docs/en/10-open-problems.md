<!-- LANG-BAR -->
**English** · [한국어](../ko/10-open-problems.md) · [简体中文](../zh-CN/10-open-problems.md) · [日本語](../ja/10-open-problems.md) · [Español](../es/10-open-problems.md)
<!-- /LANG-BAR -->

# 10. Open problems and evaluation

> Conclusion of this chapter: this spec only defines the structure; several core problems are still unsolved. The biggest is that **when contracts are weak, merges silently break features**. So this chapter proposes **Mallang-Bench** as a common yardstick for comparing implementations, and treats the "silent breakage rate" as the most important of its metrics.

## 10.1 Open problems

| # | Problem | Why it is hard | Starting point |
| --- | --- | --- | --- |
| O1 | **Contract sufficiency** | Contracts written by agents easily become tautologies ("the panel exists"). Weak contracts let merges pass while features break | Mutation testing: measure contract strength by whether the contract fails when the artifact is deliberately broken (mutation score). Use it as the criterion for selecting what is covered by the survival guarantee (B9) |
| O2 | Semantic conflict detection | Even with no textual or syntactic conflict, two changes together can break an intent | Run the union of contracts, measure afterwards with hidden check sets |
| O3 | **Feature interaction** | Two changes that are each correct behave strangely when both are on (the classic "feature interaction" problem of telecom software) | Add combination checks to G2 for pairs of changes that touch the same extension point or the same data |
| O4 | Judge reliability | Model judgments are probabilistic and wobble even on the same input | Deterministic contracts first, consensus of several judges, a reference set for calibrating judgments |
| O5 | Capability map completeness | When extension points are lacking, requests slide into D5 | Use the D5 request rate as a capability map quality metric; add points starting from the top requests |
| O6 | Lineage economics | Frequent releases raise propagation cost; infrequent ones raise drift | Optimize release cadence with the 6.8 cost model, design support periods |
| O7 | Cross-scope promotion signals | You must know that "people are building the same thing" across tenant boundaries without looking at code | Similarity using only V1 metadata, minimum aggregation size, privacy-preserving set comparison |
| O8 | Tool composition across apps | Users' work spans several apps ("tools, not apps"). One host's extension points are not enough | Common data contracts across hosts, OS-level extension points |
| O9 | Accountability | When an AI-built change causes an incident, who is responsible: the user, the tenant, the operator or the model vendor? | Link provenance records (I9) and approval records to the terms of service |
| O10 | Accessibility regressions | User modifications can break screen reading and keyboard operation | Make the G3 accessibility rules mandatory, build accessibility into catalog components |
| O11 | Code on top of CRDT | Real-time synchronization conflicts with executable code | Verify at activation time, separate only the code area into Git-style lineage |
| O12 | Measuring malleability | There is no standard scale to quantify the "gentle slope" | Plot a slope curve from time to first success and number of ask-backs per depth |
| O13 | Standards alignment | The extension manifest, MCP Apps, A2UI and skill formats each evolve on their own | Design the manifest as an **adapter target** for these standards, not a superset of them |

## 10.2 Mallang-Bench (proposal)

A benchmark design for comparing implementations under the same conditions.

### Components

| Component | Contents |
| --- | --- |
| Reference host | A small business app with about 20 extension points (e.g. one of to-do, documents, spreadsheet). Capability map published |
| Request set | 200 change requests written in ordinary user language. Each request is labeled with its **correct minimum depth** and **hidden checks** (separate from the public contract). Request text states only the task and never mentions measurement ("check", "grading", "score" and the like are forbidden) |
| Release sequence | 3 baseline releases. Includes compatibility-breaking changes (point renames, layout restructuring, point retirement) |
| Attack set | 50 items, including injections hidden in shared feature descriptions or reference documents, privilege-escalation lures, size inflation, and remote content replacement after installation |
| Extraction set | 50 conversations that try to extract source in hidden mode |
| User simulator | A script that answers ask-backs and accepts or rejects previews |

Hidden check isolation (**MUST**):
- Hidden checks and their results do not enter the context of the interpreter, generator or judge. Scoring is done by a separate process after activation completes.
- Every time the runner builds a generation or judging context, it looks for hidden check file paths and check-result marker strings, and stops the run if any are found. This check is only an alarm (tripwire), not a defense. If it fires, do not widen the marker list; fix the read path that leaks.
(Source: Harness²'s score-free run view and grading-trace tripwire, arXiv:2610.14224, google-research/harness2 `core/spec.py`, `core/context.py`)

### Metrics

| Symbol | Metric | Definition | Direction |
| --- | --- | --- | --- |
| CSR | Change success rate | Requests activated while passing hidden checks / requests feasible under policy | Higher is better |
| LPC | Least-depth compliance | Changes built at the correct minimum depth / successful changes | Higher is better |
| TFC | Time to first change | Median from request input to preview | Lower is better |
| USR | Baseline survival rate | Features passing hidden checks after a release / features active before the release | Higher is better |
| **SBR** | **Silent breakage rate** | Merges that passed the public contract but failed hidden checks / (automatic merges + `proposed` merges approved by a person). Also reported separately for the two paths | **Lower is better (top priority)** |
| HER | Human intervention rate | Conflicts that went to R5 / all conflicts | Lower is better (but read together with SBR) |
| CPC | Cost per change | Inference cost per successful change | Lower is better |
| IRR | Injection resistance rate | Share of the attack set that was blocked | Higher is better |
| LKR | Source leak rate | Share of the extraction set in which code fragments leaked | Lower is better |
| RBT | Revert time | From the revert request to full restoration | Lower is better (T0 target) |
| APB | Approval burden | Weekly approval requests per user or admin | Lower is better |

Why SBR is the top priority: the human intervention rate (HER) is easy to lower by merging aggressively. The price is silent breakage. Only reporting both metrics together makes for an honest comparison.

### Reporting format

Implementations report their metrics together with the design-space coordinates they used (A1~A11). Comparisons are fair only between the same coordinates. Example: "P2 coordinates, CSR 0.71, LPC 0.88, USR 0.83, SBR 0.04, HER 0.06".

A request whose scoring failed (hidden check execution error, judge model error) is **unscored**, not 0 points. Remove it from the metric's denominator and report the unscored count alongside the metric. Example: "CSR 0.71 (n=192, unscored 8)".

Run conditions to report as well:
- **Network restrictions**: the list of hosts the generation agent could reach. Addresses hosting the hidden checks, attack set and extraction set are blocked during the run. On public benchmarks, cases have been reported of agents downloading the grading criteria without being told to (Harness² repository `docs/EXPERIMENTS.md`).
- **Call counts**: the number of generation runs and judging sessions per successful change (including retries). CPC alone cannot fairly compare different harnesses.
- **Cache state**: whether the resolution cache and learned lessons started empty, or whether results from earlier requests were allowed to be used.

## 10.3 Conformance levels (proposal)

| Level | Conditions |
| --- | --- |
| Mallangable Core | Guarantees invariants I1~I7, I9, I10 by design. Implements the record format, contracts and revert. P1 and P5, which have no server, reach at most this level |
| Mallangable Governed | Core + I8 (authoritative enforcement through server receive-check), policy interval delegation, user floor rights F1~F7 |
| Mallangable Sealed | Governed + hidden mode (role separation, output gate, per-scope cache separation), Mallang-Bench LKR reporting |

## 10.4 Spec roadmap

| Version | Goal |
| --- | --- |
| v0.1 (this document) | Conceptual model, design space, reference architecture, experience and business coupling, draft schemas |
| v0.2 | Schema stabilization, finalized capability map format, reference host app published |
| v0.3 | Conformance test suite, Mallang-Bench alpha |
| v1.0 | At least 2 external implementations pass the Core level, record format frozen |

Areas where contributions are welcome: O1 (contract sufficiency), O3 (feature interaction), O7 (privacy-preserving promotion), the reference host app, and event mapping tables for other agent runtimes (5.6).

References: [references.md](references.md) · Glossary: [glossary.md](glossary.md)
