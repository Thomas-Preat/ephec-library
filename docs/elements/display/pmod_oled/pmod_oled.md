# PMOD OLED (SSD1306)

Ce module pilote un PMOD OLED base sur SSD1306 en SPI.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: SPI
- Dependances: `machine`, `framebuf`, `utime`

## Pinout

| Signal | Pico |
|---|---|
| SCK | GPIO 2 |
| MOSI | GPIO 3 |
| CS | GPIO 5 |
| DC | GPIO 6 |
| RST | GPIO 7 |
| VBAT | GPIO 8 |
| VDCC | GPIO 9 |

## Fonctions principales

- Initialise le controleur SSD1306 et le framebuffer.
- Affiche du texte et des graphismes via les methodes FrameBuffer.
- `show()`, `poweron()`, `poweroff()`, `contrast()`, `invert()`, `rotate_180()`.

## Remarques

- `demo()` dans la classe permet un test visuel rapide.
- La resolution par defaut est `128x32`.

## References

- Digilent PMOD OLED (reference): https://digilent.com/reference/pmod/pmodoled/start
- SSD1306 datasheet: https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf
