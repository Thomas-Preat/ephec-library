from machine import Pin
import dht
import time


class DHT11Sensor:
    def __init__(self, pin=16):
        self.pin = pin
        self.sensor = dht.DHT11(Pin(pin))
        self._last_temp_c = None
        self._last_humidity = None
        self._last_read_ms = None

    def measure(self, retries=3, retry_delay_ms=250):
        """Trigger a new measurement with optional retries."""
        retries = max(1, int(retries))

        for attempt in range(retries):
            try:
                self.sensor.measure()
                self._last_temp_c = self.sensor.temperature()
                self._last_humidity = self.sensor.humidity()
                self._last_read_ms = time.ticks_ms()
                return True
            except Exception:
                if attempt == retries - 1:
                    return False
                time.sleep_ms(retry_delay_ms)

        return False

    def read(self, retries=3):
        """Return a structured reading dictionary."""
        ok = self.measure(retries=retries)
        if not ok:
            return {
                "valid": False,
                "temperature_c": None,
                "humidity_percent": None,
                "error": "measure_failed",
            }

        return {
            "valid": True,
            "temperature_c": self._last_temp_c,
            "humidity_percent": self._last_humidity,
            "error": None,
        }

    def temperature_c(self):
        """Return last temperature in Celsius."""
        return self._last_temp_c

    def humidity_percent(self):
        """Return last relative humidity in percent."""
        return self._last_humidity

    def comfort_state(self):
        """Return a simple comfort label based on latest values."""
        if self._last_temp_c is None or self._last_humidity is None:
            return "unknown"

        if 20 <= self._last_temp_c <= 26 and 35 <= self._last_humidity <= 60:
            return "comfortable"
        if self._last_humidity < 30:
            return "dry"
        if self._last_humidity > 70:
            return "humid"
        if self._last_temp_c < 18:
            return "cold"
        if self._last_temp_c > 28:
            return "hot"
        return "ok"
