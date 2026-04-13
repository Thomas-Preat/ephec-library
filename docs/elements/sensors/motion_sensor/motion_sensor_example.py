import utime

from motion_sensor import PIRMotionSensor


sensor = PIRMotionSensor(pin=16)

print("PIR Motion Sensor demo started")
print("Waiting for motion on GPIO16. Press Ctrl+C to stop.")

last_state = sensor.read()
print("Initial state:", last_state)

try:
    while True:
        state = sensor.read()
        if state != last_state:
            if state == 1:
                print("Motion detected")
            else:
                print("No motion")
            last_state = state
        utime.sleep_ms(50)
except KeyboardInterrupt:
    print("Demo stopped")
