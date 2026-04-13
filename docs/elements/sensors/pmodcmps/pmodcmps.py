"""
PmodCMPS (HMC5883L-compatible) MicroPython driver for Raspberry Pi Pico.

I2C default address: 0x1E
Provides heading in degrees and raw magnetometer readings.

Pin selection is done when creating your I2C object, for example:

    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

Change only those Pin numbers (and bus ID 0/1) to match your wiring.
"""

from machine import I2C
from math import atan2, pi


class PmodCMPS:
    # HMC5883L registers
    _REG_CONFIG_A = 0x00
    _REG_CONFIG_B = 0x01
    _REG_MODE = 0x02
    _REG_DATA_X_MSB = 0x03
    _REG_STATUS = 0x09
    _REG_ID_A = 0x0A

    # Gain to LSB/Gauss map (Configuration Register B)
    _GAIN_TABLE = {
        0x00: 1370,
        0x01: 1090,
        0x02: 820,
        0x03: 660,
        0x04: 440,
        0x05: 390,
        0x06: 330,
        0x07: 230,
    }

    def __init__(self, i2c: I2C, addr: int = 0x1E, declination_deg: float = 0.0):
        self.i2c = i2c
        self.addr = addr
        self.declination = declination_deg * (pi / 180.0)
        self._gain_cfg = 0x01  # default gain value

        if addr not in self.i2c.scan():
            raise OSError("PmodCMPS not found on I2C bus")

        self._configure()

    def _write_reg(self, reg: int, value: int) -> None:
        self.i2c.writeto_mem(self.addr, reg, bytes([value]))

    def _read_reg(self, reg: int, nbytes: int = 1) -> bytes:
        return self.i2c.readfrom_mem(self.addr, reg, nbytes)

    @staticmethod
    def _to_signed_16(msb: int, lsb: int) -> int:
        value = (msb << 8) | lsb
        if value & 0x8000:
            value -= 0x10000
        return value

    def _configure(self) -> None:
        # 8-average, 15 Hz default output rate, normal measurement
        self._write_reg(self._REG_CONFIG_A, 0x70)

        # Gain setting (default +/-1.3 Ga)
        self.set_gain(self._gain_cfg)

        # Continuous measurement mode
        self._write_reg(self._REG_MODE, 0x00)

    def set_gain(self, gain_cfg: int) -> None:
        """
        Set sensor gain configuration (0..7).
        1 is a good default for general use.
        """
        gain_cfg &= 0x07
        self._gain_cfg = gain_cfg
        self._write_reg(self._REG_CONFIG_B, gain_cfg << 5)

    def is_ready(self) -> bool:
        """Return True when a new sample is available."""
        status = self._read_reg(self._REG_STATUS, 1)[0]
        return bool(status & 0x01)

    def read_raw(self):
        """
        Read raw axis values as signed 16-bit integers.
        Returns (x, y, z).
        """
        data = self._read_reg(self._REG_DATA_X_MSB, 6)

        x = self._to_signed_16(data[0], data[1])
        z = self._to_signed_16(data[2], data[3])
        y = self._to_signed_16(data[4], data[5])

        return x, y, z

    def read_gauss(self):
        """
        Read axis values converted to Gauss.
        Returns (x_g, y_g, z_g).
        """
        x, y, z = self.read_raw()
        lsb_per_gauss = self._GAIN_TABLE.get(self._gain_cfg, 1090)
        return x / lsb_per_gauss, y / lsb_per_gauss, z / lsb_per_gauss

    def heading(self) -> float:
        """
        Compute 2D heading in degrees from X/Y axes.
        Adds magnetic declination and normalizes to [0, 360).
        """
        x, y, _ = self.read_raw()
        angle = atan2(y, x) + self.declination

        if angle < 0:
            angle += 2 * pi
        elif angle >= 2 * pi:
            angle -= 2 * pi

        return angle * (180.0 / pi)

    def identify(self):
        """
        Return the 3-byte identification string, usually b'H43'.
        """
        return self._read_reg(self._REG_ID_A, 3)
