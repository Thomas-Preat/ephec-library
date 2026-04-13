from time import sleep
from pmod8led import Pmod8LED

# ============================================================
# LED PIN CONFIGURATION (edit only this block when rewiring)
# ============================================================
# LD0..LD7 wiring order must match this list left-to-right.
LED_PINS = [0, 1, 2, 3, 4, 5, 6, 7]
ACTIVE_HIGH = True
# ============================================================


def main():
    led = Pmod8LED(LED_PINS, active_high=ACTIVE_HIGH)

    print("Pmod8LED demo starting")
    print("LED_PINS:", LED_PINS)

    # Fill up pattern
    for value in (0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3F, 0x7F, 0xFF):
        led.write_byte(value)
        sleep(0.2)

    sleep(0.3)
    led.clear()
    sleep(0.3)

    # Continuous chase
    while True:
        led.chase(delay_s=0.08, cycles=1)


main()
