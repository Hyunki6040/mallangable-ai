<!-- LANG-BAR -->
**English** · [한국어](../ko/glossary.md) · [简体中文](../zh-CN/glossary.md) · [日本語](../ja/glossary.md) · [Español](../es/glossary.md)
<!-- /LANG-BAR -->

# Glossary

This lists terms for development and design documents alongside the expressions used on screens for ordinary users (lexicon pack `basic` level). The full dictionary for user-facing screens is in [`examples/lexicon.en.yaml`](../../examples/lexicon.en.yaml).

| Term | English | Definition | User-facing expression | First appears |
| --- | --- | --- | --- | --- |
| malleable software | malleable software | Software that users can rework to fit their own needs with little friction | — | 1.1 |
| Mallangable | Mallangable | Software in which AI builds changes inside extension points, and contracts are used to verify, record and propagate them | — | 1.2 |
| host | host | The app being made malleable. `H = ⟨C, X, K, Σ⟩` | app | 2.2 |
| core | core | The immutable part the vendor ships | — | 2.2 |
| extension point | extension point | A location where the host allows modification | place you can change | 2.2 |
| capability | capability | A name tag for an ability an extension may use | allowed scope | 2.2 |
| capability map | capability map | A machine-readable list of extension points, capabilities and schemas | — | 2.2 |
| layer | layer | A bundle of changes, such as a baseline or a user layer | — | 2.3 |
| effective app | effective app | The result of composing layers on top of the core | — | 2.3 |
| change | change (δ) | A bundle of intent, artifact, contract, capabilities, depth, points and provenance | what you changed | 2.4 |
| feature | feature | A sequence of changes that come from the same intent | feature I made | 2.4 |
| intent | intent (ι) | A summary of the purpose a person stated | — | 2.4 |
| contract | contract (κ) | Acceptance conditions on the observable behavior of the effective app | list of promises | 2.5 |
| depth | depth D1~D5 | The expressiveness and risk level of an artifact | how much it changes | 2.6 |
| least-depth rule | least-depth rule | Build at the lowest depth that satisfies the contract | — | 2.6 |
| policy | policy | The allowed interval for each knob | range your company allows | 2.7 |
| invariant | invariant I1~I10 | A property an implementation must not break by design | — | 2.9 |
| design axis | design axis A1~A11 | A dimension of architectural choice | — | 3.2 |
| structural family | structural family | One combination of the structural axes A1~A8 | — | 3.4 |
| reference profile | reference profile P1~P7 | A representative point in the design space | — | 3.5 |
| knob | knob | One controllable dimension | setting | 4.2 |
| ceiling · floor | ceiling · floor | The risky end · the guaranteed end of an allowed interval | — | 4.2 |
| user floor rights | floor rights F1~F7 | User rights that no policy can remove | — | 4.6 |
| PDP · PEP | policy decision/enforcement point | Where policy is decided · where it is enforced | — | 4.8, 7.2 |
| plane | plane | The 6 areas of responsibility in the architecture | — | 5.1 |
| harness | harness | The deterministic shell around an agent that enforces procedure, tools, policy, budget and output | — | 5.6 |
| verification gate | gate G0~G5 | Check stages that must be passed before activation | check | 5.8 |
| source-blind judging | source-blind judging | The G4 rule that keeps the judge unaware of an artifact's generator, harness and model route | — | 5.8 |
| hot swap | hot swap | Replacing only an extension slot without restarting the core | — | 5.9 |
| safe mode | safe mode | Starting with all user layers turned off | start in default mode | 5.9 |
| topology | topology | The structure of change history (snapshot · fork · lineage · crdt) | — | 6.2 |
| lineage | lineage | A fork network of a multi-level baseline hierarchy | — | 6.3 |
| baseline | baseline | The version that serves as the starting point for lower layers | default edition | 6.3 |
| drift | drift | The distance from the latest upstream release | behind the default edition | 6.3 |
| resolution ladder | resolution ladder R0~R5 | The order in which conflict-resolution methods are tried, cheapest first | — | 6.6 |
| contract-preserving merge | contract-preserving merge | A merge that satisfies both sides' contracts | combine | 6.7 |
| intent conflict | intent conflict | A state in which both sides' contracts cannot be satisfied at once | part that needs your choice | 6.7 |
| resolution cache | resolution cache | Reuse of verified conflict resolutions within the visibility scope | — | 6.8 |
| contract migration | contract migration | Weakening or moving a contract, allowed only with user consent or a point-retirement mapping table. Recorded with the `Contract-Migrated` trailer | — | 6.7 |
| promotion | promotion | Raising a feature that converged in lower layers into the upper baseline | adopted as an official feature | 6.10 |
| lethal trifecta | lethal trifecta | The combination of private data, untrusted input and external communication | — | 7.3 |
| visibility label | visibility label | The scope and level of data (V0~V3) | what admins can see | 7.5 |
| integrity label | integrity label | The third component of the label λ (trusted > untrusted). Values that decide permission increases, external transmission or extension-point selection must be trusted | — | 7.5 |
| output gate | output gate | The only point that lowers a label (the declassifier) | — | 7.5 |
| object capability | object capability | A security model in which code acts only through capability objects handed to it | — | 7.6 |
| time tier | time tier T0~T4 | Experience patterns by response-time band | — | 8.4 |
| change receipt | change receipt | A card stating what changed and how to undo it | receipt | 8.6 |
| lexicon pack | lexicon pack | A dictionary of expressions per concept id, by level, domain and language | — | 8.9 |
| model sourcing | model sourcing | Whose account and money inference runs on | how the AI engine is connected | 3.2 A9, 8.10 |
| silent breakage rate (SBR) | silent breakage rate (SBR) | The share of merges that passed the public contract but failed hidden checks | — | 10.2 |
| unscored | unscored | A request whose scoring itself failed. It is not entered as 0 points; it is removed from the denominator and its count is reported separately | — | 10.2 |
