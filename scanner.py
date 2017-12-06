
import RPi.GPIO as GPIO
import time
import serial
import os
import os.path
ser = ""

def setup():

  GPIO.setmode(GPIO.BCM) # Numbers GPIOs by physical location
  os.system('amixer set PCM -- 100%')
  print "*************************** \nIniciando AUDIOTECA DIGITAL 1.0 \n"

def start():
  Tag1 = str('0E0006989A0A')

  while True:
    os.system("killall -9 aplay");
    ser = serial.Serial('/dev/ttyAMA0',9600)
    ID = ""
    read_byte = ser.read()
    if read_byte=="\x02":
	os.system('killall -9 aplay')
        for i in range(12):
            read_byte = ser.read()
            ID = ID + str(read_byte)
        print "Code: "+ ID
	ser.close()
        print (os.path.isfile(ID + '.wav'))

    if (os.path.isfile(ID + '.wav') ):
       file = 'aplay ' + ID + '.wav'
       os.system(file)
       print "Success"
       time.sleep(0.8)

def destroy():
   print ""

if __name__ == '__main__': # Program start from here
  setup()
  try:
    start()
  except Exception as e:
   print (e)

