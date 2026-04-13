import utime
import gp2y0a21yk0f as gp2y0a21yk0f


# Change adc_pin if your sensor output is connected to a different ADC pin.
sensor = gp2y0a21yk0f.GP2Y0A21YK0F(adc_pin=27)

print("GP2Y0A21YK0F distance sensor example")
print("Press Ctrl+C to stop.")

while True:
    voltage = sensor.read_voltage()
    distance = sensor.read_distance_smooth(samples=5, delay_ms=10)

    if distance is None:
        print("Voltage: {:.3f} V | Distance: out of range".format(voltage))
    else:
        print("Voltage: {:.3f} V | Distance: {:.1f} cm".format(voltage, distance))

    utime.sleep_ms(500)