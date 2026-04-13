from machine import Pin, ADC, UART, time_pulse_us
import time


# Change this pin to match where the PMOD MAXSONAR PWM output is connected.
PIN_PWM = 15
PIN_AN = 26
PIN_SENSOR_TX = 1   # Sensor TX -> Pico UART0 RX
PIN_SENSOR_RX = 0   # Pico UART0 TX -> Sensor RX


class PmodMaxSonar:
	def __init__(
		self,
		pwm_pin=PIN_PWM,
		an_pin=PIN_AN,
		uart_id=0,
		uart_baud=9600,
		sensor_tx_pin=PIN_SENSOR_TX,
		sensor_rx_pin=PIN_SENSOR_RX,
		timeout_us=60_000,
	):
		self.pwm = Pin(pwm_pin, Pin.IN)
		self.an = ADC(Pin(an_pin))
		self.sensor_rx = Pin(sensor_rx_pin, Pin.OUT)
		self.sensor_rx.value(1)
		self.uart = UART(
			uart_id,
			baudrate=uart_baud,
			bits=8,
			parity=None,
			stop=1,
			rx=Pin(sensor_tx_pin),
			tx=Pin(sensor_rx_pin),
		)
		self.timeout_us = timeout_us

	def read_pulse_us(self):
		# Most MaxSonar PWM outputs are high pulses proportional to distance.
		return time_pulse_us(self.pwm, 1, self.timeout_us)

	def read_analog_raw(self):
		# 16-bit scaled ADC value (0..65535).
		return self.an.read_u16()

	def read_analog_volts(self, vref=3.3):
		raw = self.read_analog_raw()
		return (raw / 65535.0) * vref

	def send_range_trigger(self):
		# Sensor RX low pulse (~20 us min) triggers a new measurement cycle.
		self.sensor_rx.value(0)
		time.sleep_us(30)
		self.sensor_rx.value(1)

	def read_uart_packet(self):
		# Typical packet is ASCII like b"R123\r" at 9600 baud.
		line = self.uart.readline()
		if not line:
			return None
		if isinstance(line, bytes):
			try:
				text = line.decode().strip()
			except Exception:
				return None
		else:
			text = str(line).strip()
		return text

	def read_uart_inches(self):
		packet = self.read_uart_packet()
		if not packet:
			return None, None
		if packet.startswith("R"):
			num = packet[1:]
			if num.isdigit():
				return int(num), packet
		return None, packet


def _pulse_to_inches(pulse_us):
	# MaxSonar PWM scale is commonly 147 us per inch.
	return pulse_us / 147.0


def _analog_to_inches(raw_u16):
	# Typical MaxSonar AN scaling: Vcc/1024 volts per inch.
	# With ADC scaled to 16-bit and same Vcc reference, inches ~= raw/64.
	return raw_u16 / 64.0


def get_pwm_state(sensor, max_cm=300.0):
	"""Read only the PWM output path."""
	sensor.send_range_trigger()
	time.sleep_ms(35)
	pulse_us = sensor.read_pulse_us()

	if pulse_us < 0:
		return {
			"valid": False,
			"error": pulse_us,
			"pulse_us": pulse_us,
			"inches": None,
			"cm": None,
			"percent": 0,
		}

	inches = _pulse_to_inches(pulse_us)
	cm = inches * 2.54
	percent = int((cm * 100) / max_cm) if max_cm > 0 else 0
	if percent < 0:
		percent = 0
	if percent > 100:
		percent = 100

	return {
		"valid": True,
		"error": 0,
		"pulse_us": pulse_us,
		"inches": inches,
		"cm": cm,
		"percent": percent,
	}


def get_analog_state(sensor, max_cm=300.0):
	"""Read only the analog output path."""
	raw = sensor.read_analog_raw()
	volts = sensor.read_analog_volts()
	inches = _analog_to_inches(raw)
	cm = inches * 2.54
	percent = int((cm * 100) / max_cm) if max_cm > 0 else 0
	if percent < 0:
		percent = 0
	if percent > 100:
		percent = 100

	return {
		"raw": raw,
		"volts": volts,
		"inches": inches,
		"cm": cm,
		"percent": percent,
	}


def get_uart_state(sensor):
	"""Read only the UART output path."""
	uart_inches, uart_packet = sensor.read_uart_inches()
	return {
		"valid": uart_inches is not None,
		"packet": uart_packet,
		"inches": uart_inches,
		"cm": (uart_inches * 2.54) if uart_inches is not None else None,
	}

sensor = PmodMaxSonar()  # Initialisation du capteur