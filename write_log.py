import pyb

def writeLog(rtc, temp, hum):
    """Append a line with the current timestamp to the log file"""
    datetime=rtc.datetime()
    timestamp = ("%04d-%02d-%02d %02d:%02d:%02d" % (datetime[0],
    datetime[1], datetime[2], datetime[4], datetime[5], datetime[6]))
    logline = ("%s %s %s" % (timestamp, temp, hum))
    #print(logline)
    try:
        with open("logdata.txt", "a") as f:
            f.write("%s\n" % logline)
            f.close()
            pyb.sync()
    except:
        pass
    try:
        with open("/flash/logdata.txt", "a") as f:
            f.write("%s\n" % logline)
            f.close()
            pyb.sync()

    except OSError as error:
        print("Error: can not write to SD card. %s" % error)