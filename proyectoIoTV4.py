#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from datetime import datetime
import httplib, urllib

Led = 11
BombaAgua = 13
SensorNivelPrincipal = 12 #sensor acuario principal
temperature = 0
LuzLED = 0
bomba = 0

def setup():
        GPIO.setmode(GPIO.BOARD)      # Numbers GPIOs by physical location
        GPIO.setup(Led, GPIO.OUT)
        GPIO.setup(BombaAgua, GPIO.OUT)   # Set BombaAgua mode is output
        GPIO.setup(SensorNivelPrincipal, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set SensorNivel mode is input, and pull up to high level(3.3V)
        GPIO.output(Led, GPIO.HIGH)
        GPIO.output(BombaAgua, GPIO.HIGH) # Set BombaAgua  high(+3.3V) to off led

def swLed():
	
    if GPIO.input(SensorNivelPrincipal):
                        GPIO.output(BombaAgua, True)
                        GPIO.output(Led, True)
                        bomba =  0
                        LuzLED = 0
			time.sleep(1)
    else:
                        while not GPIO.input(SensorNivelPrincipal):
        	            GPIO.output(BombaAgua, False)
			    GPIO.output(Led, False)
                            bomba = 1
			    time.sleep(1)
                            GPIO.output(Led, True)
                            time.sleep(1)
                            LuzLED = 1

def temperatura():
        tempfile = open("/sys/bus/w1/devices/28-0416b116e1ff/w1_slave")
        thetext = tempfile.read() 
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        temperature = float(tempdata[2:])
        temperature = temperature / 1000
        # print ('Temperatura: %s' % temperature)
        return temperature

def uploadData():
    
    if GPIO.input(SensorNivelPrincipal):
        bomba = 0
        temp = temperatura()
    
    else:
        bomba = 1
    
    
    params = urllib.urlencode({'field1': temp,'filed2': bomba,'key': '96UXBAI57M2ATT9Y'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print ('Temperatura: %s' % temp)
        if (bomba == 1):
            print ('Bomba encendida')
        else:
            print ('Bomba apagada')
        print '\n'
        print strftime("%a, %d %b %Y %H:%M:%S", localtime())
        print response.status, response.reason
        data = response.read()
        conn.close()
    except:
        print "connection failed"


def destroy():
        GPIO.output(BombaAgua, GPIO.HIGH)     # pump off
        GPIO.cleanup()    

if __name__ == '__main__':     # Program start from here
        setup()
        try:
            while 1:
                swLed()
                temperatura()
                uploadData()
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                destroy()


