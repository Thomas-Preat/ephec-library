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

- Lecture de la sortie PWM (`read_pulse_us`).
- Lecture analogique (`read_analog_raw`, `read_analog_volts`).
- Lecture UART (`read_uart_packet`, `read_uart_inches`).
- Fonctions de haut niveau: `get_pwm_state`, `get_analog_state`, `get_uart_state`.

## Remarques

- Les conversions en distance reposent sur des echelles MAXSONAR usuelles.
- Les fonctions de haut niveau retournent des dictionnaires prets a exploiter.

## References

- Digilent PMOD MAXSONAR (reference): https://digilent.com/reference/pmod/pmodmaxsonar/start
- MaxBotix LV-MaxSonar datasheet: https://maxbotix.com/pages/lv-maxsonar-ez-datasheet
