# 問題データJSONスキーマ

`data/questions/<category>.json` は、以下のスキーマを満たす問題オブジェクトの配列とする。

## トップレベル

```
[
  { ...問題オブジェクト... },
  { ...問題オブジェクト... }
]
```

1ファイル = 1カテゴリ。ファイル名はカテゴリのスラッグ(例: `github.json`)。

## 問題オブジェクトのフィールド

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `id` | string | ○ | 一意なID。`<category>-NNN` 形式(例: `github-001`)。 |
| `category` | string | ○ | カテゴリ名。`GitHub` / `Salesforce構築の裏側` / `AIの理解と活用` / `AI DXコンサル実務` のいずれか。 |
| `subtopic` | string | ○ | カテゴリ内の小分類(例: `ブランチ運用`)。 |
| `question` | string | ○ | 設問文。 |
| `choices` | array(4件) | ○ | 選択肢。各要素は下記「choice要素」参照。ちょうど4件。 |
| `answer_index` | number | ○ | 正解の選択肢のインデックス(0始まり、0〜3)。 |
| `explanation` | string | ○ | 正解の理由の解説文。各`choice`側の`why_right`/`why_wrong`と重複してよいが、
本フィールドは設問全体としてのまとめの解説とする。 |
| `diagram` | string | ○ | 解説に添える静止SVGの文字列(`<svg ...>...</svg>`)。図解の型は
「箱2〜3個+矢印+ラベル+ひと言キャプション」に限定し、要素を増やさない。 |
| `salesforce_note` | string | 任意 | 「Salesforce構築ではここで出会う」という1行。無い場合はフィールド自体を省略する
(空文字列を入れない)。 |
| `difficulty` | number | ○ | 難易度。1〜3の整数(1=易・3=難)。 |

## choice要素のフィールド

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `text` | string | ○ | 選択肢の文言。 |
| `why_right` | string | 正解の選択肢のみ | この選択肢が正解である理由。正解の選択肢(`answer_index`が指す要素)にのみ持たせる。 |
| `why_wrong` | string | 誤答の選択肢のみ | この選択肢がなぜ誤りか。「惜しい・混同しやすい概念」との違いを具体的に書き、
「明らかに違う」で済ませない。誤答の選択肢すべてに持たせる。 |

各choice要素は `why_right` と `why_wrong` のどちらか一方のみを持つ(両方を持たない・
どちらも持たない、は不可)。

## バリデーション上の注意

- `choices` の長さは常に4。
- `answer_index` は0〜3の範囲内で、`choices[answer_index]` が `why_right` を持つ要素と一致すること。
- `answer_index` 以外の3要素は `why_wrong` を持つこと。
- `id` はファイル内で重複しないこと。カテゴリをまたいだ重複も避ける。

## 参照元

- 運用ルール・制約は `CLAUDE.md` を参照。
- サンプル: `data/questions/github.json`(カテゴリ(1)GitHubのサンプル3問)。
- 新規カテゴリのデータ作成手順は `README.md`「問題を追加する手順」を参照。
