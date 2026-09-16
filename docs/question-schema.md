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
| `question_type` | string | ○ | 出題形式。`term`(用語の意味を問う)/ `diagram_read`(図解を
先に見せて、その図が表す操作・概念を問う。`question`は「この図が表している操作/概念はどれか」の形にする)/
`scenario`(状況を提示し、どの操作を選ぶべきかを問う)/ `troubleshoot`(トラブルの原因・対処を問う)の
いずれか。`diagram_read`の場合、アプリの解答前画面では`question`の**上に**`diagram`を表示する
(他のquestion_typeでは解答前に`diagram`を出さない、`explanation`と合わせて解答後に初めて出す)。 |
| `key_concept` | string | ○ | その問題が扱う概念の「ひと言定義」(40字以内)。`diagram`のキャプションと
同内容にする。例: 「origin/mainは、リモートの状態をローカルに写した影」。 |
| `question` | string | ○ | 設問文。 |
| `choices` | array(4件) | ○ | 選択肢。各要素は下記「choice要素」参照。ちょうど4件。 |
| `answer_index` | number | ○ | 正解の選択肢のインデックス(0始まり、0〜3)。 |
| `explanation` | string | ○ | `why_right`の言い換えではなく、`key_concept`を一段深く説明する「仕組み」の
解説(2〜4文)。選択肢の正誤判定に必要な理由付けは各choiceの`why_right`/`why_wrong`側に書き、
本フィールドでは重複させず、概念そのものの成り立ち・メカニズムを掘り下げる。バッククォート(`` ` ``)は
使わない(下記「表記規約」参照)。 |
| `diagram` | string | ○ | 解説に添える静止SVGの文字列(`<svg ...>...</svg>`)。図解の型は
「箱2〜3個(各箱に名前を付ける。箱の名前はラベルに数えない)・矢印1〜3本・矢印ラベル3個以内・
キャプション1文(`key_concept`と同内容)」に限定し、要素を増やさない。**箱・矢印・ラベルの数以外の
配置パターン(横並び・収束型・縦積み等)は概念に合わせて自由に選んでよい。** |
| `practice_note` | string | ○ | ユーザーの実運用(ループエンジニアリング・Salesforce構築)の
どこでこの概念に出会うかを1〜2文で書く。一般論ではなく、`loop-engineering-hub`の
`CLAUDE.md`・`prompts/`・`skill-src/salesforce-trial-builder/references/setup_gotchas.md`等に
記録された実例を引用し、出典ファイル名(節があれば節名も)を末尾に括弧で添える。該当する実例が
見つからない場合は「実例未確認」と書き、省略しない。バッククォートは使わない
(下記「表記規約」参照)。 |
| `difficulty` | number | ○ | 難易度。1〜3の整数。**1=初級**(用語の意味・図解の読み取り)、
**2=中級**(状況からどの操作かを選ぶ)、**3=上級**(トラブル対処・複数概念の組み合わせ)。 |

## 表記規約

- `explanation`・`choices[].why_right`・`choices[].why_wrong`・`practice_note`の本文では
  バッククォート(`` ` ``)を使わない。コマンド名・ファイル名等を強調したい場合も、
  地の文にそのまま書く(例: 「git resetは」であって「`git reset`は」としない)。
  これはアプリ側で`textContent`により地の文のまま画面に表示するため、Markdown記法の
  記号がそのまま文字として表示されてしまうことを避けるための規約。

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
- `key_concept` は40字以内。`diagram`内のキャプション文と同内容にする。
- `practice_note` は必須。実例を引用できない場合も省略せず「実例未確認」と明記する。
- `question_type` は `term` / `diagram_read` / `scenario` / `troubleshoot` のいずれかであること。
- `explanation`・`choices[].why_right`・`choices[].why_wrong`・`practice_note` に
  バッククォート(`` ` ``)を含まないこと。

## 参照元

- 運用ルール・制約は `CLAUDE.md` を参照。
- サンプル: `data/questions/github.json`(カテゴリ(1)GitHubのサンプル3問)。
- 新規カテゴリのデータ作成手順は `README.md`「問題を追加する手順」を参照。
