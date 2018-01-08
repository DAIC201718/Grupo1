#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from datetime import datetime
import httplib, urllib
import Adafruit_CharLCD as LCD

lcd_rs        = 26
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_backlight = 4

lcd_columns = 16
lcd_rows    = 2


lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

Led = 17
BombaAgua = 27
EncenderLCD = 24 #salida a rele lcd
BotonLCD = 25 #boton para encender lcd
SensorNivelPrincipal = 18 #sensor acuario principal
SensorNivelAuxiliar = 23 #sensor acuario auxiliar fisicamente el 16
temperature = 0
temp = 0
bomb = 0
sensorPrincipal = 0
sensorAuxiliar = 0

def setup():
        GPIO.setup(Led, GPIO.OUT)
        GPIO.setup(BombaAgua, GPIO.OUT)   # Set BombaAgua mode is output
        GPIO.setup(EncenderLCD, GPIO.OUT)
        GPIO.setup(SensorNivelPrincipal, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set SensorNivel mode is input, and pull up to high level(3.3V)
        GPIO.setup(SensorNivelAuxiliar, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BotonLCD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(EncenderLCD, GPIO.HIGH)
        GPIO.output(Led, GPIO.HIGH)
        GPIO.output(BombaAgua, GPIO.HIGH) # Set BombaAgua  high(+3.3V) to off pump

def aguaBajaAuxiliar():
    
    lcd.clear()
    GPIO.output(EncenderLCD, False)
    time.sleep(2)
    lcd.message('Nivel bajo agua\nacuario auxiliar')
    time.sleep(10)
    lcd.clear
    time.sleep(10)
    GPIO.output(EncenderLCD, True)

def autoRelleno():
    
    if GPIO.input(SensorNivelPrincipal) and not GPIO.input(SensorNivelAuxiliar):
            GPIO.output(BombaAgua, GPIO.HIGH)
            #print ('Bomba apagada')
            aguaBajaAuxiliar()

    elif GPIO.input(SensorNivelPrincipal) and GPIO.input(SensorNivelAuxiliar):
            GPIO.output(BombaAgua, GPIO.HIGH)
            GPIO.output(Led, True)
            #print ('Bomba apagada')
            time.sleep(1)
    
    elif not GPIO.input(SensorNivelPrincipal) and not GPIO.input(SensorNivelAuxiliar):
            GPIO.output(BombaAgua, GPIO.HIGH)
            #print ('Bomba apagada')
            lcd.clear()
            time.sleep(5)
            aguaBajaAuxiliar()

    else:
            GPIO.output(BombaAgua, False)
            GPIO.output(Led, False)
            #print ('Bomba encendida')
            time.sleep(1)
            GPIO.output(Led, True)
            time.sleep(1)
            if not GPIO.input(SensorNivelAuxiliar):
                autoRelleno()

def botonLCD():
    
        lcd.clear()
        GPIO.output(EncenderLCD, False)
        temp = temperatura()
        lcd.message('Temperatura:\n %s ' % temp)
        time.sleep(10)
        lcd.clear()
        time.sleep(10)
        GPIO.output(EncenderLCD, True)


def temperatura():
        tempfile = open("/sys/bus/w1/devices/28-0416b116e1ff/w1_slave")
        thetext = tempfile.read() 
        tempfile.close()
        tempdata = thetext.split("\n")[1].split(" ")[9]
        temperature = float(tempdata[2:])
        temperature = temperature / 1000
        if (temperature > 2 and temperature < 30):
            return temperature
            print ('Temperatura:\n %s' % temperature)


def uploadData():
    
    temp = 0
    temp = temperatura()
    
    if GPIO.input(SensorNivelPrincipal) and (temp > 2 and temp < 30):
        bomb = 0
        params = urllib.urlencode({'field1': temp,'field2': bomb,'key': '96UXBAI57M2ATT9Y'})
    
    else:
        bomb = 1
        params = urllib.urlencode({'field2': bomb,'key': '96UXBAI57M2ATT9Y'})
    
    
    params = urllib.urlencode({'field1': temp,'field2': bomb,'key': '96UXBAI57M2ATT9Y'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print ('Temperatura: %s' % temp)
        if (bomb == 1):
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
        lcd.clear()
        GPIO.cleanup()    

if __name__ == '__main__':     # Program start from here
        setup()
        lcd.clear()
        try:
            while 1:
                autoRelleno()
                temperatura()
                uploadData()
                lcd.clear()
                time.sleep(2)
                if not GPIO.input(BotonLCD):
                    botonLCD()

        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                destroy()


