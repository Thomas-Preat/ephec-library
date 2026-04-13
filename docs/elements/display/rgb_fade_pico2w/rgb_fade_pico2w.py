from machine import Pin, PWM
import time


# Set your RGB LED pins here (change as needed).
PIN_R = 16
PIN_G = 17
PIN_B = 18

# True for common-anode RGB LED, False for common-cathode.
COMMON_ANODE = True

# Fade timing (smaller = faster animation).
STEP_DELAY_MS = 8


class RGBLed:
    def __init__(self, pin_r, pin_g, pin_b, common_anode=False, pwm_freq=1000):
        self.common_anode = common_anode

        self.r = PWM(Pin(pin_r, Pin.OUT))
        self.g = PWM(Pin(pin_g, Pin.OUT))
        self.b = PWM(Pin(pin_b, Pin.OUT))

        self.r.freq(pwm_freq)
        self.g.freq(pwm_freq)
        self.b.freq(pwm_freq)

        self.set_rgb(0, 0, 0)

    def _apply_channel(self, pwm, value):
        # value expected in range 0..255
        duty = int((max(0, min(255, value)) * 65535) / 255)
        if self.common_anode:
            duty = 65535 - duty
        pwm.duty_u16(duty)

    def set_rgb(self, red, green, blue):
        self._apply_channel(self.r, red)
        self._apply_channel(self.g, green)
        self._apply_channel(self.b, blue)

    def deinit(self):
        self.r.deinit()
        self.g.deinit()
        self.b.deinit()


def wheel(pos):
    # Convert position 0..255 to smooth RGB transition.
    pos = pos % 256
    if pos < 85:
        return 255 - pos * 3, pos * 3, 0
    if pos < 170:
        pos -= 85
        return 0, 255 - pos * 3, pos * 3
    pos -= 170
    return pos * 3, 0, 255 - pos * 3


def main():
    led = RGBLed(PIN_R, PIN_G, PIN_B, common_anode=COMMON_ANODE)
    try:
        while True:
            for i in range(256):
                r, g, b = wheel(i)
                led.set_rgb(r, g, b)
                time.sleep_ms(STEP_DELAY_MS)
    except KeyboardInterrupt:
        pass
    finally:
        led.set_rgb(0, 0, 0)
        led.deinit()


if __name__ == "__main__":
    main()
