# MAXSONAR

Ce module simplifie la lecture d'un capteur de distance MAXSONAR.

## Fiche rapide

- Plateforme: MicroPython / Raspberry Pi Pico
- Interface: PWM, ADC, UART
- Dependances: `machine`, `time`

## Pinout

| Signal | Pico |
|---|---|
| PWM | GPIO 15 |
| AN (analogique) | GPIO 26 |
| Sensor TX -> Pico RX | GPIO 1 |
| Sensor RX -> Pico TX | GPIO 0 |

## Fonctions principales

| Fonction | Parametres | Description |
|---|---|---|
| `PmodMaxSonar(...)` | `pwm_pin=15`, `an_pin=26`, `uart_id=0`, `uart_baud=9600`, `sensor_tx_pin=1`, `sensor_rx_pin=0`, `timeout_us=60000` | Initialise le capteur et configure les interfaces PWM, ADC et UART. |
| `read_pulse_us()` | Aucun | Lit la largeur d'impulsion PWM en microsecondes. |
| `read_analog_raw()` | Aucun | Lit la valeur analogique brute du capteur. |
| `read_analog_volts(vref=3.3)` | `vref`: tension de reference ADC | Convertit la lecture analogique en volts. |
| `send_range_trigger()` | Aucun | Declenche une nouvelle mesure du capteur. |
| `read_uart_packet()` | Aucun | Lit la trame UART brute envoyee par le capteur. |
| `read_uart_inches()` | Aucun | Lit la trame UART et extrait la distance en pouces si elle est valide. |
| `get_pwm_state(sensor, max_cm=300.0)` | `sensor`: instance du capteur, `max_cm`: distance max pour le pourcentage | Retourne un etat complet base sur la lecture PWM. |
| `get_analog_state(sensor, max_cm=300.0)` | `sensor`: instance du capteur, `max_cm`: distance max pour le pourcentage | Retourne un etat complet base sur la lecture analogique. |
| `get_uart_state(sensor)` | `sensor`: instance du capteur | Retourne un etat complet base sur la lecture UART. |

## Remarques

- Les conversions en distance reposent sur des echelles MAXSONAR usuelles.
- Les fonctions de haut niveau retournent des dictionnaires prets a exploiter.

## References

- Digilent PMOD MAXSONAR (reference): https://digilent.com/reference/pmod/pmodmaxsonar/start
- MaxBotix LV-MaxSonar datasheet: https://maxbotix.com/pages/lv-maxsonar-ez-datasheet
