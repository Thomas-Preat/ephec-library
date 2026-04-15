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

| Fonction | Parametres | Description |
|---|---|---|
| `RGBLed(pin_r, pin_g, pin_b, common_anode=False, pwm_freq=1000)` | `pin_r`, `pin_g`, `pin_b`: broches PWM, `common_anode`: type de LED, `pwm_freq`: frequence PWM | Initialise la LED RGB en PWM. |
| `set_rgb(red, green, blue)` | `red`, `green`, `blue`: intensites de `0` a `255` | Applique une couleur RGB a la LED. |
| `deinit()` | Aucun | Libere les sorties PWM de la LED RGB. |
| `wheel(pos)` | `pos`: position de `0` a `255` dans le cycle | Genere une couleur RGB dans un fondu continu. |

## Remarques

- `STEP_DELAY_MS` ajuste la vitesse d'animation.
- `COMMON_ANODE` permet l'usage avec LED anode commune.

## References

- Raspberry Pi Pico documentation: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html
- MicroPython PWM (officiel): https://docs.micropython.org/en/latest/library/machine.PWM.html
