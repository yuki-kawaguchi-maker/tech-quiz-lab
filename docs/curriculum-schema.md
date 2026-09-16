# カリキュラム定義JSONスキーマ

`data/curriculum.json` は、最終ゴールに向けて学ぶべきジャンルとユニットの全体量を定義する
単一オブジェクトとする。「学びの地図」画面(フィッシュボーン図)は、このファイルと
`data/lessons/*.json`・進捗データ(localStorage)を組み合わせて描画する。

## トップレベル

```
{
  "goal": "...",
  "categories": [ { ...categoryオブジェクト... }, ... ]
}
```

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `goal` | string | ○ | 最終ゴールの1文。 |
| `categories` | array | ○ | ジャンル。表示・学習選定の順序として扱う(配列の並び順=ジャンル順)。 |

## categoryオブジェクトのフィールド

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `id` | string | ○ | 一意なID(スラッグ、例: `github`)。 |
| `title` | string | ○ | ジャンル名。 |
| `summary` | string | ○ | このジャンルで学ぶ内容のひと言まとめ(1文)。 |
| `units` | array(3〜6件) | ○ | ユニット。配列の並び順=ユニット順(学習選定の順序として扱う)。 |

## unitオブジェクトのフィールド

| フィールド | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| `id` | string | ○ | 一意なID。`status`が`available`の場合、`data/lessons/*.json`内のunit `id`と一致させる。 |
| `title` | string | ○ | ユニット名(フルネーム)。教科書タブ・ユニット一覧など、学びの地図以外の画面ではこちらを表示する。 |
| `short_title` | string | ○ | 学びの地図(フィッシュボーン図)の小骨ラベル専用の短縮名。全角8字以内
(半角英数字・記号は0.5字、全角文字は1字として計算する)。`title`の意味が残るように短縮し、
「…」等による機械的な省略はしない。 |
| `status` | string | ○ | `planned`(未作成。レッスンデータが無い)または`available`(レッスンデータあり)のいずれか。 |

## バリデーション上の注意

- `id`は`category`・`unit`とも、ファイル全体で重複しないこと。
- `status`が`available`のunitは、`data/lessons/*.json`内に同じ`id`のunitが実在すること。
- 各`category`の`units`は3〜6件であること。
- `short_title`は必須で、全角8字以内(半角英数字・記号=0.5字、全角文字=1字換算の合計)であること。

## 学びの地図での使い方

- フィッシュボーン図の背骨(縦)に沿って、`categories`配列の順にジャンル(大骨)を左右交互に配置する。
- 各ユニット(小骨)の状態色は、`status`とlocalStorageの進捗(`learnedUnits`・`questionStats`)から
  実行時に判定する(本ファイル自体には進捗を持たない)。
  - `planned`: 灰(点線)
  - `available`かつ未学習(`learnedUnits`に含まれない): 白(灰の枠)
  - `available`かつ学習中(`learnedUnits`に含まれるが、そのunitの`question_ids`の正答率が
    80%未満、または解答数0): 青
  - `available`かつ習得(そのunitの`question_ids`を5問以上解答し、正答率80%以上): 緑
- 「今日のレッスン」の選定は、`categories`→`units`の配列順で、`status: "available"`のうち
  未学習のものを先頭から選ぶ(全て学習済みなら、従来どおり通算正答率が最も低いものを選ぶ)。
- 小骨のラベルには`short_title`を使う(「…」による機械的な省略はしない)。大骨の根元の
  ジャンル見出しには`title`を使い、幅に収まらない場合は最大2行に折り返して表示する。

## 参照元

- 検証スクリプトは`scripts/validate_curriculum.py`。
- レッスンデータのスキーマは`docs/lesson-schema.md`。
- サンプル: `data/curriculum.json`。
