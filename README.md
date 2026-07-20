<p align="center">
  <img src="docs/banner.svg" alt="BFU Electronics — KiCad Footprint Library" width="100%">
</p>

<p align="center">
  <a href="../../actions/workflows/validate.yml"><img src="../../actions/workflows/validate.yml/badge.svg" alt="Перевірка футпринтів"></a>
  <img src="https://img.shields.io/badge/KiCad-9.0-blue" alt="KiCad 9.0">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
</p>

Бібліотека футпринтів KiCad для проєктів **Brain From Ukraine**.
Основний споживач — **SICH**, автономний LoRa-комунікатор на ESP32-S3.

Кожен футпринт зроблено за офіційним даташитом виробника або перевіреною
бібліотекою. Розміри не вигадуються — [чому це принципово](CONTRIBUTING.md).

## Що всередині

| Бібліотека | Категорія | Компоненти |
|---|---|---|
| `BFU_RF` | RF / бездротові | E22-900M30S |
| `BFU_MCU` | Мікроконтролери | ESP32-S3-WROOM-1 |
| `BFU_Display` | Дисплеї | — |
| `BFU_Audio` | Аудіо | — |
| `BFU_GNSS` | Навігація | — |
| `BFU_Power` | Живлення | — |
| `BFU_Connector` | Роз'єми | — |
| `BFU_Sensor` | Сенсори | — |

### BFU_RF

**E22-900M30S** — Ebyte, SX1262, 1 Вт (30 dBm), 868/915 МГц.
Корпус 24.0 × 38.5 × 3.87 мм, 22 краєві SMD-пади, крок 2.54 мм.
Розміри — з офіційного механічного креслення Ebyte.

### BFU_MCU

**ESP32-S3-WROOM-1** — Espressif, Wi-Fi + BLE.
Корпус 18.0 × 25.5 × 3.1 мм, 40 SMD-падів 1.5 × 0.9 мм крок 1.27 мм,
плюс EPAD (пін 41) — 11 теплових падів 0.9 × 0.9 мм.
Land pattern з офіційної бібліотеки Espressif.

> **Увага:** верхні ~6 мм модуля — зона антени. Під нею заборонено вести мідь,
> лити полігони чи ставити компоненти. Позначена штриховою рамкою на `F.Fab`.

## Встановлення

```bash
git clone https://github.com/BrainFromUkraine/bfu-electronics-kicad.git
```

Далі в KiCad 9:

1. **Налаштування → Налаштувати шляхи** → `+`
   - Ім'я: `BFU_LIB`
   - Шлях: шлях до теки `BFU_Electronics` усередині репозиторію
2. **Налаштування → Керування бібліотеками посадкових місць** → вкладка
   **Глобальні** → кнопка **теки** → зайди в `BFU_Electronics` і вибери
   потрібні теки `.pretty` (можна кілька через Ctrl)
3. У виборі футпринта шукай за префіксом: `BFU_RF:E22-900M30S`

Детальніше — [docs/INSTALL.md](docs/INSTALL.md).

## Додавання компонента

Головне правило — [**не видумуй**](CLAUDE.md). Кожен розмір походить
з офіційного даташита або перевіреної бібліотеки виробника.

Покроково — [docs/ADDING.md](docs/ADDING.md).

Перед комітом:

```bash
python scripts/validate.py
```

## Ліцензія

MIT — див. [LICENSE](LICENSE).
Футпринти надаються як є; перед запуском плати у виробництво
завжди звіряй посадкове місце з даташитом компонента.

---

**Brain From Ukraine** · [YouTube](https://www.youtube.com/@BrainFromUkraine)

## Долучитися

Див. [CONTRIBUTING.md](CONTRIBUTING.md). Коротко: джерело розмірів обов'язкове,
перед PR проганяємо `python scripts/validate.py`.
