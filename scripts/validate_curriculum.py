#!/usr/bin/env python3
"""docs/curriculum-schema.md の必須条件に沿って data/curriculum.json を検証する。

使い方: python3 scripts/validate_curriculum.py
成功時はEXIT 0、違反があればEXIT 1で違反内容を標準出力に列挙する。
"""
import glob
import json
import sys

VALID_STATUS = {"planned", "available"}
SHORT_TITLE_MAX_WIDTH = 8


def zenkaku_width(s):
    """半角英数字・記号を0.5字、それ以外(全角文字)を1字として幅を計算する。"""
    return sum(0.5 if ord(ch) < 128 else 1.0 for ch in s)


def load_available_lesson_unit_ids():
    ids = set()
    for path in glob.glob("data/lessons/*.json"):
        if path == "data/lessons/index.json":
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for unit in data:
            if "id" in unit:
                ids.add(unit["id"])
    return ids


def main():
    errors = []
    path = "data/curriculum.json"
    try:
        with open(path, encoding="utf-8") as f:
            curriculum = json.load(f)
    except FileNotFoundError:
        print(f"{path} が見つからない")
        sys.exit(1)

    if "goal" not in curriculum or not curriculum["goal"]:
        errors.append(f"{path}: 必須フィールド'goal'が無い")
    if "categories" not in curriculum:
        errors.append(f"{path}: 必須フィールド'categories'が無い")
        print(f"NG: {len(errors)}件の違反")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)

    lesson_unit_ids = load_available_lesson_unit_ids()
    seen_category_ids = set()
    seen_unit_ids = set()
    total_units = 0
    available_count = 0

    for cat in curriculum["categories"]:
        cid = cat.get("id", "<id無し>")
        for field in ("id", "title", "summary", "units"):
            if field not in cat:
                errors.append(f"{path}:{cid}: category必須フィールド'{field}'が無い")
        if "id" in cat:
            if cat["id"] in seen_category_ids:
                errors.append(f"{path}:{cid}: category idが重複している")
            seen_category_ids.add(cat["id"])
        units = cat.get("units", [])
        if not (3 <= len(units) <= 6):
            errors.append(f"{path}:{cid}: unitsが3〜6件でない({len(units)}件)")
        for unit in units:
            total_units += 1
            uid = unit.get("id", "<id無し>")
            for field in ("id", "title", "short_title", "status"):
                if field not in unit:
                    errors.append(f"{path}:{cid}:{uid}: unit必須フィールド'{field}'が無い")
            if "short_title" in unit:
                w = zenkaku_width(unit["short_title"])
                if w > SHORT_TITLE_MAX_WIDTH:
                    errors.append(
                        f"{path}:{cid}:{uid}: short_titleが全角{SHORT_TITLE_MAX_WIDTH}字を超えている"
                        f"(換算{w}字: {unit['short_title']!r})"
                    )
            if "id" in unit:
                if unit["id"] in seen_unit_ids:
                    errors.append(f"{path}:{cid}:{uid}: unit idが重複している")
                seen_unit_ids.add(unit["id"])
            status = unit.get("status")
            if status not in VALID_STATUS:
                errors.append(f"{path}:{cid}:{uid}: statusが不正な値({status!r})")
            elif status == "available":
                available_count += 1
                if unit["id"] not in lesson_unit_ids:
                    errors.append(f"{path}:{cid}:{uid}: status=availableだがdata/lessons側に実在しない")

    if errors:
        print(f"NG: {len(errors)}件の違反")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)

    print(
        f"OK: {len(curriculum['categories'])}ジャンル・{total_units}ユニット"
        f"(available {available_count} / planned {total_units - available_count})すべて検証に合格"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
