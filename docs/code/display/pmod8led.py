from machine import Pin


class Pmod8LED:
    """
    MicroPython driver for Digilent Pmod8LD (8 LEDs).

    Provide exactly 8 GPIO pin numbers wired to LD0..LD7 in order.
    Example: [0, 1, 2, 3, 4, 5, 6, 7]
    """

    def __init__(self, led_pins, active_high=True):
        if len(led_pins) != 8:
            raise ValueError("led_pins must contain exactly 8 GPIO pin numbers")

        self.active_high = active_high
        self._pins = [Pin(pin_num, Pin.OUT) for pin_num in led_pins]
        self.clear()

    def _to_level(self, on):
        if self.active_high:
            return 1 if on else 0
        return 0 if on else 1

    def clear(self):
        """Turn all LEDs off."""
        off_level = self._to_level(False)
        for pin in self._pins:
            pin.value(off_level)

    def fill(self, on=True):
        """Turn all LEDs on or off."""
        level = self._to_level(on)
        for pin in self._pins:
            pin.value(level)

    def set_led(self, index, on=True):
        """Set one LED by index (0..7)."""
        if not 0 <= index <= 7:
            raise ValueError("index must be in range 0..7")
        self._pins[index].value(self._to_level(on))

    def toggle_led(self, index):
        """Toggle one LED by index (0..7)."""
        if not 0 <= index <= 7:
            raise ValueError("index must be in range 0..7")
        self._pins[index].value(0 if self._pins[index].value() else 1)

    def write_byte(self, value):
        """
        Write an 8-bit value to LEDs.
        Bit 0 -> LED0, ..., Bit 7 -> LED7.
        """
        value &= 0xFF
        for i in range(8):
            bit = (value >> i) & 0x01
            self._pins[i].value(self._to_level(bit == 1))

    def chase(self, delay_s=0.1, cycles=1):
        """Run a one-hot chase pattern across LEDs."""
        from time import sleep

        for _ in range(cycles):
            for i in range(8):
                self.clear()
                self.set_led(i, True)
                sleep(delay_s)
