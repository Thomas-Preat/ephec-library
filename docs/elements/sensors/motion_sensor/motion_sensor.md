# Motion Sensor

This module wraps a PIR motion sensor such as the HC-SR501 and exposes a small API for checking whether movement has been detected.

## What it does

- Configures the chosen GPIO pin as a digital input.
- Provides a `motion()` helper that returns `True` when movement is detected.
- Exposes `read()` if you need the raw `0` or `1` pin state.
- Includes `wait_for_motion()` for blocking flows where your program should pause until movement is seen.

## Typical use

Use this module when you want to trigger an action only when a person or object moves in front of the sensor.

## Notes

- PIR sensors usually need a short warm-up time after power-on.
- The exact output behavior depends on your sensor module settings.
- The default pin in this file is GPIO 16.
