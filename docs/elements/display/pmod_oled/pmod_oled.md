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

| Fonction | Parametres | Description |
|---|---|---|
| `PmodOLED(width=128, height=32, spi_id=0, baudrate=10000000, sck=2, mosi=3, cs=5, dc=6, rst=7, vbat=8, vdcc=9)` | `width`, `height`: resolution, `spi_id`: bus SPI, `baudrate`: vitesse SPI, `sck`, `mosi`, `cs`, `dc`, `rst`, `vbat`, `vdcc`: broches de controle | Initialise le controleur SSD1306 et le framebuffer SPI. |
| `show()` | Aucun | Rafraichit l'ecran avec le contenu du buffer. |
| `poweron()` | Aucun | Allume l'afficheur. |
| `poweroff()` | Aucun | Eteint l'afficheur. |
| `contrast(value)` | `value`: contraste de `0` a `255` | Regle le contraste de l'ecran. |
| `invert(invert_on=True)` | `invert_on`: active ou non l'inversion | Inverse ou restaure l'affichage des pixels. |
| `rotate_180(enabled=True)` | `enabled`: active ou non la rotation | Active ou desactive la rotation de l'ecran a `180` degres. |

## Remarques

- `demo()` dans la classe permet un test visuel rapide.
- La resolution par defaut est `128x32`.

## References

- Digilent PMOD OLED (reference): https://digilent.com/reference/pmod/pmodoled/start
- SSD1306 datasheet: https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf
