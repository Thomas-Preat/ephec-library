# LCD (mode 8 bits)

Ce module fournit des fonctions utilitaires pour afficher du texte sur un LCD parallele en mode 8 bits.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: GPIO parallele
- Dependances: `machine`, `utime`

## Pinout

| Signal | Pico |
|---|---|
| RS | A definir |
| E | A definir |
| D0-D7 | A definir |

## Fonctions principales

- `lcd_init(...)`: initialise l'afficheur.
- `lcd_command(...)`: envoie une commande.
- `lcd_write_char(...)`: envoie un caractere.
- `lcd_set_cursor(...)`: place le curseur.
- `lcd_write_string(...)`: ecrit une chaine.

## Remarques

- Le module est fonctionnel, mais ne contient pas de classe complete ni de script de demo integre.
- Les broches doivent etre configurees par le programme appelant.

## References

- HD44780 datasheet (LCD controller): https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
- MicroPython Pin API (officiel): https://docs.micropython.org/en/latest/library/machine.Pin.html
