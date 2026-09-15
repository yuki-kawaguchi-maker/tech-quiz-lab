# tech-quiz-lab

ユーザー(yuki)本人がIT基礎知識を鍛えるための、個人専用4択クイズアプリ。

## 概要

- カテゴリ: (1) GitHub (2) Salesforce構築の裏側 (3) AIの理解と活用 (4) AI DXコンサル実務
- 1問ごとに「正解の理由」と「他の3選択肢がなぜ違うか」を必ず解説する。誤答の選択肢は
  「惜しい・混同しやすい概念」で構成する。
- 解説には静止SVGの図解を1枚添える(「箱2〜3個+矢印+ラベル+ひと言キャプション」の型に限定)。
- スマホのブラウザ(幅380pxで破綻しないこと)を主対象に、GitHub Pagesで配信する
  1枚HTML+問題データJSON構成。外部ライブラリ・APIキーは使用しない。
- 問題はあらかじめバッチ生成して同梱する(実行時生成はしない)。
- 誤答・「勘で当てた」ボタンを押した問題は再出題キューに入れ、進捗はlocalStorageに
  保存する(try/catch必須)。

決定事項の経緯は [`STATE.md`](./STATE.md) の「ユーザーによる業務判断の記録」を参照。

## ディレクトリ構成

- `docs/question-schema.md` — 問題データJSONのスキーマ定義(正本)
- `data/questions/<category>.json` — カテゴリごとの問題データ
  (現状は `github.json` のサンプル3問のみ)
- `index.html` — クイズ本体のUI・ロジック(未作成、今後追加予定)

## 問題を追加する手順(バッチ生成1セッション分の型)

新しいカテゴリ、または既存カテゴリへの追加問題をバッチ生成するときは、次の順で進める。

1. **スキーマを確認する**: `docs/question-schema.md` を読み、フィールド構成
   (`id`/`category`/`subtopic`/`key_concept`/`question`/`choices`/`answer_index`/
   `explanation`/`diagram`/`practice_note`/`difficulty`、いずれも必須)を守る。
   スキーマ自体の変更が必要な場合は、データ作成より先に `docs/question-schema.md` を改訂する。
2. **出題対象を決める**: 対象カテゴリと小分類(`subtopic`)の範囲、目標問題数を決める。
   既存の `id`(`<category>-NNN`)と重複しないよう、採番を確認する。
3. **問題を作成する**: 1問ごとに、正解の選択肢には `why_right`、誤答の選択肢
   (3件)には `why_wrong` を必ず書く。誤答の選択肢は「明らかに違う」ものではなく
   「惜しい・混同しやすい概念」にする。
4. **SVG図解を作る**: 各問1枚、「箱2〜3個+矢印+ラベル+ひと言キャプション」の型を守り、
   要素を増やさない。既存問題(`data/questions/github.json`)のSVGを参考にする。
5. **バリデーションする**: 追加後、`data/questions/<category>.json` が
   `docs/question-schema.md` の各条件(choices件数・answer_indexの整合・
   why_right/why_wrongの排他等)を満たすか確認する。
6. **コミット・PR**: 変更ファイル一覧とサンプル問題のidだけをPR本文に記載し、
   解説・SVG本文はチャットやPR本文に貼らない。
