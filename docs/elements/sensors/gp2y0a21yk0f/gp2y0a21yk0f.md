# GP2Y0A21YK0F

Ce module lit un capteur infrarouge analogique de distance Sharp GP2Y0A21YK0F.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: ADC
- Dependances: `machine`, `utime`, `math`

## Pinout

| Signal | Pico |
|---|---|
| OUT (analogique) | GPIO 26 |
| VCC | 5V module |
| GND | GND |

## Fonctions principales

- Lecture brute ADC (`read_raw`) et tension (`read_voltage`).
- Conversion en distance (`read_distance`, `read_distance_raw`).
- Filtrage par moyenne (`read_distance_smooth`).
- Outils de calibration (`calibrate`, `set_calibration`, `get_calibration`).

## Remarques

- Le capteur est typiquement fiable entre environ 10 et 80 cm.
- Les coefficients de calibration peuvent etre ajustes selon votre montage.

## References

- GP2Y0A21YK0F datasheet (Sharp): https://www.pololu.com/file/0J85/gp2y0a21yk0f.pdf
- Product/application notes (Pololu): https://www.pololu.com/product/136
