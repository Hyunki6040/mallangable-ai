<!-- LANG-BAR -->
[English](../../en/research/thinkrail-analysis.md) · [한국어](../../ko/research/thinkrail-analysis.md) · [简体中文](../../zh-CN/research/thinkrail-analysis.md) · **日本語** · [Español](../../es/research/thinkrail-analysis.md)
<!-- /LANG-BAR -->

# 調査ノート — ThinkRail (JetBrains/thinkrail)

> このノートの結論: ThinkRail は `pi` コーディングエージェントを包む**エージェント IDE ホスト(host)** である。ユーザーのアプリを修正する Mallangable とは対象が異なるが、「エージェントが作った変更(change)を人が安全に受け入れられるようにするホスト」という問題は同じだ。そのまま取り入れるものは5つある。① **見たものを根拠にした取り消し(revert)**(CAS)。② **判定出力は信用しない**(形式が誤っていれば失敗、ホストのフィールドはホストが埋める)。③ **承認(approval)は対象の指紋に結びつけられ、範囲が決まっている。** ④ **受け入れた信頼はその時点の内容にだけ及ぶ**(後から生じた項目は再確認する)。⑤ **保存データには翻訳文を入れず、用語パック(lexicon pack)はデータにすぎず、共有物が書き換えることはできない。** 逆に「ホストはプロンプトを組み立てない」という原則は受け入れない。Mallangable のハーネス(harness)は強制する側だからだ。

- 確認日: 2026-11-03
- 調査対象: https://github.com/JetBrains/thinkrail (公開、Apache-2.0、JetBrains インキュベーター)。検索結果に出てくる同名のリポジトリのいくつかは、このリポジトリのフォークです。
- 固定コミット: `c10f8808cee693e4abffeeb1844a132ed0a91cc5` (2026-11-03)。以下のリンクはすべてこのコミット基準です。
- 方法: `git clone --depth 1` で空の一時ディレクトリに取得し、仕様文書(`SPEC.md`・`architecture.md`・`goal-and-requirements.md`)だけを**読みました。** コードは実行していません。

## 0. 確認したことと、できなかったこと

| 項目 | 状態 | 根拠 |
| --- | --- | --- |
| リポジトリの存在・公開状況 | 確認 | `gh repo view JetBrains/thinkrail`、クローン成功 |
| ライセンス | 確認 | [`LICENSE`](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/LICENSE) Apache 2.0。このリポジトリのスキーマ・ツールの方針(Apache-2.0)と衝突なし |
| 製品目標・アーキテクチャ文書 | 直接読んだ | `goal-and-requirements.md`, `architecture.md` |
| サーバーのサブモジュール仕様 | 一部読んだ | `changes`, `host/planReview`, `agent`, `agent/mcp`, `agent/packages`, `extensions`, `todos`, `spec-graph`。残りの `SPEC.md` は読んでいない |
| 仕様と実装の一致 | 未確認 | 仕様文書だけを読み、ソース・テストは読んでいない。以下の引用は「ThinkRail の仕様がこう定めている」という意味です |
| 実行・再現 | 行っていない | 調査範囲外 |

## 1. ThinkRail とは何か

`pi` エージェントをプロセス内で動かし、その上にエディター・diff・ターミナル・レビュー UI を載せたホストです([`goal-and-requirements.md` L10-16](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L10-L16))。3つの輪に分かれます。エンジンホスト、バージョン付きの通信契約(wire)、UI クライアントです([`architecture.md` L19-28](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L19-L28))。作業空間は git worktree なので、複数のエージェントが互いにぶつからず並行して作業します([`architecture.md` L107-122](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L107-L122))。

原則のうち、Mallangable と重なるものと分かれるもの:

| ThinkRail の原則 | Mallangable との関係 |
| --- | --- |
| **信頼は明示的である**: クローンしたリポジトリがエージェントに入れられるもの(スキル・拡張・MCP サーバー)は、プロジェクト単位の信頼承認の後にのみ読み込む。リポジトリが定義した MCP サーバーは項目ごとの承認が別途必要で、項目が変わると承認が消える ([L62-65](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L62-L65)) | 同じ方向。共有された機能(6.9)と I4 に対応 |
| **注入ではなく供給によってのみ影響する**: ホストはプロンプトを組み立てない ([L57-58](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L57-L58)) | 分かれる。Mallangable のハーネス(5.6)はポリシーを強制し、役割ごとのコンテキストを選ぶ(5.10) |
| **再計算せずに見せる**: ホストはエンジンが報告した値をそのまま見せる ([L59](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L59)) | 同じ方向。コスト表示(8.10)は `ModelPort` の計量値を使う |

