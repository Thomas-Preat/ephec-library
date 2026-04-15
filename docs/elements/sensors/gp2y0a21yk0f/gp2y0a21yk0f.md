# GP2Y0A21YK0F

Ce module lit un capteur infrarouge analogique de distance Sharp GP2Y0A21YK0F.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: ADC
- Dependances: `machine`, `utime`, `math`

## Pinout

| Signal | Pico |
|---|---|
| OUT (analogique) | GPIO 26 |
| VCC | 5V module |
| GND | GND |

## Fonctions principales

| Fonction | Parametres | Description |
|---|---|---|
| `GP2Y0A21YK0F(adc_pin=26, voltage_ref=3.3, bit_resolution=12)` | `adc_pin`: broche analogique, `voltage_ref`: tension de reference, `bit_resolution`: resolution ADC cible | Initialise le capteur de distance analogique. |
| `read_raw()` | Aucun | Retourne la lecture brute ADC. |
| `read_voltage()` | Aucun | Convertit la lecture brute en tension. |
| `read_distance()` | Aucun | Estime la distance en cm avec validation de plage. |
| `read_distance_raw()` | Aucun | Estime la distance en cm sans validation de plage. |
| `read_distance_smooth(samples=10, delay_ms=5)` | `samples`: nombre de mesures, `delay_ms`: pause entre mesures | Filtre la mesure par moyenne glissante. |
| `calibrate(known_distance_cm, samples=20)` | `known_distance_cm`: distance de reference, `samples`: nombre de mesures pour la calibration | Calibre le modele sur une distance connue. |
| `set_calibration(a_coeff, b_coeff)` | `a_coeff`, `b_coeff`: coefficients du modele | Definit manuellement la calibration active. |
| `get_calibration()` | Aucun | Retourne les coefficients de calibration actifs. |
| `test(duration_seconds=10)` | `duration_seconds`: duree du test | Lance une boucle de test et affiche les mesures. |

## Remarques

- Le capteur est typiquement fiable entre environ 10 et 80 cm.
- Les coefficients de calibration peuvent etre ajustes selon votre montage.

## References

- GP2Y0A21YK0F datasheet (Sharp): https://www.pololu.com/file/0J85/gp2y0a21yk0f.pdf
- Product/application notes (Pololu): https://www.pololu.com/product/136
