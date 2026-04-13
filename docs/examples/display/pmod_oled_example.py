import utime
from pmod_oled import PmodOLED


# Initialize OLED with default pins
# CS=5, MOSI=3, SCLK=2, DC=6, RES=7, VBATC=8, VDCC=9
oled = PmodOLED()

print("Pmod OLED example")
print("Displaying various text and graphics...")

# Display static text
oled.fill(0)
oled.text("Pmod OLED", 0, 0, 1)
oled.text("SSD1306 SPI", 0, 10, 1)
oled.text("128x32 pixels", 0, 20, 1)
oled.show()
utime.sleep(2)

# Display with rectangles
oled.fill(0)
oled.rect(0, 0, 128, 32, 1)  # Border
oled.text("Graphics Demo", 10, 5, 1)
oled.rect(10, 15, 50, 12, 1)
oled.show()
utime.sleep(2)

# Scrolling text animation
oled.fill(0)
for x in range(128):
    oled.fill(0)
    oled.text("Scroll", x - 30, 12, 1)
    oled.show()
    utime.sleep_ms(20)

# Bouncing box animation
oled.fill(0)
x, y = 0, 0
dx, dy = 1, 1

for _ in range(200):
    oled.fill(0)
    oled.rect(x, y, 20, 20, 1)
    oled.text("Box", 50, 12, 1)
    oled.show()
    
    x += dx
    y += dy
    
    if x <= 0 or x >= 108:
        dx *= -1
    if y <= 0 or y >= 12:
        dy *= -1
    
    utime.sleep_ms(30)

# Pixel art / pattern test
oled.fill(0)
for row in range(0, 32, 4):
    for col in range(0, 128, 4):
        oled.pixel(col, row, 1)

oled.text("Pattern", 40, 0, 1)
oled.show()
utime.sleep(2)

# Frame rate test - continuous loop
print("Running continuous animation. Press Ctrl+C to stop.")
frame_count = 0
start_time = utime.time()

try:
    while True:
        oled.fill(0)
        oled.text("Frame Count:", 0, 0, 1)
        oled.text(str(frame_count), 0, 10, 1)
        
        elapsed = utime.time() - start_time
        if elapsed > 0:
            fps = frame_count / elapsed
            oled.text("FPS: {:.0f}".format(fps), 0, 20, 1)
        
        oled.show()
        frame_count += 1
        
except KeyboardInterrupt:
    print("Animation stopped.")
    oled.fill(0)
    oled.text("Stopped", 30, 12, 1)
    oled.show()
