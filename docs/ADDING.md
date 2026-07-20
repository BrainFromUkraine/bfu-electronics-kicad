# Додавання нового компонента

## 1. Знайти джерело розмірів

За пріоритетом:

1. **Даташит виробника** → розділ *Recommended PCB Land Pattern* або
   *Mechanical Drawing*. Збережи PDF у `datasheets/`.
2. **Офіційна бібліотека виробника** — напр. `espressif/kicad-libraries`
   для всіх модулів ESP32.
3. **Офіційна бібліотека KiCad** — `kicad-footprints`.
4. **LCSC / JLCPCB** — за LCSC-номером:
   ```bash
   pip install easyeda2kicad
   easyeda2kicad --full --lcsc_id=C411294
   ```
   Обов'язково звірити з кресленням даташита.

Якщо жодного джерела немає — **компонент не додаємо**.

## 2. Вибрати категорію

| Категорія | Що кладемо |
|---|---|
| `BFU_RF` | LoRa, SX126x, радіомодулі, антени |
| `BFU_MCU` | ESP32, WROOM, MINI, dev-плати |
| `BFU_Display` | TFT, OLED, e-Paper, FPC-роз'єми дисплеїв |
| `BFU_Audio` | мікрофони I2S, підсилювачі, динаміки |
| `BFU_GNSS` | GPS/GNSS модулі й антени |
| `BFU_Power` | LDO, DC-DC, зарядка Li-Ion, тримачі АКБ |
| `BFU_Connector` | USB, гребінки, JST, IPEX/U.FL |
| `BFU_Sensor` | IMU, тиск, температура, вологість |

## 3. Створити файл

Ім'я файлу = **точний партномер**: `ST7789V.kicad_mod`, `INMP441.kicad_mod`.

Шаблон:

```
(footprint "PARTNUMBER" (version 20221018) (generator "BFU_Electronics")
  (layer "F.Cu")
  (descr "Виробник Партномер | ключові параметри | ГхШхВ мм | тип корпусу | джерело розмірів")
  (tags "пошукові слова")
  (attr smd)
  (fp_text reference "U**" (at 0 -Y) (layer "F.SilkS")
    (effects (font (size 1 1) (thickness 0.15))))
  (fp_text value "PARTNUMBER" (at 0 Y) (layer "F.Fab")
    (effects (font (size 1 1) (thickness 0.15))))
  ... контур на F.SilkS ...
  ... courtyard на F.CrtYd ...
  ... маркер піна 1 ...
  (pad "1" smd rect (at X Y) (size W H) (layers "F.Cu" "F.Paste" "F.Mask"))
  ...
)
```

Для THT-падів:

```
  (pad "1" thru_hole circle (at X Y) (size 1.7 1.7) (drill 1.0)
    (layers "*.Cu" "*.Mask"))
```

## 4. Обов'язкові елементи

- `descr` із **джерелом розмірів**
- `tags`
- `attr smd` / `attr through_hole`
- контур корпусу на `F.SilkS`
- `F.CrtYd` — courtyard, відступ 0.25–0.5 мм від габариту
- маркер піна 1 (кружечок на шовкографії або зріз кута)
- для RF-модулів з PCB-антеною — **зона keepout антени** на `F.Fab`

## 5. Перевірити

```bash
python scripts/validate.py
```

Потім у KiCad: **Редактор посадкових місць** → відкрити футпринт →
**Інспектор → Виміряти** — звірити крок падів і габарит із даташитом.

## 6. Закомітити

```
add(BFU_Display): ST7789V — 240x320 TFT, FPC 8-pin
```

Оновити таблицю компонентів у [README.md](../README.md).
