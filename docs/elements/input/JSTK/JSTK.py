from machine import Pin, SPI
import time


# Default wiring for Pico SPI0 (change if your PMOD is wired differently).
SPI_ID = 0
PIN_SCK = 18
PIN_MOSI = 19
PIN_MISO = 16
PIN_CS = 17


class PmodJSTK:
	def __init__(self, spi_id=SPI_ID, sck=PIN_SCK, mosi=PIN_MOSI, miso=PIN_MISO, cs=PIN_CS):
		self.cs = Pin(cs, Pin.OUT)
		self.cs.value(1)
		self.spi = SPI(
			spi_id,
			baudrate=500_000,
			polarity=0,
			phase=0,
			sck=Pin(sck),
			mosi=Pin(mosi),
			miso=Pin(miso),
		)
		self._led_state = 0
		self._tx = bytearray(5)
		self._rx = bytearray(5)
		self._tx1 = bytearray(1)
		self._rx1 = bytearray(1)

	def read(self):
		# Digilent protocol: first byte is a command (0x80 | led_state).
		self._tx[0] = 0x80 | (self._led_state & 0x03)
		self._tx[1] = 0
		self._tx[2] = 0
		self._tx[3] = 0
		self._tx[4] = 0

		self.cs.value(0)
		time.sleep_us(5)
		for i in range(5):
			# Per-byte transfer with a short delay matches the official driver.
			time.sleep_us(10)
			self._tx1[0] = self._tx[i]
			self.spi.write_readinto(self._tx1, self._rx1)
			self._rx[i] = self._rx1[0]
		time.sleep_us(5)
		self.cs.value(1)
		raw = self._rx

		x = ((raw[1] << 8) | raw[0]) & 0x03FF
		y = ((raw[3] << 8) | raw[2]) & 0x03FF
		status = raw[4]

		# PmodJSTK button bits are active-high in the Digilent reference driver.
		joy_pressed = (status & 0x01) != 0
		btn1_pressed = (status & 0x02) != 0
		btn2_pressed = (status & 0x04) != 0

		return x, y, joy_pressed, btn1_pressed, btn2_pressed, status, bytes(raw)


def _axis_percent(value):
	# 10-bit joystick axis expected in range 0..1023, center around 512.
	pct = int(((value - 512) * 100) / 511)
	if pct < -100:
		return -100
	if pct > 100:
		return 100
	return pct


def _axis_direction(pct):
	if pct > 15:
		return "POS"
	if pct < -15:
		return "NEG"
	return "CTR"


def _signed_bar(pct, half_width=12):
	if pct >= 0:
		right_count = (pct * half_width) // 100
		left = "." * half_width
		right = ("#" * right_count) + ("." * (half_width - right_count))
	else:
		left_count = ((-pct) * half_width) // 100
		left = ("." * (half_width - left_count)) + ("#" * left_count)
		right = "." * half_width
	return "[{}|{}]".format(left, right)


def _button_lamp(pressed):
	return "[ON ]" if pressed else "[off]"


def get_joystick_state(jstk):
	"""Return joystick position and button states in a reusable structure."""
	x, y, joy_pressed, btn1_pressed, btn2_pressed, status, raw = jstk.read()
	return {
		"x": x,
		"y": y,
		"joy": joy_pressed,
		"btn1": btn1_pressed,
		"btn2": btn2_pressed,
		"status": status,
		"raw": raw,
	}


def show_dashboard(jstk, refresh_s=0.08):
	"""Render a live console dashboard from joystick state."""
	print("\x1b[2J\x1b[H", end="")
	print("PMOD JSTK live dashboard")
	print("Ctrl+C to stop")
	time.sleep(0.7)

	while True:
		state = get_joystick_state(jstk)

		x = state["x"]
		y = state["y"]
		x_pct = _axis_percent(x)
		y_pct = _axis_percent(y)

		x_bar = _signed_bar(x_pct)
		y_bar = _signed_bar(y_pct)

		print("\x1b[H", end="")
		print("+---------------------------------------------+")
		print("|            PMOD JSTK DASHBOARD              |")
		print("+---------------------------------------------+")
		print("| X: {:4d} {:>4}% {} {:>3}           |".format(x, x_pct, x_bar, _axis_direction(x_pct)))
		print("| Y: {:4d} {:>4}% {} {:>3}           |".format(y, y_pct, y_bar, _axis_direction(y_pct)))
		print("|                                             |")
		print("| Buttons: Joy {}  Btn1 {}  Btn2 {}      |".format(
			_button_lamp(state["joy"]),
			_button_lamp(state["btn1"]),
			_button_lamp(state["btn2"]),
		))
		print("| Status: 0b{:08b}  Raw: {:3d},{:3d},{:3d},{:3d},{:3d} |".format(
			state["status"],
			state["raw"][0], state["raw"][1], state["raw"][2], state["raw"][3], state["raw"][4],
		))
		print("+---------------------------------------------+")

		time.sleep(refresh_s)


def main():
	jstk = PmodJSTK()
    
	try:
		show_dashboard(jstk)
	except KeyboardInterrupt:
		print("\nStopped.")


if __name__ == "__main__":
	main()
