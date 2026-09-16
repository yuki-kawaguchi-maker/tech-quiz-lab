#!/usr/bin/env python3
"""docs/lesson-schema.md の必須条件に沿って data/lessons/*.json を検証する。

使い方: python3 scripts/validate_lessons.py
成功時はEXIT 0、違反があればEXIT 1で違反内容を標準出力に列挙する。
"""
import glob
import json
import re
import sys

UNIT_REQUIRED_FIELDS = ["id", "category", "level", "title", "summary", "cards", "question_ids"]
CARD_REQUIRED_FIELDS = ["id", "title", "key_concept", "diagram", "steps", "body"]
NO_BACKTICK_CARD_FIELDS = ["body", "practice_note"]


def load_question_ids():
    ids = set()
    for path in glob.glob("data/questions/*.json"):
        if path == "data/questions/index.json":
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for q in data:
            if "id" in q:
                ids.add(q["id"])
    return ids


def validate_card(path, unit_id, card, errors, seen_card_ids):
    cid = card.get("id", "<id無し>")
    for field in CARD_REQUIRED_FIELDS:
        if field not in card:
            errors.append(f"{path}:{unit_id}:{cid}: 必須フィールド'{field}'が無い")
    if "id" in card:
        if card["id"] in seen_card_ids:
            errors.append(f"{path}:{unit_id}:{cid}: card idが重複している")
        seen_card_ids.add(card["id"])
    if "key_concept" in card and len(card["key_concept"]) > 40:
        errors.append(f"{path}:{unit_id}:{cid}: key_conceptが40字を超えている({len(card['key_concept'])}字)")
    for field in NO_BACKTICK_CARD_FIELDS:
        if field in card and "`" in card[field]:
            errors.append(f"{path}:{unit_id}:{cid}: {field}にバッククォートが含まれている")
    if "diagram" in card:
        svg = card["diagram"]
        if not svg.strip().startswith("<svg"):
            errors.append(f"{path}:{unit_id}:{cid}: diagramが<svgで始まっていない")
        boxes = svg.count("<rect")
        arrows = svg.count("marker-end")
        if not (2 <= boxes <= 3):
            errors.append(f"{path}:{unit_id}:{cid}: diagramの箱の数が2〜3個ではない({boxes}個)")
        if not (1 <= arrows <= 3):
            errors.append(f"{path}:{unit_id}:{cid}: diagramの矢印の数が1〜3本ではない({arrows}本)")
        if "key_concept" in card and card["key_concept"] not in svg:
            errors.append(f"{path}:{unit_id}:{cid}: diagramのキャプションがkey_conceptと同内容でない")
        step_nums = [int(n) for n in re.findall(r'data-step="(\d+)"', svg)]
        max_step = max(step_nums) if step_nums else 0
        if not (0 <= max_step <= 4):
            errors.append(f"{path}:{unit_id}:{cid}: data-stepの最大値が0〜4の範囲外({max_step})")
        if "steps" in card and len(card["steps"]) != max_step:
            errors.append(
                f"{path}:{unit_id}:{cid}: stepsの件数({len(card['steps'])})がdata-stepの最大値({max_step})と一致しない"
            )
        if "steps" in card and not (1 <= len(card["steps"]) <= 4):
            errors.append(f"{path}:{unit_id}:{cid}: stepsが1〜4件でない({len(card['steps'])}件)")


def validate_file(path, errors, seen_unit_ids, seen_card_ids, question_ids, seen_question_ids):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        errors.append(f"{path}: トップレベルが配列ではない")
        return
    for unit in data:
        uid = unit.get("id", "<id無し>")
        for field in UNIT_REQUIRED_FIELDS:
            if field not in unit:
                errors.append(f"{path}:{uid}: 必須フィールド'{field}'が無い")
        if "id" in unit:
            if unit["id"] in seen_unit_ids:
                errors.append(f"{path}:{uid}: unit idが重複している")
            seen_unit_ids.add(unit["id"])
        if "level" in unit and not (1 <= unit["level"] <= 3):
            errors.append(f"{path}:{uid}: levelが1〜3の範囲外")
        if "cards" in unit:
            if not (4 <= len(unit["cards"]) <= 5):
                errors.append(f"{path}:{uid}: cardsが4〜5件でない({len(unit['cards'])}件)")
            for card in unit["cards"]:
                validate_card(path, uid, card, errors, seen_card_ids)
        if "question_ids" in unit:
            for qid in unit["question_ids"]:
                if qid not in question_ids:
                    errors.append(f"{path}:{uid}: question_ids内の'{qid}'がdata/questions側に実在しない")
                if qid in seen_question_ids:
                    errors.append(f"{path}:{uid}: question_ids内の'{qid}'が他のユニットと重複している")
                seen_question_ids.add(qid)


def main():
    errors = []
    seen_unit_ids = set()
    seen_card_ids = set()
    seen_question_ids = set()
    question_ids = load_question_ids()
    files = sorted(
        p for p in glob.glob("data/lessons/*.json")
        if p != "data/lessons/index.json"
    )
    if not files:
        print("data/lessons/*.json が見つからない")
        sys.exit(1)
    for path in files:
        validate_file(path, errors, seen_unit_ids, seen_card_ids, question_ids, seen_question_ids)
    if errors:
        print(f"NG: {len(errors)}件の違反")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    total_units = sum(len(json.load(open(p, encoding='utf-8'))) for p in files)
    print(f"OK: {len(files)}ファイル・{total_units}ユニット・question_ids延べ{len(seen_question_ids)}問すべて検証に合格")
    sys.exit(0)


if __name__ == "__main__":
    main()
