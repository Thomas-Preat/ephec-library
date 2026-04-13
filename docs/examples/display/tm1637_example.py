from time import sleep_us
import tm1637 as tm1637
from machine import Pin


p_out_num_disp = tm1637.TM1637(clk=Pin(2,Pin.OUT), dio=Pin(3,Pin.OUT))



p_out_num_disp.numbers(12, 34, colon=True) # afficher 12:34
sleep_us(1000000) # attendre 1 seconde
p_out_num_disp.show("Heya")


