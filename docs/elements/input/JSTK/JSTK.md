# PMOD JSTK

Ce module lit un joystick PMOD JSTK via SPI et expose les axes et boutons.

<img src="https://placehold.co/260x160/png?text=PMOD+JSTK" alt="Illustration PMOD JSTK" width="220" align="left">

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

| Fonction | Parametres | Description |
|---|---|---|
| `PmodJSTK(spi_id=0, sck=18, mosi=19, miso=16, cs=17)` | `spi_id`: bus SPI, `sck`, `mosi`, `miso`, `cs`: broches SPI | Initialise le joystick PMOD JSTK via SPI. |
| `read()` | Aucun | Lit les axes et boutons dans leur format brut. |
| `get_joystick_state(jstk)` | `jstk`: instance `PmodJSTK` | Retourne un dictionnaire d'etat reutilisable pour les axes et boutons. |
| `show_dashboard(jstk, refresh_s=0.08)` | `jstk`: instance `PmodJSTK`, `refresh_s`: periode de rafraichissement | Affiche un tableau de bord texte en temps reel. |

## Remarques

- Le dashboard tourne en boucle jusqu'a `Ctrl+C`.
- Les fonctions utilitaires convertissent les axes en pourcentage.

## References

- Digilent PMOD JSTK2 (reference): https://digilent.com/reference/pmod/pmodjstk2/start
- MicroPython SPI API (officiel): https://docs.micropython.org/en/latest/library/machine.SPI.html

