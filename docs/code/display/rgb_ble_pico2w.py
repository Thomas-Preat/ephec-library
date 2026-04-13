from machine import Pin, PWM
import bluetooth
import struct
import time

from micropython import const


# RGB LED pins (change if needed).
PIN_R = 16
PIN_G = 17
PIN_B = 18

# Set True for common-anode LEDs.
COMMON_ANODE = True


_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID128_COMPLETE = const(0x07)

_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)


def _mac_to_str(mac_bytes):
    return ":".join("{:02X}".format(b) for b in mac_bytes)


def _advertising_payload(name=None, services=None):
    payload = bytearray()

    def _append(adv_type, value):
        payload.extend(struct.pack("BB", len(value) + 1, adv_type))
        payload.extend(value)

    _append(_ADV_TYPE_FLAGS, struct.pack("B", 0x06))

    if name:
        _append(_ADV_TYPE_NAME, name.encode())

    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, b)

    return payload


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


class BLERGBController:
    # Custom service UUIDs.
    _SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
    _COLOR_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

    _SERVICE = (
        _SERVICE_UUID,
        (
            (_COLOR_CHAR_UUID, _FLAG_READ | _FLAG_WRITE | _FLAG_NOTIFY),
        ),
    )

    def __init__(self, ble, led, name="Pico2W-RGB"):
        self._ble = ble
        self._led = led
        self._connections = set()

        self._ble.active(True)
        self._ble.irq(self._irq)

        ((self._color_handle,),) = self._ble.gatts_register_services((self._SERVICE,))
        self._ble.gatts_write(self._color_handle, b"0,0,0")

        self._payload = _advertising_payload(
            name=name,
            services=[self._SERVICE_UUID],
        )
        self._advertise()

    def _advertise(self):
        # 200 ms advertising interval.
        self._ble.gap_advertise(200_000, adv_data=self._payload)
        print("Advertising as BLE device")

    def _notify(self, msg):
        b = msg.encode()
        self._ble.gatts_write(self._color_handle, b)
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._color_handle, b)

    def _parse_color(self, text):
        t = text.strip().upper()

        if t == "OFF":
            return 0, 0, 0

        if t.startswith("#") and len(t) == 7:
            r = int(t[1:3], 16)
            g = int(t[3:5], 16)
            b = int(t[5:7], 16)
            return r, g, b

        parts = t.split(",")
        if len(parts) == 3:
            r = int(parts[0])
            g = int(parts[1])
            b = int(parts[2])
            return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))

        raise ValueError("Use OFF, #RRGGBB, or R,G,B")

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("BLE connected")

        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            print("BLE disconnected")
            self._advertise()

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if value_handle != self._color_handle:
                return

            raw = self._ble.gatts_read(self._color_handle)
            try:
                text = raw.decode().strip()
                r, g, b = self._parse_color(text)
                self._led.set_rgb(r, g, b)
                self._notify("OK {},{},{}".format(r, g, b))
                print("Set color:", r, g, b)
            except Exception as exc:
                self._notify("ERR {}".format(exc))


def main():
    led = RGBLed(PIN_R, PIN_G, PIN_B, common_anode=COMMON_ANODE)
    ble = bluetooth.BLE()
    ble.active(True)

    try:
        mac_info = ble.config("mac")
        if isinstance(mac_info, tuple) and len(mac_info) == 2:
            addr_type, mac = mac_info
            print("BLE MAC:", _mac_to_str(mac), "type:", addr_type)
        else:
            print("BLE MAC:", _mac_to_str(mac_info))
    except Exception as exc:
        print("Could not read BLE MAC:", exc)

    BLERGBController(ble, led)

    print("Connect with nRF Connect / LightBlue")
    print("Write OFF, #RRGGBB, or R,G,B (example: 255,0,120)")

    try:
        while True:
            time.sleep_ms(200)
    except KeyboardInterrupt:
        pass
    finally:
        led.set_rgb(0, 0, 0)
        led.deinit()
        ble.active(False)


if __name__ == "__main__":
    main()
