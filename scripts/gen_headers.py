#!/usr/bin/env python3
"""
Генератор THT-футпринтів гребінок/гнізд із кроком 2.54 мм для BFU Electronics.

Геометрія НЕ вигадується: це стандартна THT-геометрія гребінок 2.54 мм
з офіційної бібліотеки KiCad Connector_PinHeader_2.54mm.
  - крок 2.54 мм по обох осях
  - пад THT Ø1.7 мм, отвір Ø1.0 мм
  - пін 1 — прямокутний пад, решта — круглі
  - шари падів: "*.Cu" "*.Mask"
  - футпринт центрований у (0,0)
  - нумерація по стовпцях, у стовпці зверху вниз

Запуск:  py scripts/gen_headers.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "BFU_Electronics" / "BFU_Connector.pretty"

PITCH = 2.54
PAD_DIA = 1.7
DRILL = 1.0
SILK_OFFSET = 1.27   # половина кроку назовні від крайніх центрів падів
CRTYD_OFFSET = 0.25  # додатковий відступ courtyard від шовкографії
SILK_W = 0.12
CRTYD_W = 0.05
FAB_W = 0.1


def fmt(v: float) -> str:
    """Число без зайвих нулів; -0.0 нормалізуємо у 0."""
    v = round(v, 6)
    if v == 0:
        v = 0.0
    return f"{v:g}"


def gen(name: str, cols: int, rows: int, extra: str = "") -> str:
    n = cols * rows

    # координати сітки, центровані в (0,0)
    x0 = -(cols - 1) * PITCH / 2.0
    y0 = -(rows - 1) * PITCH / 2.0

    half_w = (cols - 1) * PITCH / 2.0
    half_h = (rows - 1) * PITCH / 2.0

    # межі шовкографії та courtyard
    sx = half_w + SILK_OFFSET
    sy = half_h + SILK_OFFSET
    cx = sx + CRTYD_OFFSET
    cy = sy + CRTYD_OFFSET

    descr = (f"BFU {cols}x{rows} THT pin header, 2.54mm pitch | {n} pins | "
             f"pad {fmt(PAD_DIA)}mm, drill {fmt(DRILL)}mm")
    if extra:
        descr += f" | {extra}"
    descr += (" | source: standard 0.1in (2.54mm) THT header geometry per "
              "official KiCad library Connector_PinHeader_2.54mm | BFU Electronics")

    tags = f"connector pin header THT 2.54mm {cols}x{rows}"

    L = []
    L.append(f'(footprint "{name}" (version 20221018) (generator "BFU_Electronics")')
    L.append('  (layer "F.Cu")')
    L.append(f'  (descr "{descr}")')
    L.append(f'  (tags "{tags}")')
    L.append('  (attr through_hole)')

    # reference над контуром, value під контуром
    L.append(f'  (fp_text reference "J**" (at 0 {fmt(-sy - 1.2)}) (layer "F.SilkS")'
             ' (effects (font (size 1 1) (thickness 0.15))))')
    L.append(f'  (fp_text value "{name}" (at 0 {fmt(sy + 1.2)}) (layer "F.Fab")'
             ' (effects (font (size 1 1) (thickness 0.15))))')

    # контур корпусу на F.SilkS
    L.append(f'  (fp_rect (start {fmt(-sx)} {fmt(-sy)}) (end {fmt(sx)} {fmt(sy)})'
             f' (stroke (width {SILK_W}) (type solid)) (fill none) (layer "F.SilkS"))')

    # контур на F.Fab (по крайніх центрах падів)
    L.append(f'  (fp_rect (start {fmt(-half_w)} {fmt(-half_h)}) (end {fmt(half_w)} {fmt(half_h)})'
             f' (stroke (width {FAB_W}) (type solid)) (fill none) (layer "F.Fab"))')

    # courtyard
    L.append(f'  (fp_rect (start {fmt(-cx)} {fmt(-cy)}) (end {fmt(cx)} {fmt(cy)})'
             f' (stroke (width {CRTYD_W}) (type solid)) (fill none) (layer "F.CrtYd"))')

    # маркер піна 1 — залитий трикутник у зовнішньому куті біля піна 1, катети 1.0 мм
    mx = -sx
    my = -sy
    L.append(f'  (fp_poly (pts (xy {fmt(mx)} {fmt(my)}) (xy {fmt(mx + 1.0)} {fmt(my)})'
             f' (xy {fmt(mx)} {fmt(my + 1.0)}))'
             f' (stroke (width {SILK_W}) (type solid)) (fill yes) (layer "F.SilkS"))')

    # пади: нумерація по стовпцях, у стовпці зверху вниз
    pin = 1
    for c in range(cols):
        for r in range(rows):
            px = x0 + c * PITCH
            py = y0 + r * PITCH
            shape = "rect" if pin == 1 else "circle"
            L.append(f'  (pad "{pin}" thru_hole {shape} (at {fmt(px)} {fmt(py)})'
                     f' (size {fmt(PAD_DIA)} {fmt(PAD_DIA)}) (drill {fmt(DRILL)})'
                     ' (layers "*.Cu" "*.Mask"))')
            pin += 1

    L.append(')')
    return "\n".join(L) + "\n"


# (ім'я, cols, rows, додатковий опис)
PARTS = [
    ("BFU_Header_1x04_P2.54mm", 4, 1, "I2C module: VCC GND SDA SCL"),
    ("BFU_Header_1x06_P2.54mm", 6, 1, "INMP441 breakout: VDD GND SD SCK WS L/R"),
    ("BFU_Header_1x07_P2.54mm", 7, 1, "MAX98357A breakout"),
    ("BFU_Header_1x08_P2.54mm", 8, 1, "ST7789 display module"),
    ("BFU_Header_2x08_P2.54mm", 8, 2, ""),
    ("BFU_Slot_2x16_P2.54mm", 16, 2,
     "BFU Module Bus: power + SPI + I2C + I2S + UART + CS/IRQ/EN"),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total_pads = 0
    for name, cols, rows, extra in PARTS:
        text = gen(name, cols, rows, extra)
        (OUT / f"{name}.kicad_mod").write_text(text, encoding="utf-8", newline="\n")
        pads = cols * rows
        total_pads += pads
        print(f"  ✓ {name}.kicad_mod  ({cols}x{rows} = {pads} pads)")
    print(f"\nЗгенеровано {len(PARTS)} футпринтів, падів: {total_pads}")


if __name__ == "__main__":
    main()
