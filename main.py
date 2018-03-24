# main.py -- put your code here!
from change_colour import print_to_display
import pyb
sw = pyb.Switch()
import lcd160cr
lcd = lcd160cr.LCD160CR('X')
uart = pyb.UART('XA', 115200)
pyb.repl_uart(uart)
#sw.callback(hdc_temp)

#usr_pressed = False
def usr_pressed_check():
    global usr_pressed
    usr_pressed = True

#sw.callback(usr_pressed_check)

while True: 
    print_to_display()
    pyb.delay(1000)
    #if usr_pressed:
        #read_sensors()
        #usr_pressed = False
    #if lcd.is_touched():
        #read_sensors()