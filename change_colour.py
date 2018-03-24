import machine
try:
    import esp
    esp.osdebug(None)
    i2c = machine.I2C(sda=machine.Pin(4), scl=machine.Pin(5))
except:
    pass
try:
    import pyb
    i2c = machine.I2C(sda=machine.Pin('Y10'), scl=machine.Pin('Y9'), freq=400000)
except:
    pass

import lcd160cr
lcd = lcd160cr.LCD160CR('X')

colours = [(255,0,0),(255, 140, 26),(255, 255, 0),(0, 230, 0),(0, 255, 255),(0, 0, 255)]
temp_levels = [32,29,26,23,20,17]
humidity_levels = [80, 70, 60, 50, 40,20]

dt = 20
b1 = bytearray(1)
b2 = bytearray(2)

def hdc1080_read(a=0):
    b1[0] = a
    i2c.writeto(64, b1)
    pyb.delay(dt)
    i2c.readfrom_into(64, b2)
    #return '%02x%02x' % (b[0], b[1])
    return (b2[0] << 8) | b2[1]

#calculating temperature
def hdc_temp():
    t = hdc1080_read(0)
    return (t / 0x10000)*165-40

#calculating humidity
def hdc_hum():
    t = hdc1080_read(1)
    return (t / 0x10000)*100

def calculate_color(value, levels):
    for i in range(len(levels)):
        if value > levels[i]:
            return i

def print_to_display(temp, humidity):
    lcd.erase()
    lcd.set_orient(lcd160cr.PORTRAIT)
    lcd.set_pos(20, 20)
    lcd.set_text_color(lcd.rgb(*colours[calculate_color(temp, temp_levels)]), lcd.rgb(0, 0, 0))
    lcd.set_font(1, 0, 0, 0, scroll=1)
    lcd.write("Temperature(°C)")
    lcd.set_pos(50, 50)
    lcd.set_font(1, 0, 0, 0, 0)
    lcd.write("%.2f" % (temp))
    lcd.set_text_color(lcd.rgb(*colours[calculate_color(humidity, humidity_levels)]), lcd.rgb(0, 0, 0)) # star unpacks the colour tuple into the rgb
    lcd.set_pos(30, 100)
    lcd.set_font(1, 0, 0, 0, scroll=1)
    lcd.write("Humidity(%)")
    lcd.set_pos(50, 130)
    lcd.set_font(1, 0, 0, 0, 0)
    lcd.write("%.2f" % (humidity))
   #print("Both sensors read at once:    %.2f  %.2f" % hdc.temp_hum())
   #print("Battery low: %s" % (hdc.battery_low()))

def check_read_out():
    current_temp = hdc_temp()
    current_hum = hdc_hum()
    while True:
        new_temp = hdc_temp()
        new_hum = hdc_hum()
        #if new_temp > current_temp + 2 or new_temp < current_temp -2 or new_humidity > current_humidity + 10 or new_humidity < current_humidity-10:
        if new_temp > current_temp + 1 or new_temp < current_temp -1 :
            print_to_display(current_temp, current_hum)
            current_temp = new_temp
            current_hum = new_hum
        pyb.delay(1000)

