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

| Fonction | Parametres | Description |
|---|---|---|
| `PmodCMPS(i2c, addr=0x1E, declination_deg=0.0)` | `i2c`: instance I2C, `addr`: adresse du capteur, `declination_deg`: declinaison magnetique | Initialise et configure le magnetometre. |
| `set_gain(gain_cfg)` | `gain_cfg`: configuration de gain | Regle le gain de mesure du capteur. |
| `is_ready()` | Aucun | Indique si de nouvelles donnees sont disponibles. |
| `read_raw()` | Aucun | Lit les axes magnetiques bruts. |
| `read_gauss()` | Aucun | Retourne les axes convertis en Gauss. |
| `heading()` | Aucun | Calcule le cap magnetique corrige de la declinaison. |
| `identify()` | Aucun | Verifie l'identite du composant. |

## Remarques

- Adresse I2C par defaut: `0x1E`.
- Un objet I2C doit etre fourni au constructeur.

## References

- Digilent PMOD CMPS2 (reference): https://digilent.com/reference/pmod/pmodcmps2/start
- HMC5883L datasheet: https://cdn.sparkfun.com/datasheets/Sensors/Magneto/HMC5883L-FDS.pdf
