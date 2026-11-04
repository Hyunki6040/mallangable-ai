<!-- LANG-BAR -->
[English](CONTRIBUTING.md) · [한국어](CONTRIBUTING.ko.md) · [简体中文](CONTRIBUTING.zh-CN.md) · **日本語** · [Español](CONTRIBUTING.es.md)
<!-- /LANG-BAR -->

# 貢献ガイド

このリポジトリは実装ではなく**仕様**です。貢献は大きく3種類あります: 本文の修正、スキーマ・例の修正、計算機のルールの修正。

## 始める前に

```bash
pip install -r requirements.txt               # check_schemas.py 用
python3 tools/design_space.py --check all     # P1~P7 がすべて clean であること
python3 tools/check_schemas.py                # 最後の行が ALL OK であること
```

2つのコマンドが通る状態で PR を送ってください。全列挙(`python3 tools/design_space.py`)には数分かかります。

## 守るべきこと

- **識別子はファイル間の契約です。** 軸 `A1~A11`、制約 `L`/`N`/`S`、不変条件 `I1~I10`、下限 `F1~F7`、ゲート `G0~G5`、解決段階 `R0~R5`、プロファイル `P1~P7`、ビジネスモデル `B1~B20` は、文書・スキーマ・`design_space.py`・`check_schemas.py` に共通して現れます。番号を変えたり消したりせず、新しい項目は後ろに付けてください。廃止するときは番号を空けたままにして「廃止」と書きます。
- **文書中の数値は計算結果です。** `AXES`・`LOGICAL_RULES`・`normative()`・`soft()`・`BMS` を変えたら、ツールを再実行し、`README.md`、`docs/01`、`docs/03`、`docs/09`、`CHANGELOG.md` の数値をすべて直します。
- **`LOGICAL_RULES` の順序を変えないでください。** 「最初の違反」の集計が順序に依存します。
- **プロファイルは3か所にあります**: `design_space.py` の `PROFILES`、`examples/profiles.yaml`、README の表。
- **例の構造を変えると**、`check_schemas.py` の `CASES` の変異パスが気づかないうちにずれることがあります。禁止文書のチェックがすべて `OK` であることを確認してください。
- **言語版**: 韓国語版(`docs/ko/`、`*.ko.md`)が原文です。英語(`docs/en/`、既定の README)・简体中文(`zh-CN`)・日本語(`ja`)・Español(`es`)は翻訳で、同じファイル名を使います。原文を直したら同じ PR で翻訳版も直すか、直せなかった言語を PR の本文に書いてください。識別子・数値・コードは翻訳しません。スキーマの説明・例・ツールのメッセージは英語で書きます。
- 本文は平易な言葉で書きます。要求レベルは 必須(MUST)・推奨(SHOULD)・任意(MAY)。出典のない数値は**設計提案値**と表示します。出典は一次資料を優先します([docs/references.md](docs/ja/references.md))。

## Issue・PR

- タイトルや本文に、該当する章とルールIDを書いてください(例: `3.3 L7`、`I10`、`6.5 R2`)。
- ルールに反対するときは、そのルールが**誤ってふるい落とす組み合わせ1つ**を `--profile` で示すと、最も早く議論が進みます。
- 大きな変更(新しい軸、新しい不変条件、スキーマの契約の変更)は、まず Issue で提案してください。反映されたら `CHANGELOG.md` に記録します。

## ライセンス

貢献した内容はリポジトリのライセンスに従います。文書(`docs/`、`README.md` など)は CC BY 4.0([LICENSE-docs](LICENSE-docs))、スキーマ・例・ツール(`schemas/`、`examples/`、`tools/`)は Apache-2.0([LICENSE](LICENSE))です。
