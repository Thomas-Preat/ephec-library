# PMOD I2S2

Ce module pilote la sortie audio I2S (DAC) du PMOD I2S2.

<img src="https://placehold.co/260x160/png?text=PMOD+I2S2" alt="Illustration PMOD I2S2" width="220" align="left">

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

| Fonction | Parametres | Description |
|---|---|---|
| `PmodI2S2TX(i2s_id=0, sample_rate=16000, bits=16, mclk_mult=256, pin_mclk=8, pin_sdout=9, pin_bclk=10, pin_lrclk=11, ibuf=20000)` | `i2s_id`: bus I2S, `sample_rate`: frequence d'echantillonnage, `bits`: resolution, `mclk_mult`: multiplicateur MCLK, `pin_*`: broches audio, `ibuf`: taille du buffer I2S | Initialise la sortie audio I2S et la generation d'horloge MCLK. |
| `play_tone(freq_hz=440, seconds=2.0, amplitude=10000, frames=512)` | `freq_hz`: frequence de la note, `seconds`: duree, `amplitude`: volume, `frames`: taille du buffer audio | Construit et joue une tonalite sinusoidale stereo. |
| `deinit()` | Aucun | Libere proprement les ressources I2S et PIO. |

## Remarques

- Frequence d'echantillonnage par defaut: `16000 Hz`.
- Le `main()` joue une sequence de test (220, 440, 523 Hz).

## References

- Digilent PMOD I2S2 (reference): https://digilent.com/reference/pmod/pmodi2s2/start
- MicroPython I2S (officiel): https://docs.micropython.org/en/latest/library/machine.I2S.html

