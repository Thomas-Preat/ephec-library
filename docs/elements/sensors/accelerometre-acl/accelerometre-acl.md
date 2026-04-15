# Accelerometre ACL (ADXL345)

Ce module permet de lire un accelerometre 3 axes ADXL345 via SPI.

<img src="https://placehold.co/260x160/png?text=ADXL345" alt="Illustration ADXL345" width="220" align="left">

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

| Fonction | Parametres | Description |
|---|---|---|
| `ADXL345(sck, mosi, miso, cs, spi_id=0)` | `sck`, `mosi`, `miso`, `cs`: broches SPI, `spi_id`: bus SPI | Initialise le capteur ADXL345 en SPI. |
| `init_adxl345()` | Aucun | Active le mode mesure du capteur. |
| `set_range(range_g)` | `range_g`: plage de mesure (`2`, `4`, `8` ou `16`) | Configure la plage de mesure de l'accelerometre. |
| `write_register(register, value)` | `register`: adresse du registre, `value`: valeur a ecrire | Ecrit une valeur dans un registre ADXL345. |
| `read_register(reg, length=1)` | `reg`: adresse du registre, `length`: nombre d'octets a lire | Lit un ou plusieurs octets depuis un registre ADXL345. |
| `read_acceleration()` | Aucun | Retourne les accelerations brutes `(x, y, z)`. |

## Remarques

- Le script en bas du fichier lance une boucle de test continue.
- Les valeurs brutes sont converties en g avec un facteur simple (`x * 0.004`).

## References

- Digilent PMOD ACL (reference): https://digilent.com/reference/pmod/pmodacl/start
- ADXL345 datasheet (Analog Devices): https://www.analog.com/media/en/technical-documentation/data-sheets/adxl345.pdf
