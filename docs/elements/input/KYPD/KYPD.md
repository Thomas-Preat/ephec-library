# KYPD (clavier matriciel)

Ce module scanne un clavier matriciel 4x4 avec des GPIO Pico.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: matrice GPIO
- Dependances: `machine`, `time`

## Pinout

| Signal | Pico |
|---|---|
| Lignes (R0-R3) | GPIO 2, 3, 4, 5 |
| Colonnes (C0-C3) | GPIO 9, 8, 7, 6 |

## Fonctions principales

| Fonction | Parametres | Description |
|---|---|---|
| `scan_keypad()` | Aucun | Scanne la matrice 4x4 et retourne la touche detectee ou `None`. |

## Remarques

- Le script utilise un delai anti-rebond simple (`time.sleep(0.3)`).

## References

- Digilent PMOD KYPD (reference): https://digilent.com/reference/pmod/pmodkypd/start
- Matrix keypad scanning concept: https://www.embeddedrelated.com/showarticle/519.php
