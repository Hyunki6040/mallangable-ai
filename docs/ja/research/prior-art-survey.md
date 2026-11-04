<!-- LANG-BAR -->
[English](../../en/research/prior-art-survey.md) · [한국어](../../ko/research/prior-art-survey.md) · [简体中文](../../zh-CN/research/prior-art-survey.md) · **日本語** · [Español](../../es/research/prior-art-survey.md)
<!-- /LANG-BAR -->

# 調査ノート — 先行事例の調査(オープンソース・仕様・エージェント標準)

> このノートの結論: この仕様が新たに定義したもの(契約保存マージ(contract-preserving merge)、系譜(lineage)の伝播(propagation)、区間委任、ユーザー権利の下限(user floor rights))と**重なる標準はない。**ただし周辺部品はすでに標準化されており、現在の仕様はその名前を使っていないか、二次出典として引用している。取り入れるものは五系統である。① 宣言的なレイヤー合成`⊕`の基本的な意味を**JSON Merge Patch(RFC 7396)** に固定し、リストのマージ規則はKubernetes Server-Side Applyのように**スキーマが宣言**するようにする。② 情報フローのラベル(7.5)に**完全性の軸**を加える(FIDES・CaMeL)。③ ポリシーの単調縮小(I5)を**Cedarのポリシー包含検証**で機械的に確認する。④ テレメトリー(5.11)を**OpenTelemetry GenAIの属性名**に合わせる。⑤ MCP最新版(2026-07-28)の**URLモードelicitation**とSamplingの廃止をモデル接続(8.10)に反映する。

- 確認日: 2026-10-30
- 方法: リポジトリは`gh api`でメタデータ・ライセンスファイル・仕様原文を読み、ウェブ文書は公式サイトのものだけを取得しました。コードは実行していません。引用したURLはすべて`curl -L`で200応答を確認しました(ACMデジタルライブラリは自動リクエストを403で遮断するため、DOIだけを記しました)。
- 範囲: この章は既存の文書を修正しません。3節の編集案を反映するかどうかは別途決定します。

## 0. 確認できたこととできなかったこと

| 項目 | 状態 | 備考 |
| --- | --- | --- |
| MCP最新改訂版 | 確認 | `2026-07-28`(2026-07-28リリース)。リポジトリの`docs/specification/2026-07-28/changelog.mdx`原文 |
| MCP Apps | 確認 | `modelcontextprotocol/ext-apps`の`specification/2026-01-26/apps.mdx`。拡張id `io.modelcontextprotocol/ui` |
| OpenTelemetry GenAI規約 | 確認 | `open-telemetry/semantic-conventions`から**`semantic-conventions-genai`リポジトリへ移動**。文書の状態はすべてDevelopment |
| A2UI | 確認 | リポジトリが`a2ui-project/a2ui`へ移動。現在v0.9.1、v1.0はRC |
| Cedarの決定規則・検証器 | 確認 | 公式ドキュメントと`cedar-policy-symcc`のREADME |
| Patchworkの内部構造 | 一部 | プロジェクトページと実験ノート07だけを読んだ。`inkandswitch/patchwork-system`リポジトリにはライセンス表記なし |
| Boxerの原文 | 読めず | ACMが自動リクエストを遮断。書誌情報だけを確認 |
| Chrome・Figma・VS Codeのドキュメントのライセンス | 未確認 | 製品ドキュメントなので引用のみとし、文言は移さない |

## 1. 項目別の調査

判定: **採用** = 引用し、フィールド名・意味を合わせる / **参考** = 関連研究として引用のみ / **無関係** = 入れない。
「対応」欄はこの仕様の節番号とスキーマファイルです。

### 1.1 マリアブル・ソフトウェアの研究

| 項目 | 何か | 一次出典 | ライセンス | 対応 | 判定 |
| --- | --- | --- | --- | --- | --- |
| Malleable softwareのエッセイ (Ink & Switch, 2025) | 閉ざされたアプリからユーザーの主体性を取り戻そうというエッセイ。緩やかな勾配・ローカル開発者の概念を整理 | https://www.inkandswitch.com/essay/malleable-software/ | エッセイ(表記なし) | 1.5、2.6 | すでに引用済み。維持 |
| Potluck (2022) | テキストの上に検索・数式・動的な注釈を重ね、段階的に構造を加える。注釈は原文を変えない重ね合わせのレイヤー | https://www.inkandswitch.com/potluck/ | エッセイ | 2.3 レイヤー、2.6 D1~D3 | **参考**。「原本に手を触れない重ね合わせのレイヤー」の先例 |
| Embark (2023) | 旅行計画の文書一つにデータ・計算・ビューをまとめて置き、アプリを解体 | https://www.inkandswitch.com/embark/ | エッセイ | 10.1 O8 (アプリを越えるツール) | **参考** |
| Patchwork (2024~) | 文章・絵などの非コード文書の汎用バージョン管理。実験ノートでは**AIボットがブランチで編集し、人がdiffを見て一部だけをマージし、履歴にボットの編集が表示される** | https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/ | リポジトリに表記なし | 6.4 `exp/*`ブランチ、6.11 `Agent:`トレーラー、8.6 レシート | **参考**。現在のreferences.mdの「Universal Version Control」リンクは研究室の一覧ページなので、Patchworkのページに替えるほうが正確 |
| Cambria (2020) | 双方向レンズでスキーマバージョン間のデータを変換 | https://www.inkandswitch.com/cambria/ · https://github.com/inkandswitch/cambria-project | MIT | 5.9 `migrate(prev)`、`extension-manifest` `state.migrate_from` | **参考**。状態の引き継ぎを単方向の`migrate`とした現在の設計で十分。双方向が必要になったときの根拠 |
| Webstrates (UIST 2015) | DOMの変更を同期し、文書とアプリの境界をぼかす。可塑性・共有・分散・計算の4原則 | https://webstrates.net/ · https://github.com/Webstrates/Webstrates | Apache-2.0 | 6.13 CRDT上のコードのリスク | **参考**。実行コードをリアルタイムで共有した先例なので、S7の根拠事例に適している |
| Boxer (diSessa & Abelson, CACM 29(9), 1986) | 非専門家が組み立て直せる計算メディア | DOI 10.1145/6592.6595 | 論文 | 1.5 | **参考**。Smalltalkの系譜は一次出典を探していないため除外 |

