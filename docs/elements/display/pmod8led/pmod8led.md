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

- `clear()` et `fill()` pour eteindre/allumer toutes les LED.
- `set_led(index, on)` et `toggle_led(index)` pour une LED.
- `write_byte(value)` pour ecrire un motif 8 bits.
- `chase()` pour un effet de chenillard.

## Remarques

- Il faut fournir exactement 8 broches dans l'ordre LED0..LED7.
- Le mode `active_high` est configurable.

## References

- Digilent PMOD 8LD (8 LEDs): https://digilent.com/reference/pmod/pmod8ld/start
- MicroPython Pin API (officiel): https://docs.micropython.org/en/latest/library/machine.Pin.html
