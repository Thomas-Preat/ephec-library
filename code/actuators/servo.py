from machine import Pin, PWM
import time

class ServoMotor:
    def __init__(self, pin_number, min_pulse=600, max_pulse=2400, frequency=50):
        self.pwm = PWM(Pin(pin_number))
        self.pwm.freq(frequency)
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.angle = 0
    
    def set_angle(self, angle):
        if angle < -90:
            angle = -90
        elif angle > 90:
            angle = 90
        
        pulse_width = self._map(angle, -90, 90, self.min_pulse, self.max_pulse)
        self.pwm.duty_u16(int(pulse_width * 65535 / 20000))
        self.angle = angle
    
    def get_angle(self):
        return self.angle
    
    def calibrate(self, min_pulse, max_pulse):
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
    
    def sweep(self, start=-90, end=90, step=5, delay=0.05):
        for angle in range(start, end + step, step):
            self.set_angle(angle)
            time.sleep(delay)
        for angle in range(end, start - step, -step):
            self.set_angle(angle)
            time.sleep(delay)
    
    def detach(self):
        self.pwm.deinit()
    
    def _map(self, value, from_low, from_high, to_low, to_high):
        return to_low + (to_high - to_low) * (value - from_low) / (from_high - from_low)
    
test_servo = ServoMotor(pin_number=15)
test_servo.sweep(start=-45, end=45, step=15, delay=0.1)
test_servo.sweep(start=-45, end=45, step=15, delay=0.1)
test_servo.sweep(start=-45, end=45, step=15, delay=0.1)
print(test_servo.get_angle())