### 1.2 拡張・プラグインのマニフェスト

| 項目 | 何か | 一次出典 | ライセンス | 対応 | 判定 |
| --- | --- | --- | --- | --- | --- |
| VS Codeのコントリビューションポイント・アクティベーションイベント | `contributes`(commands・menus・views・keybindings・configuration・`languageModelTools`など)で拡張ポイント(extension point)を宣言。1.74からはコントリビューションポイントがアクティベーションイベントを自動的に暗示 | https://code.visualstudio.com/api/references/contribution-points · https://code.visualstudio.com/api/references/activation-events | コードMIT、ドキュメントは未確認 | 2.2 拡張ポイント`kind`、`capability-map` | **参考**。`kind`(token・command・view・hook・service)との対応が自然 |
| VS Code Workspace Trust | `capabilities.untrustedWorkspaces.supported: true / false / "limited"`。信頼されていないワークスペースはRestricted Modeで開かれ、自動実行が止められる | https://code.visualstudio.com/api/extension-guides/workspace-trust | ドキュメント | 4.6 F2 セーフモード、6.9 受け取った共有 | **参考** |
| Chrome MV3の権限 | `permissions`・`optional_permissions`・`host_permissions`・`optional_host_permissions`。**警告が付く権限をアップデートで追加すると、ユーザーが承諾するまで拡張がオフになる** | https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions | ドキュメント | I4、6.5 `delta_permissions`、6.9 subscribe | **参考**。I4の実際の大規模な先例。現在の仕様の規則(権限の増加 → 提案)と同じ方向 |
| Figmaのプラグインマニフェスト | `networkAccess.allowedDomains`(`["none"]`も可)・`reasoning`(ワイルドカードなら必須)・`devAllowedDomains`、`permissions` | https://developers.figma.com/docs/plugins/manifest/ | ドキュメント | `extension-manifest` `network.allow` | **参考**。「許可理由」フィールドは4節の候補 |
| Obsidianのコミュニティプラグイン | 公式ドキュメントが「プラグインを特定の権限に制限することはできない」、ファイル・ネットワーク・プログラムのインストールにアクセスできると明記。既定はRestricted mode | https://obsidian.md/help/plugin-security | アプリは独占、`obsidian-api`はMIT | 7.6、7.7 | **参考**。隔離のない拡張の反例として引用する価値あり |
| WASM Component Model / WIT | `world`がコンポーネントのimport・exportを宣言し、ホストはimportしたものだけを供給。パッケージにバージョン(`wasi:http@0.2.0`) | https://component-model.bytecodealliance.org/design/wit.html · https://github.com/WebAssembly/component-model | Apache-2.0 | 7.6 オブジェクトケイパビリティ、`SandboxHost` `lang`アダプター、マニフェスト`permissions` | **参考**。`wasm`成果物なら、マニフェスト`permissions` ↔ worldのimportで1:1対応が可能 |
| Extism | WASMプラグインフレームワーク。マニフェストに`wasm[].hash`、`memory.max_pages`、`allowed_hosts`、`allowed_paths`、`config` | https://extism.org/docs/concepts/manifest · https://github.com/extism/extism | BSD-3-Clause | `extension-manifest` `artifact.content_hash`、`network.allow`、`resources.memory_mb` | **参考**。同じ概念がすでにある。名前を合わせる理由は弱い |
| Tauri v2 capability | すでに引用済み | (references.md) | | 7.6 | 維持 |
| Endo / SES | すでに引用済み | (references.md) | Apache-2.0 | 7.6 | 維持 |

### 1.3 エージェントプロトコル・ハーネスイベント

