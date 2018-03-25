# main.py -- put your code here!
import pyb
import utime
import lcd160cr
from change_colour import hdc_temp, hdc_hum, print_to_display
from write_log import writeLog

lcd = lcd160cr.LCD160CR('X')
uart = pyb.UART('XA', 115200)
pyb.repl_uart(uart)
#sw = pyb.Switch()
rtc = pyb.RTC()

def usr_pressed_check():
    global usr_pressed
    usr_pressed = True

#sw.callback(usr_pressed_check)

while True:
    current_temp = hdc_temp()
    current_hum = hdc_hum()
    print_to_display(current_temp, current_hum)
    while True:
        new_temp = hdc_temp()
        new_hum = hdc_hum()
        if new_temp > current_temp+1 or new_temp < current_temp-1:
            current_temp = new_temp
            current_hum = new_hum
            print_to_display(current_temp, current_hum)
        writeLog(rtc,new_temp,new_hum)
        utime.sleep_ms(1000)

    #if usr_pressed:
        #read_sensors()
        #usr_pressed = False
    #if lcd.is_touched():
        #read_sensors()