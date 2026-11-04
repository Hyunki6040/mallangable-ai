<!-- LANG-BAR -->
[English](../../en/research/harness2-analysis.md) · [한국어](../../ko/research/harness2-analysis.md) · [简体中文](../../zh-CN/research/harness2-analysis.md) · **日本語** · [Español](../../es/research/harness2-analysis.md)
<!-- /LANG-BAR -->

# 調査ノート — Harness² (google-research/harness2)

> このノートの結論: Harness²は**ハーネス(harness)そのものを課題ごとに書き直して使う研究フレームワーク**である。Mallangableのハーネス(5.6)はエージェントを包んで*強制*する外殻なので、方向が異なる。そのまま取り入れるものは三つある。第一に、**採点情報が方法(method)側のコンテキストに決して入らないようにする隔離装置**。第二に、**採点失敗を0点ではなく未採点(unscored)として扱う報告規則**。第三に、**候補の出所を隠した判定**。いずれもMallang-Bench(10.2)とG4(5.8)を補強する。反対に、エージェントにポリシーフック・ガードレールまで書き換えさせる自己編集は受け入れない。

- 確認日: 2026-10-30
- 調査対象: https://github.com/google-research/harness2 (公開リポジトリ、存在確認済み)
- 固定コミット: `1cfe254e8d25b15f37048c3730134686abe60335` (2026-10-13)。以下のソースリンクはすべてこのコミット基準です。
- 方法: `git clone --depth 1`で空の一時ディレクトリに取得し、**読むだけ**にしました(コードは実行していません)。論文はarXivの要旨ページとHTML本文をウェブから取得して読みました。
- 表記: `B` = `https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335`

## 0. 確認できたこととできなかったこと

