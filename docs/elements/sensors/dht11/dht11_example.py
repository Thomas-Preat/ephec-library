from time import sleep
from dht11 import DHT11Sensor


# Example wiring: DATA -> GP16
sensor = DHT11Sensor(pin=16)

while True:
    state = sensor.read(retries=3)

    if state["valid"]:
        temp = state["temperature_c"]
        hum = state["humidity_percent"]
        comfort = sensor.comfort_state()
        print("T={}C  H={}%%  state={}".format(temp, hum, comfort))
    else:
        print("DHT11 read failed")

    # DHT11 refresh rate is low; avoid fast polling.
    sleep(2)
