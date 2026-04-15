# DHT11

Ce module lit un capteur DHT11 pour la temperature et l'humidite.

<img src="https://placehold.co/640x360/png?text=DHT11" alt="Illustration DHT11" width="220" align="left">

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: GPIO numerique (protocole DHT)
- Dependances: `machine`, `dht`, `time`

## Pinout

| Signal | Pico |
|---|---|
| DATA | GPIO 16 |
| VCC | 3.3V |
| GND | GND |

## Fonctions principales

| Fonction | Parametres | Description |
|---|---|---|
| `DHT11Sensor(pin=16)` | `pin`: broche DATA du capteur | Initialise le capteur DHT11 sur une broche GPIO. |
| `measure(retries=3, retry_delay_ms=250)` | `retries`: nombre de tentatives, `retry_delay_ms`: delai entre tentatives | Lance une mesure et memorise la derniere lecture. |
| `read(retries=3)` | `retries`: nombre de tentatives | Retourne un dictionnaire avec validite, temperature et humidite. |
| `temperature_c()` | Aucun | Retourne la derniere temperature mesuree en degres Celsius. |
| `humidity_percent()` | Aucun | Retourne la derniere humidite relative mesuree en pourcentage. |
| `comfort_state()` | Aucun | Retourne un etat simple (`comfortable`, `dry`, `humid`, etc.). |

## Remarques

- Le DHT11 est lent: evitez les lectures plus rapides qu'environ 1 seconde.
- Le module `dht` est utilise pour gerer le protocole temporel du capteur.
- Si les lectures echouent, verifiez la resistance de tirage sur DATA (souvent 4.7k a 10k selon module).

## References

- MicroPython DHT API (officiel): https://docs.micropython.org/en/latest/library/dht.html
- DHT11 datasheet (Aosong): https://components101.com/sites/default/files/component_datasheet/DHT11-Temperature-Sensor.pdf