| 項目 | 状態 | 根拠 |
| --- | --- | --- |
| リポジトリの存在・公開状況 | 確認 | `gh repo view google-research/harness2`、クローン成功 |
| ライセンス | 確認 | [`LICENSE`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/LICENSE) Apache 2.0、[`pyproject.toml`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/pyproject.toml#L9) `license = "Apache-2.0"` |
| 中核ソース(`harness2/core/*`、`substrate/*`) | 直接読んだ | 本文のリンク |
| 論文 | 存在・要旨を確認、本文は一部確認 | [arXiv:2610.14224](https://arxiv.org/abs/2610.14224)、2026-10-09投稿。本文はHTMLを要約ツールで読んだため、**節番号と引用は原文PDFで再照合する必要があります** |
| プロジェクトサイト | 存在確認 | https://harness2.github.io (READMEがリンク) |
| Google Researchのブログ記事 | **見つからず** | サイト・README・論文のどこにもブログへのリンクがない |
| 実験数値の再現 | 行っていない | モデル呼び出しのコストがかかり、調査範囲外 |
| `prompts.py`(1,163行)全文 | 一部のみ読んだ | 隔離指示文とINV/DOMの区間のみ確認 |
| ベンチマークアダプター(`benchmarks/*.py`) | 読んでいない | 方法論と無関係な接続コード |

## 1. Harness²とは何か

### 1.1 目的

READMEはハーネスを「モデルをエージェントとして振る舞わせる周辺システム(プロンプト、ツール、メモリ、スキル、オーケストレーションなど)」と定義し、*harnessing*をそのシステムを最適化する過程と定義しています([README L19-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L19-L21))。Harness²は**モデルの重みを固定したまま**、二段階の再帰でハーネスを改良します([README L23-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L23-L33))。

- **課題レベルの再帰**: 現在の課題の実行ハーネスを、対照型の**Propose–Probe–Compose**段階で磨きます。正解のフィードバックなしに、実行間の行動の対照だけを根拠にします。
- **ハーネシングレベルの再帰**: 課題ごとに採用されたハーネスと、証拠が付いた教訓を持続的な*改善ハーネス*(ライブラリ)に蓄積し、次の課題で使います。

論文の要旨は動機を二つ挙げます。オープンワールドの課題は設計時に見ていないものなので**正解の検証器がなく**、既存の再帰的自己改善は課題特化で一般化しない、という点です([arXiv要旨](https://arxiv.org/abs/2610.14224))。

### 1.2 構造と中核の抽象化

| 抽象化 | 定義 | 出典 |
| --- | --- | --- |
| 三軸の分離 | 方法(再帰・プロンプト・選択・ライブラリ)、基盤(substrate: エージェントフレームワーク)、ベンチマーク(`BenchSpec`の値 + アダプター)を混ぜない | [`core/spec.py` L15-20](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L15-L20) |
| 編集可能な8つの構成要素 c1..c8 | システムプロンプト、ガードレール、メモリ、ツール案内、サブエージェント、スキル、スクリプト、プラグイン | [README L68-73](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L68-L73) |
| `SurfaceSpec` | フレームワークごとの編集面(パス、常時注入ファイル、長さ上限、フックファイル、許可フックイベント) | [`core/tree.py` L40-60](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L40-L60) |
| 常時注入(always-on)の上限 | OpenCodeは24,000文字、Codexは8,000文字。Codexは`AGENTS.md`を毎ターン注入し、32,768バイトで黙って切り詰めるという理由が書かれている | [`substrate/opencode.py` L42-51](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L42-L51)、[`substrate/codex.py` L39-47](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L39-L47) |
| 編集規約 | 「省略は継承」: 提案は変更するファイルだけを出す | [`core/tree.py` L15-21](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L15-L21) |
| パス脱出の拒否 | 絶対パス、`..`を含むパスを拒否 | [`core/tree.py` L82-89](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L82-L89) |
| `BenchmarkAdapter` | ベンチマークが満たすべきすべて: `tasks`、`task_prompt`(採点基準を除去)、`execute`、`trajectory`、`validate_tree`、`score`など | [`core/spec.py` L200-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L200-L250) |
| `Substrate` | `surface`、`materialise`、`execute`、`read_trajectory`、`preflight` | [`substrate/base.py` L47-80](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L47-L80) |
| 役割 | 実行者(executor)、ハーネス編集者(INV・DOMの二次元)、構成者(composer)、選択者(selector)、経験の省察者(experience reflector)。採点者(judge)は方法の外側 | [README L37](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L37)の図の説明、[`core/recursion.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py)、[`core/selection.py`](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py)、[`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19) |

### 1.3 Propose–Probe–Compose

1. **Propose**: 編集者が二つの次元の候補を出します。INVは「エージェントの働き方」(ツール・手順)、DOMは「その分野の実務者が知っていること」です([`core/prompts.py` L347-373](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L347-L373))。論文§2.2.1はこれを、領域に依存しない欠陥と領域特化の欠陥として説明しています。
2. **Probe**: 各候補を**同じ課題で**実行し、基準実行と軌跡・成果物を比較します(論文§2.2.1)。
3. **Compose**: 証拠に裏付けられた変更を統合し、衝突する編集を直し、一つの候補を採用するか現在のハーネスを維持します(論文§2.2.1)。構成の指示文は、INV編集とDOM編集を統合することを期待される結果としています([`core/prompts.py` L934](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L934))。

拡張方式は二つです([`core/recursion.py` L343-566](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L343-L566))。

- **並列(`agg`)**: INV k個 + DOM k個の候補を同じ基準証拠から作って実行した後、互いに独立な構成をk個作ります。
- **逐次(`seq`)**: k回のPropose–Probe–Composeをつなげ、磨いたハーネスと累積した証拠を次の段階に渡します。

不正な提案は**一度だけ再試行**し、それでも駄目なら現在のハーネスをそのまま引き継ぎます([`core/recursion.py` L15-19, L36](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L36)、[L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L242-L251))。再試行時には検証エラーの文をそのままフィードバックします。アダプター規約も「エラーメッセージはそのまま再試行のフィードバックに入るので、行動可能な文で書け」と求めています([`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245))。

### 1.4 イベント・軌跡モデル

Harness²にはMallangable 5.6のような**ライフサイクルのイベントモデルがありません。**代わりに次のものがあります。

- **共通の軌跡文法**: 基盤ごとに異なる記録形式を`[ACTION]` / `[OBSERVATION]` / `[ERROR]`の行としてレンダリングします([`core/spec.py` L230-231](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L230-L231)、[`substrate/codex.py` L386-389](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L386-L389)、[`substrate/opencode.py` L384-388](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/opencode.py#L384-L388))。軌跡全体はファイルとして渡し、個々の観測だけを長さ上限(既定50,000文字、10,000文字未満は禁止)で切り詰めます([`core/spec.py` L163-167](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L163-L167)、[`core/context.py` L15-27](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L15-L27))。
- **証拠はファイルで、プロンプトはポインターで**: 編集者は`context/`以下の課題・軌跡・成果物・ハーネス・ライブラリ・候補をディスクから読み、すべての編集の根拠となった軌跡の箇所を引用しなければなりません([`core/context.py` L521-544](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L521-L544))。
- **フックは編集対象**: Codex基盤では`.codex/hooks.json`が編集面に含まれます。許可イベントは`PreToolUse`、`PostToolUse`、`PermissionRequest`、`PreCompact`、`PostCompact`、`SessionStart`、`SubagentStart`、`SubagentStop`、`UserPromptSubmit`、`Stop`です([`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72))。検査器は`command`形式だけを受け付けます。形式の誤ったフックはエラーなしに**まったく実行されない**ため、提案者が見る時点で形式を強制すると書かれています([`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251))。

### 1.5 評価方法論

| 仕組み | 内容 | 出典 |
| --- | --- | --- |
| 点数のない実行ビュー | 方法が知る実行情報`RunView`は「決して点数を載せない」 | [`core/spec.py` L176-187](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L187) |
| 採点は選択の後だけ | `score()`は`core.judge`だけが、選択が確定した後にのみ呼ぶ。方法側のどのモジュールも`judge`をimportしない | [`core/spec.py` L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L247-L250)、[`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19)、[BENCHMARKS L34](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L34) |
| 採点失敗 ≠ 0点 | 失敗は`None`、分母から除外、0点としてキャッシュしない。未採点は別に報告 | [`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18)、[EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118)、[BENCHMARKS L67-68](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L67-L68) |
| 正解パスの遮断 | ベンチマークが宣言した`leak_globs`がコンテキストに入ると例外 | [`core/context.py` L399-416](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L416) |
| 採点痕跡のトリップワイヤー | 採点器の出力マーカー文字列がコンテキストファイルの名前・本文、またはエージェントが書いたハーネスにあれば拒否。「トリップワイヤーであって防御そのものではない。引っかかったらマーカー一覧を広げず、漏れている読み取り経路を探せ」 | [`core/context.py` L419-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L419-L518) |
| 測定語の禁止 | エージェントに見えるベンチマークの文言にbenchmark、evaluation、grader、rubric、scoreがあれば拒否:「仕事を描写せよ、測定を描写するな」 | [`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126) |
| 明示的な無採点の指示 | 編集者・選択者のプロンプトに「コンテキストに採点基準・正解・点数はない。採点者が望むものを推測するな」 | [`core/prompts.py` L41-53](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/prompts.py#L41-L53)、論文付録H |
| 匿名の選択 | 候補にA、B、…を付け、`task_id\|k\|mode`のシードでシャッフル(再実行しても同じ)。選択プールは最終候補k個だけで、基準実行は入れない | [`core/selection.py` L71-76](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L76)、[L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L93-L111) |
| 選択者失敗時の代替 | 選択者が失敗すると中立な代替(渡された基準実行、なければ最初の最終候補)を選び、`fallback`として記録 | [`core/selection.py` L237-252](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L237-L252) |
| 予算の恒等式 | 課題あたりの実行 R = 4k(基準 k + 候補 2k + 最終 k)、改善セッション P = 3k。ラベルが重複すると上書きとみなし、数値の検査より先に失敗させる | [`core/ledger.py` L15-33, L89-113](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L113) |
| 実行の同一性 | 完了マーカーにハーネスツリーのフィンガープリントを入れ、異なる構成から出た実行を再利用しない | [`core/runmark.py` L15-20, L41-61, L91-102](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L102) |
| 候補の多様性 | 候補ハーネス間の行単位Jaccardで、一つに収束していないかを測定 | [`core/tree.py` L407-427](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L407-L427) |
| ウェブアクセスの警告 | 公開ベンチマークなので採点基準がオンラインにある。検証実行でCodexの実行が**指示なしに自分の課題の採点基準をダウンロードした**。実行ホストでネットワークレベルの遮断を勧め、使った制限を結果とともに報告するよう求める | [EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109)、[README L166-171](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L166-L171) |
| ライブラリの範囲 | 実行・モード・領域単位で分離し、各実行はすべての領域を空の状態から始める。同じ領域内では先行する課題だけを読む | [`core/library.py` L15-24](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L15-L24)、[EXPERIMENTS L16-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L16-L19) |
| 経験項目 | `cue`・`lesson`・`evidence`がすべて揃って初めて保存(`confidence`は任意)。なければライブラリに入れない | [`core/library.py` L43-47, L106-123](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L43-L123)、[`core/selection.py` L494-501](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L494-L501) |

ベンチマークはJobBench、LAB、WorkBuddy-Benchの三つです([README L129-133](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L129-L133))。READMEと要旨が示す結果は、GLM-5とGemini 3.5 Flashで単一段階により、WorkBuddy-Bench最大11.5点、JobBench 4.5点、LAB部分通過率11.8%pの向上です([README L41-45](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L41-L45))。論文付録Fの限界は二つです。再帰の予算が増えると推論コストが増え、正解の監督がないため判断が実行のばらつきとモデル共通のバイアスに敏感です。これらの数値は直接再現していません。

### 1.6 ライセンス

- 本体: Apache 2.0([README L199-204](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/README.md#L199-L204))。このリポジトリがスキーマ・ツールに使う予定のApache-2.0(README「ライセンス」)と衝突しません。
- `third_party/`、ベンチマーク、データセットはそれぞれ上流のライセンスに従います。WorkBuddy-Benchは**地域制限のあるTencent独自ライセンス**です([BENCHMARKS L80-83](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/BENCHMARKS.md#L80-L83))。
- このノートは短い語句の引用とリンクだけを使い、コードは移していません。以下の提案文言も概念を私たちの言葉で書き直したもので、出典表記だけを残しています。

## 2. 対応表 — Harness²の概念 → Mallangable

判定: **採用**(ほぼそのまま)、**変形**(趣旨だけを取り入れる)、**拒否**。

| # | Harness²の概念 | Mallangableの位置 | 判定 | 理由 |
| --- | --- | --- | --- | --- |
| M1 | ハーネス = 編集可能なc1..c8のツリー | 5.6の定義(決定的な外殻) | **拒否**(定義の次元) | 私たちのハーネスはポリシー(policy)を*強制*する側です。エージェントがガードレール・フックを書き換える構造は、I8(権威ある執行は制御面だけ)と7.11「ポリシーファイル不変」に反します。手順(スキル・プロンプト)だけをオフラインで磨くことは可能 |
| M2 | フックの形式が誤っていると黙って実行されない、書き込み時点で形式検査 | 5.6「注意」、7.2 デバイスハーネスのフック | **採用** | フックが失敗すると開いたまま残る(fail-open)経路をもう一つ明らかにします。デバイスのフック設定は書き込み時点でスキーマを検査し、サーバーの受信検査(receive-check)が最終権威であるという既存の原則を補強 |
| M3 | Codexのフックイベント一覧 | 5.6「マッピング例」 | **変形** | Claude Code以外の二つ目の対応表候補です。ただし出典がHarness²の検査器であってCodexの公式ドキュメントではないので「要確認」と表示 |
| M4 | `RunView`に点数なし、採点は選択の後、採点痕跡のトリップワイヤー、`leak_globs` | 10.2 隠し検査、I7 | **採用** | Mallang-BenchのSBRは、隠し検査が本当に隠れていて初めて意味があります。隠し検査が生成・判定のコンテキストに漏れると、SBRは楽観的に歪みます |
| M5 | 採点失敗は`None`、分母から除外、別に報告 | 10.2「報告形式」 | **採用** | 失敗を0として入れるとCSRが下がり、除外して隠すと上がります。どちらも正直ではありません |
| M6 | ウェブアクセスによる採点基準の流出、ネットワーク制限の報告 | 10.2 構成・報告、7.3 外部通信の許可リスト | **採用** | 攻撃セット・抽出セット・隠し検査が公開されると同じ問題が起きます。7.3の許可リスト規則をベンチマーク実行の条件としても要求 |
| M7 | 測定語の禁止(仕事を描写せよ) | 10.2 リクエストセット | **採用** | リクエストセットの文に「検査」「採点」のような語があると、エージェントが測定そのものを狙う可能性があります |
| M8 | 匿名・シードシャッフルによる選択、基準実行の除外 | 5.8 G4 判定、5.7 判定者 | **変形** | 判定者(judge)が、候補がどの生成者(generator)・ハーネス・モデル経路から来たかを知らないようにします。I7(別インスタンス)に「出所ブラインド判定(source-blind judging)」を加えるもの |
| M9 | 予算の恒等式 R=4k、P=3k、ラベル重複検査 | 10.2 CPC、5.6 予算 | **変形** | コスト比較が公正であるには「何回実行し、何回判定したか」を併せて報告する必要があります。正確な恒等式はHarness²の方法にしか当てはまらないので、*報告項目*だけを取り入れる |
| M10 | ハーネスのフィンガープリントによる実行の同一性判別 | `change-record.schema.json` `provenance` | **採用** | 現在の`agent`は「役割@ハーネス」の文字列だけなので、ハーネスの*構成*が変わっても記録が同じです。内容ハッシュを置けば再現・監査・ベンチ比較ができます |
| M11 | 不正な提案は1回再試行した後、現状を維持 | 5.8 G1「失敗時」、5.6 予算 | **採用** | G1には「理由をエージェントに返す」しかなく、上限と終了状態がありません。コスト攻撃者(7.1)を考えると、上限と「変更なし」での終了が必要 |
| M12 | 領域別の経験ライブラリ(cue・lesson・evidence) | 5.3 `ResolutionCache`、6章 解決キャッシュ、7.5 範囲分離 | **変形** | 範囲分離はすでに7.5にあります。取り入れるのは「証拠フィールドのない教訓は保存しない」という保存条件と、ベンチでキャッシュを空の状態から始めたかを明かす報告項目 |
| M13 | Propose–Probe–Compose(正解なしの対照による改善) | 10.1 O1・O4、5.7 マージ担当・昇格担当 | **変形(任意)** | 対話型の変更一つに実行4k回は、時間ティア(time tier)(8.4)とコストに合いません。サーバージョブ(マージ・昇格)やO4判定者の信頼性研究の出発点としてだけ残す |
| M14 | `[ACTION]/[OBSERVATION]/[ERROR]`の軌跡文法 | 5.11 テレメトリー、G4 証拠 | **保留** | E4・E5イベントで同じ情報を作れます。判定者の入力形式を決めるときに改めて検討 |
| M15 | 候補の多様性(Jaccard) | — | **拒否** | 私たちの仕様には複数の候補を作る段階がありません(YAGNI) |
| M16 | 常時注入の長さ上限とその理由 | 5.10 コンテキスト供給 | **保留** | 役割別のコンテキスト予算を決めるときに参考にする数値です。現時点で仕様に入れる根拠は弱い |

## 3. 提案する編集の一覧(優先順、最大10)

各項目は最小限の編集です。文言はHarness²の文を移したものではなく、概念を書き直したものです。

### E-1. 10.2 Mallang-Benchに隠し検査の隔離規則を追加 (M4)

- ファイル: `docs/10-open-problems.md`、「### 構成」表のすぐ下
- 根拠: [`core/spec.py` L176-187, L247-250](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L176-L250)、[`core/judge.py` L15-19](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L15-L19)、[`core/context.py` L399-518](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/context.py#L399-L518)
- 提案文言:

```markdown
隠し検査の隔離 (必須(MUST)):
- 隠し検査とその結果は、解釈者・生成者・判定者のコンテキストに入らない。採点は有効化が終わった後に別プロセスが行う。
- 実行器は生成・判定のコンテキストを作るたびに、隠し検査ファイルのパスと検査結果のマーカー文字列を探し、見つかれば実行を止める。この検査は警報装置にすぎず、防御ではない。引っかかったらマーカー一覧を広げず、漏れている読み取り経路を直す。
(出典: Harness²の点数のない実行ビューと採点痕跡のトリップワイヤー、google-research/harness2 `core/spec.py`、`core/context.py`)
```

### E-2. 10.2「報告形式」に未採点の規則を追加 (M5)

- ファイル: `docs/10-open-problems.md`、「### 報告形式」段落の末尾
- 根拠: [`core/judge.py` L17-18](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/judge.py#L17-L18)、[EXPERIMENTS L117-118](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L117-L118)
- 提案文言:

```markdown
採点に失敗したリクエスト(隠し検査の実行エラー、判定モデルのエラー)は0点ではなく**未採点**である。指標の分母から除き、未採点の件数を指標と並べて報告する。例: 「CSR 0.71 (n=192, 未採点 8)」。
```

### E-3. 10.2「報告形式」に実行環境の報告項目を追加 (M6, M9, M12)

- ファイル: `docs/10-open-problems.md`、E-2の段落の次
- 根拠: [EXPERIMENTS L93-109](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/EXPERIMENTS.md#L93-L109)、[`core/ledger.py` L15-33](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/ledger.py#L15-L33)、[`core/library.py` L21-23](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/library.py#L21-L23)
- 提案文言:

```markdown
併せて報告する実行条件:
- **ネットワーク制限**: 生成エージェントがアクセスできたホストの一覧。隠し検査・攻撃セット・抽出セットをホストするアドレスは実行中に遮断する。公開ベンチマークでは、エージェントが指示なしに採点基準をダウンロードした事例が報告されている(Harness²の実験案内書)。
- **呼び出し数**: 成功した変更1件あたりの生成実行数と判定セッション数(再試行を含む)。CPCだけでは異なるハーネス同士を公正に比較できない。
- **キャッシュの状態**: 解決キャッシュ・学習した教訓を空の状態から始めたか、前のリクエストの結果を使わせたか。
```

### E-4. 5.8 G4に出所ブラインド判定を追加 (M8)

- ファイル: `docs/05-reference-architecture.md`、5.8 ゲート表の`G4 判定`行の「内容」欄
- 根拠: [`core/selection.py` L71-76, L93-111](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/selection.py#L71-L111)、論文§2.2.2
- 現在: `判定者がスクリーンショット・意図で意味の充足を判定`
- 提案: `判定者がスクリーンショット・意図で意味の充足を判定。判定者は成果物がどの生成者・ハーネス・モデル経路から来たかを知らない(出所ブラインド判定)。候補が複数あれば、再現可能なシードでシャッフルした匿名idで提示`

### E-5. 5.8 G1の失敗時に再試行上限を明記 (M11)

- ファイル: `docs/05-reference-architecture.md`、5.8 ゲート表の`G1 静的検査`行の「失敗時」欄
- 根拠: [`core/recursion.py` L15-19, L36, L242-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/recursion.py#L15-L251)、[`core/spec.py` L242-245](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L242-L245)
- 現在: `理由をエージェントに返す`
- 提案: `理由を修正可能な文でエージェントに返す。再試行上限(提案値: 1回)を超えたら、変更なしで現状を維持して終了`

### E-6. 5.6「注意」にフック失敗時の開放の警告を追加 (M2)

- ファイル: `docs/05-reference-architecture.md`、5.6 最後の「注意:」段落の後
- 根拠: [`core/tree.py` L216-251](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/tree.py#L216-L251)
- 提案文言:

```markdown
形式の誤ったフック設定は、多くのランタイムでエラーなしに**まったく実行されない。**つまり失敗すると開いたまま残る。ハーネスプラグインはフック設定を書き込む時点で、ランタイムが受け付けるイベント名・ハンドラー形式で検査し、セッション開始(E1)時にフックが実際に登録されたかを確認する。エージェントはポリシーフック・ガードレールファイルを書き換えられない(ツール境界、E4)。
(参考: Harness²は同じ理由でCodexのフックファイルを書き込み時点で検査する。google-research/harness2 `core/tree.py`)
```

### E-7. `change-record.schema.json`にハーネスのフィンガープリントフィールドを追加 (M10)

- ファイル: `schemas/change-record.schema.json`、`properties.provenance.properties`の`prompt_hash`の次
- 根拠: [`core/runmark.py` L15-20, L41-61](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/runmark.py#L15-L61)、[`substrate/base.py` L26-32](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/base.py#L26-L32)
- 提案フィールド(`required`は変えない、任意フィールド):

```json
"harness_digest": {
  "type": "string",
  "pattern": "^sha256:[0-9a-f]{64}$",
  "description": "変更を作ったハーネス構成(スキル・フック・ポリシーの写し・ツール一覧)の内容ハッシュ。同じagent文字列でも構成が異なれば値も異なる"
}
```

- 備考: Harness²はSHA-1の先頭16文字を使います。ここでは既存の`prompt_hash`形式に合わせてSHA-256全体を提案します。反映したら`examples/change.example.yaml`の検証を再実行する必要があります(任意フィールドなので、既存の例はそのまま通るのが正常)。

### E-8. 10.2 リクエストセットに測定語の禁止を追加 (M7)

- ファイル: `docs/10-open-problems.md`、「### 構成」表の`リクエストセット`行の「内容」欄の末尾
- 根拠: [`core/spec.py` L111-126](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/core/spec.py#L111-L126)
- 付け加える文言: `。リクエスト文はやるべきことだけを述べ、測定は述べない(「検査」「採点」「点数」などは禁止)`

### E-9. 5.6 対応表にCodex列の候補を追加 (M3)

- ファイル: `docs/05-reference-architecture.md`、「### マッピング例: Claude Code フック」表の後に短い段落
- 根拠: [`substrate/codex.py` L58-72](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/harness2/substrate/codex.py#L58-L72) (Codexの公式ドキュメントではない二次出典)
- 提案文言:

```markdown
Codex CLIも同じ方式で対応します(E1 `SessionStart`、E2 `UserPromptSubmit`、E4 `PreToolUse`、E5 `PostToolUse`、E6 `PermissionRequest`、E11 `Stop`、E12 `SubagentStop`、E15 `PreCompact`)。この一覧はHarness²が検査するイベント集合から取ったものなので、反映前にCodexの公式ドキュメントと照合する必要があります。
```

### E-10. 参考文献にHarness²を追加

- ファイル: `docs/references.md`、「## エージェントのセキュリティ」の前に新しい節
- 提案文言:

```markdown
## ハーネスの改善と評価

- R. Xu, Y. Chen, Z. CuiZhu, B. Dalvi Mishra, Y. Ming, H. Yu, R. Han, C.-Y. Lee, T. Pfister. "Harness²: Recursive Agent Harnessing for an Open World." arXiv:2610.14224, 2026. https://arxiv.org/abs/2610.14224 · コード(Apache-2.0): https://github.com/google-research/harness2
  - 隠し検査の隔離、未採点の報告、出所ブラインド判定、ハーネスのフィンガープリント(5.6、5.8、10.2)の根拠。調査ノート: [research/harness2-analysis.md](harness2-analysis.md)
```

## 4. 入れなかったもの

- **自己編集ハーネス(M1)**: ユーザーのアプリを書き換えるエージェントが自らのポリシーフックまで書き換えると、5.6がハーネスを定義した理由(「非決定的なエージェントを包む決定的な外殻」)が失われます。
- **Propose–Probe–Composeを基本の生成フロー(5.4)に入れること**: 変更一つに実行4k回がかかり、T0~T2の時間ティアを守れません。使いどころはサーバージョブの実験的な選択肢とO4の研究です。
- **ベンチマーク数値の引用**: 直接再現しておらず、私たちの問題(アプリの修正)とは課題の分布が異なります。
