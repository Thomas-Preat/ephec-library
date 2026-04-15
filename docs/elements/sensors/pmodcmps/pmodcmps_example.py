from machine import Pin, I2C
from time import sleep
from pmodcmps import PmodCMPS

# ============================================================
# I2C PIN CONFIGURATION (edit only this block when rewiring)
# ============================================================
I2C_BUS = 0          # 0 or 1
I2C_SDA_PIN = 0      # e.g. 0 for GP0
I2C_SCL_PIN = 1      # e.g. 1 for GP1
I2C_FREQ = 10000     # Start low; increase later only if stable
DECLINATION_DEG = 0.0  # Set your local magnetic declination if desired
# ============================================================


def main():
    i2c = I2C(
        I2C_BUS,
        sda=Pin(I2C_SDA_PIN),
        scl=Pin(I2C_SCL_PIN),
        freq=I2C_FREQ,
    )

    devices = i2c.scan()
    print("I2C scan:", devices)
    if 0x1E not in devices:
        print("PmodCMPS (0x1E) not found.")
        print("Check SDA/SCL pins, wiring, power, and I2C bus number.")
        return

    # Some boards need a short settling delay after bus init/scan.
    sleep(0.05)

    cmps = PmodCMPS(i2c, declination_deg=DECLINATION_DEG)
    print("PmodCMPS detected, ID:", cmps.identify())

    while True:
        x, y, z = cmps.read_raw()
        heading = cmps.heading()
        print("raw x=%d y=%d z=%d | heading=%.2f deg" % (x, y, z, heading))
        sleep(0.5)


main()
