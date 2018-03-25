# main.py -- put your code here!
from change_colour import hdc_temp, hdc_hum,  print_to_display
import pyb
import utime
import lcd160cr
lcd = lcd160cr.LCD160CR('X')
uart = pyb.UART('XA', 115200)
pyb.repl_uart(uart)
sw = pyb.Switch()
rtc = pyb.RTC()

usr_pressed = False

def usr_pressed_check():
    global usr_pressed
    usr_pressed = True

sw.callback(usr_pressed_check)

def writeLog(rtc, temp, hum):
    """Append a line with the current timestamp to the log file"""
    datetime=rtc.datetime()
    timestamp = ("%04d-%02d-%02d %02d:%02d:%02d" % (datetime[0],
    datetime[1], datetime[2], datetime[4], datetime[5], datetime[6]))
    logline = ("%s %s %s" % (timestamp, temp, hum))
    #print(logline)
    try:
        with open("/sd/logdata.txt", "a") as f:
            f.write("%s\n" % logline)
            f.close()
            pyb.sync()
    except:
        pass
    #try:
        #with open("/flash/logdata.txt", "a") as f:
           # f.write("%s\n" % logline)
           # f.close()
           # pyb.sync()

    #except OSError as error:
        #print("Error: can not write to SD card. %s" % error)


while True:
    #check_read_out()
    #pyb.delay(1000)
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
        utime.sleep_ms(100)

    #if usr_pressed:
        #read_sensors()
        #usr_pressed = False
    #if lcd.is_touched():
        #read_sensors()