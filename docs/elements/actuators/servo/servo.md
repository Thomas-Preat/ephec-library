# Servo

Ce module pilote un servomoteur via PWM avec une API simple.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: PWM
- Dependances: `machine`, `time`

## Pinout

| Signal | Pico |
|---|---|
| Signal servo | GPIO 15 |
| VCC servo | Selon le servo |
| GND servo | GND |

## Fonctions principales

- `set_angle(angle)`: positionne le servo entre `-90` et `90` degres.
- `get_angle()`: retourne l'angle courant.
- `calibrate(min_pulse, max_pulse)`: ajuste les impulsions min/max.
- `sweep(start, end, step, delay)`: effectue un balayage automatique.
- `detach()`: desactive le PWM.

## Remarques

- Frequence PWM par defaut: `50 Hz`.
- Les valeurs `min_pulse` et `max_pulse` peuvent varier selon le modele.

## References

- MicroPython PWM (officiel): https://docs.micropython.org/en/latest/library/machine.PWM.html
- Servo SG90 (specifications): https://www.servodatabase.com/servo/towerpro/sg90
