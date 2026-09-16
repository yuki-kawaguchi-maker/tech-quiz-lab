#!/usr/bin/env python3
"""docs/question-schema.md の必須条件に沿って data/questions/*.json を検証する。

使い方: python3 scripts/validate_questions.py
成功時はEXIT 0、違反があればEXIT 1で違反内容を標準出力に列挙する。
"""
import glob
import json
import sys

REQUIRED_FIELDS = [
    "id", "category", "subtopic", "key_concept", "question", "choices",
    "answer_index", "explanation", "diagram", "practice_note", "difficulty",
]


def validate_file(path, errors, seen_ids):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        errors.append(f"{path}: トップレベルが配列ではない")
        return
    for q in data:
        qid = q.get("id", "<id無し>")
        for field in REQUIRED_FIELDS:
            if field not in q:
                errors.append(f"{path}:{qid}: 必須フィールド'{field}'が無い")
        if "id" in q:
            if q["id"] in seen_ids:
                errors.append(f"{path}:{qid}: idが重複している")
            seen_ids.add(q["id"])
        if "key_concept" in q and len(q["key_concept"]) > 40:
            errors.append(f"{path}:{qid}: key_conceptが40字を超えている({len(q['key_concept'])}字)")
        if "key_concept" in q and "diagram" in q and q["key_concept"] not in q["diagram"]:
            errors.append(f"{path}:{qid}: diagramのキャプションがkey_conceptと同内容でない")
        if "choices" in q:
            choices = q["choices"]
            if len(choices) != 4:
                errors.append(f"{path}:{qid}: choicesが4件でない({len(choices)}件)")
            ai = q.get("answer_index")
            for i, c in enumerate(choices):
                has_right = "why_right" in c
                has_wrong = "why_wrong" in c
                if has_right == has_wrong:
                    errors.append(f"{path}:{qid}: choices[{i}]がwhy_right/why_wrongのどちらか一方のみを持っていない")
                if ai is not None:
                    if i == ai and not has_right:
                        errors.append(f"{path}:{qid}: answer_indexが指す選択肢にwhy_rightが無い")
                    if i != ai and not has_wrong:
                        errors.append(f"{path}:{qid}: 誤答の選択肢にwhy_wrongが無い")
        if "answer_index" in q and not (0 <= q["answer_index"] <= 3):
            errors.append(f"{path}:{qid}: answer_indexが0〜3の範囲外")
        if "difficulty" in q and not (1 <= q["difficulty"] <= 3):
            errors.append(f"{path}:{qid}: difficultyが1〜3の範囲外")
        if "diagram" in q:
            svg = q["diagram"]
            if not svg.strip().startswith("<svg"):
                errors.append(f"{path}:{qid}: diagramが<svgで始まっていない")
            boxes = svg.count("<rect")
            arrows = svg.count("marker-end")
            if not (2 <= boxes <= 3):
                errors.append(f"{path}:{qid}: diagramの箱の数が2〜3個ではない({boxes}個)")
            if not (1 <= arrows <= 3):
                errors.append(f"{path}:{qid}: diagramの矢印の数が1〜3本ではない({arrows}本)")


def main():
    errors = []
    seen_ids = set()
    files = sorted(
        p for p in glob.glob("data/questions/*.json")
        if p != "data/questions/index.json"
    )
    if not files:
        print("data/questions/*.json が見つからない")
        sys.exit(1)
    for path in files:
        validate_file(path, errors, seen_ids)
    if errors:
        print(f"NG: {len(errors)}件の違反")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    total = sum(len(json.load(open(p, encoding='utf-8'))) for p in files)
    print(f"OK: {len(files)}ファイル・{total}問すべて検証に合格")
    sys.exit(0)


if __name__ == "__main__":
    main()
