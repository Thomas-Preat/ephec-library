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

| Fonction | Parametres | Description |
|---|---|---|
| `RGBLed(pin_r, pin_g, pin_b, common_anode=False, pwm_freq=1000)` | `pin_r`, `pin_g`, `pin_b`: broches PWM, `common_anode`: type de LED, `pwm_freq`: frequence PWM | Initialise la LED RGB en PWM. |
| `set_rgb(red, green, blue)` | `red`, `green`, `blue`: intensites de `0` a `255` | Applique une couleur RGB a la LED. |
| `deinit()` | Aucun | Libere les sorties PWM de la LED RGB. |
| `BLERGBController(ble, led, name="Pico2W-RGB")` | `ble`: instance Bluetooth, `led`: instance `RGBLed`, `name`: nom du peripherique BLE | Initialise le service BLE de controle RGB et demarre la publicite. |

## Remarques

- Concu pour Pico 2W avec Bluetooth actif.
- `COMMON_ANODE` permet d'inverser la logique selon le type de LED.

## References

- Raspberry Pi Pico W documentation: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html
- MicroPython bluetooth API (officiel): https://docs.micropython.org/en/latest/library/bluetooth.html
