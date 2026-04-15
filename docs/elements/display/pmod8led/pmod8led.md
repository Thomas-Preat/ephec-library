# PMOD8LED

Ce module controle un PMOD 8 LED avec 8 GPIO.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: GPIO
- Dependances: `machine`

## Pinout

| Signal | Pico |
|---|---|
| LED0-LED7 | 8 GPIO a definir |

## Fonctions principales

| Fonction | Parametres | Description |
|---|---|---|
| `Pmod8LED(led_pins, active_high=True)` | `led_pins`: liste des 8 broches, `active_high`: logique active haute ou basse | Initialise le module 8 LED avec les broches choisies. |
| `clear()` | Aucun | Eteint toutes les LED. |
| `fill(on=True)` | `on`: etat a appliquer a toutes les LED | Allume ou eteint toutes les LED. |
| `set_led(index, on=True)` | `index`: LED de `0` a `7`, `on`: etat a appliquer | Modifie l'etat d'une LED precise. |
| `toggle_led(index)` | `index`: LED de `0` a `7` | Inverse l'etat d'une LED. |
| `write_byte(value)` | `value`: motif 8 bits a afficher | Ecrit un motif binaire sur les LED. |
| `chase(delay_s=0.1, cycles=1)` | `delay_s`: pause entre deux LED, `cycles`: nombre de cycles | Cree un effet de chenillard. |

## Remarques

- Il faut fournir exactement 8 broches dans l'ordre LED0..LED7.
- Le mode `active_high` est configurable.

## References

- Digilent PMOD 8LD (8 LEDs): https://digilent.com/reference/pmod/pmod8ld/start
- MicroPython Pin API (officiel): https://docs.micropython.org/en/latest/library/machine.Pin.html