## 2. 対応表 — ThinkRail の概念 → Mallangable

判定: **採用**(ほぼそのまま)、**変形**(趣旨だけ取り入れる)、**確認**(すでにある、根拠だけ追加)、**却下**、**保留**。

| # | ThinkRail の概念 | 出典 | Mallangable の位置 | 判定 | 理由 |
| --- | --- | --- | --- | --- | --- |
| T1 | 取り消し要求は「ユーザーが見たもの」のハッシュを持ってきて、現在の状態と異なれば `STALE_VIEW` で何も書かない。クライアントは内容を送らない | [`changes/SPEC.md` L39-43, L116-118](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/changes/SPEC.md#L39-L43) | 5.5, I3 | **採用** | ベースライン(baseline)の伝播(propagation)・別の端末・監視者の自動復旧が、有効な状態を動かしうる。「さっきのを取り消して」が見当違いの状態を取り消すと、F1 がかえって事故になる |
| T2 | 取り消しレシートの id がそのままやり直し(redo)トークンになる。やり直しも同じ演算。知らない id は黙って見過ごさず `RECEIPT_UNKNOWN` | [`changes/SPEC.md` L81-112](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/changes/SPEC.md#L81-L112) | 5.5, 8.7 | **変形** | Mallangable の取り消しはポインタ移動なので、バイトリングは不要。取り入れるのは「やり直し = 同じ演算」と「できなければ明示的に知らせる」 |
| T3 | 元データの読み取り失敗は不在ではない。不在として読むと、ファイル全体の取り消しがユーザーのファイルをゴミ箱に送る | [`changes/SPEC.md` L119-122](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/changes/SPEC.md#L119-L122) | 6.5, 2.3(`null` = 削除) | **採用** | ⊕ において `null` はキーの削除だ。上位レイヤー(layer)を読めなかったことを「なし」として扱うと、伝播がユーザーの機能を消してしまう |
| T4 | レビュアーの出力は信用しない: 判定語は厳格に検査し、形式が誤っていれば承認ではなく失敗。結果オブジェクトは明示的に作り直し、モデルがでっち上げたホスト専用フィールドを捨てる。指摘のない「修正要求」は拒否 | [`host/planReview.SPEC.md` L62-81](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L62-L81) | 5.8 G4, E12 | **採用** | E12 には「判定結果のスキーマ検査」しかなく、検査に失敗したときの結果が決まっていない |
| T5 | 承認は判定であって確定ではない: 未解決の指摘が残っていれば approve も確定しない | [`host/planReview.SPEC.md` L102-106](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L102-L106) | 5.8 G4 | **採用** | 再判定ラウンドが以前の指摘を覆い隠す経路を防ぐ |
| T6 | 2つの入口(エージェントのツール・人のボタン)が同じ修正回数の上限を共有する。共有しないと、修正→判定→修正が無限に繰り返される | [`host/planReview.SPEC.md` L117-119](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L117-L119) | 5.8 G1 の再試行上限 | **採用** | G1 の上限が1つの経路にしかかからなければ、コスト攻撃者(7.1)は別の経路で回す |
| T7 | 判定者(judge)をセッションではなく、結果を返すサブタスクとして置く。終われば結果、失敗すれば拒否、回復は一か所 | [`host/planReview.SPEC.md` L21-42](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/host/planReview.SPEC.md#L21-L42) | 5.7 判定者 | **確認** | すでに判定者は読み取り専用で、書けるのは判定結果だけだ。根拠としてのみ引用 |
| T8 | MCP ツール呼び出しの確認: `readOnlyHint` がない呼び出しだけを尋ねる。選択肢は拒否・今回だけ・この会話で・常に。「常に」はプロジェクト範囲で、対象(`command`+`args` または `url`)の SHA-256 が同じときだけ有効。肯定の答え以外のすべて(閉じる、別のメッセージ、中断)は拒否 | [`agent/mcp/SPEC.md` L129-150](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/mcp/SPEC.md#L129-L150) | 4.8, G5, 8.5 | **変形** | 承認疲れ(4.10)を減らしつつ、承認が別の対象に漏れないようにする。Mallangable には承認の範囲・寿命のルールがない |
| T9 | 信頼を与えると、**その時点にあったものだけ**を確認済みとみなす。後から pull・ブランチで生じたスキルは `pending-ack` | [`agent/SPEC.md` L993-1000](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/SPEC.md#L993-L1000) | 6.9 `subscribe` 共有 | **採用** | 購読型の共有は、送り手が直すたびに内容が変わる。最初の受諾がその後の内容まで覆うと、7.7 の「インストール後にリモートで内容を変えた」と同じ穴が生じる |
| T10 | 同じ名前なら信頼の高い側が勝つ: 内蔵 → 個人 → プロジェクトの順。リポジトリは自分のスキルを隠せない。内蔵拡張は有効な間、同名ツールの衝突で勝つ | [`agent/SPEC.md` L991-992](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/SPEC.md#L991-L992), [`extensions/SPEC.md` L32-37](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/extensions/SPEC.md#L32-L37) | 6.9, O3 | **変形** | Mallangable のレイヤー合成は「ユーザーに近い側が勝つ」だ。そのルールはそのまま残し、**受け取った共有物**がコマンド・ショートカットのような識別子を横取りする場合にだけ適用 |
| T11 | オフスイッチは、拡張が寄与したすべて(ファクトリー・ツール・スキル)をまとめて無効にする。レンダラーは残し、過去の記録は引き続き見える | [`architecture.md` L376-382](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L376-L382) | 5.9 監視者・セーフモード(safe mode) | **採用** | 1つの機能が複数のスロット・コマンド・フックにまたがるなら、スロット1つだけを無効にする隔離は半分にすぎない |
| T12 | 一覧の取得は副作用がない: カタログはインストールも拡張コードの実行もしない。ツール名は実際のロードが記録したものから読む。一覧のたびにファクトリーを回していた方式は却下された | [`agent/packages/SPEC.md` L23-25, L128-131](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/packages/SPEC.md#L23-L25) | 7.7, 7.11 | **採用** | 共有・マーケットのプレビュー画面で D4 コードを動かすと、承認前の実行になる(5.9「承認前の D4 は権限 0」に違反) |
| T13 | 計画のステップごとに作業ウィンドウ(開始時点の基準線)を開き、終わったら**そのステップが変えたパスだけ**をコミットする。別の会話とウィンドウが重なれば `shared` と表示し、帰属を推測しない | [`todos/SPEC.md` L64-80](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/todos/SPEC.md#L64-L80) | 6.4, 記録者 | **変形** | 同じユーザーの生成作業2つが1つのレイヤーで重なると、どの機能の変更なのかがぼやける(I9) |
| T14 | `agent_end` は試行の境界にすぎない(再試行・圧縮の後にさらに作業しうる)。`agent_settled` だけが完了。入力待ちはレベル信号なので、見ただけでは消えない | [`architecture.md` L141-156](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L141-L156) | 5.6 AG-UI 対応, 8.5 状態語 | **採用** | 再試行の途中で「準備できました」が出ると、状態語の固定ルール(8.5)が崩れる |
| T15 | 互換性台帳: エンジンの欠陥・欠けた API を埋める適応ごとに「アップグレード時に見直すこと」と「削除してよい条件」を書く。仕様はバージョン番号を書き直さず、何を確認したかを書く | [`pi-compatibility.md` L11-16](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/pi-compatibility.md#L11-L16), [`architecture.md` L205-211](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L205-L211) | 5.6 対応表 | **採用** | 5.6 の Claude Code 表の `onFailure` のバージョン条件のように、対応表の項目はランタイムのバージョンによって古くなる |
| T16 | UI 文字列はキーカタログ。ハードコードされた文字列はリントで失敗。保存・通信データには翻訳文を入れず、レンダリング時に文章化。ユーザーの言語ファイルはグローバルなデータフォルダーからのみ読む(クローンしたリポジトリが UI を書き換えられないように)。フォールバック順: ローカル完全一致 → 内蔵完全一致 → 内蔵デフォルト → 英語 | [`architecture.md` L430-454](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L430-L454) | 8.9 用語パック | **採用** | キーカタログ・リントはすでにある。欠けているのは保存ルール、出所の制限、フォールバック順。出所の制限がないと、共有物が権限警告の文言(「患者情報へのアクセス」)を穏やかな言葉に変えられる |
| T17 | エージェント・ツールの出力は翻訳しない | [`architecture.md` L443-444](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L443-L444) | 8.9 適用箇所(E13 説明者) | **却下** | ThinkRail のユーザーは開発者だ。Mallangable の basic ユーザーには、説明者が一般的な言葉で書き直す必要がある |
| T18 | サブエージェントの信頼は、親が**読み込んだ**信頼と現在の記録の両方を超えられない。撤回すれば子も従う | [`agent/SPEC.md` L1443-1452](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/packages/server/src/agent/SPEC.md#L1443-L1452) | 5.7 役割, I4 | **確認** | I4・役割分離ですでに保証されている。根拠としてのみ引用 |
| T19 | レビューコメントはエンジン中立のセレクター(`lineRange`・`textQuote`・`json-pointer`・`region` など)で付け、レンダラーが「置けた/置けなかった」を報告する | [`architecture.md` L330-346](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/architecture.md#L330-L346) | 8.2 画面の指し示し, 6.12 | **保留** | ベースラインが変わった後に、指し示しのアンカーが黙って別の要素に付いてしまう問題と同じだ。ケイパビリティマップ(capability map)の形式を確定するとき(10.4 ロードマップ)に再検討する |
| T20 | ホストがプロンプトを組み立てない | [`goal-and-requirements.md` L57-58](https://github.com/JetBrains/thinkrail/blob/c10f8808cee693e4abffeeb1844a132ed0a91cc5/goal-and-requirements.md#L57-L58) | 5.6, 5.10 | **却下** | ハーネスは「非決定的なエージェントを包む決定的な外殻」だ(5.6)。コンテキストの供給(5.10)は I6 を守る手段である |

## 3. 反映した編集

文言は ThinkRail の文を移したものではなく概念を書き直したもので、それぞれの箇所に出典を残しました。

| # | 対応 | ファイル・位置 | 内容 |
| --- | --- | --- | --- |
| E-1 | T4・T5・T6 | `docs/05-reference-architecture.md` 5.8 「判定出力の処理」 | 形式エラー = 失敗、ホストのフィールドはホストが、指摘のない修正要求は拒否、未解決の指摘があれば確定しない、再試行の上限はすべての入口で共有 |
| E-2 | T1・T2 | 5.5 「取り消しは見たものを根拠に」 | `revert(expect=見た状態 id)`、異なれば何もせず現在の状態を提示、やり直し = 同じ演算、できなければ明示的に通知 |
| E-3 | T11 | 5.9 「監視者とセーフモード」 | 隔離・無効化の単位は機能全体。レシート・記録は引き続き見える |
| E-4 | T14 | 5.6 AG-UI 対応の下 | 試行の境界 ≠ 完了、承認待ちはレベル信号 |
| E-5 | T15 | 5.6 マッピング例の下 | 対応表の項目ごとに、確認した動作・再確認の条件・削除の条件 |
| E-6 | T8 | `docs/04-control-spectrum.md` 4.8 配置原則 | 承認範囲は3種類、承認 = 対象の指紋に結びつく、肯定以外の応答は拒否、読み取り専用は尋ねない |
| E-7 | T3 | `docs/06-versioning-and-lineage.md` 6.5 ルール | 読み取り失敗を削除(`null`)として扱わない |
| E-8 | T13 | 6.4 | 同時生成は作業コピーを別々に、記録は自分のパスだけ、重なれば帰属の推測を禁止 |
| E-9 | T9・T10 | 6.9 ルール | 受諾はその時点の内容にだけ、受け取った共有物は識別子を横取りできない |
| E-10 | T12 | `docs/07-trust-and-security.md` 7.11 | 一覧・プレビュー・権限表示は、コードを実行せずマニフェストから |
| E-11 | T16 | `docs/08-experience-design.md` 8.9 「保存と出所」 | 概念 id + 引数で保存、用語パックの出所制限、フォールバック順 |

## 4. 入れなかったもの

- **スキーマの変更**: E-6 の「承認 = 対象の指紋」をスキーマのフィールドとして入れることは見送りました。現在のルールは既存の `permissions_delta`・`approved_by` で表現されます。承認記録を変更記録とは別に保存する形式を決めるときに入れます。
- **worktree ベースの作業空間をそのまま**: Mallangable の隔離単位はリポジトリ、作業単位はブランチです(6.4)。作業コピーをどう作るか(worktree・一時クローン)は実装の選択に委ねます。
- **正確なバージョン固定ルール(architecture の決定 10)**: リポジトリの運用ルールであって、仕様の内容ではありません。「仕様はバージョンを書き直さず、何を確認したかを書く」という趣旨だけを E-5 に反映しました。
- **レシートリングの上限(20個・64 MiB)**: Mallangable の取り消しはポインタ移動なので該当しません。
