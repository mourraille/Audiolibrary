import RPi.GPIO as GPIO
import time
import serial
ser = ""

def setup():

  GPIO.setmode(GPIO.BCM) # Numbers GPIOs by physical location
  print "*************************** \nIniciando AUDIOTECA DIGITAL 1.0 \n"

def start():
  Tag1 = str('0E0006989A0A')

  while True:
    ser = serial.Serial('/dev/ttyAMA0',9600,timeout=0.20)
    ID = ""
    read_byte = ser.read()
    if read_byte=="\x02":
        for i in range(12):
            read_byte = ser.read()
            ID = ID + str(read_byte)
        print "Code: "+ ID
	print "Titulo: Logica Digital y Diseno de Computadores"
	ser.close()
	time.sleep(1.2)

def destroy():
   print ""

if __name__ == '__main__': # Program start from here
  setup()
  try:
    start()
  except Exception as e:
   print (e)

