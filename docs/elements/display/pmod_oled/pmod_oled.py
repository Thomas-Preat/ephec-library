"""
Pmod OLED (SSD1306) driver for Raspberry Pi Pico / Pico W.

This module targets the Digilent-style Pmod OLED over SPI and provides a
simple framebuffer API for text and graphics.

Pmod OLED connector pinout:
  Pin 1  CS    -> GPIO 5
  Pin 2  MOSI  -> GPIO 3
  Pin 3  NC
  Pin 4  SCLK  -> GPIO 2
  Pin 5  GND   -> GND
  Pin 6  VCC   -> 3.3V
  Pin 7  D/C   -> GPIO 6
  Pin 8  RES   -> GPIO 7
  Pin 9  VBATC -> GPIO 8
  Pin 10 VDCC  -> GPIO 9
  Pin 11 GND   -> GND
  Pin 12 VCC   -> 3.3V
"""

from machine import Pin, SPI
import framebuf
import utime


class PmodOLED(framebuf.FrameBuffer):
    """SSD1306-based Pmod OLED over SPI."""

    def __init__(
        self,
        width=128,
        height=32,
        spi_id=0,
        baudrate=10_000_000,
        sck=2,
        mosi=3,
        cs=5,
        dc=6,
        rst=7,
        vbat=8,
        vdcc=9,
    ):
        self.width = width
        self.height = height
        self.pages = self.height // 8

        self.cs = Pin(cs, Pin.OUT, value=1)
        self.dc = Pin(dc, Pin.OUT, value=0)
        self.rst = Pin(rst, Pin.OUT, value=1)

        self.vbat = Pin(vbat, Pin.OUT, value=1)
        self.vdcc = Pin(vdcc, Pin.OUT, value=1)

        self.spi = SPI(
            spi_id,
            baudrate=baudrate,
            polarity=0,
            phase=0,
            sck=Pin(sck),
            mosi=Pin(mosi),
            miso=Pin(4),  # Not used by OLED, required by SPI constructor on some builds.
        )

        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)

        self._init_display()

    def _write_cmd(self, cmd):
        self.cs.value(1)
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray((cmd,)))
        self.cs.value(1)

    def _write_data(self, data):
        self.cs.value(1)
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

    def _hw_reset(self):
        self.rst.value(1)
        utime.sleep_ms(1)
        self.rst.value(0)
        utime.sleep_ms(10)
        self.rst.value(1)

    def _init_display(self):
        self.vdcc.value(1)
        self.vbat.value(1)

        self._hw_reset()

        init_sequence = (
            0xAE,  # display off
            0xD5, 0x80,  # clock divide
            0xA8, self.height - 1,  # multiplex
            0xD3, 0x00,  # display offset
            0x40,  # start line
            0x8D, 0x14,  # charge pump on
            0x20, 0x00,  # horizontal addressing mode
            0xA1,  # segment remap
            0xC8,  # COM scan direction remapped
            0xDA, 0x02 if self.height == 32 else 0x12,  # COM pins
            0x81, 0x8F,  # contrast
            0xD9, 0xF1,  # pre-charge
            0xDB, 0x40,  # VCOM deselect
            0xA4,  # resume to RAM content display
            0xA6,  # normal display
            0xAF,  # display on
        )

        for cmd in init_sequence:
            self._write_cmd(cmd)

        self.fill(0)
        self.show()

    def show(self):
        self._write_cmd(0x21)  # column addr
        self._write_cmd(0)
        self._write_cmd(self.width - 1)
        self._write_cmd(0x22)  # page addr
        self._write_cmd(0)
        self._write_cmd(self.pages - 1)
        self._write_data(self.buffer)

    def poweron(self):
        self._write_cmd(0xAF)

    def poweroff(self):
        self._write_cmd(0xAE)

    def contrast(self, value):
        self._write_cmd(0x81)
        self._write_cmd(value & 0xFF)

    def invert(self, invert_on=True):
        self._write_cmd(0xA7 if invert_on else 0xA6)

    def rotate_180(self, enabled=True):
        # Enabled: text appears rotated for flipped mounting.
        if enabled:
            self._write_cmd(0xA0)
            self._write_cmd(0xC0)
        else:
            self._write_cmd(0xA1)
            self._write_cmd(0xC8)
        self.show()

    def demo(): # type: ignore
        oled = PmodOLED()
        print("Pmod OLED initialized. Displaying demo text...")
        
        oled.fill(0)
        oled.text("Pmod OLED", 0, 0, 1)
        oled.text("on Pico", 0, 12, 1)
        oled.show()
        utime.sleep(2)

        x = 0
        direction = 1
        while True:
            oled.fill(0)
            oled.text("Hello", x, 0, 1)
            oled.rect(0, 18, 128, 14, 1)
            oled.text("SSD1306 SPI", 8, 21, 1)
            oled.show()

            x += direction
            if x <= 0 or x >= 88:
                direction *= -1

            utime.sleep_ms(40)