| 項目 | 何か | 一次出典 | ライセンス | 対応 | 判定 |
| --- | --- | --- | --- | --- | --- |
| MCP 2026-07-28 | ステートレス化(`initialize`の削除、リクエストごとに`_meta`にバージョン・クライアント能力)、`server/discover`、多重往復リクエスト(MRTR: `resultType: "input_required"`)、tasksは公式拡張へ移動、**Roots・Sampling・Loggingは廃止予定**、`_meta`の`traceparent`規約(SEP-414) | https://modelcontextprotocol.io/specification/2026-07-28/changelog | Apache-2.0(仕様、MITから移行中)、ドキュメントはCC-BY-4.0 | 5.3 `ModelPort`、5.6、8.10 | **採用**。8.10の`sub`経路をMCP Samplingの上に設計してはならない |
| MCPツールのannotations | `readOnlyHint`・`destructiveHint`・`idempotentHint`・`openWorldHint`。**信頼されたサーバーでなければ、クライアントはannotationsを信じてはならない(MUST)** | https://modelcontextprotocol.io/specification/2026-07-28/server/tools | 同上 | `capability-map` `capability.risk` | **採用**。`risk`の値との対応表を置く(3節 E-10) |
| MCP elicitation | formモードとURLモード。**秘密値・資格情報はformモードで受け取ってはならず、URLモードを使わなければならない(MUST)** | https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation | 同上 | 8.10 接続キー、I6 | **採用** |
| MCPの認可 | OAuth 2.1、Protected Resource Metadata(RFC 9728)、リソース指示子(RFC 8707)、`iss`の検証(RFC 9207) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | 同上 | 2.1 委任、7.2 | **参考**。エージェントαが「人から委任を受けた短期の主体」であるというI4・I9の説明の実装根拠 |
| MCP Apps (SEP-1865) | `ui://`リソース、`text/html;profile=mcp-app`、サンドボックスiframeの義務、`_meta.ui.csp`(`connectDomains`・`resourceDomains`・`frameDomains`・`baseUriDomains`)、`permissions`(camera・microphone・geolocation・clipboardWrite) | https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx | 同上 | 3.2 A4 `frame`、`extension-manifest` `network` | すでに引用済み。**採用を維持**。日付付きの仕様パスでリンクを固定 |
| MCP-UI | MCP Appsの原型。現在はMCP Apps互換のSDK | https://github.com/MCP-UI-Org/mcp-ui | Apache-2.0 | | **無関係**(MCP Appsで十分) |
| AG-UI | エージェント↔フロントエンドのイベントプロトコル。`RUN_STARTED`/`RUN_FINISHED`/`RUN_ERROR`、`STEP_*`、`TOOL_CALL_*`、`STATE_SNAPSHOT`/`STATE_DELTA`(**RFC 6902 JSON Patch**)、`SUBAGENT_*`。人による承認は`RunFinished`の`outcome: { type: "interrupt" }`の後、`resume[]`で新しい実行 | https://docs.ag-ui.com/concepts/events · https://docs.ag-ui.com/concepts/interrupts · https://github.com/ag-ui-protocol/ag-ui | MIT | 5.6 イベントモデル、8.5 進行表現、2.8 `承認待ち` | **採用**(対応表)。体験面↔生成面の間の伝送規格としてそのまま使える |
| A2A v1.0 | 不透明なエージェント間の作業プロトコル。`AgentCard`、作業状態`TASK_STATE_SUBMITTED / WORKING / INPUT_REQUIRED / AUTH_REQUIRED / COMPLETED / FAILED / CANCELED / REJECTED` | https://a2a-protocol.org/latest/specification/ · https://github.com/a2aproject/A2A | Apache-2.0 | 5.3 `JobOrchestrator`、2.8 ライフサイクル | **参考**。サーバーのマージ・昇格ジョブを外部エージェントに任せるときのアダプター候補 |
| OpenTelemetry GenAI規約 | `gen_ai.operation.name`(`invoke_agent`・`execute_tool`・`create_agent`・`invoke_workflow`)、`gen_ai.agent.id`、`gen_ai.usage.input_tokens`・`output_tokens`、`gen_ai.tool.name`、MCP属性`mcp.method.name`。**状態はDevelopment** | https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/ | Apache-2.0 | 5.11 テレメトリー | **採用**(属性名のみ)。安定版ではないのでバージョンの固定が必要 |
| OpenAI Agents SDKのトレーシング | trace(`workflow_name`・`trace_id`・`group_id`)、span(`agent`・`generation`・`function`・`guardrail`・`handoff`・`custom`)、`trace_include_sensitive_data` | https://openai.github.io/openai-agents-python/tracing/ · https://github.com/openai/openai-agents-python | MIT | 5.11、7.5 解除規則 | **参考**。機微データを既定で含める(True)のは、この仕様の既定値と逆 |
| Claude Codeのフック | イベント32個、ハンドラー5種(`command`・`http`・`mcp_tool`・`prompt`・`agent`)、`PreToolUse`の`permissionDecision`(`allow`・`deny`・`ask`・`defer`)・`updatedInput`、管理設定`allowManagedHooksOnly` | https://code.claude.com/docs/en/hooks.md | 製品ドキュメント | 5.6 対応表 | すでに引用済み。対応表に`PostToolUseFailure`(E5)、`Elicitation`(E6)を追加可能 |
| Claude Codeのプラグイン | `.claude-plugin/plugin.json`(`name`のみ必須、`skills`・`hooks`・`mcpServers`・`userConfig`の`sensitive`)、`claude plugin validate` | https://code.claude.com/docs/en/plugins-reference | 製品ドキュメント | 5.6 ハーネスの配布、8.10 `sub` | すでに引用済み。**references.mdのリンクがスペイン語版(`/docs/es/`)なので、英語版のリファレンスに差し替え** |
| Agent Skills仕様 | `SKILL.md`冒頭の`name`(64文字)・`description`(1024文字)・`license`・`compatibility`・`metadata`・`allowed-tools`(**Experimental**) | https://agentskills.io/specification · https://github.com/agentskills/agentskills | Apache-2.0 | 5.6「スキルは手順、ハーネスは強制」 | **採用**。現在の根拠が二次出典(Shiplight)なので一次仕様に差し替え。主張の内容は一次出典と一致 |

### 1.4 ポリシーエンジン・プロンプトインジェクション防御

