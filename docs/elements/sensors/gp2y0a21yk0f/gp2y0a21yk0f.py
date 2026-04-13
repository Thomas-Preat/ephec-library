"""
GP2Y0A21YK0F Sharp Infrared Distance Measuring Sensor Driver
for Raspberry Pi Pico

Sensor Specifications:
- Operating voltage: 5V
- Analog output voltage
- Measuring distance: 10-80 cm
- Output: Analog signal (higher voltage = closer distance)

Default Pico wiring:
- VCC: 5V
- GND: GND
- OUT (analog): GPIO 26 (ADC0)
"""

from machine import ADC, Pin
import utime
import math


class GP2Y0A21YK0F:
    """Driver for Sharp GP2Y0A21YK0F infrared distance sensor."""
    
    # Sensor calibration constants
    # These are typical values; calibrate for your specific sensor
    # Using the formula: distance = A / (voltage - B)
    # Or: distance = A * voltage^(-B)
    
    def __init__(self, adc_pin=26, voltage_ref=3.3, bit_resolution=12):
        """
        Initialize the distance sensor.
        
        Args:
            adc_pin: ADC pin number (GPIO 26 for ADC0)
            voltage_ref: Pico ADC reference voltage (3.3V)
            bit_resolution: ADC bit resolution (12-bit = 4096 steps)
        """
        self.adc = ADC(Pin(adc_pin))
        self.voltage_ref = voltage_ref
        self.bit_resolution = bit_resolution
        self.max_adc_value = (1 << bit_resolution) - 1  # 4095 for 12-bit
        
        # Calibration coefficients (can be adjusted)
        # Formula: distance_cm = A / (voltage_v - B)
        self.a_coeff = 27.86  # Numerator coefficient
        self.b_coeff = 0.42   # Voltage offset
        
    def read_raw(self):
        """
        Read raw ADC value.
        
        Returns:
            Raw ADC value (0-4095 for 12-bit)
        """
        return self.adc.read_u16() >> 4  # Convert 16-bit to 12-bit
        
    def read_voltage(self):
        """
        Read voltage from the sensor.
        
        Returns:
            Voltage in volts
        """
        raw_value = self.read_raw()
        voltage = (raw_value / self.max_adc_value) * self.voltage_ref
        return voltage
        
    def read_distance(self):
        """
        Read distance from the sensor using the standard formula.
        Formula: distance_cm = A / (V - B)
        
        Returns:
            Distance in centimeters (or None if out of range)
        """
        voltage = self.read_voltage()
        
        # Clamp voltage to valid range
        if voltage < self.b_coeff + 0.1:
            return None  # Out of range (too close or no signal)
            
        distance = self.a_coeff / (voltage - self.b_coeff)
        
        # Valid range is typically 10-80 cm
        if distance < 8 or distance > 100:
            return None  # Out of reliable range
            
        return distance
        
    def read_distance_raw(self):
        """
        Read distance without range checking.
        Useful for debugging and calibration.
        
        Returns:
            Distance in centimeters
        """
        voltage = self.read_voltage()
        if voltage <= self.b_coeff:
            return 0
        return self.a_coeff / (voltage - self.b_coeff)
        
    def read_distance_smooth(self, samples=10, delay_ms=5):
        """
        Read distance with noise filtering using averaging.
        
        Args:
            samples: Number of samples to average
            delay_ms: Delay between samples in milliseconds
            
        Returns:
            Averaged distance in centimeters (or None if out of range)
        """
        distances = []
        
        for _ in range(samples):
            distance = self.read_distance_raw()
            if distance is not None:
                distances.append(distance)
            utime.sleep_ms(delay_ms)
        
        if not distances:
            return None
            
        avg_distance = sum(distances) / len(distances)
        
        # Check if in valid range
        if avg_distance < 8 or avg_distance > 100:
            return None
            
        return avg_distance
        
    def calibrate(self, known_distance_cm, samples=20):
        """
        Calibrate the sensor using a known distance.
        Measures average voltage at known distance and updates coefficients.
        
        Args:
            known_distance_cm: Known distance in centimeters
            samples: Number of measurements to average
        """
        voltages = []
        
        print(f"Measuring voltage at {known_distance_cm} cm...")
        utime.sleep(1)
        
        for i in range(samples):
            voltage = self.read_voltage()
            voltages.append(voltage)
            print(f"  Sample {i+1}/{samples}: {voltage:.3f}V")
            utime.sleep_ms(50)
        
        avg_voltage = sum(voltages) / len(voltages)
        print(f"Average voltage: {avg_voltage:.3f}V")
        
        # Update A coefficient: A = distance * (V - B)
        self.a_coeff = known_distance_cm * (avg_voltage - self.b_coeff)
        print(f"Updated A coefficient: {self.a_coeff:.2f}")
        
    def set_calibration(self, a_coeff, b_coeff):
        """
        Manually set calibration coefficients.
        
        Args:
            a_coeff: Numerator coefficient
            b_coeff: Voltage offset coefficient
        """
        self.a_coeff = a_coeff
        self.b_coeff = b_coeff
        print(f"Calibration set: A={a_coeff:.2f}, B={b_coeff:.3f}")
        
    def get_calibration(self):
        """
        Get current calibration coefficients.
        
        Returns:
            Tuple of (a_coeff, b_coeff)
        """
        return (self.a_coeff, self.b_coeff)
        
    def test(self, duration_seconds=10):
        """
        Run a sensor test, printing readings for specified duration.
        
        Args:
            duration_seconds: Duration of test in seconds
        """
        print(f"Starting {duration_seconds}s sensor test...")
        print("Raw ADC | Voltage (V) | Distance (cm)")
        print("-" * 40)
        
        start_time = utime.time()
        while utime.time() - start_time < duration_seconds:
            raw = self.read_raw()
            voltage = self.read_voltage()
            distance = self.read_distance_raw()
            
            print(f"{raw:4d}   | {voltage:.3f}      | {distance:6.2f}")
            utime.sleep_ms(200)
            
        print("Test complete.")


# Example usage
if __name__ == "__main__":
    # Initialize sensor
    sensor = GP2Y0A21YK0F(adc_pin=27)
    
    # Optional: Calibrate with a known distance (uncomment to use)
    # sensor.calibrate(known_distance_cm=20)
    
    # Run test
    sensor.test(duration_seconds=10)
