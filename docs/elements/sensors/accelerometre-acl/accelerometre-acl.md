# Accelerometre ACL (ADXL345)

Ce module permet de lire un accelerometre 3 axes ADXL345 via SPI.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: SPI
- Dependances: `machine`, `time`

## Pinout

| Signal | Pico |
|---|---|
| SCK | GPIO 18 |
| MOSI | GPIO 19 |
| MISO | GPIO 16 |
| CS | GPIO 17 |

## Fonctions principales

- Initialisation SPI et mise en mode mesure.
- Configuration de la plage: `2g`, `4g`, `8g`, `16g` via `set_range()`.
- Lecture des axes bruts avec `read_acceleration()`.

## Remarques

- Le script en bas du fichier lance une boucle de test continue.
- Les valeurs brutes sont converties en g avec un facteur simple (`x * 0.004`).

## References

- Digilent PMOD ACL (reference): https://digilent.com/reference/pmod/pmodacl/start
- ADXL345 datasheet (Analog Devices): https://www.analog.com/media/en/technical-documentation/data-sheets/adxl345.pdf