| 項目 | 何か | 一次出典 | ライセンス | 対応 | 判定 |
| --- | --- | --- | --- | --- | --- |
| Cedar | 主体・行動・リソース・コンテキストのリクエスト。**forbidがpermitに勝ち、合致するpermitがなければDeny**。応答に、決定を作ったポリシーid(determining policies)とエラー一覧。エラーになったポリシーはスキップ | https://docs.cedarpolicy.com/auth/authorization.html · https://github.com/cedar-policy/cedar | Apache-2.0 | 4.8 `decide(req)`、`PolicyDecisionPoint` | **採用**(PDPアダプター) |
| Cedar SymCC | ポリシー集合をSMTに変換し、**包含(`check_implies`)・同値・常に拒否・エラーなし**を反例とともに検証。検証器はLeanで形式検証済み | https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc | Apache-2.0 | **I5 `p_child ⊑ p_parent`** | **採用**。I5を「ポリシーストアの検査」から証明可能な検査に引き上げる |
| OPA / Rego | CNCF卒業プロジェクト。決定ログに`decision_id`、`bundles.revision`、`path`、`input`、`result`、`erased`・`masked`(JSON Pointer)、`trace_id`・`span_id` | https://www.openpolicyagent.org/docs/management-decision-logs · https://github.com/open-policy-agent/opa | Apache-2.0 | 5.11、7.9 仮名化 | **採用**(決定ログのフィールド名)。ポリシー言語としてはCedarより分析性が弱いので、PDPの第一候補ではない |
| CaMeL (DeepMind 2025) | すでに引用済み。コード公開 | https://github.com/google-research/camel-prompt-injection | Apache-2.0 | 7.4 | 維持。コードへのリンクを追加 |
| FIDES (Microsoft 2025) | 計画者が**機密性と完全性のラベル**を動的な汚染追跡でたどり、ポリシーを決定的に強制。情報を選択的に隠す基本演算を提示 | https://arxiv.org/abs/2505.23643 · https://github.com/microsoft/fides | ノートブックはMIT | **7.5 情報フローのラベル** | **採用**。7.5には機密性(V0~V3)しかなく、完全性の軸がない |
| Dual LLMパターン (Willison 2023) | 特権LLMと隔離LLM、その間の非LLMコントローラー。信頼できない値は`$VAR1`のような参照でのみ渡す | https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | ブログ | 7.3 隔離された読み取り役 | **採用**(引用)。7.4が設計パターン論文を経由して間接的に引用している |
| 致命的三要素 (Willison 2025) | すでに引用済み | | | 7.3 | 維持 |

### 1.5 マージ・系譜

| 項目 | 何か | 一次出典 | ライセンス | 対応 | 判定 |
| --- | --- | --- | --- | --- | --- |
| JSON Merge Patch (RFC 7396) | オブジェクトのキーは上書きし、`null`は削除、**配列は丸ごと置換** | https://www.rfc-editor.org/rfc/rfc7396 | IETF Trust | **2.3 `⊕`**、6.6 R2 | **採用**。`⊕`の「キー単位の上書き」はまさにこの意味だが、名前がない |
| JSON Patch (RFC 6902) | 演算の一覧(add・remove・replace・move・copy・test) | https://www.rfc-editor.org/rfc/rfc6902 | IETF Trust | 8.5 部分プレビュー、AG-UI `STATE_DELTA` | **参考** |
| Kubernetes Server-Side Apply | フィールドマネージャーがフィールドの所有権を記録(`managedFields`)。スキーママーカー`x-kubernetes-list-type: atomic / set / map`、`x-kubernetes-list-map-keys`、`x-kubernetes-map-type: atomic / granular`でマージ方式を**スキーマが宣言**。他のマネージャーが所有するフィールドを変えると衝突 | https://kubernetes.io/docs/reference/using-api/server-side-apply/ | ドキュメント | **6.6 R2**「スキーマが規則を宣言」、6.11 `Overrides:` | **採用**。R2は言葉だけでスキーマのフィールドがない |
| Kustomize | base・overlay・component。componentは複数のoverlayに混ぜ込む再利用可能な機能のまとまり。`patches`はstrategic mergeとJSON 6902 | https://kubectl.docs.kubernetes.io/guides/config_management/components/ · https://github.com/kubernetes-sigs/kustomize | Apache-2.0 | 6.2 lineage、6.9 機能単位の共有 | **参考**。「ベースラインの上のオーバーレイ」の実務上の先例 |
| Automerge | CRDT。同じキーへの同時書き込みは演算idで決定的な勝者を選ぶが、**負けた値は`getConflicts()`で保存** | https://automerge.org/docs/reference/documents/conflicts/ · https://github.com/automerge/automerge | MIT | 6.13 CRDTの意味の衝突 | **参考**。現在の3.2 A6のリンクはInk & Switchの一覧ページなので、Automergeに替える |
| Yjs | CRDTの共有型 | https://yjs.dev/ · https://github.com/yjs/yjs | MIT | 3.2 A6 `crdt` | **参考** |
| Mergiraf | tree-sitterベースの構文認識マージドライバー | https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf | **GPL-3.0-only** (`Cargo.toml`) | 6.6 R1 | すでに引用済み。リンクをdocs.rsから公式サイトに替え、ライセンスを明記。6.6の「強いコピーレフト」警告の実際の対象 |

### 1.6 生成的UI

| 項目 | 何か | 一次出典 | ライセンス | 対応 | 判定 |
| --- | --- | --- | --- | --- | --- |
| A2UI v0.9.1 | 宣言的なJSON UI。メッセージ4種`createSurface`・`updateComponents`・`updateDataModel`・`deleteSurface`。サーフェスごとに**`catalogId`**(URI形式の文字列)を固定。承認されたカタログのコンポーネントだけをレンダリング | https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md | Apache-2.0 | 2.6 D3、`capability-map` `catalog`、8.5 | **採用**。現在の根拠が報道記事(The Decoder)なので一次出典に差し替え |
| json-render (Vercel Labs) | カタログ(コンポーネントのpropsをzodで定義)の中でのみAIがUIを生成。段階的レンダリング | https://json-render.dev/ · https://github.com/vercel-labs/json-render | Apache-2.0 | 2.6 D3、`capability-map` `catalog.props_schema` | **参考**。カタログ = 承認リストという同じ設計 |

### 1.7 サプライチェーン

