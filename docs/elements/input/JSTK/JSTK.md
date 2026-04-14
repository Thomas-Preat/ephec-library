# PMOD JSTK

Ce module lit un joystick PMOD JSTK via SPI et expose les axes et boutons.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: SPI
- Dependances: `machine`, `time`

## Pinout

| Signal | Pico |
|---|---|
| SCK | GPIO 18 |
| MOSI | GPIO 19 |
| MISO | GPIO 16 |
| CS | GPIO 17 |

## Fonctions principales

- Lecture des axes `x` et `y` (10 bits).
- Lecture des boutons: joystick, `btn1`, `btn2`.
- `get_joystick_state()`: retourne un dictionnaire reutilisable.
- `show_dashboard()`: affiche un tableau de bord texte en temps reel.

## Remarques

- Le dashboard tourne en boucle jusqu'a `Ctrl+C`.
- Les fonctions utilitaires convertissent les axes en pourcentage.

## References

- Digilent PMOD JSTK2 (reference): https://digilent.com/reference/pmod/pmodjstk2/start
- MicroPython SPI API (officiel): https://docs.micropython.org/en/latest/library/machine.SPI.html
