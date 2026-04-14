# PMOD I2S2

Ce module pilote la sortie audio I2S (DAC) du PMOD I2S2.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: I2S, PIO
- Dependances: `machine`, `rp2`, `math`, `array`

## Pinout

| Signal | Pico |
|---|---|
| MCLK | GPIO 8 |
| SDOUT | GPIO 9 |
| BCLK | GPIO 10 |
| LRCLK | GPIO 11 |

## Fonctions principales

- Initialise I2S en transmission stereo.
- Genere MCLK via un StateMachine PIO.
- Construit une table sinus et joue un son avec `play_tone()`.
- Libere les ressources avec `deinit()`.

## Remarques

- Frequence d'echantillonnage par defaut: `16000 Hz`.
- Le `main()` joue une sequence de test (220, 440, 523 Hz).

## References

- Digilent PMOD I2S2 (reference): https://digilent.com/reference/pmod/pmodi2s2/start
- MicroPython I2S (officiel): https://docs.micropython.org/en/latest/library/machine.I2S.html
