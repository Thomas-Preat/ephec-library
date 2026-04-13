# PMOD JSTK

This module communicates with a Digilent PMOD JSTK joystick over SPI and exposes both axis and button state.

## What it does

- Sets up the SPI bus and chip-select pin.
- Reads X and Y joystick positions.
- Reads the joystick push button plus the two extra buttons.
- Provides helper functions to convert axis values into percentages and simple dashboard output.

## Typical use

Use this module when you want directional input or button control for menus, robot control, or interactive demos.

## Notes

- The module assumes a Pico SPI0 wiring layout by default.
- `get_joystick_state()` returns a reusable dictionary.
- `show_dashboard()` prints a live terminal view until interrupted.
