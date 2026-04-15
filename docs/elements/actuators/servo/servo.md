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

| Fonction | Parametres | Description |
|---|---|---|
| `ServoMotor(pin_number, min_pulse=600, max_pulse=2400, frequency=50)` | `pin_number`: broche PWM, `min_pulse`: impulsion minimale, `max_pulse`: impulsion maximale, `frequency`: frequence PWM | Initialise le servomoteur et la sortie PWM. |
| `set_angle(angle)` | `angle`: position entre `-90` et `90` degres | Positionne le servo a l'angle demande. |
| `get_angle()` | Aucun | Retourne l'angle courant du servo. |
| `calibrate(min_pulse, max_pulse)` | `min_pulse`: nouvelle impulsion min, `max_pulse`: nouvelle impulsion max | Ajuste la calibration PWM pour le modele de servo utilise. |
| `sweep(start=-90, end=90, step=5, delay=0.05)` | `start`: angle de depart, `end`: angle final, `step`: increment, `delay`: pause entre deux positions | Effectue un balayage automatique du servo. |
| `detach()` | Aucun | Desactive la PWM et libere la ressource. |

## Remarques

- Frequence PWM par defaut: `50 Hz`.
- Les valeurs `min_pulse` et `max_pulse` peuvent varier selon le modele.

## References

- MicroPython PWM (officiel): https://docs.micropython.org/en/latest/library/machine.PWM.html
- Servo SG90 (specifications): https://www.servodatabase.com/servo/towerpro/sg90
