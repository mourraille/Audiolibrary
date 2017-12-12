import RPi.GPIO as GPIO
import time
import serial
import os
import threading
import os.path
ser = ""
ID = ""
flag = False
green = 23
blue = 21
red = 22
scannable = True
wasrecording = False
def setup():

  GPIO.setmode(GPIO.BCM) # Numbers GPIOs by physical location
  GPIO.setwarnings(False)
  GPIO.setup(green, GPIO.OUT)
  GPIO.setup(red, GPIO.OUT)
  GPIO.setup(blue, GPIO.OUT)
  GPIO.output(red, 0)
  GPIO.output(green, 0)
  GPIO.output(blue, 1)

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
	global wasrecording
	global scannable
	global flag
        global ID
	key = "0E0006989A0A"
	while True and scannable:
	    ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.20)
	    read_byte = ser.read()
            if read_byte=="\x02":
              GPIO.output(green, 1)
	      os.system('killall -9 aplay')
	      flag = False
              for i in range(12):
                read_byte = ser.read()
                ID = ID + str(read_byte)
              print "Code: "+ ID
              ser.close()
	      if (ID == key):
		if (wasrecording):
		   os.system('killall -9 arecord')
                   wasrecording = False
 		   GPIO.output(red,0)
		GPIO.output(green,0)
                GPIO.output(red,1)
	        record()
		ID = ""
	      if (os.path.isfile(ID + '.wav')):
		flag = True
                GPIO.output(green,0)
	      else:
                ID = ""
              GPIO.output(green,0)

def destroy():
   print ""

def record():
            key = "0E0006989A0A"
	    name = ""
            global scannable
	    global wasrecording
	    scannable = False
	    while not scannable:
             ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.20)
             read_byte = ser.read()
             if read_byte=="\x02":
               for i in range(12):
                 read_byte = ser.read()
                 name = name + str(read_byte)
               print "name: "+ name
               ser.close()
	       scannable = True
               if (name != key and not os.path.isfile(name + '.wav')):
	         print ("recording")
	         wasrecording = True
	         os.system ('arecord --device=hw:1,0 --format S16_LE --rate 44100 ' + name + '.wav' + ' -V mono')
	         print "recording"
 	         GPIO.output(red,0)
            name = ""
            GPIO.output(red,0)
	    return

if __name__ == '__main__':
  setup()
  try:
    sc = threading.Thread(target=scan, )
    sc.start()
    GPIO.output(red,1)
    time.sleep(0.5)
    GPIO.output(red,0)
    start()
  except Exception as e:
   GPIO.cleanup()
   print (e)

