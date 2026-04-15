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

| Fonction | Parametres | Description |
|---|---|---|
| `lcd_init(rs, e, data_pins)` | `rs`: broche RS, `e`: broche Enable, `data_pins`: liste D0 a D7 | Initialise l'afficheur LCD en mode 8 bits. |
| `lcd_command(rs, e, data_pins, cmd)` | `rs`: broche RS, `e`: broche Enable, `data_pins`: lignes de donnees, `cmd`: commande a envoyer | Envoie une commande au LCD. |
| `lcd_write_char(rs, e, data_pins, char)` | `rs`: broche RS, `e`: broche Enable, `data_pins`: lignes de donnees, `char`: caractere ASCII | Ecrit un caractere sur l'afficheur. |
| `lcd_set_cursor(rs, e, data_pins, row, col)` | `rs`: broche RS, `e`: broche Enable, `data_pins`: lignes de donnees, `row`: ligne, `col`: colonne | Place le curseur a la position voulue. |
| `lcd_write_string(rs, e, data_pins, text)` | `rs`: broche RS, `e`: broche Enable, `data_pins`: lignes de donnees, `text`: texte a afficher | Ecrit une chaine complete sur le LCD. |

## Remarques

- Le module est fonctionnel, mais ne contient pas de classe complete ni de script de demo integre.
- Les broches doivent etre configurees par le programme appelant.

## References

- HD44780 datasheet (LCD controller): https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
- MicroPython Pin API (officiel): https://docs.micropython.org/en/latest/library/machine.Pin.html
