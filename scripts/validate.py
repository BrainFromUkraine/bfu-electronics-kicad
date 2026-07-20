#!/usr/bin/env python3
"""
Перевірка футпринтів бібліотеки BFU Electronics.
Запуск:  python scripts/validate.py
Код виходу 1, якщо є помилки — зручно для CI та pre-commit.
"""
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "BFU_Electronics"

errors = []
warnings = []
stats = {"libs": 0, "footprints": 0}


def check_footprint(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    name = path.stem
    rel = path.relative_to(ROOT)

    # сучасний формат KiCad 6+
    if not text.lstrip().startswith("(footprint"):
        if text.lstrip().startswith("(module"):
            errors.append(f"{rel}: старий формат (module ...) — конвертуй у (footprint ...)")
        else:
            errors.append(f"{rel}: не схоже на футпринт KiCad")
        return

    # ім'я всередині має збігатися з іменем файлу
    m = re.match(r'\(footprint\s+"([^"]+)"', text.lstrip())
    if m and m.group(1) != name:
        errors.append(f'{rel}: ім\'я всередині "{m.group(1)}" != імені файлу "{name}"')

    # обов'язкові поля
    if "(descr" not in text:
        errors.append(f"{rel}: немає (descr ...) — опиши компонент і джерело розмірів")
    if "(tags" not in text:
        warnings.append(f"{rel}: немає (tags ...)")
    if "F.CrtYd" not in text and "B.CrtYd" not in text:
        warnings.append(f"{rel}: немає courtyard (F.CrtYd)")
    if "F.SilkS" not in text:
        warnings.append(f"{rel}: немає шовкографії (F.SilkS)")
    if not re.search(r'\(attr\s+(smd|through_hole)', text):
        warnings.append(f"{rel}: немає (attr smd|through_hole)")

    # пади
    pads = re.findall(r'\(pad\s+"?([^"\s]+)"?\s', text)
    if not pads:
        errors.append(f"{rel}: жодного пада")
    else:
        stats.setdefault("pads", 0)
        stats["pads"] = stats.get("pads", 0) + len(pads)

    # згадка джерела розмірів — м'яка вимога
    src_hint = any(k in text.lower() for k in
                   ("datasheet", "land pattern", "даташит", "official"))
    if not src_hint:
        warnings.append(f"{rel}: у descr не вказане джерело розмірів")


def main():
    if not LIB.is_dir():
        print(f"ПОМИЛКА: не знайдено теку {LIB}")
        return 1

    for lib_dir in sorted(LIB.iterdir()):
        if not lib_dir.is_dir():
            continue
        if not lib_dir.name.endswith(".pretty"):
            errors.append(f"{lib_dir.name}: тека бібліотеки має закінчуватись на .pretty")
            continue
        stats["libs"] += 1
        mods = sorted(lib_dir.glob("*.kicad_mod"))
        if not mods:
            print(f"  ○ {lib_dir.name}: порожня")
            continue
        for mod in mods:
            stats["footprints"] += 1
            check_footprint(mod)
            print(f"  ✓ {lib_dir.name}/{mod.name}")

    # fp-lib-table
    table = LIB / "fp-lib-table"
    if not table.exists():
        warnings.append("немає fp-lib-table")

    print()
    print(f"бібліотек: {stats['libs']}   футпринтів: {stats['footprints']}"
          f"   падів: {stats.get('pads', 0)}")

    if warnings:
        print(f"\nПОПЕРЕДЖЕННЯ ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")

    if errors:
        print(f"\nПОМИЛКИ ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")
        return 1

    print("\nУсе гаразд.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