| 項目 | 何か | 一次出典 | ライセンス | 対応 | 判定 |
| --- | --- | --- | --- | --- | --- |
| in-toto Attestation | 対象ダイジェスト + 述語タイプからなる署名付き陳述(Statement)の枠組み | https://github.com/in-toto/attestation | Apache-2.0 | 7.7「発行者の出所署名」 | **採用**(形式の指定) |
| SLSA Provenance v1 | `predicateType: https://slsa.dev/provenance/v1`。`buildDefinition`(`buildType`・`externalParameters`・`resolvedDependencies`)、`runDetails.builder.id` | https://slsa.dev/spec/v1.1/provenance | Community Specification License 1.0 | 7.7、`change-record` `provenance` | **採用**。ハーネスをbuilderとみなせば、共有機能の出所証明になる |

## 2. ギャップ表 — 仕様になく、先行事例が解いたもの

| # | 欠けている概念 | 現在の仕様 | 先行事例の解法 | 反映 |
| --- | --- | --- | --- | --- |
| P1 | 宣言的なレイヤー合成の正確な意味 | 2.3「同じキーは後のレイヤーが上書き」しかない。配列・削除の意味は未定 | RFC 7396: `null`で削除、配列は丸ごと置換 | E-3 |
| P2 | スキーマが宣言するマージ規則 | 6.6 R2「スキーマが規則を宣言」と書くだけでフィールドがない | SSA `list-type: map` + `list-map-keys`、`map-type: atomic/granular` | E-4 |
| P3 | 完全性ラベル | 7.5は機密性V0~V3のみ | FIDES・CaMeL: 信頼できない値が行動の選択に影響できないよう完全性を追跡 | E-1 |
| P4 | ポリシーの単調縮小の機械検証 | I5の執行点「ポリシーストアの検査」(方法なし) | Cedar SymCC `check_implies`、`check_never_errors` | E-2 |
| P5 | 決定根拠の標準的な記録 | 4.8「理由=(k, 上限を決めた層)」 | Cedar determining policies、OPA決定ログ`decision_id`・`bundles.revision`・`erased`・`masked` | E-2、E-5 |
| P6 | テレメトリーの共通語彙 | 5.11 `tokens_in`・`tokens_out`などの独自名 | OTel `gen_ai.usage.input_tokens`など、MCP `_meta.traceparent` | E-5 |
| P7 | 体験面の伝送規格 | 5.6はハーネス側のイベントのみ。体験面が何で進行・承認待ちを受け取るかがない | AG-UIのイベント・interrupt、A2A `INPUT_REQUIRED`、MCP MRTR | E-6 |
| P8 | 秘密値の入力経路 | 8.10「キーはセキュアストレージに」のみ。エージェントの対話経路で受け取る場合は未定 | MCP URLモードelicitation(MUST) | E-7 |
| P9 | D3カタログの識別・バージョン | `capability-map.catalog`は一覧だけで、id・バージョンがない | A2UI `catalogId` | E-8 |
| P10 | ケイパビリティ(capability) ↔ エージェントのツールヒント | `capability.risk`のみ | MCP `readOnlyHint`・`destructiveHint`・`idempotentHint`・`openWorldHint` | E-9 |
| P11 | 共有物の出所証明の形式 | 7.7「発行者の出所署名」(形式なし)、マニフェスト`content_hash` | in-toto Statement + SLSA provenance | E-10 |
| P12 | ネットワーク許可の理由 | `network.allow`の一覧のみ | Figma `networkAccess.reasoning` | 4節(保留) |

## 3. 提案する編集の一覧(優先順、最大12)

各項目は最小限の編集です。スキーマ項目はすべて**任意フィールドの追加**なので`required`は変わらず、既存の`examples/*.yaml`はそのまま通るのが正常です。反映後に例の検証を再実行する必要があります。

### E-1. 7.5に完全性の軸を追加 (P3)

- ファイル: `docs/07-trust-and-security.md`、7.5の`ラベル λ = (範囲, 等級)`コードブロックとその下の例の段落
- 提案文言(コードブロックの置き換え):

```text
ラベル λ = (範囲, 等級, 完全性)
  範囲   : テナント / 組織 / ユーザーの識別子
  等級   : V0 集計 < V1 メタデータ < V2 説明 < V3 コード          # 機密性
  完全性 : trusted(人の意図・検証済みのベースライン) > untrusted(共有物・外部文書・モデルが信頼できない入力を見て作った値)

派生規則:  λ(f(x, y)) = λ(x) ⊔ λ(y)          # 機密性はより機微な側、完全性はより低い側
閲覧規則:  閲覧者 s が x を見られる  ⇔  λ(x) ⊑ 権限(s)
行動規則:  権限の増加・外部送信・拡張ポイントの選択を決める値は、完全性が trusted でなければならない
解除規則:  ラベルを下げられるのは出力ゲート(解除器 declassifier)だけで、規則と記録を残す
```

