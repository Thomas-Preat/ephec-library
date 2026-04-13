# MAXSONAR

This module provides a helper around a PMOD MAXSONAR distance sensor and supports multiple reading methods.

## What it does

- Reads the PWM output and converts pulse width into distance.
- Reads the analog output and estimates distance from the ADC value.
- Reads UART packets when the sensor is connected over serial.
- Returns structured dictionaries so the sensor state can be reused in other programs.

## Typical use

Use this module when you want distance measurements for obstacle detection, range feedback, or simple robotics projects.

## Notes

- The file defines default pins for PWM, analog, and UART wiring.
- PWM and analog conversions use common MAXSONAR scaling assumptions.
- The helper methods return both raw values and converted distances.
