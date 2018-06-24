#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

//importamos las librerías necesarias
import tweepy  
from subprocess import call  
from datetime import datetime  

//cogemos la hora actual y la guardamos en la variable i
i = datetime.now()              

// aqui cogemos la variable i y la convertimos a string para que la fecha tenga el formato que hay dentro del paréntesis
now = i.strftime('%Y%m%d-%H%M%S')  

//creamos la variable photo_name para que concatene la variable now con ".jpg", así componemos el nombre
photo_name = now + '.jpg'  

//guardamos en la variable cmd un storing que será el comando que le pasaremos al método call para que lo ejecute en el shell. raspistill es un método de raspbian para hacer fotos al que le indicamos el formato de la foto, con -w el ancho de la foto, -h es el alto y con -0 le indicamos el directorio con el nombre que tendrá la imagen -vf es vertical flip y -hf es horizontal flip, hay que hacerlo porque la cámara esta girada
cmd = 'raspistill -t 500 -w 1024 -h 768 -vf -hf -o /home/pi/' + photo_name

//ejecutamos el comando en el shell
call ([cmd], shell=True)   
    
//cada sensor en raspbian crear un fichero del que leemos su valor, aquí lo que hacemos es leer el sensor de temperatura para ponerlo en el tweet
guardamos el fichero del sensor en un fichero temporal
tempfile = open("/sys/bus/w1/devices/28-0416b116e1ff/w1_slave")

//leemos y guardamos el contenido en otra variable
thetext = tempfile.read()

//cerramos el fichero
tempfile.close()

//lo parseamos
tempdata = thetext.split("\n")[1].split(" ")[9]

//lo pasamos de string a float 
temperature = float(tempdata[2:])
temperature = temperature / 1000

 
# Consumer keys and access tokens, used for OAuth  
consumer_key = 'x2INWyStWy1PuE6yzReaNV0m4'
consumer_secret = 'SPZwsRZdb2SITLwDM72raECVo3mZErnJUMgfOjsmjSTAQmSqQd'
access_token = '947786667846402048-lDyVbdYjcLOk2QjKMTN7I4v36eRm9Lv'
access_token_secret = 'SYukMDyfFDU80dWEk6Cupi1QFhgHueAXYgVE03iTXVzR6'
  
# OAuth process, using the keys and tokens  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  
   
# Creation of the actual interface, using authentication  
api = tweepy.API(auth)  
  
//mandamos el tweet que contendrá la imagen y un texto que pondrá "Aquarium temperature:" y la temperatura 
photo_path = '/home/pi/' + photo_name
status = 'Aquarium temperature: %s' % temperature + 'ºC ' + i.strftime('%Y/%m/%d %H:%M:%S')
api.update_with_media(photo_path, status=status)

//borrar es un comando de shell de tipo string que le pasamos al método call para que lo ejecute en el shell
borrar = 'rm /home/pi/*.jpg'
call([borrar], shell = True)
