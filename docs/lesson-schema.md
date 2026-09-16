# レッスンデータJSONスキーマ

`data/lessons/<category>.json` は、以下のスキーマを満たすユニット(unit)オブジェクトの
配列とする。レッスン(教科書モード)は、クイズの前に「学ぶ」段階を挟むための教材で、
対応する問題データ(`data/questions/*.json`)と`key_concept`・図解の内容を揃える。

## トップレベル

```
[
  { ...unitオブジェクト... },
  { ...unitオブジェクト... }
]
```

1ファイル = 1カテゴリ。ファイル名はカテゴリのスラッグ(例: `github.json`)。
`data/lessons/index.json` に、読み込むカテゴリとファイル名の対応表を置く
(`data/questions/index.json`と同じ形式)。

## unitオブジェクトのフィールド

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `id` | string | ○ | 一意なID。`<category>-uNN` 形式(例: `github-u01`)。 |
| `category` | string | ○ | カテゴリ名。`data/questions/*.json`の`category`と同じ値を使う。 |
| `level` | number | ○ | 難易度。1〜3の整数(問題データの`difficulty`と同じ意味)。 |
| `title` | string | ○ | ユニット名(例: 「リポジトリとコミット」)。 |
| `summary` | string | ○ | このユニットで学ぶ内容のひと言まとめ(1文)。 |
| `cards` | array(4〜5件) | ○ | カード。各要素は下記「cardオブジェクト」参照。 |
| `question_ids` | array(string) | ○ | このユニットに対応する問題id(`data/questions/*.json`の`id`)の配列。1問は1ユニットにのみ属する(ユニットをまたいで重複しない)。 |

## cardオブジェクトのフィールド

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `id` | string | ○ | 一意なID。`<unit id>-c1`のように連番にする。 |
| `title` | string | ○ | 用語または概念名。 |
| `key_concept` | string | ○ | ひと言定義(40字以内)。対応する問題の`key_concept`と揃える(同一文言でもよい)。 |
| `diagram` | string | ○ | 動く図解のSVG文字列。制約は問題データの`diagram`と同じ
(箱2〜3個・矢印1〜3本・矢印ラベル3個以内)。加えて、段階的に動かす要素には
`data-step="n"`属性を付ける(n=1始まりの整数)。`data-step`の無い要素は最初から表示する。 |
| `steps` | array(string、1〜4件) | ○ | 各段階の説明文(1文)。配列の長さは、`diagram`内`data-step`属性の最大値と一致させる。 |
| `body` | string | ○ | 3〜4文の本文。「なぜそうなるか」を説明する文を1文以上含める。バッククォート
(`` ` ``)は使わない(問題データと同じ表記規約)。 |
| `practice_note` | string | 任意 | 実運用でこの概念に出会う場面(1〜2文)。書く場合は問題データと同じ規約
(出典を括弧で明記、無い場合は「実例未確認」)に従う。 |

## 動きの型(diagramの`data-step`が表す動き)

各カードは、次の3種類のうち**1種類だけ**を使う。SMILアニメーション(`<animate>`等)や
外部ライブラリは使わない。CSSクラスの付け外しと`transition`で実現し、動きの時間は
0.4〜0.6秒にする。OSの「視差効果を減らす」設定(`prefers-reduced-motion: reduce`)が
有効な場合は、動きなしで全段階を即時表示する。

- **(a) 段階出現**: 要素が`opacity: 0`から`opacity: 1`へフェードインする。新しい概念が
  登場する段階に使う。
- **(b) 矢印が伸びる**: 線(`<line>`または`<path>`)が始点から終点へ描かれる。
  `stroke-dasharray`を線の全長に設定し、`stroke-dashoffset`を全長→0へ`transition`
  させる。操作の実行(コマンドの効果)を示す段階に使う。
- **(c) 移動**: 印(小さな`<circle>`やラベルの`<text>`/`<g>`)がAからBへ移動する。
  `transform: translate(...)`を`transition`させる。ポインタ(HEAD等)の移動や、
  データが場所を移す様子を示す段階に使う。

## diagramの制約(問題データと共通)

- 箱2〜3個(各箱に名前を付ける。箱の名前はラベルに数えない)
- 矢印1〜3本
- 矢印ラベル3個以内
- キャプション1文(`key_concept`と同内容)を`data-step`無しで最初から表示する

## 表記規約

- `body`・`practice_note`ではバッククォート(`` ` ``)を使わない(問題データと同じ規約)。

## バリデーション上の注意

- `id`はファイル内・カテゴリをまたいで重複しないこと(unit・cardとも)。
- `cards`は4〜5件。
- `question_ids`が指す問題idは、対応する`data/questions/<category>.json`に実在すること。
- `question_ids`はカテゴリ内のユニットをまたいで重複しないこと(1問は1ユニットのみ)。
- `steps`の件数は、`diagram`内`data-step`属性の最大値と一致すること。
- `key_concept`は40字以内。
- `body`・`practice_note`にバッククォートを含まないこと。
- `diagram`の箱・矢印・矢印ラベルの数は問題データと同じ上限を守ること。

## 参照元

- 問題データのスキーマは`docs/question-schema.md`を参照。
- 検証スクリプトは`scripts/validate_lessons.py`。
- サンプル: `data/lessons/github.json`(GitHub初級5ユニット)。
