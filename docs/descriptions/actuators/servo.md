# Servo Motor

This module drives a hobby servo with PWM and keeps the control API simple for student projects.

## What it does

- Configures a PWM output on the selected pin.
- Lets you set the servo angle between `-90` and `90` degrees.
- Supports pulse calibration through `calibrate()`.
- Includes a `sweep()` helper for quick movement tests.
- Allows the PWM output to be released with `detach()`.

## Typical use

Use this module when you need to point, rotate, or position a mechanical part with a servo motor.

## Notes

- The default PWM frequency is `50 Hz`, which is common for servos.
- Pulse width limits may need adjustment depending on the servo model.
- The example code at the bottom of the module immediately sweeps a test servo.
