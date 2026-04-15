# Capteur de mouvement (PIR)

Ce module encapsule un capteur PIR (ex: HC-SR501) pour detecter une presence.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: GPIO numerique
- Dependances: `machine`, `utime`

## Pinout

| Signal | Pico |
|---|---|
| OUT | GPIO 16 |
| VCC | Selon module PIR |
| GND | GND |

## Fonctions principales

| Fonction | Parametres | Description |
|---|---|---|
| `PIRMotionSensor(pin=16, pull=None)` | `pin`: broche du capteur, `pull`: configuration de resistance interne | Initialise le capteur PIR en configurant une broche GPIO en entree. |
| `motion()` | Aucun | Retourne `True` si un mouvement est detecte, sinon `False`. |
| `read()` | Aucun | Retourne l'etat brut du capteur (`0` ou `1`). |
| `wait_for_motion(timeout_ms=None, poll_ms=20)` | `timeout_ms`: delai maximal, `poll_ms`: intervalle entre deux lectures | Attend la detection d'un mouvement avec timeout optionnel. |

## Remarques

- Un capteur PIR necessite souvent un court temps de stabilisation au demarrage.
- Le comportement depend des reglages du module (sensibilite, temporisation).

## References

- HC-SR501 PIR overview: https://components101.com/sensors/hc-sr501-pir-sensor
- MicroPython Pin API (officiel): https://docs.micropython.org/en/latest/library/machine.Pin.html
