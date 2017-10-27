import time 
import serial 
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)


Tag1 = str('0E0006989A0A') 
PortRF = serial.Serial('/dev/ttyS0',9600) 
while True:
    ID = ""
    read_byte = PortRF.read()
    if read_byte=="\x02":
        for Counter in range(12):
            read_byte=PortRF.read()
            ID = ID + str(read_byte)
            print hex(ord( read_byte))
        print ID
        if ID == Tag1:
            print "matched"
        else:
            GPIO.output(23,False)
            print "Access Denied"



