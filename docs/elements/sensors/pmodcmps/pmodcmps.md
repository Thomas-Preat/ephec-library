# PMODCMPS

Ce module pilote un magnetometre type HMC5883L via I2C.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: I2C
- Dependances: `machine`, `math`

## Pinout

| Signal | Pico |
|---|---|
| SDA | A definir |
| SCL | A definir |
| Adresse I2C | 0x1E |

## Fonctions principales

- Initialisation et configuration du capteur.
- Lecture des axes bruts (`read_raw`) et en Gauss (`read_gauss`).
- Calcul du cap (`heading`) avec declinaison magnetique.
- Verification de l'identite (`identify`) et disponibilite des donnees (`is_ready`).

## Remarques

- Adresse I2C par defaut: `0x1E`.
- Un objet I2C doit etre fourni au constructeur.

## References

- Digilent PMOD CMPS2 (reference): https://digilent.com/reference/pmod/pmodcmps2/start
- HMC5883L datasheet: https://cdn.sparkfun.com/datasheets/Sensors/Magneto/HMC5883L-FDS.pdf
