# RGB Fade Pico 2W

Ce module realise un fondu de couleurs continu sur une LED RGB.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: PWM
- Dependances: `machine`, `time`

## Pinout

| Signal | Pico |
|---|---|
| R | GPIO 16 |
| G | GPIO 17 |
| B | GPIO 18 |

## Fonctions principales

- Controle PWM des 3 canaux RGB.
- Fonction `wheel(pos)` pour generer un cycle couleur fluide.
- Boucle `main()` qui fait varier la couleur en continu.

## Remarques

- `STEP_DELAY_MS` ajuste la vitesse d'animation.
- `COMMON_ANODE` permet l'usage avec LED anode commune.

## References

- Raspberry Pi Pico documentation: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html
- MicroPython PWM (officiel): https://docs.micropython.org/en/latest/library/machine.PWM.html