- 付け加える文: `完全性の軸は、FIDES(Costa et al., 2025)が計画者レベルで機密性・完全性のラベルを併せて追跡し、ポリシーを決定的に強制した方式に従います。7.4の「計画してから実行」をラベル規則として書いたものです。`
- references.md (「## エージェントのセキュリティ」の末尾):

```markdown
- M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin. "Securing AI Agents with Information-Flow Control" (FIDES). arXiv:2505.23643, 2025. https://arxiv.org/abs/2505.23643 · ノートブック(MIT): https://github.com/microsoft/fides
- Simon Willison. "The Dual LLM pattern for building AI assistants that can resist prompt injection." 2023-04-25. https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
```

### E-2. 4.8にPDPアダプターとI5の機械検証を追加 (P4, P5)

- ファイル: `docs/04-control-spectrum.md`、4.8「配置原則」リストの末尾
- 提案文言:

```markdown
- **ポリシーエンジンのアダプター** (任意(MAY)): ノブ(knob)の区間をポリシー言語に移してPDPを実装できます。Cedarはforbidがpermitに勝ち、合致するpermitがなければ拒否し、決定を作ったポリシーidを併せて返します。このidを`拒否(理由・層)`とレシート(8.6)の根拠として使います。
- **I5の機械検証** (推奨(SHOULD)): ポリシーを保存するときに`p_child ⊑ p_parent`を検査します。Cedarに移した場合は、SymCCの包含検査(`check_implies`)で反例とともに証明できます。同じツールの`check_never_errors`も併せて実行します。Cedarは評価エラーが起きたポリシーをスキップするので、エラーになるforbidは黙って開いたまま残るからです。
- **下限はエンジンより先に**: forbid優先の規則があるため、ユーザー権利の下限(F1~F7)を通常のpermitとして入れると、上位のforbidが消してしまう可能性があります。上の疑似コードのように、`FLOOR_ACTIONS`の判定をエンジン呼び出しの前に置きます。
```

- references.md (新しい節「## ポリシーエンジン」、「## マージ」の前):

```markdown
## ポリシーエンジン

- Cedarの認可の意味論(forbid優先、既定で拒否、決定ポリシーの診断)。https://docs.cedarpolicy.com/auth/authorization.html · コード(Apache-2.0): https://github.com/cedar-policy/cedar
- Cedar Symbolic Compiler(SymCC): ポリシーの包含・同値・エラーなしの検証。https://github.com/cedar-policy/cedar/tree/main/cedar-policy-symcc
- Open Policy Agentの決定ログ。https://www.openpolicyagent.org/docs/management-decision-logs
```

### E-3. 2.3 `⊕`の基本的な意味をRFC 7396に固定 (P1)

- ファイル: `docs/02-core-model.md`、2.3の`⊕`の項目
- 現在: `` `⊕` (レイヤー合成): 同じキーに触れると、後のレイヤーが前を**上書きします(override)**。宣言的データはキー単位で、コード拡張は拡張ポイントのスロット単位で合成します。 ``
- 提案: `` `⊕` (レイヤー合成): 同じキーに触れると、後のレイヤーが前を**上書きします(override)**。宣言的データの基本的な意味はJSON Merge Patch(RFC 7396)です。オブジェクトはキー単位で上書きし、`null`はそのキーを消し、配列は丸ごと置き換わります。配列を項目単位で統合するには、拡張ポイントのスキーマがマージキーを宣言しなければなりません(6.6 R2)。コード拡張は拡張ポイントのスロット単位で合成します。 ``
- 備考: 次の行の結合法則の要求(「ベースラインを事前に合成してキャッシュ」)を守るには、レイヤー同士を事前に合成するときに`null`(削除マーカー)を消さずに残さなければなりません。そうすることで、合成したレイヤーを後で適用しても、一つずつ適用した結果と同じになります。反映前に小さな例で確認すること。
- references.md (「## マージ」):

```markdown
- RFC 7396. *JSON Merge Patch.* 2014. https://www.rfc-editor.org/rfc/rfc7396
```

### E-4. `capability-map`の拡張ポイントにマージ規則フィールドを追加 (P2)

- ファイル: `schemas/capability-map.schema.json`、`$defs.extensionPoint.properties`の`output_schema`の次
- 提案フィールド:

```json
"merge": {
  "type": "object",
  "description": "このポイントの宣言的成果物をレイヤー同士で合成する規則 (仕様 2.3、6.6 R2)。キーは成果物内の JSON Pointer。宣言のない配列は atomic",
  "propertyNames": { "pattern": "^(/[^/]*)*$" },
  "additionalProperties": {
    "type": "object",
    "required": ["strategy"],
    "additionalProperties": false,
    "properties": {
      "strategy": { "type": "string", "enum": ["atomic", "set", "map"] },
      "keys": { "type": "array", "items": { "type": "string" }, "minItems": 1, "description": "strategy=map のとき項目を識別するフィールド名" }
    }
  }
}
```

- 6.6 R2の表の行「例」欄の後に付け加える文言: `(スキーマフィールド: capability-mapのextension_points[].merge。値の名前はKubernetes Server-Side Applyのx-kubernetes-list-typeに従う)`
- references.md (「## マージ」):

```markdown
- Kubernetes. *Server-Side Apply* (フィールドの所有権、`x-kubernetes-list-type`・`x-kubernetes-list-map-keys`のマージマーカー)。https://kubernetes.io/docs/reference/using-api/server-side-apply/
```

### E-5. 5.11 テレメトリーの名前をOTel GenAI・OPAに合わせる (P5, P6)

- ファイル: `docs/05-reference-architecture.md`、5.11のJSONの例とその下の段落
- 提案: JSONの`"model_cost"`を以下に置き換え、`"policy"`キーを追加します。

```json
  "gen_ai": {"operation.name": "invoke_agent", "agent.id": "builder@harness-x", "usage.input_tokens": 18200, "usage.output_tokens": 2100},
  "model_cost": {"unit_cost_ref": "route:standard"},
  "policy": {"decision_id": "dec_7Q2…", "revision": "tenant/acme@42"},
  "trace": {"traceparent": "00-…-…-01"},
```

- 付け加える文: `モデル使用量の属性はOpenTelemetry GenAIのセマンティック規約の名前に従います。この規約はまだDevelopment状態なので、実装は従った規約のバージョンを併せて記録します。ポリシーの決定はOPAの決定ログのように決定idとポリシーの版(revision)を残し、仮名化で消したフィールドはJSON Pointerの一覧で示します(7.9)。MCPサーバーを経由する呼び出しは、MCP _metaのtraceparent規約で同じトレースにまとめます。`
- references.md (新しい節「## 観測」、「## 体験設計」の前):

```markdown
## 観測

- OpenTelemetry. *Semantic Conventions for Generative AI* (Development). https://github.com/open-telemetry/semantic-conventions-genai · https://opentelemetry.io/docs/specs/semconv/gen-ai/
```

### E-6. 5.6に体験面の伝送対応表を追加 (P7)

- ファイル: `docs/05-reference-architecture.md`、「### マッピング例: Claude Code フック」表の次、「注意:」段落の前
- 提案文言:

```markdown
体験面はハーネスのイベントをそのまま受け取らず、ユーザー向けの進行シグナルとして受け取ります。AG-UIを伝送規格として使う場合、次のように対応します。

| Mallangable | AG-UI | 備考 |
| --- | --- | --- |
| E2 受付 ~ E11 終了 | `RUN_STARTED` · `RUN_FINISHED` · `RUN_ERROR` | |
| 状態語4つ(8.5) | `STEP_STARTED` · `STEP_FINISHED` | step名を状態語のidに固定 |
| 部分プレビュー(8.5) | `STATE_SNAPSHOT` · `STATE_DELTA`(RFC 6902) | 「まだ未確認」の表示を維持 |
| E6 `permission.request`、2.8 `承認待ち` | `RUN_FINISHED`の`outcome.type = "interrupt"` → 次の実行の`resume[]` | 承認は新しい実行へと続く |

サーバージョブを外部エージェントに任せるときはA2Aの作業状態(`TASK_STATE_INPUT_REQUIRED`・`TASK_STATE_AUTH_REQUIRED`)が、MCPツールの中では多重往復リクエスト(`resultType: "input_required"`)が同じ役割を担います。Claude Codeの対応表には`PostToolUseFailure`(E5)、`Elicitation`(E6)も加えられます。
```

- references.md (「## 生成的UI・拡張の標準」):

```markdown
- AG-UI: Agent-User Interaction Protocol (イベント、interrupt)。MIT. https://docs.ag-ui.com/concepts/events · https://github.com/ag-ui-protocol/ag-ui
- A2A Protocol v1.0. Apache-2.0. https://a2a-protocol.org/latest/specification/
```

### E-7. 8.10にMCP経路の秘密値入力規則を追加 (P8)

- ファイル: `docs/08-experience-design.md`、8.10「### セキュリティとコストの表示」の最初の項目の次
- 提案文言:

```markdown
- `sub`経路のように公式アシスタントの中でMCPツールとして動作するとき、接続キーや外部サービスのトークンを対話やformモードの入力で受け取りません。MCP仕様は秘密値・資格情報にURLモードのelicitationを使うよう求めています(2026-07-28版)。キーがエージェントのコンテキストに一度も入らないことで、I6が守られます。
- 同じ版でMCP Samplingは廃止予定です。モデル呼び出しをMCPクライアントに押し付ける方式で`ModelPort`アダプターを作りません。
```

- references.md (「## 生成的UI・拡張の標準」):

```markdown
- Model Context Protocol仕様 2026-07-28 (変更点、ツールのannotations、elicitation)。https://modelcontextprotocol.io/specification/2026-07-28/changelog · https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation
```

### E-8. `capability-map`にカタログのid・バージョンを追加 (P9)

- ファイル: `schemas/capability-map.schema.json`、最上位の`properties`の`catalog`の前
- 提案フィールド:

```json
"catalog_id": {
  "type": "string",
  "description": "D3 カタログの識別子。URI 形式の文字列で、ダウンロード可能である必要はない。カタログの内容が変われば値も変わる (A2UI catalogId と同じ意味)",
  "examples": ["https://todo.example/catalogs/v3"]
}
```

- 付け加える場所: `schemas/extension-manifest.schema.json` `artifact.properties`に`"catalog_id": { "type": "string", "description": "D3 成果物が前提としたカタログ。ケイパビリティマップの catalog_id と異なれば G1 で拒否" }`
- references.md: 「## 生成的UI・拡張の標準」の`Google A2UI 報道。The Decoder.`の行を以下に置き換え。

```markdown
- A2UI: Agent-to-User Interface仕様 v0.9.1 (`createSurface`・`catalogId`)。Apache-2.0. https://a2ui.org/ · https://github.com/a2ui-project/a2ui/blob/main/specification/v0_9_1/docs/a2ui_protocol.md
```

### E-9. `capability-map`のケイパビリティとMCPツールヒントの対応 (P10)

- ファイル: `schemas/capability-map.schema.json`、`$defs.capability.properties.risk`の`description`
- 現在: `"egress=外部送信, sensitive=他人・機微なデータ"`
- 提案: `"egress=外部送信, sensitive=他人・機微なデータ。機能を MCP ツールとして公開するとき、read は readOnlyHint=true、egress は openWorldHint=true として出力する。受け取った側の MCP annotations は信頼せず、この値が権威を持つ (I8)"`
- 任意フィールドを一つ追加: `"destructive": { "type": "boolean", "description": "取り消せない書き込み。MCP destructiveHint と同じ意味。true なら有効化ポリシーに関係なく G5" }`
- 5.8 G5行の「内容」欄に`· 取り消せない書き込み(destructive)機能の使用時`を追加。
- references.md: E-7のMCP仕様の項目に`https://modelcontextprotocol.io/specification/2026-07-28/server/tools`を併記します。

### E-10. 7.7 サプライチェーンに出所証明の形式を指定 (P11)

- ファイル: `docs/07-trust-and-security.md`、7.7 統制表の`一つのアカウントが大量にアップロードした`行の「統制」欄
- 現在: `発行者の出所署名、新規発行者の制限、キュレーション等級`
- 提案: `発行者の出所署名(in-toto StatementにSLSA provenanceの述語。対象はマニフェストのcontent_hash、builder.idはハーネスid)、新規発行者の制限、キュレーション等級`
- references.md (「## エージェントのセキュリティ」の末尾、または新しい節「## サプライチェーン」):

```markdown
- in-toto Attestation Framework. Apache-2.0. https://github.com/in-toto/attestation
- SLSA. *Provenance v1.1.* https://slsa.dev/spec/v1.1/provenance
```

### E-11. 1.5 関連研究にマリアブルなメディアの先例を補強

- ファイル: `docs/01-introduction.md`、1.5の表の最初の行(Malleable software)の次
- 提案する行:

```markdown
| 計算メディア・動的文書 (Boxer, 1986 · [Webstrates](https://webstrates.net/), 2015 · [Potluck](https://www.inkandswitch.com/potluck/), 2022 · [Embark](https://www.inkandswitch.com/embark/), 2023) | 文書とアプリの境界をなくし、ユーザーが計算を重ねて載せる | 原本に手を触れない重ね合わせのレイヤー(2.3)、アプリを越えるツール(O8) | 既存の商用アプリの上で、ベンダーのアップデートに耐える構造として定義 |
```

- 同じ表のLocal-firstの行のリンクを`https://www.inkandswitch.com/project/patchwork/`に替え、「取り入れたもの」欄に`· AIの編集をブランチに置き、人が選んでマージ(Patchworkの実験ノート)`を付け加えます。
- references.md (「## マリアブル・ソフトウェアとエンドユーザープログラミング」):

```markdown
- A. diSessa, H. Abelson. "Boxer: A Reconstructible Computational Medium." *Communications of the ACM* 29(9), 1986. DOI 10.1145/6592.6595
- C. N. Klokmose et al. "Webstrates: Shareable Dynamic Media." UIST 2015. https://webstrates.net/ · コード(Apache-2.0): https://github.com/Webstrates/Webstrates
- Ink & Switch. *Potluck: Dynamic documents as personal software.* 2022. https://www.inkandswitch.com/potluck/
- Ink & Switch. *Embark: Dynamic documents for making plans.* 2023. https://www.inkandswitch.com/embark/
- Ink & Switch. *Patchwork* (実験ノート07 "AI bots in version control")。https://www.inkandswitch.com/project/patchwork/ · https://www.inkandswitch.com/patchwork/notebook/2024-version-control/07/
```

- 備考: Potluck・Embarkの副題は、ページタイトルをそのまま移す前に原文ともう一度照合する必要があります(要約ツールで読んだため)。

### E-12. references.mdの二次出典を一次出典に差し替え

- ファイル: `docs/references.md`
- 置き換える行:

| 現在 | 差し替え |
| --- | --- |
| `Agent Skills標準のまとめ。Shiplight, 2026. https://www.shiplight.ai/blog/agent-skills` | `Agent Skills仕様 (SKILL.md冒頭、allowed-toolsはExperimental)。Apache-2.0. https://agentskills.io/specification · https://github.com/agentskills/agentskills` |
| `Claude Codeプラグインの概要。https://code.claude.com/docs/es/plugins/overview` | `Claude Codeプラグインマニフェストのリファレンス。https://code.claude.com/docs/en/plugins-reference` |
| `Mergiraf: 構文認識のGitマージドライバー。https://docs.rs/crate/mergiraf/latest` | `Mergiraf: 構文認識のGitマージドライバー。GPL-3.0-only. https://mergiraf.org/ · https://codeberg.org/mergiraf/mergiraf` |
| `SEP-1865. *MCP Apps …* https://modelcontextprotocol.io/seps/1865-…` | そのまま残し、後ろに` · 仕様(2026-01-26): https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx` |
| CaMeLの項目 | 後ろに` · コード(Apache-2.0): https://github.com/google-research/camel-prompt-injection` |

- 本文のリンクも併せて替えます: 5.6の`[Shiplight, 2026]` → `[Agent Skills仕様](https://agentskills.io/specification)`、1.5のA2UI・Agent Skillsのリンク、3.2 A6のAutomergeのリンク → `https://automerge.org/docs/reference/documents/conflicts/`、6.6 R1のMergirafのリンク → `https://mergiraf.org/`。
- `確認日`を反映日に更新します。

## 4. 入れなかったもの

- **Figmaの`networkAccess.reasoning`式の許可理由フィールド(P12)**: 有用ではあるが、現在`network.allow`を書く主体は人ではなく生成エージェントです。エージェントが書いた理由は承認カードの根拠になりません。承認カード(G5)を設計するときに改めて検討します。
- **WIT・Extismのフィールド名の整合**: 同じ概念がすでにマニフェストにあり、成果物形式一つ(`wasm`)のための整合です。D4 `lang`アダプターの文書を書くときに対応表で十分です。
- **VS Codeのアクティベーションイベント**: 遅延ロードはランタイム実装の問題で、契約・マージとは無関係です。G3の起動時間予算が同じ目的を担います。
- **Chrome式の`optional_permissions`**: 「必要なときに要求する」は、I4の人による承認フロー(E6)ですでに表現されています。静的な宣言をもう一つ置くと、二つの経路が分かれます。
- **OPAを既定のPDPに**: 決定ログの形式は取り入れるが、I5の包含検証ができるCedarのほうが、この仕様の単調性の要求に合っています。
- **MCP-UI、Yjsの個別の整合**: それぞれMCP Apps、Automergeの引用で十分です。
- **Smalltalkの系譜**: 一次出典を探していません。引用するには原論文を確認する必要があります。
