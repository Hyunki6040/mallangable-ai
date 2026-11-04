<!-- LANG-BAR -->
**English** · [한국어](../ko/01-introduction.md) · [简体中文](../zh-CN/01-introduction.md) · [日本語](../ja/01-introduction.md) · [Español](../es/01-introduction.md)
<!-- /LANG-BAR -->

# 1. Introduction — why "malleable software architecture" needs its own definition

> Conclusion of this chapter: AI has made code cheap, but there is still no standard **structure for putting that code inside an existing app, running it safely, and making it survive updates**. Mallangable-AI defines that structure.

## 1.1 The problem: code got cheap, software is still rigid

Mass-produced software is built for the average user. The further users are from the average, the more they bend their way of working to fit the software. Ink & Switch likens this state to "appliances bought at a store" and calls an ecosystem where users rework their tools **malleable software** ([Ink & Switch, 2025](https://www.inkandswitch.com/essay/malleable-software/)).

In 2025~2026 the cost of code generation fell sharply. Yet, as the same essay points out, **AI code generation alone does not make software malleable.** App builders only make new apps; they cannot fix the apps people already use. In practice, things get stuck in three places.

| Gap | Symptom | Where this document addresses it |
| --- | --- | --- |
| **No place to put it** (surface gap) | Even when the AI builds a feature, there is no slot to fit it into the existing app. People end up patching the core source directly | Chapter 2 extension points and depth, chapter 5 runtime |
| **Does not survive updates** (persistence gap) | When the vendor ships a new version, user modifications break. Thousands of users × every version | Chapter 6 lineage and contract-preserving merge |
| **No control** (governance gap) | Nobody knows who changed what, what that code can access, or who pays | Chapter 4 control spectrum, chapter 7 trust, chapter 9 business |

The third gap is not theoretical; incidents have already happened. In early 2026, 341 of 2,857 audited skills on one agent skill marketplace were confirmed malicious ([The Hacker News, 2026.02](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)), and even after a scanner was introduced, some skills remained that evaded inspection by inflating their file size ([Unit 42, 2026.06](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/)). The root cause was structural: "skills run with the agent's full permissions."

## 1.2 Definition

> **Mallangable software** is software in which, when a user expresses an intent through natural language, pointing at the screen, or demonstration, an AI agent builds a change **inside extension points the host app has defined in advance**, and that change is **verified by a contract, recorded so it can be reverted, and managed so that it survives updates to the upstream baseline**.

Origin of the name: Korean **말랑(mallang)**, meaning soft or squishy, + English **-able**. It was chosen to sound like the English *malleable* (able to be hammered into shape).

### How it differs from similar approaches

| Approach | What changes | Who changes it | Modifies the existing app | Survives updates | Risk control |
| --- | --- | --- | --- | --- | --- |
| Settings | Values the vendor exposed in advance | User | Yes (narrowly) | High | High |
| Plugins | Parts opened through the vendor API | Developer | Yes | Medium (breaks when the API changes) | Varies by ecosystem |
| No-code builders | A new app inside the builder | User | No | Platform-dependent | Platform-dependent |
| App generators (vibe coding) | An entire new app | User + AI | No | N/A | Low~medium |
| Generative UI (one-off) | The screen for this conversation | AI | No (ephemeral) | N/A | Limited by catalog |
| **Mallangable** | Features, screens and behavior inside extension points | User + AI (+ org) | **Yes** | **Design goal** | **Tuned by policy** |

## 1.3 Contributions of this document

1. **Formal model**: defines host, layer, change, contract and policy, and presents 10 invariants the architecture must keep (chapter 2).
2. **Change depth hierarchy D1~D5**: a risk grading that applies the Rule of Least Power ("solve it with the weakest expression") to user changes (chapter 2).
3. **Design space**: filters the **1,944,000** raw combinations of 11 axes with logical, normative and recommendation constraints down to **36,772 (1.89%)** in **863** structural families, and publishes a tool to recompute them (chapter 3, `tools/design_space.py`).
4. **Control spectrum**: defines what is allowed to users and what operators control as an "interval delegation" model, with **user floor rights that no policy can take away** (chapter 4).
5. **Reference architecture**: defines 6 planes, port and adapter interfaces, a vendor-neutral harness event model and verification gates (chapter 5).
6. **Contract-preserving merge and lineage propagation**: presents the conditions under which user modifications survive baseline updates, and a cost model (chapter 6).
7. **Experience design conventions**: defines input surfaces, time tiers (T0~T4), how the generation process is shown, lexicon packs and the model connection flow (chapter 8).
8. **Business coupling matrix**: links 20 BMs to the architecture choices they require, in a computable form (chapter 9).

## 1.4 Scope and non-scope

**In scope**
- The concepts, boundaries, interfaces and options needed to make existing software (web SaaS, desktop, mobile, internal business tools) malleable.
- Control, visibility and billing structures from individual users to enterprise and public-sector environments.

**Out of scope**
- Implementation in a specific language or framework. This document defines only interfaces and conventions.
- Prompting techniques for specific models. Models are treated as replaceable parts.
- Legal advice. Privacy, labor and copyright matters are noted only as design considerations; actual application requires review under the applicable law.

## 1.5 Related work and differences

| Lineage | Key idea | What we took | How we differ |
| --- | --- | --- | --- |
| Malleable software ([Ink & Switch](https://www.inkandswitch.com/essay/malleable-software/)) | A gentle slope from user to creator, tool-centered | Motivation for the depth hierarchy, community creation | Defines AI agents, enterprise governance and billing as architecture |
| Computational media and dynamic documents (Boxer, 1986 · [Webstrates](https://webstrates.net/), 2015 · [Potluck](https://www.inkandswitch.com/potluck/), 2022 · [Embark](https://www.inkandswitch.com/embark/), 2023) | Removes the boundary between documents and apps; users layer computation on top | Overlay layers that leave the original untouched (2.3), tools that span apps (O8) | Defined on top of existing commercial apps, as a structure that survives vendor updates |
| Gentle slope (MacLean et al., 1990, cited in the essay above) | As customization power grows, the learning required should increase only a little at a time | D1~D5 designed as a "slope without cliffs" | Each step of the slope is mapped to a level of risk and verification strength |
| [Rule of Least Power](https://www.w3.org/2001/tag/doc/leastPower.html) (W3C TAG) | The less expressive a language, the easier analysis, reuse and security | The "build at the minimum depth needed" rule | Enforced so that agents, not people, choose the depth |
| Dynamic software product lines (DSPL) and feature models ([Capilla et al., 2014](https://research.chalmers.se/publication/198081)) | Feature configuration at runtime, constraints between features | Computing the design space as a constrained configuration model | The configuring party is the user + AI, not the vendor |
| Local-first, CRDT, Patchwork ([Ink & Switch](https://www.inkandswitch.com/project/patchwork/)) | User-owned data, general-purpose version control | Topology options, branch = experiment · putting AI edits on a branch and letting a person pick and merge (Patchwork lab notes) | Adds lineage (baseline hierarchy) and contract-preserving merge |
| Generative UI standards ([A2UI](https://a2ui.org/), [MCP Apps](https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp)) | Declarative UI instead of code, sandboxed iframe UI | D3 artifact format | Persistent, versioned changes rather than one-off ones |
| Agent skills and plugins ([Agent Skills](https://agentskills.io/specification)) | Packaging procedures as folders, portable across agents | Harness distribution format | A skill is only a procedure; enforcing permissions is the architecture's job |
| Prompt injection defense ([CaMeL](https://arxiv.org/abs/2503.18813), [design patterns](https://arxiv.org/abs/2506.08837), [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)) | Separating control flow from untrusted data, privilege separation | Agent role separation, information-flow labels | Applied to the context of code generation and merging |
| In-app generation ([n.codes](https://github.com/yungookim/n.codes), [Glaze](https://www.implicator.ai/raycast-launches-glaze-a-platform-for-building-desktop-apps-through-ai-prompts/)) | Per-user UI generation from an app's capability map, sharing and forking apps | Capability map, sharing flow | Defines update survival, lineage and the control spectrum as a general model |

## 1.6 Notation

- **MUST**: an implementation that does not comply is not a conforming Mallangable-AI implementation.
- **SHOULD**: may be departed from for a valid reason, but that reason must be documented.
- **MAY**: optional.
- Axes are written `A1`~`A11`, constraints `L` (logical) · `N` (normative) · `S` (warning), invariants `I1`~`I10`, profiles `P1`~`P7`, BMs `B1`~`B20`.
- Numbers without a source link (e.g. size limits, score weights) are **design proposal values** and must be tuned by experiment.

Next chapter: [2. Core model](02-core-model.md)
