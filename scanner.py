
import RPi.GPIO as GPIO
import time
import serial
import os
import threading
import os.path
ser = ""
ID = ""
flag = False

def setup():

  GPIO.setmode(GPIO.BCM) # Numbers GPIOs by physical location
  os.system('amixer set PCM -- 100%')
  print "*************************** \nIniciando AUDIOTECA DIGITAL 1.0 \n"

def start():
	global flag
        global ID
 	while True:
         if flag:
	      flag = False
              file = 'aplay ' + ID + '.wav'
              ID = ""
              os.system(file)


def scan ():
	global flag
        global ID
	key = "0E0006989A0A"
	while True:
	    ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.20)
	    read_byte = ser.read()
            if read_byte=="\x02":
              os.system('killall -9 aplay')
	      flag = False
              for i in range(12):
                read_byte = ser.read()
                ID = ID + str(read_byte)
              print "Code: "+ ID
              ser.close()
	      if (ID == key):
	        record()
		ID = ""
	      if (os.path.isfile(ID + '.wav')):
		flag = True
	      else:
                ID = ""
              time.sleep(0.8)

def destroy():
   print ""

def record():
	print "recording"

if __name__ == '__main__': # Program start from here
  setup()
  try:
    sc = threading.Thread(target=scan, )
    sc.start()
    start()
  except Exception as e:
   print (e)

