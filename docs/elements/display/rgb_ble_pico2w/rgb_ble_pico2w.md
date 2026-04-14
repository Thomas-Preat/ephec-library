# RGB BLE Pico 2W

Ce module pilote une LED RGB via BLE avec un service GATT personnalise.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico 2W
- Interface: PWM, BLE
- Dependances: `machine`, `bluetooth`, `micropython`, `time`

## Pinout

| Signal | Pico |
|---|---|
| R | GPIO 16 |
| G | GPIO 17 |
| B | GPIO 18 |

## Fonctions principales

- Controle PWM des canaux rouge, vert, bleu.
- Expose une caracteristique BLE pour ecrire une couleur.
- Formats acceptes: `OFF`, `#RRGGBB`, `R,G,B`.
- Notification de retour `OK ...` ou `ERR ...`.

## Remarques

- Concu pour Pico 2W avec Bluetooth actif.
- `COMMON_ANODE` permet d'inverser la logique selon le type de LED.

## References

- Raspberry Pi Pico W documentation: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html
- MicroPython bluetooth API (officiel): https://docs.micropython.org/en/latest/library/bluetooth.html
