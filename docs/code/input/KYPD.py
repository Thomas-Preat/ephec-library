from machine import Pin
import time

# Définir les pins pour lignes et colonnes
rows = [Pin(i, Pin.OUT) for i in (2, 3, 4, 5)]
cols = [Pin(i, Pin.IN, Pin.PULL_UP) for i in (9, 8, 7, 6)]

keys = [
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['0','F','E','D']
]

def scan_keypad():
    for row_idx, row_pin in enumerate(rows):
        row_pin.low()
        for col_idx, col_pin in enumerate(cols):
            if col_pin.value() == 0:
                row_pin.high()
                return keys[row_idx][col_idx]
        row_pin.high()
    return None

while True:
    key = scan_keypad()
    if key:
        print("Touche appuyée:", key)
        time.sleep(0.3)